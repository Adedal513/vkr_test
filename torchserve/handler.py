# Input/Output
import io
import json

# Сам торч, логи, доступ к ОС
import torch
import logging
import os

from model import BERTMulticlassToxicityClassifier
from transformers import BertTokenizer, AutoModel

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)

class ModelHandler(BaseHandler):

    TOKENIZER_CHECKPOINT = 'cointegrated/rubert-tiny-toxicity'

    def __init__(self):
        self.mapping = {
            0: 'non-toxic',
            1: 'insult',
            2: 'threat',
            3: 'obscenity'
        }

    def initialize(self, ctx):

        self.manifest = ctx.manifest

        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        # Get additional parts of the model
        bert = AutoModel.from_pretrained(self.TOKENIZER_CHECKPOINT)
        self.tokenizer = BertTokenizer.from_pretrained(self.TOKENIZER_CHECKPOINT)

        # Get the model itself
        self.model = BERTMulticlassToxicityClassifier(bert)

        # Load model up

        model_file = self.manifest['model']['serializedFile']
        model_path = os.path.join(model_dir, model_file)

        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        logger.debug('Transformer model from path {0} loaded successfully'.format(model_dir+''))

        self.initialized = True
    
    def preprocess(self, data):
        text = data[0].get('text')
        
        if text is None:
            raw_data = data[0].get('body')
            text = raw_data.get('text')
        logger.error('FUCK FUCK FUCCCCCKK')
        logger.error(data)
        logger.error(text)
        tokens = self.tokenizer.encode_plus(
            text,
            max_length = 50,
            add_special_tokens=True,
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return tokens

    def inference(self, tokens, *args, **kwargs):
        input_ids = tokens['input_ids'].to('cpu')
        attention_mask = tokens['attention_mask'].to('cpu')
        with torch.no_grad():
            output = self.model(input_ids, attention_mask)

        logging.info('Probabilities successfully created.')

        fin_data = torch.nn.functional.softmax(output)[0].tolist()

        return fin_data

    def postprocess(self, outputs: list):
        return [{self.mapping[i]: outputs[i] for i in range(len(outputs))}]