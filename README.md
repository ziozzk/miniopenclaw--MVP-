# 🤖 Mini OpenClaw

**轻量级 AI Agent 框架** - 基于 LangChain 构建，支持 Skills 系统和本地记忆管理

---

## ✨ 特性

- 🛠️ **5 个内置工具**: Terminal、Python REPL、Fetch URL、Read File、RAG Search
- 📚 **Skills 系统**: 类似 Anthropic Skills 的可扩展技能机制
- 💾 **本地记忆**: 会话历史、系统消息、长期记忆全部本地存储
- 🔒 **安全优先**: 工具沙箱化、文件访问限制、命令黑名单
- 📝 **Markdown 配置**: 所有配置使用 Markdown 文件，易于编辑和版本控制

---

## 🚀 快速开始

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
# OPENAI_API_KEY=sk-xxx
```

### 3. 启动

```bash
python main.py
```

### 4. 开始对话

```
你：你好
🤖 你好！我是 mini OpenClaw，有什么可以帮你？

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
│   │   ├── __init__.py            # 工具注册
│   │   ├── terminal.py            # Shell 工具
│   │   ├── python_repl.py         # Python 解释器
│   │   ├── fetch_url.py           # 网络获取
│   │   ├── read_file.py           # 文件读取
│   │   └── rag_search.py          # RAG 检索
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
| **SKILLS_SNAPSHOT.md** | 可用 Skills 列表 (自动生成) |
| **SOUL.md** | 人格、语气与边界 |
| **IDENTITY.md** | 名称、风格与表情 |
| **USER.md** | 用户画像与称呼方式 |
| **AGENTS.md** | 操作指令、记忆使用规则 |
| **MEMORY.md** | 跨线程长期记忆 |

---

## 🛠️ 内置工具

### 1. Terminal (命令行操作)
```python
# 安全执行 Shell 命令，限制在 root_dir 内
# 自动拦截高危命令 (rm -rf, sudo 等)
```

### 2. Python REPL (代码解释器)
```python
# 执行 Python 代码，用于计算和数据处理
```

### 3. Fetch URL (网络获取)
```python
# 获取网页内容，自动清洗 HTML 为 Markdown
```

### 4. Read File (文件读取)
```python
# 读取本地文件，限制在项目目录内
```

### 5. RAG Search (知识检索)
```python
# 在知识库中进行混合检索 (BM25 + 向量)
```

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
llm:
  provider: openai  # 或 qwen
  model: gpt-4o-mini
  api_key: ${OPENAI_API_KEY}

tools:
  terminal:
    enabled: true
    root_dir: .
```

### .env
```bash
OPENAI_API_KEY=sk-xxx
ALPHA_VANTAGE_API_KEY=xxx
```

---

## 🔒 安全特性

- **工具沙箱化**: Terminal 和 Read File 限制操作范围
- **命令黑名单**: 拦截高危 Shell 命令
- **URL 过滤**: 禁止访问内网地址
- **会话隔离**: 每个会话独立存储

---

## 📊 会话管理

- 会话存储在 `sessions/` 目录
- 每个会话一个 JSON 文件
- `sessions.json` 记录会话元数据
- 支持历史压缩 (超出阈值自动总结)

---

## 🚧 待实现功能

- [ ] Web 界面
- [ ] 飞书机器人集成
- [ ] 流式输出
- [ ] 完整的 RAG 索引 (LlamaIndex)
- [ ] 会话压缩算法

---

## 📄 许可证

MIT License

---

**基于 LangChain 构建 | 本地优先 | 安全可控**
