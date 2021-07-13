import uvicorn
from fastapi import FastAPI
from mt_cv import mt_cv_api

app = FastAPI()
app.include_router(mt_cv_api.router)


@app.get("/")
async def root():
    return {"message": "Hello MTCV!"}

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
