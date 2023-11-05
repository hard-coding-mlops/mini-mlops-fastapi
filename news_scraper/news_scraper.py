from datetime import datetime
import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from functools import partial

from news_scraper.news_category import NewsCategory
from news_scraper.format_time import get_formatted_current_date_time, get_formatted_current_date, format_date

MAX_PAGE = 15

class NewsScraper:
    def __init__(self):
        self.results = []

    def scrape_url_per_category(self, category):
        articles = []
        for page in range(1, MAX_PAGE):
            page_url =f"https://news.daum.net/breakingnews/{category}?page={page}"
            response = requests.get(page_url)
        
            if response.status_code != 200:
                print(f"{page_url}를 불러오는 데 문제가 발생했습니다")
                print(f"\t- {category.upper()} PROCESS POOL을 비정상 종료합니다.\n")
                return

            print(f" ######  {category}, {page}")
            news_list_html = BeautifulSoup(response.text, "html.parser")

            # 페이지 내 전체 뉴스 기사 목록을 가져옴
            url_list = news_list_html.find("ul", class_="list_news2 list_allnews")
            if url_list is None:
                print(f"\t- {category.upper()} {page}페이지는 존재하지 않습니다.")
                print(f"\t- {category.upper()} PROCESS POOL을 종료합니다.\n")
                break

            # 전체 목록에서 개별 기사들을 리스트로 저장
            urls = url_list.find_all("a", class_="link_txt")
            if urls is None:
                print(f"\t- {category.upper()} {page}페이지는 존재하지 않습니다.")
                print(f"\t- {category.upper()} PROCESS POOL을 종료합니다.\n")
                break

            for index, url in enumerate(urls):
                print(f"\t- {category.upper()} {page}페이지 {index + 1}번째 기사, {url['href']}를 성공적으로 가져왔습니다.")
                scraped_article = self.scrape_article_from_url(url["href"], category)
                articles.append(scraped_article)

        return articles

    def scrape_article_from_url(self, url, category):
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

        # print(f"\t    날짜: {upload_time}\n\t    제목: {title}\n\t    내용: {content[:30].strip()} ...")
        
        return {
            "scraping_time": current_time,
            "category": category,
            "upload_time": format_date(upload_time),
            "title": title,
            "content": content
        }

    def run(self):
        print("뉴스 스크래핑을 시작합니다.")

        # news_231106.csv
        current_date = get_formatted_current_date()
        file_name = f"news_data/news_{current_date}.csv"

        # ["society", "politics", "economic", "foreign", "culture", "entertain", "sports", "digital"]
        news_categories = [category.value for category in NewsCategory]

        with Pool(processes=len(news_categories)) as pool:
            results = pool.map(self.scrape_url_per_category, news_categories)

            # results csv로 저장
            with open(file_name, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Scraping Time", "Article Category", "Article Upload Time", "Article Title", "Article Content"])
                for articles in results:
                    for article in articles:
                        csv_writer.writerow([article["scraping_time"], article["category"], article["upload_time"], article["title"], article["content"]])
                
                print(f"\n- [Mini MLOps] '{file_name}'에 저장되었습니다.")


        print("\n- [Mini MLOps] 뉴스 스크래핑을 마칩니다.\n")


# if __name__ == "__main__":
#     news_scraper = NewsScraper()
#     news_scraper.run()
