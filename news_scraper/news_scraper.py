from datetime import datetime
import csv
import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from functools import partial

from news_article import *
from news_scraper.news_category import NewsCategory
from news_scraper.format_time import *
from database import *

MAX_PAGE = 10

class NewsScraper:
    def __init__(self):
        self.results = []

    def scrape_url_per_category(self, category):
        articles = []
        for page in range(1, MAX_PAGE+1):
            page_url = f"https://news.daum.net/breakingnews/{category}?page={page}"
            response = requests.get(page_url)

            if response.status_code != 200:
                print(f"{page_url}를 불러오는 데 문제가 발생했습니다")
                print(f"\t- {category.upper()} PROCESS POOL을 비정상 종료합니다.\n")
                return

            print(f" ######  {category}, {page}")
            news_list_html = BeautifulSoup(response.text, "html.parser")
            url_list = news_list_html.find("ul", class_="list_news2 list_allnews")

            if url_list is None:
                print(f"\t- {category.upper()} {page}페이지는 존재하지 않습니다.")
                print(f"\t- {category.upper()} PROCESS POOL을 종료합니다.\n")
                break

            urls = url_list.find_all("a", class_="link_txt")
            
            if not urls:
                print(f"\t- {category.upper()} {page}페이지는 존재하지 않습니다.")
                print(f"\t- {category.upper()} PROCESS POOL을 종료합니다.\n")
                break

            articles.extend(self.scrape_articles_from_urls(urls, category))
        
        return articles

    def scrape_articles_from_urls(self, urls, category):
        articles = []

        for index, url in enumerate(urls):
            #print(f"\t- {category.upper()} {index + 1}번째 기사, {url['href']}를 성공적으로 가져왔습니다.")
            scraped_article = self.scrape_article_from_url(url["href"], category)
            articles.append(scraped_article)

        return articles

    def scrape_article_from_url(self, url, category):
        #time.sleep(0.5)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"{url}를 불러오는 데 문제가 발생했습니다")
            print(f"\t- {category.upper()} PROCESS POOL을 종료합니다.\n")
            return
        
        news_html = BeautifulSoup(response.text, "html.parser")
        current_time = get_formatted_current_date_time()
        upload_time = news_html.find("span", class_="num_date").text
        title = news_html.find("h3", class_="tit_view").text
        content = news_html.find("div", class_="article_view").text.strip()

        return Article(
            current_time = current_time,
            category = category,
            upload_time = upload_time,
            title = title,
            content = content)
        
    def run(self): 
        news_categories = [category.value for category in NewsCategory]
         
        print("뉴스 스크래핑을 시작합니다.")

        with Pool(processes=len(NewsCategory)) as pool:
            article_list = pool.map(self.scrape_url_per_category, news_categories)     
            return article_list
        

if __name__ == "__main__":
    newscraper = NewsScraper()
    newscraper.run()
    
    
