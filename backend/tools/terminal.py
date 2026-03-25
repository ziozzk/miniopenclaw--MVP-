#!/usr/bin/env python3
"""
安全 Shell 工具 - 限制操作范围，拦截高危指令
"""

import os
import subprocess
from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class SafeShellInput(BaseModel):
    """Shell 命令输入"""
    command: str = Field(description="要执行的 shell 命令")


class SafeShellTool(BaseTool):
    """安全 Shell 工具"""
    
    name: str = "terminal"
    description: str = "在受限的安全环境下执行 Shell 命令。用于执行文件操作、系统查询等任务。"
    args_schema: Type[BaseModel] = SafeShellInput
    root_dir: str = "."
    
    def __init__(self, root_dir: str = ".", **kwargs):
        super().__init__(root_dir=os.path.abspath(root_dir), **kwargs)
        object.__setattr__(self, "blacklist", [
            "rm -rf /",
            "sudo",
            "mkfs",
            "dd if=/dev/zero",
            ":(){:|:&};:",
            "chmod 777 /",
            "chown -R",
        ])
    
    def _run(self, command: str) -> str:
        """执行 Shell 命令"""
        # 安全检查
        if not self._is_safe_command(command):
            return "❌ 错误：命令包含高危操作，已被拦截"
        
        try:
            # 在限制的目录内执行
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.root_dir,
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n错误：{result.stderr}"
            
            return output.strip() or "命令执行成功，无输出"
            
        except subprocess.TimeoutExpired:
            return "❌ 错误：命令执行超时 (30 秒)"
        except Exception as e:
            return f"❌ 错误：{str(e)}"
    
    def _is_safe_command(self, command: str) -> bool:
        """检查命令是否安全"""
        command_lower = command.lower()
        
        # 检查黑名单
        for blocked in self.blacklist:
            if blocked in command_lower:
                return False
        
        # 检查是否尝试跳出根目录
        if ".." in command and self.root_dir in command:
            return False
        
        return True
    
    async def _arun(self, command: str) -> str:
        """异步执行 (暂不支持)"""
        return self._run(command)
