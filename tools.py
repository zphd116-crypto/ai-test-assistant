"""
tools.py —— 工具函数实现
========================
🎯 学员需要补全的文件（1 / 2）

本文件包含 4 个工具函数，对应模块四实战的 4 个核心能力。
每个函数都已写好"骨架代码"，学员只需要填写 ___ 标记的关键位置。

⚠️ 注意事项：
1. 不要改函数名和参数名 —— main.py 的调度依赖这些名字
2. 每个函数都必须返回 dict（会被 json 序列化后回传给 LLM）
3. 实现完成后，记得同步补全 schemas.py
"""
import json
import os
from datetime import datetime
from typing import Any

import requests
import yaml


TEST_DATA_FILE = "test_data.yaml"
TEST_RESULT_FILE = "test_results.json"
HTTP_TIMEOUT = 10


# ==============================================================
# 工具 1 / 4：read_test_case
# ==============================================================
# 功能：根据用例 ID，从 yaml 文件中读取对应的测试用例
# 难度：⭐（最简单，建议第一个写）
# ==============================================================
def read_test_case(case_id: str) -> dict:
    """从 test_data.yaml 读取一条测试用例。

    参数:
        case_id: 用例 id，如 "TC001"

    返回:
        找到时: {"id": "TC001", "name": "...", "method": "GET", ...}
        找不到时: {"error": "用例 TC001 不存在"}
    """
    # --- 骨架代码（填写 ___ 处） ---

    # 第 1 步：打开 yaml 文件，读取所有用例
    with open(TEST_DATA_FILE, "r", encoding="utf-8") as f:
        cases = yaml.safe_load(f)

    # 第 2 步：遍历用例列表，找到 id 匹配的那一条
    for case in cases:
        if case["id"] == case_id:       # ← 填入：要匹配的变量名是什么？
            return case       # ← 填入：找到了应该返回什么？

    # 第 3 步：没找到，返回错误信息
    return {"error": f"用例 {case_id} 不存在"}


# ==============================================================
# 工具 2 / 4：http_request
# ==============================================================
# 功能：向被测接口发起 HTTP 请求
# 难度：⭐⭐（需要了解 requests 库）
# ==============================================================
def http_request(method: str, url: str, body: dict | None = None) -> dict:
    """向被测接口发起 HTTP 请求。

    参数:
        method: "GET" / "POST" / "PUT" / "DELETE"
        url: 完整接口 URL
        body: 请求体（仅 POST/PUT 需要，GET/DELETE 传 None）

    返回:
        正常:  {"status_code": 200, "response": {...}}
        异常:  {"error": "..."}
    """
    # --- 骨架代码（填写 ___ 处） ---

    try:
        method = method.upper()

        if method == "GET":
            resp = requests.get(url, timeout=HTTP_TIMEOUT)
        elif method == "POST":
            resp = requests.post(url, json=body, timeout=HTTP_TIMEOUT)    # ← 填入：POST 的请求体变量
        elif method == "PUT":
            resp = requests.put(url, json=body, timeout=HTTP_TIMEOUT)     # ← 填入：PUT 的请求体变量
        elif method == "DELETE":
            resp = requests.delete(url, timeout=HTTP_TIMEOUT)
        else:
            return {"error": f"不支持的方法: {method}"}

        # 尝试解析 JSON 响应
        try:
            data = resp.json()
        except ValueError:
            data = resp.text

        return {"status_code": resp.status_code, "response": data}       # ← 填入：返回的数据变量

    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


# ==============================================================
# 工具 3 / 4：assert_field
# ==============================================================
# 功能：断言响应中某个字段是否等于期望值
# 难度：⭐⭐（需要理解 dict 取值和比较）
# ==============================================================
def assert_field(response: dict, field_path: str, expected: Any) -> dict:
    """断言响应的某个字段等于期望值。

    参数:
        response: 接口返回的 dict（通常传 http_request 返回的 response 部分）
        field_path: 字段路径，如 "userId"（本课只需支持一级字段即可）
        expected: 期望值

    返回:
        通过: {"status": "pass", "field": "userId", "actual": 1, "expected": 1}
        失败: {"status": "fail", "field": "userId", "actual": 2, "expected": 1,
               "reason": "期望 1，实际 2"}
    """
    # --- 骨架代码（填写 ___ 处） ---

    # 第 1 步：从 response 中取出要断言的字段值
    actual = response.get(field_path)          # ← 填入：要从 response 里取哪个 key？

    # 第 2 步：比较实际值和期望值（用 str 转换后比较，兼容类型差异）
    if str(actual) == str(expected):
        return {
            "status": "pass",
            "field": field_path,
            "actual": actual,
            "expected": expected
        }
    else:
        return {
            "status": "fail",              # ← 填入："pass" 还是 "fail"？
            "field": field_path,
            "actual": actual,
            "expected": expected,
            "reason": f"期望 {expected}，实际 {actual}"
        }


# ==============================================================
# 工具 4 / 4：save_test_log
# ==============================================================
# 功能：把测试结果保存到本地 JSON 文件
# 难度：⭐⭐（需要了解 JSON 文件读写）
# ==============================================================
def save_test_log(case_name: str, status: str, detail: str = "") -> dict:
    """把一条测试结果追加保存到 test_results.json。

    参数:
        case_name: 用例名
        status: "pass" / "fail"
        detail: 详细信息（可选）

    返回:
        {"saved": True, "file": "test_results.json", "total": 5}
    """
    # --- 骨架代码（填写 ___ 处） ---

    # 第 1 步：读取已有记录（文件不存在就从空列表开始）
    if os.path.exists(TEST_RESULT_FILE):
        with open(TEST_RESULT_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    # 第 2 步：构造新的一条测试记录
    log_entry = {
        "case_name": case_name,               # ← 填入：用例名变量
        "status": status,                  # ← 填入：状态变量
        "detail": detail,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    # 第 3 步：追加到列表
    logs.append(log_entry)

    # 第 4 步：写回文件
    with open(TEST_RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)   # json.dump(数据, 文件对象, 其他参数)

    return {"saved": True, "file": TEST_RESULT_FILE, "total": len(logs)}
