<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  Activity,
  Bell,
  BookOpen,
  Boxes,
  Building2,
  ClipboardCheck,
  ClipboardList,
  FileText,
  Gauge,
  LibraryBig,
  Moon,
  PanelLeftClose,
  PanelLeftOpen,
  RefreshCcw,
  Search,
  ShieldCheck,
  Sun,
  TerminalSquare
} from 'lucide-vue-next'
import { blogTestingGuides } from './assets/blog-testing-guides'
import dashboardData from './assets/test-assets/test-dashboard.json'
import AutomationEvidenceViewer from './components/AutomationEvidenceViewer.vue'
import PerformanceTrendChart from './components/PerformanceTrendChart.vue'
import QualityGatePanel from './components/QualityGatePanel.vue'
import RiskQueue from './components/RiskQueue.vue'
import RunEvidenceStrip from './components/RunEvidenceStrip.vue'
import StatusBadge from './components/StatusBadge.vue'
import TestCaseEvidenceTable from './components/TestCaseEvidenceTable.vue'

const apiBaseUrl = import.meta.env.VITE_DIRECT_API_BASE_URL ?? ''

type ModuleSummary = { name: string; scope: string; testingValue: string }
type OverviewResponse = { project: string; version: string; modules: ModuleSummary[]; statistics: Record<string, number> }
type UserItem = { id: number; username: string; displayName: string; roleCode: string; status: string }
type LoginResponse = { token: string; user: UserItem; permissions: string[] }
type ActivityItem = { id: number; title: string; organizer: string; location: string; capacity: number; registeredCount: number; status: string; registered: boolean }
type RoomItem = { id: number; name: string; building: string; capacity: number; status: string; activeReservations: number }
type RoomReservationItem = { id: number; roomName: string; reservationDate: string; startHour: number; endHour: number; status: string }
type DeviceItem = { id: number; name: string; category: string; totalQuantity: number; availableQuantity: number; status: string }
type DeviceBorrowItem = { id: number; deviceName: string; quantity: number; status: string; borrowedAt: string; dueAt: string }
type BookItem = { id: number; isbn: string; title: string; author: string; category: string; totalCopies: number; availableCopies: number }
type BookBorrowItem = { id: number; title: string; status: string; borrowedAt: string; dueAt: string; renewCount: number }
type ReviewTaskItem = { id: number; taskType: string; title: string; applicant: string; status: string; reviewer: string | null; comment: string | null }
type NotificationItem = { id: number; title: string; readFlag: boolean }
type ActionResponse = { code: string; message: string }
type ActiveView = 'mission-control' | 'test-run' | 'evidence'

const overview = ref<OverviewResponse | null>(null)
const session = ref<LoginResponse | null>(null)
const activities = ref<ActivityItem[]>([])
const rooms = ref<RoomItem[]>([])
const roomReservations = ref<RoomReservationItem[]>([])
const devices = ref<DeviceItem[]>([])
const deviceBorrows = ref<DeviceBorrowItem[]>([])
const notifications = ref<NotificationItem[]>([])
const books = ref<BookItem[]>([])
const borrows = ref<BookBorrowItem[]>([])
const reviewTasks = ref<ReviewTaskItem[]>([])

const username = ref('student01')
const password = ref('campus123')
const bookKeyword = ref('')
const roomReservationDate = ref('2026-06-30')
const roomStartHour = ref(9)
const roomEndHour = ref(11)
const deviceBorrowDate = ref('2026-06-30')
const deviceDueDate = ref('2026-07-07')
const deviceQuantity = ref(1)

const loading = ref(true)
const busy = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const theme = ref<'light' | 'dark'>('light')
const activeView = ref<ActiveView>('mission-control')
const selectedBlogId = ref(1)
const articlePanelMode = ref<'guide' | 'original'>('guide')
const isSidebarCollapsed = ref(false)
const isBlogIndexCollapsed = ref(false)
const isPracticeGuideOpen = ref(false)
const guideRatio = ref(65)
const isResizingGuideSplit = ref(false)
const floatingGuideSize = ref<'compact' | 'normal' | 'wide'>('normal')
const floatingGuidePosition = ref({ x: 22, y: 22 })
const floatingGuideDragOffset = ref({ x: 0, y: 0 })
const isDraggingFloatingGuide = ref(false)

const qualityDashboard = dashboardData
const blogGuides = blogTestingGuides
const selectedBlog = computed(() => blogGuides.find((item) => item.id === selectedBlogId.value) ?? blogGuides[0])
const completedArticleCount = computed(() => blogGuides.filter((item) => item.status === '已成稿').length)
const selectedWalkthrough = computed(() => buildWalkthrough(selectedBlog.value.id))
const evidenceMatrix = computed(() => blogGuides.map((blog) => {
  const normalizedModule = blog.module.toLowerCase()
  const relatedCases = qualityDashboard.testCases.filter((item) => {
    const moduleName = item.module.toLowerCase()
    return normalizedModule.includes(moduleName) || moduleName.includes(normalizedModule.split(/[ /]/)[0])
  })
  const relatedScreenshots = qualityDashboard.automation.screenshots.filter((item) => {
    const moduleName = item.module.toLowerCase()
    return normalizedModule.includes(moduleName) || moduleName.includes(normalizedModule.split(/[ /]/)[0])
  })
  const relatedBugs = qualityDashboard.bugs.filter((item) => normalizedModule.includes(item.module.toLowerCase()))
  const hasPerformance = blog.id >= 23 || normalizedModule.includes('活动')

  return {
    id: blog.id,
    title: blog.title,
    module: blog.module,
    theme: blog.testingTheme,
    caseCount: relatedCases.length,
    screenshotCount: relatedScreenshots.length,
    bugCount: relatedBugs.length,
    hasPerformance,
    status: blog.status === '已成稿' ? '可跟做' : '规划中'
  }
}))
const markdownPreviewLines = computed(() => selectedBlog.value.originalMarkdown.split(/\r?\n/).slice(0, 120))
const currentUser = computed(() => session.value?.user ?? null)
const isReviewer = computed(() => session.value?.permissions.includes('REVIEW_TASK_DECIDE') ?? false)
const unreadCount = computed(() => notifications.value.filter((item) => !item.readFlag).length)
const bookAvailability = computed(() => {
  const total = books.value.reduce((sum, item) => sum + item.totalCopies, 0)
  const available = books.value.reduce((sum, item) => sum + item.availableCopies, 0)
  return { total, available }
})

