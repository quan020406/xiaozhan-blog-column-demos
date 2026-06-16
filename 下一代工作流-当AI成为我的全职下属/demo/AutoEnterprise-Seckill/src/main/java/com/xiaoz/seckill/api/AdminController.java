package com.xiaoz.seckill.api;

import com.xiaoz.seckill.domain.SeckillProduct;
import com.xiaoz.seckill.mapper.SeckillOrderMapper;
import com.xiaoz.seckill.mapper.SeckillProductMapper;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.Map;

@Validated
@RestController
@RequestMapping("/api")
public class AdminController {
    private static final long PRODUCT_ID = 1L;

    private final SeckillProductMapper productMapper;
    private final SeckillOrderMapper orderMapper;

    public AdminController(SeckillProductMapper productMapper, SeckillOrderMapper orderMapper) {
        this.productMapper = productMapper;
        this.orderMapper = orderMapper;
    }

    @GetMapping("/products/{productId}")
    public Map<String, Object> status(@PathVariable Long productId) {
        SeckillProduct product = productMapper.selectById(productId);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("product", product);
        result.put("orderCount", orderMapper.countByProductId(productId));
        return result;
    }

    @Transactional
    @PostMapping("/admin/reset")
    public Map<String, Object> reset(@RequestParam(defaultValue = "100") @Min(1) @Max(100000) int stock) {
        orderMapper.deleteByProductId(PRODUCT_ID);
        productMapper.resetStock(PRODUCT_ID, stock);
        return status(PRODUCT_ID);
    }
}

