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



def resize(image_location: str, width, height) -> np.ndarray:
    img = cv2.imread(image_location, cv2.IMREAD_UNCHANGED)
    return cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

def resize(image: np.ndarray, width, height) -> np.ndarray:
    return cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)


h_ranges_spatial = np.array([[0, 12.5], [13.0, 20.0], [20.5, 60.0], [60.5, 95.0], [95.5, 135.0], [135.5, 148], [148.5, 157.5], [158.0, 180.0]])
s_ranges_spatial = np.array([[0, 50.5], [51.0, 179.0], [179.5, 255]])
v_ranges_spatial = np.array([[0, 50.5], [51.0, 179.0], [179.5, 255]])
# s_ranges_spatial = np.array([[0, 180], [181, 255]])
# v_ranges_spatial = np.array([[0, 180], [181, 255]])
# s_ranges_spatial = np.array([[0, 255]])
# v_ranges_spatial = np.array([[0, 255]])

def get_vector_spatial(image: np.ndarray) -> np.ndarray:
    # h_masks = [(h[0] <= image[:, :, 0]) & (image[:, :, 0] <= h[1]) for h in h_ranges_spatial]
    
    # color_vector = [np.sum((hm)) for hm in h_masks]

    # return color_vector

    h = round(image[:, :, 0].mean())
    s = round(image[:, :, 1].mean())
    v = round(image[:, :, 2].mean())
    # print(h,s,v)
    h_index = np.where((h >= h_ranges_spatial[:, 0]) & (h <= h_ranges_spatial[:, 1]))[0]
    s_index = np.where((s >= s_ranges_spatial[:, 0]) & (s <= s_ranges_spatial[:, 1]))[0]
    v_index = np.where((v >= v_ranges_spatial[:, 0]) & (v <= v_ranges_spatial[:, 1]))[0]


    vector = np.zeros(72)
    vector[9 * h_index + 3 * s_index + v_index] = 1
    return vector

def compare_spatially(input_image_location: str, dataset_image_location: str):
    input_image = load_image_as_hsv(input_image_location)
    dataset_image = load_image_as_hsv(dataset_image_location)

    input_image = resize(input_image, 201, 201)
    dataset_image = resize(dataset_image, 201, 201)

    input_submatrices = split(input_image, 3, 3)
    dataset_submatrices = split(dataset_image, 3, 3)

    return sum([cosine_similarity(get_vector_spatial(matrix_1), get_vector_spatial(matrix_2)) for matrix_1, matrix_2 in zip(input_submatrices, dataset_submatrices)])