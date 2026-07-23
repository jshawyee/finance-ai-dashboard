<script setup lang="ts">
import type { DailyReport } from '../types/finance'
defineProps<{ report: DailyReport }>()
</script>

<template>
  <article class="report">
    <div class="report-title"><span class="eyebrow">RULE-BASED BRIEF</span><span class="bias" :class="report.market_bias">{{ report.market_bias }}</span></div>
    <h2>{{ report.headline }}</h2>
    <p class="report-overview">{{ report.overview }}</p>
    <div class="report-sections">
      <section v-for="section in report.sections" :key="section.title" :class="`tone-${section.tone}`">
        <h3>{{ section.title }}</h3><p>{{ section.summary }}</p>
        <ul><li v-for="item in section.evidence" :key="item">{{ item }}</li></ul>
      </section>
    </div>
    <div class="report-lists">
      <div><h3>今日观察</h3><p v-for="item in report.highlights" :key="item">{{ item }}</p></div>
      <div><h3>后续关注</h3><p v-for="item in report.focus_next" :key="item">{{ item }}</p></div>
      <div class="risk-list"><h3>风险提示</h3><p v-for="item in report.risks" :key="item">{{ item }}</p></div>
    </div>
    <small class="disclaimer">{{ report.disclaimer }}</small>
  </article>
</template>

