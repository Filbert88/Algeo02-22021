from app import app
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for

@app.route('/')
def index():
    os.makedirs('data/img/user_img', exist_ok=True)
    os.makedirs('data/img/dataset', exist_ok=True)
    return render_template('index.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/program')
def program():
    return render_template('program.html')

@app.route('/upload_image', methods=['POST'])
def upload_image() :
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return "<h1>File uploaded successfully.</h1>"
    
@app.route('/reset_message', methods=['GET'])
def reset_message() :
    return ""