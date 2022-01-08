import os
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data

from datasets import DisflQA
from models import LSTM_ED, WordEmbedding
from utils import train, test, save, load
from losses import CELossShift

# --- Hyperparameters ---
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# os.environ["OMP_NUM_THREADS"] = "1"
# torch.set_num_threads(1)
# torch.manual_seed(seed=0)

if __name__ == '__main__':
    train_dataset = DisflQA(
        file_name='Datasets/Disfl-QA/train.json', 
        vocab_file='Datasets/Disfl-QA/spm.model', 
        max_len=1000, return_len=False)

    val_dataset = DisflQA(
        file_name='Datasets/Disfl-QA/dev.json', 
        vocab_file='Datasets/Disfl-QA/spm.model', 
        max_len=1000, return_len=False)

    train_loader = data.DataLoader(train_dataset, batch_size=8, num_workers=2, shuffle=True)
    val_loader = data.DataLoader(train_dataset, batch_size=8, num_workers=2)

    vocab_emb = WordEmbedding(len(train_dataset.vocab), 128)
    model = LSTM_ED(vocab_emb, emb_dim=128, hid_dim=128, n_layers=1, dropout=0.0).cuda()
    optimizer = optim.AdamW(model.parameters(), lr=3e-4)
    criterion = CELossShift(ignore_index=3)
    scaler = torch.cuda.amp.GradScaler()

    n_epochs = 10
    for i in range(n_epochs):
        train(train_loader, model, optimizer, criterion, device='cuda', scaler=scaler, kw_src=['input','output'])