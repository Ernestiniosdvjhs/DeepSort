import os.path
import sys
from flask import Flask, redirect, request, render_template
from werkzeug.utils import secure_filename


allowed_extensions = {'mp4', 'docx'}


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect("/osn")


@app.route('/osn', methods=['POST', 'GET'])
def page_main():
    if request.method == 'POST':
        if request.form.get('Osn'):
            return redirect("/osn")
        elif request.form.get("O_Nas"):
            return redirect("/o_nas/")
        elif request.form.get("O_Pr"):
            return redirect("/o_pr/")
        f = request.files['file']
        filename = secure_filename(f.filename)
        if filename.split('.')[1] not in allowed_extensions:
            return 'Error file type'
        else:
            f.save(os.path.join(os.path.dirname(sys.argv[0]), filename))
    return render_template('Osn.html')


@app.route('/o_nas/', methods=['GET', 'POST'])
def page_about_us():
    if request.method == 'POST':
        if request.form.get('Osn'):
            return redirect("/")
        elif request.form.get("O_Nas"):
            return redirect("/o_nas/")
        elif request.form.get("O_Pr"):
            return redirect("/o_pr/")
    return render_template('O_Nas.html')


@app.route('/o_pr/', methods=['GET', 'POST'])
def page_about_project():
    if request.method == 'POST':
        if request.form.get('Osn'):
            return redirect("/")
        elif request.form.get("O_Nas"):
            return redirect("/o_nas/")
        elif request.form.get("O_Pr"):
            return redirect("/o_pr/")
    return render_template('O_Pr.html')


if __name__ == '__main__':
    app.run()
