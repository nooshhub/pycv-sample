from fastapi import APIRouter, HTTPException
from mt_cv import land_color_processor as lcp, \
    image_util, \
    hot_cold_processor as hcp, \
    image_segmentation_processor as isp, \
    color_region_processor as crp, \
    scale_region_processor as srp, \
    image_downloader as img_dl, \
    image_generator as img_gen
from mt_cv.mt_cv_api_model import InputData

router = APIRouter(
    prefix="/mt/cv",
    tags=["cv"],
)


@router.post("/land_color", summary="输入图片URL，返回地块与颜色信息")
def land_color(img_url: str = 'http://localhost:8002/images/demo/demo3_1.png', land_data_only: bool = False
               , clean_image: bool = True):
    """地块与色块信息

    Args:
        img_url: 图片URL
        land_data_only: True只返回地块信息，用于计算冷热分区
        clean_image: True删除所有生成的图片，False保留生成的图片，用于分析图片处理的问题

    Returns:
        地块与色块信息

    """
    # 根据img_url下载图片
    image_folder, image_path = img_dl.download_img(img_url)

    # 对下载的图片进行分割
    land_region_path, color_region_path, scale_region_path = isp.process(image_folder, image_path)

    # 根据分割后的图片，获取颜色
    bgr_colors = crp.process(color_region_path)
    if len(bgr_colors) == 0:
        raise HTTPException(status_code=500, detail="无法识别色块")

    # 根据分割后的图片，获取比例尺的像素
    scale = srp.process(scale_region_path)
    if scale == 0:
        raise HTTPException(status_code=500, detail="无法识别比例尺")

    # 从分割后的图片计算地块和色块信息
    land_color_data, image_width_height = lcp.process(land_region_path, bgr_colors, scale,
                                                      land_data_only=land_data_only)
    # TODO 添加地块的一些校验

    # 清理图片
    if clean_image:
        img_dl.clean_img(image_folder)

    if land_data_only:
        response_data = {
            # "direction": 'N',
            # "bgr_colors": bgr_colors,
            "scale": {'pixel': int(scale), 'km': int(1)},
            "land_data": land_color_data['data'],
            "img_data": image_width_height
        }
    else:
        response_data = {
            # "direction": 'N',
            # "bgr_colors": bgr_colors,
            "scale": {'pixel': int(scale), 'km': int(1)},
            "land_color_data": land_color_data,
            "image_data": image_width_height
        }

    return response_data


@router.post("/hot_cold", summary="按照图像，地块，比例尺数据，返回冷热分区信息，地块按供能方块分组")
def hot_cold(input_data: InputData, clean_image: bool = True):
    """按照图像，地块，比例尺数据生成图片，然后进行分组

    Args:
        input_data: 图像，地块，比例尺数据
        clean_image: True删除所有生成的图片，False保留生成的图片，用于分析图片处理的问题

    Returns:
        冷热地块数据

    """

    # 根据输入数据，生成图片
    image_folder, image_path, color_id_dict = img_gen.generate(input_data)

    # 生成冷热地块数据
    scale = input_data.scale
    hot_cold_data, image_width_height = hcp.process(image_folder, image_path, color_id_dict, scale.pixel, scale.km,
                                debug=not clean_image)

    # 清理图片
    if clean_image:
        img_dl.clean_img(image_folder)

    return {
        'hot_cold_data': hot_cold_data,
        "image_data": image_width_height
    }
