# Mini MLOps FastAPI

이 프로젝트는 FastAPI를 사용하여 구축된 미니 MLOps 플랫폼입니다. 뉴스 기사 수집, 전처리, BERT 모델 학습 및 분류 서비스 제공을 위한 API를 제공합니다.

## 기능

- **뉴스 수집**: 지정된 카테고리의 뉴스 기사를 스크래핑합니다.
- **데이터 전처리**: 수집된 뉴스 기사의 중복을 제거하고 한글 이외의 문자를 제거하여 정제합니다.
- **BERT 모델 학습**: 전처리된 데이터를 사용하여 BERT 모델을 학습합니다. (관련 코드는 `routers/bert_model/index.py`에 포함되어 있으나, 현재는 주석 처리되어 있습니다.)
- **뉴스 분류**: 학습된 모델을 사용하여 입력된 텍스트를 분류합니다.
- **데이터 관리**: 수집 및 전처리된 데이터를 관리하고 다운로드할 수 있는 API를 제공합니다.
- **사용자 인증**: Kakao OAuth2를 사용한 사용자 로그인 및 로그아웃 기능을 제공합니다.

## API 엔드포인트

### User (`/user`)

- `POST /kakao/login`: Kakao OAuth2를 사용하여 로그인하고 액세스 토큰을 발급받습니다.
- `GET /kakao/logout`: 로그아웃합니다.

### Data Management (`/data_management`)

- `GET /scrape-and-preprocess`: 뉴스 기사를 수집하고 전처리합니다.
- `GET /download-preprocessed-data/{id}`: 전처리된 데이터를 CSV 파일로 다운로드합니다.
- `GET /total-ordered-data`: 수집된 데이터 그룹의 목록을 가져옵니다.
- `GET /single-group/{id}`: 특정 그룹의 상세 정보를 가져옵니다.
- `DELETE /single-group/{id}`: 특정 그룹의 데이터를 삭제합니다.

### News Scraper (`/scraper`)

- `GET /`: 모든 뉴스 기사를 가져옵니다.
- `GET /scrape`: 뉴스 기사 스크래핑을 시작하고 진행 상황을 스트리밍합니다.

### Preprocessor (`/preprocessor`)

- `GET /preprocess`: 데이터 전처리를 시작하고 진행 상황을 스트리밍합니다.

### BERT Model (`/model`)

- `GET /`: 학습된 모든 모델의 목록을 가져옵니다.
- `GET /top-five`: 정확도 상위 5개 모델을 가져옵니다.
- `GET /currently-active`: 현재 활성화된 모델의 정보를 가져옵니다.
- `GET /deploy/{id}`: 특정 모델을 배포합니다.
- `POST /evaluate`: 모델의 예측 결과를 평가합니다.
- `GET /clients`: 클라이언트 요청 기록을 가져옵니다.
- `GET /clients/{client_id}`: 특정 클라이언트 요청의 상세 정보를 가져옵니다.
- `GET /{id}`: 특정 모델의 상세 정보(에포크, 그래프 포함)를 가져옵니다.

### News Classifier (`/classifier`)

- `POST /classify`: 입력된 텍스트를 분류합니다.

## 프로젝트 구조

```
C:\mini-mlops-fastapi\
├───.gitignore
├───main.py
├───.git\...
├───.github\
│   └───ISSUE_TEMPLATE\
│       └───issue-template.md
├───database\
│   └───conn.py
├───models\
│   ├───client.py
│   ├───deployment.py
│   ├───epoch.py
│   ├───graph.py
│   ├───model.py
│   ├───news_article.py
│   ├───preprocessed_article.py
│   ├───scraped_order.py
│   ├───test.py
│   └───user.py
└───routers\
    ├───bert_model\
    │   └───index.py
    ├───data_management\
    │   └───index.py
    ├───news_classifier\
    │   └───index.py
    ├───news_scraper\
    │   ├───format_time.py
    │   ├───index.py
    │   ├───news_category.py
    │   └───news_scraper.py
    ├───preprocessor\
    │   ├───category_label.py
    │   └───index.py
    └───user\
        └───index.py
```

## 시작하기

### 요구사항

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- 기타 필요한 라이브러리 (전체 목록은 `requirements.txt` 파일을 생성하여 관리하는 것을 권장합니다.)

### 설치

1.  저장소를 클론합니다.
    ```bash
    git clone https://github.com/your-username/mini-mlops-fastapi.git
    cd mini-mlops-fastapi
    ```

2.  필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```
    *(참고: `requirements.txt` 파일이 현재 없으므로, 프로젝트에 사용된 라이브러리를 기반으로 직접 생성해야 합니다.)*

3.  `.env` 파일을 생성하고 Kakao API 키를 설정합니다.
    ```
    KAKAO_REST_API_KEY=your_kakao_rest_api_key
    KAKAO_REDIRECT_URI=http://localhost:3000/auth/kakao/callback
    ```

### 실행

애플리케이션을 실행하려면 다음 명령을 사용하세요.

```bash
uvicorn main:app --reload
```

API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.
