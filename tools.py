"""
tools.py 鈥斺€?宸ュ叿鍑芥暟瀹炵幇
========================
馃幆 瀛﹀憳闇€瑕佽ˉ鍏ㄧ殑鏂囦欢锛? / 2锛?

鏈枃浠跺寘鍚?4 涓伐鍏峰嚱鏁帮紝瀵瑰簲妯″潡鍥涘疄鎴樼殑 4 涓牳蹇冭兘鍔涖€?
姣忎釜鍑芥暟閮藉凡鍐欏ソ"楠ㄦ灦浠ｇ爜"锛屽鍛樺彧闇€瑕佸～鍐?___ 鏍囪鐨勫叧閿綅缃€?

鈿狅笍 娉ㄦ剰浜嬮」锛?
1. 涓嶈鏀瑰嚱鏁板悕鍜屽弬鏁板悕 鈥斺€?main.py 鐨勮皟搴︿緷璧栬繖浜涘悕瀛?
2. 姣忎釜鍑芥暟閮藉繀椤昏繑鍥?dict锛堜細琚?json 搴忓垪鍖栧悗鍥炰紶缁?LLM锛?
3. 瀹炵幇瀹屾垚鍚庯紝璁板緱鍚屾琛ュ叏 schemas.py
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
# 宸ュ叿 1 / 4锛歳ead_test_case
# ==============================================================
# 鍔熻兘锛氭牴鎹敤渚?ID锛屼粠 yaml 鏂囦欢涓鍙栧搴旂殑娴嬭瘯鐢ㄤ緥
# 闅惧害锛氣瓙锛堟渶绠€鍗曪紝寤鸿绗竴涓啓锛?
# ==============================================================
def read_test_case(case_id: str) -> dict:
    """浠?test_data.yaml 璇诲彇涓€鏉℃祴璇曠敤渚嬨€?

    鍙傛暟:
        case_id: 鐢ㄤ緥 id锛屽 "TC001"

    杩斿洖:
        鎵惧埌鏃? {"id": "TC001", "name": "...", "method": "GET", ...}
        鎵句笉鍒版椂: {"error": "鐢ㄤ緥 TC001 涓嶅瓨鍦?}
    """
    # --- 楠ㄦ灦浠ｇ爜锛堝～鍐?___ 澶勶級 ---

    # 绗?1 姝ワ細鎵撳紑 yaml 鏂囦欢锛岃鍙栨墍鏈夌敤渚?
    with open(TEST_DATA_FILE, "r", encoding="utf-8") as f:
        cases = yaml.safe_load(f)

    # 绗?2 姝ワ細閬嶅巻鐢ㄤ緥鍒楄〃锛屾壘鍒?id 鍖归厤鐨勯偅涓€鏉?
    for case in cases:
        if case["id"] == ___:       # 鈫?濉叆锛氳鍖归厤鐨勫彉閲忓悕鏄粈涔堬紵
            return ___              # 鈫?濉叆锛氭壘鍒颁簡搴旇杩斿洖浠€涔堬紵

    # 绗?3 姝ワ細娌℃壘鍒帮紝杩斿洖閿欒淇℃伅
    return {"error": f"鐢ㄤ緥 {case_id} 涓嶅瓨鍦?}


# ==============================================================
# 宸ュ叿 2 / 4锛歨ttp_request
# ==============================================================
# 鍔熻兘锛氬悜琚祴鎺ュ彛鍙戣捣 HTTP 璇锋眰
# 闅惧害锛氣瓙猸愶紙闇€瑕佷簡瑙?requests 搴擄級
# ==============================================================
def http_request(method: str, url: str, body: dict | None = None) -> dict:
    """鍚戣娴嬫帴鍙ｅ彂璧?HTTP 璇锋眰銆?

    鍙傛暟:
        method: "GET" / "POST" / "PUT" / "DELETE"
        url: 瀹屾暣鎺ュ彛 URL
        body: 璇锋眰浣擄紙浠?POST/PUT 闇€瑕侊紝GET/DELETE 浼?None锛?

    杩斿洖:
        姝ｅ父:  {"status_code": 200, "response": {...}}
        寮傚父:  {"error": "..."}
    """
    # --- 楠ㄦ灦浠ｇ爜锛堝～鍐?___ 澶勶級 ---

    try:
        method = method.upper()

        if method == "GET":
            resp = requests.get(url, timeout=HTTP_TIMEOUT)
        elif method == "POST":
            resp = requests.post(url, json=___, timeout=HTTP_TIMEOUT)    # 鈫?濉叆锛歅OST 鐨勮姹備綋鍙橀噺
        elif method == "PUT":
            resp = requests.put(url, json=___, timeout=HTTP_TIMEOUT)     # 鈫?濉叆锛歅UT 鐨勮姹備綋鍙橀噺
        elif method == "DELETE":
            resp = requests.delete(url, timeout=HTTP_TIMEOUT)
        else:
            return {"error": f"涓嶆敮鎸佺殑鏂规硶: {method}"}

        # 灏濊瘯瑙ｆ瀽 JSON 鍝嶅簲
        try:
            data = resp.json()
        except ValueError:
            data = resp.text

        return {"status_code": resp.status_code, "response": ___}       # 鈫?濉叆锛氳繑鍥炵殑鏁版嵁鍙橀噺

    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


# ==============================================================
# 宸ュ叿 3 / 4锛歛ssert_field
# ==============================================================
# 鍔熻兘锛氭柇瑷€鍝嶅簲涓煇涓瓧娈垫槸鍚︾瓑浜庢湡鏈涘€?
# 闅惧害锛氣瓙猸愶紙闇€瑕佺悊瑙?dict 鍙栧€煎拰姣旇緝锛?
# ==============================================================
def assert_field(response: dict, field_path: str, expected: Any) -> dict:
    """鏂█鍝嶅簲鐨勬煇涓瓧娈电瓑浜庢湡鏈涘€笺€?

    鍙傛暟:
        response: 鎺ュ彛杩斿洖鐨?dict锛堥€氬父浼?http_request 杩斿洖鐨?response 閮ㄥ垎锛?
        field_path: 瀛楁璺緞锛屽 "userId"锛堟湰璇惧彧闇€鏀寔涓€绾у瓧娈靛嵆鍙級
        expected: 鏈熸湜鍊?

    杩斿洖:
        閫氳繃: {"status": "pass", "field": "userId", "actual": 1, "expected": 1}
        澶辫触: {"status": "fail", "field": "userId", "actual": 2, "expected": 1,
               "reason": "鏈熸湜 1锛屽疄闄?2"}
    """
    # --- 楠ㄦ灦浠ｇ爜锛堝～鍐?___ 澶勶級 ---

    # 绗?1 姝ワ細浠?response 涓彇鍑鸿鏂█鐨勫瓧娈靛€?
    actual = response.get(___)          # 鈫?濉叆锛氳浠?response 閲屽彇鍝釜 key锛?

    # 绗?2 姝ワ細姣旇緝瀹為檯鍊煎拰鏈熸湜鍊硷紙鐢?str 杞崲鍚庢瘮杈冿紝鍏煎绫诲瀷宸紓锛?
    if str(actual) == str(expected):
        return {
            "status": "pass",
            "field": field_path,
            "actual": actual,
            "expected": expected
        }
    else:
        return {
            "status": ___,              # 鈫?濉叆锛?pass" 杩樻槸 "fail"锛?
            "field": field_path,
            "actual": actual,
            "expected": expected,
            "reason": f"鏈熸湜 {expected}锛屽疄闄?{actual}"
        }


# ==============================================================
# 宸ュ叿 4 / 4锛歴ave_test_log
# ==============================================================
# 鍔熻兘锛氭妸娴嬭瘯缁撴灉淇濆瓨鍒版湰鍦?JSON 鏂囦欢
# 闅惧害锛氣瓙猸愶紙闇€瑕佷簡瑙?JSON 鏂囦欢璇诲啓锛?
# ==============================================================
def save_test_log(case_name: str, status: str, detail: str = "") -> dict:
    """鎶婁竴鏉℃祴璇曠粨鏋滆拷鍔犱繚瀛樺埌 test_results.json銆?

    鍙傛暟:
        case_name: 鐢ㄤ緥鍚?
        status: "pass" / "fail"
        detail: 璇︾粏淇℃伅锛堝彲閫夛級

    杩斿洖:
        {"saved": True, "file": "test_results.json", "total": 5}
    """
    # --- 楠ㄦ灦浠ｇ爜锛堝～鍐?___ 澶勶級 ---

    # 绗?1 姝ワ細璇诲彇宸叉湁璁板綍锛堟枃浠朵笉瀛樺湪灏变粠绌哄垪琛ㄥ紑濮嬶級
    if os.path.exists(TEST_RESULT_FILE):
        with open(TEST_RESULT_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    # 绗?2 姝ワ細鏋勯€犳柊鐨勪竴鏉℃祴璇曡褰?
    log_entry = {
        "case_name": ___,               # 鈫?濉叆锛氱敤渚嬪悕鍙橀噺
        "status": ___,                  # 鈫?濉叆锛氱姸鎬佸彉閲?
        "detail": detail,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    # 绗?3 姝ワ細杩藉姞鍒板垪琛?
    logs.append(log_entry)

    # 绗?4 姝ワ細鍐欏洖鏂囦欢
    with open(TEST_RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, ___, ensure_ascii=False, indent=2)   # 鈫?濉叆锛氬啓鍒板摢涓枃浠跺璞★紵

    return {"saved": True, "file": TEST_RESULT_FILE, "total": len(logs)}

