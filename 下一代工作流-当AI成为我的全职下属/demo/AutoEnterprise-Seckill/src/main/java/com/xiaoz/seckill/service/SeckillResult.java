package com.xiaoz.seckill.service;

public record SeckillResult(boolean success, Long orderId, String mode, String message) {
    public static SeckillResult success(Long orderId, String mode) {
        return new SeckillResult(true, orderId, mode, "秒杀成功");
    }

    public static SeckillResult soldOut(String mode) {
        return new SeckillResult(false, null, mode, "库存不足");
    }
}

