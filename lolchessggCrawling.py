import warnings
warnings.filterwarnings("ignore")

import requests
import time
import random
import pandas as pd
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
pd.set_option('display.max_column', 100)

# selenium을 백그라운드로 실행하기 위해 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

# 우리가 데이터를 가져올 웹 페이지입니다.
# opgg_url = 'https://www.op.gg/champions'

# selenium이 제어할 chrome을 실행합니다.
driver = webdriver.Chrome("../../chromedriver")

# 데이터를 가져올 페이지로 이동합니다.
# driver.get(opgg_url)

# 결과가 들어갈 빈 리스트를 만듭니다.
champions = []
lane = [[] for _ in range(160)]
tier = []
counters = [[] for _ in range(160)]
easy_counter = [[] for _ in range(160)]
spell = [[] for _ in range(160)]
build = [[] for _ in range(160)]
shoes = []
skill_build = [[] for _ in range(160)]
rhun = []
win_rate = []
pick_rate = []

# 각 게임에 대해 웹 페이지에 기재된 스탯을 찾아서(selector 사용) 결과 리스트에 append하기
for i in range(1, 160):
    print(i)
    opgg_url = 'https://www.op.gg/champions'
    driver.get(opgg_url)
    time.sleep(random.uniform(2, 5))
    
    ## 챔피언 이름 / RIP 챔 고려
    try:
        champions.append(driver.find_element_by_xpath(f'//*[@id="content-container"]/aside/nav/a[{i}]/img').get_attribute('alt'))
    except Exception as e:
        try:
            champions.append(driver.find_element_by_xpath(f'//*[@id="content-container"]/aside/nav/a[{i}]/div/img').get_attribute('alt'))
        except Exception as e:
            pass
    
    ## 챔피언 상세로 들어가기
    driver.find_element_by_xpath(f'//*[@id="content-container"]/aside/nav/a[{i}]').click()
    time.sleep(random.uniform(3, 5))

    ## RIP 챔이라서 안들어가졋는지 try/except로 확인, 들어갔으면 카운터 챔피언 크롤링
    try:
        counters[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/a[1]/img').get_attribute('alt'))
    except Exception as e:
        continue
    counters[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/a[2]/img').get_attribute('alt'))
    counters[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/a[3]/img').get_attribute('alt'))
    
    ## 상대하기 쉬운챔 크롤링 위해 버튼 누르기
    driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/div/a[2]').click()
    
    ## 상대하기 쉬운 챔피언 크롤링
    easy_counter[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/a[1]/img').get_attribute('alt'))
    easy_counter[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/a[2]/img').get_attribute('alt'))
    easy_counter[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[2]/a[3]/img').get_attribute('alt'))
    
    ## 챔피언 라인 크롤링, 1~3개 에서 수집
    try:
        lane[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/div[1]/a[1]/div/span[1]').text)
        try:
            lane[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/div[1]/a[2]/div/span[1]').text)
            try:
                lane[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/div[1]/a[3]/div/span[1]').text)
            except Exception as e:
                pass
        except Exception as e:
                pass
    except Exception as e:
        print(e)
        lane[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/div[1]/a/div/span[1]').text)

    ## 챔피언 티어 크롤링
    tier.append(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div[1]/div[2]/div[1]/span').text.strip())

    ##챔피언 스펠 크롤링 (2개)
    spell[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div/ul/li[1]/div/img').get_attribute('alt'))
    spell[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div/ul/li[2]/div[2]/img').get_attribute('alt'))

    ## 챔피언 템빌드 중 첫 템빌드
    build[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[2]/tbody/tr[3]/td[1]/div/ul/li[1]/div/img').get_attribute('alt'))
    build[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[2]/tbody/tr[3]/td[1]/div/ul/li[2]/div[2]/img').get_attribute('alt'))
    build[i-1].append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[2]/tbody/tr[3]/td[1]/div/ul/li[3]/div[2]/img').get_attribute('alt'))
    
    ## 상위 탑 1티어 신발 / 카시 신발 안심음 issue..
    if i==128: pass
    else: shoes.append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[2]/tbody/tr[8]/td[1]/div/ul/li/div/img').get_attribute('alt'))
    
    ## 주 룬 1개 설정
    rhun.append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[1]/table[3]/tbody[1]/tr/td/div/div[1]/div/div[2]/div[1]').text)
    
    ## 승률과 픽률 크롤링
    win_rate.append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/div[1]/div[2]/section/div[1]/div[1]/div[2]').text)
    pick_rate.append(driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/div[1]/div[3]/section/div[1]/div[1]/div[2]').text)
    time.sleep(random.uniform(1, 4)) #랜덤 쉬기


# selenium이 제어하는 크롬을 종료합니다.
driver.quit()

# DataFrame으로 변환 후 출력
total_df = pd.DataFrame([champions, lane, tier, counters, easy_counter, spell, build, shoes, rhun, win_rate, pick_rate]
                        ,index = ['champion_name', 'lane', 'tier', 'counters', 'easy', 'spell', 'build', 'shoes', 'rhun', 'win_rate', 'pick_rate'])
print(total_df)
total_df.to_csv('C:/Users/helen/Desktop/1git/Web-Crawling/lolchessggCrawling/counters3.csv', encoding='cp949', index=True)