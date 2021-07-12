from fastapi import APIRouter, File, UploadFile
from mt_cv import land_color_processor as lcp

router = APIRouter(
    prefix="/mt/cv",
    tags=["cv"],
)


@router.post("/land_color", summary="输入图片路径，返回地块与颜色信息")
async def land_color(img_path: str):
    """地块与色块信息

    Args:
        img_path: 图片路径
        TODO 假设img_path是id1/id1.png
    Returns:
        地块与色块信息

    Raises:
    """
    land_dict = lcp.process(img_path)

    return {
        # "direction": 'N',
        # "colors": {'value': [255, 0, 0], 'label': '商场'},
        # "scale": {'pixel': 670, 'meter': 1000},
        "land_color_data": land_dict,
    }
