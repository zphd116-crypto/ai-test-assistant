# AI 接口测试小助手 v1.0 · 课堂脚手架

《AI 测试种子计划》第三讲 · Function Calling 实战项目。

---

## 这是什么？

一个"半成品"AI Agent 项目：

- ✅ **对话循环、LLM 调用、工具派发** —— 讲师已写好（`main.py`）
- ⭕ **4 个工具函数 + 4 个 Schema** —— **学员要在课上补全**（`tools.py` / `schemas.py`）

补全之后，你就能用**自然语言**驱动 AI 完成完整的接口测试任务：读用例 → 发请求 → 断言 → 存日志。

---

## 快速开始（课前自检用）

### 1. 克隆仓库

```bash
git clone <课前通知里的仓库地址> ai-test-assistant
cd ai-test-assistant
```

### 2. 装依赖

```bash
pip install -r requirements.txt
# 下载慢可加清华镜像：-i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 配 API Key

```bash
# Windows
Copy-Item .env.example .env
# macOS / Linux
cp .env.example .env
```

打开 `.env`，把 `LLM_API_KEY` 换成你自己的**智谱 GLM-4-Flash Key**（[申请入口](https://open.bigmodel.cn/)，永久免费）。

### 4. 跑起来（此时只有空壳，会报 NotImplementedError，属正常）

```bash
python main.py
```

看到类似：

```
============================================================
🤖 AI 接口测试小助手 v1.0
   模型  : glm-4-flash
   入口  : https://open.bigmodel.cn/api/paas/v4/
   工具数: 4
============================================================
>>> 请输入指令:
```

**出现这个提示符 = ✅ 环境就绪**，课堂上按讲师节奏补全 4 个工具即可。

---

## 项目结构

```
ai-test-assistant/
├── main.py              # ✅ 讲师写好：对话循环、工具派发（不要改）
├── tools.py             # ⭕ 学员要填：4 个工具函数（带 TODO 提示）
├── schemas.py           # ⭕ 学员要填：4 个 Schema（含 1 个样板）
├── test_data.yaml       # ✅ 讲师写好：5 条测试用例
├── requirements.txt     # 依赖清单
├── .env.example         # API Key 配置模板
├── .gitignore
└── README.md            # 本文件
```

---

## 课堂任务清单

### 步骤一：补全 `tools.py`（4 个函数）

按照每个函数的 docstring 和 `# TODO` 提示实现：

| # | 函数 | 做什么 |
|---|---|---|
| 1 | `read_test_case(case_id)` | 从 yaml 读一条用例 |
| 2 | `http_request(method, url, body)` | 发 HTTP 请求 |
| 3 | `assert_field(response, field_path, expected)` | 断言字段值 |
| 4 | `save_test_log(case_name, status, detail)` | 保存一条测试结果 |

### 步骤二：补全 `schemas.py`（3 个 Schema）

对照已写好的 `HTTP_REQUEST_SCHEMA`，补全另外 3 个。重点是 `description` —— 这是 LLM 选择工具最关键的依据。

### 步骤三：与 AI 对话，完成 5 句必做

启动 `python main.py`，依次输入：

1. `帮我执行 TC001`
2. `TC001 到 TC005 全部执行，告诉我哪些通过哪些失败`
3. `TC004 为什么失败了？`
4. `把所有失败的用例重新跑一遍`
5. `把今天的测试结果整理成一段日报，发我`

每句都要跑通并截图。

---

## 作业提交

课后在班级群提交：

- [ ] `tools.py` + `schemas.py`（补全后的代码）
- [ ] 5 条对话的运行截图（或文本日志）
- [ ] 生成的 `test_results.json`
- [ ] （作业二）把 URL 换成自己业务的接口后，再跑 3 条对话

---

## 常见问题

- **报 NotImplementedError** → 说明对应工具还没实现，按 TODO 提示补即可。
- **API 401 / 余额不足** → 换备选 Key（见 `.env.example` 注释里其他配置）。
- **LLM 不调用工具，只回答了文字** → 多半是 Schema 的 `description` 写得不够清楚；重读模块二的 5 条黄金法则。
- **中文乱码** → Windows PowerShell 先运行 `chcp 65001`。

---

## 课后扩展

想把这个小助手用到自己业务线？只需：

1. 把 `test_data.yaml` 换成你们业务的用例
2. 把 `url` 字段换成你们业务的接口
3. 代码一行都不用改

就这么简单。

---

*《AI 测试种子计划》第二讲 · 研发测试部 · AI 变革团队*
