from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


#注册接口校验
class UserRequest(BaseModel):
    username: str
    password: str

# 【步骤 1】定义通用响应数据类型（新建 schemas/response.py）
# ------------------------------------------------------------
# 1. 继承 Pydantic 的 BaseModel
# 2. 定义三个字段：code、message、data
#    - code 设为 int 类型，默认值 200
#    - message 设为 str 类型，默认值 "success"
#    - data 设为 Optional[Any]，默认值 None
# 3. 内部配置 model_config 开启 from_attributes = True
#    （作用：支持传入 SQLAlchemy ORM 对象时自动序列化）
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname:Optional[str] = Field(None,max_length=50,description="昵称")#昵称可以为空
    avatar:Optional[str] = Field(None,max_length=255,description="头像URL")#头像URL可以为空
    gender:Optional[str] = Field(None,max_length=10,description="性别")#性别可以为空
    bio:Optional[str] = Field(None,max_length=500,description="个人简介")#个人简介可以为空

# 用户信息响应数据模型
class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes=True,  # 支持传入 SQLAlchemy ORM 模型对象时自动序列化
    )
# 用户验证接口返回数据
class UserVerification(BaseModel):
    token: str
    userInfo: UserInfoResponse = Field(...,alias="userInfo")

    model_config = ConfigDict(
        from_attributes=True,    # 支持传入 SQLAlchemy ORM 模型对象时自动序列化
        populate_by_name=True   # 支持传入字段名时自动填充字段
    )

#定义请求更新用户信息模型类
class UpdateUserInfo(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: int = None

#定义更新密码信息模型类
class UpdatePassword(BaseModel):
    old_password: str = Field(...,alias="oldPassword",description="旧密码")
    new_password: str = Field(...,alias="newPassword",description="新密码")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

