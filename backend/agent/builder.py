#!/usr/bin/env python3
"""
Agent 构建器 - 基于 LangChain 构建 AI Agent
使用 LangChain 最新 API (基于 LangGraph)
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


class AgentBuilder:
    """Agent 构建器"""
    
    def __init__(self, config, tools, memory_manager):
        self.config = config
        self.tools = tools
        self.memory_manager = memory_manager
    
    def build(self):
        """构建 Agent"""
        # 1. 初始化 LLM
        llm = self._init_llm()
        
        # 2. 获取系统消息
        system_prompt = self.memory_manager.build_system_message()
        
        # 3. 创建 Agent (使用 LangChain 最新 create_agent API)
        agent = self._create_agent(llm, system_prompt)
        
        return agent
    
    def _init_llm(self):
        """初始化 LLM (使用 langchain-openai 包)"""
        llm_config = self.config["llm"]
        
        # 硬编码 API Key (私人使用)
        DASHSCOPE_API_KEY = "sk-e2ee61e61a8943efb1cd3758deb4817e"
        
        if llm_config["provider"] == "openai":
            return ChatOpenAI(
                model=llm_config["model"],
                api_key=llm_config["api_key"],
                temperature=llm_config["temperature"],
                max_tokens=llm_config["max_tokens"],
            )
        elif llm_config["provider"] == "qwen":
            # 通义千问配置 (使用 OpenAI 兼容接口)
            return ChatOpenAI(
                model=llm_config["model"],
                api_key=DASHSCOPE_API_KEY,  # 直接使用硬编码 Key
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                temperature=llm_config["temperature"],
                max_tokens=llm_config["max_tokens"],
            )
        elif llm_config["provider"] == "kimi":
            # Kimi 配置 (使用 OpenAI 兼容接口)
            return ChatOpenAI(
                model=llm_config["model"],
                api_key=llm_config["api_key"],
                base_url="https://api.moonshot.cn/v1",
                temperature=llm_config["temperature"],
                max_tokens=llm_config["max_tokens"],
            )
        else:
            raise ValueError(f"不支持的 LLM 提供商：{llm_config['provider']}")
    
    def _create_agent(self, llm, system_prompt):
        """创建 Agent (使用 LangChain 最新 create_agent API)"""
        # 转换为 LangChain 工具格式
        langchain_tools = list(self.tools.values())
        
        # 使用 LangChain 最新 create_agent API
        # 基于 LangGraph 构建，支持持久化执行、人工介入等高级功能
        agent = create_agent(
            model=llm,
            tools=langchain_tools,
            system_prompt=system_prompt,
        )
        
        return agent
