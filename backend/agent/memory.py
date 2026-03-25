#!/usr/bin/env python3
"""
记忆管理系统 - 负责会话管理、系统消息拼接、历史对话存储
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, config):
        self.config = config
        self.sessions_path = config["sessions"]["storage_path"]
        self.workspace_path = "workspace/"
        self.sessions_file = os.path.join(self.sessions_path, "sessions.json")
        
        # 确保目录存在
        os.makedirs(self.sessions_path, exist_ok=True)
        os.makedirs(self.workspace_path, exist_ok=True)
    
    def initialize(self):
        """初始化记忆系统"""
        # 1. 创建系统文件模板 (如果不存在)
        self._create_system_files()
        
        # 2. 生成 SKILLS_SNAPSHOT.md
        self._generate_skills_snapshot()
        
        # 3. 初始化 sessions.json
        self._init_sessions_file()
    
    def _create_system_files(self):
        """创建系统文件模板"""
        templates = {
            "SOUL.md": self._get_soul_template(),
            "IDENTITY.md": self._get_identity_template(),
            "USER.md": self._get_user_template(),
            "AGENTS.md": self._get_agents_template(),
            "MEMORY.md": "# 长期记忆\n\n## 偏好\n\n## 决策\n\n",
        }
        
        for filename, content in templates.items():
            filepath = os.path.join(self.workspace_path, filename)
            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
    
    def _get_soul_template(self):
        """SOUL.md 模板"""
        return """# SOUL.md

## 人格（Persona）
- **友好、专业、严谨**：以一种既友好又专业的语气与用户进行交互
- **适应性强**：根据用户的需求和情境调整语气和内容

## 语气（Tone）
- **友好而专业**：保持温和、友好，但又不失专业性
- **正向鼓励**：积极鼓励用户的努力，提供建设性反馈
- **适应性语气调整**：在不同情境下灵活调整语气

## 边界（Boundaries）
- **隐私保护**：尊重用户隐私，不收集敏感信息
- **任务范围限制**：在能力范围内提供帮助
- **道德与法律合规性**：遵循道德规范和法律规定
"""
    
    def _get_identity_template(self):
        """IDENTITY.md 模板"""
        return """# IDENTITY.md

## 名称（Name）
- **名称**：mini OpenClaw

## 风格（Vibe）
- **风格**：技术感与现代感兼具
- **简洁明了**：界面和交互设计简洁清晰
- **高效且精准**：专注于高效执行任务
- **易于扩展**：适应更多定制需求

## 表情（Emoji）
- **表情**：🤖
"""
    
    def _get_user_template(self):
        """USER.md 模板"""
        return """# USER.md

## 用户画像（User Profile）
- **用户类型**：技术人员、开发人员、职场人士
- **用户需求**：高效的知识查询、任务自动化、编程支持

## 称呼方式（Preferred Addressing）
- **默认称呼**：您
- **个性化称呼**：根据用户偏好调整
"""
    
    def _get_agents_template(self):
        """AGENTS.md 模板"""
        return """# AGENTS.md

## 操作指令（Operating Instructions）
- **工具优先级**：优先使用内置工具完成任务
- **任务分配**：根据用户指令自动选择适合的工具
- **任务执行**：遵循安全规则，高风险操作需用户确认

## 记忆使用规则（Memory Usage Rules）
- **长期记忆管理**：本地优先，所有历史对话存储在本地
- **重要事项存储**：用户反复强调的事项写入 MEMORY.md

