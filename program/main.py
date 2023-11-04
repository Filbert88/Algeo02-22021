import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def get_global_color_vector(image_location):

    img = cv2.imread(image_location)
    height, width, depth = img.shape

    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_ranges = [(0, 59), (60, 119), (120, 180)]
    s_ranges = [(0, 84), (85, 169), (170, 255)]
    v_ranges = [(0, 84), (85, 169), (170, 255)]

    r_masks = [(r[0] <= image[:, :, 0]) & (image[:, :, 0] <= r[1]) for r in h_ranges]
    g_masks = [(g[0] <= image[:, :, 1]) & (image[:, :, 1] <= g[1]) for g in s_ranges]
    b_masks = [(b[0] <= image[:, :, 2]) & (image[:, :, 2] <= b[1]) for b in v_ranges]

    partitions = [(rm & gm & bm) for rm in r_masks for gm in g_masks for bm in b_masks]
    
    color_vector = [np.sum(partition) for partition in partitions]
    
    return color_vector


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
    h_bins = 20
    s_bins = 5
    v_bins = 5
    vec1 = get_global_color_vector("/home/azzmi/projects/Algeo02-22021/program/rainbow/pic01.png", h_bins, s_bins, v_bins)
    # vec1 = get_global_color_vector("/home/azzmi/projects/Algeo02-22021/program/apples/apple01.png", h_bins, s_bins, v_bins)
    # vec2 = get_feature_vector("/home/azzmi/projects/Algeo02-22021/program/apples/apple09.png", h_bins, s_bins, v_bins)
    # print(np.sum(vec1))
    # print(cosine_similarity(vec1, vec2))
