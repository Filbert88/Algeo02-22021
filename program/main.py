from color_cbir import *

if __name__ == "__main__":
    image_1 = load_image_as_hsv("/home/azzmi/Desktop/image1.png")
    vector_1 = get_vector(image_1)


    image_2 = load_image_as_hsv("/home/azzmi/Desktop/image2.png")
    vector_2 = get_vector(image_2)

    similarity = cosine_similarity(vector_1, vector_2)
    print(similarity)