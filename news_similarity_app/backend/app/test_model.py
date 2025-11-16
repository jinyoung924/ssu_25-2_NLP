from app.model import SIMILARITY_MODEL
from sentence_transformers.util import cos_sim

# 더미 문장 두 개
sentence_1 = "오늘 날씨가 정말 좋다."
sentence_2 = "하늘이 맑고 햇살이 따뜻하다."

# 문장 임베딩 생성
embeddings = SIMILARITY_MODEL.encode([sentence_1, sentence_2])

# 유사도 계산
similarity_score = cos_sim(embeddings[0], embeddings[1]).item()

print(f"문장 1: {sentence_1}")
print(f"문장 2: {sentence_2}")
print(f"유사도 점수: {similarity_score:.4f}")
