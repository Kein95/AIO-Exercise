# -*- coding: utf-8 -*-
"""M1_W3_Q1_Softmax.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KEdlJpF8tt0ZnV8FeVxzzwM1njJmG--m
"""

import torch
import torch.nn.functional as F

# softmax function
def softmax(x):
    return torch.exp(x) / torch.sum(torch.exp(x), dim=0)

# stable softmax function
def softmax_stable(x):
    c = torch.max(x)
    exps = torch.exp(x - c)
    return exps / torch.sum(exps, dim=0)

# Example
data = torch.tensor([1.0, 2.0, 3.0])

# softmax
output_softmax = softmax(data)
print("Standard Softmax Output:", output_softmax)

# stable softmax
output_softmax_stable = softmax_stable(data)
print("Stable Softmax Output:", output_softmax_stable)

"""trắc nghiệm"""

import torch
import torch.nn.functional as F

# softmax function
def softmax(x):
    return torch.exp(x) / torch.sum(torch.exp(x), dim=0)

# stable softmax function
def softmax_stable(x):
    c = torch.max(x)
    exps = torch.exp(x - c)
    return exps / torch.sum(exps, dim=0)

# Example 1
data = torch.tensor([1.0, 2.0, 3.0])

# softmax
output_softmax = softmax(data)
print("Standard Softmax Output:", output_softmax)

# stable softmax
output_softmax_stable = softmax_stable(data)
print("Stable Softmax Output:", output_softmax_stable)

# Example 2
data = torch.tensor([5.0, 2.0, 4.0])

# softmax
output_softmax = softmax(data)
print("Standard Softmax Output:", output_softmax)

# stable softmax
output_softmax_stable = softmax_stable(data)
print("Stable Softmax Output:", output_softmax_stable)

# Example 3
data = torch.tensor([1 , 2 , 300000000])

# softmax
output_softmax = softmax(data)
print("Standard Softmax Output:", output_softmax)

# stable softmax
output_softmax_stable = softmax_stable(data)
print("Stable Softmax Output:", output_softmax_stable)

# Example 4
import torch
import torch.nn as nn

class SoftmaxStable(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        x_max = torch.max(x, dim=0, keepdims=True)
        x_exp = torch.exp(x - x_max.values)
        partition = x_exp.sum(0, keepdims=True)
        return x_exp / partition

data = torch.Tensor([1, 2, 3])

softmax_stable = SoftmaxStable()

output = softmax_stable(data)

print("Stable Softmax Output:", output)

assert round(output[-1].item(), 2) == 0.67