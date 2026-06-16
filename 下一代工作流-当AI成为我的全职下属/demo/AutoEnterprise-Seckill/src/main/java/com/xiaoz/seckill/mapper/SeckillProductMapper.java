package com.xiaoz.seckill.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xiaoz.seckill.domain.SeckillProduct;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Update;

public interface SeckillProductMapper extends BaseMapper<SeckillProduct> {
    @Update("UPDATE seckill_product SET stock = stock - 1, version = version + 1 " +
            "WHERE id = #{productId} AND stock > 0")
    int deductStockIfAvailable(@Param("productId") Long productId);

    @Update("UPDATE seckill_product SET stock = #{stock}, version = 0 WHERE id = #{productId}")
    int resetStock(@Param("productId") Long productId, @Param("stock") int stock);
}

