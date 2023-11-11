import numpy as np
from image_processing import load_image_as_hsv, cosine_similarity

h_ranges = np.array([[158.0, 180.0], [0, 12.5], [13.0, 20.0], [20.5, 60.0], [60.5, 95.0], [95.5, 135.0], [135.5, 147.5], [147.5, 157.5]])
s_ranges = np.array([[0, 50.5], [51.0, 179.0], [179.5, 255]])
v_ranges = np.array([[0, 50.5], [51.0, 179.0], [179.5, 255]])

def get_vector(image: np.ndarray) -> np.ndarray:
    h_masks = [(h[0] <= image[:, :, 0]) & (image[:, :, 0] <= h[1]) for h in h_ranges]
    s_masks = [(s[0] <= image[:, :, 1]) & (image[:, :, 1] <= s[1]) for s in s_ranges]
    v_masks = [(v[0] <= image[:, :, 2]) & (image[:, :, 2] <= v[1]) for v in v_ranges]

    histogram = [(hm & sm & vm) for hm in h_masks for sm in s_masks for vm in v_masks]
    
    color_vector = [np.sum(bin) for bin in histogram]

    return color_vector


# Asumsi: image_1 dan image_2 sudah diload secara HSV
def compare_from_array(image_1: np.ndarray, image_2: np.ndarray):
    vector_1 = get_vector(image_1)
    vector_2 = get_vector(image_2)
    return cosine_similarity(vector_1, vector_2)

def compare_from_vector(vector_1: np.ndarray, vector_2: np.ndarray):
    return cosine_similarity(vector_1, vector_2)

def compare_from_location(image_location_1: str, image_location_2: str) :
    image_1 = load_image_as_hsv(image_location_1)
    image_2 = load_image_as_hsv(image_location_2)
    
    vector_1 = get_vector(image_1)
    vector_2 = get_vector(image_2)
    return cosine_similarity(vector_1, vector_2)