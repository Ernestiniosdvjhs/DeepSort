import os

import psycopg2
import cv2

def db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="db_track",
        user="admindb",
        password="pass",
        port="5432"
    )
    return conn

def count(filename):
    conn = db_connection()
    cur = conn.cursor()
    TXTFILE = f'/home/lineked/PycharmProjects/deepsort_project/results/{filename[:-4]}.txt'
    MP4FILE = f'/home/lineked/PycharmProjects/deepsort_project/results/{filename}'
    video = cv2.VideoCapture(MP4FILE)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = frame_count / fps
    minutes = int(seconds / 60)
    rem_sec = int(seconds % 60)
    duration = f"{minutes}:{rem_sec}"
    with open(TXTFILE) as file:
        k = sum([1 for _ in file])
    cur.execute('INSERT INTO data (filename, duration_video, statistic)'
                'VALUES (%s, %s, %s);',
                (f'{filename}',
                 f'{duration}',
                 f'{k}')
                )
    conn.commit()