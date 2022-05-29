import psycopg2
if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        database="db_track",
        user="admindb",
        password="pass",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS data;')
    cur.execute('CREATE TABLE data (id SERIAL NOT NULL,'
                'filename VARCHAR NOT NULL,'
                'duration_video VARCHAR NOT NULL,'
                'statistic VARCHAR NOT NULL);'
                )
    conn.commit()
