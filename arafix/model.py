from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from .config import MODEL_NAME

class AraFixModel:
    def __init__(self):
        self._model = None
        self._tokenizer = None
        
    @property
    def model(self):
        if self._model is None:
            self._model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        return self._model
    
    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        return self._tokenizer
    
    def predict(self, text):
        
        if not text:
            return None
        
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        if 'token_type_ids' in inputs:
            del inputs['token_type_ids']

        outputs = self.model.generate(**inputs, max_new_tokens=128)
        decoded_output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return decoded_output