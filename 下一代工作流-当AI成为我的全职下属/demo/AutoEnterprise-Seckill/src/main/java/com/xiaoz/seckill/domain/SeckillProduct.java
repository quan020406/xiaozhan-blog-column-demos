package com.xiaoz.seckill.domain;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

@TableName("seckill_product")
public class SeckillProduct {
    @TableId
    private Long id;
    private String name;
    private Integer stock;
    private Integer version;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Integer getStock() { return stock; }
    public void setStock(Integer stock) { this.stock = stock; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

