from fastapi import APIRouter
from mt_cv import land_color_processor as lcp, image_util, hot_cold_processor as hcp

router = APIRouter(
    prefix="/mt/cv",
    tags=["cv"],
)


@router.post("/land_color", summary="输入图片路径，返回地块与颜色信息")
async def land_color(img_path: str):
    """地块与色块信息

    Args:
        img_path: 图片路径
        TODO 假设img_path是/id1/id1.png
    Returns:
        地块与色块信息

    Raises:
    """
    land_color_data = lcp.process(image_util.img_abs_path('/images' + img_path))

    return {
        # "direction": 'N',
        # "colors": {'value': [255, 0, 0], 'label': '商场'},
        # "scale": {'pixel': 670, 'meter': 1000},
        "land_color_data": land_color_data,
    }


@router.post("/hot_cold", summary="输入图片路径，返回冷热分区信息，地块按供能方块分组")
async def land_color(img_path: str):
    """地块按供能方块分组信息

    Args:
        img_path: 图片路径
        TODO 假设img_path是/id1/id1.png
    Returns:
        地块与色块信息

    Raises:
    """
    rr_land_data = hcp.process(image_util.img_abs_path('/images' + img_path))

    return rr_land_data
