from app import app
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for
from app import color_cbir, texture_cbir
import json
import numpy as np
import shutil
import zipfile
import orjson
import threading
import time

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

@app.route('/upload_image', methods=['GET', 'POST'])
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
        with open('data/dataset_vec.json', 'rb') as f:
            dataset = orjson.loads(f)
        
        #HANDLE NO DATA
        if len(dataset) == 0 :
            return "<h1>No Data in Dataset</h1>"
        
        similar_images = []
        for data_el in dataset :
            similarity = color_cbir.cosine_similarity(vec, np.fromstring(data_el["vec"].strip('[]'), sep=', '))
            if similarity >= 0.6 :
                similar_images.append({
                    "img_url" : data_el["image_path"],
                    "similarity" : similarity})
        
        for el in similar_images :
             print(el["img_url"], el["similarity"], "\n")

        return "<h1>Search successful</h1>"
    
@app.route('/reset_message', methods=['GET'])
def reset_message() :
    return ""

@app.route('/upload_dataset', methods=['POST'])
def upload_dataset() :
    if 'zipfile' not in request.files:
            print("NO FILE PART")
            return "NO FILE PART"
    file = request.files['zipfile']
    if file.filename == '':
        return 'NO SELECTED FILE'
    if file and file.filename.endswith('.zip'):
        dataset_dir = app.config['DATASET_FOLDER']
        start_time = time.time()
        extract_zip(file, 'data/img')
        end_time = time.time()
        extract_duration = end_time - start_time
        print(f"EXTRACT TIME: {extract_duration}")
        start_time = time.time()
        save_every_image_vec_to_json(dataset_dir)
        end_time = time.time()
        process_duration = end_time - start_time
        print(f"PROCESS DATASET TIME: {process_duration}")
        return '<h1>File successfully uploaded and images extracted.</h1>'

def extract_images_from_zip(file, dir_path):
    dataset_folder = os.path.join(dir_path, 'dataset')
    if os.path.exists(dataset_folder) and os.path.isdir(dataset_folder):
        shutil.rmtree(dataset_folder)
    os.makedirs(dataset_folder)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                with zip_ref.open(file_info) as source, open(os.path.join(dataset_folder, os.path.basename(file_info.filename)), 'wb') as target:
                    shutil.copyfileobj(source, target)

def process_file_chunk(file_chunk, result_list):
    temp_data = []
    for filename in file_chunk:
        vec_color = color_cbir.get_vec_from_hsv_load(filename)
        vec_texture = texture_cbir.get_vector_from_image(filename)
        texture = [vec_texture[0], vec_texture[1], vec_texture[2]]
        temp_data.append({
            "image_path": filename,
            "vec_color": str(vec_color),
            "vec_texture": str(texture)
        })
    result_list.extend(temp_data)

def save_every_image_vec_to_json(dir_path):
    with open('data/dataset_vec.json', 'wb') as f:
        f.write(orjson.dumps([]))

    file_list = [os.path.join(dir_path, filename) for filename in os.listdir(dir_path)]
    total_files = len(file_list)
    
    num_threads = 8
    chunk_size = total_files // num_threads

    file_chunks = [file_list[i:i + chunk_size] for i in range(0, total_files, chunk_size)]

    thread_results = []

    threads = []
    for chunk in file_chunks:
        thread = threading.Thread(target=process_file_chunk, args=(chunk, thread_results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open('data/dataset_vec.json', 'wb') as f:
        f.write(orjson.dumps(thread_results))

def extract_zip(file, dir_path) :
    output_dir = 'data/img'
    extract_images_from_zip(file, output_dir)