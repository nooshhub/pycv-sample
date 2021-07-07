from fastapi import FastAPI
from mt_file import mt_file_manager

app = FastAPI()
app.include_router(mt_file_manager.router)


@app.get("/")
async def root():
    return {"message": "Hello MTCV!"}
