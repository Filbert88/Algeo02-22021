import numpy as np
import color_cbir
import cv2


import time
cur_time = time.time()

location_1 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple01.png" # "/home/azzmi/projects/Algeo02-22021/images/apples/apple01.png"
location_2 = "/home/azzmi/projects/Algeo02-22021/images/apples/apple02.png"

#"/home/azzmi/projects/Algeo02-22021/images/misc/darkbrown.png"
# image = color_cbir.load_image_as_hsv(location)
# vector = color_cbir.get_vector(image)


result = color_cbir.compare_spatially(location_1, location_2)

print(result)
print("Time taken", time.time() - cur_time)
# cv2.imshow("Resized image", resized)
# print(resized.shape)
# cv2.waitKey(0)

# print(vector)

