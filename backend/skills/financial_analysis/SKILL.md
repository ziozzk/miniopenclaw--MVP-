---
name: financial_analysis
description: 分析美股上市公司的财报数据，生成 One Pager 报告
---

# 财报分析

## 功能
分析美股上市公司的财务数据，生成结构化的 One Pager 报告，包括业务概览、财务摘要、投资亮点和风险提示。

## 使用方式
提供公司名称或股票代码，返回该公司的财报分析报告。

## 示例
- 输入：AAPL 或 苹果
- 输出：Apple Inc. 的 One Pager 报告

## 数据源
使用 fetch_url 工具从 Alpha Vantage API 获取数据：
- 实时股价：https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={SYMBOL}&apikey={API_KEY}
- 利润表：https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={SYMBOL}&apikey={API_KEY}

## 返回格式
```markdown
## 📊 {公司全称} ({股票代码})

### 🏢 业务概览
- **行业**: {行业分类}
- **主营业务**: {描述}
- **市场地位**: {地位描述}

### 💰 财务摘要 (TTM)
| 指标 | 数值 |
|------|------|
| 市值 | {市值} |
| 营收 | {营收} |
| 净利润 | {净利润} |
| 毛利率 | {毛利率}% |
| PE (TTM) | {PE} |

### ✨ 投资亮点
- {亮点 1}
- {亮点 2}

### ⚠️ 风险提示
- {风险 1}
- {风险 2}
```

## 常用股票代码
| 公司 | 代码 |
|------|------|
| 苹果 | AAPL |
| 微软 | MSFT |
| 谷歌 | GOOGL |
| 亚马逊 | AMZN |
| 特斯拉 | TSLA |
| 英伟达 | NVDA |
