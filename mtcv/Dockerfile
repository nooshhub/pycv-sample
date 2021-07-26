FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -U pip
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

RUN pip install fastapi uvicorn aiofiles opencv-python==4.5.1.48 opencv-contrib-python==4.5.1.48

EXPOSE 8000

COPY ./ /
ENV MTCV_HOME=""
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]