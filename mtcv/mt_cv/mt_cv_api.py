from fastapi import APIRouter, File, UploadFile
from mt_cv import land_color_processor as lcp

router = APIRouter(
    prefix="/mt/cv",
    tags=["cv"],
)


@router.post("/land_color", summary="上传单个图片，返回地块与颜色信息")
async def land_color(file: UploadFile = File(...)):
    """地块与色块信息

    Args:
        file: 图片文件

    Returns:
        地块与色块信息

    Raises:

    """
    img_path = 'upload/' + file.filename
    with open(img_path, 'wb') as img:
        img.write(await file.read())

    land_dict = lcp.process(img_path)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "direction": 'N',
        "colors": {'value': [255, 0, 0], 'label': '商场'},
        "scale": {'pixel': 670, 'meter': 1000},
        "land_color_data": land_dict,
    }
