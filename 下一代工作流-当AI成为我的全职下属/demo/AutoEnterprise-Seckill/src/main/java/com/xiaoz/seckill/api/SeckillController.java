package com.xiaoz.seckill.api;

import com.xiaoz.seckill.service.AtomicSeckillService;
import com.xiaoz.seckill.service.RedissonSeckillService;
import com.xiaoz.seckill.service.SeckillResult;
import com.xiaoz.seckill.service.UnsafeSeckillService;
import jakarta.validation.constraints.Min;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
@RequestMapping("/api/seckill")
public class SeckillController {
    private final UnsafeSeckillService unsafeService;
    private final AtomicSeckillService atomicService;
    private final RedissonSeckillService redissonService;

    public SeckillController(UnsafeSeckillService unsafeService,
                             AtomicSeckillService atomicService,
                             RedissonSeckillService redissonService) {
        this.unsafeService = unsafeService;
        this.atomicService = atomicService;
        this.redissonService = redissonService;
    }

    @PostMapping("/unsafe")
    public SeckillResult unsafe(@RequestParam @Min(1) Long userId,
                                @RequestParam(defaultValue = "1") @Min(1) Long productId) {
        return unsafeService.execute(userId, productId);
    }

    @PostMapping("/atomic")
    public SeckillResult atomic(@RequestParam @Min(1) Long userId,
                                @RequestParam(defaultValue = "1") @Min(1) Long productId) {
        return atomicService.execute(userId, productId);
    }

    @PostMapping("/redisson")
    public SeckillResult redisson(@RequestParam @Min(1) Long userId,
                                  @RequestParam(defaultValue = "1") @Min(1) Long productId) {
        return redissonService.execute(userId, productId);
    }
}

