import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup

# [1] 저장 폴더 설정
SAVE_DIR = "research_data/top_skins"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_driver():
    options = Options()
    # 보안 차단 확인을 위해 창이 뜨도록 설정
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 봇 탐지 방지 설정 (사람처럼 보이게 설정)
    stealth(driver,
        languages=["ko-KR", "ko", "en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def get_skin_ids(driver, page_num):
    # 사용자님이 찾으신 정답 URL 구조 반영
    if page_num == 1:
        url = "https://www.minecraftskins.com"
    else:
        url = f"https://www.minecraftskins.com/{page_num}/"
    
    print(f"\n🌐 {url} 접속 시도 중...")
    driver.get(url)
    
    # Cloudflare 통과 대기 (창이 뜨면 수동으로 클릭!)
    print(f"⏳ {page_num}페이지 보안 통과 대기 중... 필요 시 체크박스를 클릭하세요.")
    time.sleep(15) 
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ids = []
    
    # 상세 페이지 링크에서 ID 추출
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("/skin/"):
            parts = href.split('/')
            if len(parts) >= 3:
                ids.append(parts[2])
    
    return list(set(ids))

def download_skin(skin_id):
    save_path = f"{SAVE_DIR}/{skin_id}.png"
    if os.path.exists(save_path): 
        return False
    
    # 사이트에서 제공하는 직접 다운로드 엔드포인트
    img_url = f"https://www.minecraftskins.com/skin/download/{skin_id}"
    
    # [핵심] 403 에러를 피하기 위한 '신분증' 설정
    # Referer는 "내가 이 상세페이지를 보고 다운로드 버튼을 눌렀다"는 증거입니다.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': f'https://www.minecraftskins.com/skin/{skin_id}/',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }
    
    try:
        # 서버가 봇으로 의심하지 않게 약간의 간격을 둡니다.
        time.sleep(2)
        
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(save_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"      ❌ {skin_id} 다운로드 실패: {e}")
        return False

if __name__ == "__main__":
    driver = get_driver()
    
    try:
        # 테스트로 1, 2페이지만 진행
        for p in [1, 2]:
            ids = get_skin_ids(driver, p)
            
            if not ids:
                print(f"❓ {p}페이지에서 스킨 ID를 찾지 못했습니다. 차단 화면을 확인하세요.")
                continue
                
            print(f"🔎 {p}페이지에서 {len(ids)}개의 스킨 발견! 다운로드 시작...")
            
            for s_id in ids:
                if download_skin(s_id):
                    print(f"   ✅ 저장 완료: {s_id}.png")
                else:
                    # 실패 시 건너뜀
                    pass
                    
    finally:
        print("\n✨ 수집 프로세스가 종료되었습니다.")
        print(f"📁 저장된 위치: {os.path.abspath(SAVE_DIR)}")
        driver.quit()