# Spring Boot 高并发秒杀实战：AI Agent 写出 `@Transactional`，为什么仍然超卖？

![AI Agent 秒杀超卖事故封面](../assets/images/article-01-overselling.png)

> **专栏**：《下一代工作流：当 AI 成为我的全职下属》第一期  
> **关键词**：Spring Boot、MyBatis-Plus、事务、并发安全、超卖、AI Agent  
> **配套代码**：`demo/AutoEnterprise-Seckill`

## 摘要

把“判断库存、扣减库存、创建订单”交给 AI Agent，它很容易生成一段看上去规范的 `@Transactional` 代码。然而事务只能保证一组数据库操作的原子提交，不能自动把“先查询、再修改”变成并发安全的库存扣减。

本文用一个可以直接运行的 Spring Boot 3 + MyBatis-Plus + H2 Demo，复现 500 个请求争抢 100 件库存时的超卖，并用数据库条件更新修复问题。重点不是嘲笑 AI，而是建立一条工程判断：**代码能编译、事务能提交，不等于业务约束在并发下成立。**

## 1. 实验环境与问题定义

本次实测环境：

| 项目 | 版本或参数 |
| --- | --- |
| JDK | 17.0.15 |
| Spring Boot | 3.5.15 |
| MyBatis-Plus | 3.5.15 |
| 数据库 | H2 内存库，MySQL 兼容模式 |
| 初始库存 | 100 |
| 请求数 | 500 |
| 并发线程 | 100 |

业务约束只有三条：

1. 库存不能小于 0。
2. 成功订单数不能超过初始库存。
3. 库存扣减与订单创建必须在同一事务中完成。

## 2. AI Agent 最容易生成的错误实现

下面的代码没有语法错误，也加了事务：

```java
@Transactional
public SeckillResult execute(Long userId, Long productId) {
    SeckillProduct product = productMapper.selectById(productId);
    if (product == null || product.getStock() <= 0) {
        return SeckillResult.soldOut("unsafe");
    }

    product.setStock(product.getStock() - 1);
    productMapper.updateById(product);
    SeckillOrder order = orderCreator.create(userId, productId, "unsafe");
    return SeckillResult.success(order.getId(), "unsafe");
}
```

单线程下，它的执行过程完全正确。问题出现在两个线程同时读到相同库存时：

```text
线程 A：读取 stock = 100
线程 B：读取 stock = 100
线程 A：写入 stock = 99
线程 B：写入 stock = 99
```

两笔订单已经创建，库存却只减少 1。这叫**丢失更新**。因此超卖不一定表现为负库存；它也可能表现为“订单数远大于售出库存，但库存值仍然看起来正常”。

![先查后改导致丢失更新](../assets/images/article-01-race-condition.png)

## 3. 真实压测结果

启动项目：

```powershell
cd demo\AutoEnterprise-Seckill
mvn.cmd spring-boot:run
```

命令要求当前终端中的 `java -version` 已指向 JDK 17 或更高版本，不在项目中记录任何本机 JDK 安装路径。

执行压测：

```powershell
python pipeline\run_stress_test.py `
  --base-url $env:SECKILL_BASE_URL `
  --mode unsafe `
  --concurrency 100 `
  --requests 500 `
  --stock 100
```

本机一次实测结果：

```json
{
  "mode": "unsafe",
  "requests": 500,
  "concurrency": 100,
  "initial_stock": 100,
  "success_responses": 500,
  "database_orders": 500,
  "remaining_stock": 49,
  "oversold": true
}
```

500 个请求全部拿到“秒杀成功”，数据库出现 500 条订单，但初始库存只有 100。更危险的是剩余库存仍为正数，单看库存字段甚至不容易发现事故。

> 吞吐量受机器、数据库连接池和后台进程影响。判断正确性的关键不是 QPS，而是 `订单数 <= 初始库存` 这一业务不变量。

### 3.1 如何判断实验复现成功

- `unsafe` 模式的 `database_orders` 大于 100，说明已复现超卖。
- `remaining_stock` 不一定为负数；丢失更新时它可能仍为正数。
- 如果本机并发较低未复现，可增加 `--requests`，但不要直接把结果当作生产容量数据。

## 4. 正确修复：把判断和扣减合并成一条 SQL

MyBatis-Plus Mapper 中增加条件更新：

```java
@Update("""
    UPDATE seckill_product
    SET stock = stock - 1, version = version + 1
    WHERE id = #{productId} AND stock > 0
    """)
int deductStockIfAvailable(@Param("productId") Long productId);
```

Service 只在影响行数为 1 时创建订单：

```java
@Transactional
public SeckillResult execute(Long userId, Long productId) {
    if (productMapper.deductStockIfAvailable(productId) != 1) {
        return SeckillResult.soldOut("atomic");
    }
    SeckillOrder order = orderCreator.create(userId, productId, "atomic");
    return SeckillResult.success(order.getId(), "atomic");
}
```

这条 SQL 将“库存大于 0 的判断”和“库存减 1”交给数据库原子执行。多个线程竞争时，最多只有 100 次更新成功。

同样参数再次压测：

```json
{
  "mode": "atomic",
  "requests": 500,
  "concurrency": 100,
  "initial_stock": 100,
  "success_responses": 100,
  "database_orders": 100,
  "remaining_stock": 0,
  "oversold": false
}
```

## 5. 为什么 `@Transactional` 没有失效？

事务没有失效。每个线程内部的“更新库存 + 插入订单”仍然一起提交或回滚。真正的问题是多个事务都基于旧库存做出了合法但互相冲突的决定。

需要区分两个概念：

- **事务原子性**：一个事务中的操作要么全部成功，要么全部失败。
- **并发业务正确性**：多个事务同时执行后，系统仍满足库存不超卖等业务不变量。

前者不能自动推导出后者。

## 6. 应该怎样给 AI 下发任务

不要只写“注意并发安全”，而要把可验证约束写进 Issue：

```text
库存初始值为 100，发起 300 个并发请求：
1. 成功响应必须恰好为 100；
2. 订单表必须恰好新增 100 行；
3. 最终库存必须为 0；
4. 禁止通过降低并发度、跳过测试或修改断言让 CI 通过。
```

AI 擅长实现目标，但目标必须被写成测试可以判断的条件。

## 7. 小结

这次事故给出了专栏的第一条原则：

> **不要审查 AI 写得像不像人，要审查它是否守住了业务不变量。**

下一期将解决另一个常见问题：项目越来越大后，为什么把整个仓库塞进上下文，反而会让 Agent 更容易改错文件。

### 适用边界

条件更新适合单商品库存这一类简单不变量。涉及多仓、预占库存、超时释放、消息最终一致性时，还需要库存流水、幂等键和补偿机制；本文 Demo 不代表完整电商生产方案。

---

**下一篇**：[基于 AST 的上下文治理：别把整个 Java 项目塞给 AI](02-ast-context-governance.md)

## 参考资料

- [Spring Boot System Requirements](https://docs.spring.io/spring-boot/system-requirements.html)
- [MyBatis-Plus Spring Boot 3 安装说明](https://baomidou.com/getting-started/install/)
