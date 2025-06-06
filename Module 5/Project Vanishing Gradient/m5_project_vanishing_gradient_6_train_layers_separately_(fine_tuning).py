# -*- coding: utf-8 -*-
"""M5_Project_Vanishing_Gradient_6_Train_layers_separately_(fine_tuning).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pswFysFbyYbIxb9-8UyLIIbkvp1ylB4d
"""

!pip install torch torchvision matplotlib

import random
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch import nn
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.datasets import FashionMNIST

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

SEED = 42
set_seed(SEED)

train_dataset = FashionMNIST('./data',
                             train=True,
                             download=True,
                             transform=transforms.ToTensor())

test_dataset = FashionMNIST('./data',
                            train=False,
                            download=True,
                            transform=transforms.ToTensor())

train_ratio = 0.9
train_size = int(len(train_dataset) * train_ratio)
val_size = len(train_dataset) - train_size

train_subset, val_subset = random_split(train_dataset, [train_size, val_size])

# Thêm định nghĩa batch_size ở đây
batch_size = 64

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(f"Train size: {len(train_subset)}")
print(f"Validation size: {len(val_subset)}")
print(f"Test size: {len(test_dataset)}")

"""(a) Xây dựng các mô hình thành phần"""

class MLP_1layer(nn.Module):
    def __init__(self, input_dims, output_dims):
        super(MLP_1layer, self).__init__()
        self.layer1 = nn.Linear(input_dims, output_dims)

        # Khởi tạo trọng số
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=0.05)
                nn.init.constant_(module.bias, 0.0)

    def forward(self, x):
        x = nn.Flatten()(x)
        x = self.layer1(x)
        x = nn.Sigmoid()(x)
        return x

class MLP_2layers(nn.Module):
    def __init__(self, input_dims, output_dims):
        super(MLP_2layers, self).__init__()
        self.layer1 = nn.Linear(input_dims, output_dims)
        self.layer2 = nn.Linear(output_dims, output_dims)

        # Khởi tạo trọng số
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=0.05)
                nn.init.constant_(module.bias, 0.0)

    def forward(self, x):
        x = nn.Flatten()(x)
        x = self.layer1(x)
        x = nn.Sigmoid()(x)
        x = self.layer2(x)
        x = nn.Sigmoid()(x)
        return x

"""(b) Khởi tạo các module thành phần"""

# Khởi tạo các thành phần mạng
first = MLP_2layers(input_dims=784, output_dims=128)    # Mô hình đầu tiên: 2 lớp
second = MLP_2layers(input_dims=128, output_dims=128)   # Mô hình thứ hai: 2 lớp
third = MLP_2layers(input_dims=128, output_dims=128)    # Mô hình thứ ba: 2 lớp
fourth = MLP_1layer(input_dims=128, output_dims=128)    # Mô hình thứ tư: 1 lớp

# Thiết lập learning rate và hàm mất mát
lr = 1e-2
criterion = nn.CrossEntropyLoss()

"""(c) Giai đoạn 1 - Huấn luyện chỉ với thành phần đầu tiên"""

