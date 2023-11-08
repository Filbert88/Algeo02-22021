import numpy as np
import cv2

def get_vector(image: np.ndarray) -> np.ndarray:
    h_ranges = [[158.0, 180.0], [0.5, 12.5], [13.0, 20.0], [20.5, 60.0], [60.5, 95.0], [95.5, 135.0], [135.5, 147.5], [147.5, 157.5]]
    s_ranges = [[0, 50.5], [51.0, 179.0], [179.5, 255]]
    v_ranges = [[0, 50.5], [51.0, 179.0], [179.5, 255]]

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