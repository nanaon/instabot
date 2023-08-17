from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import unicodedata


with open('/파일/경로/followers.txt', 'r') as file:
    content = file.read()
followers = eval(content)

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

# 좋아요 누르지 않고 넘어갈 본문 키워드 목록
ad_keywords = ['좋아요', '누르지', '않을', '본문', '키워드']

chunk_size = 5 # 봇 사용으로 썰리지 않기 위해 일정 사이즈로 끊어서 작업
currently_done_cnt = 0
currently_like_cnt = 0
total_cnt = len(followers)
print('작업을 시작합니다.')
for i in range(0, len(followers), chunk_size):
    chunk = followers[i : i + chunk_size]
    for follower in chunk:
        driver.get(f'https://www.instagram.com/{follower}')
        time.sleep(random.uniform(4.0, 7.0))
        try:
            driver.find_element(By.CSS_SELECTOR, '._aa_u') # 비공개 계정 pass
        except:
            try:
                first_post = driver.find_elements(By.XPATH, '//article//img //ancestor :: div[2]')[0]
                first_post.click()
                time.sleep(3)

                article = driver.find_elements(By.XPATH, '//h1/a') # 본문 추출
                time.sleep(10)
                is_ad = False
                current_keyword = ''
                for texts in article :
                    text = unicodedata.normalize('NFC',texts.get_attribute('innerText'))
                    for keyword in ad_keywords:
                        if text.find(keyword) == -1:
                            continue
                        else:
                            # 광고 계정 거르기
                            print(f'광고 키워드 : {keyword}. 좋아요를 누르지 않고 넘어갑니다.')
                            is_ad = True
                            current_keyword = keyword
                            break
                    if current_keyword in ad_keywords:
                        break
                if not is_ad:
                    span = driver.find_element(By.XPATH, '//*[@aria-label="좋아요" or @aria-label="좋아요 취소"]//ancestor :: span[2]')  
                    like_btn = span.find_element(By.TAG_NAME, 'div') # div: 좋아요 버튼의 요소
                    btn_svg = like_btn.find_element(By.TAG_NAME, 'svg') 
                    svg = btn_svg.get_attribute('aria-label')
                    
                    if svg == '좋아요':
                        like_btn.click() 
                        currently_like_cnt += 1
                        time.sleep(random.randrange(3,5))            
                    else:
                        pass
            except:
              pass
            currently_done_cnt += 1
    print(f'총 {total_cnt}명 중 {currently_done_cnt}명 완료. 그중 {currently_like_cnt}명에게 좋아요를 눌렀습니다.')
    time.sleep(random.uniform(10.0, 15.0))
print(f'{currently_done_cnt}명 완료')
