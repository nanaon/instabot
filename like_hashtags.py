from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

def click_like_btn(hashtag):
    like_cnt = random.randrange(10,20)
    driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    time.sleep(10)

    # 인기 게시글 이외의 게시글이 PC 버전에서도 뜨고, 인기 게시글 이외의 포스트에 좋아요를 누르고 싶을 때는 index를 [9]로 수정
    new_feed = driver.find_elements(By.XPATH, '//article//img //ancestor :: div[2]')[0]
    new_feed.click()

    num_of_like = 0
    for i in range(like_cnt): 
        time.sleep(3)
        span = driver.find_element(By.XPATH, '//*[@aria-label="좋아요" or @aria-label="좋아요 취소"]//ancestor :: span[2]')  
        like_btn = span.find_element(By.TAG_NAME, 'div') # div: 좋아요 버튼의 요소
        btn_svg = like_btn.find_element(By.TAG_NAME, 'svg') 
        svg = btn_svg.get_attribute('aria-label') 
        
        if svg == '좋아요' : 
            like_btn.click() 
            num_of_like += 1
            print(f'좋아요를 {num_of_like}번째 눌렀습니다.')
            time.sleep(random.randrange(3,5))
        else :
            print('이미 작업한 피드입니다.')               
            time.sleep(random.randrange(5))        

        if i < like_cnt - 1 : 
            next_feed_xpath = driver.find_element(By.XPATH, '//*[@aria-label="다음" and @height="16"]//ancestor :: div[2]')
            next_feed = next_feed_xpath.find_element(By.TAG_NAME, 'button') 
            next_feed.click() 
            time.sleep(random.randrange(5))

while True :
    tags = ['좋아요', '누르고싶은', '태그들']
    random.shuffle(tags)
    for tag in tags:
        try : 
            print(f'작업 태그는 {tag} 입니다.')
            click_like_btn(tag)
            print(f'{tag} 태그 작업이 끝났습니다. 다음 태그로 넘어갑니다.')
        except Exception as e:
            print(e, '새로운 피드가 없거나, 다음 피드가 없습니다. 다음 태그로 넘어갑니다.')
            driver.refresh()
