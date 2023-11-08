import numpy as np
import cv2

def get_co_occurence_matrix(image: np.ndarray) -> np.ndarray:
    quantization = 256

    all_but_first_column = image[:,1:].ravel()
    all_but_last_column = image[:,:-1].ravel()

    hist, xedges, yedges = np.histogram2d(all_but_last_column, all_but_first_column, bins=quantization, range=[[0, quantization - 1], [0, quantization - 1]])

    return hist.astype(np.uint32)

def get_contrast(occurence_matrix: np.ndarray):
    return np.einsum('ij,ij->', occurence_matrix, (np.indices(occurence_matrix.shape)[0] - np.indices(occurence_matrix.shape)[1])**2)

def get_homogeneity(occurence_matrix: np.ndarray):
    return np.einsum('ij,ij->', occurence_matrix, 1 / (1 + (np.indices(occurence_matrix.shape)[0] - np.indices(occurence_matrix.shape)[1])**2))

def get_entropy(occurence_matrix: np.ndarray):
    non_zero_mask = (occurence_matrix != 0)

    log_result = occurence_matrix[non_zero_mask] * np.log(occurence_matrix[non_zero_mask])
    return -np.sum(log_result)

def get_vector(occurence_matrix: np.ndarray):
    return np.array([get_contrast(occurence_matrix), get_homogeneity(occurence_matrix), get_entropy(occurence_matrix)])

def load_image_as_grayscale(image_location: str) -> np.ndarray:
    return cv2.imread(image_location, cv2.IMREAD_GRAYSCALE)

def get_vector_from_image(image_location: str) :
    return get_vector(get_co_occurence_matrix(load_image_as_grayscale(image_location)))

def cosine_similarity(vec_1, vec_2):
    return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))
