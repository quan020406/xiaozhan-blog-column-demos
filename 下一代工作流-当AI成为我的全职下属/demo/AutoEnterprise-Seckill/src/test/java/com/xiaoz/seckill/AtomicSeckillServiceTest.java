package com.xiaoz.seckill;

import com.xiaoz.seckill.mapper.SeckillOrderMapper;
import com.xiaoz.seckill.mapper.SeckillProductMapper;
import com.xiaoz.seckill.service.AtomicSeckillService;
import com.xiaoz.seckill.service.SeckillResult;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class AtomicSeckillServiceTest {
    private static final long PRODUCT_ID = 1L;
    private static final int STOCK = 100;

    @Autowired
    private AtomicSeckillService service;
    @Autowired
    private SeckillProductMapper productMapper;
    @Autowired
    private SeckillOrderMapper orderMapper;

    @BeforeEach
    void reset() {
        orderMapper.deleteByProductId(PRODUCT_ID);
        productMapper.resetStock(PRODUCT_ID, STOCK);
    }

    @Test
    void shouldNeverCreateMoreOrdersThanStock() throws Exception {
        int requests = 300;
        ExecutorService pool = Executors.newFixedThreadPool(32);
        CountDownLatch start = new CountDownLatch(1);
        List<Future<SeckillResult>> futures = new ArrayList<>();

        for (long userId = 1; userId <= requests; userId++) {
            long currentUser = userId;
            futures.add(pool.submit(() -> {
                start.await();
                return service.execute(currentUser, PRODUCT_ID);
            }));
        }

        start.countDown();
        long successCount = 0;
        for (Future<SeckillResult> future : futures) {
            if (future.get(10, TimeUnit.SECONDS).success()) {
                successCount++;
            }
        }
        pool.shutdown();
        assertThat(pool.awaitTermination(10, TimeUnit.SECONDS)).isTrue();

        assertThat(successCount).isEqualTo(STOCK);
        assertThat(orderMapper.countByProductId(PRODUCT_ID)).isEqualTo(STOCK);
        assertThat(productMapper.selectById(PRODUCT_ID).getStock()).isZero();
    }
}

