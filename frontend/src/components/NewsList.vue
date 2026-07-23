<script setup lang="ts">
import type { NewsItem } from '../types/finance'
defineProps<{ news: NewsItem[] }>()
const date = (value: string) => new Intl.DateTimeFormat('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(value))
</script>

<template>
  <div class="news-list">
    <a v-for="item in news" :key="item.id" class="news-item" :href="item.url === '#' ? undefined : item.url" target="_blank" rel="noreferrer">
      <div class="news-meta"><span :class="{ official: item.is_official }">{{ item.is_official ? '官方' : item.category }}</span><time>{{ date(item.published_at) }}</time></div>
      <h3>{{ item.title }}</h3>
      <div class="news-source"><span>{{ item.source }}</span><span v-if="item.symbols.length">{{ item.symbols.slice(0, 3).join(' · ') }}</span></div>
    </a>
    <div v-if="!news.length" class="empty-state">当前没有可验证的相关新闻</div>
  </div>
</template>

