import json
import os

jsonl_path = "research_data/metadata.jsonl"
img_dir = "train_data/img/100_mcskin"

# 폴더가 없으면 생성
os.makedirs(img_dir, exist_ok=True)

with open(jsonl_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        
        # 첫 번째 데이터에서 키 목록 확인 및 출력
        if i == 0:
            print(f"🔍 데이터 구조 확인: {data.keys()}")
            # 실제 존재하는 키 이름을 찾습니다.
            target_key = "file_name" if "file_name" in data else ("image" if "image" in data else None)
            
            if not target_key:
                print("❌ 이미지 경로와 관련된 키를 찾을 수 없습니다. 위 리스트를 보고 직접 알려주세요!")
                break
        
        # 이미지 파일명 추출
        file_path = data[target_key]
        file_name = os.path.basename(file_path)
        
        # .txt 파일 생성
        txt_name = os.path.splitext(file_name)[0] + ".txt"
        txt_path = os.path.join(img_dir, txt_name)
        
        with open(txt_path, "w", encoding="utf-8") as txt_f:
            # 캡션 키도 확인 (보안책)
            caption = data.get("caption", data.get("text", ""))
            txt_f.write(caption)

print("✅ 변환 프로세스가 완료되었습니다!")