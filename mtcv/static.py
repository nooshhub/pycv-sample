import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import pathlib

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
async def root():
    return list_images()


def list_images():
    image_paths = []
    for path, subdirs, files in os.walk('images'):
        for name in files:
            image_paths.append(pathlib.PurePath(path, name).as_posix())
    return image_paths


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