const navItems = computed(() => [
  { id: 'mission-control' as ActiveView, label: '博客测试台', icon: FileText, badge: `${completedArticleCount.value}/26` },
  { id: 'test-run' as ActiveView, label: '实操工作台', icon: ClipboardCheck, badge: currentUser.value ? currentUser.value.username : '未登录' },
  { id: 'evidence' as ActiveView, label: '证据资产库', icon: LibraryBig, badge: `${qualityDashboard.testCases.length} cases` }
])

type WalkthroughStep = {
  title: string
  target: string
  input: string
  action: string
  expected: string
  fallback: string
}

function controlHint(step: WalkthroughStep) {
  const text = `${step.title} ${step.target} ${step.action}`
  if (text.includes('登录') && text.includes('管理员')) return '在“测试账号”卡片点击“管理员”快捷按钮；如需手输，先填“用户名”“密码”，再点“登录并加载工作台”。'
  if (text.includes('登录')) return '在“测试账号”卡片填写“用户名”和“密码”两个输入框，然后点击绿色按钮“登录并加载工作台”。'
  if (text.includes('活动报名') || text.includes('报名')) return '在“活动报名”卡片的活动表格中，找到目标活动所在行，点击该行最右侧按钮“报名”；已报名后同一位置会变成“取消”。'
  if (text.includes('场地预约') || text.includes('场地')) return '在“场地预约”卡片先填写日期、开始小时、结束小时 3 个输入框，再点击目标场地卡片底部按钮“预约”。'
  if (text.includes('设备借用') || text.includes('设备')) return '在“设备借用”卡片先填写借用日期、归还日期、数量 3 个输入框，再点击目标设备卡片底部按钮“借用”。'
  if (text.includes('BookNest') || text.includes('图书') || text.includes('借阅')) return '在“BookNest 借阅”卡片可先用检索输入框和“检索”按钮缩小范围，再点击目标图书卡片底部按钮“借阅”。'
  if (text.includes('通知') || text.includes('已读')) return '在“消息通知”卡片找到未读通知行，点击该行右侧按钮“已读”。'
  if (text.includes('审核') || text.includes('通过') || text.includes('驳回')) return '用管理员登录后，在“后台审核”卡片找到待审核任务行，点击该行按钮“通过”或“驳回”。'
  if (text.includes('证据资产库') || text.includes('用例') || text.includes('Bug')) return '点击左侧导航“证据资产库”；在“用例证据矩阵”点击“查看详情”，或在“缺陷与风险队列”点击“查看复盘”。'
  if (text.includes('性能') || text.includes('JMeter')) return '点击左侧导航“证据资产库”，滚动到“活动报名接口性能趋势”和“执行摘要”；命令行步骤按卡片里的命令执行。'
  return '先点击顶部或左侧对应视图入口，再按当前卡片内的主按钮执行；按钮文字以页面上显示为准。'
}

function observeHint(step: WalkthroughStep) {
  const text = `${step.title} ${step.target}`
  if (text.includes('登录')) return '观察顶部成功提示、左侧“实操工作台”徽标和“测试账号”卡片里的当前用户信息。'
  if (text.includes('活动报名')) return '观察同一活动行里的报名人数、状态标签和按钮文案是否变化。'
  if (text.includes('场地预约')) return '观察场地卡片下方的预约记录条，重点看场地名、日期和“待审核”状态。'
  if (text.includes('设备借用')) return '观察设备卡片库存数字和下方借用记录，重点看设备名、数量和审核状态。'
  if (text.includes('通知')) return '观察通知行状态是否从“未读”变成“已读”。'
  return step.expected
}

function goPractice() {
  activeView.value = 'test-run'
  isPracticeGuideOpen.value = true
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value))
}

function startGuideSplitResize(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  target.setPointerCapture(event.pointerId)
  isResizingGuideSplit.value = true
  updateGuideRatio(event)
}

function moveGuideSplitResize(event: PointerEvent) {
  if (!isResizingGuideSplit.value) return
  updateGuideRatio(event)
}

function stopGuideSplitResize(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  if (target.hasPointerCapture(event.pointerId)) target.releasePointerCapture(event.pointerId)
  isResizingGuideSplit.value = false
}

function updateGuideRatio(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  const grid = target.closest('.guide-article-grid') as HTMLElement | null
  if (!grid) return
  const rect = grid.getBoundingClientRect()
  guideRatio.value = Math.round(clamp(((event.clientX - rect.left) / rect.width) * 100, 45, 80))
}

function backToBlogConsole() {
  activeView.value = 'mission-control'
  isPracticeGuideOpen.value = false
}

function floatingGuideStyle() {
  const widths = {
    compact: 340,
    normal: 430,
    wide: 560
  }
  return {
    width: `${widths[floatingGuideSize.value]}px`,
    right: `${floatingGuidePosition.value.x}px`,
    bottom: `${floatingGuidePosition.value.y}px`
  }
}

function startFloatingGuideDrag(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  target.setPointerCapture(event.pointerId)
  isDraggingFloatingGuide.value = true
  floatingGuideDragOffset.value = {
    x: event.clientX,
    y: event.clientY
  }
}

function moveFloatingGuide(event: PointerEvent) {
  if (!isDraggingFloatingGuide.value) return
  const deltaX = event.clientX - floatingGuideDragOffset.value.x
  const deltaY = event.clientY - floatingGuideDragOffset.value.y
  floatingGuidePosition.value = {
    x: Math.max(12, floatingGuidePosition.value.x - deltaX),
    y: Math.max(12, floatingGuidePosition.value.y - deltaY)
  }
  floatingGuideDragOffset.value = {
    x: event.clientX,
    y: event.clientY
  }
}

function stopFloatingGuideDrag(event: PointerEvent) {
  const target = event.currentTarget as HTMLElement
  if (target.hasPointerCapture(event.pointerId)) target.releasePointerCapture(event.pointerId)
  isDraggingFloatingGuide.value = false
}

function markdownLineClass(line: string) {
  if (line.startsWith('# ')) return 'md-h1'
  if (line.startsWith('## ')) return 'md-h2'
  if (line.startsWith('### ')) return 'md-h3'
  if (line.startsWith('>')) return 'md-quote'
  if (line.startsWith('|')) return 'md-table'
  if (/^\s*[-*]\s+/.test(line)) return 'md-list'
  if (/^\s*\d+\.\s+/.test(line)) return 'md-list'
  if (!line.trim()) return 'md-blank'
  return 'md-p'
}

