import torch
import pickle

from transformers import BertConfig, BertForMaskedLM
config = BertConfig(vocab_size=5438+2)
model = BertForMaskedLM(config).cuda()
state_dict = pickle.load(open('chess.sd', 'rb'))
model.load_state_dict(state_dict)

from ChessTokenizer import ChessTokenizer
tokenizer = ChessTokenizer()

def move(game_so_far):
    input_ids = [tokenizer.encode([game_so_far])[0][:-1]]

    with torch.no_grad():
        outputs = model(torch.tensor(input_ids).long().cuda())
        return tokenizer.decode(torch.argmax(outputs.logits, dim=-1))[0]
    
game = ''
print('Ready for your move')
while (game := game + ' ' + input()) != 'END':
    print(game := move(game))