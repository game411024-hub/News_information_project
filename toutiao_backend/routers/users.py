from fastapi import HTTPException,status
from schemas.favorites import CheckIsFavorite
from toutiao_backend.config.db_conf import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from toutiao_backend.crud.users import authenticate_user, create_token
from toutiao_backend.models.users import  User
from toutiao_backend.schemas.users import UserRequest, UserVerification, UserInfoResponse, UpdateUserInfo, \
    UpdatePassword
from toutiao_backend.crud import users
from toutiao_backend.utils.Response import success_response
from toutiao_backend.utils.auth import authenticate_current_user

# 用户模块
router = APIRouter(prefix="/api/user", tags=["user"])

"""
    用户注册模块
"""


#用户注册接口
@router.post("/register")
async def register(
        update_data: UserRequest,
        db: AsyncSession = Depends(get_db)
        ):
    #先根据用户名查询数据库，再进行添加创建
    existing_users = await users.get_user_by_username(db,update_data.username)
    #判断一下是否有这个账户，如果有的话返回结果
    if existing_users:
        raise HTTPException(
            status_code=404,
            detail="该用户已注册！"
        )
    #调用创建用户方法，返回 SQLAlchemy 的 ORM 对象（User 实例）
    users_im = await users.create_user(db,update_data)
    #Token令牌验证，返回 Token 记录（ORM 对象）
    token_verification = await users.create_token(db,users_im.id)
#返回通用响应josn格式数据
    return success_response(
        message="注册成功",
        data=UserVerification(
            token=token_verification.token,
            # 把 ORM 对象(users_im)转换为 Pydantic 模型 UserInfoResponse
            # 使用 model_validate() 而非 model_config：model_config 是配置属性(dict)，不可调用
            # 前提：schemas/users.py 中 UserInfoResponse 已配置 from_attributes=True
            # 效果：自动读取 User 对象上的 id、username、nickname、avatar 等属性，构建响应模型
            userInfo=UserInfoResponse.model_validate(users_im)
        )
    )
    # return {
    #         "code": 200,
    #         "message": "注册成功",
    #         "data": {
    #           "token":token_verification.token, #获取令牌对象
    #           "userInfo": {
    #             "id": users_im.id,              #获取用户id对象
    #             "username": users_im.username,  #获取用户名字
    #             "bio": users_im.bio,            #获取个人简介
    #             "avatar": users_im.avatar       #获取用户头像
    #                     }
    #                 }
    #         }

#用户登录接口
@router.post("/login")
async def login(
        user_data:UserRequest,
        db:AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    token = await create_token(db,user.id)
    data = UserVerification(token=token.token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登陆成功！",data=data)

#获取用户信息
@router.get("/info")
async def get_user_info(
        user_info:User = Depends(authenticate_current_user)
):
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="没有找到此用户"
        )
    data = UserInfoResponse.model_validate(user_info)
    return success_response(message="获取成功！",data = data)

# 修改用户信息：验证Token → 更新（用户输入数据 put 提交 → 请求体参数 → 定义PyDatatc模型类） → 响应结果
# 参数：用户输入的 + 验证Token的 + db（调用更新的方法）
#修改用户信息
@router.put("/update")
async def update_user_data(
        user_data:UpdateUserInfo,
        auth_token:User = Depends(authenticate_current_user),
        db:AsyncSession = Depends(get_db)
):
    #调用函数更新用户数据,返回最新的用户信息
    user = await users.update_user_data(db,auth_token.username,user_data)
    data = UserInfoResponse.model_validate(user)
    return success_response(message="更新成功！",data=data)

#修改密码
@router.put("/password")
async def update_user_password(
        user_pwd : UpdatePassword,
        db:AsyncSession = Depends(get_db),
        auth_token_user:User = Depends(authenticate_current_user),

):
    orm_db_user = await users.update_user_password(db,auth_token_user.username,user_pwd)
    await create_token(db,orm_db_user.id)
    data = CheckIsFavorite
    return success_response(message="密码修改成功",data=data)