import numpy as np
import cv2
import os
from image_processing import load_image_as_hsv, resize_from_location, resize_from_array, split, cosine_similarity

RESIZE_DIMENSION = 150
BLOCK_DIMENSION = 3

def resize_preprocessing_to_location(image_location: str, output_file_location=None):
    resized = resize_from_location(image_location, RESIZE_DIMENSION, RESIZE_DIMENSION)
    if output_file_location == None:
        folder_location = os.path.dirname(image_location)
        file_name = os.path.splitext(image_location)[0]
        output_file_location = os.path.join(folder_location, file_name + "_resized" + '.' + "png")
    cv2.imwrite(output_file_location, resized)

def resize_preprocessing_to_array(image: np.ndarray):
    resized = resize_from_array(image, RESIZE_DIMENSION, RESIZE_DIMENSION)
    return resized

h_ranges_spatial = np.array([[0, 12.5], [13.0, 20.0], [20.5, 60.0], [60.5, 95.0], [95.5, 135.0], [135.5, 148], [148.5, 157.5], [158.0, 180.0]])
s_ranges_spatial = np.array([[0, 255]])
v_ranges_spatial = np.array([[0, 255]])

def get_vector(image: np.ndarray) -> np.ndarray:
    h = round(np.mean(image[:,:,0])) 
    s = round(np.mean(image[:,:,1]))  
    v = round(np.mean(image[:,:,2]))  
    
    h_index = np.where((h >= h_ranges_spatial[:, 0]) & (h <= h_ranges_spatial[:, 1]))[0]
    s_index = np.where((s >= s_ranges_spatial[:, 0]) & (s <= s_ranges_spatial[:, 1]))[0]
    v_index = np.where((v >= v_ranges_spatial[:, 0]) & (v <= v_ranges_spatial[:, 1]))[0]
    
    vector = np.zeros(72)
    vector[9 * h_index + 3 * s_index + v_index] = 1
    return vector


# Prekondisi: input image dan dan dataset image punya ukuran sama yaitu RESIZE_DIMENSION x RESIZE_DIMENSION.
# Kalau belum memenuhi prekondisi, harus panggil resize_preprocessing dulu.
def compare_from_location(input_image_location: str, dataset_image_location: str):
    input_image = load_image_as_hsv(input_image_location)
    dataset_image = load_image_as_hsv(dataset_image_location)

    input_submatrices = split(input_image, BLOCK_DIMENSION, BLOCK_DIMENSION)
    dataset_submatrices = split(dataset_image, BLOCK_DIMENSION, BLOCK_DIMENSION)

    return sum([cosine_similarity(get_vector(matrix_1), get_vector(matrix_2)) for matrix_1, matrix_2 in zip(input_submatrices, dataset_submatrices)]) / ((RESIZE_DIMENSION / BLOCK_DIMENSION) ** 2)


# Prekondisi: input image dan dan dataset image punya ukuran sama yaitu RESIZED_DIMENDION x RESIZED_DIMENDION.
# Kalau belum memenuhi prekondisi, harus panggil resize_preprocessing dulu.
def compare_from_array(input_image: np.ndarray, dataset_image: np.ndarray):
    input_submatrices = split(input_image, BLOCK_DIMENSION, BLOCK_DIMENSION)
    dataset_submatrices = split(dataset_image, BLOCK_DIMENSION, BLOCK_DIMENSION)

    return sum([cosine_similarity(get_vector(matrix_1), get_vector(matrix_2)) for matrix_1, matrix_2 in zip(input_submatrices, dataset_submatrices)]) / ((RESIZE_DIMENSION / BLOCK_DIMENSION) ** 2)