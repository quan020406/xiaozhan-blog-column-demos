<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type ModuleSummary = {
  name: string
  scope: string
  testingValue: string
}

type OverviewResponse = {
  project: string
  version: string
  modules: ModuleSummary[]
  statistics: Record<string, number>
}

type UserItem = {
  id: number
  username: string
  displayName: string
  roleCode: string
  status: string
}

type LoginResponse = {
  token: string
  user: UserItem
  permissions: string[]
}

type ActivityItem = {
  id: number
  title: string
  organizer: string
  location: string
  capacity: number
  registeredCount: number
  status: string
  registered: boolean
}

type BookItem = {
  id: number
  isbn: string
  title: string
  author: string
  category: string
  totalCopies: number
  availableCopies: number
}

type BookBorrowItem = {
  id: number
  title: string
  status: string
  borrowedAt: string
  dueAt: string
  renewCount: number
}

type ReviewTaskItem = {
  id: number
  taskType: string
  title: string
  applicant: string
  status: string
  reviewer: string | null
  comment: string | null
}

type ActionResponse = {
  code: string
  message: string
}

const overview = ref<OverviewResponse | null>(null)
const session = ref<LoginResponse | null>(null)
const activities = ref<ActivityItem[]>([])
const books = ref<BookItem[]>([])
const borrows = ref<BookBorrowItem[]>([])
const reviewTasks = ref<ReviewTaskItem[]>([])
const username = ref('student01')
const password = ref('campus123')
const bookKeyword = ref('')
const loading = ref(true)
const busy = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const theme = ref<'light' | 'dark'>('light')

const currentUser = computed(() => session.value?.user ?? null)
const isReviewer = computed(() => session.value?.permissions.includes('REVIEW_TASK_DECIDE') ?? false)
const bookAvailability = computed(() => {
  const total = books.value.reduce((sum, item) => sum + item.totalCopies, 0)
  const available = books.value.reduce((sum, item) => sum + item.availableCopies, 0)
  return { total, available }
})

onMounted(async () => {
  initTheme()
  await loadOverview()
  loading.value = false
})

function initTheme() {
  const savedTheme = localStorage.getItem('campushub-theme')
  const nextTheme = savedTheme === 'dark' ? 'dark' : 'light'
  theme.value = nextTheme
  document.documentElement.dataset.theme = nextTheme
}

function toggleTheme() {
  const nextTheme = theme.value === 'light' ? 'dark' : 'light'
  theme.value = nextTheme
  document.documentElement.dataset.theme = nextTheme
  localStorage.setItem('campushub-theme', nextTheme)
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
    await loadWorkspace()
  })
}

