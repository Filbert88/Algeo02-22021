from texture_cbir import *
import color_cbir
import time


if __name__ == "__main__":
    input_num = 42
    input = load_image_as_grayscale(f"/home/azzmi/projects/Algeo02-22021/images/plastic/{input_num}.jpg")
    input_vector = get_vector(get_co_occurence_matrix(input))

    current_time = time.time()

    output_num = -1
    output_distance = 1e15

    for i in range(1):
        file_num = i + 1
        if file_num == input_num:
            continue
        file_name = f"/home/azzmi/projects/Algeo02-22021/images/plastic/{file_num}.jpg"
        image = load_image_as_grayscale(file_name)
            
        matrix = get_co_occurence_matrix(image)
        vector = get_vector(matrix)

        distance = euclidian_distance(input_vector, vector)

        if distance < output_distance:
            output_distance = distance
            output_num = file_num
    print(time.time() - current_time)
    print(output_num, output_distance)