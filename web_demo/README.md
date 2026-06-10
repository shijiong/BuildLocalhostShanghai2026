# GitHub Copilot SDK + FastAPI Demo

## 功能
- 文本问题输入
- 图片选择上传（可选）
- 模型来源选择：`gpt-5.4` 或 `ollama`
- 后端调用 Copilot SDK 分析文本/图像
- 前端流式展示回答
- 集成自定义工具 `lookup_knowledge`

## 覆盖的 SDK 特性（对应示例）
- 基础会话与消息发送：`1_FirstMessage.py`
- 流式响应事件：`2_StreamingResponses.py`
- 自定义工具：`3_CustomTool.py`
- 助手式持续对话思路：`4_weatherAssistant.py`
- 图像 blob 附件：`5_imageFile.py`
- Ollama provider 切换：`6_ollamademo.py`

## 运行
```bash
cd web_demo
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

浏览器访问：`http://127.0.0.1:8000`

## Ollama 配置
如果选择 `ollama`，后端会使用 OpenAI 兼容接口。
可通过环境变量修改：
- `OLLAMA_BASE_URL`，默认 `http://127.0.0.1:11434/v1`
- `OLLAMA_MODEL`，默认 `qwen3:8b`

Windows PowerShell 示例：
```powershell
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434/v1"
$env:OLLAMA_MODEL="qwen3:8b"
uvicorn main:app --reload --port 8000
```

## 目录
- `main.py`: FastAPI 路由与网页服务
- `copilot_service.py`: Copilot SDK 会话封装、工具和流式输出
- `templates/index.html`: 页面
- `static/app.js`: 前端请求与流式渲染
- `static/styles.css`: 样式
