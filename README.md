# 🤖 Mini OpenClaw

**轻量级 AI Agent 框架** - 基于 LangChain 构建，支持 Skills 系统和本地记忆管理

>  **当前状态**: Alpha 版本，仅支持命令行交互模式，Web 和飞书集成模式开发中。

---

## ✨ 特性

- 🛠️ **5 个内置工具**: Terminal、Python REPL、Fetch URL、Read File、RAG Search
- 📚 **Skills 系统**: 类似 Anthropic Skills 的可扩展技能机制
- 💾 **本地记忆**: 会话历史、系统消息、长期记忆全部本地存储
- 🔒 **安全优先**: 工具沙箱化、文件访问限制、命令黑名单、URL 过滤
- 📝 **Markdown 配置**: 所有配置使用 Markdown 文件，易于编辑和版本控制

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- pip 包管理器

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 填入 API Key
# 通义千问 (推荐，免费额度)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx

# 或 OpenAI
# OPENAI_API_KEY=sk-xxxxxxxxxxxx

# 或 Moonshot/Kimi
# KIMI_API_KEY=km-xxxxxxxxxxxx
```

### 3. 启动

```bash
cd backend
python main.py
```

### 4. 开始对话

```
🤖 Mini OpenClaw v0.1.0
==================================================
✅ API Key 已加载：sk-xxxxx...xxxxx

📦 初始化系统...
🛠️  注册工具...
   已加载 5 个工具：terminal, python_repl, fetch_url, read_file, rag_search
💾 初始化记忆系统...
🧠 构建 Agent...
📄 加载系统消息...
   系统消息长度：2847 字符

✅ 初始化完成!

==================================================
💬 命令行交互模式 (输入 '退出' 或 'quit' 结束)
==================================================

你：你好
🤖 你好！我是 Mini OpenClaw，有什么可以帮你？

你：查询北京天气
🤖 [调用 get_weather skill]
北京当前天气为晴，温度 25°C，湿度 60%

你：帮我分析 AAPL 的财报
🤖 [调用 financial_analysis skill]
[生成 One Pager 报告]
```

---

## 📁 项目结构

```
mini-openclaw/
├── backend/
│   ├── main.py                    # 主入口
│   ├── agent/
│   │   ├── builder.py             # Agent 构建器
│   │   └── memory.py              # 记忆管理
│   ├── tools/
│   │   ├── __init__.py            # 工具注册 (5 个核心工具)
│   │   ├── terminal.py            # 安全 Shell 工具 (带命令黑名单)
│   │   ├── fetch_url.py           # 安全网络获取 (内网 URL 过滤)
│   │   ├── read_file.py           # 安全文件读取 (目录限制)
│   │   └── rag_search.py          # RAG 知识检索
│   │   # 注：Python REPL 使用 LangChain 内置工具，无独立文件
│   ├── skills/
│   │   ├── get_weather/
│   │   │   └── SKILL.md
│   │   └── financial_analysis/
│   │       └── SKILL.md
│   ├── sessions/                  # 会话存储
│   ├── workspace/                 # 系统配置
│   │   ├── SOUL.md
│   │   ├── IDENTITY.md
│   │   ├── USER.md
│   │   └── AGENTS.md
│   ├── SKILLS_SNAPSHOT.md         # Skills 汇总
│   ├── MEMORY.md                  # 长期记忆
│   ├── config.yaml                # 配置文件
│   └── requirements.txt           # 依赖
└── README.md
```

---

## 📚 系统消息构成

Mini OpenClaw 的系统消息由 6 部分组成：

| 文件 | 用途 |
|------|------|
| **SKILLS_SNAPSHOT.md** | 可用 Skills 列表 (自动生成，启动时扫描 `skills/` 目录) |
| **SOUL.md** | 人格、语气与边界 |
| **IDENTITY.md** | 名称、风格与表情 |
| **USER.md** | 用户画像与称呼方式 |
| **AGENTS.md** | 操作指令、记忆使用规则 |
| **MEMORY.md** | 跨会话长期记忆 |

---

## 🛠️ 内置工具

### 1. Terminal (命令行操作)
- 安全执行 Shell 命令，限制在 `root_dir` 内
- 自动拦截高危命令 (`rm -rf /`, `sudo`, `mkfs`, `dd` 等)
- 超时保护 (30 秒)

### 2. Python REPL (代码解释器)
- 执行 Python 代码，用于计算和数据处理
- 基于 LangChain 内置工具
- 支持异步执行

### 3. Fetch URL (网络获取)
- 获取网页内容，自动清洗 HTML 为 Markdown
- URL 安全过滤 (禁止访问内网地址)
- 超时保护 (10 秒)

### 4. Read File (文件读取)
- 读取本地文件，限制在项目目录内
- 防止目录穿越攻击
- 支持 UTF-8 编码

### 5. RAG Search (知识检索)
- 在知识库中进行混合检索 (BM25 + 向量)
- 基于 LlamaIndex 实现
- 可配置返回数量 (top_k)

---

## 📝 创建新 Skill

1. 在 `skills/` 下创建文件夹
2. 添加 `SKILL.md` 文件

```markdown
---
name: my_skill
description: 我的技能描述
---