async function loadWorkspace() {
  const activeUsername = currentUser.value?.username ?? ''
  const [nextActivities, nextBooks] = await Promise.all([
    request<ActivityItem[]>(`/api/activities?username=${encodeURIComponent(activeUsername)}`),
    request<BookItem[]>(`/api/books?keyword=${encodeURIComponent(bookKeyword.value)}`)
  ])
  activities.value = nextActivities
  books.value = nextBooks
  if (activeUsername) {
    borrows.value = await request<BookBorrowItem[]>(`/api/book-borrows?username=${encodeURIComponent(activeUsername)}`)
  }
  if (isReviewer.value) {
    reviewTasks.value = await request<ReviewTaskItem[]>('/api/admin/review-tasks')
  } else {
    reviewTasks.value = []
  }
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
  const response = await fetch(url, {
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
  if (!currentUser.value) {
    throw new Error('请先登录')
  }
  return currentUser.value.username
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    OPEN: '开放报名',
    CLOSED: '已关闭',
    BORROWED: '已借出',
    RETURNED: '已归还',
    OVERDUE: '已逾期',
    PENDING: '待审核',
    APPROVED: '已通过',
    REJECTED: '已驳回',
    ACTIVE: '正常'
  }
  return labels[status] ?? status
}

function statusTone(status: string) {
  if (['OPEN', 'APPROVED', 'RETURNED', 'ACTIVE'].includes(status)) return 'success'
  if (['PENDING', 'BORROWED'].includes(status)) return 'info'
  if (['OVERDUE', 'CLOSED'].includes(status)) return 'warning'
  if (['REJECTED'].includes(status)) return 'danger'
  return 'neutral'
}
</script>

<template>
  <main class="app-shell">
    <aside class="app-sidebar" aria-label="CampusHub 模块导航">
      <div class="brand">
        <span class="brand-mark">CH</span>
        <div>
          <strong>CampusHub</strong>
          <span>Testing Lab</span>
        </div>
      </div>
      <nav class="nav-group">
        <span class="nav-label">总览</span>
        <a class="nav-item active" href="#overview">首页</a>
        <a class="nav-item" href="#activities">活动报名</a>
        <a class="nav-item" href="#booknest">BookNest</a>
        <a class="nav-item" href="#review">后台审核</a>
      </nav>
      <div class="sidebar-note">
        <strong>教学目标</strong>
        <span>保留真实业务流和稳定测试定位，方便手工、接口和自动化测试练习。</span>
      </div>
    </aside>

    <section class="app-main">
      <header class="app-header">
        <div>
          <span class="breadcrumb">总览 / 测试实验室</span>
          <h1>校园服务协作平台测试实验室</h1>
        </div>
        <div class="header-actions">
          <div class="status-panel" data-testid="service-status">
            <span class="status-dot" :class="{ muted: loading || errorMessage }"></span>
            <span>{{ loading ? '正在连接后端' : errorMessage ? '存在待处理错误' : '后端已连接' }}</span>
          </div>
          <button class="button secondary" type="button" data-testid="theme-toggle" @click="toggleTheme">
            {{ theme === 'light' ? '深色实验室' : '浅色模式' }}
          </button>
        </div>
      </header>

      <section id="overview" class="page-hero">
        <div>
          <p class="eyebrow">CampusHub Testing Lab</p>
          <h2>从业务动作进入测试证据</h2>
          <p class="summary">
            当前版本提供登录、活动报名、BookNest 图书借阅和后台审核的最小闭环，可作为手工测试、接口测试和自动化测试练习对象。
          </p>
        </div>
        <div class="evidence-card">
          <span>下一步建议</span>
          <strong>{{ currentUser ? '执行核心流程回归' : '先使用示例账号登录' }}</strong>
          <small>学生账号 student01，管理员账号 admin01，密码均为 campus123。</small>
        </div>
      </section>

      <section v-if="overview" class="metrics-grid" aria-label="示例数据统计">
        <article v-for="(value, key) in overview.statistics" :key="key" class="metric-card">
          <span>{{ key }}</span>
          <strong>{{ value }}</strong>
        </article>
      </section>

      <p v-if="errorMessage" class="message error-message" data-testid="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="message success-message" data-testid="success-message">{{ successMessage }}</p>

      <section class="workbench">
      <aside class="panel login-panel" aria-label="演示登录">
        <div class="panel-header">
          <h2>演示登录</h2>
          <span class="status-badge neutral">{{ currentUser ? currentUser.roleCode : '未登录' }}</span>
        </div>
        <label>
          用户名
          <input v-model="username" data-testid="login-username" />
        </label>
        <label>
          密码
          <input v-model="password" type="password" data-testid="login-password" />
        </label>
        <button class="button primary" :disabled="busy" data-testid="login-submit" @click="loginAs()">登录</button>
        <div class="quick-login">
          <button class="button secondary" :disabled="busy" @click="loginAs('student01')">学生</button>
          <button class="button secondary" :disabled="busy" data-testid="login-admin" @click="loginAs('admin01')">管理员</button>
        </div>
        <div v-if="currentUser" class="user-card">
          <strong>{{ currentUser.displayName }}</strong>
          <span>{{ currentUser.username }} · {{ statusLabel(currentUser.status) }}</span>
        </div>
      </aside>

      <section class="main-panels">
        <article id="activities" class="panel">
          <div class="panel-header">
            <div>
              <h2>活动报名</h2>
              <p>查看可报名活动，验证名额、重复报名和关闭状态。</p>
            </div>
            <span>{{ activities.length }} 条活动</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>活动</th>
                <th>地点</th>
                <th>名额</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="activity in activities" :key="activity.id">
                <td>
                  <strong>{{ activity.title }}</strong>
                  <span>{{ activity.organizer }}</span>
                </td>
                <td>{{ activity.location }}</td>
                <td>{{ activity.registeredCount }}/{{ activity.capacity }}</td>
                <td>
                  <span class="status-badge" :class="activity.registered ? 'info' : statusTone(activity.status)">
                    {{ activity.registered ? '已报名' : statusLabel(activity.status) }}
                  </span>
                </td>
                <td>
                  <button
                    class="button primary"
                    v-if="!activity.registered"
                    :disabled="busy || !currentUser || activity.status !== 'OPEN'"
                    data-testid="register-activity"
                    @click="registerActivity(activity.id)"
                  >
                    提交报名
                  </button>
                  <button v-else class="button secondary" :disabled="busy" @click="cancelActivity(activity.id)">取消报名</button>
                </td>
              </tr>
            </tbody>
          </table>
        </article>

        <article id="booknest" class="panel">
          <div class="panel-header">
            <div>
              <h2>BookNest 图书借阅</h2>
              <p>按书名、分类或 ISBN 检索图书，验证库存边界和借阅动作。</p>
            </div>
            <span>可借 {{ bookAvailability.available }} / 总藏书 {{ bookAvailability.total }}</span>
          </div>
          <div class="toolbar">
            <input v-model="bookKeyword" placeholder="按书名、作者、分类或 ISBN 检索" data-testid="book-keyword" />
            <button class="button secondary" :disabled="busy" data-testid="book-search" @click="loadWorkspace()">检索图书</button>
          </div>
          <div class="book-grid">
            <div v-for="book in books" :key="book.id" class="book-item">
              <strong>{{ book.title }}</strong>
              <span>{{ book.category }} · {{ book.availableCopies }}/{{ book.totalCopies }}</span>
              <small>{{ book.isbn }}</small>
              <button
                class="button primary"
                :disabled="busy || !currentUser || book.availableCopies <= 0"
                data-testid="borrow-book"
                @click="borrowBook(book.id)"
              >
                提交借阅
              </button>
            </div>
          </div>
        </article>

        <article class="panel">
          <div class="panel-header">
            <div>
              <h2>我的借阅</h2>
              <p>检查借阅状态、应还日期和续借次数限制。</p>
            </div>
            <span>{{ borrows.length }} 条记录</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>图书</th>
                <th>状态</th>
                <th>应还日期</th>
                <th>续借</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="borrow in borrows" :key="borrow.id">
                <td>{{ borrow.title }}</td>
                <td>
                  <span class="status-badge" :class="statusTone(borrow.status)">
                    {{ statusLabel(borrow.status) }}
                  </span>
                </td>
                <td>{{ borrow.dueAt }}</td>
                <td>{{ borrow.renewCount }}/1</td>
                <td>
                  <button
                    class="button secondary"
                    :disabled="busy || borrow.status !== 'BORROWED' || borrow.renewCount >= 1"
                    data-testid="renew-book"
                    @click="renewBorrow(borrow.id)"
                  >
                    续借
                  </button>
                  <button
                    class="button secondary"
                    :disabled="busy || !['BORROWED', 'OVERDUE'].includes(borrow.status)"
                    data-testid="return-book"
                    @click="returnBorrow(borrow.id)"
                  >
                    归还
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </article>

        <article id="review" class="panel" data-testid="review-panel">
          <div class="panel-header">
            <div>
              <h2>后台审核</h2>
              <p>用管理员角色处理待审核任务，验证通过、驳回和状态流转。</p>
            </div>
            <span>{{ isReviewer ? `${reviewTasks.length} 条任务` : '需管理员角色' }}</span>
          </div>
          <table v-if="isReviewer">
            <thead>
              <tr>
                <th>任务</th>
                <th>申请人</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in reviewTasks" :key="task.id">
                <td>
                  <strong>{{ task.title }}</strong>
                  <span>{{ task.taskType }}</span>
                </td>
                <td>{{ task.applicant }}</td>
                <td>
                  <span class="status-badge" :class="statusTone(task.status)">
                    {{ statusLabel(task.status) }}
                  </span>
                </td>
                <td>
                  <button
                    class="button primary"
                    :disabled="busy || task.status !== 'PENDING'"
                    data-testid="approve-task"
                    @click="decideTask(task.id, 'APPROVED')"
                  >
                    通过
                  </button>
                  <button class="button danger" :disabled="busy || task.status !== 'PENDING'" @click="decideTask(task.id, 'REJECTED')">
                    驳回申请
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else class="empty-note">使用 `admin01 / campus123` 登录后可处理审核任务。</p>
        </article>
      </section>
    </section>
    </section>
  </main>
</template>
