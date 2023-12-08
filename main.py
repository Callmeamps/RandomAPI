from fastapi import FastAPI
from api.chat import router as chat_router
from api.auth import router as auth_router
from api.post import router as post_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(post_router)

# @app.get("/")
# def welcome():
#     return {"Message": "Hello"}
