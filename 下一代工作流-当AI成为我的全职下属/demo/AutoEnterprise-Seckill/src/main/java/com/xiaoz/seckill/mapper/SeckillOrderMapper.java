package com.xiaoz.seckill.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xiaoz.seckill.domain.SeckillOrder;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

public interface SeckillOrderMapper extends BaseMapper<SeckillOrder> {
    @Select("SELECT COUNT(*) FROM seckill_order WHERE product_id = #{productId}")
    long countByProductId(@Param("productId") Long productId);

    @Delete("DELETE FROM seckill_order WHERE product_id = #{productId}")
    int deleteByProductId(@Param("productId") Long productId);
}