function markdownLineText(line: string) {
  return line
    .replace(/^#{1,6}\s+/, '')
    .replace(/^>\s?/, '')
    .replace(/^\s*[-*]\s+/, '• ')
    .replace(/\*\*/g, '')
}

onMounted(async () => {
  initTheme()
  await loadOverview()
  loading.value = false
})

function initTheme() {
  const savedTheme = localStorage.getItem('campushub-theme')
  theme.value = savedTheme === 'dark' ? 'dark' : 'light'
  document.documentElement.dataset.theme = theme.value
}

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.dataset.theme = theme.value
  localStorage.setItem('campushub-theme', theme.value)
}

function buildWalkthrough(blogId: number): WalkthroughStep[] {
  if ([1, 11, 12, 15].includes(blogId)) {
    return [
      {
        title: '登录学生账号',
        target: '实操工作台 / 测试账号',
        input: '用户名 student01，密码 campus123',
        action: '点击“登录并加载工作台”。',
        expected: '顶部出现“测试学生一号 登录成功”，左侧导航的实操工作台徽标变为 student01。',
        fallback: '如果登录失败，先确认后端在线；再检查是否把预填账号重复输入了一遍。'
      },
      {
        title: '执行一次活动报名',
        target: '实操工作台 / 活动报名',
        input: '选择状态为“开放”且按钮可点击的活动，例如“社团招新宣讲会”。',
        action: '点击该行右侧“报名”。',
        expected: '该活动状态变为“已报名”或报名按钮变为“取消”，报名人数同步变化。',
        fallback: '如果按钮不可点，说明活动已满、已报名或未登录；换一个开放活动再测。'
      },
      {
        title: '验证重复/边界规则',
        target: '实操工作台 / 活动报名',
        input: '继续观察同一活动，或选择已满活动。',
        action: '尝试再次报名、取消后再报名，或观察满员活动按钮状态。',
        expected: '重复报名不能造成重复名额；满员活动不能继续提交报名。',
        fallback: '如果页面看不出原因，到证据资产库查看接口用例和 Postman 集合。'
      },
      {
        title: '检查通知证据',
        target: '实操工作台 / 消息通知',
        input: '沿用 student01 登录态。',
        action: '滚动到消息通知卡片，查看是否出现报名相关通知，并点击“已读”。',
        expected: '通知从“未读”变为“已读”，说明业务动作有后续反馈。',
        fallback: '没有通知时，先确认刚才报名是否成功；再把现象记成待确认问题。'
      }
    ]
  }

  if ([3, 4, 5, 6, 14].includes(blogId)) {
    return [
      {
        title: '登录学生账号',
        target: '实操工作台 / 测试账号',
        input: '用户名 student01，密码 campus123',
        action: '点击“登录并加载工作台”。',
        expected: '页面加载出场地预约卡片。',
        fallback: '未加载时先看顶部是否显示后端在线。'
      },
      {
        title: '提交一条可用场地预约',
        target: '实操工作台 / 场地预约',
        input: '日期 2026-06-30，开始 9，结束 11，选择 A101 自习室或 B203 会议室。',
        action: '点击场地卡片里的“预约”。',
        expected: '下方出现“场地名 · 日期 · 待审核”的预约记录。',
        fallback: '如果提示冲突，换日期或换场地；这正好可作为冲突规则观察点。'
      },
      {
        title: '验证维护/冲突规则',
        target: '实操工作台 / 场地预约',
        input: '选择状态不是“可用”的场地，或复用刚才的日期时段。',
        action: '观察按钮是否禁用，或提交后是否给出失败原因。',
        expected: '维护场地不可预约；重复时段不能形成两条有效预约。',
        fallback: '如果当前版本只能看到提交和待审核，记录“取消/审核闭环未完整”作为阶段缺口。'
      },
      {
        title: '把现象写成需求或 Bug 证据',
        target: '证据资产库 / 缺陷与用例',
        input: '刚才的日期、场地、账号、实际提示。',
        action: '对照样例 Bug 或用例模板补齐前置条件、步骤、实际结果和预期结果。',
        expected: '输出一条别人可复现的测试记录。',
        fallback: '描述不清时回到页面重新执行，并补一张截图或接口返回。'
      }
    ]
  }

  if ([8].includes(blogId)) {
    return [
      {
        title: '登录学生账号',
        target: '实操工作台 / 测试账号',
        input: '用户名 student01，密码 campus123',
        action: '点击“登录并加载工作台”。',
        expected: '设备借用卡片显示设备库存和借用按钮。',
        fallback: '如果看不到设备，确认是否还在博客测试台，需要点击“去实操”。'
      },
      {
        title: '执行成功借用用例',
        target: '实操工作台 / 设备借用',
        input: '借用日期 2026-06-30，归还日期 2026-07-07，数量 1，选择可用设备。',
        action: '点击“借用”。',
        expected: '下方出现设备借用记录，状态为待审核或相关状态。',
        fallback: '如果设备库存为 0，换一个可用设备；库存为 0 是另一条反向用例。'
      },
      {
        title: '执行重复申请反向用例',
        target: '实操工作台 / 设备借用',
        input: '沿用同一账号、同一设备、同一日期。',
        action: '再次点击“借用”。',
        expected: '系统应拒绝重复申请，不能产生两条同类有效借用。',
        fallback: '如果页面只显示错误提示，把提示内容写入用例实际结果。'
      },
      {
        title: '沉淀成测试用例',
        target: '证据资产库 / 测试用例',
        input: '成功借用、库存不足、重复申请三组数据。',
        action: '把每组数据写成前置条件、步骤、预期结果。',
        expected: '形成可复查、可回归的设备借用用例。',
        fallback: '如果预期结果无法判断，说明需求规则还没澄清。'
      }
    ]
  }

  if ([7].includes(blogId)) {
    return [
      {
        title: '制造一条通知证据',
        target: '实操工作台 / 活动报名或设备借用',
        input: 'student01 / campus123',
        action: '登录后执行一次报名、预约或借用。',
        expected: '消息通知卡片出现业务通知。',
        fallback: '没有通知时，记录业务动作、账号、时间和页面提示。'
      },
      {
        title: '验证通知已读',
        target: '实操工作台 / 消息通知',
        input: '未读通知一条。',
        action: '点击“已读”。',
        expected: '状态从未读变为已读。',
        fallback: '状态未变化时，作为可复现缺陷记录。'
      },
      {
        title: '整理争议沟通材料',
        target: '博客测试台 / 本期指南',
        input: '现象、截图、用户影响、需求口径。',
        action: '用“事实 -> 影响 -> 建议处理方式”的结构整理说明。',
        expected: '沟通内容不再是“我觉得”，而是可判断的交付风险。',
        fallback: '证据不足时先补截图或接口返回。'
      }
    ]
  }

  if ([9, 10, 17, 20, 21, 22].includes(blogId)) {
    return [
      {
        title: '验证正常登录',
        target: '实操工作台 / 测试账号',
        input: 'student01 / campus123',
        action: '点击“登录并加载工作台”。',
        expected: '登录成功并加载活动、场地、设备、图书模块。',
        fallback: '失败时先确认账号是否被改动，或后端是否在线。'
      },
      {
        title: '验证管理员权限差异',
        target: '实操工作台 / 测试账号',
        input: 'admin01 / campus123',
        action: '点击“管理员”快捷按钮。',
        expected: '后台审核卡片显示审核任务，可以看到“通过/驳回”操作。',
        fallback: '如果无审核任务，先用学生账号提交场地或设备申请。'
      },
      {
        title: '验证异常登录',
        target: '实操工作台 / 测试账号',
        input: 'student_locked / campus123，或 student01 / wrong-password',
        action: '手动输入账号密码并登录。',
        expected: '锁定账号或错误密码不能进入工作台，并给出清楚提示。',
        fallback: '如果错误提示不清楚，记录为可用性或安全提示问题。'
      }
    ]
  }

  if ([23, 24, 25, 26].includes(blogId)) {
    return [
      {
        title: '先看当前性能证据',
        target: '博客测试台 / 右侧素材',
        input: 'test-dashboard.json、JMeter README、性能探针脚本。',
        action: '确认本期要看的指标是响应时间、p95、错误率或链路状态。',
        expected: '能说清这次性能样例回答的是哪个问题。',
        fallback: '如果只看到“快/慢”，说明指标口径还不够。'
      },
      {
        title: '运行最小性能探针',
        target: '命令行 / campushub-testing-lab',
        input: '后端已启动，例如 http://localhost:8080。',
        action: '执行 python scripts\\run_performance_probe.py --base-url http://localhost:8080 --loops 5。',
        expected: '生成 JTL 或摘要文件，错误率应能被看板识别。',
        fallback: '失败时优先检查后端地址、中文查询参数编码和接口状态码。'
      },
      {
        title: '回到看板判断结论',
        target: '证据资产库 / 性能与运行证据',
        input: '刚生成的报告。',
        action: '重新生成测试看板或查看性能趋势。',
        expected: '结论只基于当前环境和样本，不写成生产容量承诺。',
        fallback: '有失败样本时不能标为 passed，需要先解释错误率。'
      }
    ]
  }

  return [
    {
      title: '阅读本期目标',
      target: '博客测试台 / 本期指南',
      input: '当前选中的博客期数。',
      action: '先看“涉及的测试”和“做到什么算完成”。',
      expected: '知道本期要验证的质量风险，而不是直接乱点页面。',
      fallback: '如果目标仍不明确，先打开原文查看开篇场景。'
    },
    {
      title: '进入实操工作台',
      target: '实操工作台',
      input: 'student01 / campus123 或 admin01 / campus123',
      action: '按本期模块找到对应卡片并执行一次主流程。',
      expected: '页面状态、业务记录或通知产生可观察变化。',
      fallback: '没有变化时，把账号、输入、按钮状态和提示记录下来。'
    },
    {
      title: '整理证据',
      target: '证据资产库',
      input: '操作结果、素材路径、用例或 Bug 模板。',
      action: '把观察结果写成用例、缺陷或检查清单。',
      expected: '输出能复查的测试交付物。',
      fallback: '无法复查时，补充前置条件和预期结果。'
    }
  ]
}

