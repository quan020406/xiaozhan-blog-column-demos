# 贯穿项目素材区

这里存放《软件测试从入门到实战：用项目思维学测试》的贯穿项目设定。当前主线已确定为 **CampusHub 校园服务协作平台 + 内置 BookNest 图书借阅模块**；需求、测试用例、Bug 报告、自动化脚本和性能素材都围绕这一方案沉淀。

## 历史选型记录

| 方案 | 项目 | 适合方向 | 文件 |
| --- | --- | --- | --- |
| A | CampusHub 校园服务协作平台 | 已确定为主平台，覆盖账号、活动、场地、设备、通知、审核 | [option-a-campushub.md](./options/option-a-campushub.md) |
| C | BookNest 图书借阅与阅读社区 | 已并入 CampusHub，作为内置图书借阅模块 | [option-c-booknest.md](./options/option-c-booknest.md) |
| B | FitReserve 健身房预约与会员平台 | 历史备选，不作为当前主线 | [option-b-fitreserve.md](./options/option-b-fitreserve.md) |
| D | TaskFlow 团队任务协作平台 | 历史备选，不作为当前主线 | [option-d-taskflow.md](./options/option-d-taskflow.md) |
| E | ClinicLite 轻量门诊预约平台 | 历史备选，不作为当前主线 | [option-e-cliniclite.md](./options/option-e-cliniclite.md) |

详细对比见：[../docs/00-贯穿项目方案.md](../docs/00-贯穿项目方案.md)。

## 后续素材沉淀方向

- `requirements/`：按模块沉淀需求说明。
- `test-cases/`：存放手工测试用例模板。
- `bug-reports/`：存放缺陷报告示例。
- `automation/`：后续如需要，可加入 Selenium 或接口自动化示例。
- `performance/`：后续如需要，可加入 JMeter 脚本说明。

后续素材只使用虚拟账号、虚拟学校场景、示例接口和可复现本地配置，不放真实个人信息、真实学校数据、真实接口地址或本机环境配置。
