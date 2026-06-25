# 🎮 Minecraft Skin AI Generator

> **An end-to-end AI pipeline for generating Minecraft skins from natural language using Stable Diffusion and LoRA.**
>
> This project goes beyond simply training an AI model. It implements the entire workflow—from large-scale web crawling and dataset preprocessing to LoRA training and Stable Diffusion inference optimization.

---

# 📖 Overview

Minecraft skins follow a strict **64×64 (or 64×32) UV layout**, making them fundamentally different from ordinary images.

Traditional Stable Diffusion models struggle to preserve this structure, often producing distorted faces, limbs, or misplaced textures.

This project addresses these challenges by building a complete AI pipeline for:

- Large-scale dataset collection
- Automated dataset preprocessing
- LoRA training
- Stable Diffusion inference optimization

---

# ✨ Features

- 🚀 Multi-threaded web crawler
- 🏷️ Automated prompt labeling
- 📄 JSONL dataset generation
- 📝 sd-scripts compatible TXT generation
- 🤖 Local LoRA training
- 🎨 Stable Diffusion WebUI integration
- ⚙️ ADetailer-based inference optimization

---

# 📊 Current Status

## Completed

- ✅ Collected approximately **870 Minecraft skins**
- ✅ Automated preprocessing pipeline
- ✅ JSONL dataset generation
- ✅ TXT conversion pipeline
- ✅ Trained a custom LoRA model
- ✅ Generated `mc_skin_lora.safetensors`
- ✅ Successfully generated structurally valid Minecraft skins

## In Progress

- Improving facial details
- Stabilizing UV layouts
- Enhancing generation quality
- Fine-tuning LoRA

---

# 🏗 Pipeline

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

# 📁 Project Structure

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

| File | Description |
|------|-------------|
| fast_scraper.py | Multi-threaded Minecraft skin crawler |
| scraper.py | Basic crawler |
| labeler.py | Prompt labeling tool |
| jsonl_maker.py | JSONL dataset generator |
| jsonl_to_txt.py | Converts JSONL into sd-scripts TXT format |

---

# 🚀 Usage

## 1. Crawl Dataset

```bash
python fast_scraper.py
```

## 2. Label & Generate JSONL

```bash
python labeler.py
python jsonl_maker.py
```

## 3. Convert to TXT

```bash
python jsonl_to_txt.py
```

## 4. Train LoRA

Train the generated image/TXT pairs using **sd-scripts**.

Output:

```
mc_skin_lora.safetensors
```

## 5. Generate Minecraft Skins

Copy the trained LoRA into:

```
stable-diffusion-webui/models/Lora/
```

Example prompt:

```
<lora:mc_skin_lora:1>

a minecraft skin of pink hair boy

64x64 flat texture
```

---

# 🛠 Tech Stack

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

# ⚡ Challenges

Minecraft skins require a strict UV layout, making generation significantly more difficult than ordinary image synthesis.

Key challenges addressed:

- Preserving UV structure
- Resolving NumPy compatibility issues
- Integrating ADetailer
- Building automated JSONL → TXT preprocessing
- Improving LoRA training quality

---

# 🎯 Future Work

- Expand the dataset
- Support additional skin styles
- Improve UV consistency
- Automatic prompt generation
- Deploy a web demo

---

# 📄 License

This project is intended for educational and research purposes.

Minecraft and related assets are the property of Mojang Studios.
