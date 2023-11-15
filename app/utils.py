from app import texture_cbir, local_color_cbir
import os
import zipfile
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import mimetypes
import threading
import orjson
import shutil
from app import app

def pathjoin(dir, filename) :
    return dir + '/' + filename

def process_file_chunk(file_chunk, result_list):
    temp_data = []
    for filename in file_chunk:
        vec_color = local_color_cbir.get_block_vector_from_image(filename)
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
    
    num_threads = 6
    chunk_size = max(1, total_files // num_threads)

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