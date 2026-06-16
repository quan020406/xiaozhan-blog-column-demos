package com.xiaoz.seckill.config;

import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;

@Configuration
public class RedissonConfig {
    @Bean(destroyMethod = "shutdown")
    @ConditionalOnProperty(name = "app.redis.enabled", havingValue = "true")
    RedissonClient redissonClient(@Value("${app.redis.address}") String address, Environment environment) {
        Config config = new Config();
        var singleServerConfig = config.useSingleServer().setAddress(address);
        String password = environment.getProperty("REDIS_PASSWORD");
        if (password != null && !password.isBlank()) {
            singleServerConfig.setPassword(password);
        }
        return Redisson.create(config);
    }
}
