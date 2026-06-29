<script setup lang="ts">
import { TerminalSquare } from 'lucide-vue-next'
import StatusBadge from './StatusBadge.vue'

type CommandEvidence = {
  name: string
  command: string
  cwd: string
  status: string
  summary: string
}

defineProps<{ commands: CommandEvidence[] }>()

function tone(status: string) {
  if (status === 'passed') return 'success'
  if (status === 'failed') return 'danger'
  return 'warning'
}
</script>

<template>
  <section class="panel command-panel">
    <div class="section-head">
      <div>
        <span class="eyebrow">Run evidence</span>
        <h2>执行摘要</h2>
      </div>
      <TerminalSquare :size="20" aria-hidden="true" />
    </div>

    <div class="command-grid">
      <article v-for="item in commands" :key="item.name" class="command-card">
        <div>
          <strong>{{ item.name }}</strong>
          <StatusBadge :label="item.status" :tone="tone(item.status)" />
        </div>
        <code>{{ item.command }}</code>
        <span>{{ item.summary }}</span>
      </article>
    </div>
  </section>
</template>
