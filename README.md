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

打开终端（Windows 用 **PowerShell** 或 **CMD** / macOS 用 **Terminal**）。

先 cd 到你想放项目的位置（比如"文档"文件夹），然后 clone：

```bash
# 先进入你想存放项目的文件夹（按自己实际情况改路径）
cd C:\Users\你的用户名\Documents

# 克隆仓库（会自动在当前目录下创建 ai-test-assistant 文件夹）
git clone https://github.com/zphd116-crypto/ai-test-assistant.git

# 进入项目目录（⚠️ 后续所有命令都要在这个目录下执行）
cd ai-test-assistant
```

> ⚠️ **如果报 `'git' 不是内部或外部命令`**：
> - 说明你的电脑没有安装独立版 Git
> - 解决：去 [git-scm.com/download/win](https://git-scm.com/download/win) 下载安装（保持默认选项），**装完重开终端**再试
> - 装不了？用下面的 **zip 方式**代替

> 💡 **不想装 Git？直接下载 zip 也行**：
> 1. 点本页面上方绿色 **`Code`** 按钮 → **`Download ZIP`**
> 2. 解压到你想放的位置
> 3. 打开终端，cd 进去：`cd 解压后的文件夹路径\ai-test-assistant-main`
>
> （zip 解压出来的文件夹名多了个 `-main` 后缀，注意写对）

> 💡 公司网访问 GitHub 慢？联系助教获取 zip 包或 Gitee 镜像地址。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

> 下载慢可加清华镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### 3. 配置 API Key（重点步骤）

#### 第一步：复制配置文件

确保你在项目目录下（上一步 `cd ai-test-assistant` 后就是），运行：

```bash
# Windows CMD（命令提示符）
copy .env.example .env

# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

> 💡 **怎么区分 CMD 和 PowerShell？** 看窗口标题栏——写着"命令提示符"就是 CMD，写着"PowerShell"就是 PowerShell。不确定的话，两条都试一下，总有一条能成功。

#### 第二步：编辑 `.env` 文件，填入你的 Key

用**以下任一方式**打开 `.env` 文件：

```bash
# 方式 A：用记事本打开（Windows 最简单）
notepad .env

# 方式 B：用 Cursor 打开
cursor .env

# 方式 C：用 VSCode 打开
code .env

# 方式 D：直接在 Cursor / VSCode 侧边栏找到 .env 文件，双击打开
```

打开后你会看到：

```
LLM_API_KEY=你的智谱Key粘贴在这里
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
LLM_MODEL=glm-4-flash
```

**只需修改第一行**：把 `你的智谱Key粘贴在这里` 替换成你自己的智谱 Key（形如 `xxxxxxxx.yyyyyyyy`），保存关闭。

> 🔑 还没有 Key？去 [智谱开放平台](https://open.bigmodel.cn/) 注册，免费获取 GLM-4-Flash API Key（详见《课前准备_环境配置教程.md》第三节）。

> ⚠️ **Windows 用户请不要用 PowerShell 的 `echo` 或 `Set-Content` 写 .env 文件**，可能产生编码问题。用记事本/Cursor/VSCode 编辑最稳妥。

### 4. 验证 Key 可用

```bash
python test_key.py
```

看到模型返回一段文字 = ✅ **Key 配置正确**。

如果报错，请检查：
- `.env` 里的 Key 是否粘贴完整（不能有多余空格）
- 网络是否能访问 `open.bigmodel.cn`

### 5. 启动脚手架

```bash
python main.py
```

看到类似：

```
============================================================
🤖 AI 接口测试小助手 v1.0
   模型  : glm-4-flash
   入口  : https://open.bigmodel.cn/api/paas/v4/
   工具数: 1 / 4 （已补全 / 全部）

⚠️  以下 Schema 还没在 schemas.py 中补全，先跳过不发给 LLM：
     • read_test_case
     • assert_field
     • save_test_log
============================================================
>>> 请输入指令:
```

**出现 `>>> 请输入指令:` = ✅ 环境就绪**，课堂上按讲师节奏补全 4 个工具即可。

> 💡 此时工具数显示 `1 / 4` 是正常的 —— 讲师只写好了 1 个样板（`http_request`），另外 3 个由你在课上补全。

---

## 项目结构

```
ai-test-assistant/
├── main.py              # ✅ 讲师写好：对话循环、工具派发（不要改）
├── tools.py             # ⭕ 学员要填：4 个工具函数（带 TODO 提示）
├── schemas.py           # ⭕ 学员要填：4 个 Schema（含 1 个样板）
├── test_data.yaml       # ✅ 讲师写好：5 条测试用例
├── test_key.py          # ✅ API Key 验证脚本
├── requirements.txt     # 依赖清单
├── .env.example         # API Key 配置模板
├── demo/                # 讲师课堂演示代码（学员无需修改）
│   ├── demo1_weather.py
│   └── demo2_jsonplaceholder.py
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

| 问题 | 解决方案 |
|------|---------|
| **报 `NotImplementedError`** | 正常，说明对应工具还没实现，按 TODO 提示补即可 |
| **报 `ModuleNotFoundError: No module named 'xxx'`** | 重新运行 `pip install -r requirements.txt` |
| **API 401 / Key 无效** | 检查 `.env` 里 Key 是否完整，或换备选配置（见 `.env.example` 注释） |
| **LLM 不调用工具，只回答文字** | Schema 的 `description` 写得不够清楚，重读模块二的 5 条黄金法则 |
| **`.env` 配了 Key 但程序说没配** | 可能是 BOM 编码问题，用记事本/Cursor 重新编辑保存 `.env` |
| **PowerShell 卡住不动** | 可能进入"选择模式"，按 `Esc` 键恢复（详见课前教程 Q8） |
| **中文乱码** | PowerShell 先运行 `chcp 65001`，或使用 Cursor/VSCode 内置终端 |

---

## 课后扩展

想把这个小助手用到自己业务线？只需：

1. 把 `test_data.yaml` 换成你们业务的用例
2. 把 `url` 字段换成你们业务的接口
3. 代码一行都不用改

就这么简单。

---

*《AI 测试种子计划》第三讲 · 研发测试部 · AI 变革团队*
