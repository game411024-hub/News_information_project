# 新闻资讯 App

一个前后端分离的新闻资讯项目，包含新闻浏览、分类查看、新闻详情、用户注册登录、个人资料、收藏、浏览历史以及 AI 问答功能。

前端基于 Vue 3、Vite、Vant、Pinia 构建移动端页面；后端基于 FastAPI、SQLAlchemy 异步 ORM、MySQL、Redis 提供接口服务，并通过 Ollama/OpenAI 兼容接口实现流式 AI 对话。

## 功能特性

- 新闻首页、分类新闻列表、新闻详情展示
- 新闻阅读量更新和相关推荐
- 用户注册、登录、Token 鉴权
- 用户资料查看与修改、密码修改
- 新闻收藏、取消收藏、收藏列表、清空收藏
- 浏览历史新增、列表查询、单条删除、清空历史
- AI 问答页面，支持 SSE 流式返回
- 中英文国际化、主题设置、本地状态持久化

## 技术栈

### 前端

- Vue 3
- Vite
- Vue Router
- Pinia
- Vant
- Axios
- vue-i18n
- marked、DOMPurify

### 后端

- Python
- FastAPI
- Uvicorn
- SQLAlchemy Async
- aiomysql
- Redis
- Passlib bcrypt
- OpenAI SDK
- Ollama 本地模型

### 数据库

- MySQL
- Redis

## 项目结构

```text
toutiao_news/
+-- news_app.sql              # MySQL 数据库初始化脚本
+-- toutiao_backend/          # FastAPI 后端
|   +-- main.py               # 后端入口
|   +-- cache/                # 新闻缓存逻辑
|   +-- config/               # 数据库、Redis、AI 配置
|   +-- crud/                 # 数据库操作
|   +-- models/               # SQLAlchemy ORM 模型
|   +-- routers/              # API 路由
|   +-- schemas/              # Pydantic 数据模型
|   +-- utils/                # 鉴权、响应、异常、AI 工具
+-- xwzx-news/                # Vue 前端
    +-- public/
    +-- src/
    |   +-- components/       # 公共组件
    |   +-- config/           # 前端 API 配置
    |   +-- i18n/             # 国际化
    |   +-- router/           # 路由配置
    |   +-- store/            # Pinia 状态管理
    |   +-- views/            # 页面组件
    +-- package.json
    +-- vite.config.js
```

## 环境要求

- Node.js 18+
- Python 3.10+
- MySQL 8+
- Redis 6+
- Ollama，可选，用于本地 AI 问答

## 后端启动

1. 进入后端目录：

```bash
cd toutiao_backend
```

2. 创建并激活 Python 虚拟环境：

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 创建 MySQL 数据库并导入数据：

```sql
CREATE DATABASE news_app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

然后导入项目根目录下的 `news_app.sql`。

5. 配置环境变量：

将根目录下的 `.env.example` 复制为 `.env`，并填写本机的 MySQL、Redis、DeepSeek、Ollama 配置。

```bash
cp .env.example .env
```

`.env` 已被 `.gitignore` 忽略，不会上传到 GitHub。

6. 配置 Python 模块搜索路径：

Windows PowerShell：

```powershell
$env:PYTHONPATH = "$PWD\.."
```

macOS / Linux：

```bash
export PYTHONPATH="$(pwd)/.."
```

7. 启动后端服务：

```bash
python main.py
```

默认服务地址：

```text
http://127.0.0.1:8000
```

FastAPI 接口文档：

```text
http://127.0.0.1:8000/docs
```

## 前端启动

1. 进入前端目录：

```bash
cd xwzx-news
```

2. 安装依赖：

```bash
npm install
```

3. 启动开发服务器：

```bash
npm run dev
```

前端默认会请求后端地址：

```text
http://127.0.0.1:8000
```

该地址配置在 `xwzx-news/src/config/api.js` 中。

## AI 问答配置

项目当前 AI 问答接口使用本地 Ollama 的 OpenAI 兼容接口：

```text
http://localhost:11434/v1
```

默认模型为：

```text
deepseek-r1:7b
```

如果需要使用本地模型，请先安装并启动 Ollama，然后拉取模型：

```bash
ollama pull deepseek-r1:7b
ollama serve
```

Ollama 地址和模型名通过 `.env` 配置：

```text
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=deepseek-r1:7b
```

DeepSeek 在线 API 也通过 `.env` 配置：

```text
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## 主要接口

### 新闻模块

- `GET /api/news/categories` 获取新闻分类
- `GET /api/news/list` 获取新闻列表
- `GET /api/news/detail` 获取新闻详情

### 用户模块

- `POST /api/user/register` 用户注册
- `POST /api/user/login` 用户登录
- `GET /api/user/info` 获取用户信息
- `PUT /api/user/update` 修改用户信息
- `PUT /api/user/password` 修改密码

### 收藏模块

- `GET /api/favorite/check` 检查是否收藏
- `POST /api/favorite/add` 添加收藏
- `DELETE /api/favorite/remove` 取消收藏
- `GET /api/favorite/list` 获取收藏列表
- `DELETE /api/favorite/clear` 清空收藏

### 浏览历史模块

- `POST /api/history/add` 添加浏览历史
- `GET /api/history/list` 获取浏览历史
- `DELETE /api/history/delete/{history_id}` 删除单条历史
- `DELETE /api/history/clear` 清空浏览历史

### AI 模块

- `POST /api/ai/chat` AI 流式问答

## 打包构建

前端生产构建：

```bash
cd xwzx-news
npm run build
```

本地预览构建结果：

```bash
npm run preview
```

## 许可证

本项目仅用于学习和课程实践。
