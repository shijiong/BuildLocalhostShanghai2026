# BuildLocalhostShanghai2026

中文 | [English](#english)

## 中文

### 项目简介

`BuildLocalhostShanghai2026` 是一个面向 GitHub Copilot SDK 的示例项目仓库，展示了如何在 Python 环境中构建基于大模型的交互式应用。仓库目前包含两部分内容：一组独立运行的 Python SDK 示例脚本，以及一个基于 FastAPI 的 Web Demo，用于演示文本问答、图片输入、流式响应和本地模型接入等能力。

这个项目适合以下场景：
- 学习 GitHub Copilot SDK 的基础用法
- 了解会话创建、流式输出、工具调用、技能和自定义 Agent 的集成方式
- 快速搭建一个支持文本和图像分析的 Web 原型
- 体验通过 Ollama 接入本地模型的方式

### 项目结构

```text
BuildLocalhostShanghai2026/
├─ README.md
├─ python_demo/
│  ├─ 1_firstMessage.py
│  ├─ 2_streamingResponses.py
│  ├─ 3_customTool.py
│  ├─ 4_weatherAssistant.py
│  ├─ 5_imageFile.py
│  ├─ 6_ollamademo.py
│  ├─ 7_customAgentsDemo.py
│  ├─ 8_skillsDemo.py
│  └─ demo_skills/
└─ web_demo/
   ├─ main.py
   ├─ copilot_service.py
   ├─ requirements.txt
   ├─ templates/
   └─ static/
```

### Python 示例说明

`python_demo` 目录展示了多个由浅入深的 GitHub Copilot SDK 使用示例：

- `1_firstMessage.py`：最基础的会话创建与单轮消息发送
- `2_streamingResponses.py`：演示如何监听流式输出事件并逐步打印回答
- `3_customTool.py`：演示如何通过 `define_tool` 注册自定义工具
- `4_weatherAssistant.py`：构建一个可持续对话的命令行天气助手
- `5_imageFile.py`：演示如何上传图片附件并进行多模态分析
- `6_ollamademo.py`：演示如何通过 OpenAI 兼容接口接入 Ollama
- `7_customAgentsDemo.py`：演示如何配置和切换自定义 Agent
- `8_skillsDemo.py`：演示如何加载本地 Skills，并与自定义 Agent 组合使用

### Web Demo 说明

`web_demo` 是一个基于 FastAPI 的示例应用，主要特性包括：

- 支持用户输入文本问题
- 支持上传图片作为分析附件
- 支持流式返回模型回答
- 支持在 `gpt-5.4` 和 `ollama` 之间切换模型来源
- 后端集成了自定义工具 `lookup_knowledge`
- 前端提供基础网页交互界面，适合快速演示和二次开发

核心文件说明：

- `web_demo/main.py`：定义 FastAPI 路由、页面入口和流式接口
- `web_demo/copilot_service.py`：封装 Copilot SDK 会话、附件处理和流式事件
- `web_demo/templates/index.html`：页面模板
- `web_demo/static/app.js`：前端请求和流式渲染逻辑
- `web_demo/static/styles.css`：页面样式

### 环境准备

建议使用 Python 3.11+。

安装 Web Demo 依赖：

```bash
cd web_demo
pip install -r requirements.txt
```

如果你希望运行 Python 示例，也需要确保本地环境已安装项目所需的 `copilot-sdk` 及相关依赖。

### 运行方式

#### 运行 Web Demo

```bash
cd web_demo
uvicorn main:app --reload --port 8000
```

启动后，打开浏览器访问：

```text
http://127.0.0.1:8000
```

#### 运行 Python 示例

在仓库根目录或 `python_demo` 目录下执行对应脚本，例如：

```bash
python python_demo/1_firstMessage.py
python python_demo/2_streamingResponses.py
python python_demo/3_customTool.py
```

### Ollama 配置

如果你希望在 Web Demo 或示例脚本中使用本地模型，可通过环境变量配置 Ollama 的地址和模型名。

常用环境变量：

- `OLLAMA_BASE_URL`：Ollama 的 OpenAI 兼容接口地址
- `OLLAMA_MODEL`：使用的模型名称，默认示例为 `qwen3:8b`

Windows PowerShell 示例：

```powershell
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434/v1"
$env:OLLAMA_MODEL="qwen3:8b"
cd web_demo
uvicorn main:app --reload --port 8000
```

### 适合继续扩展的方向

你可以基于这个仓库继续扩展：

- 接入真实业务 API 或内部知识库
- 将自定义工具替换为真实的数据查询能力
- 增加更多 Skills 或自定义 Agents
- 为 Web Demo 增加会话历史、用户认证或多模型配置
- 将项目部署到容器或云环境中

---

## English

### Overview

`BuildLocalhostShanghai2026` is a GitHub Copilot SDK sample repository that demonstrates how to build interactive AI applications in Python. The repository currently contains two main parts: a set of standalone Python SDK demos and a FastAPI-based web application that showcases text chat, image input, streaming responses, and local model integration.

This project is useful if you want to:
- learn the basics of the GitHub Copilot SDK
- understand session creation, streaming, tool calling, skills, and custom agent integration
- build a quick web prototype for text and image analysis
- experiment with local models through Ollama

### Repository Structure

```text
BuildLocalhostShanghai2026/
├─ README.md
├─ python_demo/
│  ├─ 1_firstMessage.py
│  ├─ 2_streamingResponses.py
│  ├─ 3_customTool.py
│  ├─ 4_weatherAssistant.py
│  ├─ 5_imageFile.py
│  ├─ 6_ollamademo.py
│  ├─ 7_customAgentsDemo.py
│  ├─ 8_skillsDemo.py
│  └─ demo_skills/
└─ web_demo/
   ├─ main.py
   ├─ copilot_service.py
   ├─ requirements.txt
   ├─ templates/
   └─ static/
```

### Python Demo Guide

The `python_demo` folder contains progressively richer GitHub Copilot SDK examples:

- `1_firstMessage.py`: create a basic session and send a single prompt
- `2_streamingResponses.py`: listen to streaming events and print output incrementally
- `3_customTool.py`: register a custom tool with `define_tool`
- `4_weatherAssistant.py`: build a simple multi-turn command-line assistant
- `5_imageFile.py`: send an image attachment for multimodal analysis
- `6_ollamademo.py`: connect to Ollama through an OpenAI-compatible provider
- `7_customAgentsDemo.py`: configure and observe custom agents
- `8_skillsDemo.py`: load local skills and combine them with custom agents

### Web Demo Guide

The `web_demo` application is built with FastAPI and includes:

- text question input
- optional image upload for analysis
- streaming model responses
- model source switching between `gpt-5.4` and `ollama`
- a backend custom tool named `lookup_knowledge`
- a simple browser UI for demos and further extension

Key files:

- `web_demo/main.py`: FastAPI routes, page entry, and streaming API
- `web_demo/copilot_service.py`: Copilot SDK session setup, attachments, and streaming logic
- `web_demo/templates/index.html`: HTML template
- `web_demo/static/app.js`: frontend request and streaming rendering logic
- `web_demo/static/styles.css`: styles

### Requirements

Python 3.11+ is recommended.

Install dependencies for the web demo:

```bash
cd web_demo
pip install -r requirements.txt
```

If you want to run the Python demos, make sure your environment also has `copilot-sdk` and related dependencies available.

### How to Run

#### Run the Web Demo

```bash
cd web_demo
uvicorn main:app --reload --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

#### Run the Python Demos

From the repository root or from inside `python_demo`, run any example script, for example:

```bash
python python_demo/1_firstMessage.py
python python_demo/2_streamingResponses.py
python python_demo/3_customTool.py
```

### Ollama Configuration

To use local models in the web demo or sample scripts, configure the Ollama endpoint and model name through environment variables.

Common environment variables:

- `OLLAMA_BASE_URL`: OpenAI-compatible Ollama endpoint
- `OLLAMA_MODEL`: model name, with `qwen3:8b` used in the examples by default

Windows PowerShell example:

```powershell
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434/v1"
$env:OLLAMA_MODEL="qwen3:8b"
cd web_demo
uvicorn main:app --reload --port 8000
```

### Ideas for Extension

You can continue building on this repository by:

- connecting real business APIs or knowledge bases
- replacing the demo tool with production data access
- adding more skills or custom agents
- extending the web demo with chat history, authentication, or model configuration
- deploying the project in containers or cloud environments
