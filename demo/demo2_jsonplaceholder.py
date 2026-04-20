"""
模块三 · Demo 2：调用真实接口（JSONPlaceholder）
================================================
目标：让 AI 真正发起 HTTP 请求，亲眼看到"AI 动手做事"。

讲解节奏（约 10 分钟）：
  1. 运行一次，看 AI 调 http_get → 真实 HTTP 请求 → 返回数据
  2. 追问"再查 /posts/2 和 /posts/3 告诉我标题"，看多轮对话
  3. 追问"userId 是不是 1"，看 AI 基于上下文的判断

与 Demo 1 的关键区别：
  - 工具函数变成真正的 requests.get()
  - 对话支持多轮，messages 持续累积

用法：
  python demo/demo2_jsonplaceholder.py
"""
import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
)
MODEL = os.getenv("LLM_MODEL", "glm-4-flash")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "http_get",
            "description": (
                "对一个 HTTP 接口发起 GET 请求，返回 JSON 响应。"
                "用于查询接口数据，不会修改服务端状态。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "完整的接口 URL（包含协议和路径）",
                    }
                },
                "required": ["url"],
            },
        },
    }
]


def http_get(url: str) -> dict:
    """真实发起 HTTP GET 请求。"""
    try:
        resp = requests.get(url, timeout=10)
        return {"status_code": resp.status_code, "body": resp.json()}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def chat_loop() -> None:
    messages = [
        {
            "role": "system",
            "content": "你是一个 API 探索助手。遇到查询需求时，主动调 http_get 工具去拿真实数据。",
        }
    ]
    print("💬 多轮对话已启动，输入 quit 退出\n")
    print("👉 建议依次试这 3 句：")
    print("   1. 查一下 https://jsonplaceholder.typicode.com/posts/1 这个接口返回什么")
    print("   2. 再查 /posts/2 和 /posts/3，告诉我这三篇文章的标题")
    print("   3. /posts/1 的 userId 是多少？是不是 1？\n")

    while True:
        user_input = input(">>> 用户: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        while True:
            resp = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS
            )
            msg = resp.choices[0].message
            messages.append(msg.model_dump(exclude_unset=True))

            if not msg.tool_calls:
                print(f"\n🤖 助手: {msg.content}\n")
                break

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                print(f"  🔧 调用: http_get({args})")
                result = http_get(**args)
                preview = json.dumps(result, ensure_ascii=False)[:150]
                print(f"  📥 返回: {preview}{'...' if len(preview) >= 150 else ''}")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )


if __name__ == "__main__":
    chat_loop()
