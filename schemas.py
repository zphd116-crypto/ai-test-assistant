"""
schemas.py —— Function Schema 定义
==================================
🎯 学员需要补全的文件（2 / 2）

这是本课最核心的练习 —— Schema 写得好不好，直接决定 Agent 智不智能。

✅ 讲师已写好 1 个样板（http_request），学员照葫芦画瓢补全另外 3 个。

黄金法则（模块二课上讲过）：
  1. description 用业务语言写清楚（这是 LLM 选工具最重要的依据）
  2. 参数命名要直观（order_id 优于 id）
  3. 善用 enum 限制取值
  4. 必填项 vs 可选项要严格区分
  5. 错误返回要结构化
"""


# ==============================================================
# ⭐ 讲师样板：http_request 的 Schema
#    这道题已经写好，供其他 3 个参考
# ==============================================================
HTTP_REQUEST_SCHEMA = {
    "type": "function",
    "function": {
        "name": "http_request",
        "description": (
            "向被测 HTTP 接口发起请求，用于执行接口测试。"
            "支持 GET/POST/PUT/DELETE 四种方法。"
            "GET/DELETE 不需要 body，POST/PUT 需要传 body。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE"],
                    "description": "HTTP 方法",
                },
                "url": {
                    "type": "string",
                    "description": "完整的接口 URL（包含协议、域名、路径）",
                },
                "body": {
                    "type": "object",
                    "description": "请求体，仅 POST/PUT 需要；GET/DELETE 可不传",
                },
            },
            "required": ["method", "url"],
        },
    },
}


# ==============================================================
# TODO 1 / 3：补全 read_test_case 的 Schema
# ------------------------------------------------------------
# 该工具用于从本地 yaml 文件读取一条预置的测试用例。
# 参数：case_id (string, 必填)
# ==============================================================
READ_TEST_CASE_SCHEMA = {
    # 请在此补全，参考 HTTP_REQUEST_SCHEMA 的结构
    # 提示：description 要写清楚"做什么"、"参数长啥样"、"返回什么"
}


# ==============================================================
# TODO 2 / 3：补全 assert_field 的 Schema
# ------------------------------------------------------------
# 该工具用于断言接口响应中的某个字段等于期望值。
# 参数：
#   - response     (object,     必填)  接口响应 dict
#   - field_path   (string,     必填)  字段名，如 "userId"
#   - expected     (任意类型,    必填)  期望值；可以是 string / number / boolean
#                   可以写 {"type": ["string", "number", "boolean"]}
# ==============================================================
ASSERT_FIELD_SCHEMA = {
    # 请在此补全
}


# ==============================================================
# TODO 3 / 3：补全 save_test_log 的 Schema
# ------------------------------------------------------------
# 该工具用于把一条测试结果保存到本地 json 日志文件。
# 参数：
#   - case_name    (string, 必填)  用例名
#   - status       (string, 必填)  "pass" 或 "fail"（建议用 enum 限制）
#   - detail       (string, 可选)  详细信息
# ==============================================================
SAVE_TEST_LOG_SCHEMA = {
    # 请在此补全
}


# ==============================================================
# 汇总给 main.py 使用 —— 不要改这个变量名
# ==============================================================
TOOL_SCHEMAS = [
    HTTP_REQUEST_SCHEMA,
    READ_TEST_CASE_SCHEMA,
    ASSERT_FIELD_SCHEMA,
    SAVE_TEST_LOG_SCHEMA,
]
