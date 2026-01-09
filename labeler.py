import os
import json
import base64
import requests

# 경로 설정
IMAGE_DIR = "research_data/top_skins"
LABEL_DIR = "research_data/labels"
if not os.path.exists(LABEL_DIR):
    os.makedirs(LABEL_DIR)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_label_from_ai(image_path):
    base64_image = encode_image(image_path)
    
    # Ollama API를 사용하여 AI에게 질문
    url = "http://localhost:11434/api/generate"
    prompt = """
    Analyze this Minecraft skin texture. 
    Provide the following tags in JSON format:
    1. Gender (Male, Female, Neutral)
    2. Theme (Human, Animal, Robot, Monster, etc.)
    3. Main Color
    4. Style (Cute, Cool, Simple, Detailed)
    Only return the JSON object.
    """
    
    data = {
        "model": "llava",
        "prompt": prompt,
        "images": [base64_image],
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(url, json=data)
        return json.loads(response.json()['response'])
    except Exception as e:
        print(f"❌ 라벨링 실패: {e}")
        return None

if __name__ == "__main__":
    files = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]
    print(f"🏷️ 총 {len(files)}개의 스킨 라벨링 시작...")

    for filename in files:
        skin_id = filename.split('.')[0]
        label_path = f"{LABEL_DIR}/{skin_id}.json"
        
        if os.path.exists(label_path): continue # 이미 완료된 건 건너뜀
        
        img_path = os.path.join(IMAGE_DIR, filename)
        print(f"🔎 분석 중: {filename}...")
        
        tags = get_label_from_ai(img_path)
        if tags:
            with open(label_path, 'w', encoding='utf-8') as f:
                json.dump(tags, f, indent=4)
            print(f"✅ 라벨 저장 완료: {skin_id}.json")

    print("\n🎉 모든 라벨링이 완료되었습니다!")