<script setup lang="ts">
import { computed } from 'vue'
import type { Quote } from '../types/finance'

const props = defineProps<{ quote: Quote; active?: boolean }>()
const emit = defineEmits<{ select: [quote: Quote] }>()
const positive = computed(() => props.quote.change_pct >= 0)
const points = computed(() => {
  const values = props.quote.history.slice(-12).map((item) => item.close)
  if (values.length < 2) return ''
  const min = Math.min(...values)
  const max = Math.max(...values)
  return values.map((value, index) => {
    const x = (index / (values.length - 1)) * 112
    const y = 34 - ((value - min) / Math.max(max - min, 1)) * 28
    return `${x},${y}`
  }).join(' ')
})
</script>

<template>
  <button class="index-card" :class="{ active }" type="button" @click="emit('select', quote)">
    <div class="index-head">
      <div><span class="market-tag">{{ quote.market }}</span><h3>{{ quote.name }}</h3></div>
      <span class="source-dot" :class="quote.status" :title="`${quote.source} · ${quote.trade_date}`" />
    </div>
    <div class="index-body">
      <div>
        <strong>{{ quote.close.toLocaleString('zh-CN', { maximumFractionDigits: 2 }) }}</strong>
        <span :class="positive ? 'gain' : 'loss'">{{ positive ? '+' : '' }}{{ quote.change_pct.toFixed(2) }}%</span>
      </div>
      <svg class="sparkline" viewBox="0 0 112 38" aria-hidden="true">
        <defs><linearGradient :id="`spark-${quote.symbol.replace(/\W/g, '')}`" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="positive ? '#6ee7b7' : '#fb923c'" stop-opacity=".3"/><stop offset="1" :stop-color="positive ? '#6ee7b7' : '#fb923c'" stop-opacity="0"/></linearGradient></defs>
        <polyline :points="points" fill="none" :stroke="positive ? '#6ee7b7' : '#fb923c'" stroke-width="2" />
      </svg>
    </div>
    <div class="card-foot"><span>{{ quote.symbol }}</span><span>{{ quote.trade_date }} 收盘</span></div>
  </button>
</template>

