#!/usr/bin/env python3
"""
安全网络获取工具 - 获取 URL 内容并清洗为 Markdown
"""

import requests
from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

try:
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    BeautifulSoup = None
    html2text = None


class FetchURLInput(BaseModel):
    """URL 输入"""
    url: str = Field(description="要获取的 URL 地址")


class SafeRequestsGetTool(BaseTool):
    """安全网络获取工具"""
    
    name: str = "fetch_url"
    description: str = "获取指定 URL 的网页内容，返回清洗后的 Markdown 或纯文本。用于联网查询信息。"
    args_schema: Type[BaseModel] = FetchURLInput
    timeout: int = 10
    
    def __init__(self, timeout: int = 10, **kwargs):
        super().__init__(timeout=timeout, **kwargs)
    
    def _run(self, url: str) -> str:
        """获取 URL 内容"""
        # URL 安全检查
        if not self._is_safe_url(url):
            return "❌ 错误：URL 不安全或被禁止访问"
        
        try:
            # 发送请求
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; MiniOpenClaw/1.0)"
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            # 获取内容
            content = response.text
            
            # 清洗 HTML
            if BeautifulSoup and html2text:
                content = self._clean_html(content)
            
            # 限制返回长度
            if len(content) > 10000:
                content = content[:10000] + "\n\n[...内容已截断...]"
            
            return content
            
        except requests.Timeout:
            return f"❌ 错误：请求超时 ({self.timeout}秒)"
        except requests.RequestException as e:
            return f"❌ 错误：{str(e)}"
    
    def _is_safe_url(self, url: str) -> bool:
        """检查 URL 是否安全"""
        # 禁止访问内网地址
        forbidden_prefixes = [
            "file://",
            "http://localhost",
            "http://127.",
            "http://192.168.",
            "http://10.",
            "http://172.16.",
        ]
        
        for prefix in forbidden_prefixes:
            if url.lower().startswith(prefix):
                return False
        
        return True
    
    def _clean_html(self, html_content: str) -> str:
        """清洗 HTML 为 Markdown"""
        try:
            # 使用 html2text 转换
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = True
            h.ignore_emphasis = False
            markdown = h.handle(html_content)
            return markdown
        except Exception:
            # 降级：使用 BeautifulSoup 提取文本
            soup = BeautifulSoup(html_content, "html.parser")
            # 移除脚本和样式
            for tag in soup(["script", "style"]):
                tag.decompose()
            return soup.get_text(separator="\n", strip=True)
    
    async def _arun(self, url: str) -> str:
        """异步执行 (暂不支持)"""
        return self._run(url)
