"""
模块三 · Demo 1：Hello Function Calling
=========================================
目标：让学员亲眼看到 LLM 返回的原始 tool_calls 结构。

3 个"啊哈时刻"：
  1. 正常调用 → 看到 tool_calls JSON
  2. 缺参数 → LLM 反问而不是瞎编
  3. 并行调用 → 一次返回多个 tool_call

用法：
  python demo/demo1_weather.py
"""
import json
import os

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
            "name": "get_weather",
            "description": "查询指定城市的实时天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，例如：上海、北京",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


def mock_get_weather(city: str) -> dict:
    """模拟天气 API（不真发请求，课堂演示用）"""
    fake = {
        "上海": {"temp": 22, "weather": "多云"},
        "北京": {"temp": 28, "weather": "晴"},
        "广州": {"temp": 31, "weather": "雷阵雨"},
        "深圳": {"temp": 30, "weather": "阴"},
    }
    return fake.get(city, {"temp": 20, "weather": "未知"})


def ask(question: str) -> None:
    print("\n" + "=" * 60)
    print(f"👤 用户: {question}")
    print("=" * 60)

    messages = [{"role": "user", "content": question}]

    resp = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS
    )
    msg = resp.choices[0].message

    print("\n📦 LLM 首轮返回（关键观察对象）：")
    print(json.dumps(msg.model_dump(exclude_unset=True), ensure_ascii=False, indent=2))

    if not msg.tool_calls:
        print(f"\n🤖 LLM 直接回复（未调用工具）: {msg.content}")
        return

    messages.append(msg.model_dump(exclude_unset=True))
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments or "{}")
        print(f"\n🔧 LLM 建议调用: {tc.function.name}({args})")
        result = mock_get_weather(**args)
        print(f"📥 mock 返回: {result}")
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False),
            }
        )

    resp2 = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    print(f"\n🤖 LLM 最终回复: {resp2.choices[0].message.content}")


def main():
    print("=" * 60)
    print("🌤️  天气 Demo —— 体验 Function Calling")
    print("=" * 60)
    print()
    print("预设问题（输入数字直接体验）：")
    print("  1. 上海今天天气怎么样？        → 正常调用，观察 tool_calls")
    print("  2. 今天天气怎么样？            → 缺参数，观察 LLM 反问")
    print("  3. 上海和北京哪个更热？        → 并行调用，观察多个 tool_call")
    print()
    print("也可以直接输入你自己的问题，输入 quit 退出")
    print("=" * 60)

    presets = {
        "1": "上海今天天气怎么样？",
        "2": "今天天气怎么样？",
        "3": "上海和北京哪个更热？",
    }

    while True:
        try:
            user_input = input("\n>>> 选择(1/2/3) 或输入问题: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 再见")
            break

        question = presets.get(user_input, user_input)
        ask(question)


if __name__ == "__main__":
    main()
