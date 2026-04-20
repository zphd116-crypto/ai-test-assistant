"""
tools.py —— 工具函数实现
========================
🎯 学员需要补全的文件（1 / 2）

本文件包含 4 个工具函数，对应模块四实战的 4 个核心能力。
学员需要按照每个函数的"函数签名 + 文档字符串 + TODO 提示"逐一实现。

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
def read_test_case(case_id: str) -> dict:
    """从 test_data.yaml 读取一条测试用例。

    参数:
        case_id: 用例 id，如 "TC001"

    返回:
        找到时:
            {"id": "TC001", "name": "...", "method": "GET",
             "url": "...", "assert_field": "...", "expected": ...}
        找不到时:
            {"error": "用例 TC001 不存在"}
    """
    # TODO（学员实现）：
    #   1) 打开 TEST_DATA_FILE，用 yaml.safe_load 读取得到 list
    #   2) 遍历，找到 item["id"] == case_id 的那一条
    #   3) 找到则返回该 dict；找不到返回 {"error": f"用例 {case_id} 不存在"}
    raise NotImplementedError("请在 tools.py 中实现 read_test_case")


# ==============================================================
# 工具 2 / 4：http_request
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
    # TODO（学员实现）：
    #   1) 根据 method 大小写，调用 requests.get / post / put / delete
    #      注意统一加 timeout=HTTP_TIMEOUT
    #   2) POST/PUT 使用 json=body 传入请求体
    #   3) 返回 {"status_code": resp.status_code, "response": resp.json()}
    #      如果响应不是 JSON，response 里放 resp.text
    #   4) 捕获异常，返回 {"error": f"{type(e).__name__}: {e}"}
    raise NotImplementedError("请在 tools.py 中实现 http_request")


# ==============================================================
# 工具 3 / 4：assert_field
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
               "reason": "..."}
    """
    # TODO（学员实现）：
    #   1) 从 response 中取 field_path 的值：actual = response.get(field_path)
    #   2) 比较 actual 与 expected
    #   3) 通过:    返回 {"status": "pass", "field": ..., "actual": ..., "expected": ...}
    #      不通过:  返回 {"status": "fail", "field": ..., "actual": ..., "expected": ...,
    #                    "reason": f"期望 {expected}，实际 {actual}"}
    raise NotImplementedError("请在 tools.py 中实现 assert_field")


# ==============================================================
# 工具 4 / 4：save_test_log
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
    # TODO（学员实现）：
    #   1) 若 TEST_RESULT_FILE 存在，读取已有 list；否则初始化 []
    #   2) append 一条新记录 {
    #        "case_name": case_name,
    #        "status": status,
    #        "detail": detail,
    #        "timestamp": datetime.now().isoformat(timespec="seconds")
    #      }
    #   3) 写回文件，使用 json.dump(..., ensure_ascii=False, indent=2)
    #   4) 返回 {"saved": True, "file": TEST_RESULT_FILE, "total": len(logs)}
    raise NotImplementedError("请在 tools.py 中实现 save_test_log")
