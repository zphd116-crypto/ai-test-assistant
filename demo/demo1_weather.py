"""
模块三 · Demo 1：Hello Function Calling
=========================================
目标：让学员亲眼看到 LLM 返回的原始 tool_calls 结构。

讲解节奏（约 10 分钟）：
  1. 运行一次，展示"正常调用"
  2. 打印 resp 的原始 JSON，指出 tool_calls 字段
  3. 故意问"今天天气怎么样"（不带城市），观察 LLM 反问
  4. 问"上海和北京哪个热"，观察并行调用（一次返回多个 tool_call）

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
    """模拟一个天气 API（不真发请求，课堂演示用）"""
    fake = {
        "上海": {"temp": 22, "weather": "多云"},
        "北京": {"temp": 28, "weather": "晴"},
    }
    return fake.get(city, {"temp": 20, "weather": "未知"})


def ask(question: str) -> None:
    print("=" * 60)
    print(f"👤 用户: {question}")
    print("=" * 60)

    messages = [{"role": "user", "content": question}]

    # 第一次调用：让 LLM 选工具
    resp = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS
    )
    msg = resp.choices[0].message

    print("\n📦 LLM 首轮返回（关键观察对象）：")
    print(json.dumps(msg.model_dump(exclude_unset=True), ensure_ascii=False, indent=2))

    if not msg.tool_calls:
        print(f"\n🤖 LLM 直接回复（未调用工具）: {msg.content}")
        return

    # 有 tool_calls，依次执行
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

    # 第二次调用：让 LLM 把结果组织成人话
    resp2 = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    print(f"\n🤖 LLM 最终回复: {resp2.choices[0].message.content}")


if __name__ == "__main__":
    # 👇 依次解除注释即可看到 3 个"啊哈时刻"

    # 啊哈 1：正常调用，看到原始 tool_calls JSON
    ask("上海今天天气怎么样？")

    # 啊哈 2：缺参数，LLM 会主动反问，不会瞎编
    # ask("今天天气怎么样？")

    # 啊哈 3：并行调用，一次返回多个 tool_call
    # ask("上海和北京哪个更热？")
