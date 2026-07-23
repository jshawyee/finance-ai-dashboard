<script setup lang="ts">
import type { SectorSummary } from '../types/finance'
defineProps<{ sectors: SectorSummary[] }>()
const color = (value: number) => value >= 0 ? `rgba(48, 196, 132, ${Math.min(.25 + Math.abs(value) / 4, .8)})` : `rgba(237, 112, 60, ${Math.min(.25 + Math.abs(value) / 4, .8)})`
</script>

<template>
  <div class="heatmap-grid">
    <article v-for="sector in sectors" :key="sector.key" class="heat-tile" :style="{ background: color(sector.average_change_pct) }">
      <span>{{ sector.name }}</span>
      <strong>{{ sector.average_change_pct >= 0 ? '+' : '' }}{{ sector.average_change_pct.toFixed(2) }}%</strong>
      <small>{{ sector.advancing }} 涨 · {{ sector.declining }} 跌</small>
      <div><span>领涨 {{ sector.leader }}</span><span>落后 {{ sector.laggard }}</span></div>
    </article>
  </div>
</template>

