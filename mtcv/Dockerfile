FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install fastapi uvicorn opencv-python==4.5.1.48 opencv-contrib-python==4.5.1.48

EXPOSE 8000

COPY ./ /

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]