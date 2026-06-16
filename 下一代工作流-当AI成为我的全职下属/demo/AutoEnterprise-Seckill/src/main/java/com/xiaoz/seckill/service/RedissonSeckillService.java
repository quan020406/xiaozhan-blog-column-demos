package com.xiaoz.seckill.service;

import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Service
public class RedissonSeckillService {
    private final ObjectProvider<RedissonClient> redissonProvider;
    private final AtomicSeckillService atomicSeckillService;

    public RedissonSeckillService(ObjectProvider<RedissonClient> redissonProvider,
                                  AtomicSeckillService atomicSeckillService) {
        this.redissonProvider = redissonProvider;
        this.atomicSeckillService = atomicSeckillService;
    }

    public SeckillResult execute(Long userId, Long productId) {
        RedissonClient redisson = redissonProvider.getIfAvailable();
        if (redisson == null) {
            throw new RedisUnavailableException("Redisson 未启用，请使用 redis Profile 启动应用");
        }

        RLock lock = redisson.getLock("seckill:product:" + productId);
        boolean acquired = false;
        try {
            acquired = lock.tryLock(500, TimeUnit.MILLISECONDS);
            if (!acquired) {
                return new SeckillResult(false, null, "redisson", "系统繁忙，请重试");
            }
            SeckillResult result = atomicSeckillService.execute(userId, productId);
            return new SeckillResult(result.success(), result.orderId(), "redisson", result.message());
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("获取分布式锁时线程被中断", exception);
        } finally {
            if (acquired && lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}

