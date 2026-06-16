package com.xiaoz.seckill;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@MapperScan("com.xiaoz.seckill.mapper")
@SpringBootApplication
public class AutoEnterpriseSeckillApplication {
    public static void main(String[] args) {
        SpringApplication.run(AutoEnterpriseSeckillApplication.class, args);
    }
}

