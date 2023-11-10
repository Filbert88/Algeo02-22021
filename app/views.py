from app import app
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from app import color_cbir, texture_cbir
import numpy as np
import shutil
import zipfile
import orjson
import threading
import time

@app.route('/')
def index():
    with open('app/data/dataset_vec.json', 'wb') as f:
        f.write(orjson.dumps([]))
    os.makedirs('app/data/img/user', exist_ok=True)
    os.makedirs('app/data/img/dataset', exist_ok=True)
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

@app.route('/dataset_images/<path:filename>')
def serve_dataset_image(filename):
    return send_from_directory('data/img/dataset', filename)

@app.route('/upload_image', methods=['POST'])
def upload_image() :
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        start = time.time()
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        vec = color_cbir.get_vec_from_hsv_load(save_path)
        os.remove(save_path)
        with open('app/data/dataset_vec.json', 'rb') as f:
            dataset = orjson.loads(f.read())
        
        #HANDLE NO DATA
        if len(dataset) == 0 :
            return "<div class='errorMsg'>No Data in Dataset</div>"
        
        similar_images = []
        for data_el in dataset :
            similarity = color_cbir.cosine_similarity(vec, np.fromstring(data_el["vec_color"].strip('[]'), sep=', '))
            if similarity >= 0.6 :
                similar_images.append({
                    "filename" : data_el["filename"],
                    "similarity" : str(round(similarity, 4)),
                    "image_url": url_for('serve_dataset_image', filename=data_el["filename"])
                })
        similar_images = sorted(similar_images, key=lambda x: x["similarity"], reverse=True)
        end = time.time()
        duration = round(end - start, 2)
        for el in similar_images :
            print(el["filename"], el["similarity"])
        
        with open('app/data/result.json', 'wb') as f:
            f.write(orjson.dumps(similar_images))
        
        return render_template('result.html', result=len(similar_images), duration=duration)

@app.route('/upload_zip', methods=['POST'])
def upload_zip() :
    if 'zipfile' not in request.files:
            print("NO FILE PART")
            return "NO FILE PART"
    file = request.files['zipfile']
    if file.filename == '':
        return 'NO SELECTED FILE'
    if file and file.filename.endswith('.zip'):
        dataset_dir = app.config['DATASET_FOLDER']
        start_time = time.time()
        extract_images_from_zip(file, dataset_dir)
        end_time = time.time()
        extract_duration = end_time - start_time
        print(f"EXTRACT TIME: {extract_duration}")
        start_time = time.time()
        save_every_image_vec_to_json(dataset_dir)
        end_time = time.time()
        process_duration = end_time - start_time
        print(f"PROCESS DATASET TIME: {process_duration}")
        return render_template('success.html')

def extract_images_from_zip(file, dir_path):
    dataset_folder = dir_path
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
            "filename": filename.split('/')[-1],
            "vec_color": str(vec_color),
            "vec_texture": str(texture)
        })
    result_list.extend(temp_data)

def save_every_image_vec_to_json(dir_path):
    file_list = [pathjoin(dir_path, filename) for filename in os.listdir(dir_path)]
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

    with open('app/data/dataset_vec.json', 'wb') as f:
        f.write(orjson.dumps(thread_results))

@app.route('/close_upload_form', methods=['GET'])
def close_form():
    return ""

@app.route('/upload_popup', methods=['GET'])
def upload_popup():
    return render_template('upload_popup.html')

@app.route('/upload_zip_form', methods=['GET'])
def upload_zip_form():
    return render_template('upload_zip_form.html')

@app.route('/upload_folder_form', methods=['GET'])
def upload_folder_form():
    return render_template('upload_folder_form.html')

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    app.config['MAX_CONTENT_LENGTH'] = None
    uploaded_files = request.files.getlist('files[]')
    dataset_folder = 'app/data/img/dataset/'
    if os.path.exists(dataset_folder) and os.path.isdir(dataset_folder):
        shutil.rmtree(dataset_folder)
    os.makedirs(dataset_folder)

    for file in uploaded_files:
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(pathjoin(dataset_folder, filename))

    start_time = time.time()
    save_every_image_vec_to_json(dataset_folder)
    end_time = time.time()
    process_duration = end_time - start_time
    print(f"PROCESS DATASET TIME: {process_duration}")
    
    return render_template('success.html')

def pathjoin(dir, filename) :
    return dir + '/' + filename

@app.route('/paginate', methods=['GET'])
def paginate() :
    page = int(request.args.get('page', 1))
    items_per_page = 4
    with open('app/data/result.json', 'rb') as f:
            data = orjson.loads(f.read())
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    if (len(data) / items_per_page) > (len(data) // items_per_page) :
        total_pages = len(data)//items_per_page + 1
    else :
        total_pages = len(data)//items_per_page
    
    paginated_data = data[start_index:end_index]
    for el in paginated_data :
        el["similarity"] = str(float(el["similarity"]) * 100)

    return render_template('pagination_template.html', data=paginated_data, current_page=page, total_pages=total_pages)