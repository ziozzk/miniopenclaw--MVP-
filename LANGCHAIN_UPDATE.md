# 🔄 LangChain 技术更新说明

**更新时间:** 2026-03-24  
**依据:** LangChain 官方文档 (https://docs.langchain.com)

---

## ✅ 已完成的更新

### 1. Agent 构建 API 更新

**旧方式 (已废弃):**
```python
from langchain.agents import create_openai_functions_agent, AgentExecutor

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

**新方式 (推荐):**
```python
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant",
)
```

**优势:**
- ✅ 更简洁的 API (少于 10 行代码)
- ✅ 基于 LangGraph 构建，支持持久化执行
- ✅ 自动支持人工介入、流式输出等高级功能
- ✅ 更好的错误处理和调试支持

---

### 2. LLM 导入更新

**旧方式:**
```python
from langchain.chat_models import ChatOpenAI
```

**新方式 (推荐):**
```python
from langchain_openai import ChatOpenAI
```

**说明:**
- LangChain 现在使用独立的包 `langchain-openai`
- 更好的版本控制和依赖管理
- 支持 OpenAI 兼容接口 (通义千问等)

---

### 3. 依赖包更新

**requirements.txt 变更:**

| 旧包 | 新包 | 说明 |
|------|------|------|
| `langchain.chat_models` | `langchain-openai` | 独立包 |
| `langchain.agents` | `langchain.agents` (内置) | 基于 LangGraph |
| - | `langchain-anthropic` | Claude 支持 (可选) |
| - | `langchain-google-genai` | Gemini 支持 (可选) |

---

## 📦 更新后的依赖

```txt
# LangChain 核心 (使用最新包结构)
langchain>=0.3.0
langchain-openai>=0.2.0  # OpenAI/通义千问模型
langchain-anthropic>=0.2.0  # Claude 模型 (可选)
langchain-google-genai>=0.1.0  # Google Gemini (可选)

# LangChain 社区工具
langchain-community>=0.3.0
langchain-experimental>=0.3.0  # Python REPL
```

---

## 🔧 代码变更

### agent/builder.py

**变更前:**
```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor

def _create_agent(self, llm, prompt):
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    return agent_executor
```

**变更后:**
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

def _create_agent(self, llm, system_prompt):
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent
```

---

### main.py

**变更前:**
```python
response = self.agent.invoke({"input": user_message, "history": messages})
```

**变更后:**
```python
response = self.agent.invoke({"messages": [{"role": "user", "content": user_message}]})
```

---

## 🎯 LangChain 官方推荐

根据官方文档，LangChain 产品矩阵:

| 产品 | 用途 | 推荐场景 |
|------|------|---------|
| **LangChain** | 快速构建 Agent | 标准 Agent 应用 ✅ |
| **Deep Agents** | 内置高级功能 | 需要自动压缩、子 Agent 等 |
| **LangGraph** | 低级编排框架 | 需要高度定制化 |

**Mini OpenClaw 选择:** LangChain (快速构建，满足需求)

---

## 📊 技术对比

| 特性 | 旧版本 | 新版本 |
|------|-------|-------|
| Agent API | `create_openai_functions_agent` | `create_agent` |
| 执行器 | `AgentExecutor` | 内置 (基于 LangGraph) |
| LLM 导入 | `langchain.chat_models` | `langchain_openai` |
| 代码行数 | ~15 行 | ~5 行 |
| LangGraph 支持 | ❌ | ✅ 内置 |
| 持久化执行 | ❌ | ✅ |
| 人工介入 | ❌ | ✅ |
| 流式输出 | ⚠️ | ✅ |

---

## ✅ 验证更新

运行以下命令验证:
```bash
cd backend
pip install -r requirements.txt
python main.py
```

测试对话:
```
你：你好
你：查询北京天气
你：列出当前目录
```

---

## 📚 参考文档

- LangChain 概述：https://docs.langchain.com/oss/python/langchain/overview
- Agent 快速开始：https://docs.langchain.com/oss/python/langchain/agents
- 工具集成：https://docs.langchain.com/oss/python/integrations/tools
- 安装指南：https://docs.langchain.com/oss/python/langchain/install

---

**更新完成！现在使用的是 LangChain 最新官方 API。** 🎉
