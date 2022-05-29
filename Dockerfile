FROM python:3.9
WORKDIR /home/lineked/PycharmProjects/deepsort_project/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-pythond
COPY . .
EXPOSE 8888
CMD ["python", "app.py"]