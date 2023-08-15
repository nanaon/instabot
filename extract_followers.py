from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

driver = webdriver.Chrome()

driver.get('https://instagram.com')
driver.implicitly_wait(15)

inputbox = driver.find_element(By.XPATH, '//input[@aria-label="전화번호, 사용자 이름 또는 이메일"]')
inputbox.click()
inputbox.send_keys('내 아이디')

inputbox = driver.find_element(By.XPATH, '//input[@aria-label="비밀번호"]')
inputbox.click()
inputbox.send_keys('내 비밀번호')

inputbox.send_keys(Keys.ENTER)
time.sleep(random.uniform(4.0, 6.0))

driver.get('https://www.instagram.com/대상계정/followers')
driver.implicitly_wait(15)

previousHeight = -1
currentHeight = -2

while previousHeight != currentHeight:
    previousHeight = currentHeight
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._aano'))) # ._aano: 팔로워 목록 팝업의 리스트 영역 클래스명
    currentHeight = driver.execute_script("return document.querySelector('._aano').scrollHeight")
    print('스크롤 영역: ', currentHeight)
    driver.execute_script("document.querySelector('._aano').scrollTo(0, document.querySelector('._aano').scrollHeight)")
    time.sleep(random.uniform(3.0, 5.0))
print('스크롤링 완료')

soup = BeautifulSoup(driver.page_source, 'html.parser')
followers = soup.findAll('a',['FPmhX','notranslate','_0imsa'])
followers_list = []
for follower in followers:
    followers_list.append(follower.get_text())

file_path = '/팔로워/목록을/저장할/파일/경로/followers.txt' # 팔로워 목록이 리스트 형태의 문자열로 저장됨
with open(file_path, "w", encoding="utf-8") as file:
    file.write(str(followers_list))
    print('파일 저장 완료')

print('팔로워 수: ' + str(len(followers_list)))
print('팔로워 목록: ', followers_list)