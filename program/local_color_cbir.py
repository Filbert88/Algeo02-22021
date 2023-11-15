import numpy as np
import cv2
from image_processing import cosine_similarity
import time

RESIZE_DIMENSION = 150
BLOCK_DIMENSION = 3

def resize_preprocessing_to_array(image: np.ndarray):
    resized = resize_from_array(image, RESIZE_DIMENSION, RESIZE_DIMENSION)
    return resized

def resize_from_array(image: np.ndarray, width, height) -> np.ndarray:
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)


def cosine_similarity(vec_1, vec_2):
    return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))

def split(array, nrows, ncols):
    if array.shape[0] % nrows != 0:
        array = array[:-(array.shape[0] % nrows)]
    if array.shape[1] % ncols != 0:
        array = array[:, :-(array.shape[1] % ncols)]

    _, h, _ = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols, 3)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols, 3))

def get_vector(image: np.ndarray) -> np.ndarray:
    h_ranges = np.array([[0, 12.5], [13.0, 20.0], [20.5, 60.0], [60.5, 95.0], [95.5, 135.0], [135.5, 147.5], [147.5, 157.5], [158.0, 180.0]])
    s_ranges = np.array([[0, 50.5], [51.0, 179.0], [179.5, 255]])
    v_ranges = np.array([[0, 50.5], [51.0, 179.0], [179.5, 255]])

    h_masks = [(h[0] <= image[:, :, 0]) & (image[:, :, 0] <= h[1]) for h in h_ranges]
    s_masks = [(s[0] <= image[:, :, 1]) & (image[:, :, 1] <= s[1]) for s in s_ranges]
    v_masks = [(v[0] <= image[:, :, 2]) & (image[:, :, 2] <= v[1]) for v in v_ranges]

    histogram = [(hm & sm & vm) for hm in h_masks for sm in s_masks for vm in v_masks]

    color_vector = [np.sum(bin) for bin in histogram]

    return color_vector


def rgb_to_hsv_vectorized(bgr_image):
    rgb_image = bgr_image[..., ::-1]

    rgb_image = rgb_image.astype('float32') / 255.0

    c_max = np.max(rgb_image, axis=-1)
    c_min = np.min(rgb_image, axis=-1)
    delta = c_max - c_min

    hsv_image = np.zeros_like(rgb_image)

    mask = delta > 0
    idx = (rgb_image[..., 0] == c_max) & mask
    hsv_image[..., 0][idx] = (60 * (rgb_image[..., 1][idx] - rgb_image[..., 2][idx]) / delta[idx] + 360) % 360
    idx = (rgb_image[..., 1] == c_max) & mask
    hsv_image[..., 0][idx] = (60 * (rgb_image[..., 2][idx] - rgb_image[..., 0][idx]) / delta[idx] + 120) % 360
    idx = (rgb_image[..., 2] == c_max) & mask
    hsv_image[..., 0][idx] = (60 * (rgb_image[..., 0][idx] - rgb_image[..., 1][idx]) / delta[idx] + 240) % 360

    delta = np.nan_to_num(delta)
    c_max = np.nan_to_num(c_max)

    threshold = 1e-10

    hsv_image[..., 1] = np.where(c_max > threshold, delta / np.maximum(c_max, threshold), 0)

    hsv_image[..., 2] = c_max

    hsv_image[..., 0] /= 2
    hsv_image[..., 1] *= 255.0
    hsv_image[..., 2] *= 255.0

    return hsv_image.astype('uint8')

def load_image_as_hsv(image_location: str) -> np.ndarray:
    bgr_image = cv2.imread(image_location)
    hsv_image = rgb_to_hsv_vectorized(bgr_image)
    return hsv_image

def split_image_and_compute_vectors(image: np.ndarray) -> list:
    image = resize_preprocessing_to_array(image)
    block_vectors = []

    # Calculate the dimensions of each block
    block_height = image.shape[0] // 3
    block_width = image.shape[1] // 3

    for i in range(3):
        for j in range(3):
            # Extract the block from the image
            block = image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width]

            # Calculate the color histogram vector for the block
            vector = get_vector(block)

            # Append the vector to the list of block vectors
            block_vectors.append(vector)

    return np.array(block_vectors)


def calculate_average_similarity(input_vectors: list, dataset_vectors: list) -> float:
    start = time.time()
    similarities = [cosine_similarity(v1, v2) for v1, v2 in zip(input_vectors, dataset_vectors)]
    average_similarity = sum(similarities) / len(similarities)
    end = time.time()
    print(f"time: {end - start}")
    return average_similarity

# Prekondisi: input image dan dan dataset image punya ukuran sama yaitu RESIZED_DIMENDION x RESIZED_DIMENDION.
# Kalau belum memenuhi prekondisi, harus panggil resize_preprocessing dulu.
def compare_from_array(input_image: np.ndarray, dataset_image: np.ndarray):
    input_submatrices = split(input_image, BLOCK_DIMENSION, BLOCK_DIMENSION)
    dataset_submatrices = split(dataset_image, BLOCK_DIMENSION, BLOCK_DIMENSION)

    return sum([cosine_similarity(get_vector(matrix_1), get_vector(matrix_2)) for matrix_1, matrix_2 in zip(input_submatrices, dataset_submatrices)]) / ((RESIZE_DIMENSION / BLOCK_DIMENSION) ** 2)

def cosine_similarity(vec_1, vec_2):
    return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))