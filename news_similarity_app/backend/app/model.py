import numpy as np
import torch
import re
import json
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoConfig
from sentence_transformers import SentenceTransformer
from newspaper import Article
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


# ✅ 모델 디렉토리 경로
SUMMARY_MODEL_DIR = Path("app/models/kobart_finetuned")
SIMILARITY_MODEL_DIR = Path("app/models/similarity_model")

# ✅ 디바이스 설정
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ✅ 요약 모델 로딩 함수
def load_summary_model(model_dir: Path):
    config_path = model_dir / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for key in ["id2label", "label2id", "num_labels", "problem_type"]:
            cfg.pop(key, None)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    config = AutoConfig.from_pretrained(model_dir, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=True, local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir, config=config, local_files_only=True)
    model.to(DEVICE).eval()
    return tokenizer, model


# ✅ 유사도 모델 로딩 함수
def load_similarity_model(model_dir: Path):
    try:
        model = SentenceTransformer(str(model_dir))
        with open(model_dir / "best_threshold.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            threshold = data["threshold"]
            f1_score = data.get("f1", None)
        return model, threshold, f1_score
    except Exception as e:
        raise RuntimeError(f"유사도 모델 로딩 실패: {e}")


# ✅ 모델 로드 (전역 변수)
SUMMARY_TOKENIZER, SUMMARY_MODEL = load_summary_model(SUMMARY_MODEL_DIR)
SIMILARITY_MODEL, SIM_THRESHOLD, SIM_F1 = load_similarity_model(SIMILARITY_MODEL_DIR)


# ✅ 기사 추출 함수
def extract_article(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")

    # 네이버 뉴스일 경우
    if "naver.com" in domain:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.select_one("h2#title_area") or soup.select_one("h3#articleTitle")
        body_tag = soup.select_one("article#dic_area") or soup.select_one("div#articleBodyContents")

        title = title_tag.get_text(strip=True) if title_tag else "(제목 추출 실패)"
        body = body_tag.get_text(separator="\n", strip=True) if body_tag else "(본문 추출 실패)"
        publisher = soup.select_one("meta[property='og:article:author']")
        publisher = publisher["content"] if publisher and "content" in publisher.attrs else domain

        return title, body, publisher

    # 일반 기사
    article = Article(url, language='ko')
    article.download()
    article.parse()

    return article.title, article.text, domain


# ✅ 본문 요약
def summarize_text(text: str, min_new_tokens: int = 40, max_new_tokens: int = 150) -> str:
    if not text.strip():
        return ""
    inputs = SUMMARY_TOKENIZER(text, return_tensors="pt", truncation=True, max_length=1024)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = SUMMARY_MODEL.generate(
            **inputs,
            do_sample=False,
            num_beams=5,
            min_new_tokens=min_new_tokens,
            max_new_tokens=max_new_tokens,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            pad_token_id=SUMMARY_TOKENIZER.pad_token_id,
            eos_token_id=SUMMARY_TOKENIZER.eos_token_id,
            early_stopping=True,
        )
    decoded = SUMMARY_TOKENIZER.decode(outputs[0], skip_special_tokens=True)
    return drop_incomplete_sentences(tidy_korean_summary(decoded))


# ✅ 낚시성 판단
def predict_clickbait(title: str, summary: str) -> dict:
    e1 = SIMILARITY_MODEL.encode([title], normalize_embeddings=True)
    e2 = SIMILARITY_MODEL.encode([summary], normalize_embeddings=True)
    sim = float(np.dot(e1[0], e2[0]))
    pred = int(sim < SIM_THRESHOLD)
    return {
        "similarity": round(sim, 4),
        "threshold": SIM_THRESHOLD,
        "pred": pred,
        "label": "낚시성 기사" if pred else "정상 기사"
    }


# ✅ 최종 분석 함수
def summarize_article(title: str, body: str) -> dict:
    summary = summarize_text(body)
    prediction = predict_clickbait(title, summary)
    return {
        "title": title,
        "summary": summary,
        "similarity": prediction["similarity"],
        "label": prediction["label"],
        "threshold": prediction["threshold"]
    }


# ✅ 텍스트 정리 함수들
def tidy_korean_summary(text: str) -> str:
    t = re.sub(r"\s+", " ", (text or "")).strip()
    if t and t[-1] not in ".!?…。\"'”’":
        t += "."
    return t


def drop_incomplete_sentences(text: str) -> str:
    if not text.strip():
        return ""
    sentences = re.split(r'(?<=[\.\?\!。\!?])\s*', text)
    sentences = [s.strip() for s in sentences if s]
    if len(sentences) <= 1:
        return sentences[0] if sentences else ""
    last = sentences[-1]
    if len(last.split()) < 4 or not re.search(r'[.!?]$', last):
        sentences = sentences[:-1]
    return " ".join(sentences).strip()
