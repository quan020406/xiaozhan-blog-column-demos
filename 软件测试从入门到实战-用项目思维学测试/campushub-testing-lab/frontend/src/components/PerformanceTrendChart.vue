<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, LegendComponent, MarkLineComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import StatusBadge from './StatusBadge.vue'

echarts.use([LineChart, GridComponent, LegendComponent, MarkLineComponent, TooltipComponent, CanvasRenderer])

type PerformancePoint = {
  time: string
  avgResponseMs: number
  p95ResponseMs: number
  throughputPerSecond: number
  errorRate: number
  note: string
}

type PerformanceData = {
  title: string
  dataSource: string
  status?: string
  sampleCount?: number
  failureCount?: number
  totalErrorRate?: number
  thresholds: {
    p95ResponseMs: number
    errorRate: number
  }
  series: PerformancePoint[]
  notes: string
}

const props = defineProps<{ performance: PerformanceData; theme: 'light' | 'dark' }>()
const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

function renderChart() {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  const isDark = props.theme === 'dark'
  chart.setOption({
    backgroundColor: 'transparent',
    color: isDark ? ['#7dd3fc', '#a7f3d0', '#fbbf24'] : ['#0f766e', '#2563eb', '#d97706'],
    tooltip: {
      trigger: 'axis',
      formatter: (params: unknown) => {
        const rows = params as Array<{ marker: string; seriesName: string; value: number; dataIndex: number }>
        const point = props.performance.series[rows[0]?.dataIndex ?? 0]
        return [
          `<strong>${point.time}</strong>`,
          ...rows.map((row) => `${row.marker}${row.seriesName}: ${row.value}`),
          `说明: ${point.note}`
        ].join('<br/>')
      }
    },
    legend: { top: 0, textStyle: { color: isDark ? '#cbd5e1' : '#475569' } },
    grid: { top: 46, right: 22, bottom: 28, left: 48 },
    xAxis: {
      type: 'category',
      data: props.performance.series.map((item) => item.time),
      axisLabel: { color: isDark ? '#cbd5e1' : '#64748b' },
      axisLine: { lineStyle: { color: isDark ? '#334155' : '#cbd5e1' } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: isDark ? '#cbd5e1' : '#64748b' },
      splitLine: { lineStyle: { color: isDark ? '#243044' : '#e2e8f0' } }
    },
    series: [
      {
        name: 'p95 ms',
        type: 'line',
        smooth: true,
        data: props.performance.series.map((item) => item.p95ResponseMs),
        markLine: {
          symbol: 'none',
          lineStyle: { type: 'dashed', color: isDark ? '#fbbf24' : '#d97706' },
          data: [{ yAxis: props.performance.thresholds.p95ResponseMs, name: 'p95 阈值' }]
        }
      },
      {
        name: '平均 ms',
        type: 'line',
        smooth: true,
        data: props.performance.series.map((item) => item.avgResponseMs)
      },
      {
        name: '错误率 %',
        type: 'line',
        smooth: true,
        data: props.performance.series.map((item) => item.errorRate)
      }
    ]
  })
}

function sourceLabel() {
  if (props.performance.dataSource === 'generated') return '脚本生成'
  if (props.performance.dataSource === 'missing') return '缺少结果'
  return '样例趋势'
}

function resizeChart() {
  chart?.resize()
}

onMounted(() => {
  renderChart()
  window.addEventListener('resize', resizeChart)
})

watch(() => [props.performance, props.theme], renderChart, { deep: true })

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chart?.dispose()
  chart = null
})
</script>

<template>
  <section class="panel performance-panel" data-testid="performance-trend-chart">
    <div class="section-head">
      <div>
        <span class="eyebrow">Performance trend</span>
        <h2>{{ performance.title }}</h2>
        <p>p95 阈值 {{ performance.thresholds.p95ResponseMs }}ms，错误率阈值 {{ performance.thresholds.errorRate }}%。</p>
      </div>
      <StatusBadge :label="sourceLabel()" :tone="performance.status === 'passed' ? 'success' : 'warning'" />
    </div>
    <div class="perf-stats">
      <span><strong>{{ performance.sampleCount ?? performance.series.length }}</strong>样本</span>
      <span><strong>{{ performance.failureCount ?? 0 }}</strong>失败</span>
      <span><strong>{{ performance.totalErrorRate ?? 0 }}%</strong>错误率</span>
    </div>
    <div ref="chartRef" class="chart-surface" aria-label="性能趋势图"></div>
  </section>
</template>
