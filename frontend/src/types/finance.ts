export type DataStatus = 'fresh' | 'stale' | 'unavailable' | 'demo'

export interface Candle {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface Quote {
  symbol: string
  name: string
  market: string
  category: string
  currency: string
  trade_date: string
  close: number
  previous_close: number
  change: number
  change_pct: number
  trend_5d: number
  status: DataStatus
  source: string
  history: Candle[]
}

export interface SectorSummary {
  key: string
  name: string
  average_change_pct: number
  advancing: number
  declining: number
  unchanged: number
  leader: string
  laggard: string
  status: DataStatus
}

export interface NewsItem {
  id: string
  title: string
  url: string
  source: string
  published_at: string
  category: string
  symbols: string[]
  is_official: boolean
}

export interface ReportSection {
  title: string
  tone: 'positive' | 'negative' | 'neutral' | 'warning'
  summary: string
  evidence: string[]
}

export interface DailyReport {
  headline: string
  overview: string
  market_bias: 'risk-on' | 'risk-off' | 'mixed'
  sections: ReportSection[]
  highlights: string[]
  risks: string[]
  focus_next: string[]
  disclaimer: string
}

export interface DashboardMeta {
  generated_at: string
  report_date: string
  timezone: string
  status: 'fresh' | 'partial' | 'demo' | 'error'
  status_message: string
  next_update: string
  version: string
}

export interface DashboardData {
  meta: DashboardMeta
  indices: Quote[]
  macro: Quote[]
  stocks: Quote[]
  sectors: SectorSummary[]
  news: NewsItem[]
  report: DailyReport
}

