import numpy as np


def get_signature(cosmic_filepath: str):
    with open(cosmic_filepath) as f:
        lines = f.read().split("\n")[:-1]

    mat = np.array(list(map(lambda x: x.split("\t"), lines)))
    grch38_sig = mat[:, 2][1:].astype(np.float32)

    return grch38_sig

    '''
    print(grch38.shape)
    print(grch38)
    '''

    hg38_32vec = np.repeat(np.load("hg38-32vec.npy"), 3).astype(np.float32)

hg38_32vec = hg38_32vec / np.sum(hg38_32vec)
print(hg38_32vec.shape)
print(hg38_32vec)

print(np.dot(grch38, hg38_32vec))
