#!/usr/bin/env python3
"""
安全文件读取工具 - 限制读取范围，防止访问系统文件
"""

import os
from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    """文件读取输入"""
    file_path: str = Field(description="要读取的文件路径")


class SafeReadFileTool(BaseTool):
    """安全文件读取工具"""
    
    name: str = "read_file"
    description: str = "读取本地指定文件的内容。用于读取 Skills 文档、配置文件等。"
    args_schema: Type[BaseModel] = ReadFileInput
    root_dir: str = "."
    
    def __init__(self, root_dir: str = ".", **kwargs):
        super().__init__(root_dir=os.path.abspath(root_dir), **kwargs)
    
    def _run(self, file_path: str) -> str:
        """读取文件内容"""
        # 安全检查
        safe_path = self._get_safe_path(file_path)
        
        if not safe_path:
            return f"❌ 错误：禁止访问该路径 (超出根目录范围)"
        
        if not os.path.exists(safe_path):
            return f"❌ 错误：文件不存在：{file_path}"
        
        if not os.path.isfile(safe_path):
            return f"❌ 错误：不是文件：{file_path}"
        
        try:
            with open(safe_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 限制返回长度
            if len(content) > 50000:
                content = content[:50000] + "\n\n[...内容已截断...]"
            
            return content
            
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(safe_path, "r", encoding="gbk") as f:
                    content = f.read()
                return content
            except Exception:
                return "❌ 错误：无法解码文件 (可能是二进制文件)"
        except Exception as e:
            return f"❌ 错误：{str(e)}"
    
    def _get_safe_path(self, file_path: str) -> str:
        """获取安全路径"""
        # 如果是相对路径，拼接根目录
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.root_dir, file_path)
        
        # 解析绝对路径
        abs_path = os.path.abspath(file_path)
        
        # 检查是否在根目录内
        if not abs_path.startswith(self.root_dir):
            return None
        
        return abs_path
    
    async def _arun(self, file_path: str) -> str:
        """异步执行 (暂不支持)"""
        return self._run(file_path)
