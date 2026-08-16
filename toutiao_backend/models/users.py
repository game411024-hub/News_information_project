from datetime import datetime
from typing import Optional
from sqlalchemy import Index, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Enum


#定义模型类
class Base(DeclarativeBase):
    created_at = mapped_column(DateTime, insert_default=func.now(), default=func.now(), comment="创建时间")

#创建用户表
class User(Base):
    """
    用户信息表ORM
    """
    __tablename__ = "user"
    #创建索引
    __table_args__ = (
        Index("username_UNIQUE","username"),
        Index("phone_UNIQUE", "phone"),
                      )
    id: Mapped[int] = mapped_column(Integer,nullable= False,primary_key=True,autoincrement=True,comment="用户ID")
    username: Mapped[str] = mapped_column(String(50),unique= True,nullable=False,comment="用户名")
    password: Mapped[str] = mapped_column(String(255),nullable=False,comment="密码（加密存储）")
    nickname: Mapped[Optional[str]] = mapped_column(String(50),comment="昵称")#昵称可以为空,Optional表示可以为空
    avatar: Mapped[Optional[str]] = mapped_column(String(255),default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",comment="头像")
    gender: Mapped[Optional[str]] = mapped_column(Enum("male", "female", "unknown"),default="unknown",comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(500),default="这个⼈很懒，什么都没留下",comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20),comment="手机号")
    updated_at: Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),onupdate=func.now(),default=func.now(),comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, nickname={self.nickname}, avatar={self.avatar}, gender={self.gender}, bio={self.bio}, phone={self.phone}, created_at={self.created_at}, updated_at={self.updated_at})>"

class Token(Base):
    """
    用户Token表ORM
    """
    __tablename__ = "user_token"
    id: Mapped[int] = mapped_column(Integer,nullable= False,primary_key=True,autoincrement=True,comment="用户ID")
    user_id: Mapped[int] = mapped_column(Integer,nullable=False,comment="用户ID")
    token: Mapped[str] = mapped_column(String(255),nullable=False,comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime,nullable=False,default=func.now(),comment="过期时间")