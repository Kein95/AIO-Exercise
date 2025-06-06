# -*- coding: utf-8 -*-
"""M6_W1_2_Cassava_Leaf_Disease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wogmJnmC6n9rHvFpxaECPNwnKPDxOjb0
"""

# Download and unzip the dataset
!wget --no-check-certificate https://storage.googleapis.com/emcassavadata/cassavaleafdata.zip \
    -O /content/cassavaleafdata.zip
!unzip /content/cassavaleafdata.zip

# Import necessary libraries
import os
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.utils.data as data

import torchvision.transforms as transforms
import torchvision.datasets as datasets

from torchsummary import summary
import matplotlib.pyplot as plt
from PIL import Image

# Tạo các thư mục cần thiết
for path in data_paths.values():
    os.makedirs(path, exist_ok=True)

print("Directories created successfully!")

# Định nghĩa cấu trúc thư mục
data_paths = {
    'train': './train',
    'valid': './validation',
    'test': './test'
}

# Tạo dữ liệu mẫu
for key, path in data_paths.items():
    for class_name in ['class1', 'class2']:  # Hai lớp: class1, class2
        class_path = os.path.join(path, class_name)
        os.makedirs(class_path, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
        for i in range(5):  # Tạo 5 ảnh mẫu cho mỗi lớp
            img = Image.fromarray((np.random.rand(150, 150, 3) * 255).astype('uint8'))
            img.save(os.path.join(class_path, f'image_{i}.jpg'))

print("Sample data structure created successfully!")

# Define data paths
data_paths = {
    'train': './train',
    'valid': './validation',
    'test': './test'
}

# Function to load an image from a given path
def loader(path):
    return Image.open(path)

# Image size for resizing
img_size = 150

# Define transformations for the data
train_transforms = transforms.Compose([
    transforms.Resize((img_size, img_size)),
    transforms.ToTensor(),
])

# Load datasets with ImageFolder
train_data = datasets.ImageFolder(
    root=data_paths['train'],
    loader=loader,
    transform=train_transforms
)

valid_data = datasets.ImageFolder(
    root=data_paths['valid'],
    transform=train_transforms
)

test_data = datasets.ImageFolder(
    root=data_paths['test'],
    transform=train_transforms
)

class LeNetClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(
            in_channels=3, out_channels=6, kernel_size=5, padding='same'
        )
        self.avgpool1 = nn.AvgPool2d(kernel_size=2)
        self.conv2 = nn.Conv2d(
            in_channels=6, out_channels=16, kernel_size=5
        )
        self.avgpool2 = nn.AvgPool2d(kernel_size=2)
        self.flatten = nn.Flatten()
        self.fc_1 = nn.Linear(16 * 35 * 35, 120)
        self.fc_2 = nn.Linear(120, 84)
        self.fc_3 = nn.Linear(84, num_classes)

    def forward(self, inputs):
        outputs = self.conv1(inputs)
        outputs = self.avgpool1(outputs)
        outputs = F.relu(outputs)
        outputs = self.conv2(outputs)
        outputs = self.avgpool2(outputs)
        outputs = F.relu(outputs)
        outputs = self.flatten(outputs)
        outputs = self.fc_1(outputs)
        outputs = self.fc_2(outputs)
        outputs = self.fc_3(outputs)
        return outputs

# Training function
def train(model, optimizer, criterion, train_dataloader, device, epoch=0, log_interval=50):
    model.train()
    total_acc, total_count = 0, 0
    losses = []
    start_time = time.time()

    for idx, (inputs, labels) in enumerate(train_dataloader):
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        # Forward pass
        predictions = model(inputs)

        # Compute loss
        loss = criterion(predictions, labels)
        losses.append(loss.item())

        # Backward pass
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
        optimizer.step()

        total_acc += (predictions.argmax(1) == labels).sum().item()
        total_count += labels.size(0)

        if idx % log_interval == 0 and idx > 0:
            elapsed = time.time() - start_time
            print(
                f"| epoch {epoch:3d} | {idx:5d}/{len(train_dataloader):5d} batches "
                f"| accuracy {total_acc / total_count:8.3f}"
            )
            total_acc, total_count = 0, 0
            start_time = time.time()

    epoch_acc = total_acc / total_count
    epoch_loss = sum(losses) / len(losses)
    return epoch_acc, epoch_loss


# Evaluation function
def evaluate(model, criterion, valid_dataloader):
    model.eval()
    total_acc, total_count = 0, 0
    losses = []

    with torch.no_grad():
        for idx, (inputs, labels) in enumerate(valid_dataloader):
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Forward pass
            predictions = model(inputs)

            # Compute loss
            loss = criterion(predictions, labels)
            losses.append(loss.item())

            total_acc += (predictions.argmax(1) == labels).sum().item()
            total_count += labels.size(0)

    epoch_acc = total_acc / total_count
    epoch_loss = sum(losses) / len(losses)
    return epoch_acc, epoch_loss

import time

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Define data paths
data_paths = {
    'train': './train',
    'valid': './validation',
    'test': './test'
}

# Define transformations
train_transforms = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
])

