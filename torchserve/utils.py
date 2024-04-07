import torch
from transformers import AutoModel, BertTokenizer

def predict(text: str, model: torch.nn.Module, tokenizer: BertTokenizer):
    tokens = tokenizer.encode_plus(
        text,
        max_length = 50,
        add_special_tokens=True,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
    )
    
    input_ids = tokens['input_ids'].to('cpu')
    attention_mask = tokens['attention_mask'].to('cpu')
    with torch.no_grad():
        output = model(input_ids, attention_mask)
    
    _, prediction = torch.max(output, dim=1)
    print(f'Review text: {text}')
    print(f'Sentiment  : {torch.nn.functional.softmax(output)}')