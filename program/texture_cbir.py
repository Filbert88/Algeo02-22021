import numpy as np
import cv2
import math

def get_co_occurence_matrix(image: np.ndarray) -> np.ndarray:
    quantization = 256

    all_but_first_column = image[:,1:].ravel()
    all_but_last_column = image[:,:-1].ravel()

    hist, xedges, yedges = np.histogram2d(all_but_last_column, all_but_first_column, bins=quantization, range=[[0, quantization - 1], [0, quantization - 1]])

    hist += np.transpose(hist)
    sum = np.sum(hist.ravel())
    hist /= sum
    return hist

def get_contrast(occurence_matrix: np.ndarray):
    return np.einsum('ij,ij->', occurence_matrix, (np.indices(occurence_matrix.shape)[0] - np.indices(occurence_matrix.shape)[1])**2)

def get_homogeneity(occurence_matrix: np.ndarray):
    return np.einsum('ij,ij->', occurence_matrix, 1 / (1 + (np.indices(occurence_matrix.shape)[0] - np.indices(occurence_matrix.shape)[1])**2))

def get_entropy(occurence_matrix: np.ndarray):
    non_zero_mask = (occurence_matrix != 0)

    log_result = occurence_matrix[non_zero_mask] * np.log(occurence_matrix[non_zero_mask])
    return -np.sum(log_result)

# def test_get_entropy(occurence_matrix: np.ndarray):
#     result = 0
#     for i in range(256):
#         for j in range(256):
#             if occurence_matrix[i, j] == 0:
#                 continue

#             result -= occurence_matrix[i, j] * math.log(occurence_matrix[i, j])

#     return result

# def test_get_homogeneity(occurence_matrix: np.ndarray):
#     result = 0
#     for i in range(256):
#         for j in range(256):
#             result += occurence_matrix[i, j] / (1 + (i - j) ** 2)
#     return result

# def test_get_contrast(occurence_matrix: np.ndarray):
#     result = 0
#     for i in range(256):
#         for j in range(256):
#             result += occurence_matrix[i, j] * ((i - j) ** 2)
#     return result

def get_vector(occurence_matrix: np.ndarray):
    # contrast = test_get_contrast(occurence_matrix)
    # homogeneity = test_get_homogeneity(occurence_matrix)
    # entropy = test_get_entropy(occurence_matrix)
    contrast = get_contrast(occurence_matrix)
    homogeneity = get_homogeneity(occurence_matrix)
    entropy = get_entropy(occurence_matrix)
    return np.array([contrast, homogeneity, entropy])

def load_image_as_grayscale(image_location: str) -> np.ndarray:
    return cv2.imread(image_location, cv2.IMREAD_GRAYSCALE)

def euclidian_distance(vec_1, vec_2):
    return np.linalg.norm(vec_2 - vec_1)
