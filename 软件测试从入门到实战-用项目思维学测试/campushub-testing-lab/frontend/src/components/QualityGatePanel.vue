<script setup lang="ts">
import { ShieldAlert, ShieldCheck, ShieldX } from 'lucide-vue-next'
import StatusBadge from './StatusBadge.vue'

type Summary = {
  totalCases: number
  passed: number
  failed: number
  blocked: number
  skipped: number
  passRate: number
  openBugs: number
  criticalBugs: number
  performanceStatus: string
  qualityGate: string
  qualityScore: number
  qualityReason: string
}

const props = defineProps<{ summary: Summary }>()

function gateMeta() {
  if (props.summary.qualityGate === 'passed') {
    return { label: '可发布', tone: 'success' as const, icon: ShieldCheck }
  }
  if (props.summary.qualityGate === 'blocked') {
    return { label: '阻塞', tone: 'danger' as const, icon: ShieldX }
  }
  return { label: '需复核', tone: 'warning' as const, icon: ShieldAlert }
}
</script>

<template>
  <section class="quality-gate" :class="`gate-${gateMeta().tone}`" data-testid="quality-gate-panel">
    <div class="gate-main">
      <div class="gate-icon">
        <component :is="gateMeta().icon" :size="30" aria-hidden="true" />
      </div>
      <div>
        <span class="eyebrow">Release gate</span>
        <h2>{{ gateMeta().label }}</h2>
        <p>{{ summary.qualityReason }}</p>
      </div>
    </div>

    <div class="gate-score">
      <strong>{{ summary.qualityScore }}</strong>
      <span>/ 100</span>
      <StatusBadge :label="gateMeta().label" :tone="gateMeta().tone" />
    </div>

    <div class="gate-metrics">
      <span><strong>{{ summary.passed }}/{{ summary.totalCases }}</strong>用例通过</span>
      <span><strong>{{ summary.openBugs }}</strong>真实开放缺陷</span>
      <span><strong>{{ summary.performanceStatus }}</strong>性能状态</span>
    </div>
  </section>
</template>
