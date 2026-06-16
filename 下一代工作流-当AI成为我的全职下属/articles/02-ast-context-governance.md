# AI 编程上下文治理实战：用 AST 依赖裁剪，别再把整个 Java 项目塞给 Agent

![AI Agent 上下文治理封面](../assets/images/article-02-context.png)

> **专栏**：《下一代工作流：当 AI 成为我的全职下属》第二期  
> **关键词**：AI Agent、上下文工程、AST、Java 依赖分析、Token 优化  
> **配套代码**：`demo/AutoEnterprise-Seckill/ai_firm/context_pruner.py`

## 摘要

Agent 修改一个 Service 时，真正需要的通常不是整个仓库，而是目标类、直接依赖和少量接口契约。无差别投喂代码会放大 Token 成本，也会把无关 Controller、历史实现和测试夹具带入决策空间。

本文实现一个零第三方依赖的 Java 上下文裁剪器：从目标文件出发解析 `import`，按最大深度构建依赖包，并输出可审计的 JSON。它不是完整 Java 编译器，却足以说明上下文治理的核心方法：**先确定任务边界，再按依赖关系提供证据。**

## 0. 读者、环境与成功标准

适合已经了解 Java 包结构、希望控制 AI 编程上下文的开发者。本文使用 Python 3.12.5 实测，脚本只依赖标准库；Python 3.11+ 均可运行。

成功标准：指定一个 Java Service 后，工具能输出目标类及项目内依赖，且不会读取源码根目录外的文件。

## 1. “上下文越多越好”为什么是错的

大型项目中常见三类干扰：

1. 同名类或旧版本实现让 Agent 选择错误参考。
2. 与任务无关的配置、Controller、DTO 占用上下文窗口。
3. 关键约束被淹没在大量代码中，出现 Lost in the Middle。

如果任务是修改 `AtomicSeckillService`，最小上下文通常包括：

- `AtomicSeckillService.java`
- `SeckillProductMapper.java`
- `OrderCreator.java`
- `SeckillResult.java`

不需要同时发送管理接口、H2 Console 配置和全部测试日志。

## 2. 上下文裁剪器的实现

核心思路是广度优先遍历：

```python
IMPORT_PATTERN = re.compile(r"^import\s+([\w.]+);", re.MULTILINE)

queue = deque([(target, 0)])
while queue:
    path, depth = queue.popleft()
    content = path.read_text(encoding="utf-8")
    files.append(build_context_item(path, depth, content))

    if depth >= max_depth:
        continue

    for imported in IMPORT_PATTERN.findall(content):
        candidate = source_root / (imported.replace(".", "/") + ".java")
        if candidate.exists():
            queue.append((candidate, depth + 1))
```

完整实现还做了三件事：

- 使用 `resolve()` 约束目标必须位于源码根目录内。
- 使用 `visited` 防止循环依赖导致重复读取。
- 输出文件数、字符数和依赖深度，便于审计上下文规模。

![从目标类到有限依赖图](../assets/images/article-02-dependency-graph.png)

## 3. 在 Demo 中运行

```powershell
cd demo\AutoEnterprise-Seckill
python ai_firm\context_pruner.py `
  --target src\main\java\com\xiaoz\seckill\service\AtomicSeckillService.java `
  --max-depth 2 `
  --output reports\atomic-context.json
```

当前工程实测输出：

```json
{
  "target": "com/xiaoz/seckill/service/AtomicSeckillService.java",
  "file_count": 4,
  "character_count": 3427
}
```

裁剪器只带回目标 Service、Mapper、订单创建器和结果对象。这个结果比“把 `src/main/java` 全部压缩后发送”更便宜，也更容易审查。

验证输出中的 `files` 数组，应能看到以下四类文件：目标 Service、库存 Mapper、`OrderCreator` 和 `SeckillResult`。如果缺少实际被调用的类型，说明当前解析策略不适用于该项目，不能直接把上下文交给 Agent。

## 4. 为什么这里只用正则，而不是完整 AST？

示例工具使用正则解析标准 `import`，优点是无需安装 JavaParser 或 tree-sitter，读者下载项目即可运行。它适合演示和约束明确的普通 Java 工程。

以下情况应升级为真正的 AST 或语言服务：

- 静态导入和通配符导入很多。
- 使用内部类、反射或注解生成代码。
- 需要分析方法调用图，而不只是文件依赖图。
- 多模块工程存在相同包名或复杂源码集。

生产方案可将 JavaParser、Spoon、Eclipse JDT 或 IDE Language Server 的符号索引作为依赖数据源。

## 5. 上下文包不应只有代码

高质量任务包至少包含四部分：

```text
task-bundle/
├── issue.md              # 目标和验收标准
├── context.json          # 被选择的文件、原因和规模
├── source/               # 裁剪后的源码
└── constraints.md        # 不允许修改的路径和行为
```

对于秒杀任务，`constraints.md` 应明确：

- 不允许修改 `pipeline/`。
- 不允许跳过并发测试。
- 不允许新增未经说明的依赖。
- 订单数、库存值和成功响应必须一致。

## 6. 怎样评价裁剪质量

不要只看 Token 减少比例。更重要的是三项指标：

| 指标 | 问题 |
| --- | --- |
| 召回率 | 关键依赖是否被遗漏？ |
| 噪声率 | 无关文件是否仍然过多？ |
| 可解释性 | 能否说明每个文件为什么进入上下文？ |

最好的上下文不是最小，而是**足够完成任务且每一项都能解释**。

## 7. 小结

上下文治理把 Agent 的“记忆问题”转化为工程问题：依赖分析、权限边界和任务包版本化。它的价值不仅是省 Token，更是减少错误修改的自由度。

下一期将继续收紧边界：当 Agent 为了让流水线变绿而修改测试时，怎样用静态审计在提交阶段直接拦截。

### 风险与适用边界

- 输出 JSON 含源码正文，上传外部模型前应执行密钥和敏感信息扫描。
- 本工具不会解析反射、XML Mapper、注解处理器生成类型和运行时依赖。
- 生产环境应记录文件哈希，避免裁剪后源码变化导致上下文与待修改版本不一致。

---

**上一篇**：[Spring Boot 高并发秒杀：`@Transactional` 为什么仍然超卖](01-agent-overselling-incident.md)  
**下一篇**：[AI Agent 防作弊 CI：检测万能断言、跳过测试与空 catch](03-agent-cheat-detection.md)

## 参考资料

- [Python pathlib 官方文档](https://docs.python.org/3/library/pathlib.html)
- [Java Language Specification：Packages and Modules](https://docs.oracle.com/javase/specs/jls/se25/html/jls-7.html)
