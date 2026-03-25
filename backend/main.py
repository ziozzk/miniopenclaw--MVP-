#!/usr/bin/env python3
"""
Mini OpenClaw - 轻量级 AI Agent 框架
基于 LangChain 构建，支持 Skills 系统和本地记忆管理
"""

import os
import sys
import yaml
import argparse
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量 (优先加载当前目录的 .env)
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"📦 已加载 .env 文件：{env_path}")
else:
    print("⚠️  未找到 .env 文件")

from agent.builder import AgentBuilder
from agent.memory import MemoryManager
from tools import register_tools


class MiniOpenClaw:
    """Mini OpenClaw 主类"""
    
    def __init__(self, config_path="config.yaml"):
        """初始化 Mini OpenClaw"""
        self.config = self._load_config(config_path)
        self.memory_manager = MemoryManager(self.config)
        self.agent = None
        self.current_session = None
        
        print("\n🤖 Mini OpenClaw v0.1.0")
        print("=" * 50)
        
        # 调试：检查 API Key
        api_key = self.config["llm"]["api_key"]
        if api_key:
            print(f"✅ API Key 已加载：{api_key[:10]}...{api_key[-5:]}")
        else:
            print("❌ 警告：API Key 为空，请检查 .env 文件")
        
    def _load_config(self, config_path):
        """加载配置文件"""
        # 从环境变量读取 API Key
        dashscope_api_key = os.getenv("DASHSCOPE_API_KEY", "")
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        kimi_api_key = os.getenv("KIMI_API_KEY", "")
        
        # 如果环境变量为空，尝试直接读取 .env 文件
        if not dashscope_api_key:
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("DASHSCOPE_API_KEY="):
                            dashscope_api_key = line.split("=", 1)[1].strip()
                            break
        
        default_config = {
            "llm": {
                "provider": "qwen",
                "model": "qwen-max",
                "api_key": dashscope_api_key or openai_api_key or kimi_api_key,
                "temperature": 0.7,
                "max_tokens": 4096,
            },
            "tools": {
                "terminal": {"enabled": True, "root_dir": os.getcwd()},
                "python_repl": {"enabled": True, "timeout": 30},
                "fetch_url": {"enabled": True, "timeout": 10},
                "read_file": {"enabled": True, "root_dir": os.getcwd()},
                "rag_search": {"enabled": True, "top_k": 5},
            },
            "sessions": {
                "storage_path": "sessions/",
                "max_history": 50,
                "compress_threshold": 10000,
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = yaml.safe_load(f)
                # 合并配置
                for key in default_config:
                    if key in file_config:
                        if isinstance(default_config[key], dict):
                            default_config[key].update(file_config[key])
                        else:
                            default_config[key] = file_config[key]
        
        return default_config
    
    def initialize(self):
        """初始化系统"""
        print("\n📦 初始化系统...")
        
        # 1. 注册工具
        print("🛠️  注册工具...")
        self.tools = register_tools(self.config["tools"])
        print(f"   已加载 {len(self.tools)} 个工具: {', '.join(self.tools.keys())}")
        
        # 2. 初始化记忆管理
        print("💾 初始化记忆系统...")
        self.memory_manager.initialize()
        
        # 3. 构建 Agent
        print("🧠 构建 Agent...")
        self.agent = AgentBuilder(self.config, self.tools, self.memory_manager).build()
        
        # 4. 加载系统消息
        print("📄 加载系统消息...")
        system_message = self.memory_manager.build_system_message()
        print(f"   系统消息长度：{len(system_message)} 字符")
        
        print("\n✅ 初始化完成!\n")
        return self
    
    def start_cli(self):
        """启动命令行交互模式"""
        print("=" * 50)
        print("💬 命令行交互模式 (输入 '退出' 或 'quit' 结束)")
        print("=" * 50 + "\n")
        
        while True:
            try:
                user_input = input("你：").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["退出", "quit", "exit"]:
                    print("\n🤖 再见！会话已保存。")
                    break
                
                # 处理用户输入
                response = self._process_message(user_input)
                print(f"\n🤖 {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 再见！会话已保存。")
                break
            except Exception as e:
                print(f"\n❌ 错误：{str(e)}\n")
    
    def _process_message(self, user_message):
        """处理用户消息"""
        # 1. 获取或创建会话
        if not self.current_session:
            self.current_session = self.memory_manager.create_session("新会话")
        
        # 2. 构建消息队列
        messages = self.memory_manager.build_messages(
            self.current_session,
            user_message
        )
        
        # 3. 调用 Agent (使用最新 LangChain API)
        response = self.agent.invoke({"messages": [{"role": "user", "content": user_message}]})
        
        # 4. 提取 AI 回复内容
        ai_content = ""
        if isinstance(response, dict):
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    ai_content = last_message.content
                elif isinstance(last_message, dict):
                    ai_content = last_message.get("content", "")
        elif hasattr(response, "content"):
            ai_content = response.content
        else:
            ai_content = str(response)
        
        # 5. 保存对话
        self.memory_manager.append_message(
            self.current_session,
            "user",
            user_message
        )
        self.memory_manager.append_message(
            self.current_session,
            "assistant",
            ai_content
        )
        
        return ai_content


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Mini OpenClaw - 轻量级 AI Agent 框架")
    parser.add_argument("--config", type=str, default="config.yaml", help="配置文件路径")
    parser.add_argument("--web", action="store_true", help="启动 Web 模式")
    parser.add_argument("--feishu", action="store_true", help="启动飞书机器人模式")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    
    args = parser.parse_args()
    
    # 创建并初始化 Mini OpenClaw
    app = MiniOpenClaw(config_path=args.config)
    app.initialize()
    
    # 启动模式
    if args.web:
        print(f"\n🌐 Web 服务已启动")
        print(f"📍 访问地址：http://localhost:{args.port}")
        # TODO: 实现 Web 服务器
        print("⚠️  Web 模式尚未实现，请使用命令行模式")
        app.start_cli()
    elif args.feishu:
        print(f"\n🔔 飞书 Webhook 已启动")
        print(f"📍 Webhook URL: http://0.0.0.0:{args.port}/feishu/webhook")
        # TODO: 实现飞书 Webhook
        print("⚠️  飞书模式尚未实现，请使用命令行模式")
        app.start_cli()
    else:
        app.start_cli()


if __name__ == "__main__":
    main()
