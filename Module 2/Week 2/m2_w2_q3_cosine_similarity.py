# -*- coding: utf-8 -*-
"""M2_W2_Q3_Cosine_Similarity.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14lNbwwvRO6nRAV3DQZov7XHETqE82Y1p
"""

import numpy as np
from numpy import dot
from numpy.linalg import norm

def computeDotProduct(v1, v2):
    return dot(v1, v2)

def computeVectorLength(v):
    return norm(v)

def compute_cosine(v1, v2):
    cos_sim = computeDotProduct(v1, v2) / (computeVectorLength(v1) * computeVectorLength(v2))
    return cos_sim

x = np.array([1, 2, 3, 4])
y = np.array([1, 0, 3, 0])
result = compute_cosine(x,y)
print(round(result, 3))