# Mô hình: Thành phần first + lớp đầu ra
model = nn.Sequential(
    first,                        # Thành phần first: MLP_2layers
    nn.Linear(128, 10)            # Lớp đầu ra: 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""(d) Giai đoạn 2 - Thêm thành phần thứ hai"""

# Cố định trọng số của thành phần first
for param in first.parameters():
    param.requires_grad = False  # Không cho phép cập nhật trọng số

# Xây dựng mô hình: Thêm thành phần second và một lớp đầu ra
model = nn.Sequential(
    first,                # Thành phần first đã được huấn luyện
    second,               # Thành phần second mới thêm vào
    nn.Linear(128, 10)    # Lớp đầu ra: chuyển 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""(e) Giai đoạn 3 - Cập nhật toàn bộ thành phần hiện có"""

# Bỏ cố định trọng số của thành phần first
for param in first.parameters():
    param.requires_grad = True  # Cho phép cập nhật trọng số

# Xây dựng mô hình: Gồm first, second và lớp đầu ra
model = nn.Sequential(
    first,                # Thành phần first
    second,               # Thành phần second
    nn.Linear(128, 10)    # Lớp đầu ra: chuyển 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""(f) Giai đoạn 4 - Thêm thành phần thứ ba"""

# Cố định trọng số của thành phần first và second
for param in first.parameters():
    param.requires_grad = False  # Giữ cố định first
for param in second.parameters():
    param.requires_grad = False  # Giữ cố định second

# Xây dựng mô hình: Thêm thành phần third và một lớp đầu ra
model = nn.Sequential(
    first,                 # Thành phần first đã huấn luyện
    second,                # Thành phần second đã huấn luyện
    third,                 # Thành phần third mới được thêm vào
    nn.Linear(128, 10)     # Lớp đầu ra: chuyển 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""(g) Giai đoạn 5 - Cập nhật toàn bộ thành phần hiện có"""

# Cho phép cập nhật trọng số của tất cả các thành phần
for param in first.parameters():
    param.requires_grad = True  # Cho phép cập nhật first
for param in second.parameters():
    param.requires_grad = True  # Cho phép cập nhật second
for param in third.parameters():
    param.requires_grad = True  # Cho phép cập nhật third

# Xây dựng mô hình: first + second + third + lớp đầu ra
model = nn.Sequential(
    first,                 # Thành phần first
    second,                # Thành phần second
    third,                 # Thành phần third
    nn.Linear(128, 10)     # Lớp đầu ra: chuyển 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""(h) Giai đoạn 6 - Thêm thành phần thứ tư"""

# Cố định trọng số của first, second, và third
for param in first.parameters():
    param.requires_grad = False  # Giữ cố định first
for param in second.parameters():
    param.requires_grad = False  # Giữ cố định second
for param in third.parameters():
    param.requires_grad = False  # Giữ cố định third

# Xây dựng mô hình: Thêm thành phần fourth và lớp đầu ra
model = nn.Sequential(
    first,                 # Thành phần first đã huấn luyện
    second,                # Thành phần second đã huấn luyện
    third,                 # Thành phần third đã huấn luyện
    fourth,                # Thành phần fourth mới được thêm vào
    nn.Linear(128, 10)     # Lớp đầu ra: chuyển 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""(i) Giai đoạn 7 - Mở khóa toàn bộ thành phần"""

# Mở khóa tất cả các thành phần để cho phép cập nhật trọng số
for param in first.parameters():
    param.requires_grad = True  # Mở khóa first
for param in second.parameters():
    param.requires_grad = True  # Mở khóa second
for param in third.parameters():
    param.requires_grad = True  # Mở khóa third
for param in fourth.parameters():
    param.requires_grad = True  # Mở khóa fourth

# Xây dựng mô hình: Kết hợp tất cả các thành phần
model = nn.Sequential(
    first,                 # Thành phần first
    second,                # Thành phần second
    third,                 # Thành phần third
    fourth,                # Thành phần fourth
    nn.Linear(128, 10)     # Lớp đầu ra: chuyển 128 -> 10 nhãn
).to(device)

# Khởi tạo optimizer và hàm mất mát
optimizer = optim.SGD(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

epochs = 100
train_loss_lst = []
train_acc_lst = []
val_loss_lst = []
val_acc_lst = []

for epoch in range(epochs):
    train_loss = 0.0
    train_acc = 0.0
    count = 0

    # Chế độ huấn luyện
    model.train()
    for X_train, y_train in train_loader:
        X_train, y_train = X_train.to(device), y_train.to(device)
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        train_acc += (torch.argmax(outputs, 1) == y_train).sum().item()
        count += len(y_train)

    train_loss /= len(train_loader)
    train_loss_lst.append(train_loss)
    train_acc /= count
    train_acc_lst.append(train_acc)

    # Chế độ đánh giá
    val_loss = 0.0
    val_acc = 0.0
    count = 0
    model.eval()
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            outputs = model(X_val)
            loss = criterion(outputs, y_val)
            val_loss += loss.item()
            val_acc += (torch.argmax(outputs, 1) == y_val).sum().item()
            count += len(y_val)

    val_loss /= len(val_loader)
    val_loss_lst.append(val_loss)
    val_acc /= count
    val_acc_lst.append(val_acc)

    # In kết quả sau mỗi epoch
    print(f"EPOCH {epoch + 1}/{epochs}, "
          f"Train_Loss: {train_loss:.4f}, Train_Acc: {train_acc:.4f}, "
          f"Validation Loss: {val_loss:.4f}, Val_Acc: {val_acc:.4f}")

"""Trực quan hóa kết quả huấn luyện"""

fig, ax = plt.subplots(2, 2, figsize=(12, 10))

# Vẽ Training Loss
ax[0, 0].plot(train_loss_lst, color='green')
ax[0, 0].set(xlabel='Epoch', ylabel='Loss')
ax[0, 0].set_title('Training Loss')

# Vẽ Validation Loss
ax[0, 1].plot(val_loss_lst, color='orange')
ax[0, 1].set(xlabel='Epoch', ylabel='Loss')
ax[0, 1].set_title('Validation Loss')

# Vẽ Training Accuracy
ax[1, 0].plot(train_acc_lst, color='green')
ax[1, 0].set(xlabel='Epoch', ylabel='Accuracy')
ax[1, 0].set_title('Training Accuracy')

# Vẽ Validation Accuracy
ax[1, 1].plot(val_acc_lst, color='orange')
ax[1, 1].set(xlabel='Epoch', ylabel='Accuracy')
ax[1, 1].set_title('Validation Accuracy')

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()

"""Đánh giá mô hình"""

test_target = []
test_predict = []

# Đặt mô hình ở chế độ đánh giá
model.eval()
with torch.no_grad():
    for X_test, y_test in test_loader:
        X_test = X_test.to(device)
        y_test = y_test.to(device)
        outputs = model(X_test)

        # Lưu lại dự đoán và nhãn thực tế
        test_predict.append(outputs.cpu())
        test_target.append(y_test.cpu())

# Ghép kết quả từ các batch thành một tensor duy nhất
test_predict = torch.cat(test_predict)
test_target = torch.cat(test_target)

# Tính toán độ chính xác
test_acc = (torch.argmax(test_predict, 1) == test_target).sum().item() / len(test_target)

# In kết quả
print('Evaluation on test set:')
print(f'Accuracy: {test_acc:.4f}')