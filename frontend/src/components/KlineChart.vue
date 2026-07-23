<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CandlestickChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { Quote } from '../types/finance'

use([CandlestickChart, BarChart, GridComponent, TooltipComponent, DataZoomComponent, CanvasRenderer])
const props = defineProps<{ quote: Quote }>()
const option = computed(() => {
  const history = props.quote.history.slice(-45)
  return {
    animationDuration: 400,
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross', lineStyle: { color: '#64748b' } }, borderColor: '#25403a', backgroundColor: '#0c1715', textStyle: { color: '#e8f2ed' } },
    grid: [{ left: 58, right: 18, top: 16, height: '65%' }, { left: 58, right: 18, top: '78%', height: '14%' }],
    xAxis: [
      { type: 'category', data: history.map((item) => item.date.slice(5)), boundaryGap: true, axisLine: { lineStyle: { color: '#29413b' } }, axisLabel: { color: '#78928a' } },
      { type: 'category', gridIndex: 1, data: history.map((item) => item.date.slice(5)), axisLabel: { show: false }, axisLine: { show: false }, axisTick: { show: false } },
    ],
    yAxis: [
      { scale: true, splitLine: { lineStyle: { color: 'rgba(114,145,135,.12)' } }, axisLabel: { color: '#78928a' } },
      { scale: true, gridIndex: 1, splitNumber: 2, axisLabel: { show: false }, splitLine: { show: false } },
    ],
    dataZoom: [{ type: 'inside', xAxisIndex: [0, 1], start: Math.max(0, 100 - (30 / Math.max(history.length, 1)) * 100), end: 100 }],
    series: [
      { name: props.quote.name, type: 'candlestick', data: history.map((item) => [item.open, item.close, item.low, item.high]), itemStyle: { color: '#5ee2ad', color0: '#f28c52', borderColor: '#5ee2ad', borderColor0: '#f28c52' } },
      { name: '成交量', type: 'bar', xAxisIndex: 1, yAxisIndex: 1, data: history.map((item) => item.volume), itemStyle: { color: '#315c50' } },
    ],
  }
})
</script>

<template><v-chart class="kline" :option="option" autoresize /></template>

