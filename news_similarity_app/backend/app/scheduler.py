from apscheduler.schedulers.background import BackgroundScheduler
from app import model, database, models
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
import time

def crawl_news_urls():
    """네이버 뉴스 홈에서 주요 뉴스 URL 수집"""
    url = "https://news.naver.com/"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    links = soup.select("a[href^='https://n.news.naver.com/article']")
    news_urls = list({link["href"] for link in links})  # 중복 제거
    return news_urls[:10]  # 상위 10개 기사만 예시로

def test_news_extraction():
    print("[테스트] 뉴스 기사 수집 및 추출 시작")

    urls = crawl_news_urls()
    print(f"[테스트] 수집된 뉴스 URL 수: {len(urls)}")

    for url in urls:
        try:
            print(f"\n[URL] {url}")
            title, body, publisher = model.extract_article(url)
            print(f"[제목] {title}")
            print(f"[본문] {body[:150]}...")
            print(f"[언론사] {publisher}")
        except Exception as e:
            print(f"[오류] 기사 파싱 실패 - {e}")
            
def run_daily_news_analysis():
    db = next(database.get_db())

    news_urls = crawl_news_urls()
    print(f"[스케줄러] 수집된 기사 수: {len(news_urls)}")

    for url in news_urls:
        try:
            title, body, publisher = model.extract_article(url)
            score, _ = model.get_similarity_and_summary(title, body)

            db_score = models.Score(publisher=publisher, score=score)
            db.add(db_score)
        except Exception as e:
            print(f"[오류] {url} 처리 중 실패: {e}")
    
    db.commit()
    print("[스케줄러] 유사도 분석 및 저장 완료")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_daily_news_analysis, 'cron', hour=0, minute=0)  # 매일 00:00
    scheduler.start()

##테스트를 위한 코드
if __name__ == "__main__":
    test_news_extraction()