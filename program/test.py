import numpy as np

def split(array, nrows, ncols):

    if array.shape[0] % nrows != 0:
        array = array[:-(array.shape[0] % nrows)]
    if array.shape[1] % ncols != 0:
        array = array[:, :-(array.shape[1] % ncols)]

    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))


array = np.array([
    [1, 1, 2, 2],
    [3, 3, 4, 4],
    [5, 5, 6, 6],
    [7, 7, 8, 8]])

array += np.transpose(array)
sum = np.sum(array)
print(array, sum)
print(array/sum)

# array = np.array([
#     [1, 1, 2, 2, 0],
#     [3, 3, 4, 4, 0],
#     [5, 5, 6, 6, 0],
#     [7, 7, 8, 8, 0]])

# nrows = 2
# ncols = 2

# print(array.shape[0])
# array = array[:-(0)]

# array = array[:-(array.shape[0] % nrows)]
# print(array)
# array = array[:, :-(array.shape[1] % ncols)]
# print(array)
# print(split(array, 2, 2))


# A, B =  split(array, 4, 2)

# print(A)
# print(B)