import os
import json
import requests
import time

# 경로 설정
IMAGE_DIR = "research_data/top_skins"
LABEL_DIR = "research_data/labels"

# 라벨 저장 폴더가 없으면 생성
if not os.path.exists(LABEL_DIR):
    os.makedirs(LABEL_DIR)

def label_skin(image_path):
    """
    Ollama의 Llava 모델을 사용하여 마인크래프트 스킨 이미지를 분석합니다.
    """
    with open(image_path, "rb") as f:
        import base64
        img_data = base64.b64encode(f.read()).decode("utf-8")

    prompt = """
    Analyze this Minecraft skin and provide the following details in JSON format:
    - Gender: (Male, Female, Neutral)
    - Theme: (e.g., Robot, Knight, Casual, Animal, Fantasy, etc.)
    - Main Color: (The most dominant color)
    - Style: (Simple, Detailed)
    
    Only return the JSON object.
    """

    payload = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [img_data]
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        
        # 응답 텍스트에서 JSON 부분만 추출 (추후 정규식 등으로 보강 가능)
        result_text = response.json().get("response", "").strip()
        # 단순 텍스트 내 JSON 추출 시도
        if "{" in result_text:
            json_str = result_text[result_text.find("{"):result_text.rfind("}")+1]
            return json.loads(json_str)
        return None
    except Exception as e:
        print(f"   ❌ 라벨링 오류: {e}")
        return None

if __name__ == "__main__":
    # 이미지 파일 목록 가져오기
    skin_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]
    print(f"📊 총 {len(skin_files)}개의 스킨을 발견했습니다.")

    count = 0
    for filename in skin_files:
        skin_id = filename.split(".png")[0]
        image_path = os.path.join(IMAGE_DIR, filename)
        json_path = os.path.join(LABEL_DIR, f"{skin_id}.json")

        # [핵심 로직] 이미 라벨링된 JSON 파일이 있다면 건너뜁니다.
        if os.path.exists(json_path):
            # print(f"⏩ 스킵 (이미 라벨링됨): {skin_id}")
            continue

        print(f"🔎 분석 중: {filename}...")
        label_data = label_skin(image_path)

        if label_data:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(label_data, f, indent=4, ensure_ascii=False)
            count += 1
            print(f"   ✅ 완료 ({count}개 진행 중)")
        
        # GPU 과열 방지 및 API 부하 조절을 위한 짧은 휴식
        time.sleep(0.5)

    print(f"\n✨ 작업 완료! 새로 라벨링된 스킨: {count}개")