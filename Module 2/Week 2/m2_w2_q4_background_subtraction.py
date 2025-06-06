# -*- coding: utf-8 -*-
"""M2_W2_Q4_Background_subtraction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t2AtxuijPzvGSLBwDss3a0ynh0evCXIf
"""

#(a) Resize các ảnh đầu vào về cùng kích thước:

import numpy as np
from google.colab.patches import cv2_imshow
import cv2

bg1_image = cv2.imread('/content/GreenBackground.png', 1)
bg1_image = cv2.resize(bg1_image, (678, 381))

ob_image = cv2.imread('/content/Object.png', 1)
ob_image = cv2.resize(ob_image, (678, 381))

bg2_image = cv2.imread('/content/NewBackground.jpg', 1)
bg2_image = cv2.resize(bg2_image, (678, 381))

#(b) Xây dựng hàm compute_difference():

def computeDifference(bg_img, input_img):
    difference_three_channel = cv2.absdiff(bg_img, input_img)
    difference_single_channel = np.sum(difference_three_channel, axis=2) / 3.0
    difference_single_channel = difference_single_channel.astype('uint8')

    return difference_single_channel

# đoạn code bên dưới để hiển thị kết quả (hình 2) của hàm compute_difference() như sau:

difference_single_channel = computeDifference(bg1_image, ob_image)
cv2_imshow(difference_single_channel)

#(c) Xây dựng hàm compute_binary_mask():

def computeBinaryMask(difference_single_channel):
    difference_binary = np.where(difference_single_channel >= 15, 255, 0)
    difference_binary = np.stack((difference_binary,)*3, axis=-1)
    return difference_binary

# đoạn code bên dưới để hiển thị kết quả (hình 3) của hàm compute_binary_mask() như sau:

binary_mask = computeBinaryMask(difference_single_channel)
cv2_imshow(binary_mask)

#(d) Xây dựng hàm replace_background():

def replaceBackGround(bg1_image, bg2_image, ob_image):
    difference_single_channel = computeDifference(bg1_image,ob_image)
    binary_mask = computeBinaryMask(difference_single_channel)

    output = np.where(binary_mask==255, ob_image, bg2_image)

    return output

output = replaceBackGround(bg1_image, bg2_image, ob_image)

cv2_imshow(output)