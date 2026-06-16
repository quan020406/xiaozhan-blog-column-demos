package com.xiaoz.seckill.service;

import com.xiaoz.seckill.domain.SeckillOrder;
import com.xiaoz.seckill.domain.SeckillProduct;
import com.xiaoz.seckill.mapper.SeckillProductMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UnsafeSeckillService {
    private final SeckillProductMapper productMapper;
    private final OrderCreator orderCreator;

    public UnsafeSeckillService(SeckillProductMapper productMapper, OrderCreator orderCreator) {
        this.productMapper = productMapper;
        this.orderCreator = orderCreator;
    }

    @Transactional
    public SeckillResult execute(Long userId, Long productId) {
        SeckillProduct product = productMapper.selectById(productId);
        if (product == null || product.getStock() <= 0) {
            return SeckillResult.soldOut("unsafe");
        }

        widenRaceWindow();
        product.setStock(product.getStock() - 1);
        productMapper.updateById(product);
        SeckillOrder order = orderCreator.create(userId, productId, "unsafe");
        return SeckillResult.success(order.getId(), "unsafe");
    }

    private void widenRaceWindow() {
        try {
            Thread.sleep(8);
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("线程被中断", exception);
        }
    }
}