async function loadOverview() {
  overview.value = await request<OverviewResponse>('/api/overview')
}

async function loginAs(nextUsername?: string) {
  if (nextUsername) {
    username.value = nextUsername
    password.value = 'campus123'
  }
  await runAction(async () => {
    session.value = await request<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    successMessage.value = `${session.value.user.displayName} 登录成功`
    activeView.value = 'test-run'
    await loadWorkspace()
  })
}

async function loadWorkspace() {
  const activeUsername = currentUser.value?.username ?? ''
  const [nextActivities, nextRooms, nextDevices, nextBooks] = await Promise.all([
    request<ActivityItem[]>(`/api/activities?username=${encodeURIComponent(activeUsername)}`),
    request<RoomItem[]>('/api/rooms'),
    request<DeviceItem[]>('/api/devices'),
    request<BookItem[]>(`/api/books?keyword=${encodeURIComponent(bookKeyword.value)}`)
  ])
  activities.value = nextActivities
  rooms.value = nextRooms
  devices.value = nextDevices
  books.value = nextBooks

  if (activeUsername) {
    const [nextBorrows, nextReservations, nextDeviceBorrows, nextNotifications] = await Promise.all([
      request<BookBorrowItem[]>(`/api/book-borrows?username=${encodeURIComponent(activeUsername)}`),
      request<RoomReservationItem[]>(`/api/room-reservations?username=${encodeURIComponent(activeUsername)}`),
      request<DeviceBorrowItem[]>(`/api/device-borrows?username=${encodeURIComponent(activeUsername)}`),
      request<NotificationItem[]>(`/api/notifications?username=${encodeURIComponent(activeUsername)}`)
    ])
    borrows.value = nextBorrows
    roomReservations.value = nextReservations
    deviceBorrows.value = nextDeviceBorrows
    notifications.value = nextNotifications
  }

  reviewTasks.value = isReviewer.value ? await request<ReviewTaskItem[]>('/api/admin/review-tasks') : []
}

