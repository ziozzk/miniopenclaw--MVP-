#!/bin/bash
# Mini OpenClaw 快速启动脚本

echo "🤖 Mini OpenClaw 启动脚本"
echo "========================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    exit 1
fi

echo "✅ Python 版本：$(python3 --version)"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo ""
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "📦 检查依赖..."
pip install -q -r requirements.txt

# 检查配置文件
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  未找到 .env 文件"
    echo "📝 请复制 .env.example 并配置 API Key:"
    echo "   cp .env.example .env"
    echo ""
fi

if [ ! -f "config.yaml" ]; then
    echo ""
    echo "⚠️  未找到 config.yaml 文件"
    echo "📝 请复制 config.yaml.example:"
    echo "   cp config.yaml.example config.yaml"
    echo ""
fi

# 启动
echo ""
echo "🚀 启动 Mini OpenClaw..."
echo ""
python main.py "$@"
