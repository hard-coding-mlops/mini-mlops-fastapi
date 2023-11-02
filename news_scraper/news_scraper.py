from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from IPython.display import display, Image
import re
import pandas as pd
import csv

from news_scraper.news_category import NewsCategory
from news_scraper.format_time import getFormattedCurrentTime

def getNews():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.daum.net/')
    driver.implicitly_wait(5)
    
    maxPage = 3
    newsLastIndex = 3
    
    with open('news.csv', encoding='utf-8', mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['스크래핑 시간', '기사 카테고리', '기사 제목', '기사 내용']) # 헤더 항목
    
        for category in NewsCategory:
            
            print(f'Current category: {category.value}')
            
            # 페이지는 바뀌나, html parsing 지속됨
            for page in range(1, maxPage):
                print(f'Current page: {page}')
                pageURL = f'https://news.daum.net/breakingnews/{category.value}?page={page}'
                driver.get(pageURL)
                driver.implicitly_wait(5)
                
                for index in range(1, newsLastIndex):
                    print(f'##########"{category.value}"뉴스 {page}페이지, {index}번째 기사##########')

                    print('\t 1) 뉴스 기사 URL 클릭')
                    linkToNewsXPATH = f'/html/body/div[2]/div/div/div[1]/div[3]/ul/li[{index}]/div/strong/a'
                    try:
                        linkToNews = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, linkToNewsXPATH)))
                        # linkToNews = driver.find_element(By.XPATH, linkToNewsXPATH)
                        driver.implicitly_wait(5)
                        # print('**********not clicked yet...')
                        # linkToNews.click()
                        driver.execute_script('arguments[0].click();', linkToNews)
                        # print('**********clicked!')
                    except (TimeoutException, NoSuchElementException):
                        print(f'##########[크롤링 실패] "{category.value}"뉴스 {page}페이지, {index}번째 기사 크롤링에 실패했습니다.##########\n##########다음 기사로 넘어갑니다.##########\n')
                        continue
                    #driver.implicitly_wait(5)
                    
                    print('\t 1) 성공')
                    driver.implicitly_wait(5)

                    scrapeStartTime = getFormattedCurrentTime()
                    
                    print('\t 2) 뉴스 기사 제목 가져오기')
                    titleXPATH = '/html/body/div[1]/main/section/div/article/div[1]/h3'
                    try:
                        getTitle = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, titleXPATH)))
    #                     getTitle = driver.find_element(By.XPATH, titleXPATH)
                        driver.implicitly_wait(5)
                    except TimeoutException:
                        print('\t 2) 실패')
                        print(f'##########[크롤링 실패] "{category.value}"뉴스 {page}페이지, {index}번째 기사 크롤링에 실패했습니다.##########\n##########다음 기사로 넘어갑니다.##########\n')
                        driver.back()
                        driver.implicitly_wait(5)
                        continue
                    # print(getTitle.text)
                    print('\t 2) 성공')
                    
                    
                    
                    print('\t 3) 뉴스 기사 내용 가져오기')
                    # 첫 번째 XPath
                    try:
                        contentXPATH = '/html/body/div[1]/main/section/div/article/div[2]/div[2]/section'
                        try:
                            getContent = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, contentXPATH)))
    #                         getContent = driver.find_element(By.XPATH, contentXPATH)
                            driver.implicitly_wait(5)
                        except TimeoutException:
                            print('\t 3) 실패')
                            print(f'##########[크롤링 실패] "{category.value}"뉴스 {page}페이지, {index}번째 기사 크롤링에 실패했습니다.##########\n##########다음 기사로 넘어갑니다.##########\n')
                            driver.back()
                            driver.implicitly_wait(5)
                            continue
                    except NoSuchElementException:
                        # 첫 번째 XPath 실패 -> 두 번째 XPath
                        contentXPATH = '/html/body/div[1]/main/section/div/article/div[2]/div/section'
                        try:
                            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, contentXPATH)))
                            getContent = driver.find_element(By.XPATH, contentXPATH)
                            driver.implicitly_wait(5)
                        except TimeoutException:
                            print('\t 3) 실패')
                            print(f'##########[크롤링 실패] "{category.value}"뉴스 {page}페이지, {index}번째 기사 크롤링에 실패했습니다.##########\n##########다음 기사로 넘어갑니다.##########\n')
                            driver.back()
                            driver.implicitly_wait(5)
                            continue
                    driver.implicitly_wait(5)
                    # print(getContent.text)
                    print('\t 3) 성공')
                    
            
            
                    print('\t 4) CSV 파일에 추가')
                    # 현재 시간, 스크래핑 분야, 스크래핑한 기사 제목, 스크래핑한 기사 내용 추가
                    writer.writerow([scrapeStartTime, category.value, getTitle.text, getContent.text])
                    driver.implicitly_wait(5)
                    print('\t 4) 성공')
            
            
                    print('##########다음 기사를 가져옵니다##########\n')
                    
                    driver.back()
                    driver.implicitly_wait(5)
                # end of [for page in range(1, maxPage):]
                driver.implicitly_wait(5)


    driver.quit()

    print('end')