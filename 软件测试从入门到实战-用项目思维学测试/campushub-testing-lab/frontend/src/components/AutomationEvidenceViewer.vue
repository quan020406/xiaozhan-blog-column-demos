<script setup lang="ts">
import { computed, ref } from 'vue'
import StatusBadge from './StatusBadge.vue'

type ScreenshotItem = {
  id: string
  title: string
  module: string
  status: string
  imagePath: string
  caption: string
}

const props = defineProps<{
  latestRun: {
    status: string
    runId: string
    browser: string
    scriptPath: string
    stepCount?: number
  }
  screenshots: ScreenshotItem[]
}>()

const selectedId = ref(props.screenshots[0]?.id ?? '')
const selected = computed(() => props.screenshots.find((item) => item.id === selectedId.value) ?? props.screenshots[0])

function imageUrl(path: string) {
  const normalizedPath = path.replace(/^src\//, '../')
  return new URL(normalizedPath, import.meta.url).href
}

function moduleLabel(module: string) {
  const labels: Record<string, string> = {
    auth: '账号中心',
    activity: '活动报名',
    room: '场地预约',
    device: '设备借用',
    notification: '消息通知',
    booknest: 'BookNest'
  }
  return labels[module] ?? module
}
</script>

<template>
  <section class="panel evidence-panel" data-testid="automation-evidence-viewer">
    <div class="section-head">
      <div>
        <span class="eyebrow">Automation evidence</span>
        <h2>Selenium 运行证据</h2>
        <p>{{ latestRun.scriptPath }}</p>
      </div>
      <StatusBadge :label="latestRun.status" :tone="latestRun.status === 'passed' ? 'success' : 'warning'" />
    </div>

    <div v-if="selected" class="evidence-layout">
      <figure class="screenshot-stage">
        <img :src="imageUrl(selected.imagePath)" :alt="selected.title" />
      </figure>
      <div class="evidence-copy">
        <strong>{{ selected.title }}</strong>
        <span>{{ selected.caption }}</span>
        <span>{{ latestRun.browser }} · {{ latestRun.runId }} · {{ latestRun.stepCount ?? screenshots.length }} steps</span>
        <span>关联模块：{{ moduleLabel(selected.module) }} · 当前状态：{{ selected.status }}</span>
        <code>{{ selected.imagePath }}</code>
      </div>
      <div class="shot-tabs" aria-label="自动化截图">
        <button
          v-for="shot in screenshots"
          :key="shot.id"
          type="button"
          :class="{ active: selected?.id === shot.id }"
          @click="selectedId = shot.id"
        >
          {{ moduleLabel(shot.module) }}
        </button>
      </div>
      <div class="evidence-meta-grid">
        <span><strong>证据来源</strong>Selenium 自动化截图</span>
        <span><strong>关联脚本</strong>{{ latestRun.scriptPath }}</span>
        <span><strong>复盘价值</strong>用于确认读者跟做步骤里的页面状态和自动化脚本断言是否一致。</span>
      </div>
    </div>
  </section>
</template>
