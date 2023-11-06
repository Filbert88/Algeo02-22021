from app import app
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for
from app import color_cbir
import json
import numpy as np
import shutil
import zipfile
import subprocess
import orjson

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
    # if 'image' not in request.files:
    #     return redirect(request.url)
    # file = request.files['image']
    # if file.filename == '':
    #     return redirect(request.url)
    # if file:
    #     filename = secure_filename(file.filename)
    #     save_path = os.path.join(app.config['DATASET_FOLDER'], filename)
    #     file.save(save_path)
    #     vec = color_cbir.get_vec_from_hsv_load(save_path)
    #     temp_data = {
    #         "image_path" : save_path,
    #         "vec" : str(vec)
    #     }
    #     with open('data/dataset_vec.json', 'r') as f:
    #         dataset = json.load(f)
    #     dataset.append(temp_data)
    #     with open('data/dataset_vec.json', 'w') as f:
    #         json.dump(dataset, f, indent=4)
    #     return "<h1>File uploaded successfully.</h1>"
    
    #Read Zip
    if 'zipfile' not in request.files:
            print("no file part")
            return "no file part"
    file = request.files['zipfile']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.zip'):
        dataset_dir = app.config['DATASET_FOLDER']
        rust_extract_zip(file, 'data/img')
        save_every_image_vec_to_json(dataset_dir)
        return '<h1>File successfully uploaded and images extracted.</h1>'

def extract_images(file, dir_path):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                with zip_ref.open(file_info) as source, open(os.path.join(dir_path, os.path.basename(file_info.filename)), 'wb') as target:
                    shutil.copyfileobj(source, target)

def save_every_image_vec_to_json(dir_path) :
    with open('data/dataset_vec.json', 'w') as f:
        json.dump([], f, indent=4)

    file_list = os.listdir(dir_path)
    total_files = len(file_list)
    counter = 1
    n = 10
    delta = total_files - (total_files % n)

    list_data = []
    for filename in file_list:
        file_path = os.path.join(dir_path, filename)
        vec = color_cbir.get_vec_from_hsv_load(file_path)
        temp_data = {
            "image_path": file_path,
            "vec": str(vec)
        }
        list_data.append(temp_data)
        if counter % n == 0 or (counter > delta):
            with open('data/dataset_vec.json', 'rb') as f:  # Read bytes
                dataset = orjson.loads(f.read())
            dataset.extend(list_data)
            with open('data/dataset_vec.json', 'wb') as f:  # Write bytes
                f.write(orjson.dumps(dataset))
            list_data = []
        counter += 1

def rust_extract_zip(file, dir_path) :
    zip_file_path = os.path.join(dir_path, file.filename)
    file.save(zip_file_path)

    rust_binary_path = 'rust_zip_extractor/target/release/rust_zip_extractor.exe'
    
    output_dir = 'data/img'

    command = [rust_binary_path, zip_file_path, output_dir]

    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        print('Success')
    except subprocess.CalledProcessError as e:
        print(f'Error: {e.returncode}\nOutput: {e.output}')
    os.remove(zip_file_path)