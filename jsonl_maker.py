import os
import json

# 경로 설정
LABEL_DIR = "research_data/labels"
OUTPUT_FILE = "research_data/metadata.jsonl"

def create_jsonl():
    label_files = [f for f in os.listdir(LABEL_DIR) if f.endswith(".json")]
    print(f"📦 총 {len(label_files)}개의 라벨 파일을 병합합니다...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for filename in label_files:
            skin_id = filename.split(".json")[0]
            json_path = os.path.join(LABEL_DIR, filename)
            
            try:
                with open(json_path, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                
                # AI 학습을 위해 파일명과 태그 정보를 한 줄의 딕셔너리로 구성
                # 예: {"file_name": "23778327.png", "text": "A female skin, Fantasy theme, Pink color, Detailed style"}
                caption = f"A {data.get('Gender', 'neutral')} skin, {data.get('Theme', 'casual')} theme, {data.get('Main Color', 'various')} color, {data.get('Style', 'simple')} style"
                
                line = {
                    "file_name": f"{skin_id}.png",
                    "text": caption
                }
                
                # 한 줄씩 저장 (JSON Lines 형식)
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
            except Exception as e:
                print(f"   ⚠️ {filename} 처리 중 오류 발생: {e}")

    print(f"\n✅ 최종 데이터셋 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_jsonl()