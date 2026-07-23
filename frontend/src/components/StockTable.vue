<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Quote, SectorSummary } from '../types/finance'
const props = defineProps<{ stocks: Quote[]; sectors: SectorSummary[] }>()
const active = ref(props.sectors[0]?.key ?? 'technology')
const rows = computed(() => props.stocks.filter((item) => item.category === active.value).sort((a, b) => b.change_pct - a.change_pct))
const formatPrice = (quote: Quote) => quote.close.toLocaleString('zh-CN', { maximumFractionDigits: quote.close > 1000 ? 0 : 2 })
</script>

<template>
  <div class="stock-table-wrap">
    <div class="tabs" role="tablist">
      <button v-for="sector in sectors" :key="sector.key" type="button" :class="{ active: active === sector.key }" @click="active = sector.key">{{ sector.name }}</button>
    </div>
    <div class="stock-table">
      <div class="stock-row stock-head"><span>公司 / 代码</span><span>收盘价</span><span>日涨跌</span><span>5 日趋势</span></div>
      <div v-for="quote in rows" :key="quote.symbol" class="stock-row">
        <span><strong>{{ quote.name }}</strong><small>{{ quote.symbol }} · {{ quote.market }}</small></span>
        <span><strong>{{ formatPrice(quote) }}</strong><small>{{ quote.currency }} · {{ quote.trade_date }}</small></span>
        <span :class="quote.change_pct >= 0 ? 'gain' : 'loss'">{{ quote.change_pct >= 0 ? '+' : '' }}{{ quote.change_pct.toFixed(2) }}%</span>
        <span :class="quote.trend_5d >= 0 ? 'gain' : 'loss'">{{ quote.trend_5d >= 0 ? '↗' : '↘' }} {{ Math.abs(quote.trend_5d).toFixed(2) }}%</span>
      </div>
    </div>
  </div>
</template>
