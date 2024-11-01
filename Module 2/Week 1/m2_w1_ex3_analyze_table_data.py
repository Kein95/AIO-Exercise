# -*- coding: utf-8 -*-
"""M2_W1_Ex3_Analyze_Table_Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11mTgXbPMcJx2m4ymuuoQVcrUoOC36Rbl
"""

# Download data
! gdown 1iA0WmVfW88HyJvTBSQDI5vesf-pgKabq

import pandas as pd
df = pd . read_csv ('/content/advertising.csv')

data = df . to_numpy ()
df

max_value = df['Sales'].max()
max_index = df['Sales'].idxmax()
print("Max:", max_value, "- Index:", max_index)

average_tv = df['TV'].mean()
print("The average value of the TV column is:", round(average_tv, 1))

count = (df['Sales'] >= 20).sum()
print("Number of records with Sales >= 20:", count)

average_radio = df['Radio'][df['Sales'] >= 15].mean()
print("The average value of the Radio column is:", round(average_radio, 1))

sum_sales = df[df['Newspaper'] > df['Newspaper'].mean()]['Sales'].sum()
print("Sum of Sales where Newspaper > average:", round(sum_sales, 1))

#Gọi giá trị trung bình của cột Sales (average_sales) là A
A = df['Sales'].mean()
#Tạo ra mảng mới scores chứa các giá trị Good, Average và Bad sao cho: nếu giá trị hiện tại > A => giá trị trong mảng mới là Good, < A thì sẽ là Bad và = A sẽ là Average.
scores = ['Good' if x > A else 'Bad' if x < A else 'Average' for x in df['Sales']]
print(scores[7:10])

#Gọi giá trị trên cột Sales gần nhất với giá trị trung bình cũng chính cột Sales (closest_to_average) là A
mean_sales = df['Sales'].mean()
closest_to_mean = df.iloc[(df['Sales'] - mean_sales).abs().argsort()[:1]]
A = closest_to_mean['Sales'].values[0]
scores = ['Good' if x > A else 'Average' if x == A else 'Bad' for x in df['Sales']]
print(scores[7:10])