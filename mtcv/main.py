from fastapi import FastAPI
from mt_cv import mt_cv_api

app = FastAPI()
app.include_router(mt_cv_api.router)


@app.get("/")
async def root():
    return {"message": "Hello MTCV!"}
