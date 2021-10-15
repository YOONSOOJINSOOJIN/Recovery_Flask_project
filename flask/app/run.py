from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
# from app import app
from flask import Flask, render_template, request, flash, redirect
import os
import glob
application = Flask(__name__)

UPLOAD_FOLDER = '/Users/afoter/FlaskProject/flask/app/static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

img_list = glob.glob(UPLOAD_FOLDER + '/*')
img_name = img_list[0].split('/')[-1]



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 게시 요청에 파일 부분이 있는지 확인
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # 사용자가 파일을 선택하지 않으면 브라우저는
        # 파일 이름이없는 빈 파일.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))

    return render_template('upload_page.html', image_file = img_name)


# @application.route('/', methods = ['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(upload_path + secure_filename(f.filename))
#     return render_template('upload_page.html', image_file = upload_path + recent_file)

# @application.route('/uploader', methods = ['GET', 'POST'])
# def uploader_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(upload_path + secure_filename(f.filename))
#         return 'file uploaded successfully'



if __name__ == '__main__':
    application.secret_key = 'super secret key'
    application.config['SESSION_TYPE'] = 'filesystem'
    application.run(debug=True)
