# ============================================================
# 异常处理器（utils/exceptions.py）
# ============================================================
# 作用：统一处理各类异常，返回规范化的 JSON 响应
# 配置：DEBUG_MODE = True 时返回详细错误信息，便于调试
# ============================================================

# ============================================================
# 【这个文件是干嘛的？—— 新手必读】
# ============================================================
# 程序运行时难免会遇到"出意外"的情况，比如：
#   1. 用户注册时，用户名已经被别人注册了（业务冲突）
#   2. 往数据库插入重复数据，违反唯一约束（数据库错误）
#   3. 数据库连接突然断了（连接错误）
#   4. 代码里某个没预料到的 bug（未知异常）
#
# 这些"意外"在 Python 里就叫【异常】（Exception）。
# 如果不处理，程序会直接崩溃，前端只会收到一屏看不懂的英文报错。
#
# 这个文件做的事情：给这些"意外"安排专门的【救援队】（异常处理器），
# 把错误"翻译"成统一格式的 JSON 返回给前端：
#       {"code": 400, "message": "用户名已存在", "data": ...}
# 这样前端就能友好地提示用户。
#
# 文件里一共定义了 4 支"救援队"（异常处理器）：
#   1. http_exception_handler    → 处理业务逻辑主动抛出的 HTTPException
#   2. integrity_error_handler   → 处理数据库"完整性约束"错误（如唯一约束）
#   3. sqlalchemy_error_handler  → 处理 SQLAlchemy 数据库层面的错误
#   4. general_exception_handler → 兜底：处理所有没被上面接住的异常
#
# 注意：定义了"救援队"还不够，最后还要【注册】（在 main.py 里用
# app.add_exception_handler() 告诉 FastAPI"哪种意外派哪支队伍"）。
# 注册方式见本文件最后一段注释。
# ============================================================

import traceback
# 标准库模块：生成"错误堆栈信息"（精确到出错的文件和行号），调试时定位 bug 全靠它

from fastapi import HTTPException, Request
# HTTPException：FastAPI 内置的"业务异常"类。
#               路由里写 raise HTTPException(status_code=404, detail="xxx") 就会抛出它
# Request：代表一次 HTTP 请求，处理器需要它才能知道"出错的是哪个网址"
from fastapi.responses import JSONResponse
# FastAPI 的 JSON 响应对象：把错误信息包装成 JSON 格式返回给前端
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# IntegrityError：数据库"完整性约束"被违反时抛出的错误
#                （如用户名重复、外键指向不存在的记录）
# SQLAlchemyError：所有 SQLAlchemy 数据库错误的"总爸爸"（基类），
#                  连接失败、SQL 写错等都算它
from starlette import status
# 提供 HTTP 状态码常量，如 status.HTTP_400_BAD_REQUEST 就是数字 400

