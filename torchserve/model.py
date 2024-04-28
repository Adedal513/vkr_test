import torch.nn as nn
import torch
from transformers import AutoModel, BertTokenizer


bert = AutoModel.from_pretrained('cointegrated/rubert-tiny')
tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny')


class BERTMulticlassToxicityClassifier(nn.Module):
    def __init__(self, bert):
        super(BERTMulticlassToxicityClassifier, self).__init__()
        self.bert = bert # Оригинальная BERT-модель
        self.dropout = nn.Dropout(0.1) # Dropout для предотвращения переобучения
        self.relu1 = nn.ReLU() # Нелинейный слой
        self.fc1 = nn.Linear(312,64)
        self.relu2 = nn.ReLU() # Нелинейный слой
        self.fc2 = nn.Linear(64, 4)
    
    def forward(self, sent_id, mask):
        _, cls_hs = self.bert(sent_id, attention_mask = mask, return_dict = False)
        x = self.dropout(cls_hs)
        x = self.relu1(x)
        x = self.fc1(x)
        x = self.relu2(x)
        x = self.fc2(x)
        
        return x