# 技能名称

## 功能
描述技能的功能

## 使用方式
如何使用

## 示例
- 输入：xxx
- 输出：xxx
```

---

## ⚙️ 配置说明

### config.yaml
```yaml
# LLM 配置
llm:
  provider: qwen  # 支持：qwen, openai, anthropic, google
  model: qwen-turbo  # 通义千问免费模型
  api_key: ${DASHSCOPE_API_KEY}
  temperature: 0.7
  max_tokens: 4096

# 工具配置
tools:
  terminal:
    enabled: true
    root_dir: .
  python_repl:
    enabled: true
    timeout: 30
  fetch_url:
    enabled: true
    timeout: 10
  read_file:
    enabled: true
    root_dir: .
  rag_search:
    enabled: true
    top_k: 5

# 会话配置
sessions:
  storage_path: sessions/
  max_history: 50
  compress_threshold: 10000
```

### .env
```bash
# 通义千问 API Key (推荐，免费额度)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx

# OpenAI API Key (可选)
# OPENAI_API_KEY=sk-xxxxxxxxxxxx

# Moonshot/Kimi API Key (可选)
# KIMI_API_KEY=km-xxxxxxxxxxxx

# Alpha Vantage API Key (财报数据，可选)
# ALPHA_VANTAGE_API_KEY=xxxxxxxxxxxx
```

---

## 🔒 安全特性

- **工具沙箱化**: Terminal 和 Read File 限制在项目目录内操作
- **命令黑名单**: 拦截高危 Shell 命令 (`rm -rf /`, `sudo`, `mkfs`, `dd if=/dev/zero` 等)
- **URL 过滤**: 禁止访问内网地址 (`localhost`, `127.x.x.x`, `192.168.x.x`, `10.x.x.x`, `file://` 等)
- **会话隔离**: 每个会话独立存储在 `sessions/` 目录
- **输出截断**: 单次返回内容限制 10KB，防止 token 溢出
- **超时保护**: 命令执行超时自动终止 (30 秒)

---

## 📊 会话管理

- 会话存储在 `sessions/` 目录
- 每个会话一个 JSON 文件
- `sessions.json` 记录会话元数据
- 支持历史压缩 (超出阈值自动总结)

---

## 🚧 待实现功能

- [ ] Web 界面 (FastAPI + React)
- [ ] 飞书机器人集成 (Webhook 模式)
- [ ] 流式输出 (Server-Sent Events)
- [ ] 完整的 RAG 索引 (LlamaIndex + ChromaDB)
- [ ] 会话压缩算法 (超出阈值自动总结)
- [ ] 更多内置 Skills (日历、邮件、待办等)

---


## 📄 许可证

MIT License

---
##  简单运行

<img width="2418" height="1259" alt="屏幕截图 2026-03-24 210213" src="https://github.com/user-attachments/assets/ddd144a9-166f-4b5b-9d5c-0c1d0b79cff7" />

---

**基于 LangChain 构建 | 本地优先 | 安全可控**
