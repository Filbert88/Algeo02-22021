import numpy as np
import cv2

def load_image_as_grayscale(image_location: str) -> np.ndarray:
    bgr_image = cv2.imread(image_location)

    if bgr_image is None:
        raise FileNotFoundError(f"No image found at {image_location}")

    weights = np.array([0.114, 0.587, 0.299])
    grayscale_image = np.dot(bgr_image, weights)
    return grayscale_image.astype('uint8')

def resize_from_location(image_location: str, width, height) -> np.ndarray:
    img = cv2.imread(image_location, cv2.IMREAD_UNCHANGED)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

def resize_from_array(image: np.ndarray, width, height) -> np.ndarray:
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def cosine_similarity(vec_1, vec_2):
    return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))

def euclidian_distance(vec_1, vec_2):
    return np.linalg.norm(vec_2 - vec_1)