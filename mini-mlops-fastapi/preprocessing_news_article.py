from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, SMALLINT, JSON
from database import *
from datetime import datetime

# article_category_num : 카테고리 별 숫자로 변환
# article_text : 기사 제목 + 기사 본문
# article_tokenizer : article_text를 명사만 토큰화(type: 리스트)
# article_embedding : article_tokenizer 임베딩(type: 리스트)

Base = declarative_base()

class Preprcessing_Article(Base):
	__tablename__ = 'preprocessing_news_article'

	id = Column(SMALLINT, autoincrement=True, primary_key=True)
	article_category = Column(Text, nullable=False)
	article_category_num = Column(SMALLINT, nullable=False)
	article_text = Column(Text, nullable=False)
	article_tokenizer = Column(JSON, nullable=False)
	#article_embedding = Column(JSON)

	def __init__(self, category, category_num, text, tokenizer):
		self.article_category = category, 
		self.article_category_num = category_num, 
		self.article_text = text, 
		self.article_tokenizer = tokenizer,
		#self.article_embedding = embedding

#Base.metadata.create_all(engine)


	
	