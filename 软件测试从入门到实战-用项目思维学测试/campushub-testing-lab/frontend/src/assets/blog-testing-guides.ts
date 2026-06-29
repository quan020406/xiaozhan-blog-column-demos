import article01 from '../../../../articles/01-软件测试到底在测什么.md?raw'
import article02 from '../../../../articles/02-测试岗位与能力路线.md?raw'
import article03 from '../../../../articles/03-需求不是一句话-测试如何读懂需求.md?raw'
import article04 from '../../../../articles/04-软件生命周期里测试应该什么时候介入.md?raw'
import article05 from '../../../../articles/05-V模型和W模型-为什么测试不能只等提测.md?raw'
import article06 from '../../../../articles/06-一个Bug是怎么诞生流转和关闭的.md?raw'
import article07 from '../../../../articles/07-和开发争Bug时测试应该怎么沟通.md?raw'
import article08 from '../../../../articles/08-测试用例是什么-为什么不能只靠随便点点.md?raw'

export type BlogTestingGuide = {
  id: number
  title: string
  status: '已成稿' | '规划中'
  module: string
  testingTheme: string
  readerGoal: string
  originalMarkdown: string
  blogUrl?: string
  testFocus: string[]
  operationSteps: string[]
  assets: string[]
  acceptance: string[]
}

function plannedOriginal(id: number, title: string, module: string, testingTheme: string) {
  return `# ${String(id).padStart(2, '0')}-${title}

> 本期正式正文尚未放入 articles/ 目录。当前展示的是专栏细纲中的规划稿，用于告诉读者本期会围绕 ${module} 讲解 ${testingTheme}。

## 本期要解决的问题

读者打开 CampusHub Testing Lab 后，不应该只知道“页面能点”，而要知道这一期文章要验证哪类质量风险、该打开哪个模块、该观察哪些数据和证据。

## 建议阅读方式

先看右侧“本期测试指南”，再进入“测试执行台”按步骤操作。执行完成后，到“证据资产库”查看对应的用例、缺陷、接口、自动化或性能素材。
`
}

