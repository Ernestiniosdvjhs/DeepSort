import os.path
import sys
from flask import *
from werkzeug.utils import secure_filename
import time
import psycopg2

UPLOAD_FOLDER = '/home/lineked/PycharmProjects/deepsort_project/uploads'
FOLDER_WIT_FILE = '/home/lineked/PycharmProjects/deepsort_project/runs/track'
ALLOWED_EXTENSIONS = {'mp4'}#Расширения файлов, которые можно загрузить

app = Flask(__name__)
app.config['SECRET_KEY']= 'oifeeowwffwefew342'
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
                               'duration_video VARCHAR NOT NULL);'
                            )


@app.route('/', methods=['GET'])
def index():
    return redirect("/main")

def send_file(file, filename):
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    os.system(f'python3 track.py --source uploads/{filename} --yolo_model weights.pt --save-vid --save-txt')
    os.remove(f'uploads/{filename}')
    get_files = os.listdir(FOLDER_WIT_FILE)
    print(get_files.sort())
    FOLDER_WITH_FILE = f"/home/lineked/PycharmProjects/deepsort_project/runs/track/{get_files[-1]}"
    app.config['FOLDER_WITH_FILE'] = FOLDER_WITH_FILE
    print(FOLDER_WITH_FILE)
    time.sleep(30)
    cur.execute('INSERT INTO data (filename, duration_video) '
                'VALUES (%s, %s)',
                ('video1',
                 'test')
                )
    conn.commit()
    cur.close()
    conn.close()
    return send_from_directory(app.config['FOLDER_WITH_FILE'], filename, as_attachment=True)


@app.route('/main', methods=['POST', 'GET'])
def page_main():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect("/main")
        elif request.form.get("info"):
            return redirect("/info/")
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            if filename.split('.')[1] not in ALLOWED_EXTENSIONS:
                flash('Неправильный формат файла. Пожалуйста, выберите файл формата .mp4', category='error')
            else:
                return send_file(file, filename)
        else:
            flash("Нет выбранного файла", category='nofile')
    return render_template('main.html')

@app.route('/info/', methods=['GET', 'POST'])
def page_about_us():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect("/main")
        elif request.form.get("info"):
            return redirect("/info/")
    return render_template('info.html')


if __name__ == '__main__':
    app.run()
