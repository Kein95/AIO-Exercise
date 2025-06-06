# -*- coding: utf-8 -*-
"""M9-Project-TGIG-Text-To-Image-Conditional-Flow-Matching.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bX6W_ZDG7WW71LmO6z5nHwRb9TRYuDCZ

## **Dataset**
"""

!pip install -q datasets torchcfm

from datasets import load_dataset

ds = load_dataset("wanhin/naruto-captions", split="train")

import torch
from sentence_transformers import SentenceTransformer

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)
text_encoder = SentenceTransformer(
    "all-mpnet-base-v2"
).to(device)

ds["text"][0]

ds["image"][0]

ds["image"][0].save("text_to_image.png", format="PNG")

from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

preprocessed_image = transform(ds["image"][0])
preprocessed_image.shape

ds["text"][0]

embed_text = text_encoder.encode(ds["text"][:2], convert_to_tensor=True)

embed_text.shape

from torch.utils.data import Dataset, DataLoader

class CFMDataset(Dataset):
    def __init__(self, dataset, transform, text_encoder, device):
        self.dataset = dataset
        self.transform = transform
        self.text_encoder = text_encoder
        self.device = device
        self.images = dataset["image"]
        self.captions = dataset["text"]
        self.embed_captions = text_encoder.encode(
            self.captions, convert_to_tensor=True, device=self.device
        )

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        # get a image
        image = self.images[idx]
        image = self.transform(image)

        # get a text
        caption = self.captions[idx]
        caption_embedding = self.embed_captions[idx]

        return {
            "image": image,
            "caption": caption,
            "caption_embedding": caption_embedding,
        }

train_ds = CFMDataset(ds, transform, text_encoder, device)
train_loader = DataLoader(train_ds, batch_size=256, shuffle=True)

"""## **Model**"""

import math
import torch.nn as nn
from torchcfm.models.unet import UNetModel

def timestep_embedding(timesteps, dim, max_period=10000):
    """Create sinusoidal timestep embeddings.

    :param timesteps: a 1-D Tensor of N indices, one per batch element. These may be fractional.
    :param dim: the dimension of the output.
    :param max_period: controls the minimum frequency of the embeddings.
    :return: an [N x dim] Tensor of positional embeddings.
    """
    half = dim // 2
    freqs = torch.exp(
        -math.log(max_period)
        * torch.arange(start=0, end=half, dtype=torch.float32, device=timesteps.device)
        / half
    )
    args = timesteps[:, None].float() * freqs[None]
    embedding = torch.cat([torch.cos(args), torch.sin(args)], dim=-1)
    if dim % 2:
        embedding = torch.cat([embedding, torch.zeros_like(embedding[:, :1])], dim=-1)
    return embedding

class UNetModelWithTextEmbedding(UNetModel):
    def __init__(self, dim, num_channels, num_res_blocks, embedding_dim, *args, **kwargs):
        super().__init__(dim, num_channels, num_res_blocks, *args, **kwargs)

        self.embedding_layer = nn.Linear(embedding_dim, num_channels*4)
        self.fc = nn.Linear(num_channels*8, num_channels*4)

    def forward(self, t, x, text_embeddings=None):
        """Apply the model to an input batch, incorporating text embeddings."""
        timesteps = t

        while timesteps.dim() > 1:
            timesteps = timesteps[:, 0]
        if timesteps.dim() == 0:
            timesteps = timesteps.repeat(x.shape[0])

        hs = []
        emb = self.time_embed(
            timestep_embedding(timesteps, self.model_channels)
        )

        if text_embeddings is not None:
            text_embedded = self.embedding_layer(text_embeddings)

            # ⭐️ Sửa lỗi: ép cả emb và text_embedded về 2D để cat đúng
            if emb.dim() > 2:
                emb = emb.view(emb.size(0), -1)
            if text_embedded.dim() > 2:
                text_embedded = text_embedded.view(text_embedded.size(0), -1)

            emb = torch.cat([emb, text_embedded], dim=1) # 128*2
            emb = self.fc(emb)

        h = x.type(self.dtype)
        for module in self.input_blocks:
            h = module(h, emb)
            hs.append(h)
        h = self.middle_block(h, emb)
        for module in self.output_blocks:
            h = torch.cat([h, hs.pop()], dim=1)
            h = module(h, emb)
        h = h.type(x.dtype)
        return self.out(h)

"""## **Training**"""

model = UNetModelWithTextEmbedding(
    dim=(3, 64, 64), num_channels=32, num_res_blocks=1, embedding_dim=768
).to(device)
optimizer = torch.optim.Adam(model.parameters())

from tqdm import tqdm

n_epochs = 2000 #thay 20000 về 2000
for epoch in tqdm(range(n_epochs)):
    losses = []
    for batch in train_loader:
        optimizer.zero_grad()
        x1 = batch["image"].to(device)
        text_embeddings = batch["caption_embedding"].to(device)

        x0 = torch.randn_like(x1).to(device)

        t = torch.rand(x0.shape[0], 1, 1, 1).to(device)

        xt = t * x1 + (1 - t) * x0
        ut = x1 - x0

        t = t.squeeze()

        vt = model(t, xt, text_embeddings=text_embeddings)

        loss = torch.mean(((vt - ut) ** 2))

        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    avg_loss = sum(losses) / len(losses)
    if (epoch + 1) % 500 == 0:
        print(f"Epoch [{epoch+1}/{n_epochs}], Loss: {avg_loss:.4f}")

"""## **Inference**"""

sample = next(iter(train_ds))

color_image_tensor = sample["image"].unsqueeze(0).to(device)
text_embedding = sample["caption_embedding"].unsqueeze(0).to(device)

model.eval()
def euler_method(model, text_embedding, t_steps, dt, noise):
    y = noise
    y_values = [y]
    with torch.no_grad():
        for t in t_steps[1:]:
            t = t.reshape(-1, )
            dy = model(
                t.to(device), y,
                text_embeddings=text_embedding
            )
            y = y + dy * dt
            y_values.append(y)
    return torch.stack(y_values)

# Initial random image and class (optional)
noise = torch.randn((3, 64, 64), device=device).unsqueeze(0)
text_embedding = text_embeddings.unsqueeze(0).to(device)

# Time parameters
t_steps = torch.linspace(0, 1, 100, device=device)
dt = t_steps[1] - t_steps[0]

# Solve the ODE using Euler method
results = euler_method(model, text_embedding, t_steps, dt, noise)

import matplotlib.pyplot as plt
from torchvision.transforms import ToPILImage
from torchvision.utils import make_grid

grid = make_grid(
    color_image_tensor[0].clip(-1, 1), value_range=(-1, 1), padding=0, nrow=10
)
img = ToPILImage()(grid)
plt.imshow(img)
plt.show()