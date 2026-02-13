import numpy as np

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# if __name__ == '__main__':
    vec1 = [1, 0, 0]
    vec2 = [1, 1, 0]
    print('COSINE SIMILARITY:', cosine_similarity(vec1, vec2))