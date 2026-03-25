#!/usr/bin/env python3
"""
工具注册模块 - 注册 5 个内置核心工具
"""

from langchain_community.tools import ShellTool, RequestsGetTool
from langchain_community.tools.file_management import ReadFileTool
from langchain_experimental.tools import PythonREPLTool

from tools.terminal import SafeShellTool
from tools.fetch_url import SafeRequestsGetTool
from tools.read_file import SafeReadFileTool
from tools.rag_search import RAGSearchTool


def register_tools(tool_config):
    """注册所有工具"""
    tools = {}
    
    # 1. Terminal (命令行操作)
    if tool_config.get("terminal", {}).get("enabled", True):
        root_dir = tool_config["terminal"].get("root_dir", ".")
        tools["terminal"] = SafeShellTool(root_dir=root_dir)
    
    # 2. Python REPL (代码解释器)
    if tool_config.get("python_repl", {}).get("enabled", True):
        timeout = tool_config["python_repl"].get("timeout", 30)
        tools["python_repl"] = PythonREPLTool()
    
    # 3. Fetch URL (网络信息获取)
    if tool_config.get("fetch_url", {}).get("enabled", True):
        timeout = tool_config["fetch_url"].get("timeout", 10)
        tools["fetch_url"] = SafeRequestsGetTool(timeout=timeout)
    
    # 4. Read File (文件读取)
    if tool_config.get("read_file", {}).get("enabled", True):
        root_dir = tool_config["read_file"].get("root_dir", ".")
        tools["read_file"] = SafeReadFileTool(root_dir=root_dir)
    
    # 5. RAG Search (知识检索)
    if tool_config.get("rag_search", {}).get("enabled", True):
        top_k = tool_config["rag_search"].get("top_k", 5)
        tools["rag_search"] = RAGSearchTool(top_k=top_k)
    
    return tools


__all__ = ["register_tools"]
