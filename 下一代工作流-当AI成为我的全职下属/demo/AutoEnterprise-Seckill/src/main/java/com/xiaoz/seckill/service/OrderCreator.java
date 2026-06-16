package com.xiaoz.seckill.service;

import com.xiaoz.seckill.domain.SeckillOrder;
import com.xiaoz.seckill.mapper.SeckillOrderMapper;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class OrderCreator {
    private final SeckillOrderMapper orderMapper;

    public OrderCreator(SeckillOrderMapper orderMapper) {
        this.orderMapper = orderMapper;
    }

    public SeckillOrder create(Long userId, Long productId, String mode) {
        SeckillOrder order = new SeckillOrder();
        order.setUserId(userId);
        order.setProductId(productId);
        order.setMode(mode);
        order.setCreatedAt(LocalDateTime.now());
        orderMapper.insert(order);
        return order;
    }
}

