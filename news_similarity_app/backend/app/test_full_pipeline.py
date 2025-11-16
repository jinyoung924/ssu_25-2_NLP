# 파일 경로: app/test_full_pipeline.py
from app.model import summarize_article

# 더미 제목과 본문 입력
dummy_title = "AI가 바꾸는 세상, 기대와 우려 공존"
dummy_body = """
AI 기술이 빠르게 발전하면서 우리 삶의 다양한 영역에 영향을 미치고 있다.
특히 생성형 AI는 콘텐츠 생산, 고객 응대, 의료, 교육 등에서 혁신적인 도구로 떠오르고 있다.
하지만 동시에 윤리적 문제와 일자리 대체에 대한 우려도 커지고 있다.
정부와 기업들은 AI 기술의 책임 있는 활용을 위한 기준 마련에 힘쓰고 있다.
"""

# 테스트 실행
result = summarize_article(dummy_title, dummy_body)

# 결과 출력
print("▶ 제목:", result["title"])
print("▶ 요약:", result["summary"])
print("▶ 유사도:", result["similarity"])
print("▶ 판정:", result["label"])
print("▶ 기준 임계값:", result["threshold"])
