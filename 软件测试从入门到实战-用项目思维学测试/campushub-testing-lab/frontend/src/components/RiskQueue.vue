<script setup lang="ts">
import { AlertTriangle } from 'lucide-vue-next'
import { ref, computed } from 'vue'
import StatusBadge from './StatusBadge.vue'

type BugItem = {
  id: string
  title: string
  module: string
  severity: string
  priority: string
  status: string
  relatedCaseId: string
  summary: string
  evidenceType?: string
  reproducePath?: string
  createdAt?: string
}

const props = defineProps<{ bugs: BugItem[] }>()
const selectedBugId = ref('')
const selectedBug = computed(() => props.bugs.find((item) => item.id === selectedBugId.value))

function severityTone(severity: string) {
  if (severity === 'critical') return 'danger'
  if (severity === 'major') return 'warning'
  return 'info'
}

function severityLabel(severity: string) {
  const labels: Record<string, string> = {
    critical: 'Critical',
    major: 'Major',
    minor: 'Minor',
    trivial: 'Trivial'
  }
  return labels[severity] ?? severity
}
</script>

<template>
  <section class="panel risk-panel" data-testid="risk-queue">
    <div class="section-head">
      <div>
        <span class="eyebrow">Defect triage</span>
        <h2>缺陷与风险队列</h2>
      </div>
      <AlertTriangle :size="20" aria-hidden="true" />
    </div>

    <div class="risk-list">
      <article v-for="bug in bugs.slice(0, 4)" :key="bug.id" class="risk-row" :class="`risk-${bug.severity}`">
        <div class="risk-title">
          <strong>{{ bug.title }}</strong>
          <StatusBadge :label="severityLabel(bug.severity)" :tone="severityTone(bug.severity)" />
        </div>
        <p>{{ bug.summary }}</p>
        <div class="risk-meta">
          <span>{{ bug.id }}</span>
          <span>{{ bug.priority }}</span>
          <span>{{ bug.status }}</span>
          <span v-if="bug.evidenceType">{{ bug.evidenceType }}</span>
        </div>
        <button class="button secondary" type="button" @click="selectedBugId = bug.id">查看复盘</button>
      </article>
    </div>

    <aside v-if="selectedBug" class="detail-drawer" aria-label="缺陷复盘详情">
      <div class="detail-drawer-head">
        <div>
          <span class="eyebrow">Bug detail</span>
          <h2>{{ selectedBug.id }}</h2>
        </div>
        <button class="icon-button" type="button" @click="selectedBugId = ''">×</button>
      </div>
      <div class="detail-grid">
        <span><strong>标题</strong>{{ selectedBug.title }}</span>
        <span><strong>严重级别</strong>{{ severityLabel(selectedBug.severity) }}</span>
        <span><strong>影响模块</strong>{{ selectedBug.module }}</span>
        <span><strong>优先级</strong>{{ selectedBug.priority }}</span>
        <span><strong>当前状态</strong>{{ selectedBug.status }}</span>
        <span><strong>关联用例</strong>{{ selectedBug.relatedCaseId || '教学样例未绑定具体用例' }}</span>
      </div>
      <section class="detail-block">
        <h3>实际结果</h3>
        <p>{{ selectedBug.summary }}</p>
      </section>
      <section class="detail-block">
        <h3>证据来源</h3>
        <p>{{ selectedBug.evidenceType ?? '未标记' }}</p>
        <code v-if="selectedBug.reproducePath">{{ selectedBug.reproducePath }}</code>
      </section>
      <section class="detail-block">
        <h3>回归标准</h3>
        <p>复现路径、预期结果和实际结果需要能被开发复查；修复后应回到关联模块执行主流程和反向用例。</p>
      </section>
    </aside>
  </section>
</template>
