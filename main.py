"""
AI 接口测试小助手 v1.0 —— 主程序（脚手架）
================================================
《AI 测试种子计划》第三讲 · Function Calling 实战

职责：
- 加载 .env 中的 LLM 配置
- 维护多轮对话循环
- 把学员写的 Tool Schemas 发给 LLM
- 解析 LLM 返回的 tool_calls，派发到 tools.py 的函数
- 把函数结果回传 LLM，拿到自然语言回复

⚠️ 学员无需修改本文件，只需补全 tools.py 和 schemas.py。
"""
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

import tools
from schemas import TOOL_SCHEMAS


load_dotenv(encoding="utf-8-sig")


def _clean(v):
    """剥掉 BOM + 去首尾空白，兼容 PowerShell Set-Content 写出来的 .env。"""
    return v.lstrip("\ufeff").strip() if v else v


API_KEY = _clean(os.getenv("LLM_API_KEY"))
BASE_URL = _clean(os.getenv("LLM_BASE_URL")) or "https://open.bigmodel.cn/api/paas/v4/"
MODEL = _clean(os.getenv("LLM_MODEL")) or "glm-4-flash"

if not API_KEY or API_KEY.startswith("你的"):
    print("❌ 请先在 .env 中填入 LLM_API_KEY（智谱 GLM-4-Flash 免费 Key）")
    print("   参考 .env.example 创建 .env 文件")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


EXPECTED_TOOLS = ["http_request", "read_test_case", "assert_field", "save_test_log"]


def _validate_schemas():
    """过滤掉未补全的 Schema，返回合法列表 + 缺失名单。学员可边写边测。"""
    valid, missing = [], []
    for name, schema in zip(EXPECTED_TOOLS, TOOL_SCHEMAS):
        if (
            isinstance(schema, dict)
            and schema.get("type") == "function"
            and isinstance(schema.get("function"), dict)
            and schema["function"].get("name")
        ):
            valid.append(schema)
        else:
            missing.append(name)
    return valid, missing


VALID_SCHEMAS, MISSING_SCHEMAS = _validate_schemas()


TOOL_REGISTRY = {
    "read_test_case": tools.read_test_case,
    "http_request": tools.http_request,
    "assert_field": tools.assert_field,
    "save_test_log": tools.save_test_log,
}


SYSTEM_PROMPT = """你是一个接口测试工程师助理，擅长用工具完成测试任务。

你有 4 个可用工具：
- read_test_case: 从本地 yaml 读取测试用例详情
- http_request: 发起 HTTP 请求（GET/POST/PUT/DELETE）
- assert_field: 断言响应中的字段等于期望值
- save_test_log: 把测试结果保存到本地 json 文件

工作原则：
1. 面对"执行用例"类请求，标准流程是：读用例 → 发请求 → 断言 → 存日志
2. 面对"批量执行"请求，逐条完成后再汇总结论
3. 面对"为什么失败"类请求，优先基于上下文分析，不要重复执行
4. 用简洁清晰的中文回复，必要时用表格呈现测试结果
"""


def run_tool(name: str, raw_args: str) -> str:
    """执行学员写的工具函数，结果序列化为字符串返回给 LLM。"""
    if name not in TOOL_REGISTRY:
        return json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False)
    try:
        args = json.loads(raw_args or "{}")
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"参数 JSON 解析失败: {e}"}, ensure_ascii=False)
    try:
        result = TOOL_REGISTRY[name](**args)
        return json.dumps(result, ensure_ascii=False, default=str)
    except NotImplementedError as e:
        return json.dumps(
            {"error": f"工具 {name} 尚未实现，请在 tools.py 中补全：{e}"},
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps({"error": f"{type(e).__name__}: {e}"}, ensure_ascii=False)


def chat_turn(messages: list) -> str:
    """单轮对话：循环处理 tool_calls，直到 LLM 给出最终自然语言回复。"""
    max_rounds = 10
    for _ in range(max_rounds):
        kwargs = {"model": MODEL, "messages": messages}
        if VALID_SCHEMAS:
            kwargs["tools"] = VALID_SCHEMAS
        resp = client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message
        messages.append(
            {
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [tc.model_dump() for tc in (msg.tool_calls or [])] or None,
            }
        )

        if not msg.tool_calls:
            return msg.content or "(模型未返回文本内容)"

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = tc.function.arguments or "{}"
            print(f"  🔧 调用工具: {fn_name}({fn_args})")
            result = run_tool(fn_name, fn_args)
            preview = result[:200] + ("..." if len(result) > 200 else "")
            print(f"  📥 工具返回: {preview}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                }
            )

    return "⚠️ 达到最大工具调用轮数，任务未完成。"


def print_banner() -> None:
    print("=" * 60)
    print("🤖 AI 接口测试小助手 v1.0")
    print(f"   模型  : {MODEL}")
    print(f"   入口  : {BASE_URL}")
    print(f"   工具数: {len(VALID_SCHEMAS)} / {len(EXPECTED_TOOLS)} （已补全 / 全部）")
    if MISSING_SCHEMAS:
        print()
        print("⚠️  以下 Schema 还没在 schemas.py 中补全，先跳过不发给 LLM：")
        for name in MISSING_SCHEMAS:
            print(f"     • {name}")
        print("    补全后重启程序即可自动接入。")
    print("=" * 60)
    print("💡 试试下面这 5 句必做对话（依次输入）：")
    print("   1. 帮我执行 TC001")
    print("   2. TC001 到 TC005 全部执行，告诉我哪些通过哪些失败")
    print("   3. TC004 为什么失败了？")
    print("   4. 把所有失败的用例重新跑一遍")
    print("   5. 把今天的测试结果整理成一段日报，发我")
    print()
    print("输入 'quit' / 'exit' / Ctrl+C 退出")
    print("=" * 60)


def main() -> None:
    print_banner()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        try:
            user_input = input("\n>>> 请输入指令: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见")
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 再见")
            break

        messages.append({"role": "user", "content": user_input})
        try:
            reply = chat_turn(messages)
        except Exception as e:
            print(f"❌ 对话出错: {type(e).__name__}: {e}")
            continue
        print(f"\n🤖 助手:\n{reply}")


if __name__ == "__main__":
    main()
