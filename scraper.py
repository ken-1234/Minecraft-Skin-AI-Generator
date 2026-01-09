import os
import time
import requests
from bs4 import BeautifulSoup

# --- [설정 부분] ---
TARGET_BASE_URL = "https://www.minecraftskins.com/top" # 인기 스킨 페이지
SAVE_DIR = "research_data/top_skins"                   # 저장 경로
START_PAGE = 1                                         # 시작 페이지
END_PAGE = 5                                           # 끝 페이지 (테스트용으로 5페이지까지)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Academic-Research-Project'
}

# 저장 폴더 생성
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
    print(f"📂 폴더 생성 완료: {SAVE_DIR}")

def get_skin_ids_from_page(page_num):
    """특정 페이지에서 스킨 상세 ID들을 수집합니다."""
    url = f"{TARGET_BASE_URL}/{page_num}/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"❌ 페이지 {page_num} 접근 실패 (상태 코드: {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        # Skindex의 스킨 링크 패턴: /skin/12345678/name
        skin_links = soup.find_all('a', href=True)
        
        ids = []
        for link in skin_links:
            href = link['href']
            if href.startswith("/skin/"):
                # href에서 ID 숫자만 추출
                parts = href.split('/')
                if len(parts) >= 3:
                    ids.append(parts[2])
        
        return list(set(ids)) # 중복 제거
    except Exception as e:
        print(f"❌ 에러 발생 (페이지 {page_num}): {e}")
        return []

def download_skin(skin_id):
    """ID를 이용해 실제 스킨 .png 파일을 다운로드합니다."""
    save_path = f"{SAVE_DIR}/{skin_id}.png"
    
    # 이미 다운로드한 파일은 건너뛰기
    if os.path.exists(save_path):
        return False

    download_url = f"https://www.minecraftskins.com/skin/download/{skin_id}"
    try:
        # 서버 매너: 1.5초 쉬기 (매우 중요!)
        time.sleep(1.5)
        
        resp = requests.get(download_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            return True
    except:
        pass
    return False

# --- [메인 실행부] ---
if __name__ == "__main__":
    print(f"🚀 {START_PAGE}페이지부터 {END_PAGE}페이지까지 수집을 시작합니다...")
    
    total_downloaded = 0
    
    for p in range(START_PAGE, END_PAGE + 1):
        print(f"📄 현재 {p}페이지 분석 중...")
        skin_ids = get_skin_ids_from_page(p)
        
        print(f"🔎 {len(skin_ids)}개의 스킨 발견! 다운로드를 시작합니다...")
        for s_id in skin_ids:
            if download_skin(s_id):
                total_downloaded += 1
                print(f"   ✅ [{total_downloaded}] 다운로드 완료: {s_id}.png")
            else:
                # 이미 있거나 실패한 경우 출력 생략 (터미널 깔끔하게 유지)
                pass

    print(f"\n✨ 작업 완료! 총 {total_downloaded}개의 새로운 스킨을 수집했습니다.")
    print(f"📍 저장 위치: {os.path.abspath(SAVE_DIR)}")