# 📦 Mini OpenClaw 安装指南

---

## 系统要求

- **Python**: 3.10 或更高版本
- **操作系统**: macOS / Linux / Windows
- **内存**: 4GB+
- **存储**: 1GB+

---

## 快速安装

### 1. 克隆/下载项目

```bash
cd ~/Desktop/mini-openclaw/backend
```

### 2. 安装依赖

**macOS/Linux:**
```bash
pip install -r requirements.txt
```

**Windows:**
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

**macOS/Linux:**
```bash
cp .env.example .env
nano .env  # 编辑填入 API Key
```

**Windows:**
```bash
copy .env.example .env
notepad .env  # 编辑填入 API Key
```

### 4. 配置配置文件

```bash
cp config.yaml.example config.yaml
```

### 5. 启动

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

或直接运行:
```bash
python main.py
```

---

## 获取 API Key

### OpenAI (推荐)
1. 访问：https://platform.openai.com/api-keys
2. 创建新 API Key
3. 复制到 `.env`:
   ```bash
   OPENAI_API_KEY=sk-xxxxx
   ```

### 通义千问 (国内)
1. 访问：https://dashscope.console.aliyun.com/
2. 创建 API Key
3. 修改 `config.yaml`:
   ```yaml
   llm:
     provider: qwen
     model: qwen-plus
   ```
4. 复制到 `.env`:
   ```bash
   DASHSCOPE_API_KEY=sk-xxxxx
   ```

### Alpha Vantage (股票数据)
1. 访问：https://www.alphavantage.co/support/#api-key
2. 免费获取 API Key
3. 复制到 `.env`:
   ```bash
   ALPHA_VANTAGE_API_KEY=xxxxx
   ```

---

## 验证安装

```bash
python main.py
```

看到以下输出表示成功:
```
🤖 Mini OpenClaw v0.1.0
==================================================

📦 初始化系统...
🛠️  注册工具...
   已加载 5 个工具：terminal, python_repl, fetch_url, read_file, rag_search
💾 初始化记忆系统...
🧠 构建 Agent...
📄 加载系统消息...
   系统消息长度：xxxx 字符

✅ 初始化完成!

==================================================
💬 命令行交互模式 (输入 '退出' 或 'quit' 结束)
==================================================
```

---

## 常见问题

### Q: `pip install` 失败
**A:** 尝试使用国内镜像:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 找不到 Python
**A:** 确保 Python 3.10+ 已安装并添加到 PATH

### Q: 导入错误
**A:** 确保在 `backend/` 目录下运行，并且已激活虚拟环境

### Q: API Key 错误
**A:** 检查 `.env` 文件是否正确配置，确保没有多余的空格

---

## 下一步

安装完成后，查看 [README.md](README.md) 了解使用方法。
