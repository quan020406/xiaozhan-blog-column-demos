<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Activity, Bell, BookOpen, Boxes, Building2, ClipboardList, FileText, LogIn, Moon, Search, ShieldCheck, Sun, UserRound } from 'lucide-vue-next'
import StatusBadge from './components/StatusBadge.vue'
import { useCampusHubApi } from './composables/useCampusHubApi'
import { useTheme } from './composables/useTheme'
import { statusLabel, statusTone } from './utils/testingStatus'

type ActiveSection = 'activities' | 'books' | 'rooms' | 'devices' | 'notifications' | 'records' | 'admin' | 'assets'

const loading = ref(true)
const activeSection = ref<ActiveSection>('activities')
const { theme, initTheme, toggleTheme } = useTheme()

const {
  overview,
  activities,
  rooms,
  roomReservations,
  devices,
  deviceBorrows,
  notifications,
  books,
  borrows,
  reviewTasks,
  username,
  password,
  bookKeyword,
  roomReservationDate,
  roomStartHour,
  roomEndHour,
  deviceBorrowDate,
  deviceDueDate,
  deviceQuantity,
  busy,
  errorMessage,
  successMessage,
  currentUser,
  isReviewer,
  bookAvailability,
  loadOverview,
  loginAs,
  loadWorkspace,
  registerActivity,
  cancelActivity,
  reserveRoom,
  borrowDevice,
  markNotificationRead,
  borrowBook,
  renewBorrow,
  returnBorrow,
  decideTask
} = useCampusHubApi({
  onLoginSuccess: () => {
    activeSection.value = 'activities'
  }
})

const registeredActivities = computed(() => activities.value.filter((item) => item.registered))
const unreadNotifications = computed(() => notifications.value.filter((item) => !item.readFlag))
const lowStockBooks = computed(() => books.value.filter((item) => item.availableCopies <= 1).slice(0, 5))
const adminActivityRows = computed(() => activities.value.slice(0, 5))
const adminBookRows = computed(() => books.value.slice(0, 5))
const isAdmin = computed(() => currentUser.value?.roleCode === 'SYSTEM_ADMIN')
const currentRoleLabel = computed(() => {
  if (!currentUser.value) return '未登录'
  return currentUser.value.roleCode === 'SYSTEM_ADMIN' ? '管理员' : '学生'
})

const navItems = [
  { id: 'activities' as ActiveSection, label: '活动列表', icon: Activity },
  { id: 'books' as ActiveSection, label: '图书列表', icon: BookOpen },
  { id: 'rooms' as ActiveSection, label: '场地预约', icon: Building2 },
  { id: 'devices' as ActiveSection, label: '设备借用', icon: Boxes },
  { id: 'notifications' as ActiveSection, label: '消息通知', icon: Bell },
  { id: 'records' as ActiveSection, label: '我的记录', icon: ClipboardList },
  { id: 'admin' as ActiveSection, label: '管理员入口', icon: ShieldCheck },
  { id: 'assets' as ActiveSection, label: '测试素材', icon: FileText }
]

const projectAssets = [
  { title: '需求说明', path: 'docs/requirements.md' },
  { title: '测试用例', path: 'test-assets/test-cases/core-cases.md' },
  { title: 'Bug 报告', path: 'test-assets/bug-reports/sample-activity-registration-full.md' },
  { title: '接口集合', path: 'test-assets/postman/campushub.postman_collection.json' },
  { title: '已知缺陷', path: 'test-assets/known-defects.md' },
  { title: '01-26 素材追踪', path: 'test-assets/article-evidence-map.md' },
  { title: 'Selenium 脚本', path: 'test-assets/selenium/test_login_activity_book.py' },
  { title: 'JMeter 脚本', path: 'test-assets/jmeter/campushub-activity-booknest-smoke.jmx' }
]

onMounted(async () => {
  initTheme()
  await loadOverview()
  await loadWorkspace()
  loading.value = false
})

async function submitLogin(nextUsername?: string) {
  errorMessage.value = ''
  successMessage.value = ''
  if (nextUsername) {
    await loginAs(nextUsername)
    return
  }
  if (!username.value.trim()) {
    errorMessage.value = '请输入用户名'
    return
  }
  if (!password.value.trim()) {
    errorMessage.value = '请输入密码'
    return
  }
  await loginAs()
}

async function searchBooks() {
  await loadWorkspace()
  activeSection.value = 'books'
}
</script>

