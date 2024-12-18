# -*- coding: utf-8 -*-
"""ÔN LUYỆN CHO MODUL 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j3ovaULkcx38Dh9EFAqFOCToYIBYbYAc

# Day 32: Basic Python - Bayes Theory
https://drive.google.com/file/d/1rxg44UO1Qp4s9novMxF4XA3_a-V0YuiG/view
"""

import numpy as np

# Số lượng sản phẩm A và B
n_A = 60
n_B = 40

# Tổng số sản phẩm
total_products = n_A + n_B

# Tính xác suất tiên nghiệm của mỗi lớp
P_A = n_A / total_products
P_B = n_B / total_products

# In kết quả
print(f"Xác suất tiên nghiệm của Sản phẩm A (P(A)) là: {P_A:.2f}")
print(f"Xác suất tiên nghiệm của Sản phẩm B (P(B)) là: {P_B:.2f}")

# Số lượng sản phẩm với các đặc trưng trong lớp A
red_small_A = 20
red_large_A = 10
green_small_A = 15
green_large_A = 15

# Số lượng sản phẩm với các đặc trưng trong lớp B
red_small_B = 10
red_large_B = 5
green_small_B = 10
green_large_B = 15

# Tổng số sản phẩm trong từng lớp
total_A = 60
total_B = 40

# Xác suất điều kiện trong lớp A
P_red_small_given_A = red_small_A / total_A
P_red_large_given_A = red_large_A / total_A
P_green_small_given_A = green_small_A / total_A
P_green_large_given_A = green_large_A / total_A

# Xác suất điều kiện trong lớp B
P_red_small_given_B = red_small_B / total_B
P_red_large_given_B = red_large_B / total_B
P_green_small_given_B = green_small_B / total_B
P_green_large_given_B = green_large_B / total_B

# Kết quả
print(f"P(Đỏ và Nhỏ | A) = {P_red_small_given_A:.3f}")
print(f"P(Đỏ và Lớn | A) = {P_red_large_given_A:.3f}")
print(f"P(Xanh và Nhỏ | A) = {P_green_small_given_A:.3f}")
print(f"P(Xanh và Lớn | A) = {P_green_large_given_A:.3f}")

print(f"P(Đỏ và Nhỏ | B) = {P_red_small_given_B:.3f}")
print(f"P(Đỏ và Lớn | B) = {P_red_large_given_B:.3f}")
print(f"P(Xanh và Nhỏ | B) = {P_green_small_given_B:.3f}")
print(f"P(Xanh và Lớn | B) = {P_green_large_given_B:.3f}")

# Đã tính từ bước trước
P_A = 0.6
P_B = 0.4

P_red_small_given_A = 0.333
P_red_small_given_B = 0.250

# Tính xác suất sau cùng cho lớp A và B
P_A_given_red_small = P_red_small_given_A * P_A
P_B_given_red_small = P_red_small_given_B * P_B

# Kết quả
print(f"P(A | Đỏ và Nhỏ) = {P_A_given_red_small:.4f}")
print(f"P(B | Đỏ và Nhỏ) = {P_B_given_red_small:.4f}")