import type { Candle, DashboardData, Quote } from '../types/finance'

const dates = ['2026-07-14', '2026-07-15', '2026-07-16', '2026-07-17', '2026-07-20']

const candles = (base: number): Candle[] => dates.map((date, index) => {
  const factor = 0.97 + index * 0.009
  return {
    date,
    open: Number((base * factor).toFixed(2)),
    high: Number((base * (factor + 0.014)).toFixed(2)),
    low: Number((base * (factor - 0.011)).toFixed(2)),
    close: Number((base * (factor + 0.005)).toFixed(2)),
    volume: 1_040_000 + index * 91_000,
  }
})

const quote = (
  symbol: string,
  name: string,
  market: string,
  category: string,
  close: number,
  changePct: number,
  currency = 'USD',
): Quote => ({
  symbol,
  name,
  market,
  category,
  currency,
  trade_date: '2026-07-20',
  close,
  previous_close: close / (1 + changePct / 100),
  change: close - close / (1 + changePct / 100),
  change_pct: changePct,
  trend_5d: changePct * 1.8,
  status: 'demo',
  source: '演示数据',
  history: candles(close),
})

export const fallbackData: DashboardData = {
  meta: {
    generated_at: '2026-07-22T10:00:00+08:00',
    report_date: '2026-07-22',
    timezone: 'Asia/Shanghai',
    status: 'demo',
    status_message: '等待首次自动任务，当前为界面演示数据',
    next_update: '每天北京时间 10:00（含 10:20、10:50 补偿任务）',
    version: '1.0.0',
  },
  indices: [
    quote('^IXIC', '纳斯达克综合', '美国', 'index', 23031.21, 0.82),
    quote('^GSPC', '标普 500', '美国', 'index', 7266.99, 0.46),
    quote('^SOX', '费城半导体', '美国', 'index', 12681.12, 1.18),
    quote('^N225', '日经 225', '日本', 'index', 66115.6, -0.18, 'JPY'),
    quote('^TOPX', 'TOPIX', '日本', 'index', 4011.5, 0.31, 'JPY'),
    quote('^KS11', 'KOSPI', '韩国', 'index', 6747.95, 0.56, 'KRW'),
    quote('^KQ11', 'KOSDAQ', '韩国', 'index', 1192.78, 0.39, 'KRW'),
  ],
  macro: [
    quote('^VIX', 'VIX', '美国', 'macro', 18.42, -2.11),
    quote('^TNX', '美国 10Y', '美国', 'macro', 4.21, 0.24, '%'),
    quote('DX-Y.NYB', '美元指数', '全球', 'macro', 98.74, -0.16),
    quote('JPY=X', 'USD/JPY', '外汇', 'macro', 146.52, 0.12, 'JPY'),
    quote('KRW=X', 'USD/KRW', '外汇', 'macro', 1378.4, -0.21, 'KRW'),
    quote('CL=F', 'WTI 原油', '商品', 'macro', 73.18, 0.64),
    quote('GC=F', '黄金', '商品', 'macro', 3342.6, 0.32),
  ],
  stocks: [
    quote('SPCX', 'SpaceX', '美国', 'space', 282.54, 3.08),
    quote('RKLB', 'Rocket Lab', '美国', 'space', 83.35, -0.07),
    quote('ASTS', 'AST SpaceMobile', '美国', 'space', 71.92, 1.22),
    quote('LUNR', 'Intuitive Machines', '美国', 'space', 14.86, -1.14),
    quote('MU', 'Micron', '美国', 'memory', 148.8, 1.11),
    quote('SNDK', 'SanDisk', '美国', 'memory', 91.43, -0.65),
    quote('STX', 'Seagate', '美国', 'memory', 154.19, 0.76),
    quote('WDC', 'Western Digital', '美国', 'memory', 83.82, 0.42),
    quote('005930.KS', 'Samsung Electronics', '韩国', 'memory', 78600, 1.44, 'KRW'),
    quote('000660.KS', 'SK hynix', '韩国', 'memory', 284500, -1.37, 'KRW'),
    quote('285A.T', 'Kioxia', '日本', 'memory', 8120, 2.64, 'JPY'),
    quote('LIN', 'Linde', '美国', 'chemicals', 485.62, 0.28),
    quote('DOW', 'Dow', '美国', 'chemicals', 31.44, -0.33),
    quote('DD', 'DuPont', '美国', 'chemicals', 91.28, 0.51),
    quote('APD', 'Air Products', '美国', 'chemicals', 308.74, 0.19),
    quote('4063.T', 'Shin-Etsu Chemical', '日本', 'chemicals', 6070, 0.73, 'JPY'),
    quote('051910.KS', 'LG Chem', '韩国', 'chemicals', 324500, -0.57, 'KRW'),
    quote('NVDA', 'NVIDIA', '美国', 'technology', 188.42, 1.35),
    quote('AMD', 'AMD', '美国', 'technology', 212.6, 0.84),
    quote('AVGO', 'Broadcom', '美国', 'technology', 388.69, 4.83),
    quote('MSFT', 'Microsoft', '美国', 'technology', 528.12, 0.36),
    quote('GOOGL', 'Alphabet', '美国', 'technology', 201.74, -0.22),
    quote('AMZN', 'Amazon', '美国', 'technology', 231.48, 0.58),
    quote('META', 'Meta', '美国', 'technology', 694.16, 0.72),
    quote('AAPL', 'Apple', '美国', 'technology', 226.38, -0.18),
  ],
  sectors: [
    { key: 'space', name: '商业航天', average_change_pct: 0.77, advancing: 2, declining: 2, unchanged: 0, leader: 'SPCX', laggard: 'LUNR', status: 'demo' },
    { key: 'memory', name: '存储与内存', average_change_pct: 0.61, advancing: 5, declining: 2, unchanged: 0, leader: '285A.T', laggard: '000660.KS', status: 'demo' },
    { key: 'chemicals', name: '化工与材料', average_change_pct: 0.14, advancing: 4, declining: 2, unchanged: 0, leader: '4063.T', laggard: '051910.KS', status: 'demo' },
    { key: 'technology', name: '科技龙头', average_change_pct: 1.04, advancing: 6, declining: 2, unchanged: 0, leader: 'AVGO', laggard: 'GOOGL', status: 'demo' },
  ],
  news: [
    { id: 'demo-1', title: '等待首次数据任务：新闻将在自动更新后显示', url: '#', source: '系统', published_at: '2026-07-22T10:00:00+08:00', category: 'system', symbols: [], is_official: true },
  ],
  report: {
    headline: '科技与半导体相对活跃，区域市场表现分化',
    overview: '这是界面演示报告。首次自动任务完成后，系统将根据真实收盘数据和可追溯新闻生成规则化日报。',
    market_bias: 'mixed',
    sections: [
      { title: '美国市场', tone: 'positive', summary: '纳指、标普和费城半导体指数多数收高。', evidence: ['费城半导体指数领涨', '科技龙头涨多跌少'] },
      { title: '日、韩市场', tone: 'neutral', summary: '日本与韩国市场使用最近完整交易日收盘数据。', evidence: ['不混入北京时间 10:00 的盘中价格'] },
      { title: '主题板块', tone: 'positive', summary: '商业航天和存储板块保持较高活跃度。', evidence: ['板块统计来自成分股等权平均'] },
    ],
    highlights: ['所有行情均标记实际交易日期', '官方公告优先于普通新闻'],
    risks: ['免费行情可能延迟', '规则分析只表示相关性，不证明因果关系'],
    focus_next: ['美联储政策信号', '存储价格与产能指引', '商业航天发射及合同进展'],
    disclaimer: '仅供个人信息整理，不构成投资建议。',
  },
}
