<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import DailyReport from './components/DailyReport.vue'
import IndexCard from './components/IndexCard.vue'
import IndustryHeatmap from './components/IndustryHeatmap.vue'
import KlineChart from './components/KlineChart.vue'
import NewsList from './components/NewsList.vue'
import StatusPill from './components/StatusPill.vue'
import StockTable from './components/StockTable.vue'
import { useDashboardData } from './composables/useDashboardData'
import type { Quote } from './types/finance'

const { data, loading, error, refresh } = useDashboardData()
const selected = ref<Quote>()
watch(data, (value) => { if (!selected.value && value?.indices.length) selected.value = value.indices[0] }, { immediate: true })
const generatedTime = computed(() => data.value ? new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(data.value.meta.generated_at)) : '--')
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <a class="brand" href="#top" aria-label="Market Pulse 首页"><span class="brand-mark">M</span><span><strong>MARKET PULSE</strong><small>PERSONAL FINANCE COCKPIT</small></span></a>
      <nav><a href="#markets">市场</a><a href="#themes">主题</a><a href="#brief">日报</a><a href="#news">新闻</a></nav>
      <div v-if="data" class="top-actions"><StatusPill :meta="data.meta" /><button class="refresh" type="button" :disabled="loading" @click="refresh">{{ loading ? '载入中' : '刷新' }}</button></div>
    </header>

    <main v-if="data" id="top">
      <section class="hero">
        <div><span class="eyebrow">DAILY MARKET INTELLIGENCE · {{ data.meta.report_date }}</span><h1>全球市场，<em>一屏掌握。</em></h1><p>聚焦美、日、韩收盘行情，追踪商业航天、存储、化工与科技龙头。规则分析，零 API 费用。</p></div>
        <div class="update-card"><span>最后生成</span><strong>{{ generatedTime }}</strong><p>{{ data.meta.status_message }}</p><small>{{ data.meta.next_update }}</small></div>
      </section>

      <section class="macro-strip" aria-label="宏观指标">
        <div v-for="item in data.macro" :key="item.symbol"><span>{{ item.name }}</span><strong>{{ item.close.toLocaleString('zh-CN', { maximumFractionDigits: 2 }) }}</strong><small :class="item.change_pct >= 0 ? 'gain' : 'loss'">{{ item.change_pct >= 0 ? '+' : '' }}{{ item.change_pct.toFixed(2) }}%</small></div>
      </section>

      <section id="markets" class="section-block">
        <div class="section-heading"><div><span class="section-index">01</span><h2>全球指数</h2></div><p>均为最近完整交易日收盘，不混入日、韩盘中价格</p></div>
        <div class="index-grid"><IndexCard v-for="item in data.indices" :key="item.symbol" :quote="item" :active="selected?.symbol === item.symbol" @select="selected = $event" /></div>
      </section>

      <section class="split-grid chart-area">
        <article class="panel chart-panel">
          <div class="panel-head"><div><span class="eyebrow">PRICE ACTION</span><h2>{{ selected?.name }} <small>{{ selected?.symbol }}</small></h2></div><span v-if="selected">{{ selected.trade_date }} · {{ selected.source }}</span></div>
          <KlineChart v-if="selected" :quote="selected" />
        </article>
        <article id="themes" class="panel heat-panel"><div class="panel-head"><div><span class="eyebrow">SECTOR PULSE</span><h2>行业热力图</h2></div><span>等权日涨跌</span></div><IndustryHeatmap :sectors="data.sectors" /></article>
      </section>

      <section class="section-block">
        <div class="section-heading"><div><span class="section-index">02</span><h2>关注池</h2></div><p>按板块查看收盘价、当日表现和五日趋势</p></div>
        <StockTable :stocks="data.stocks" :sectors="data.sectors" />
      </section>

      <section class="split-grid content-area">
        <div id="brief"><DailyReport :report="data.report" /></div>
        <article id="news" class="panel news-panel"><div class="panel-head"><div><span class="eyebrow">VERIFIED SIGNALS</span><h2>相关新闻</h2></div><span>{{ data.news.length }} 条</span></div><NewsList :news="data.news" /></article>
      </section>

      <footer><div><strong>MARKET PULSE</strong><span>数据源：Yahoo Finance 公共行情、GDELT 与公司官方披露</span></div><p>{{ data.report.disclaimer }} 免费数据可能延迟或暂时不可用，请以交易所及公司公告为准。</p></footer>
    </main>

    <div v-else class="loading-screen"><span class="brand-mark">M</span><p>{{ error || '正在读取金融驾驶舱…' }}</p><button v-if="error" type="button" @click="refresh">重试</button></div>
  </div>
</template>

