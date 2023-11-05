from app import app
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for
from app import color_cbir
import json
import numpy as np

@app.route('/')
def index():
    os.makedirs('data/img/user', exist_ok=True)
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
        vec = color_cbir.get_vec_from_hsv_load(save_path)
        os.remove(save_path)
        with open('data/dataset_vec.json', 'r') as f:
                dataset = json.load(f)
        if len(dataset) == 0 :
            return "<h1>No Data in Dataset</h1>"
        similar_images = []
        for data_el in dataset :
            similarity = color_cbir.cosine_similarity(vec, np.fromstring(data_el["vec"].strip('[]'), sep=', '))
            if similarity >= 0.6 :
                similar_images.append([data_el["image_path"], similarity])
        for el in similar_images :
             print(el[0], el[1], "\n")
        return "<h1>Search successfully.</h1>"
    
@app.route('/reset_message', methods=['GET'])
def reset_message() :
    return ""

@app.route('/upload_dataset', methods=['POST'])
def upload_dataset() :
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['DATASET_FOLDER'], filename)
        file.save(save_path)
        vec = color_cbir.get_vec_from_hsv_load(save_path)
        temp_data = {
            "image_path" : save_path,
            "vec" : str(vec)
        }
        with open('data/dataset_vec.json', 'r') as f:
            dataset = json.load(f)
        dataset.append(temp_data)
        with open('data/dataset_vec.json', 'w') as f:
            json.dump(dataset, f, indent=4)
        return "<h1>File uploaded successfully.</h1>"