<template>
  <main class="lite-shell">
    <header class="lite-topbar">
      <div>
        <span class="eyebrow">CampusHub Testing Lab</span>
        <h1>校园服务协作平台</h1>
        <p>按 01-26 期文章顺序承载登录、活动、BookNest、场地、设备、通知、审核、自动化和性能测试练习。</p>
      </div>
      <div class="lite-topbar-actions">
        <div class="service-pill" data-testid="service-status">
          <span class="pulse" :class="{ warn: loading || errorMessage }"></span>
          <span>{{ loading ? '连接后端' : errorMessage ? '接口异常' : '后端在线' }}</span>
        </div>
        <button
          class="icon-button"
          type="button"
          data-testid="theme-toggle"
          :aria-label="theme === 'light' ? '切换到深色主题' : '切换到浅色主题'"
          @click="toggleTheme"
        >
          <Moon v-if="theme === 'light'" :size="18" aria-hidden="true" />
          <Sun v-else :size="18" aria-hidden="true" />
        </button>
      </div>
    </header>

    <p v-if="errorMessage" class="message error-message" role="alert" data-testid="error-message">{{ errorMessage }}</p>
    <p v-if="successMessage" class="message success-message" role="status" aria-live="polite" data-testid="success-message">{{ successMessage }}</p>

    <section class="lite-hero">
      <aside class="panel lite-login-card">
        <div class="section-head">
          <div>
            <span class="eyebrow">登录入口</span>
            <h2>学生 / 管理员</h2>
          </div>
          <StatusBadge :label="currentRoleLabel" tone="neutral" />
        </div>
        <label>用户名<input v-model="username" data-testid="login-username" autocomplete="username" /></label>
        <label>密码<input v-model="password" type="password" data-testid="login-password" autocomplete="current-password" /></label>
        <button class="button primary" :disabled="busy" data-testid="login-submit" @click="submitLogin()">
          <LogIn :size="16" aria-hidden="true" />登录
        </button>
        <div class="quick-actions">
          <button class="button secondary" :disabled="busy" @click="submitLogin('student01')">学生账号</button>
          <button class="button secondary" :disabled="busy" data-testid="login-admin" @click="submitLogin('admin01')">管理员账号</button>
        </div>
        <div v-if="currentUser" class="session-box">
          <UserRound :size="18" aria-hidden="true" />
          <div>
            <strong>{{ currentUser.displayName }}</strong>
            <span>{{ currentUser.username }} · {{ statusLabel(currentUser.status) }}</span>
          </div>
        </div>
      </aside>

      <section class="panel lite-overview-card">
        <span class="eyebrow">业务概览</span>
        <h2>{{ overview?.project ?? 'CampusHub Testing Lab' }}</h2>
        <div class="lite-stat-grid">
          <span><strong>{{ overview?.statistics.activities ?? 0 }}</strong>活动</span>
          <span><strong>{{ overview?.statistics.books ?? 0 }}</strong>图书</span>
          <span><strong>{{ overview?.statistics.rooms ?? 0 }}</strong>场地</span>
          <span><strong>{{ overview?.statistics.devices ?? 0 }}</strong>设备</span>
        </div>
        <p>读者先完成真实业务操作，再回到测试素材查看需求、用例、Bug、接口、Selenium 和 JMeter 练习。</p>
      </section>
    </section>

    <nav class="lite-nav" aria-label="CampusHub 导航">
      <button
        v-for="item in navItems"
        :key="item.id"
        type="button"
        class="lite-nav-button"
        :class="{ active: activeSection === item.id }"
        @click="activeSection = item.id"
      >
        <component :is="item.icon" :size="18" aria-hidden="true" />
        <span>{{ item.label }}</span>
      </button>
    </nav>

    <section v-if="activeSection === 'activities'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">活动报名</span>
          <h2>活动列表</h2>
        </div>
      </div>
      <div class="lite-card-grid">
        <article v-for="activity in activities" :key="activity.id" class="business-card">
          <div class="business-card-head">
            <strong>{{ activity.title }}</strong>
            <StatusBadge :label="activity.registered ? '已报名' : statusLabel(activity.status)" :tone="activity.registered ? 'info' : statusTone(activity.status)" />
          </div>
          <p>{{ activity.organizer }} · {{ activity.location }}</p>
          <span class="metric-line">{{ activity.registeredCount }}/{{ activity.capacity }} 人已报名</span>
          <button
            v-if="!activity.registered"
            class="button primary"
            :disabled="busy || !currentUser || activity.status !== 'OPEN'"
            data-testid="register-activity"
            @click="registerActivity(activity.id)"
          >
            报名
          </button>
          <button v-else class="button secondary" :disabled="busy" @click="cancelActivity(activity.id)">取消报名</button>
        </article>
      </div>
    </section>

    <section v-else-if="activeSection === 'books'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">BookNest</span>
          <h2>图书列表</h2>
        </div>
        <div class="search-row">
          <input v-model="bookKeyword" aria-label="BookNest 图书检索关键词" placeholder="书名、分类、ISBN" data-testid="book-keyword" />
          <button class="button secondary" :disabled="busy" data-testid="book-search" @click="searchBooks">
            <Search :size="16" aria-hidden="true" />检索
          </button>
        </div>
      </div>
      <div class="lite-card-grid">
        <article v-for="book in books" :key="book.id" class="business-card">
          <div class="business-card-head">
            <strong>{{ book.title }}</strong>
            <StatusBadge :label="book.availableCopies > 0 ? '可借' : '无库存'" :tone="book.availableCopies > 0 ? 'success' : 'danger'" />
          </div>
          <p>{{ book.author }} · {{ book.category }}</p>
          <span class="metric-line">{{ book.availableCopies }}/{{ book.totalCopies }} 本可借</span>
          <button class="button primary" :disabled="busy || !currentUser || book.availableCopies <= 0" data-testid="borrow-book" @click="borrowBook(book.id)">借阅</button>
        </article>
      </div>
    </section>

    <section v-else-if="activeSection === 'rooms'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">场地预约</span>
          <h2>时段冲突和审核流转</h2>
        </div>
        <div class="form-row">
          <input v-model="roomReservationDate" type="date" aria-label="场地预约日期" data-testid="room-date" />
          <input v-model.number="roomStartHour" type="number" min="8" max="21" aria-label="开始小时" />
          <input v-model.number="roomEndHour" type="number" min="9" max="22" aria-label="结束小时" />
        </div>
      </div>
      <div class="lite-card-grid">
        <article v-for="room in rooms" :key="room.id" class="business-card">
          <div class="business-card-head">
            <strong>{{ room.name }}</strong>
            <StatusBadge :label="statusLabel(room.status)" :tone="statusTone(room.status)" />
          </div>
          <p>{{ room.building }} · 容量 {{ room.capacity }} 人</p>
          <span class="metric-line">有效预约 {{ room.activeReservations }} 条</span>
          <button class="button primary" :disabled="busy || !currentUser || room.status !== 'AVAILABLE'" data-testid="reserve-room" @click="reserveRoom(room.id)">预约</button>
        </article>
      </div>
    </section>

    <section v-else-if="activeSection === 'devices'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">设备借用</span>
          <h2>库存、重复申请和审核任务</h2>
        </div>
        <div class="form-row">
          <input v-model="deviceBorrowDate" type="date" aria-label="设备借用日期" data-testid="device-borrow-date" />
          <input v-model="deviceDueDate" type="date" aria-label="设备归还日期" data-testid="device-due-date" />
          <input v-model.number="deviceQuantity" type="number" min="1" max="9" aria-label="设备借用数量" />
        </div>
      </div>
      <div class="lite-card-grid">
        <article v-for="device in devices" :key="device.id" class="business-card">
          <div class="business-card-head">
            <strong>{{ device.name }}</strong>
            <StatusBadge :label="statusLabel(device.status)" :tone="statusTone(device.status)" />
          </div>
          <p>{{ device.category }}</p>
          <span class="metric-line">{{ device.availableQuantity }}/{{ device.totalQuantity }} 可借</span>
          <button class="button primary" :disabled="busy || !currentUser || device.status !== 'AVAILABLE' || device.availableQuantity <= 0" data-testid="borrow-device" @click="borrowDevice(device.id)">借用</button>
        </article>
      </div>
    </section>

    <section v-else-if="activeSection === 'notifications'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">消息通知</span>
          <h2>业务反馈和已读状态</h2>
        </div>
        <StatusBadge :label="`${unreadNotifications.length} 条未读`" :tone="unreadNotifications.length ? 'info' : 'neutral'" />
      </div>
      <div class="record-list">
        <div v-for="item in notifications" :key="item.id" class="record-row">
          <span>{{ item.title }}</span>
          <StatusBadge :label="item.readFlag ? '已读' : '未读'" :tone="item.readFlag ? 'neutral' : 'info'" />
          <button class="button secondary" :disabled="busy || item.readFlag" data-testid="read-notification" @click="markNotificationRead(item.id)">标记已读</button>
        </div>
        <p v-if="!notifications.length" class="empty-note">登录并执行一次报名、预约、借用或借阅后展示通知。</p>
      </div>
    </section>

    <section v-else-if="activeSection === 'records'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">我的记录</span>
          <h2>报名和借阅</h2>
        </div>
      </div>
      <div class="records-grid">
        <article class="panel">
          <h3>活动报名记录</h3>
          <div class="record-list">
            <div v-for="activity in registeredActivities" :key="activity.id" class="record-row">
              <span>{{ activity.title }}</span>
              <StatusBadge label="已报名" tone="info" />
            </div>
            <p v-if="!registeredActivities.length" class="empty-note">当前账号还没有活动报名记录。</p>
          </div>
        </article>
        <article class="panel">
          <h3>图书借阅记录</h3>
          <div class="record-list">
            <div v-for="borrow in borrows" :key="borrow.id" class="record-row">
              <span>{{ borrow.title }} · 到期 {{ borrow.dueAt }}</span>
              <StatusBadge :label="statusLabel(borrow.status)" :tone="statusTone(borrow.status)" />
              <button class="button secondary" :disabled="busy || borrow.status !== 'BORROWED' || borrow.renewCount >= 1" data-testid="renew-book" @click="renewBorrow(borrow.id)">续借</button>
              <button class="button secondary" :disabled="busy || !['BORROWED', 'OVERDUE'].includes(borrow.status)" data-testid="return-book" @click="returnBorrow(borrow.id)">归还</button>
            </div>
            <p v-if="!borrows.length" class="empty-note">当前账号还没有图书借阅记录。</p>
          </div>
        </article>
        <article class="panel">
          <h3>场地预约记录</h3>
          <div class="record-list">
            <div v-for="item in roomReservations" :key="item.id" class="record-row">
              <span>{{ item.roomName }} · {{ item.reservationDate }} {{ item.startHour }}:00-{{ item.endHour }}:00</span>
              <StatusBadge :label="statusLabel(item.status)" :tone="statusTone(item.status)" />
            </div>
            <p v-if="!roomReservations.length" class="empty-note">当前账号还没有场地预约记录。</p>
          </div>
        </article>
        <article class="panel">
          <h3>设备借用记录</h3>
          <div class="record-list">
            <div v-for="item in deviceBorrows" :key="item.id" class="record-row">
              <span>{{ item.deviceName }} x{{ item.quantity }} · {{ item.borrowedAt }} 至 {{ item.dueAt }}</span>
              <StatusBadge :label="statusLabel(item.status)" :tone="statusTone(item.status)" />
            </div>
            <p v-if="!deviceBorrows.length" class="empty-note">当前账号还没有设备借用记录。</p>
          </div>
        </article>
      </div>
    </section>

    <section v-else-if="activeSection === 'admin'" class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">管理员入口</span>
          <h2>审核与统计简表</h2>
        </div>
        <StatusBadge :label="isAdmin ? '允许查看' : '需要管理员'" :tone="isAdmin ? 'success' : 'warning'" />
      </div>
      <p v-if="!isAdmin" class="empty-note">请使用 `admin01 / campus123` 登录后查看活动报名统计、图书库存和异常样例。</p>
      <div v-else class="admin-grid">
        <article class="panel">
          <h3>活动报名统计</h3>
          <div class="record-list">
            <div v-for="activity in adminActivityRows" :key="activity.id" class="record-row">
              <span>{{ activity.title }}</span>
              <strong>{{ activity.registeredCount }}/{{ activity.capacity }}</strong>
            </div>
          </div>
        </article>
        <article class="panel">
          <h3>图书库存简表</h3>
          <div class="record-list">
            <div v-for="book in adminBookRows" :key="book.id" class="record-row">
              <span>{{ book.title }}</span>
              <strong>{{ book.availableCopies }}/{{ book.totalCopies }}</strong>
            </div>
          </div>
        </article>
        <article class="panel">
          <h3>异常样例</h3>
          <div class="record-list">
            <div v-for="book in lowStockBooks" :key="book.id" class="record-row">
              <span>{{ book.title }}</span>
              <StatusBadge label="低库存" tone="warning" />
            </div>
            <div v-if="isReviewer && reviewTasks.length" class="record-row">
              <span>待观察审核任务</span>
              <strong>{{ reviewTasks.length }} 条</strong>
            </div>
          </div>
        </article>
        <article class="panel">
          <h3>审核任务</h3>
          <div class="record-list">
            <div v-for="task in reviewTasks" :key="task.id" class="record-row">
              <span>{{ task.title }} · {{ task.applicant }}</span>
              <StatusBadge :label="statusLabel(task.status)" :tone="statusTone(task.status)" />
              <button class="button primary" :disabled="busy || task.status !== 'PENDING'" data-testid="approve-task" @click="decideTask(task.id, 'APPROVED')">通过</button>
              <button class="button danger" :disabled="busy || task.status !== 'PENDING'" @click="decideTask(task.id, 'REJECTED')">驳回</button>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section v-else class="lite-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">辅助入口</span>
          <h2>01-26 项目素材</h2>
        </div>
      </div>
      <div class="asset-list">
        <article v-for="asset in projectAssets" :key="asset.path" class="business-card">
          <strong>{{ asset.title }}</strong>
          <code>{{ asset.path }}</code>
        </article>
      </div>
    </section>
  </main>
</template>
