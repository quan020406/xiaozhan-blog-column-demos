<script setup lang="ts">
import { computed, ref } from 'vue'
import StatusBadge from './StatusBadge.vue'

type TestCaseItem = {
  id: string
  title: string
  module: string
  type: string
  priority: string
  status: string
  executor: string
  lastRunAt?: string
  evidence: { kind: string; summary: string; path: string }
  automation?: { available: boolean; scriptPath: string; screenshotPath: string }
  performance?: { related: boolean; scenarioId: string }
}

const props = defineProps<{ cases: TestCaseItem[] }>()

const statusFilter = ref('all')
const moduleFilter = ref('all')
const selectedCaseId = ref('')

const modules = computed(() => Array.from(new Set(props.cases.map((item) => item.module))))
const filteredCases = computed(() => props.cases.filter((item) => {
  const statusMatches = statusFilter.value === 'all' || item.status === statusFilter.value
  const moduleMatches = moduleFilter.value === 'all' || item.module === moduleFilter.value
  return statusMatches && moduleMatches
}))
const selectedCase = computed(() => props.cases.find((item) => item.id === selectedCaseId.value))

function tone(status: string) {
  if (status === 'passed') return 'success'
  if (status === 'failed') return 'danger'
  if (status === 'blocked') return 'blocked'
  return 'neutral'
}

function moduleLabel(module: string) {
  const labels: Record<string, string> = {
    auth: '账号中心',
    activity: '活动报名',
    room: '场地预约',
    device: '设备借用',
    notification: '消息通知',
    booknest: 'BookNest',
    review: '后台审核',
    system: '系统健康'
  }
  return labels[module] ?? module
}
</script>

<template>
  <section class="panel case-panel">
    <div class="section-head">
      <div>
        <span class="eyebrow">Traceability</span>
        <h2>用例证据矩阵</h2>
      </div>
      <div class="filters">
        <select v-model="statusFilter" aria-label="按状态筛选">
          <option value="all">全部状态</option>
          <option value="passed">passed</option>
          <option value="failed">failed</option>
          <option value="blocked">blocked</option>
          <option value="skipped">skipped</option>
        </select>
        <select v-model="moduleFilter" aria-label="按模块筛选">
          <option value="all">全部模块</option>
          <option v-for="module in modules" :key="module" :value="module">{{ module }}</option>
        </select>
      </div>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>用例</th>
            <th>模块</th>
            <th>优先级</th>
            <th>状态</th>
            <th>执行器</th>
            <th>证据</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="testCase in filteredCases" :key="testCase.id">
            <td>
              <strong>{{ testCase.title }}</strong>
              <span>{{ testCase.id }}</span>
            </td>
            <td>{{ moduleLabel(testCase.module) }}</td>
            <td>{{ testCase.priority }}</td>
            <td><StatusBadge :label="testCase.status" :tone="tone(testCase.status)" /></td>
            <td>{{ testCase.executor }}</td>
            <td>
              <span>{{ testCase.evidence.summary }}</span>
              <code>{{ testCase.evidence.path }}</code>
            </td>
            <td>
              <button class="button secondary" type="button" @click="selectedCaseId = testCase.id">查看详情</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <aside v-if="selectedCase" class="detail-drawer" aria-label="用例证据详情">
      <div class="detail-drawer-head">
        <div>
          <span class="eyebrow">Case detail</span>
          <h2>{{ selectedCase.id }}</h2>
        </div>
        <button class="icon-button" type="button" @click="selectedCaseId = ''">×</button>
      </div>
      <div class="detail-grid">
        <span><strong>用例标题</strong>{{ selectedCase.title }}</span>
        <span><strong>关联模块</strong>{{ moduleLabel(selectedCase.module) }}</span>
        <span><strong>测试类型</strong>{{ selectedCase.type }}</span>
        <span><strong>优先级</strong>{{ selectedCase.priority }}</span>
        <span><strong>当前状态</strong><StatusBadge :label="selectedCase.status" :tone="tone(selectedCase.status)" /></span>
        <span><strong>最近执行</strong>{{ selectedCase.lastRunAt ?? '未记录' }}</span>
      </div>
      <section class="detail-block">
        <h3>证据来源</h3>
        <p>{{ selectedCase.evidence.summary }}</p>
        <code>{{ selectedCase.evidence.path }}</code>
      </section>
      <section class="detail-block">
        <h3>复盘价值</h3>
        <p>这条记录用于说明 {{ moduleLabel(selectedCase.module) }} 的 {{ selectedCase.type }} 验证结果，可回到对应文章或测试用例中复查前置条件、操作步骤和预期结果。</p>
      </section>
      <section class="detail-block">
        <h3>关联资产</h3>
        <p v-if="selectedCase.automation?.available">自动化脚本：{{ selectedCase.automation.scriptPath }}</p>
        <p v-else>自动化截图：当前用例未绑定 Selenium 截图。</p>
        <p v-if="selectedCase.performance?.related">性能场景：{{ selectedCase.performance.scenarioId }}</p>
        <p v-else>性能数据：当前用例不直接参与性能趋势。</p>
      </section>
    </aside>
  </section>
</template>
