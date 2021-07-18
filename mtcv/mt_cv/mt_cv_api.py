from fastapi import APIRouter
from mt_cv import land_color_processor as lcp, \
    image_util, \
    hot_cold_processor as hcp, \
    image_segementation_processor as isp, \
    color_region_processor as crp

router = APIRouter(
    prefix="/mt/cv",
    tags=["cv"],
)


@router.post("/land_color", summary="输入图片URL，返回地块与颜色信息")
async def land_color(img_id: str, img_url: str):
    """地块与色块信息

    Args:
        img_id: 图片id
        img_url: 图片URL
    Returns:
        地块与色块信息

    Raises:
    """
    # TODO 根据img_url下载图片

    # 对下载的图片进行分割
    img_id = 'id2'
    file_name = 'id2.png'
    img_path = '../images/' + img_id + '/' + file_name
    land_color_scale_dict = isp.process(img_id, file_name, img_path)

    # 根据分割后的图片，获取颜色
    bgr_colors = crp.process(land_color_scale_dict['color_region'])

    # TODO 根据分割后的图片，获取比例尺的像素
    # scale = find_scale(src)
    scale = 670

    # 从分割后的图片计算地块和色块信息
    land_color_data = lcp.process(land_color_scale_dict['land_region'], bgr_colors)

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
