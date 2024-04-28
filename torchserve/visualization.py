from model import BERTMulticlassToxicityClassifier
from transformers import AutoModel, BertTokenizer
from torchviz import make_dot
import torch

bert = AutoModel.from_pretrained('cointegrated/rubert-tiny')
tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny')

model = BERTMulticlassToxicityClassifier(bert)

text = 'Привет, мои котики!'
tokens = tokenizer.encode_plus(
            text,
            max_length = 50,
            add_special_tokens=True,
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',
)

model.load_state_dict(torch.load('saved_weights.pt', map_location=torch.device('cpu')))

input_ids = tokens['input_ids'].to('cpu')
attention_mask = tokens['attention_mask'].to('cpu')


output = model(input_ids, attention_mask)

make_dot(
    var=output,
    params=dict(list(model.named_parameters()))
).render(format='png')