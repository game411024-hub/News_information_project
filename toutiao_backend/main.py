from routers import news,users,favorites,history,ai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toutiao_backend.utils.Exception_handing import exceptons_handler


"""
FastAPI 配置
"""
app = FastAPI()

#注册异常处理器
exceptons_handler(app)


"""
CORS处理
"""
# Origins = [
#     "http://localhost:8000",
#     "http://localhost:",
#     "http://localhost:5173"
# ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许的源
    allow_credentials=True,     # 允许携带cookie
    allow_methods=["*"],        # 允许的请求方法
    allow_headers=["*"],        # 允许的请求头
)



#挂载routers
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(ai.router)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)