# 开发模式开关（DEBUG_MODE）：
#   True  → 把详细错误信息（错误类型、完整堆栈）放进 data 返回，方便你调试
#   False → 只返回"给用户看的简单提示"，不暴露内部细节（生产环境防止泄露敏感信息）
# 教学项目保持开启，方便排查问题
DEBUG_MODE = True


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    处理 HTTPException 异常（业务逻辑主动抛出的异常）

    触发场景：这是"预期内的意外"——你在路由里主动 raise 的异常。
    例如注册接口里：raise HTTPException(status_code=404, detail="该用户已注册！")
    处理逻辑：把抛出时设置的状态码和提示信息，原样包装成 JSON 返回。
    """
    return JSONResponse(
        status_code=exc.status_code,   # 取出抛出时设置的状态码（如 404）
        content={
            "code": exc.status_code,   # 业务码：跟 HTTP 状态码保持一致
            "message": exc.detail,     # 取出抛出时的提示信息（"该用户已注册！"）
            "data": None               # 错误响应没有数据
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    处理数据库完整性约束错误（唯一约束、外键约束等）

    触发场景：数据库"拒绝执行"某条 SQL。常见两种：
      1. 插入的用户名已存在 → 违反唯一约束（UNIQUE）
      2. 插入的外键指向不存在的记录 → 违反外键约束（FOREIGN KEY）
    """
    # exc.orig 是底层数据库驱动（如 pymysql）抛出的"原始英文错误信息"
    error_msg = str(exc.orig)

    # 通过关键词判断是哪种约束被违反了，给出对应的中文提示
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        # ① 唯一约束：用户名重复了 → 提示用户换一个
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        # ② 外键约束：关联的数据不存在
        detail = "关联数据不存在"
    else:
        # ③ 其他没预料到的约束冲突，给出通用提示
        detail = "数据约束冲突，请检查输入"

    # 开发模式下，额外附带详细调试信息（错误类型、原始信息、出错网址）
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",   # 错误类型
            "error_detail": error_msg,        # 数据库原始错误信息
            "path": str(request.url)          # 出错请求的网址
        }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,  # 400 = 客户端请求有问题（通常是用户输入导致的）
        content={
            "code": 400,
            "message": detail,      # 给用户看的友好中文提示
            "data": error_data      # 调试信息（生产模式下为 None）
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    处理 SQLAlchemy 数据库错误（连接失败、语法错误等）

    触发场景：数据库层面出了意外——连不上数据库、SQL 写错、查询超时等。
    注意：IntegrityError 也属于 SQLAlchemyError 的子类，
    但 FastAPI 会优先派给更专门的 integrity_error_handler（谁更具体，谁先上）。
    """
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,     # 具体错误类名（如 OperationalError）
            "error_detail": str(exc),             # 错误描述
            "traceback": traceback.format_exc(),  # 完整堆栈：精确定位出错文件与行号
            "path": str(request.url)              # 出错请求的网址
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 = 服务器内部错误
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后重试",  # 不向用户暴露内部细节，统一友好提示
            "data": error_data
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    处理所有未捕获的未知异常（兜底处理器）

    这是"最后一道防线"：前面 3 支救援队都接不住的异常
    （比如代码里一个低级 bug），都会掉到这里。
    作用：保证程序不崩溃，前端能收到统一的 JSON 错误提示，而不是一屏乱码。
    """
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,     # 异常类名，一眼看出是什么错
            "error_detail": str(exc),             # 异常描述
            "traceback": traceback.format_exc(),  # 完整堆栈：定位 bug 全靠它
            "path": str(request.url)              # 出错请求的网址
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 = 服务器内部错误
        content={
            "code": 500,
            "message": "服务器内部错误",            # 对外保持简洁，不暴露内部细节
            "data": error_data
        }
    )


# ============================================================
# 注册异常处理器（在 main.py 中调用）
# ============================================================
# 上面只定义了 4 支"救援队"，但 FastAPI 还不知道"哪种意外派谁"。
# 必须在 main.py 里【注册】，告诉 FastAPI 的映射关系：
#
#   app.add_exception_handler(HTTPException,     http_exception_handler)
#   app.add_exception_handler(IntegrityError,    integrity_error_handler)
#   app.add_exception_handler(SQLAlchemyError,   sqlalchemy_error_handler)
#   app.add_exception_handler(Exception,         general_exception_handler)
#
# 映射规则解读：
#   第一行：遇到 HTTPException 类型异常 → 派 http_exception_handler
#   第二行：遇到 IntegrityError 类型异常 → 派 integrity_error_handler
#   第三行：遇到 SQLAlchemyError 类型异常 → 派 sqlalchemy_error_handler
#   第四行：遇到 Exception（所有异常）→ 派 general_exception_handler（兜底）
#
# 调用规则像"医院分诊"：挂了"骨科"（具体科室），又挂了"全科"（兜底）。
# FastAPI 会先找最匹配的异常类型，找不到才轮到最后一行的兜底处理器。
# 去掉这 4 行注释、把代码粘贴到 main.py 中，异常处理器就生效了。
# ============================================================