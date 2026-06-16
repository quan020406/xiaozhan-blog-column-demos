package com.xiaoz.seckill.service;

import com.xiaoz.seckill.domain.SeckillOrder;
import com.xiaoz.seckill.mapper.SeckillProductMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AtomicSeckillService {
    private final SeckillProductMapper productMapper;
    private final OrderCreator orderCreator;

    public AtomicSeckillService(SeckillProductMapper productMapper, OrderCreator orderCreator) {
        this.productMapper = productMapper;
        this.orderCreator = orderCreator;
    }

    @Transactional
    public SeckillResult execute(Long userId, Long productId) {
        if (productMapper.deductStockIfAvailable(productId) != 1) {
            return SeckillResult.soldOut("atomic");
        }
        SeckillOrder order = orderCreator.create(userId, productId, "atomic");
        return SeckillResult.success(order.getId(), "atomic");
    }
}

