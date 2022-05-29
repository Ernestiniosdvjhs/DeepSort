import os.path
from flask import *
from werkzeug.utils import secure_filename
import time
import count_detect

UPLOAD_FOLDER = '/home/lineked/PycharmProjects/deepsort_project/uploads'
RESULTS = '/home/lineked/PycharmProjects/deepsort_project/results'
FOLDER_WITH_FILE = '/home/lineked/PycharmProjects/deepsort_project/runs/track'
ALLOWED_EXTENSIONS = {'mp4'}#Расширения файлов, которые можно загрузить

app = Flask(__name__)
app.config['SECRET_KEY']= 'DKcd8!@ks_daHAFg'


@app.route('/', methods=['GET'])
def index():
    return redirect("/main")


def download(file, filename):#загрузка файла
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    os.system(f'python3 track.py --source uploads/{filename} --yolo_model weights.pt --save-vid --save-txt')
    os.remove(f'uploads/{filename}')
    if len(os.listdir(RESULTS))>0:
        os.system(f'rm -rf {RESULTS}/*')
    FILE = f'/home/lineked/PycharmProjects/deepsort_project/runs/track/weights_osnet_x0_25/{filename}'
    TXTFILE = f'/home/lineked/PycharmProjects/deepsort_project/runs/track/weights_osnet_x0_25/tracks/{filename[:-4]}.txt'
    time.sleep(20)
    os.system(f'cp {FILE} {RESULTS}')
    os.system(f'cp {TXTFILE} {RESULTS}')
    os.system('rm -rf runs/track/*')
    count_detect.count(filename)
    app.config['RESULTS'] = RESULTS
    return send_from_directory(app.config['RESULTS'], filename, as_attachment=True)


@app.route('/main', methods=['POST', 'GET'])#главная страница
def page_main():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect('/main')
        elif request.form.get('info'):
            return redirect('/info/')
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            if filename.split('.')[1] not in ALLOWED_EXTENSIONS:
                flash('Неправильный формат файла. Пожалуйста, выберите файл формата .mp4', category='error')
            else:
                return download(file, filename)
        else:
            flash('Нет выбранного файла', category='nofile')
    return render_template('main.html')


@app.route('/info/', methods=['GET', 'POST'])#информация о проекте
def page_about_us():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect('/main')
        elif request.form.get('info'):
            return redirect('info/')
    return render_template('info.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)