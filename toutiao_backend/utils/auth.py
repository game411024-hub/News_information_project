from fastapi import Header, Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from toutiao_backend.config.db_conf import get_db
from toutiao_backend.crud import users
from toutiao_backend.models.users import Token, User


#获取token信息
async def authenticate_current_user(
        Authentication = Header(...,alias="Authorization"),
        db: AsyncSession = Depends(get_db)
                                    ):
    """
    :param Authentication: 认证信息
    :param db: 数据库连接
    :return: 用户信息
    """

    # user_token_info = Authentication.split(" ")[1]
    user_token_info = Authentication.replace("Bearer ","")
    db_token_user = await users.auth_token_info(db,user_token_info)#-> Token表信息
    if not db_token_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期~"
        )
    stmt = await db.execute(select(User).where(User.id == db_token_user.user_id))
    db_user = stmt.scalars().one_or_none()
    return db_user #-> User表信息

