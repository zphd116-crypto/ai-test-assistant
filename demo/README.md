# 模块三现场 Demo 代码

这两份代码是讲师在**模块三（现场 Demo · 25 分钟）**中现场演示用的。

## Demo 1：`demo1_weather.py`（约 10 分钟）

**目标**：让学员第一次亲眼看到 LLM 返回的 `tool_calls` 结构。

**演示步骤**：

1. 先讲"我们定义了 1 个工具 `get_weather`，参数是 `city`"
2. 运行 `python demo/demo1_weather.py`，屏幕上会打印 **LLM 的原始 JSON 返回**
   - 重点让学员看 `tool_calls[0].function.name` 和 `arguments`
3. 注释掉"啊哈 1"的 `ask(...)`，打开"啊哈 2"，重跑
   - 故意不带城市，LLM 会主动反问，**不会瞎编参数**
4. 切到"啊哈 3"：问"上海和北京哪个热"
   - 观察 **并行调用**（一次返回 2 个 tool_call）

## Demo 2：`demo2_jsonplaceholder.py`（约 10 分钟）

**目标**：让 AI **真正发起** HTTP 请求，看到"动手做事"。

**演示步骤**：

1. 运行 `python demo/demo2_jsonplaceholder.py`
2. 依次输入启动提示里的 3 句对话，让学员看到：
   - AI 真的发起了真实 HTTP 请求
   - 多轮对话下 AI 会记住上下文
   - AI 会基于真实数据做判断（如 "是不是等于 1"）

## 与模块四的衔接

Demo 2 用的是同一个 JSONPlaceholder API，**和模块四的实战脚手架使用的是同一个被测系统**，无缝过渡。

## 所需环境

和主项目一样：`pip install -r ../requirements.txt` + 配好 `.env`。
