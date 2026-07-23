# finance-ai-dashboard

一个零服务器成本、零大模型 API 费用的个人金融驾驶舱。系统每天用 GitHub Actions 获取美、日、韩最近完整收盘行情，生成可追溯的规则化日报，部署到 GitHub Pages，并通过飞书机器人推送。

> 本项目不调用 OpenAI API，也不消耗 API Token。日常运行使用 GitHub Actions、GitHub Pages、Yahoo Finance 公共接口和 GDELT 的免费能力。

## 查看内容

- 全球指数：纳斯达克综合、标普 500、费城半导体、日经 225、TOPIX、KOSPI、KOSDAQ
- 主题股票：商业航天、存储与内存、化工与材料、科技龙头
- 宏观背景：VIX、美债 10 年、美元、日元、韩元、WTI 原油、黄金
- K 线、板块热力图、关注池、规则日报、相关新闻与数据状态

## 自动更新时间

主任务为北京时间每天 **10:00**，补偿任务为 **10:20** 和 **10:50**。同一天已经成功生成完整日报时，补偿任务自动跳过采集与飞书推送。GitHub Actions 的定时任务可能有几分钟排队延迟，网站会显示实际生成时间及数据交易日期。

## 你需要配置的内容

仓库的 `Settings → Secrets and variables → Actions` 中添加：

| Secret | 用途 |
|---|---|
| `FEISHU_WEBHOOK_URL` | 飞书自定义机器人 Webhook |
| `FEISHU_WEBHOOK_SECRET` | 飞书机器人的签名校验密钥 |

不要把真实值写入 `.env` 或提交到 Git。项目不需要 OpenAI Key。

## 第一次上线

1. 把本项目推送到 GitHub 的 `main` 分支。
2. 打开仓库 `Actions`，允许工作流运行。
3. 打开 `Actions → Daily Finance Dashboard → Run workflow`，手动执行第一次任务。
4. 完成后网站地址为 `https://jshawyee.github.io/finance-ai-dashboard/`。
5. 若 Pages 尚未启用，进入 `Settings → Pages`，将 Source 设为 **GitHub Actions**，再运行一次工作流。

## 本地开发

要求 Python 3.11+、Node.js 20+ 和 pnpm 10。Python 数据流水线只使用标准库。

```bash
python scripts/run_daily.py
python scripts/sync_frontend_data.py
cd frontend
pnpm install
pnpm dev
```

仅测试前端布局时，即使没有生成 JSON，也会自动显示明确标记的演示数据。

## 验证

```bash
python -m unittest discover -s tests
cd frontend
pnpm run check
pnpm run build
```

## 目录

```text
agent/                 行情、新闻、指标和规则分析
config/markets.json    观察代码与市场收盘配置
data/latest/           网站使用的最新 JSON
data/history/          最近 120 份日报历史
frontend/              Vue 3 + Vite + TypeScript + ECharts + TailwindCSS
notification/feishu/   飞书签名与卡片消息
scripts/               日常运行、同步和推送入口
.github/workflows/     定时采集、构建、部署工作流
tests/                 Python 核心规则测试
```

详细设计及故障降级见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 数据与免责声明

Yahoo Finance 和 GDELT 均为免费公共数据源，可能延迟、调整、限流或改变接口，不能保证交易级实时性。网站展示原始链接、实际交易日期、数据来源和新鲜度；异常时保留缓存，不伪造缺失值。所有文字由固定规则生成，只表达同步变化和可能因素，不构成投资建议。关键决策请以交易所、监管机构和公司正式公告为准。
