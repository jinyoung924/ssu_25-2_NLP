backend/
│
├── main.py                   : FastAPI 앱 실행 진입점, API 및 스케줄러 등록
├── database.py              : SQLAlchemy DB 연결 및 세션 설정
├── models.py                : DB 테이블 모델 정의 (Score 등)
├── schemas.py               : API 요청/응답용 Pydantic 스키마 정의
│
├── api.py                   : FastAPI 라우터 정의 (API 엔드포인트들)
├── model.py                 : 기사 유사도 분석 및 요약 처리 함수 정의
├── leaderboard.py           : 리더보드 점수 처리 및 평균 계산 로직
├── crud.py                  : DB 조작 함수들 (Create, Read 등)
├── scheduler.py             : 매일 자정 뉴스 수집 및 자동 분석 스케줄러
│
├── test.db                  : SQLite 테스트용 DB 파일 (로컬 저장)
├── requirements.txt         : 백엔드에 필요한 Python 패키지 목록
frontend/
│
├── package.json             : 프론트엔드(React) 의존성 및 실행 스크립트 설정
├── public/                  : 정적 파일 폴더 (index.html 포함)
│
├── src/                     : 실제 React 컴포넌트 작성 폴더
│   └── App.jsx              : 전체 앱의 메인 컴포넌트, API 통신 포함
├── node_modules/            : 설치된 npm 패키지 모음 (자동 생성)
