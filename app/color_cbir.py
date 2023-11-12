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

    if bgr_image is None:
        raise FileNotFoundError(f"No image found at {image_location}")

    hsv_image = rgb_to_hsv_vectorized(bgr_image)
    return hsv_image

def get_vec_from_hsv_load(image_location: str) -> np.ndarray:
    return get_vector(load_image_as_hsv(image_location))

def cosine_similarity(vec1, vec2, h_bins=-1, s_bins=-1, v_bins=-1):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))