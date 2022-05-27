import os.path
import sys
from flask import *
from werkzeug.utils import secure_filename
import time

UPLOAD_FOLDER = '/home/lineked/PycharmProjects/deepsort_project/uploads'
FOLDER_WIT_FILE = '/home/lineked/PycharmProjects/deepsort_project/runs/track'
ALLOWED_EXTENSIONS = {'mp4'}#Расширения файлов, которые можно загрузить

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect("/main")

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
                flash('Нет выбранного файла')
            else:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                os.system(f'python3 track.py --source uploads/{filename} --yolo_model weights.pt --save-vid')
                os.remove(f'uploads/{filename}')
                get_files = os.listdir(FOLDER_WIT_FILE)
                print(get_files.sort())
                FOLDER_WITH_FILE = f"/home/lineked/PycharmProjects/deepsort_project/runs/track/{get_files[-1]}"
                app.config['FOLDER_WITH_FILE'] = FOLDER_WITH_FILE
                print(FOLDER_WITH_FILE)
                time.sleep(30)
                return send_from_directory(app.config['FOLDER_WITH_FILE'], filename, as_attachment=True)
    return render_template('main.html')


@app.route('/info/', methods=['GET', 'POST'])
def page_about_us():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect("/main")
        elif request.form.get("info"):
            return redirect("/info/")
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