async function registerActivity(activityId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/activities/${activityId}/registrations`, {
      method: 'POST',
      body: JSON.stringify({ username: requireUsername() })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function cancelActivity(activityId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(
      `/api/activities/${activityId}/registrations/${encodeURIComponent(requireUsername())}`,
      { method: 'DELETE' }
    )
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function reserveRoom(roomId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/rooms/${roomId}/reservations`, {
      method: 'POST',
      body: JSON.stringify({
        username: requireUsername(),
        reservationDate: roomReservationDate.value,
        startHour: Number(roomStartHour.value),
        endHour: Number(roomEndHour.value)
      })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function borrowDevice(deviceId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/devices/${deviceId}/borrow`, {
      method: 'POST',
      body: JSON.stringify({
        username: requireUsername(),
        quantity: Number(deviceQuantity.value),
        borrowedAt: deviceBorrowDate.value,
        dueAt: deviceDueDate.value
      })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function markNotificationRead(notificationId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/notifications/${notificationId}/read`, {
      method: 'POST',
      body: JSON.stringify({ username: requireUsername() })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function borrowBook(bookId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/books/${bookId}/borrow`, {
      method: 'POST',
      body: JSON.stringify({ username: requireUsername() })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function renewBorrow(borrowId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/book-borrows/${borrowId}/renew`, {
      method: 'POST',
      body: JSON.stringify({ username: requireUsername() })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function returnBorrow(borrowId: number) {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/book-borrows/${borrowId}/return`, {
      method: 'POST',
      body: JSON.stringify({ username: requireUsername() })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function decideTask(taskId: number, decision: 'APPROVED' | 'REJECTED') {
  await runAction(async () => {
    const response = await request<ActionResponse>(`/api/admin/review-tasks/${taskId}/decision`, {
      method: 'POST',
      body: JSON.stringify({
        reviewer: requireUsername(),
        decision,
        comment: decision === 'APPROVED' ? '示例审核通过' : '示例审核驳回'
      })
    })
    successMessage.value = response.message
    await loadWorkspace()
  })
}

async function runAction(action: () => Promise<void>) {
  busy.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    await action()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '操作失败'
  } finally {
    busy.value = false
  }
}

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${url}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
    ...options
  })
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}))
    throw new Error(payload.detail ?? payload.message ?? `接口请求失败：${response.status}`)
  }
  return response.json() as Promise<T>
}

function requireUsername() {
  if (!currentUser.value) throw new Error('请先登录')
  return currentUser.value.username
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    OPEN: '开放',
    FULL: '已满',
    CLOSED: '关闭',
    BORROWED: '借出',
    RETURNED: '归还',
    RESERVED: '预约',
    AVAILABLE: '可用',
    OUT_OF_STOCK: '无库存',
    MAINTENANCE: '维护',
    OVERDUE: '逾期',
    PENDING: '待审核',
    APPROVED: '通过',
    REJECTED: '驳回',
    ACTIVE: '正常'
  }
  return labels[status] ?? status
}

function statusTone(status: string) {
  if (['OPEN', 'APPROVED', 'RETURNED', 'ACTIVE', 'AVAILABLE'].includes(status)) return 'success'
  if (['PENDING', 'BORROWED', 'RESERVED'].includes(status)) return 'info'
  if (['OVERDUE', 'FULL', 'CLOSED', 'OUT_OF_STOCK'].includes(status)) return 'warning'
  if (['REJECTED'].includes(status)) return 'danger'
  return 'neutral'
}

function statLabel(key: string) {
  const labels: Record<string, string> = {
    users: '示例用户',
    activities: '活动',
    books: '图书',
    rooms: '场地',
    devices: '设备'
  }
  return labels[key] ?? key
}
</script>

<template>
  <main class="qa-shell" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <aside class="qa-sidebar">
      <div class="brand-block">
        <span class="brand-mark">QA</span>
        <div class="brand-copy">
          <strong>CampusHub Lab</strong>
          <span>测试管理示范项目</span>
        </div>
        <button class="collapse-button" type="button" @click="isSidebarCollapsed = !isSidebarCollapsed">
          <PanelLeftOpen v-if="isSidebarCollapsed" :size="18" aria-hidden="true" />
          <PanelLeftClose v-else :size="18" aria-hidden="true" />
        </button>
      </div>

      <nav class="nav-list" aria-label="测试平台导航">
        <button
          v-for="item in navItems"
          :key="item.id"
          type="button"
          class="nav-button"
          :class="{ active: activeView === item.id }"
          @click="activeView = item.id"
        >
          <component :is="item.icon" :size="18" aria-hidden="true" />
          <span class="nav-label-text">{{ item.label }}</span>
          <small>{{ item.badge }}</small>
        </button>
      </nav>

      <section class="release-card">
        <span>Release readiness</span>
        <strong>{{ qualityDashboard.summary.qualityScore }}/100</strong>
        <p>{{ qualityDashboard.summary.qualityGate }} · {{ qualityDashboard.dataMode }}</p>
      </section>
    </aside>

    <section class="qa-main">
      <header class="topbar">
        <div class="topbar-main">
          <span class="breadcrumb">CampusHub / {{ activeView === 'mission-control' ? '博客测试台' : activeView === 'test-run' ? '实操工作台' : '证据资产库' }}</span>
          <div class="title-with-picker">
            <h1>{{ activeView === 'mission-control' ? '博客测试台' : activeView === 'test-run' ? '实操工作台' : '证据资产库' }}</h1>
            <section v-if="activeView === 'mission-control'" class="blog-inline-index" :class="{ collapsed: isBlogIndexCollapsed }">
              <button class="icon-button" type="button" @click="isBlogIndexCollapsed = !isBlogIndexCollapsed">
                <PanelLeftOpen v-if="isBlogIndexCollapsed" :size="17" aria-hidden="true" />
                <PanelLeftClose v-else :size="17" aria-hidden="true" />
              </button>
              <StatusBadge v-if="!isBlogIndexCollapsed" :label="`${completedArticleCount}/26 已成稿`" tone="info" />
              <button v-if="isBlogIndexCollapsed" class="blog-active-pill" type="button" @click="isBlogIndexCollapsed = false">
                {{ String(selectedBlog.id).padStart(2, '0') }}
              </button>
              <div v-else class="blog-inline-list" aria-label="博客期数列表">
                <button
                  v-for="blog in blogGuides"
                  :key="blog.id"
                  type="button"
                  class="blog-list-item"
                  :class="{ active: selectedBlog.id === blog.id }"
                  @click="selectedBlogId = blog.id"
                >
                  <span>{{ String(blog.id).padStart(2, '0') }}</span>
                  <strong>{{ blog.title }}</strong>
                  <small>{{ blog.module }} · {{ blog.status }}</small>
                </button>
              </div>
            </section>
          </div>
        </div>
        <div class="topbar-actions">
          <div class="service-pill" data-testid="service-status">
            <span class="pulse" :class="{ warn: loading || errorMessage }"></span>
            <span>{{ loading ? '连接后端' : errorMessage ? '接口异常' : '后端在线' }}</span>
          </div>
          <button v-if="activeView === 'test-run'" class="button secondary" type="button" @click="isPracticeGuideOpen = true">打开指南</button>
          <button class="icon-button" type="button" data-testid="theme-toggle" @click="toggleTheme">
            <Moon v-if="theme === 'light'" :size="18" aria-hidden="true" />
            <Sun v-else :size="18" aria-hidden="true" />
          </button>
        </div>
      </header>

      <p v-if="errorMessage" class="message error-message" data-testid="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="message success-message" data-testid="success-message">{{ successMessage }}</p>

      <section v-if="activeView === 'mission-control'" class="view-stack">
        <section class="blog-command-layout">
          <section
            class="guide-article-grid"
            :class="{ resizing: isResizingGuideSplit }"
            :style="{ '--guide-fr': `${guideRatio}fr`, '--article-fr': `${100 - guideRatio}fr` }"
          >
            <section class="panel test-guide">
              <div class="section-head compact-head">
                <div>
                  <span class="eyebrow">Testing guide</span>
                  <h2>{{ String(selectedBlog.id).padStart(2, '0') }} 本期怎么测</h2>
                </div>
                <button class="button primary" type="button" @click="goPractice">去实操</button>
              </div>

              <section class="guide-brief">
                <div>
                  <span>本期文章</span>
                  <strong>{{ selectedBlog.title }}</strong>
                </div>
                <div>
                  <span>实操模块</span>
                  <strong>{{ selectedBlog.module }}</strong>
                </div>
                <div>
                  <span>学习目标</span>
                  <strong>{{ selectedBlog.testingTheme }}</strong>
                </div>
              </section>

              <section class="guide-block">
                <h3>先确认这期到底在测什么</h3>
                <ul class="check-list">
                  <li v-for="item in selectedBlog.testFocus" :key="item">{{ item }}</li>
                </ul>
              </section>

              <section class="guide-block">
                <h3>照着做：一步一步完成测试</h3>
                <div class="walkthrough-list">
                  <article v-for="(step, index) in selectedWalkthrough" :key="step.title" class="walkthrough-step">
                    <span class="step-index">{{ index + 1 }}</span>
                    <div class="step-body">
                      <strong>{{ step.title }}</strong>
                      <dl>
                        <div><dt>去哪里</dt><dd>{{ step.target }}</dd></div>
                        <div><dt>用什么</dt><dd>{{ step.input }}</dd></div>
                        <div><dt>按哪个控件</dt><dd>{{ controlHint(step) }}</dd></div>
                        <div><dt>怎么做</dt><dd>{{ step.action }}</dd></div>
                        <div><dt>看哪里</dt><dd>{{ observeHint(step) }}</dd></div>
                        <div><dt>应该看到</dt><dd>{{ step.expected }}</dd></div>
                        <div><dt>不对怎么办</dt><dd>{{ step.fallback }}</dd></div>
                      </dl>
                    </div>
                  </article>
                </div>
              </section>

              <section class="guide-block">
                <h3>对应素材</h3>
                <div class="asset-list">
                  <code v-for="asset in selectedBlog.assets" :key="asset">{{ asset }}</code>
                </div>
              </section>

              <section class="guide-block">
                <h3>做到什么算完成</h3>
                <ul class="check-list">
                  <li v-for="item in selectedBlog.acceptance" :key="item">{{ item }}</li>
                </ul>
              </section>

              <section class="guide-actions">
                <button class="button primary" type="button" @click="goPractice">打开实操工作台</button>
                <button class="button secondary" type="button" @click="activeView = 'evidence'">查看证据资产库</button>
              </section>
            </section>

            <div
              class="guide-splitter"
              role="separator"
              aria-label="调整 Testing guide 和 Article 宽度"
              @pointerdown="startGuideSplitResize"
              @pointermove="moveGuideSplitResize"
              @pointerup="stopGuideSplitResize"
              @pointercancel="stopGuideSplitResize"
            >
              <span>{{ guideRatio }}/{{ 100 - guideRatio }}</span>
            </div>

            <aside class="panel blog-reader">
              <div class="reader-toolbar">
                <div>
                  <span class="eyebrow">Article</span>
                  <h2>{{ String(selectedBlog.id).padStart(2, '0') }} {{ selectedBlog.title }}</h2>
                  <p>{{ selectedBlog.readerGoal }}</p>
                </div>
                <div class="segmented">
                  <button type="button" :class="{ active: articlePanelMode === 'guide' }" @click="articlePanelMode = 'guide'">摘要</button>
                  <button type="button" :class="{ active: articlePanelMode === 'original' }" @click="articlePanelMode = 'original'">MD预览</button>
                </div>
              </div>

              <div v-if="articlePanelMode === 'guide'" class="guide-overview">
                <article class="guide-summary">
                  <span>读者先做什么</span>
                  <strong>按中间步骤卡执行</strong>
                  <p>不要先乱点工作台，先明确入口、数据、动作和预期。</p>
                </article>
                <article class="guide-summary">
                  <span>正文状态</span>
                  <strong>{{ selectedBlog.status }}</strong>
                  <p>{{ selectedBlog.status === '已成稿' ? '可直接切到原文阅读' : '当前展示规划稿，正式正文后续补入' }}</p>
                </article>
              </div>

              <div v-else class="article-original">
                <div class="article-link-row">
                  <span>{{ selectedBlog.blogUrl ? '博客原文链接' : '博客链接待配置' }}</span>
                  <a v-if="selectedBlog.blogUrl" class="button secondary" :href="selectedBlog.blogUrl" target="_blank" rel="noreferrer">打开博客</a>
                  <button v-else class="button secondary" type="button" disabled>发布后挂链接</button>
                </div>
                <div class="markdown-preview">
                  <div
                    v-for="(line, index) in markdownPreviewLines"
                    :key="`${selectedBlog.id}-${index}`"
                    :class="markdownLineClass(line)"
                  >
                    {{ markdownLineText(line) }}
                  </div>
                </div>
              </div>
            </aside>
          </section>
        </section>
        <nav class="mobile-action-bar" aria-label="移动端测试入口">
          <button class="button primary" type="button" @click="goPractice">开始实操</button>
          <button class="button secondary" type="button" @click="activeView = 'evidence'">查看证据</button>
        </nav>
      </section>

      <section v-else-if="activeView === 'test-run'" class="view-stack">
        <section class="execution-grid">
          <aside class="panel login-card">
            <div class="section-head">
              <div>
                <span class="eyebrow">Session</span>
                <h2>测试账号</h2>
              </div>
              <StatusBadge :label="currentUser ? currentUser.roleCode : '未登录'" tone="neutral" />
            </div>
            <label>用户名<input v-model="username" data-testid="login-username" /></label>
            <label>密码<input v-model="password" type="password" data-testid="login-password" /></label>
            <button class="button primary" :disabled="busy" data-testid="login-submit" @click="loginAs()">登录并加载工作台</button>
            <div class="quick-actions">
              <button class="button secondary" :disabled="busy" @click="loginAs('student01')">学生</button>
              <button class="button secondary" :disabled="busy" data-testid="login-admin" @click="loginAs('admin01')">管理员</button>
            </div>
            <div v-if="currentUser" class="session-box">
              <strong>{{ currentUser.displayName }}</strong>
              <span>{{ currentUser.username }} · {{ statusLabel(currentUser.status) }}</span>
            </div>
          </aside>

          <section class="scenario-board">
            <article class="scenario-card">
              <div class="scenario-head">
                <Activity :size="19" aria-hidden="true" />
                <div><h2>活动报名</h2><p>验证名额、满员、重复报名和取消报名。</p></div>
              </div>
              <div class="table-wrap compact">
                <table>
                  <tbody>
                    <tr v-for="activity in activities.slice(0, 5)" :key="activity.id">
                      <td><strong>{{ activity.title }}</strong><span>{{ activity.registeredCount }}/{{ activity.capacity }} · {{ activity.location }}</span></td>
                      <td><StatusBadge :label="activity.registered ? '已报名' : statusLabel(activity.status)" :tone="activity.registered ? 'info' : statusTone(activity.status)" /></td>
                      <td>
                        <button v-if="!activity.registered" class="button primary" :disabled="busy || !currentUser || activity.status !== 'OPEN'" data-testid="register-activity" @click="registerActivity(activity.id)">报名</button>
                        <button v-else class="button secondary" :disabled="busy" @click="cancelActivity(activity.id)">取消</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </article>

            <article class="scenario-card">
              <div class="scenario-head">
                <Building2 :size="19" aria-hidden="true" />
                <div><h2>场地预约</h2><p>验证可用、维护、时段冲突和待审核。</p></div>
              </div>
              <div class="form-row">
                <input v-model="roomReservationDate" type="date" data-testid="room-date" />
                <input v-model.number="roomStartHour" type="number" min="8" max="21" />
                <input v-model.number="roomEndHour" type="number" min="9" max="22" />
              </div>
              <div class="card-grid">
                <div v-for="room in rooms.slice(0, 4)" :key="room.id" class="mini-card">
                  <strong>{{ room.name }}</strong>
                  <span>{{ room.building }} · {{ room.capacity }} 人</span>
                  <StatusBadge :label="statusLabel(room.status)" :tone="statusTone(room.status)" />
                  <button class="button primary" :disabled="busy || !currentUser || room.status !== 'AVAILABLE'" data-testid="reserve-room" @click="reserveRoom(room.id)">预约</button>
                </div>
              </div>
              <div v-if="roomReservations.length" class="record-strip">
                <span v-for="item in roomReservations" :key="item.id">{{ item.roomName }} · {{ item.reservationDate }} · {{ statusLabel(item.status) }}</span>
              </div>
            </article>

            <article class="scenario-card">
              <div class="scenario-head">
                <Boxes :size="19" aria-hidden="true" />
                <div><h2>设备借用</h2><p>验证库存、重复申请和审核任务生成。</p></div>
              </div>
              <div class="form-row">
                <input v-model="deviceBorrowDate" type="date" data-testid="device-borrow-date" />
                <input v-model="deviceDueDate" type="date" data-testid="device-due-date" />
                <input v-model.number="deviceQuantity" type="number" min="1" max="9" />
              </div>
              <div class="card-grid">
                <div v-for="device in devices.slice(0, 4)" :key="device.id" class="mini-card">
                  <strong>{{ device.name }}</strong>
                  <span>{{ device.category }} · {{ device.availableQuantity }}/{{ device.totalQuantity }}</span>
                  <StatusBadge :label="statusLabel(device.status)" :tone="statusTone(device.status)" />
                  <button class="button primary" :disabled="busy || !currentUser || device.status !== 'AVAILABLE' || device.availableQuantity <= 0" data-testid="borrow-device" @click="borrowDevice(device.id)">借用</button>
                </div>
              </div>
              <div v-if="deviceBorrows.length" class="record-strip">
                <span v-for="item in deviceBorrows" :key="item.id">{{ item.deviceName }} x{{ item.quantity }} · {{ statusLabel(item.status) }}</span>
              </div>
            </article>

            <article class="scenario-card wide">
              <div class="scenario-head">
                <BookOpen :size="19" aria-hidden="true" />
                <div><h2>BookNest 借阅</h2><p>验证检索、库存、借阅、续借和归还。</p></div>
              </div>
              <div class="search-row">
                <input v-model="bookKeyword" placeholder="按书名、分类、ISBN 检索" data-testid="book-keyword" />
                <button class="button secondary" :disabled="busy" data-testid="book-search" @click="loadWorkspace()"><Search :size="16" />检索</button>
                <span>{{ bookAvailability.available }}/{{ bookAvailability.total }} 可借</span>
              </div>
              <div class="card-grid four">
                <div v-for="book in books.slice(0, 8)" :key="book.id" class="mini-card">
                  <strong>{{ book.title }}</strong>
                  <span>{{ book.category }} · {{ book.availableCopies }}/{{ book.totalCopies }}</span>
                  <button class="button primary" :disabled="busy || !currentUser || book.availableCopies <= 0" data-testid="borrow-book" @click="borrowBook(book.id)">借阅</button>
                </div>
              </div>
              <div v-if="borrows.length" class="table-wrap compact">
                <table>
                  <tbody>
                    <tr v-for="borrow in borrows" :key="borrow.id">
                      <td><strong>{{ borrow.title }}</strong><span>{{ borrow.dueAt }} · 续借 {{ borrow.renewCount }}/1</span></td>
                      <td><StatusBadge :label="statusLabel(borrow.status)" :tone="statusTone(borrow.status)" /></td>
                      <td>
                        <button class="button secondary" :disabled="busy || borrow.status !== 'BORROWED' || borrow.renewCount >= 1" data-testid="renew-book" @click="renewBorrow(borrow.id)">续借</button>
                        <button class="button secondary" :disabled="busy || !['BORROWED', 'OVERDUE'].includes(borrow.status)" data-testid="return-book" @click="returnBorrow(borrow.id)">归还</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </article>

            <article class="scenario-card">
              <div class="scenario-head">
                <Bell :size="19" aria-hidden="true" />
                <div><h2>消息通知</h2><p>验证业务动作通知和本人已读。</p></div>
              </div>
              <div class="record-list">
                <div v-for="item in notifications" :key="item.id" class="record-row">
                  <span>{{ item.title }}</span>
                  <StatusBadge :label="item.readFlag ? '已读' : '未读'" :tone="item.readFlag ? 'neutral' : 'info'" />
                  <button class="button secondary" :disabled="busy || item.readFlag" data-testid="read-notification" @click="markNotificationRead(item.id)">已读</button>
                </div>
                <p v-if="!notifications.length" class="empty-note">登录并执行一次业务动作后展示通知。</p>
              </div>
            </article>

            <article class="scenario-card">
              <div class="scenario-head">
                <ClipboardList :size="19" aria-hidden="true" />
                <div><h2>后台审核</h2><p>验证管理员通过、驳回和任务状态。</p></div>
              </div>
              <div v-if="isReviewer" class="record-list">
                <div v-for="task in reviewTasks" :key="task.id" class="record-row">
                  <span>{{ task.title }}</span>
                  <StatusBadge :label="statusLabel(task.status)" :tone="statusTone(task.status)" />
                  <button class="button primary" :disabled="busy || task.status !== 'PENDING'" data-testid="approve-task" @click="decideTask(task.id, 'APPROVED')">通过</button>
                  <button class="button danger" :disabled="busy || task.status !== 'PENDING'" @click="decideTask(task.id, 'REJECTED')">驳回</button>
                </div>
              </div>
              <p v-else class="empty-note">用 admin01 登录后查看审核任务。</p>
            </article>
          </section>
        </section>
      </section>

      <section v-else class="view-stack">
        <section class="asset-hero panel">
          <div>
            <span class="eyebrow">Evidence library</span>
            <h2>文章、测试资产和运行证据</h2>
            <p>这里把测试文章需要的需求、用例、缺陷、自动化截图和性能数据统一映射到真实文件。</p>
          </div>
          <TerminalSquare :size="28" aria-hidden="true" />
        </section>
        <section class="data-boundary panel">
          <div>
            <span class="eyebrow">Data boundary</span>
            <h2>当前证据数据来源</h2>
            <p>{{ qualityDashboard.datasetNote }}</p>
          </div>
          <div class="boundary-grid">
            <span><strong>{{ qualityDashboard.dataMode }}</strong>数据模式</span>
            <span><strong>{{ qualityDashboard.generatedAt }}</strong>生成时间</span>
            <span><strong>{{ qualityDashboard.summary.qualityReason }}</strong>质量结论</span>
          </div>
        </section>
        <section class="panel trace-matrix">
          <div class="section-head">
            <div>
              <span class="eyebrow">Article traceability</span>
              <h2>文章-证据追踪矩阵</h2>
              <p>每篇文章都能回到模块、测试主题、用例、截图、缺陷和性能证据。</p>
            </div>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>文章</th>
                  <th>模块</th>
                  <th>测试主题</th>
                  <th>用例</th>
                  <th>缺陷</th>
                  <th>截图</th>
                  <th>性能</th>
                  <th>状态</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in evidenceMatrix" :key="item.id">
                  <td><strong>{{ String(item.id).padStart(2, '0') }} {{ item.title }}</strong></td>
                  <td>{{ item.module }}</td>
                  <td>{{ item.theme }}</td>
                  <td>{{ item.caseCount ? `${item.caseCount} 条` : '待补充' }}</td>
                  <td>{{ item.bugCount ? `${item.bugCount} 条` : '无' }}</td>
                  <td>{{ item.screenshotCount ? `${item.screenshotCount} 张` : '待补充' }}</td>
                  <td>{{ item.hasPerformance ? qualityDashboard.performance.scenarioId : '不适用' }}</td>
                  <td><StatusBadge :label="item.status" :tone="item.status === '可跟做' ? 'success' : 'neutral'" /></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        <section class="article-map">
          <article class="map-card"><strong>需求分析</strong><span>docs/requirements.md</span></article>
          <article class="map-card"><strong>用例设计</strong><span>test-assets/test-cases/...</span></article>
          <article class="map-card"><strong>缺陷管理</strong><span>test-assets/bug-reports/...</span></article>
          <article class="map-card"><strong>接口测试</strong><span>docs/api-contract.md · Postman</span></article>
          <article class="map-card"><strong>自动化测试</strong><span>Selenium 脚本和截图</span></article>
          <article class="map-card"><strong>性能测试</strong><span>JMeter · 性能探针 · JTL</span></article>
        </section>
        <TestCaseEvidenceTable :cases="qualityDashboard.testCases" />
        <AutomationEvidenceViewer :latest-run="qualityDashboard.automation.latestRun" :screenshots="qualityDashboard.automation.screenshots" />
        <PerformanceTrendChart :performance="qualityDashboard.performance" :theme="theme" />
        <RunEvidenceStrip :commands="qualityDashboard.runEvidence.commands" />
        <RiskQueue :bugs="qualityDashboard.bugs" />
      </section>
    </section>

    <aside
      v-if="isPracticeGuideOpen && activeView === 'test-run'"
      class="floating-guide"
      :class="[`floating-guide-${floatingGuideSize}`, { dragging: isDraggingFloatingGuide }]"
      :style="floatingGuideStyle()"
    >
      <div
        class="floating-guide-head"
        @pointerdown="startFloatingGuideDrag"
        @pointermove="moveFloatingGuide"
        @pointerup="stopFloatingGuideDrag"
        @pointercancel="stopFloatingGuideDrag"
      >
        <div>
          <span class="eyebrow">跟做指南</span>
          <strong>{{ String(selectedBlog.id).padStart(2, '0') }} {{ selectedBlog.module }}</strong>
        </div>
        <div class="floating-guide-actions">
          <button class="button secondary" type="button" @pointerdown.stop @click="backToBlogConsole">返回</button>
          <select v-model="floatingGuideSize" class="floating-size-select" @pointerdown.stop>
            <option value="compact">小</option>
            <option value="normal">中</option>
            <option value="wide">大</option>
          </select>
          <button class="icon-button" type="button" @pointerdown.stop @click="isPracticeGuideOpen = false">×</button>
        </div>
      </div>
      <div class="floating-step-list">
        <article v-for="(step, index) in selectedWalkthrough" :key="`float-${step.title}`" class="floating-step">
          <span>{{ index + 1 }}</span>
          <div>
            <strong>{{ step.title }}</strong>
            <p><b>去哪里：</b>{{ step.target }}</p>
            <p><b>按哪个控件：</b>{{ controlHint(step) }}</p>
            <p><b>怎么做：</b>{{ step.action }}</p>
            <p><b>看哪里：</b>{{ observeHint(step) }}</p>
            <p><b>应该看到：</b>{{ step.expected }}</p>
          </div>
        </article>
      </div>
    </aside>
  </main>
</template>
