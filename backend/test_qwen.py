#!/usr/bin/env python3
"""测试通义千问免费模型"""

import requests

api_key = "sk-e2ee61e61a8943efb1cd3758deb4817e"

print(f"测试 API Key: {api_key[:10]}...{api_key[-5:]}")
print("模型：qwen-turbo (免费)")
print("-" * 50)

response = requests.post(
    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "qwen-turbo",
        "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}]
    }
)

print(f"\n状态码：{response.status_code}")

if response.status_code == 200:
    data = response.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(f"\n✅ 成功!\n")
    print(f"AI 回复：{content}")
else:
    print(f"\n❌ 失败!\n")
    print(f"错误信息：{response.text}")
    print("\n可能原因:")
    print("1. API Key 无效或已过期")
    print("2. 账号未开通百炼服务")
    print("3. 账号欠费")
    print("\n请访问 https://bailian.console.aliyun.com/ 检查")