export const blogTestingGuides: BlogTestingGuide[] = [
  {
    id: 1,
    title: '软件测试到底在测什么',
    status: '已成稿',
    module: '活动报名',
    testingTheme: '从用户目标、业务规则和数据一致性理解测试对象',
    readerGoal: '知道测试不是随便点页面，而是验证一次报名动作是否稳定、正确、可追踪。',
    originalMarkdown: article01,
    testFocus: ['未满员活动允许报名', '重复报名被阻止', '满员活动不可继续报名', '报名后人数、状态、通知同步变化'],
    operationSteps: ['进入测试执行台，使用 student01 / campus123 登录。', '在活动报名卡片中选择开放活动，点击“报名”。', '观察按钮状态是否变为已报名，并确认报名人数变化。', '再次尝试同类操作，观察重复报名或满员场景是否被拦截。', '切到消息通知，检查是否生成报名成功通知。'],
    assets: ['test-assets/test-cases/activity-and-booknest-core-cases.md', 'test-assets/postman/campushub-testing-lab.postman_collection.json', 'frontend/src/assets/test-assets/test-dashboard.json'],
    acceptance: ['主流程能完成报名', '异常规则有明确提示或禁用态', '页面状态和接口数据不矛盾']
  },
  {
    id: 2,
    title: '测试岗位与能力路线',
    status: '已成稿',
    module: '协作分工',
    testingTheme: '区分产品、开发、测试、测开的交付职责',
    readerGoal: '能把同一个活动报名需求拆成不同角色的输入、输出和协作边界。',
    originalMarkdown: article02,
    testFocus: ['产品验收标准是否清楚', '开发接口和页面是否可被验证', '测试用例是否覆盖业务风险', '自动化脚本是否适合沉淀为回归资产'],
    operationSteps: ['先阅读原文中的岗位职责表。', '打开测试执行台，走一遍登录和活动报名主流程。', '回到本页，把每一步分别标记为产品标准、开发实现、测试验证或自动化回归。', '进入证据资产库，查看用例、脚本和看板如何承接这些职责。'],
    assets: ['test-assets/selenium/test_login_activity_book.py', 'test-assets/article-evidence-map.md', 'README.md'],
    acceptance: ['能说明谁定义规则、谁实现、谁验证、谁维护脚本', '不会把“测试”和“测开”简单理解成会不会写代码']
  },
  {
    id: 3,
    title: '需求不是一句话-测试如何读懂需求',
    status: '已成稿',
    module: '场地预约',
    testingTheme: '把模糊需求拆成字段、规则、边界和验收标准',
    readerGoal: '能从“我要预约自习室”追问出日期、时段、冲突、维护和审核规则。',
    originalMarkdown: article03,
    testFocus: ['预约日期是否合法', '开始/结束时间是否形成有效时段', '维护场地不可预约', '重复时段或冲突时段需要拦截', '提交后形成待审核记录'],
    operationSteps: ['进入测试执行台并登录学生账号。', '在场地预约卡片中选择日期、开始小时和结束小时。', '对可用场地提交预约，观察待审核记录。', '尝试维护场地或冲突时段，记录系统反馈。', '把观察结果对照原文中的需求澄清表。'],
    assets: ['backend/src/main/resources/schema.sql', 'backend/src/main/resources/data.sql', 'test-assets/postman/campushub-testing-lab.postman_collection.json'],
    acceptance: ['每条需求都能落到可验证字段或规则', '异常场景不是靠猜，而是来自需求澄清']
  },
  {
    id: 4,
    title: '软件生命周期里测试应该什么时候介入',
    status: '已成稿',
    module: '场地预约',
    testingTheme: '从需求评审到上线验证规划测试活动',
    readerGoal: '知道测试越早介入，越容易在低成本阶段发现规则遗漏。',
    originalMarkdown: article04,
    testFocus: ['需求阶段发现取消/审核规则缺口', '设计阶段发现通知和审核链路影响', '开发阶段准备接口和数据检查', '上线前执行冒烟和回归'],
    operationSteps: ['阅读原文中的生命周期时间线。', '在测试执行台查看场地预约当前已支持的提交和待审核能力。', '记录当前还缺失的取消预约、审核通过/驳回闭环。', '在证据资产库查看这些缺口如何转为后续用例或缺陷。'],
    assets: ['docs/02-后续优化开发实施方案.md', 'test-assets/test-cases/activity-and-booknest-core-cases.md'],
    acceptance: ['能指出测试在每个阶段的产出物', '能识别“等提测再说”带来的返工风险']
  },
  {
    id: 5,
    title: 'V模型和W模型-为什么测试不能只等提测',
    status: '已成稿',
    module: '场地预约',
    testingTheme: '理解开发阶段与测试阶段的对应和并行关系',
    readerGoal: '能用 CampusHub 场地预约解释 V 模型和 W 模型的实际价值。',
    originalMarkdown: article05,
    testFocus: ['需求和验收测试对应', '概要设计和系统测试对应', '详细设计和集成测试对应', '编码和单元测试对应', '测试活动应并行前置'],
    operationSteps: ['先看原文中的模型对照表。', '打开测试执行台，观察场地预约涉及页面、接口、数据和审核。', '把每个验证点放入 V/W 模型对应位置。', '记录哪些问题如果等提测后才发现会扩大影响面。'],
    assets: ['docs/01-CampusHub项目开发实施方案.md', 'backend/src/main/java/io/github/campushub/lab/api/RoomController.java'],
    acceptance: ['不是背模型图，而是能说明每个阶段能发现什么问题']
  },
  {
    id: 6,
    title: '一个Bug是怎么诞生流转和关闭的',
    status: '已成稿',
    module: '场地预约 / Bug管理',
    testingTheme: '把发现的问题写成可复现、可分派、可回归的缺陷记录',
    readerGoal: '能从“取消后名额未释放”这类现象写出合格 Bug 单。',
    originalMarkdown: article06,
    testFocus: ['标题是否描述业务影响', '前置条件是否可复现', '步骤是否可执行', '实际结果和预期结果是否分开', '回归标准是否明确'],
    operationSteps: ['阅读原文中的 Bug 单模板。', '在测试执行台构造一个业务异常或使用已有样例缺陷。', '到证据资产库查看 sample-book-inventory-inconsistency.md。', '对照模板补齐环境、步骤、实际结果、预期结果和影响范围。'],
    assets: ['test-assets/bug-reports/sample-book-inventory-inconsistency.md', 'frontend/src/assets/test-assets/screenshots/selenium-failure.png'],
    acceptance: ['Bug 不只是“有问题”，而是能被开发复现并被测试回归']
  },
  {
    id: 7,
    title: '和开发争Bug时测试应该怎么沟通',
    status: '已成稿',
    module: '消息通知',
    testingTheme: '用证据、影响范围和规则口径处理缺陷争议',
    readerGoal: '能把“我觉得有问题”改成“这个风险影响了哪些用户和交付目标”。',
    originalMarkdown: article07,
    testFocus: ['争议是否回到需求标准', '是否提供截图/接口/日志证据', '是否说明用户影响', '是否区分缺陷、体验问题和优化建议'],
    operationSteps: ['登录学生账号，执行一次报名、预约或借用。', '查看消息通知是否生成、是否能标记已读。', '如果通知延迟或缺失，用原文的话术整理沟通内容。', '把现象、证据、影响、建议处理方式分开写。'],
    assets: ['frontend/src/assets/test-assets/screenshots/selenium-notification.png', 'test-assets/article-evidence-map.md'],
    acceptance: ['争议沟通能落到事实和风险，不靠情绪表达']
  },
  {
    id: 8,
    title: '测试用例是什么-为什么不能只靠随便点点',
    status: '已成稿',
    module: '设备借用',
    testingTheme: '把测试思路沉淀成可执行、可复查、可回归的用例',
    readerGoal: '能围绕设备借用写出成功、库存不足、重复申请等核心用例。',
    originalMarkdown: article08,
    testFocus: ['成功借用', '库存不足', '重复申请', '借用后生成审核任务', '归还/损坏登记作为后续扩展'],
    operationSteps: ['进入测试执行台并登录。', '在设备借用卡片中选择可用设备、借用日期、归还日期和数量。', '提交借用后观察库存和借用记录。', '重复提交同一设备，观察是否拦截。', '把每次操作写成用例的前置条件、步骤和预期结果。'],
    assets: ['test-assets/test-cases/activity-and-booknest-core-cases.md', 'backend/src/main/java/io/github/campushub/lab/api/DeviceController.java'],
    acceptance: ['用例步骤能复现', '预期结果可判断', '不只覆盖正常流程']
  },
  {
    id: 9,
    title: '设计测试用例的通用思路',
    status: '规划中',
    module: '账号登录',
    testingTheme: '先拆测试点，再选择测试设计方法',
    readerGoal: '能从登录表单拆出输入、状态、权限、错误提示和安全限制。',
    originalMarkdown: plannedOriginal(9, '设计测试用例的通用思路', '账号登录', '测试点拆解'),
    testFocus: ['有效账号登录', '错误密码失败', '锁定账号禁止登录', '管理员和学生权限不同', '错误提示不泄露敏感信息'],
    operationSteps: ['进入测试执行台。', '分别用 student01、admin01、student_locked 尝试登录。', '记录成功、失败、锁定三类反馈。', '把每类反馈转成测试点清单。'],
    assets: ['backend/src/main/resources/data.sql', 'backend/src/test/java/io/github/campushub/lab/api/CampusHubControllerTest.java'],
    acceptance: ['测试点覆盖功能、数据、流程、权限、异常和提示']
  },
  {
    id: 10,
    title: '等价类划分：用最少数据覆盖最多情况',
    status: '规划中',
    module: '账号登录',
    testingTheme: '按输入规则划分有效类和无效类',
    readerGoal: '能为用户名、密码、角色状态选择代表性数据。',
    originalMarkdown: plannedOriginal(10, '等价类划分：用最少数据覆盖最多情况', '账号登录', '等价类划分'),
    testFocus: ['有效学生账号', '有效管理员账号', '不存在账号', '错误密码', '锁定账号'],
    operationSteps: ['在登录区准备 5 组账号数据。', '逐组执行登录。', '记录响应、页面状态和权限差异。', '把数据归入有效等价类或无效等价类。'],
    assets: ['backend/src/main/resources/data.sql', 'test-assets/postman/campushub-testing-lab.postman_collection.json'],
    acceptance: ['每个等价类都有选择依据和代表数据']
  },
  {
    id: 11,
    title: '边界值分析：Bug 最爱藏在边界附近',
    status: '规划中',
    module: '活动报名',
    testingTheme: '围绕名额上限和时间边界设计用例',
    readerGoal: '能验证第 N 人成功、第 N+1 人失败这类边界。',
    originalMarkdown: plannedOriginal(11, '边界值分析：Bug 最爱藏在边界附近', '活动报名', '边界值分析'),
    testFocus: ['0 人报名', '剩 1 个名额', '刚好满员', '超出名额', '报名截止后提交'],
    operationSteps: ['查看活动列表中的 capacity 和 registeredCount。', '选择接近满员的活动观察按钮状态。', '用接口或页面提交报名。', '检查满员后是否禁止继续报名。'],
    assets: ['backend/src/main/resources/data.sql', 'test-assets/test-cases/activity-and-booknest-core-cases.md'],
    acceptance: ['边界点包含刚好等于和刚好超出']
  },
  {
    id: 12,
    title: '判定表法：多条件组合怎么测才不乱',
    status: '规划中',
    module: '活动报名',
    testingTheme: '用条件和动作整理报名规则组合',
    readerGoal: '能把状态、名额、是否已报名、账号状态组合成判定表。',
    originalMarkdown: plannedOriginal(12, '判定表法：多条件组合怎么测才不乱', '活动报名', '判定表法'),
    testFocus: ['活动开放/关闭', '名额有/无', '用户已/未报名', '账号正常/锁定', '允许报名/拒绝报名/提示原因'],
    operationSteps: ['列出活动报名的 4 个条件。', '在页面上寻找对应状态的活动和用户。', '执行允许和拒绝两类动作。', '把结果填入判定表。'],
    assets: ['test-assets/test-cases/activity-and-booknest-core-cases.md'],
    acceptance: ['条件互相独立，动作结果清晰且可验证']
  },
  {
    id: 13,
    title: '正交法：组合太多时怎么压缩用例数量',
    status: '规划中',
    module: '活动列表',
    testingTheme: '为筛选条件选择代表组合',
    readerGoal: '知道正交法是压缩组合，不是替代风险判断。',
    originalMarkdown: plannedOriginal(13, '正交法：组合太多时怎么压缩用例数量', '活动列表', '正交法'),
    testFocus: ['关键词', '状态', '地点', '容量区间', '高风险组合不能省略'],
    operationSteps: ['以活动列表为对象列出筛选因素。', '为每个因素列 2-3 个水平。', '设计压缩后的组合。', '对明显高风险组合单独补充用例。'],
    assets: ['frontend/src/App.vue', 'test-assets/test-cases/activity-and-booknest-core-cases.md'],
    acceptance: ['说明为什么保留或舍弃某些组合']
  },
  {
    id: 14,
    title: '场景法：从主流程到异常流程',
    status: '规划中',
    module: '场地预约',
    testingTheme: '围绕用户任务设计基本流和备选流',
    readerGoal: '能从查询场地到提交预约、审核、取消构建完整场景。',
    originalMarkdown: plannedOriginal(14, '场景法：从主流程到异常流程', '场地预约', '场景法'),
    testFocus: ['预约成功基本流', '场地维护备选流', '时段冲突异常流', '取消预约后名额释放', '审核驳回通知'],
    operationSteps: ['按用户路径写出预约基本流。', '在页面执行一次可用场地预约。', '补充维护、冲突、取消和审核相关备选流。', '标记当前工程尚未闭环的步骤。'],
    assets: ['backend/src/main/java/io/github/campushub/lab/api/RoomController.java', 'docs/02-后续优化开发实施方案.md'],
    acceptance: ['场景覆盖状态变化和数据一致性']
  },
  {
    id: 15,
    title: '错误猜测法和探索式测试',
    status: '规划中',
    module: '活动报名',
    testingTheme: '把经验风险转成有记录的探索任务',
    readerGoal: '能围绕重复点击、刷新、多标签提交等行为设计探索记录。',
    originalMarkdown: plannedOriginal(15, '错误猜测法和探索式测试', '活动报名', '探索式测试'),
    testFocus: ['重复点击报名', '刷新后状态保持', '多标签重复提交', '网络中断重试', '提示和数据是否一致'],
    operationSteps: ['设定 15 分钟探索目标。', '围绕活动报名做重复点击和刷新操作。', '记录每个发现、时间、数据和截图证据。', '把有效发现沉淀成正式回归用例。'],
    assets: ['test-assets/bug-reports/sample-book-inventory-inconsistency.md'],
    acceptance: ['探索有目标、有记录、有后续沉淀']
  },
  {
    id: 16,
    title: '测试分类一次讲清',
    status: '规划中',
    module: '发布验收',
    testingTheme: '按风险选择功能、接口、性能、安全、兼容等测试活动',
    readerGoal: '知道不同测试类型回答不同质量问题。',
    originalMarkdown: plannedOriginal(16, '测试分类一次讲清', '发布验收', '测试分类'),
    testFocus: ['功能是否正确', '接口契约是否稳定', '性能是否达标', '权限是否越权', '浏览器兼容是否可用'],
    operationSteps: ['查看测试指挥台的质量门禁。', '进入证据资产库查看用例、Bug、Selenium、JMeter 证据。', '把每类证据归入对应测试类型。'],
    assets: ['frontend/src/assets/test-assets/test-dashboard.json', 'test-assets/article-evidence-map.md'],
    acceptance: ['能用质量问题解释测试分类，而不是背名词']
  },
  {
    id: 17,
    title: '单元、集成、系统、验收测试有什么区别',
    status: '规划中',
    module: '登录与通知链路',
    testingTheme: '按测试范围区分不同阶段',
    readerGoal: '能说明从单个函数到完整用户验收的范围变化。',
    originalMarkdown: plannedOriginal(17, '单元、集成、系统、验收测试有什么区别', '登录与通知链路', '测试阶段'),
    testFocus: ['登录校验逻辑', '登录接口和数据库集成', '登录后业务页面加载', '用户视角验收完整链路'],
    operationSteps: ['查看后端 MockMvc 测试覆盖。', '在页面执行登录。', '再执行报名并查看通知。', '说明每一步属于哪个测试层级。'],
    assets: ['backend/src/test/java/io/github/campushub/lab/api/CampusHubControllerTest.java', 'test-assets/selenium/test_login_activity_book.py'],
    acceptance: ['能区分测试范围，而不是只按执行人员区分']
  },
  {
    id: 18,
    title: '冒烟测试、回归测试、Alpha/Beta 测试怎么用',
    status: '规划中',
    module: '版本发布',
    testingTheme: '发布前准入、变更验证和灰度试用',
    readerGoal: '能为 CampusHub 设计发布检查清单。',
    originalMarkdown: plannedOriginal(18, '冒烟测试、回归测试、Alpha/Beta 测试怎么用', '版本发布', '发布测试策略'),
    testFocus: ['后端健康检查', '登录冒烟', '活动/图书核心回归', '新增场地设备模块回归', '发布前检查脚本'],
    operationSteps: ['运行本地检查脚本或查看 README 命令。', '打开测试指挥台确认 qualityGate。', '登录后执行一个核心业务动作。', '查看证据资产是否有自动化和性能摘要。'],
    assets: ['scripts/check_release.py', 'README.md', 'RELEASE_CHECKLIST.md'],
    acceptance: ['冒烟用于准入，回归用于确认旧功能未坏']
  },
  {
    id: 19,
    title: '自动化测试不是什么时候都该自动化',
    status: '规划中',
    module: '自动化候选筛选',
    testingTheme: '用收益、稳定性和维护成本判断自动化范围',
    readerGoal: '能判断哪些流程适合 Selenium 回归，哪些暂时保留手工。',
    originalMarkdown: plannedOriginal(19, '自动化测试不是什么时候都该自动化', '自动化候选筛选', '自动化策略'),
    testFocus: ['登录适合自动化', '活动报名适合核心回归', '频繁变动 UI 暂缓', '依赖复杂数据的流程需先治理数据'],
    operationSteps: ['查看自动化证据卡片。', '对登录、活动、BookNest、场地、设备逐项评估稳定性。', '给每个流程标记自动化优先级。'],
    assets: ['test-assets/selenium/README.md', 'frontend/src/assets/test-assets/screenshots'],
    acceptance: ['自动化范围有取舍理由']
  },
  {
    id: 20,
    title: 'Selenium Web 自动化入门',
    status: '规划中',
    module: '登录自动化',
    testingTheme: '驱动浏览器执行操作并断言结果',
    readerGoal: '能看懂最小 Selenium 脚本结构。',
    originalMarkdown: plannedOriginal(20, 'Selenium Web 自动化入门', '登录自动化', 'Selenium 入门'),
    testFocus: ['打开页面', '定位用户名和密码', '点击登录', '断言登录成功', '保存截图'],
    operationSteps: ['启动后端和前端。', '运行 Selenium 脚本。', '查看 screenshots 目录中的登录截图。', '对照页面 data-testid 理解定位方式。'],
    assets: ['test-assets/selenium/test_login_activity_book.py', 'frontend/src/assets/test-assets/screenshots/selenium-login.png'],
    acceptance: ['脚本有操作也有断言，不只是打开页面']
  },
  {
    id: 21,
    title: 'Selenium 常用操作与稳定性问题',
    status: '规划中',
    module: '活动自动化',
    testingTheme: '定位、等待、截图和可控数据',
    readerGoal: '能识别 flaky 脚本的常见原因。',
    originalMarkdown: plannedOriginal(21, 'Selenium 常用操作与稳定性问题', '活动自动化', '自动化稳定性'),
    testFocus: ['稳定定位', '显式等待', '失败截图', '测试数据可重复', '避免固定 sleep'],
    operationSteps: ['查看 Selenium 脚本中使用的 data-testid。', '对比页面中的按钮和输入框。', '查看自动化截图。', '记录可能导致不稳定的页面变化。'],
    assets: ['test-assets/selenium/test_login_activity_book.py', 'frontend/src/App.vue'],
    acceptance: ['能说清页面、数据、等待、断言四类稳定性问题']
  },
  {
    id: 22,
    title: '从手工用例到自动化脚本',
    status: '规划中',
    module: '手工用例转脚本',
    testingTheme: '把步骤拆成数据、页面对象、业务动作和断言',
    readerGoal: '能判断哪些手工步骤需要脚本化，哪些需要抽象。',
    originalMarkdown: plannedOriginal(22, '从手工用例到自动化脚本', '手工用例转脚本', '脚本分层'),
    testFocus: ['测试数据', '页面定位', '业务动作', '断言', '失败证据'],
    operationSteps: ['打开用例 Markdown。', '选择一条登录或活动用例。', '对照 Selenium 脚本找到对应步骤。', '标记哪些步骤应封装为可复用函数。'],
    assets: ['test-assets/test-cases/activity-and-booknest-core-cases.md', 'test-assets/selenium/test_login_activity_book.py'],
    acceptance: ['不是逐字翻译手工步骤，而是形成可维护脚本结构']
  },
  {
    id: 23,
    title: '性能测试入门：响应时间、并发、TPS、QPS',
    status: '规划中',
    module: '活动接口性能',
    testingTheme: '理解性能指标服务于什么业务问题',
    readerGoal: '能解释 p95、错误率、吞吐量和并发的意义。',
    originalMarkdown: plannedOriginal(23, '性能测试入门：响应时间、并发、TPS、QPS', '活动接口性能', '性能指标'),
    testFocus: ['响应时间', 'p95', '错误率', '读取接口和写入接口差异', '性能结论不能脱离环境'],
    operationSteps: ['查看测试指挥台的性能趋势。', '运行性能探针或查看 JTL 样例。', '对比 p95、失败数和错误率。', '写出只基于当前样例的谨慎结论。'],
    assets: ['scripts/run_performance_probe.py', 'frontend/src/assets/test-assets/reports', 'test-assets/jmeter/README.md'],
    acceptance: ['能解释指标，不伪造性能承诺']
  },
  {
    id: 24,
    title: '负载、压力、稳定性、容量测试怎么区分',
    status: '规划中',
    module: '性能测试类型',
    testingTheme: '不同性能测试回答不同问题',
    readerGoal: '能为热门活动报名选择合适的性能测试类型。',
    originalMarkdown: plannedOriginal(24, '负载、压力、稳定性、容量测试怎么区分', '性能测试类型', '性能测试分类'),
    testFocus: ['负载测试看目标负载是否稳定', '压力测试找极限', '稳定性测试看长时间运行', '容量测试估算上限'],
    operationSteps: ['选择活动报名作为业务对象。', '为四类测试分别写目标和退出条件。', '查看当前性能探针属于哪一类。', '说明当前样例不能代表生产容量。'],
    assets: ['test-assets/jmeter/campushub-activity-booknest-smoke.jmx', 'scripts/run_performance_probe.py'],
    acceptance: ['每类测试都有目标、指标和停止条件']
  },
  {
    id: 25,
    title: 'JMeter 从 0 到 1：完成一次接口压测',
    status: '规划中',
    module: 'JMeter 单接口',
    testingTheme: '用线程组、HTTP 请求、断言和监听器跑通最小压测',
    readerGoal: '能理解一个最小 JMeter 脚本由哪些元件组成。',
    originalMarkdown: plannedOriginal(25, 'JMeter 从 0 到 1：完成一次接口压测', 'JMeter 单接口', 'JMeter 入门'),
    testFocus: ['线程组', 'HTTP 请求', '断言', '结果文件', '错误率'],
    operationSteps: ['打开 JMeter README。', '查看 campushub-activity-booknest-smoke.jmx。', '确认请求目标和断言。', '运行或查看生成的 JTL。'],
    assets: ['test-assets/jmeter/README.md', 'test-assets/jmeter/campushub-activity-booknest-smoke.jmx'],
    acceptance: ['脚本可导入、请求有断言、结果可追踪']
  },
  {
    id: 26,
    title: 'JMeter 进阶：登录态、JSON 提取和并发集合点',
    status: '规划中',
    module: 'JMeter 业务链路',
    testingTheme: '把登录、变量提取、后续请求和断言串成业务链路',
    readerGoal: '能区分真实业务链路压测和简单复制 HTTP 请求。',
    originalMarkdown: plannedOriginal(26, 'JMeter 进阶：登录态、JSON 提取和并发集合点', 'JMeter 业务链路', '业务链路压测'),
    testFocus: ['登录响应提取变量', '后续请求引用变量', '报名链路断言最终状态', '集合点的价值和局限', '测试数据清理'],
    operationSteps: ['回顾第 25 期单接口脚本。', '设计登录 -> 查看活动 -> 报名 -> 查询状态链路。', '标记需要提取和传递的变量。', '补充每一步断言和数据清理策略。'],
    assets: ['test-assets/jmeter/README.md', 'scripts/run_performance_probe.py', 'test-assets/article-evidence-map.md'],
    acceptance: ['链路中每一步都有状态传递、断言和清理边界']
  }
]
