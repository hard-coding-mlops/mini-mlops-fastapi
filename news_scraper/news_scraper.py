from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import pandas as pd

from news_scraper.news_category import NewsCategory
from news_scraper.format_time import getFormattedCurrentDateTime, getFormattedCurrentDate

MAX_PAGE = 11
NEWS_LAST_INDEX = 16

class NewsScraper:
    def __init__(self):
        self.driver = self.setup_driver()
        self.data = []

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def click_news_link(self, xpath):
        try:
            link_to_news = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script('arguments[0].click();', link_to_news)
            print('>>> 성공')
            return True
        except (TimeoutException, NoSuchElementException):
            print('>>> 실패')
            return False

    def get_element_text(self, xpath):
        try:
            element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print('>>> 성공')
            return element.text
        except TimeoutException:
            print('>>> 실패')
            return None

    def scrape_news(self):
        for category in NewsCategory:
            for page in range(1, MAX_PAGE):
                page_url = f'https://news.daum.net/breakingnews/{category.value}?page={page}'
                self.driver.get(page_url)

                for index in range(1, NEWS_LAST_INDEX):
                    print(f'\n########## "{category.value}"뉴스 {page}페이지, {index}번째 기사 ##########')
                    print('\t 1) 뉴스 기사 URL 클릭하기', end='\t')
                    if not self.click_news_link(f'/html/body/div[2]/div/div/div[1]/div[3]/ul/li[{index}]/div/strong/a'):
                        continue

                    scrape_start_time = getFormattedCurrentDateTime()

                    print('\t 2) 뉴스 기사 제목 가져오기', end='\t')
                    title = self.get_element_text('/html/body/div[1]/main/section/div/article/div[1]/h3')

                    if title is not None:
                        print('\t 3) a) 뉴스 기사 내용 가져오기', end='\t')
                        # 첫 번째 XPath
                        content_xpath = '/html/body/div[1]/main/section/div/article/div[2]/div[2]/section'
                        content = self.get_element_text(content_xpath)
                        if content is None:
                            # 첫 번째 XPath 실패 -> 두 번째 XPath
                            print('\t    b) XPATH 변경하여 재시도', end='\t')
                            content_xpath = '/html/body/div[1]/main/section/div/article/div[2]/div/section'
                            retry_content = self.get_element_text(content_xpath)
                            if retry_content is None:
                                print('>>> 실패')
                                # print(f'##########[크롤링 실패] "{category.value}"뉴스 {page}페이지, {index}번째 기사 크롤링에 실패했습니다.##########\n##########다음 기사로 넘어갑니다.##########\n')
                                self.driver.back()
                                continue
                        self.data.append({'scrape_time': scrape_start_time, 'category': category.value, 'title': title, 'content': content})

                    self.driver.back()

    def save_data_to_csv(self):
        current_date = getFormattedCurrentDate()
        file_name = f"news_{current_date}.csv"
        df = pd.DataFrame(self.data)
        df.to_csv(file_name, encoding='utf-8', index=False)
        print(f'\n- [Mini MLOps] {file_name}에 저장했습니다.')

    def cleanup(self):
        self.driver.quit()

# API 호출 시 실행 안 됨
if __name__ == "__main__":
    print('\n- [Mini MLOps] 뉴스 스크래핑을 시작합니다.')
    scraper = NewsScraper()
    scraper.scrape_news()
    scraper.save_data_to_csv()
    scraper.cleanup()
    print('- [Mini MLOps] 뉴스 스크래핑을 마칩니다.\n')