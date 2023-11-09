import numpy as np
import cv2

h_ranges = [[158.0, 180.0], [0, 12.5], [13.0, 20.0], [20.5, 60.0], [60.5, 95.0], [95.5, 135.0], [135.5, 147.5], [147.5, 157.5]]
s_ranges = [[0, 50.5], [51.0, 179.0], [179.5, 255]]
v_ranges = [[0, 50.5], [51.0, 179.0], [179.5, 255]]

def get_vector(image: np.ndarray) -> np.ndarray:
    h_masks = [(h[0] <= image[:, :, 0]) & (image[:, :, 0] <= h[1]) for h in h_ranges]
    s_masks = [(s[0] <= image[:, :, 1]) & (image[:, :, 1] <= s[1]) for s in s_ranges]
    v_masks = [(v[0] <= image[:, :, 2]) & (image[:, :, 2] <= v[1]) for v in v_ranges]

    histogram = [(hm & sm & vm) for hm in h_masks for sm in s_masks for vm in v_masks]
    
    color_vector = [np.sum(bin) for bin in histogram]

    return color_vector

def load_image_as_hsv(image_location: str) -> np.ndarray:
    return cv2.cvtColor(cv2.imread(image_location), cv2.COLOR_BGR2HSV)

def cosine_similarity(vec_1, vec_2):
    return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))


def split(array, nrows, ncols):

    if array.shape[0] % nrows != 0:
        array = array[:-(array.shape[0] % nrows)]
    if array.shape[1] % ncols != 0:
        array = array[:, :-(array.shape[1] % ncols)]

    r, h, _ = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols, 3)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols, 3))


def compare_spatially(image_location_1: str, image_location_2: str):
    image_1 = load_image_as_hsv(image_location_1)
    image_2 = load_image_as_hsv(image_location_2)

    sub_matrices_1 = split(image_1, 3, 3)
    sub_matrices_2 = split(image_2, 3, 3)

    print(sub_matrices_1[0].shape)
    print(sub_matrices_2.shape)

    import time
    current_time = time.time()
    
    
    vectors_1 = np.array([get_vector(matrix) for matrix in sub_matrices_1])
    vectors_2 = np.array([get_vector(matrix) for matrix in sub_matrices_2])

    current_time = time.time()
    similarity = 0
    for i in range(len(vectors_1)):
        similarity += cosine_similarity(vectors_1[i], vectors_2[i])
    print("Time:", time.time() - current_time)
    return similarity