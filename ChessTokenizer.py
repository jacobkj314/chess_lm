from tokens import MOVES

import re

from torch import tensor

def pairs(collection):
    for i in range(0, len(collection), 2):
        yield collection[i:i+2]

class ChessTokenizer:
    def __init__(self):
        self.tokens = set(MOVES)
        
        self.id2token = {i+2 : move for i, move in enumerate(MOVES)}
        self.id2token[0] = '<' #end/padding token
        self.id2token[1] = '>' #start token
        
        self.token2id = {v:k for k, v in self.id2token.items()}
        self.token2id['<'] = 0
        self.token2id['>'] = 1


    def _encode_text(self, text):
        text = re.sub(r'[x+#]', '', text)
        text = re.sub(r'\.', ' ', text)
        tokens = re.split(r'\s+', text)
        ids = [1] + [self.token2id[token] for token in tokens if token in self.tokens] + [0]
        return ids

    def encode(self, texts):
        texts = [self._encode_text(text) for text in texts]
        lengths = [len(tokenized_text) for tokenized_text in texts]
        padding_length = max(lengths)
        texts = [text + [0 for _ in range(padding_length - len(text))] for text in texts]
        return texts

    def _decode_ids(self, ids):
        ids = [self.id2token[int(tid)] for i, tid in enumerate(ids) if not (i == 0 and tid == 1)] #remove leading start token
        text = ' '.join((' '.join([f'{i+1}.'] + pair)) for i, pair in enumerate(pairs(ids)))
        text = re.sub(r'( <)?( \d+\. < <)*$', '', text) #remove trailing end/padding tokens
        return text
    
    def decode(self, idss):
        texts = [self._decode_ids(ids) for ids in idss]
        return texts
