import os
import time
import random
import urllib.request

# [1] 저장 폴더 설정
SAVE_DIR = "research_data/top_skins"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def stealth_download(skin_id):
    save_path = f"{SAVE_DIR}/{skin_id}.png"
    
    # 중복 방지 로직 (우리가 아까 강조한 부분!)
    if os.path.exists(save_path):
        return "exists"
    
    # 직접 다운로드 링크 생성
    img_url = f"https://www.minecraftskins.com/skin/download/{skin_id}"
    
    # 서버가 봇으로 의심하지 않도록 정교한 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': f'https://www.minecraftskins.com/skin/{skin_id}/', # 상세페이지에서 온 척 하기
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        # 1.5 ~ 3초 사이의 랜덤 딜레이 (서버 과부하 방지 및 인간미 추가)
        time.sleep(random.uniform(1.5, 3.0))
        
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.read())
                return "success"
    except Exception as e:
        return f"fail: {e}"

if __name__ == "__main__":
    # 1페이지에서 확인했던 가장 큰 ID 근처에서 시작하세요.
    # 예: 22442200. 폴더에서 직접 확인하고 수정해 주세요!
    start_id = 23779321
    
    print(f"🚀 직접 다운로드(Stealth Mode) 시작: ID {start_id}부터 거꾸로...")
    
    success_count = 0
    fail_count = 0
    
    # 1,000개를 목표로 시도해 봅니다.
    for i in range(1000):
        current_id = start_id - i
        result = stealth_download(current_id)
        
        if result == "success":
            success_count += 1
            print(f"✅ [{success_count}] 저장 완료: {current_id}")
            fail_count = 0 # 성공하면 실패 카운트 초기화
        elif result == "exists":
            print(f"⏩ 스킵 (이미 존재): {current_id}")
        else:
            print(f"➖ 존재하지 않거나 오류: {current_id}")
            fail_count += 1
            
        # 만약 너무 많이 연속으로 실패하면(ID가 비어있는 구간), 종료하거나 점프해야 합니다.
        if fail_count > 50:
            print("🚨 연속 실패가 너무 많아 안전을 위해 중단합니다.")
            break

    print(f"\n✨ 수집 종료! 새로 추가된 스킨: {success_count}개")