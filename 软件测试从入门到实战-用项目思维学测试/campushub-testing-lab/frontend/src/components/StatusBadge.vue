<script setup lang="ts">
defineProps<{
  label: string
  tone?: 'success' | 'info' | 'warning' | 'danger' | 'blocked' | 'neutral'
}>()
</script>

<template>
  <span class="status-badge" :class="tone ?? 'neutral'">{{ label }}</span>
</template>
