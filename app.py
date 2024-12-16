from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from toll_ocr import extract_plate_and_toll

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return render_template('index.html', uploaded_image=file.filename)
    return render_template('index.html', uploaded_image=None)

@app.route('/detect/<filename>')
def detect(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    plate, state, toll = extract_plate_and_toll(file_path)
    return render_template('result.html', plate=plate, state=state, toll=toll, image=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
