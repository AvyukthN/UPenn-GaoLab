import numpy as np

with open(input("file name: ")) as f:
    lines = f.read().split("\n")[:-1]

mat = np.array(list(map(lambda x: x.split("\t"), lines)))
grch38 = mat[:, 2][1:].astype(np.float32)
print(grch38.shape)
print(grch38)

hg38_32vec = np.repeat(np.load("hg38-32vec.npy"), 3).astype(np.float32)
hg38_32vec = hg38_32vec / np.sum(hg38_32vec)
print(hg38_32vec.shape)
print(hg38_32vec)

print(np.dot(grch38, hg38_32vec))
