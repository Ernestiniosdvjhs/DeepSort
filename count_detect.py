import psycopg2
import cv2
import os.path

def db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="db_track",
        user="admindb",
        password="pass",
        port="5432"
    )
    return conn

def count(filename):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS data (id SERIAL NOT NULL,'
                'filename VARCHAR NOT NULL,'
                'duration_video VARCHAR NOT NULL,'
                'statistic VARCHAR NOT NULL);'
                )
    conn.commit()
    TXTFILE = f'{os.path.join(os.path.dirname(__file__))}/results/{filename[:-4]}.txt'
    MP4FILE = f'{os.path.join(os.path.dirname(__file__))}/results/{filename}'
    video = cv2.VideoCapture(MP4FILE)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = frame_count / fps
    minutes = int(seconds / 60)
    rem_sec = int(seconds % 60)
    duration = f"{minutes}:{rem_sec}"
    with open(TXTFILE) as file:
        sum_detect = sum([1 for _ in file])
    cur.execute('INSERT INTO data (filename, duration_video, statistic)'
                'VALUES (%s, %s, %s);',
                (f'{filename}',
                 f'{duration}',
                 f'{sum_detect}')
                )
    conn.commit()