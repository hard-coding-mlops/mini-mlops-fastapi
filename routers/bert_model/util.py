import torch
import pandas as pd
import gluonnlp as nlp
import numpy as np
from torch.utils.data import Dataset, DataLoader
import sys
sys.path.append('C:/Users/admin/mini-mlops-fastapi')

# 이제 모듈을 import할 수 있어야 함
from database.conn import db_dependency
from routers.data_management.index import preprocessed_articles_to_dataframe

# 데이터를 한번에 불러오면 메모리에 부담이 되므로 하나씩불러 오도록 Dataset과 DataLoader를 사용한다
class BERTDataset(Dataset):
    # 생성자, 데이터를 전처리 하는 부분
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len, pad, pair):
        print("BERTDataset Start")
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, vocab=vocab, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    # idx(인덱스)에 해당하는 입출력 데이터를 반환한다.
    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    # 데이터셋의 총 길이를 반환하는 부분
    def __len__(self):
        return (len(self.labels))

async def load_data(db:db_dependency):
    print("load_data Start")

    result = await preprocessed_articles_to_dataframe(db)
    
    preprocess_news_articles = pd.DataFrame(result, columns=['original_article_id', 'category_no', 'formatted_text'])

    # CSV 파일 읽기
    #preprocess_news_articles = pd.read_csv("news_articles_202311211411.csv", encoding='utf-8')
 
    data_list = []
    for q, label in zip(preprocess_news_articles['formatted_text'], preprocess_news_articles['category_no']) :
        data = []
        data.append(q)
        data.append(str(label))

        data_list.append(data)
    print("load_data End")
    return data_list

def split_data(self,data_list):
    print("split_data Start")
    #train & test 데이터로 나누기
    from sklearn.model_selection import train_test_split
    data_train, data_test = train_test_split(data_list, test_size=0.25, random_state=0)
    print("split_data End")
    return data_train, data_test

