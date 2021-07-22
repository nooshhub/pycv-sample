from fastapi import APIRouter
from mt_cv import land_color_processor as lcp, \
    image_util, \
    hot_cold_processor as hcp, \
    image_segmentation_processor as isp, \
    color_region_processor as crp, \
    image_downloader as img_dl

router = APIRouter(
    prefix="/mt/cv",
    tags=["cv"],
)


@router.post("/land_color", summary="输入图片URL，返回地块与颜色信息")
async def land_color(img_url: str):
    """地块与色块信息

    Args:
        img_url: 图片URL
    Returns:
        地块与色块信息

    Raises:
    """
    # 根据img_url下载图片
    folder_name, image_path = img_dl.download_img(img_url)

    # 对下载的图片进行分割
    land_region_path, color_region_path, scale_region_path = isp.process(folder_name, image_path)

    # 根据分割后的图片，获取颜色
    bgr_colors = crp.process(color_region_path)

    # TODO 根据分割后的图片，获取比例尺的像素
    # scale = find_scale(scale_region_path)
    scale = 670

    # 从分割后的图片计算地块和色块信息
    land_color_data = lcp.process(land_region_path, bgr_colors)

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
    hot_cold_data = hcp.process(image_util.img_abs_path('/images' + img_path))

    return {'hot_cold_data': hot_cold_data}
