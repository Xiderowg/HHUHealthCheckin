# HHUHealthCheckin

一个河海大学非官方云上自动健康打卡小程序，基于 vue 和 flask

## 内容列表

- [概述](#概述)
  - [背景](##背景)
  - [截图](##截图)
  - [技术组成](##技术组成)
- [安装](#安装)
  - [前端](##前端)
  - [后端](##后端)
    - [开发与测试环境设置](###开发与测试环境设置)
    - [CLI 安装与初始化](###CLI安装与初始化)
    - [运行](###运行)
      - [Celery](####Celery)
      - [Gunicorn](####Gunicorn)
      - [uWSGI](####uWSGI)
      - [flask](####flask)
- [调试](#调试)
  - [tox](##tox)
  - [pytest](##pytest)
  - [手动调试](##手动调试)
    - [后端路由表](###后端路由表)
    - [账号认证](###账号认证)
    - [用户信息](###用户信息)
    - [其他路由](###其他路由)
- [参考](#参考)

## 概述

### 背景

由于不想写 3000 字检讨，本 repo 应运而生:smile:

![jydsb](images/jydsb.png)

### 截图

![screenshot](images/screenshot.jpg)

### 技术组成

- 前端使用了 `vue.js` 和 `uniapp` 用于构建跨平台的小程序应用
- 后端使用了 `flask` 构建 RESTful API，使用 `celery+redis/rabbitMQ` 作为任务队列，支持 `Gunicorn` 和 `uWSGI` 托管 API，提供了简易的 `docker`和`docker-compose` 示例

## 安装

### 前端

uniapp 官方推荐使用 HBuilder X 进行开发和部署，这里以 HBuilder X 为例

使用 HBuilder X 打开 frontend_app 文件夹，按照下图指引即可生成 H5 或微信小程序代码：

![fron_end](images/front_end.png)

将 H5 代码上传部署至服务器或发布微信小程序不在本例的讨论范围，请自行查找相关方法

### 后端

#### 开发与测试环境设置

```bash
mkdir hhucheckin
cd hhucheckin
git clone https://github.com/Xiderowg/HHUHealthCheckin.git
cd backend_api
vi .flaskenv
...
vi .testenv
...
```

- .flaskenv 示例

```bash
FLASK_ENV=production
FLASK_APP=checkin_api.app:create_app
SECRET_KEY=修改这里的秘钥
DATABASE_URI=mysql://guest:guest@localhost/checkin
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND_URL=redis://localhost:6379/0
MAIL_SMTP_HOST=邮件服务器
MAIL_SMTP_PORT=邮件服务器端口
MAIL_SMTP_USER=邮件服务用户名
MAIL_SMTP_PASS=邮件服务密码
```

- .testenv 示例

```bash
FLASK_ENV=development
FLASK_APP=checkin_api.app:create_app
SECRET_KEY=testing
DATABASE_URI=mysql://guest:guest@localhost:1433/hhucheckin?driver=SQL Server
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
MAIL_SMTP_HOST=邮件服务器
MAIL_SMTP_PORT=邮件服务器端口
MAIL_SMTP_USER=邮件服务用户名
MAIL_SMTP_PASS=邮件服务密码
```

#### CLI 安装与初始化

```bash
pip install -r requirements.txt
pip install -e .
checkin_api db upgrade
checkin_api init
```

\*注：默认管理员用户名和密码均为`admin`

#### 运行

##### Celery

后台(自动)打卡任务依赖于 Celery Worker，需要确保 Celery Worker 正常运行才能保证每日按时打卡

```bash
celery worker -A checkin_api.celery_app:app --loglevel=info -B
```

##### 推荐 - Gunicorn

```bash
pip install gunicorn
gunicorn checkin_api.wsgi:app
```

\*注: gunicorn 默认运行在 8000 端口上，如果要配合 docker 使用请修改`Dockerfile`和`docekr-compose.yml`

##### 推荐 - uWSGI

```bash
pip install uwsgi
uwsgi --http 127.0.0.1:5000 --module checkin.wsgi:app
```

##### 不推荐 - flask 服务器

```bash
checkin_api run
```

## 调试

### tox 测试

最简单的调试方式是使用 tox 这一插件进行调试

- 安装 tox：

```bash
pip install tox
```

- 执行测试：

```bash
tox -e test
```

### pytest

- 安装 pytest:

```bash
pip install pytest pytest-runner pytest-flask pytest-factoryboy factory_boy
```

- 执行测试：

```bash
pytest
```

建议在 pycharm 中以`debug`模式进行 pytest，将会自动读取`.testenv`中的环境变量进行测试

### 手动调试

#### 后端路由表

```text
Endpoint                     Methods           Rule
---------------------------  ----------------  -------------------------
api.checkin_all              POST              /checkin/all
api.checkin_data             GET               /users/data
api.checkin_data_by_user_id  GET               /users/data/<int:user_id>
api.checkin_user             POST              /checkin
api.create_user              POST              /users/create
api.get_current_user         GET, PUT          /users
api.get_user_by_id           DELETE, GET, PUT  /users/<int:user_id>
api.list_users               GET               /users/all
auth.login                   POST              /auth/login
auth.refresh                 POST              /auth/refresh
auth.revoke_access_token     DELETE            /auth/revoke_access
auth.revoke_refresh_token    DELETE            /auth/revoke_refresh
auth.user_role               GET               /auth/role
```

#### 账号认证

账号认证路由为`/auth/login`，利用 curl 测试的例子如下：

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:5000/auth/login
```

用户名和密码正确的情况下，接口会返回如下数据：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDQ0MSwiZnJlc2giOmZhbHNlLCJqdGkiOiI2OTg0MjZiYi00ZjJjLTQ5MWItYjE5YS0zZTEzYjU3MzFhMTYiLCJuYmYiOjE1MTAwMDA0NDEsImV4cCI6MTUxMDAwMTM0MX0.P-USaEIs35CSVKyEow5UeXWzTQTrrPS_YjVsltqi7N4",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTEwMDAwNDQxLCJ0eXBlIjoicmVmcmVzaCIsImp0aSI6IjRmMjgxOTQxLTlmMWYtNGNiNi05YmI1LWI1ZjZhMjRjMmU0ZSIsIm5iZiI6MTUxMDAwMDQ0MSwiZXhwIjoxNTEyNTkyNDQxfQ.SJPsFPgWpZqZpHTc4L5lG_4aEKXVVpLLSW1LO7g4iU0"
}
```

#### 用户信息

利用上一步得到的`access_token`即可访问其他路由，示例如下：

```
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDQ0MSwiZnJlc2giOmZhbHNlLCJqdGkiOiI2OTg0MjZiYi00ZjJjLTQ5MWItYjE5YS0zZTEzYjU3MzFhMTYiLCJuYmYiOjE1MTAwMDA0NDEsImV4cCI6MTUxMDAwMTM0MX0.P-USaEIs35CSVKyEow5UeXWzTQTrrPS_YjVsltqi7N4" http://127.0.0.1:5000/users
```

#### 其他路由

其他路由测试方法类似，请参找源码构建测试用例

## 参考

- [HHUHealthCheckinGUI](https://github.com/Xiderowg/HHUHealthCheckinGUI)
- [uniapp](https://github.com/dcloudio/uni-ui)
- [cookiecutter-flask-restful](https://github.com/karec/cookiecutter-flask-restful)
