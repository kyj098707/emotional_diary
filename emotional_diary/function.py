import torch
from torch import nn
from torch.utils.data import Dataset
from transformers import AutoModel


class EmotionalClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.klue = AutoModel.from_pretrained('klue/roberta-small') # from transformers package

        self.fc1 = nn.Linear(768, 32)
        self.relu = nn.ReLU()
        self.fear_clf = nn.Linear(32,1)
        self.disgust_clf = nn.Linear(32,1)
        self.surprise_clf = nn.Linear(32,1)
        self.happiness_clf = nn.Linear(32,1)
        self.sadness_clf = nn.Linear(32,1)
        self.angry_clf = nn.Linear(32,1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids, attention_mask):
        # input_ids : token's id / attention_mask : make a model to focus on which token
        klue_out = self.klue(input_ids= input_ids, attention_mask = attention_mask)[0][:,0]
        x = self.fc1(klue_out)
        x = self.relu(x)
        fear_output = self.fear_clf(x)
        fear_output = self.sigmoid(fear_output)
        disgust_output = self.disgust_clf(x)
        disgust_output = self.sigmoid(disgust_output)
        surprise_output = self.surprise_clf(x)
        surprise_output = self.sigmoid(surprise_output)
        happiness_output = self.happiness_clf(x)
        happiness_output = self.sigmoid(happiness_output)
        sadness_output = self.sadness_clf(x)
        sadness_output = self.sigmoid(sadness_output)
        angry_output = self.angry_clf(x)
        angry_output = self.sigmoid(angry_output)
        return fear_output, disgust_output, surprise_output, happiness_output, sadness_output, angry_output

