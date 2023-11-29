import argparse

import torch
import torch.nn as nn
import gluonnlp as nlp

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel

from torch.utils.data import DataLoader
from util import load_data,split_data
from util import BERTDataset
from model import BERTClassifier

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

from trainer import Trainer

from database.conn import db_dependency

def define_argparser():
    print("define_argparser Start")
    p = argparse.ArgumentParser()

    #p.add_argument('--model_fn', required=True)
    p.add_argument('--gpu_id', type=int, default=0 if torch.cuda.is_available() else -1)
    #해당 길이를 초과하는 단어에 대해서는 bert가 학습하지 않는다
    p.add_argument('--max_len', type=int, default=512)
    p.add_argument('--batch_size', type=int, default=8)
    p.add_argument('--num_epochs', type=int, default=5)
    #warmup 비율만큼의 학습 스텝 동안 learning rate를 증가
    p.add_argument('--warmup_ratio', type=float, default=0.1)
    p.add_argument('--max_grad_norm', type=int, default=1)
    # 몇 번의 배치마다 로그를 출력할지 나타냅니다
    p.add_argument('--log_interval', type=int, default=200)
    p.add_argument('--learning_rate', type=float, default=5e-5)

    config = p.parse_args()

    print("define_argparser End")
    return config

def main(config, db:db_dependency):
    # Set device based on user defined configuration.
    device = torch.device('cpu') if config.gpu_id < 0 else torch.device('cuda:%d' % config.gpu_id)

    data_list = load_data(db)

    # from_pretrained : 웹에서 모델을 다운로드
    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1', sp_model_kwargs={'nbest_size': -1, 'alpha': 0.6, 'enable_sampling': True})
    bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')
    # 토큰화
    tok = tokenizer.tokenize
    print("max_len = ", config.max_len)
    data_list = BERTDataset(data_list, 0, 1, tok, vocab, config.max_len, True, False)

    data_train, data_test = split_data(data_list)

    train_dataloader = DataLoader(data_train, batch_size=config.batch_size, num_workers=5)
    test_dataloader = DataLoader(data_test, batch_size=config.batch_size, num_workers=5)

    # dr_rate : 모델 정의 시에 사용되는 드롭아웃 비율
    model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

    #optimizer와 schedule 설정
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]

    optimizer = torch.optim.AdamW(optimizer_grouped_parameters, lr=config.learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    trainer = Trainer(model, optimizer, loss_fn, device)
    trainer.train(train_dataloader, test_dataloader, config=config)

###############################################################################################

if __name__ == '__main__':
    config = define_argparser()
    main(config, db_dependency)