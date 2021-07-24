from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    公司 MTCV_HOME = 'D:/anaconda3/pycv-sample/mtcv'
    家 MTCV_HOME = 'D:/opencv/pynotebook/mtcv'
    server MTCV_HOME = ''
    """
    MTCV_HOME: str = ''


settings = Settings()

if __name__ == '__main__':
    print(settings)
