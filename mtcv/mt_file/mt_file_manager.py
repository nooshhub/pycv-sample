from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/mt/files",
    tags=["file"],
)


@router.get("/", summary="list files", description="list all files and folders under /img")
def list_files():
    return "list all files and folders under /img"


@router.post("/", summary="create file")
async def create_file(file: bytes = File(...)):
    """
    单个文件上传
    """
    return {"file_size": len(file)}


@router.post("/upload", summary="create upload file, what's the difference with File")
async def create_upload_file(file: UploadFile = File(...)):
    """
    单个文件上传
    """
    contents = await file.read()
    return {"filename": file.filename,
            "content_type": file.content_type}


@router.post("/multiple")
def upload_multiple(files: List[bytes] = File(...)):
    """
    多个文件上传
    """
    return {"file_sizes": [len(file) for file in files]}


@router.post("/multiple_upload")
def upload_multiple_upload(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@router.get("/help")
async def help():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
