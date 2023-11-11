import texture_cbir
import time


def test_get_vector():
    location_1 = "/home/azzmi/projects/Algeo02-22021/images/misc/car.png"
    
    vector_1 = texture_cbir.get_vector_from_location(location_1)
    print(vector_1)


def test_compare():
    # Ini tes nya harus pakai gambar tekstur, bukan gambar asal 
    location_1 = "/home/azzmi/projects/Algeo02-22021/images/texture/14.png"
    location_2 = "/home/azzmi/projects/Algeo02-22021/images/texture/16.png"

    result = texture_cbir.compare_from_location(location_1, location_2)
    return result

def test_compare_from_dataset():
    folder_location = "/home/azzmi/projects/Algeo02-22021/images/texture/"
    input_image = 4
    input_location = folder_location + f"{input_image}.png"

    best_similarity = -1
    best_name = 1
    for i in range(1, 21):
        if i == input_image:
            continue

        file_location = folder_location + f"{i}.png"
        similarity = texture_cbir.compare_from_location(input_location, file_location)
        if similarity > best_similarity:
            best_name = i
            best_similarity = similarity
    
    print(best_name)

if __name__ == "__main__":
    start_time = time.time()
    
    test_compare_from_dataset()

    time_taken = time.time() - start_time
    print("Time taken", time_taken)

# def test_get_entropy(occurence_matrix: np.ndarray):
#     result = 0
#     for i in range(256):
#         for j in range(256):
#             if occurence_matrix[i, j] == 0:
#                 continue

#             result -= occurence_matrix[i, j] * math.log(occurence_matrix[i, j])

#     return result

# def test_get_homogeneity(occurence_matrix: np.ndarray):
#     result = 0
#     for i in range(256):
#         for j in range(256):
#             result += occurence_matrix[i, j] / (1 + (i - j) ** 2)
#     return result

# def test_get_contrast(occurence_matrix: np.ndarray):
#     result = 0
#     for i in range(256):
#         for j in range(256):
#             result += occurence_matrix[i, j] * ((i - j) ** 2)
#     return result