## 优先级（Priorities）
- **安全优先**：始终将安全放在首位
- **效率优先**：选择高效的任务执行方式
- **用户体验优先**：提供流畅、无缝的交互体验
"""
    
    def _generate_skills_snapshot(self):
        """生成 SKILLS_SNAPSHOT.md"""
        skills_path = "skills/"
        skills_xml = ["<available_skills>"]
        
        if os.path.exists(skills_path):
            for skill_name in os.listdir(skills_path):
                skill_path = os.path.join(skills_path, skill_name)
                skill_md = os.path.join(skill_path, "SKILL.md")
                
                if os.path.isdir(skill_path) and os.path.exists(skill_md):
                    # 读取元数据
                    with open(skill_md, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 解析 YAML frontmatter
                    name = skill_name
                    description = "暂无描述"
                    
                    if content.startswith("---"):
                        lines = content.split("\n")
                        for line in lines[1:]:
                            if line.startswith("name:"):
                                name = line.replace("name:", "").strip()
                            elif line.startswith("description:"):
                                description = line.replace("description:", "").strip()
                    
                    skills_xml.append(f"""  <skill>
    <name>{name}</name>
    <description>{description}</description>
    <location>./skills/{skill_name}/SKILL.md</location>
  </skill>""")
        
        skills_xml.append("</available_skills>")
        
        # 写入文件
        with open("SKILLS_SNAPSHOT.md", "w", encoding="utf-8") as f:
            f.write("\n".join(skills_xml))
    
    def _init_sessions_file(self):
        """初始化 sessions.json"""
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, "w", encoding="utf-8") as f:
                json.dump({"sessions": []}, f, ensure_ascii=False, indent=2)
    
    def build_system_message(self):
        """构建系统消息 (6 部分拼接)"""
        parts = []
        
        # 1. SKILLS_SNAPSHOT.md
        skills_snapshot = self._read_file("SKILLS_SNAPSHOT.md")
        parts.append(skills_snapshot)
        
        # 2. SOUL.md
        soul = self._read_file(os.path.join(self.workspace_path, "SOUL.md"))
        parts.append(soul)
        
        # 3. IDENTITY.md
        identity = self._read_file(os.path.join(self.workspace_path, "IDENTITY.md"))
        parts.append(identity)
        
        # 4. USER.md
        user = self._read_file(os.path.join(self.workspace_path, "USER.md"))
        parts.append(user)
        
        # 5. AGENTS.md
        agents = self._read_file(os.path.join(self.workspace_path, "AGENTS.md"))
        parts.append(agents)
        
        # 6. MEMORY.md
        memory = self._read_file("MEMORY.md")
        parts.append(memory)
        
        # 拼接，每部分超过 20k 则截断
        system_message = ""
        for part in parts:
            if len(part) > 20000:
                part = part[:20000] + "\n\n[...内容已截断...]"
            system_message += part + "\n\n"
        
        return system_message
    
    def _read_file(self, filepath):
        """读取文件"""
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    
    def create_session(self, title):
        """创建新会话"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_file = os.path.join(self.sessions_path, f"{title}.json")
        
        session_data = {
            "session_id": session_id,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": {
                "model": self.config["llm"]["model"],
                "token_count": 0,
            }
        }
        
        # 保存会话文件
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        # 更新 sessions.json
        self._update_sessions_index(title, session_file)
        
        return title
    
    def _update_sessions_index(self, title, session_file):
        """更新 sessions.json 索引"""
        with open(self.sessions_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 检查是否已存在
        for session in data["sessions"]:
            if session["title"] == title:
                session["updated_at"] = datetime.now().isoformat()
                break
        else:
            data["sessions"].append({
                "title": title,
                "file": os.path.basename(session_file),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message_count": 0,
            })
        
        with open(self.sessions_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def build_messages(self, session_title, current_message):
        """构建消息队列"""
        session_file = os.path.join(self.sessions_path, f"{session_title}.json")
        
        if os.path.exists(session_file):
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            # 获取历史消息
            history = session_data.get("messages", [])
            
            # 限制历史消息数量
            max_history = self.config["sessions"]["max_history"]
            if len(history) > max_history:
                history = history[-max_history:]
            
            return history
        return []
    
    def append_message(self, session_title, role, content):
        """追加消息到会话"""
        session_file = os.path.join(self.sessions_path, f"{session_title}.json")
        
        if os.path.exists(session_file):
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            # 追加消息
            session_data["messages"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
            })
            session_data["updated_at"] = datetime.now().isoformat()
            session_data["metadata"]["message_count"] = len(session_data["messages"])
            
            # 保存
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            # 更新索引
            self._update_sessions_index(session_title, session_file)
