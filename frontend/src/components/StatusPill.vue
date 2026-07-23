<script setup lang="ts">
import { computed } from 'vue'
import type { DashboardMeta } from '../types/finance'

const props = defineProps<{ meta: DashboardMeta }>()
const label = computed(() => ({ fresh: '数据已更新', partial: '部分数据缓存', demo: '演示数据', error: '更新异常' })[props.meta.status])
</script>

<template>
  <div class="status-pill" :class="`status-${meta.status}`" :title="meta.status_message">
    <span class="status-dot" />
    <span>{{ label }}</span>
  </div>
</template>

