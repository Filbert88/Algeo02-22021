from app import app
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from app import texture_cbir, color_cbir, image_processing
import numpy as np
import shutil
import zipfile
import orjson
import threading
import time
from app import create_pdf
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import mimetypes

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

@app.route('/camera_page')
def camera_page():
    return render_template('camera_page.html')

@app.route('/dataset_images/<path:filename>')
def serve_dataset_image(filename):
    return send_from_directory('data/img/dataset', filename)

@app.route('/upload_image_color', methods=['POST'])
def upload_image_color() :
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        start = time.time()
        filename = secure_filename(file.filename)
        upload_dir = app.config['UPLOAD_FOLDER']
        save_path = os.path.join(upload_dir, filename)
        shutil.rmtree(upload_dir)
        os.makedirs(upload_dir)
        file.save(save_path)
        vec = color_cbir.get_vec_from_hsv_load(save_path)
        with open('app/data/dataset_vec.json', 'rb') as f:
            dataset = orjson.loads(f.read())
        
        #HANDLE NO DATA
        if len(dataset) == 0 :
            return "<div class='errorMsg'>No Data in Dataset</div>"
        
        similar_images = []
        for data_el in dataset :
            similarity = image_processing.cosine_similarity(vec, np.fromstring(data_el["vec_color"].strip('[]'), sep=', '))
            if similarity >= 0.6 :
                similar_images.append({
                    "filename" : data_el["filename"],
                    "type" : "COLOR",
                    "file_path" : data_el["file_path"],
                    "similarity" : str(similarity),
                    "image_url": url_for('serve_dataset_image', filename=data_el["filename"])
                })
        similar_images = sorted(similar_images, key=lambda x: x["similarity"], reverse=True)
        end = time.time()
        duration = round(end - start, 2)
        
        with open('app/data/result.json', 'wb') as f:
            f.write(orjson.dumps(similar_images))

        if len(similar_images) == 0 :
            return render_template('noresult.html', result=0, duration=duration)
        return render_template('result.html', result=len(similar_images), duration=duration)

@app.route('/upload_zip', methods=['POST'])
def upload_zip() :
    time.sleep(0.5)
    if 'zipfile' not in request.files:
            print("NO FILE PART")
            return render_template('dataset_error.html')
    file = request.files['zipfile']
    if file.filename == '':
        return render_template('dataset_error.html')
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
        vec_texture = texture_cbir.get_vector_from_location(filename)
        texture = [vec_texture[0], vec_texture[1], vec_texture[2]]
        temp_data.append({
            "filename": filename.split('/')[-1],
            "file_path": filename,
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
    time.sleep(0.5)
    app.config['MAX_CONTENT_LENGTH'] = None
    uploaded_files = request.files.getlist('files[]')
    dataset_folder = 'app/data/img/dataset/'
    if os.path.exists(dataset_folder) and os.path.isdir(dataset_folder):
        shutil.rmtree(dataset_folder)
    os.makedirs(dataset_folder)

    if len(uploaded_files) == 0 :
        return render_template('dataset_error.html')

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
    if len(data) == 0 :
        return ""
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    if (len(data) / items_per_page) > (len(data) // items_per_page) :
        total_pages = len(data)//items_per_page + 1
    else :
        total_pages = len(data)//items_per_page
    
    paginated_data = data[start_index:end_index]

    for el in paginated_data :
        similarity_value = round(float(el["similarity"]), 5)
        if similarity_value % 1 > 0:
            el["similarity"] = "{:.3f}%".format(similarity_value * 100)
        else:
            el["similarity"] = "{:.0f}%".format(similarity_value * 100)

    return render_template('pagination_template.html', data=paginated_data, current_page=page, total_pages=total_pages)

@app.route('/upload_image_texture', methods=['POST'])
def upload_image_texture() :
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        start = time.time()
        filename = secure_filename(file.filename)
        upload_dir = app.config['UPLOAD_FOLDER']
        save_path = os.path.join(upload_dir, filename)
        shutil.rmtree(upload_dir)
        os.makedirs(upload_dir)
        file.save(save_path)
        vec = texture_cbir.get_vector_from_location(save_path)
        with open('app/data/dataset_vec.json', 'rb') as f:
            dataset = orjson.loads(f.read())
        
        #HANDLE NO DATA
        if len(dataset) == 0 :
            return "<div class='errorMsg'>No Data in Dataset</div>"
        
        similar_images = []
        for data_el in dataset :
            similarity = image_processing.cosine_similarity(vec, np.fromstring(data_el["vec_texture"].strip('[]'), sep=', '))
            if similarity >= 0.6 :
                similar_images.append({
                    "filename" : data_el["filename"],
                    "type" : "TEXTURE",
                    "file_path" : data_el["file_path"],
                    "similarity" : str(similarity),
                    "image_url" : url_for('serve_dataset_image', filename=data_el["filename"])
                })
        similar_images = sorted(similar_images, key=lambda x: x["similarity"], reverse=True)
        end = time.time()
        duration = round(end - start, 2)
        
        with open('app/data/result.json', 'wb') as f:
            f.write(orjson.dumps(similar_images))
        
        return render_template('result.html', result=len(similar_images), duration=duration)

@app.route('/show_loading', methods=['GET'])
def show_loading():
    return render_template('loading.html')

@app.route('/show_download_button', methods=['GET'])
def show_download_button():
    create_pdf.create_report()
    return render_template('download_report.html')

@app.route('/delete_download_button', methods=['GET'])
def delete_download_button():
    return ""

@app.route('/webscrape_popup', methods=['GET'])
def webscrape_popup():
    return render_template('scrape_popup.html')

@app.route('/scrape_url', methods=['POST'])
def submit_url():
    time.sleep(0.5)
    url = request.form['url']
    have_img = scrape_and_save_images(url)
    if have_img == 1 :
        dataset_dir = app.config["DATASET_FOLDER"]
        start_time = time.time()
        save_every_image_vec_to_json(dataset_dir)
        duration = time.time() - start_time
        print(f"PROCESS TIME: {duration}")
        return render_template('scrape_success.html', url=url)
    elif have_img == 0 :
        return render_template('scrape_no_img.html', url=url)
    else :
        return render_template('scrape_fail.html', url=url)

def scrape_and_save_images(url):
    try :
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        images = soup.find_all('img')
        if not images:
            return 0

        dataset_dir = app.config['DATASET_FOLDER']
        shutil.rmtree(dataset_dir)
        os.makedirs(dataset_dir)

        for i, img in enumerate(images):
            img_url = img.get('src')
            if not img_url:
                continue

            if not img_url.startswith('http'):
                img_url = url + img_url
            
            parsed_url = urlparse(img_url)
            query_params = parse_qs(parsed_url.query)
            if 'url' in query_params:
                img_path = query_params['url'][0]
                img_url = urlparse(url).scheme + "://" + urlparse(url).netloc + img_path

            img_response = requests.get(img_url)
            if img_response.status_code != 200:
                continue

            content_type = img_response.headers['Content-Type']
            file_extension = mimetypes.guess_extension(content_type)

            if file_extension != None :
                if file_extension in ['.jpg', '.jpeg', '.png']:
                    with open(os.path.join(dataset_dir, f'image_{i}{file_extension}'), 'wb') as file:
                        file.write(img_response.content)

        if len(os.listdir(dataset_dir)) == 0 :
            return 0
        
        return 1
    except Exception as e :
        return 2
    

@app.route('/webscrape_loading', methods=['GET'])
def webscrape_loading() :
    return render_template('scrape_loading.html')