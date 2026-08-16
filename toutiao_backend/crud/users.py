import uuid
from datetime import datetime,timedelta
from fastapi import HTTPException,status
from sqlalchemy import select,update
from sqlalchemy.ext.asyncio import AsyncSession
from toutiao_backend.models.users import User,Token
from toutiao_backend.schemas.users import UserRequest, UpdateUserInfo, UpdatePassword
from toutiao_backend.utils import Security
from toutiao_backend.utils.Security import verify_password


#根据用户名查询数据库
async def get_user_by_username( db: AsyncSession,username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()#返回查询结果,返回的查询结果是一个对象

#创建用户
async def create_user(db: AsyncSession,user_data:UserRequest):

    #先利用passlib密码加密
    encryption_password = Security.get_hash(user_data.password)
    user = User(username=user_data.username,password=encryption_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

#创建Token
async def create_token(db: AsyncSession,user_id: int):
       token = str(uuid.uuid4())    #生成随机数
       #验证Token时间
       expire_time = datetime.utcnow() + timedelta(days=7)#7天后过期
       token_data = Token(user_id=user_id, token=token, expires_at=expire_time)
       # 先查Token表，如果存在user_id用户，就更新，如果没有则创建
       result = await db.execute(select(Token).where(Token.user_id == user_id))
       stmt =result.scalar_one_or_none()
       if stmt:
           stmt.token = token
           stmt.expires_at = expire_time
           db.add(stmt)
           await db.commit()
           await db.refresh(stmt)
           return stmt
       db.add(token_data)
       await db.commit()
       await db.refresh(token_data)
       return token_data

#用户登录验证
async def authenticate_user(db: AsyncSession,username: str,password: str):
    user = await get_user_by_username(db,username)
    if not user:
        return  None
    #验证密码
    user_password = verify_password(password,user.password)
    if not user_password:
        return None
    return user

#验证token信息
async def auth_token_info(db: AsyncSession,token: str):
    stmt = await db.execute(select(Token).where(Token.token == token))
    user_token = stmt.scalars().one_or_none()#--返回查询结果Token对象
    if not user_token or user_token.expires_at < datetime.now():#验证Token时间
        return  None
    return user_token

#更新用户信息
async def update_user_data(
        db: AsyncSession,
        username:str,
        user_data:UpdateUserInfo
):
    user =await get_user_by_username(db,username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到此用户"
        )

    update_stmt = update(User).where(User.username == username).values(
        **user_data.model_dump(#**user_data.model_dump解包操作，忽略未设置和未定义的参数
        exclude_unset=True, #忽略未设置参数
        exclude_none=True,#忽略未定义参数
    )
    )
    await db.execute(update_stmt)
    await db.commit()
    await db.refresh(user)
    return user#返回的是user的查询结果

#修改用户密码
async def update_user_password(
        db: AsyncSession,
        username:str,
        user_data:UpdatePassword
):
    user =await get_user_by_username(db,username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到此用户"
        )
    #验证用户的旧密码是否和数据库里面的密码一致
    verify_pwd = verify_password(user_data.old_password,user.password)
    if not verify_pwd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误"
        )
    update_stmt = update(User).where(User.username == username).values(
        password=Security.get_hash(user_data.new_password)
    )
    await db.execute(update_stmt)
    await db.commit()
    await db.refresh(user)
    return user








