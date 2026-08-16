from passlib.context import CryptContext

# ============================================================
# passlib 密码加密（bcrypt）
# ============================================================
# 【安装】
# pip install "passlib[bcrypt]==1.7.4"
# 【初始化加密上下文】
# from passlib.context import CryptContext
# pwd_context = CryptContext(
#     schemes=["bcrypt"],   # 指定加密算法为 bcrypt
#     deprecated="auto"     # 新旧的密码加密方式兼容
# )
# 【加密】用户注册时，将明文密码加密后存入数据库
# hashed_password = pwd_context.hash(plain_password)
# 【校验】用户登录时，验证输入的密码是否匹配数据库中的哈希值
# is_valid = pwd_context.verify(input_password, hashed_password_from_db)
# # 返回 True 表示密码正确，False 表示错误
# ============================================================
"""
总结：不同场景的选型建议
存储用户密码：优先用 Argon2id，其次选 bcrypt 或 scrypt。

加密大量业务数据（如数据库）：选 AES，它速度快且安全。

做数字签名或身份认证：选 RSA 或 ECC。

验证文件是否被篡改：用 SHA-256 这类哈希算法。

对接国内政企项目：需要留意 国密算法（SM2/SM3/SM4） 的要求。
"""



#初始化加密上下文
#bcrypt通过“工作因子”（Cost Factor）控制计算强度，适配不同性能的硬件。注意：bcrypt有72字节的密码长度限制
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(password: str):
    """
    获取密码的哈希值
    """
    return pwd_context.hash(password)

#验证密码
def verify_password(plain_password, hashed_password): #密码明文，密码密文
    return pwd_context.verify(plain_password, hashed_password)
    #返回True表示密码正确，False表示错误