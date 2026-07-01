import { computed, ref } from 'vue'

const apiBaseUrl = import.meta.env.VITE_DIRECT_API_BASE_URL ?? ''

function localDateAfter(days: number) {
  const date = new Date()
  date.setDate(date.getDate() + days)
  const offsetDate = new Date(date.getTime() - date.getTimezoneOffset() * 60_000)
  return offsetDate.toISOString().slice(0, 10)
}

type ModuleSummary = { name: string; scope: string; testingValue: string }
export type OverviewResponse = { project: string; version: string; modules: ModuleSummary[]; statistics: Record<string, number> }
export type UserItem = { id: number; username: string; displayName: string; roleCode: string; status: string }
export type LoginResponse = { token: string; user: UserItem; permissions: string[] }
export type ActivityItem = { id: number; title: string; organizer: string; location: string; capacity: number; registeredCount: number; status: string; registered: boolean }
export type RoomItem = { id: number; name: string; building: string; capacity: number; status: string; activeReservations: number }
export type RoomReservationItem = { id: number; roomName: string; reservationDate: string; startHour: number; endHour: number; status: string }
export type DeviceItem = { id: number; name: string; category: string; totalQuantity: number; availableQuantity: number; status: string }
export type DeviceBorrowItem = { id: number; deviceName: string; quantity: number; status: string; borrowedAt: string; dueAt: string }
export type BookItem = { id: number; isbn: string; title: string; author: string; category: string; totalCopies: number; availableCopies: number }
export type BookBorrowItem = { id: number; title: string; status: string; borrowedAt: string; dueAt: string; renewCount: number }
export type ReviewTaskItem = { id: number; taskType: string; title: string; applicant: string; status: string; reviewer: string | null; comment: string | null }
export type NotificationItem = { id: number; title: string; readFlag: boolean }
type ActionResponse = { code: string; message: string }

type CampusHubApiOptions = {
  onLoginSuccess?: () => void
}

export function useCampusHubApi(options: CampusHubApiOptions = {}) {
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
  const roomReservationDate = ref(localDateAfter(1))
  const roomStartHour = ref(9)
  const roomEndHour = ref(11)
  const deviceBorrowDate = ref(localDateAfter(0))
  const deviceDueDate = ref(localDateAfter(7))
  const deviceQuantity = ref(1)

  const busy = ref(false)
  const errorMessage = ref('')
  const successMessage = ref('')

  const currentUser = computed(() => session.value?.user ?? null)
  const isReviewer = computed(() => session.value?.permissions.includes('REVIEW_TASK_DECIDE') ?? false)
  const unreadCount = computed(() => notifications.value.filter((item) => !item.readFlag).length)
  const bookAvailability = computed(() => {
    const total = books.value.reduce((sum, item) => sum + item.totalCopies, 0)
    const available = books.value.reduce((sum, item) => sum + item.availableCopies, 0)
    return { total, available }
  })

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
      options.onLoginSuccess?.()
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

  async function request<T>(url: string, requestOptions: RequestInit = {}): Promise<T> {
    const response = await fetch(`${apiBaseUrl}${url}`, {
      headers: { 'Content-Type': 'application/json', ...(requestOptions.headers ?? {}) },
      ...requestOptions
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

  return {
    overview,
    session,
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
    unreadCount,
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
  }
}
