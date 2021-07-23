from pydantic import BaseModel
from typing import List, Optional


class MtImage(BaseModel):
    """处理地块和色块信息时，生成的图片的宽高"""
    width: int = None
    height: int = None


class MtScale(BaseModel):
    """比例尺用于画供能半径，根据 rr_radius = km * pixel"""
    pixel: int = None
    km: int = None


class MtCoordinate(BaseModel):
    """坐标"""
    xAxis: int = None
    yAxis: int = None


class LandData(BaseModel):
    """地块数据"""
    id: str = None
    points: List[MtCoordinate] = []


class InputData(BaseModel):
    """图像，地块，比例尺数据"""
    img_data: MtImage = None
    land_data: List[LandData] = []
    scale: MtScale = None
