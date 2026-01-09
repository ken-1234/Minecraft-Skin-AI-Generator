import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

# 저장 폴더 설정
SAVE_DIR = "research_data/top_skins"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- 브라우저 설정 ---
chrome_options = Options()
chrome_options.add_argument("--headless") # 창 없이 실행 (속도 향상)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 드라이버 자동 설치 및 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_skin_ids_with_selenium(page_num):
    url = f"https://www.minecraftskins.com/top/{page_num}/"
    print(f"🌐 {page_num}페이지 접속 시도 중...")
    
    driver.get(url)
    time.sleep(3) # 페이지 로딩 대기
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    ids = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("/skin/"):
            parts = href.split('/')
            if len(parts) >= 3:
                ids.append(parts[2])
    
    return list(set(ids))

# 이미지 다운로드는 그대로 requests를 쓰되, 403 방지를 위해 헤더를 강화합니다.
def download_skin(skin_id):
    save_path = f"{SAVE_DIR}/{skin_id}.png"
    if os.path.exists(save_path): return False

    img_url = f"https://www.minecraftskins.com/skin/download/{skin_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        time.sleep(2)
        resp = requests.get(img_url, headers=headers)
        if resp.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            return True
    except:
        pass
    return False

if __name__ == "__main__":
    try:
        for p in range(1, 3): # 테스트용 1~2페이지
            ids = get_skin_ids_with_selenium(p)
            print(f"🔎 {len(ids)}개의 ID 발견!")
            for s_id in ids:
                if download_skin(s_id):
                    print(f"   ✅ 다운로드 완료: {s_id}")
    finally:
        driver.quit() # 브라우저 종료