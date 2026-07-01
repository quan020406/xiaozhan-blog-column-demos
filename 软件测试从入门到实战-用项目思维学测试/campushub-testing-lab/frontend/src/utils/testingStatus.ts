export type StatusTone = 'success' | 'info' | 'warning' | 'danger' | 'blocked' | 'neutral'

export function statusLabel(status: string) {
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
    ACTIVE: '正常',
    passed: '通过',
    failed: '失败',
    blocked: '阻塞',
    skipped: '待执行',
    sample: '需复核',
    captured: '通过',
    missing: '证据缺失',
    running: '执行中'
  }
  return labels[status] ?? status
}

export function statusTone(status: string): StatusTone {
  if (['OPEN', 'APPROVED', 'RETURNED', 'ACTIVE', 'AVAILABLE', 'passed', 'captured'].includes(status)) return 'success'
  if (['PENDING', 'BORROWED', 'RESERVED', 'running'].includes(status)) return 'info'
  if (['OVERDUE', 'FULL', 'CLOSED', 'OUT_OF_STOCK', 'skipped', 'missing', 'sample'].includes(status)) return 'warning'
  if (['REJECTED', 'failed'].includes(status)) return 'danger'
  if (['blocked'].includes(status)) return 'blocked'
  return 'neutral'
}

export function qualityGateLabel(status: string) {
  if (status === 'passed') return '通过'
  if (status === 'blocked') return '阻塞'
  if (status === 'failed') return '失败'
  return '需复核'
}

export function qualityGateTone(status: string): StatusTone {
  if (status === 'passed') return 'success'
  if (status === 'blocked') return 'blocked'
  if (status === 'failed') return 'danger'
  return 'warning'
}
