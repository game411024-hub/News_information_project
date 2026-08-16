from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from toutiao_backend.utils.Exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def exceptons_handler(app):
    """
    异常处理集合
    注册全局异常处理:子类在前，父类在后;具体在前，抽象在后
    """
    app.add_exception_handler(HTTPException,http_exception_handler)#业务层异常处理
    app.add_exception_handler(IntegrityError,integrity_error_handler)#数据库异常处理
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)#数据库异常处理
    app.add_exception_handler(Exception,general_exception_handler)#处理所有未捕获的未知异常（兜底处理器）