import numpy as np
import cv2

def rgb_to_hsv(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    
    c_max = max(r, max(g, b))
    c_min = min(r, min(g, b))

    # max_b_g = b
    # if g > max_b_g:
    #     max_b_g = g
    # min_b_g = b + g - max_b_g

    # c_max = r
    # if max_b_g > c_max:
    #     c_max = max_b_g

    # c_min = r
    # if c_min > min_b_g:
    #     c_min = min_b_g

    delta = c_max - c_min
    
    # Hue
    if delta == 0:
        h = 0
    elif c_max == r:
        h = 60 * ((g - b) / delta % 6)
    elif c_max == g:
        h = 60 * ((b - r) / delta + 2)
    elif c_max == b:
        h = 60 * ((r - g) / delta + 4)
    h = (h + 360) % 360
    h /= 2

    # Saturation
    if c_max == 0:
        s = 0
    else:
        s = delta / c_max
    s *= 255

    # Value
    v = c_max
    v *= 255

    return np.array([h, s, v])

def rgb_to_grayscale(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b

def load_image_as_bgr(image_location: str):
    return cv2.imread(image_location)

def load_image_as_hsv(image_location: str) -> np.ndarray:
    image = load_image_as_bgr(image_location)
    # result = np.array([[rgb_to_hsv(bgr[2], bgr[1], bgr[0]) for bgr in row] for row in image])
    result = cv2.cvtColor(cv2.imread(image_location), cv2.COLOR_BGR2HSV)
    return result

def load_image_as_grayscale(image_location: str) -> np.ndarray:
    image = load_image_as_bgr(image_location)
    # result = np.array([rgb_to_grayscale(bgr[2], bgr[1], bgr[0]) for bgr in row] for row in image)
    result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return result

def resize_from_location(image_location: str, width, height) -> np.ndarray:
    img = cv2.imread(image_location, cv2.IMREAD_UNCHANGED)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

def resize_from_array(image: np.ndarray, width, height) -> np.ndarray:
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def split(array, nrows, ncols):
    if array.shape[0] % nrows != 0:
        array = array[:-(array.shape[0] % nrows)]
    if array.shape[1] % ncols != 0:
        array = array[:, :-(array.shape[1] % ncols)]

    _, h, _ = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols, 3)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols, 3))


def cosine_similarity(vec_1, vec_2):
    return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))

def euclidian_distance(vec_1, vec_2):
    return np.linalg.norm(vec_2 - vec_1)