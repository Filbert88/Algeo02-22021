import cv2
import numpy as np
import math

def get_feature_vector(image_location, h_bins, s_bins, v_bins):

    img = cv2.imread(image_location)
    height, width, depth = img.shape

    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [180, 256, 256], [0., 180., 0., 256., 0., 256.])

    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [h_bins, s_bins, v_bins], [0., 180., 0., 256., 0., 256.])

    return hist

def cosine_similarity(vec1, vec2, h_bins=-1, s_bins=-1, v_bins=-1):
    return np.sum(vec1 * vec2) / (np.sqrt(np.sum(vec1 * vec1)) * np.sqrt(np.sum(vec2 * vec2)))
    # dot_product = 0
    # a = 0
    # b = 0
    # for i in range(h_bins):
    #     for j in range(s_bins):
    #         for k in range(v_bins):
    #             dot_product += vec1[i][j][k] * vec2[i][j][k]
    #             a += vec1[i][j][k] * vec1[i][j][k]
    #             b += vec2[i][j][k] * vec2[i][j][k]
    
    # return dot_product / (math.sqrt(a) * math.sqrt(b))

if __name__ == "__main__":
    h_bins = 30
    s_bins = 30
    v_bins = 30
    vec1 = get_feature_vector("/home/azzmi/projects/Algeo02-22021/program/apples/apple01.png", h_bins, s_bins, v_bins)
    vec2 = get_feature_vector("/home/azzmi/projects/Algeo02-22021/program/apples/apple13.png", h_bins, s_bins, v_bins)

    print(cosine_similarity(vec1, vec2))
