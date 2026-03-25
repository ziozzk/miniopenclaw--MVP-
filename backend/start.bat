@echo off
REM Mini OpenClaw Windows 启动脚本

echo.
echo 🤖 Mini OpenClaw 启动脚本
echo ========================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python
    exit /b 1
)

echo ✅ Python 版本:
python --version
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo.
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo 📦 检查依赖...
pip install -q -r requirements.txt

REM 检查配置文件
if not exist ".env" (
    echo.
    echo ⚠️  未找到 .env 文件
    echo 📝 请复制 .env.example 并配置 API Key:
    echo    copy .env.example .env
    echo.
)

if not exist "config.yaml" (
    echo.
    echo ⚠️  未找到 config.yaml 文件
    echo 📝 请复制 config.yaml.example:
    echo    copy config.yaml.example config.yaml
    echo.
)

REM 启动
echo.
echo 🚀 启动 Mini OpenClaw...
echo.
python main.py %*
