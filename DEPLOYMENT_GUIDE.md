# 项目上线指南 🚀

本指南将帮助您将HelloAgents智能旅行助手项目正式上线。

## 项目概述

这是一个前后端分离的智能旅行规划助手项目：

- **后端**：基于HelloAgents框架的FastAPI应用
- **前端**：Vue3 + TypeScript + Vite应用

## 1. 准备工作

### 1.1 环境要求

- **后端**：Python 3.10+
- **前端**：Node.js 16+
- **生产服务器**：Linux服务器（推荐Ubuntu 20.04+）
- **域名**：（可选）用于访问服务
- **SSL证书**：（可选）用于HTTPS访问

### 1.2 API密钥准备

您需要准备以下API密钥：

- **LLM API密钥**：OpenAI、DeepSeek或其他LLM提供商的密钥
- **高德地图API密钥**：
  - Web服务API密钥
  - Web端JS API密钥
- **Unsplash API密钥**：用于获取图片

## 2. 后端部署

### 2.1 安装依赖

1. 进入后端目录：
```bash
cd backend
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 2.2 配置环境变量

1. 复制.env.example文件为.env：
```bash
cp .env.example .env
```

2. 编辑.env文件，填入您的API密钥和配置：
```env
# LLM配置
LLM_MODEL_ID="deepseek-ai/DeepSeek-V3.2"
LLM_API_KEY="your_llm_api_key"
LLM_BASE_URL="https://api-inference.modelscope.cn/v1"

# 服务器配置
HOST=0.0.0.0
PORT=8000

# CORS配置（生产环境中替换为您的前端域名）
CORS_ORIGINS=https://your-frontend-domain.com,http://your-frontend-domain.com

# 日志级别
LOG_LEVEL=INFO

# Unsplash API Credentials
UNSPLASH_ACCESS_KEY="your_unsplash_access_key"
UNSPLASH_SECRET_KEY="your_unsplash_secret_key"

# 高德地图API配置
AMAP_API_KEY="your_amap_api_key"
```

### 2.3 运行后端服务

#### 方式1：使用Uvicorn直接运行（开发环境）

```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

#### 方式2：使用Gunicorn+Uvicorn（生产环境推荐）

1. 安装Gunicorn：
```bash
pip install gunicorn
```

2. 运行服务：
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.api.main:app --bind 0.0.0.0:8000
```

#### 方式3：使用进程管理器（生产环境推荐）

使用Supervisor管理进程：

1. 安装Supervisor：
```bash
sudo apt-get install supervisor
```

2. 创建Supervisor配置文件：
```bash
sudo nano /etc/supervisor/conf.d/trip-planner-backend.conf
```

3. 填入以下内容：
```ini
[program:trip-planner-backend]
command=/path/to/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.api.main:app --bind 0.0.0.0:8000
directory=/path/to/backend
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/trip-planner-backend.log
```

4. 更新Supervisor配置：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start trip-planner-backend
```

## 3. 前端部署

### 3.1 安装依赖

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

### 3.2 配置环境变量

1. 复制.env.example文件为.env：
```bash
cp .env.example .env
```

2. 编辑.env文件，填入您的配置：
```env
# 后端API地址（生产环境中替换为您的后端域名）
VITE_API_BASE_URL=https://your-backend-domain.com

# 高德地图Web API Key
VITE_AMAP_WEB_KEY=your_amap_web_api_key
# 高德地图Web端JS API Key
VITE_AMAP_WEB_JS_KEY=your_amap_web_js_key
```

### 3.3 构建生产版本

```bash
npm run build
```

构建完成后，生产文件将生成在`dist/`目录中。

### 3.4 部署静态文件

#### 方式1：使用Nginx部署（推荐）

1. 安装Nginx：
```bash
sudo apt-get install nginx
```

2. 创建Nginx配置文件：
```bash
sudo nano /etc/nginx/sites-available/trip-planner-frontend
```

3. 填入以下内容：
```nginx
server {
    listen 80;
    server_name your-frontend-domain.com;

    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 配置反向代理，将API请求转发到后端
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. 启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/trip-planner-frontend /etc/nginx/sites-enabled/
```

5. 测试Nginx配置：
```bash
sudo nginx -t
```

6. 重启Nginx：
```bash
sudo systemctl restart nginx
```

## 4. 容器化部署（可选）

### 4.1 后端Docker配置

创建`backend/Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 前端Docker配置

创建`frontend/Dockerfile`：

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

创建`frontend/nginx.conf`：

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.3 Docker Compose配置

在项目根目录创建`docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### 4.4 运行Docker Compose

```bash
docker-compose up -d
```

## 5. 生产环境优化

### 5.1 后端优化

1. **使用缓存**：对于频繁调用的API，可以考虑使用Redis缓存结果
2. **调整进程数**：根据服务器CPU核心数调整Gunicorn的worker数量
3. **启用Gzip压缩**：在FastAPI中启用Gzip压缩
4. **使用异步处理**：对于IO密集型操作，使用异步函数提高性能

### 5.2 前端优化

1. **启用CDN**：将静态资源部署到CDN上
2. **优化构建配置**：在vite.config.ts中添加构建优化配置
3. **懒加载**：对路由和组件进行懒加载
4. **图片优化**：使用适当尺寸的图片，考虑使用WebP格式

### 5.3 安全性

1. **使用HTTPS**：配置SSL证书，使用Let's Encrypt免费证书
2. **设置安全头**：在Nginx中配置安全相关的HTTP头
3. **限制API访问频率**：使用中间件限制API访问频率
4. **保护敏感配置**：不要将敏感配置硬编码到代码中

## 6. 监控和日志

### 6.1 后端日志

- 后端使用loguru记录日志，日志文件默认输出到控制台
- 生产环境中建议配置日志文件路径和滚动策略

### 6.2 服务器监控

- 使用Prometheus + Grafana监控服务器性能
- 使用ELK Stack或其他日志管理工具集中管理日志
- 配置告警规则，及时发现问题

## 7. 常见问题和解决方案

### 7.1 CORS错误

如果前端访问后端API时出现CORS错误，请检查后端.env文件中的CORS_ORIGINS配置，确保包含了前端的域名。

### 7.2 API调用失败

- 检查API密钥是否正确
- 检查网络连接是否正常
- 查看后端日志，了解具体错误信息

### 7.3 前端构建失败

- 检查依赖是否安装正确
- 检查环境变量是否配置正确
- 查看构建日志，了解具体错误信息

## 8. 维护建议

1. **定期更新依赖**：定期更新前后端依赖，修复安全漏洞
2. **备份数据**：如果项目后续添加了数据库，定期备份数据
3. **监控系统性能**：定期检查服务器性能，及时调整配置
4. **更新API密钥**：定期更新API密钥，提高安全性

## 9. 总结

本指南提供了将HelloAgents智能旅行助手项目上线的详细步骤，包括前后端部署、环境配置、容器化部署、性能优化和安全建议。根据您的实际需求和服务器环境，可以选择适合的部署方式。

祝您项目上线顺利！ 🎉