import torch
from torch import Tensor

import transformers
from transformers import BertConfig, BertForMaskedLM
from torch.utils.data import Dataset, DataLoader
import pandas

from ChessTokenizer import ChessTokenizer



config = BertConfig(vocab_size=5438+2)
model = BertForMaskedLM(config).cuda()

games = pandas.read_csv('Modern.pgn')
games = games['Moves'].tolist()
dataloader = DataLoader(games, batch_size=8, shuffle=True)

tokenizer = ChessTokenizer()

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

loss_fn = torch.nn.CrossEntropyLoss(ignore_index=0)




model.train()
for epoch in range(10):
    for batch in dataloader:

        batch = Tensor(tokenizer.encode(batch)).long().cuda()
        optimizer.zero_grad()
        input_ids = batch[:, :-1]
        labels = batch[:, 1:]


        outputs = model(input_ids=input_ids) # # #, labels=labels)
        logits = outputs.logits.reshape(-1, outputs.logits.shape[-1]) # # # 
        labels = labels.reshape(-1) # # # 
        loss = loss_fn(logits, labels) # # # loss = outputs.loss
        loss.backward()
        optimizer.step()

    print('Epoch {}: loss = {}'.format(epoch+1, loss.item()))