from datetime import datetime
import csv
import requests
from bs4 import BeautifulSoup

from news_scraper.news_category import NewsCategory
from news_scraper.format_time import get_formatted_current_date_time, get_formatted_current_date, format_date

MAX_PAGE = 11

class NewsScraper:
    def __init__(self):
        self.results = []

    def scrape_daum_news(self, category):
        for page in range(1, MAX_PAGE):
            page_url = f"https://news.daum.net/breakingnews/{category.value}?page={page}"
            response = requests.get(page_url)

            if response.status_code != 200:
                print(f"{page_url}를 불러오는 데 문제가 발생했습니다")
                continue

            print(f"\n- {category.value} {page}페이지 가져옴")

            soup = BeautifulSoup(response.text, "html.parser")
            ul = soup.find("ul", class_="list_news2 list_allnews")

            for index, li in enumerate(ul.find_all("li")):
                a = li.find("a", class_="link_txt")
                result = requests.get(a["href"])
                print(f"\t- {index + 1}. {a['href']} 가져오는 중...")
                article_info = self.scrape_article(result, category)
                self.results.append(article_info)

    def scrape_article(self, response, category):
        soup = BeautifulSoup(response.text, "html.parser")
        current_time = get_formatted_current_date_time()

        upload_time = soup.find("span", class_="num_date").text
        title = soup.find("h3", class_="tit_view").text
        content = soup.find("div", class_="article_view").text.strip()

        print(f"\t    날짜: {upload_time}\n\t    제목: {title}\n\t    내용: {content[:30].strip()} ...")

        return {
            "scraping_time": current_time,
            "article_category": category.value,
            "article_upload_time": format_date(upload_time),
            "article_title": title,
            "article_text": content
        }

    def run(self):
        print("뉴스 스크래핑을 시작합니다.")

        current_date = get_formatted_current_date()
        file_name = f"news_data/news_{current_date}.csv"

        with open(file_name, encoding="UTF-8", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["scraping_time", "article_category", "article_upload_time", "article_title", "article_text"])
            writer.writeheader()

            for category in NewsCategory:
                self.scrape_daum_news(category)
                writer.writerows(self.results)

        print("\n- [Mini MLOps] 뉴스 스크래핑을 마칩니다.\n")

if __name__ == "__main__":
    news_scraper = NewsScraper()
    news_scraper.run()
