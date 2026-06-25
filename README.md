# 🎮 Minecraft Skin AI Generator

> **Stable Diffusion과 LoRA를 활용하여 자연어 프롬프트로 마인크래프트 스킨(전개도)을 생성하는 AI 프로젝트입니다.**
>
> 본 프로젝트는 단순히 AI 모델을 학습시키는 것을 넘어, **웹 크롤링 → 데이터 전처리 → JSONL 생성 → LoRA 학습 → Stable Diffusion 추론 최적화**까지의 **End-to-End AI 데이터 파이프라인**을 직접 구축한 프로젝트입니다.

---

# 📸 Demo

## Prompt

```
A cute boy with pink hair and cat ears
```

↓

**Generated Minecraft Skin**

(생성 이미지 추가)

↓

**Minecraft Preview**

(마인크래프트 적용 이미지 추가)

---

# 📖 프로젝트 소개

Minecraft 스킨은 일반 이미지와 달리 **64×64(또는 64×32)의 UV 전개도 규칙**을 반드시 따라야 합니다.

기존 Stable Diffusion 모델은 이러한 구조를 이해하지 못하기 때문에 피부, 얼굴, 팔 등의 위치가 쉽게 깨지는 문제가 발생합니다.

본 프로젝트에서는 이러한 문제를 해결하기 위해

- 대량의 Minecraft 스킨 데이터 수집
- AI 학습용 데이터셋 자동 구축
- LoRA 학습
- Stable Diffusion WebUI 추론 최적화

까지의 전 과정을 직접 구현했습니다.

---

# ✨ 주요 기능

- 🚀 멀티스레드 기반 스킨 크롤러 구현
- 🏷️ 자동 데이터 라벨링
- 📄 JSONL 데이터셋 생성
- 📝 Stable Diffusion(sd-scripts) 학습 포맷 변환
- 🤖 LoRA 모델 학습
- 🎨 Stable Diffusion WebUI 연동
- ⚙️ ADetailer 및 추론 파라미터 최적화

---

# 📊 프로젝트 현황

## 완료

- ✅ 약 **870장**의 Minecraft 스킨 데이터 수집
- ✅ 데이터 전처리 자동화
- ✅ JSONL 생성 파이프라인 구축
- ✅ TXT 변환 자동화
- ✅ LoRA 학습 완료
- ✅ `mc_skin_lora.safetensors` 생성
- ✅ 형태가 유지되는 스킨 생성 성공

## 진행 중

- 얼굴 및 머리카락 디테일 향상
- UV 구조 안정화
- 생성 품질 개선
- LoRA 재학습

---

# 🏗 프로젝트 파이프라인

```
Web Crawling
      │
      ▼
Prompt Labeling
      │
      ▼
JSONL Dataset
      │
      ▼
TXT Conversion
      │
      ▼
LoRA Training
      │
      ▼
Stable Diffusion WebUI
      │
      ▼
Minecraft Skin Generation
```

---

# 📁 프로젝트 구조

```
Minecraft-Skin-AI/
│
├── fast_scraper.py
├── scraper.py
├── labeler.py
├── jsonl_maker.py
├── jsonl_to_txt.py
│
├── research_data/
├── dataset.jsonl
│
└── README.md
```

| 파일 | 설명 |
|------|------|
| fast_scraper.py | 멀티스레드 기반 Minecraft 스킨 크롤러 |
| scraper.py | 기본 크롤러 |
| labeler.py | 이미지 라벨링 및 프롬프트 생성 |
| jsonl_maker.py | JSONL 데이터셋 생성 |
| jsonl_to_txt.py | sd-scripts 학습용 TXT 생성 |

---

# 🚀 실행 방법

## 1. 데이터 수집

```bash
python fast_scraper.py
```

---

## 2. 라벨링 및 JSONL 생성

```bash
python labeler.py
python jsonl_maker.py
```

---

## 3. TXT 생성

```bash
python jsonl_to_txt.py
```

---

## 4. LoRA 학습

생성된 이미지 + TXT 데이터를 이용하여 `sd-scripts`로 LoRA를 학습합니다.

출력

```
mc_skin_lora.safetensors
```

---

## 5. Stable Diffusion에서 사용

LoRA 파일을

```
stable-diffusion-webui/models/Lora/
```

에 복사한 후

```
<lora:mc_skin_lora:1>
a minecraft skin of pink hair boy
64x64 flat texture
```

와 같이 프롬프트를 입력하면 스킨을 생성할 수 있습니다.

---

# 🛠 기술 스택

- Python
- Stable Diffusion
- LoRA
- sd-scripts
- Stable Diffusion WebUI
- ADetailer
- JSONL
- Multi-threading
- Web Crawling

---

# ⚡ 해결한 문제

Minecraft 스킨은 일반 이미지와 달리 **정확한 UV 구조**를 유지해야 합니다.

프로젝트 진행 중 다음과 같은 문제를 해결했습니다.

- Stable Diffusion이 전개도 구조를 깨뜨리는 문제
- NumPy 버전 충돌
- WebUI 확장(ADetailer) 의존성 문제
- 데이터셋 포맷(JSONL → TXT) 자동 변환
- LoRA 학습 품질 개선

---

# 🎯 향후 계획

- 데이터셋 확장
- 다양한 스킨 스타일 지원
- UV 구조 정확도 향상
- 자동 프롬프트 생성
- 웹 데모 개발

---

# 📄 License

교육 및 연구 목적으로 제작되었습니다.

Minecraft 및 관련 리소스의 저작권은 Mojang Studios에 있습니다.