# Load datasets
train_data = datasets.ImageFolder(
    root=data_paths['train'],
    transform=train_transforms
)

valid_data = datasets.ImageFolder(
    root=data_paths['valid'],
    transform=train_transforms
)

# Create DataLoaders
BATCH_SIZE = 32

train_dataloader = DataLoader(
    train_data,
    batch_size=BATCH_SIZE,
    shuffle=True
)

valid_dataloader = DataLoader(
    valid_data,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Ensure the save directory exists
if not os.path.exists(save_model):
    os.makedirs(save_model)

# Number of classes in the dataset
num_classes = len(train_data.classes)

# Set the device for computation
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize the model
lenet_model = LeNetClassifier(num_classes)
lenet_model.to(device)

# Loss function and optimizer
criterion = torch.nn.CrossEntropyLoss()
learning_rate = 2e-4
optimizer = optim.Adam(lenet_model.parameters(), lr=learning_rate)

# Training configuration
num_epochs = 10
save_model = './model'

# Lists to store training and evaluation metrics
train_accs, train_losses = [], []
eval_accs, eval_losses = [], []
best_loss_eval = float('inf')  # Initialize to a large value

# Training loop
for epoch in range(1, num_epochs + 1):
    epoch_start_time = time.time()

    # Training
    train_acc, train_loss = train(
        lenet_model, optimizer, criterion, train_dataloader, device, epoch, log_interval=10
    )
    train_accs.append(train_acc)
    train_losses.append(train_loss)

    # Evaluation
    eval_acc, eval_loss = evaluate(lenet_model, criterion, valid_dataloader)
    eval_accs.append(eval_acc)
    eval_losses.append(eval_loss)

    # Save the best model
    if eval_loss < best_loss_eval:
        torch.save(lenet_model.state_dict(), save_model + '/lenet_model.pt')
        best_loss_eval = eval_loss

    # Print loss and accuracy at the end of the epoch
    print("-" * 59)
    print(
        f"| End of epoch {epoch:3d} | Time: {time.time() - epoch_start_time:5.2f}s | "
        f"Train Accuracy {train_acc:8.3f} | Train Loss {train_loss:8.3f} "
        f"| Valid Accuracy {eval_acc:8.3f} | Valid Loss {eval_loss:8.3f} "
    )
    print("-" * 59)

# Load the best model
lenet_model.load_state_dict(torch.load(save_model + '/lenet_model.pt'))
lenet_model.eval()

# Define transformations for the test dataset
test_transforms = transforms.Compose([
    transforms.Resize((150, 150)),  # Kích thước ảnh, đảm bảo phù hợp với mô hình
    transforms.ToTensor(),
])

# Load the test dataset
test_data = datasets.ImageFolder(
    root=data_paths['test'],  # Đường dẫn thư mục test
    transform=test_transforms
)

# Create DataLoader for the test data
BATCH_SIZE = 32  # Hoặc bất kỳ giá trị nào bạn muốn
test_dataloader = DataLoader(
    test_data,
    batch_size=BATCH_SIZE,
    shuffle=False  # Không cần xáo trộn dữ liệu trong tập test
)

# Evaluate the model on the test data
test_acc, test_loss = evaluate(lenet_model, criterion, test_dataloader)

# Print test accuracy and loss
print(f"Test Accuracy: {test_acc:.3f}")
print(f"Test Loss: {test_loss:.3f}")