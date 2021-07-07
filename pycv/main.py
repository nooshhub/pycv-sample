from fastapi import Depends, FastAPI

from dependencies import get_query_token
from internal import admin
from routers import items, users
from mtfile import mtfile_manager

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)
app.include_router(mtfile_manager.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
