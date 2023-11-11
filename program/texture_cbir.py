import numpy as np
import image_processing
import cv2
import os

QUANTIZATION = 256
CROPPED_DIMENSION = 300

CONTRAST_WEIGHT = 1/50
HOMOGENEITY_WEIGHT = 1
ENTROPY_WEIGHT = 1

def crop_preprocessing_to_location(image_location: str, output_file_location=None):
    image = image_processing.load_image_as_bgr(image_location)
    cropped = image[0:CROPPED_DIMENSION, 0:CROPPED_DIMENSION]
    if output_file_location == None:
        folder_location = os.path.dirname(image_location)
        file_name = os.path.splitext(image_location)[0]
        output_file_location = os.path.join(folder_location, file_name + "_cropped" + '.' + "png")
    cv2.imwrite(output_file_location, cropped)

def crop_preprocessing_to_array(image: np.ndarray):
    cropped = image[0:CROPPED_DIMENSION, 0:CROPPED_DIMENSION]
    return cropped


# Prekondisi: Gambar harus berukuran CROPPED_DIMENSION x CROPPED_DIMENSION
def get_co_occurence_matrix(image: np.ndarray) -> np.ndarray:
    all_but_first_column = image[:,1:].ravel()
    all_but_last_column = image[:,:-1].ravel()

    histogram, _, _ = np.histogram2d(all_but_last_column, all_but_first_column, bins=QUANTIZATION, range=[[0, QUANTIZATION - 1], [0, QUANTIZATION - 1]])

    histogram += np.transpose(histogram)
    sum = np.sum(histogram.ravel())
    histogram /= sum

    return histogram

def get_contrast(occurence_matrix: np.ndarray):
    return np.einsum('ij,ij->', occurence_matrix, (np.indices(occurence_matrix.shape)[0] - np.indices(occurence_matrix.shape)[1])**2)

def get_homogeneity(occurence_matrix: np.ndarray):
    return np.einsum('ij,ij->', occurence_matrix, 1 / (1 + (np.indices(occurence_matrix.shape)[0] - np.indices(occurence_matrix.shape)[1])**2))

def get_entropy(occurence_matrix: np.ndarray):
    non_zero_mask = (occurence_matrix != 0)

    log_result = occurence_matrix[non_zero_mask] * np.log(occurence_matrix[non_zero_mask])
    return -np.sum(log_result)

# Prekondisi: Gambar harus berukuran CROPPED_DIMENSION x CROPPED_DIMENSION
def get_vector_from_occurence_matrix(occurence_matrix: np.ndarray):
    contrast = get_contrast(occurence_matrix)
    homogeneity = get_homogeneity(occurence_matrix)
    entropy = get_entropy(occurence_matrix)
    return np.array([contrast * CONTRAST_WEIGHT, homogeneity * HOMOGENEITY_WEIGHT, entropy * ENTROPY_WEIGHT])

# Prekondisi: Gambar harus berukuran CROPPED_DIMENSION x CROPPED_DIMENSION
def get_vector_from_location(image_location: str):
    image = image_processing.load_image_as_hsv(image_location)
    matrix = get_co_occurence_matrix(image)
    return get_vector_from_occurence_matrix(matrix)


def compare_from_location(input_image_location: str, dataset_image_location: str):
    input_image = image_processing.load_image_as_grayscale(input_image_location)
    dataset_image = image_processing.load_image_as_grayscale(dataset_image_location)

    input_matrix = get_co_occurence_matrix(input_image)
    dataset_matrix = get_co_occurence_matrix(dataset_image)

    input_vector = get_vector_from_occurence_matrix(input_matrix)
    dataset_vector = get_vector_from_occurence_matrix(dataset_matrix)

    print("Input vector", input_vector)
    print("Dataset vector", dataset_vector)

    return image_processing.cosine_similarity(input_vector, dataset_vector)

def compare_from_array(input_image: np.ndarray, dataset_image: np.ndarray):
    input_matrix = get_co_occurence_matrix(input_image)
    dataset_matrix = get_co_occurence_matrix(dataset_image)

    input_vector = get_vector_from_occurence_matrix(input_matrix)
    dataset_vector = get_vector_from_occurence_matrix(dataset_matrix)

    return image_processing.cosine_similarity(input_vector, dataset_vector)