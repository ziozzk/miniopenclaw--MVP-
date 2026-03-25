#!/usr/bin/env python3
"""
RAG 检索工具 - 基于 LlamaIndex 的混合检索 (BM25 + 向量检索)
"""

import os
from typing import Type, List
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class RAGSearchInput(BaseModel):
    """RAG 检索输入"""
    query: str = Field(description="检索查询语句")


class RAGSearchTool(BaseTool):
    """RAG 检索工具"""
    
    name: str = "search_knowledge_base"
    description: str = "在本地知识库中进行深度检索，支持关键词和语义检索。用于查询文档、PDF、笔记等。"
    args_schema: Type[BaseModel] = RAGSearchInput
    top_k: int = 5
    
    def __init__(self, top_k: int = 5, **kwargs):
        super().__init__(top_k=top_k, **kwargs)
        object.__setattr__(self, "index_path", "storage/vector_index")
        object.__setattr__(self, "knowledge_path", "knowledge/")
        object.__setattr__(self, "_index", None)
    
    def _run(self, query: str) -> str:
        """执行检索"""
        try:
            # 尝试使用 LlamaIndex (如果安装)
            try:
                from llama_index.core import (
                    StorageContext,
                    VectorStoreIndex,
                    load_index_from_storage,
                )
                from llama_index.core.node_parser import SimpleDirectoryReader
                
                # 检查索引是否存在
                if os.path.exists(self.index_path) and os.listdir(self.index_path):
                    # 加载已有索引
                    storage_context = StorageContext.from_defaults(persist_dir=self.index_path)
                    index = load_index_from_storage(storage_context)
                else:
                    # 构建新索引
                    if not os.path.exists(self.knowledge_path):
                        os.makedirs(self.knowledge_path)
                        return f"⚠️  知识库目录为空，请先在 {self.knowledge_path} 中添加文档"
                    
                    documents = SimpleDirectoryReader(self.knowledge_path).load_data()
                    index = VectorStoreIndex.from_documents(documents)
                    index.storage_context.persist(persist_dir=self.index_path)
                
                # 执行检索
                query_engine = index.as_query_engine(similarity_top_k=self.top_k)
                response = query_engine.query(query)
                
                return str(response)
                
            except ImportError:
                # LlamaIndex 未安装，使用简单关键词检索
                return self._simple_search(query)
                
        except Exception as e:
            return f"❌ 检索错误：{str(e)}"
    
    def _simple_search(self, query: str) -> str:
        """简单关键词检索 (降级方案)"""
        if not os.path.exists(self.knowledge_path):
            return "⚠️  知识库目录不存在"
        
        results = []
        query_lower = query.lower()
        
        # 遍历知识库文件
        for filename in os.listdir(self.knowledge_path):
            filepath = os.path.join(self.knowledge_path, filename)
            
            if os.path.isfile(filepath) and filename.endswith((".md", ".txt")):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 简单关键词匹配
                    if query_lower in content.lower():
                        # 提取相关片段
                        lines = content.split("\n")
                        for i, line in enumerate(lines):
                            if query_lower in line.lower():
                                # 获取上下文
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                snippet = "\n".join(lines[start:end])
                                results.append(f"📄 {filename}:\n{snippet}\n")
                                break
                
                except Exception:
                    continue
        
        if results:
            return "\n---\n".join(results[:self.top_k])
        else:
            return "未找到相关内容"
    
    async def _arun(self, query: str) -> str:
        """异步执行 (暂不支持)"""
        return self._run(query)
