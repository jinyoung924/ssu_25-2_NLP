import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from newspaper import Article
from urllib.parse import urlparse
from newspaper import Article
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

def extract_article(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")

    # ✅ 네이버 뉴스일 경우 별도 처리
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

    # ✅ 일반 기사 (newspaper3k로 처리)
    article = Article(url, language='ko')
    article.download()
    article.parse()

    title = article.title
    body = article.text
    publisher = domain

    return title, body, publisher
'''
similarity_model = SentenceTransformer("./models/similarity_model")
summary_model = BartForConditionalGeneration.from_pretrained("./models/summary_model")
summary_tokenizer = BartTokenizer.from_pretrained("./models/summary_model")

def get_similarity_and_summary(title: str, body: str):
    # ✅ 유사도 계산
    title_emb = similarity_model.encode(title, convert_to_tensor=True)
    body_emb = similarity_model.encode(body, convert_to_tensor=True)
    score = cosine_similarity([title_emb.cpu().numpy()], [body_emb.cpu().numpy()])[0][0]

    # ✅ 요약
    inputs = summary_tokenizer([body], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = summary_model.generate(inputs["input_ids"], num_beams=4, max_length=128, early_stopping=True)
    summary = summary_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return round(float(score), 4), summary
'''

##테스트용 코드
if __name__ == "__main__":
    url = "https://n.news.naver.com/article/081/0003587293?cds=news_media_pc&type=editn"
    title, body, publisher = extract_article(url)
    print("제목:", title)
    print("본문:", body[:200])
    print("언론사:", publisher)