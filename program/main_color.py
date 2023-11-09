from color_cbir import *

def compare_global_color(location_1, location_2):
    image_1 = load_image_as_hsv(location_1)
    vector_1 = get_vector(image_1)


    image_2 = load_image_as_hsv(location_2)
    vector_2 = get_vector(image_2)

    similarity = cosine_similarity(vector_1, vector_2)
    return similarity



if __name__ == "__main__":
    l = []
    for i in range(50):
        num = i + 1
        location = f"/home/azzmi/projects/Algeo02-22021/program/plastic/{num}.jpg"
        l.append(get_vector(load_image_as_hsv(location)))
    
    input_image = 43
    similarity = cosine_similarity(l[input_image - 1], l[1])
    output_image = 2

    for i in range(50):
        if i + 1 == input_image:
            continue
        current_similarity = cosine_similarity(l[input_image - 1], l[i])
        print(i+1, current_similarity)
        if current_similarity > similarity:
            similarity = current_similarity
            output_image = i + 1
        
    print(output_image, similarity)
    