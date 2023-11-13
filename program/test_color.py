import global_color_cbir
import local_color_cbir
import image_processing
import time
import json
import numpy as np

def test_resizing():
    location_1 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple02.png"
    

    # Resize lewat ini, outputnya namanya "{nama}_processed.png"
    local_color_cbir.resize_preprocessing_to_location(location_1)
    
    
    # Resize lewat ini, outputnya namanya di parameter
    local_color_cbir.resize_preprocessing_to_location(location_1, "/home/azzmi/projects/Algeo02-22021/images/apples/resized.png")

def test_spatial_without_resizing():
    location_1 = r"C:\Users\LENOVO\OneDrive\Desktop\Algeo02-22021\images\cardataset\1.jpg"
    location_2 = r"C:\Users\LENOVO\OneDrive\Desktop\Algeo02-22021\images\wood\7.jpg"

    
    image_1 = local_color_cbir.resize_preprocessing_to_array(local_color_cbir.load_image_as_hsv(location_1))
    image_2 = local_color_cbir.resize_preprocessing_to_array(local_color_cbir.load_image_as_hsv(location_2))
    # result = local_color_cbir.compare_spatially_from_location(location_1, location_2)

    result = local_color_cbir.compare_from_array(image_1, image_2)

    return result

def test_vec():
    location_1 = r"C:\Users\LENOVO\OneDrive\Desktop\Algeo02-22021\images\cardataset\1.jpg"
    location_2 = r"C:\Users\LENOVO\OneDrive\Desktop\Algeo02-22021\images\wood\7.jpg"
    vec1 = local_color_cbir.calculate_vector_from_image(location_1)
    vec2 = local_color_cbir.calculate_vector_from_image(location_2)
    data = [
        {
            "image" : location_1,
            "vec" : [vec.tolist() for vec in vec1]
        }
    ]

    with open("data.json", 'w') as json_file:
        json.dump(data, json_file)
    return local_color_cbir.calculate_average_similarity(vec1, vec2)
    

def test_spatial_with_resizing():
    location_1 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple01.png"
    location_2 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple02.png"

    output_location_1 = "/home/azzmi/projects/Algeo02-22021/program/output_1.png"
    output_location_2 = "/home/azzmi/projects/Algeo02-22021/program/output_2.png"

    local_color_cbir.resize_preprocessing_to_location(location_1, output_location_1)
    local_color_cbir.resize_preprocessing_to_location(location_2, output_location_2)

    result = local_color_cbir.compare_from_location(output_location_1, output_location_2)

    return result

def test_global():
    location_1 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple01.png"
    location_2 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple02.png"

    result = global_color_cbir.compare_from_location(location_1, location_2)
    return result


if __name__ == "__main__":
    start_time = time.time()
    similarity = test_spatial_without_resizing()
    print(f"sim1: {similarity}")
    time_taken = time.time() - start_time
    print("Time taken", time_taken)
    start_time = time.time()
    similarity = test_vec()
    print(f"sim2: {similarity}")
    time_taken = time.time() - start_time
    print("Time taken", time_taken)
