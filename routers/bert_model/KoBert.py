# import torch
# from torch import nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torch.utils.data import Dataset, DataLoader
# import gluonnlp as nlp
# import numpy as np
import pandas as pd
# from tqdm import tqdm, tqdm_notebook
# from tqdm.notebook import tqdm
# from kobert_tokenizer import KoBERTTokenizer
# from transformers import BertModel
# from transformers import AdamW
# from transformers.optimization import get_cosine_schedule_with_warmup

from database.conn import db_dependency
from routers.data_management.index import preprocessed_articles_to_dataframe

# bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
# vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

async def bert_learn(db: db_dependency, id: int):
    result = await preprocessed_articles_to_dataframe(db, id)

    df = pd.DataFrame(result, columns=['original_article_id', 'category_no', 'formatted_text'])

    return df
