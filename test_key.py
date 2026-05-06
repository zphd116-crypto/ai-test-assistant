"""
test_key.py —— API Key 验证脚本
运行此脚本确认你的 .env 配置正确、模型可正常调用。

用法：
    python test_key.py
"""
import os
import sys

from dotenv import load_dotenv

load_dotenv(encoding="utf-8-sig")

API_KEY = (os.getenv("LLM_API_KEY") or "").lstrip("\ufeff").strip()
BASE_URL = (os.getenv("LLM_BASE_URL") or "https://open.bigmodel.cn/api/paas/v4/").strip()
MODEL = (os.getenv("LLM_MODEL") or "glm-4-flash").strip()

if not API_KEY or API_KEY.startswith("你的"):
    print("=" * 50)
    print("  ERROR: .env 中的 LLM_API_KEY 还没有填写")
    print("=" * 50)
    print()
    print("请按以下步骤操作：")
    print("  1. 用编辑器打开项目根目录下的 .env 文件")
    print("  2. 把 LLM_API_KEY= 后面的内容换成你的智谱 Key")
    print("  3. 保存后重新运行本脚本")
    print()
    print("还没有 Key？去 https://open.bigmodel.cn/ 免费注册")
    sys.exit(1)

print(f"正在验证 API Key...")
print(f"  模型  : {MODEL}")
print(f"  接口  : {BASE_URL}")
print(f"  Key   : {API_KEY[:8]}...{API_KEY[-4:]}")
print()

try:
    from openai import OpenAI

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "你好，请用一句话介绍 Function Calling"}],
    )
    content = resp.choices[0].message.content
    print("=" * 50)
    print("  OK! Key 验证通过")
    print("=" * 50)
    print()
    print(f"  模型回复: {content}")
    print()
    print("  你的环境已就绪，课堂上可以直接开干！")

except Exception as e:
    print("=" * 50)
    print("  FAILED! Key 验证失败")
    print("=" * 50)
    print()
    print(f"  错误信息: {e}")
    print()
    print("  请检查：")
    print(f"    1. Key 是否正确（当前: {API_KEY[:8]}...）")
    print(f"    2. 网络能否访问 {BASE_URL}")
    print(f"    3. 模型名 {MODEL} 是否正确")
    print()
    print("  仍有问题？班级群 @助教")
    sys.exit(1)
