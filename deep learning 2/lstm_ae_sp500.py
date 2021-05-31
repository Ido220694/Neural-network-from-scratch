import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torch.optim as op
import torch.nn as nn
import pandas as pd
from matplotlib import pyplot as plt
import math
from torchvision import datasets, transforms
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale


transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
mnist_tarin = datasets.LSTM_AE_MNIST("./data", train = True, download = True, transform =transform)
mnist_test = list(datasets.LSTM_AE_MNIST("./data", train = False, download = True, transform =transform))



class LSTM_AE_MNIST(Dataset):
    def __init__(self, df):
        self.our_list = list(df.index)
        x = minmax_scale(df, axis=1)
        x = x - x.mean(axis=1, keepdims=True) + 0.5
        self.data = []
        self.tags = []
        for i in x:
            self.data.extend([torch.tensor(i[:-1]).unsqueeze(1)])
            self.tags.extend([torch.tensor(i[1:]).unsqueeze(1)])


    def length(self):
        return len(self.data)

    def object(self, index):
        return self.our_list[index], self.tags[index] ,self.data[index]


class AE(nn.Moudle):
    def __init__(self, hidden_layer_size, n_inputs):
        super(AE, self).__init__()
        self.encoder_LSTM = nn.LSTM(1, hidden_layer_size, batch_first=True)
        self.decoder_LSTM = nn.LSTM(hidden_layer_size, hidden_layer_size, batch_first=True)
        self.hidden_layer_size = hidden_layer_size
        self.func = nn.Linear(hidden_layer_size,1)
        self.forecast = nn.Linear(hidden_layer_size, 1)

    def forward(self, x_t):
        x, (z,y) = self.encoder_LSTM(x_t)
        z = z.reshape(-1, 1, self.hidden_layer_size).repeat(1, x_t.size(1) , 1)
        h_temp , s =self.decoder_LSTM(z)
        return self.func(h_temp), self.forecast(h_temp)

    # def grid_search(self, values, data):
    #     hidden_state_size = [32, 64, 128, 256]
    #     learning_rates =[0.0001, 0.001, 0.01 , 0.1]
    #     gradient_clipping = [0.01, 0.1, 0.5, 1]
    #
    #     min_loss = math.inf
    #     min_losses = []
    #     min_train =[]
    #     chosen_lr =0
    #     chosen_clipping = 0
    #     chosen_hidden =0
    #     index =1
    #
    #     for clip in gradient_clipping:
    #         for learn in learning_rates:
    #             for hidden in hidden_state_size:
    #                 optim = op.adam(AE(hidden).cuda().parameters(), lr=learn)
    #                 tr_los, v_los = training(optim, hidden, clip, data, values)
    #                 if min_loss > v_los[-1]:
    #                     chosen_clipping = clip
    #                     chosen_lr = learn
    #                     chosen_hidden = hidden
    #                     min_loss = v_los[-1]
    #                     min_losses = v_los
    #                     min_train = tr_los
    #
    #     return [chosen_clipping, chosen_lr, chosen_hidden, min_loss, min_losses, min_train]
