# 프로젝트: BizTone Converter

## 프로젝트 개요

BizTone Converter는 직장인, 특히 신입사원이나 비즈니스 커뮤니케이션에 익숙하지 않은 사람들이 자신의 생각을 전문적인 업무 언어로 쉽고 빠르게 변환할 수 있도록 돕기 위해 설계된 AI 기반 웹 솔루션입니다. 이 프로젝트는 커뮤니케이션 효율성을 개선하고, 커뮤니케이션 품질을 표준화하며, 직원 교육 비용을 절감하는 것을 목표로 합니다.

이 애플리케이션은 HTML, Tailwind CSS, JavaScript로 구축된 현대적이고 반응형 사용자 인터페이스를 특징으로 하며, 다양한 장치에서 직관적인 경험을 제공합니다. 백엔드는 Python으로 작성된 경량 Flask 서버로, API 요청 처리, 톤 변환을 위한 Groq AI API 통합 및 정적 프론트엔드 파일 제공을 담당합니다.

주요 기능은 다음과 같습니다:
*   **핵심 톤 변환:** Groq AI의 `moonshotai/kimi-k2-instruct-0905` 모델을 활용하여 "상사" (Upward), "동료" (Lateral), "고객" (External) 의사소통 대상에 적합한 톤으로 텍스트를 변환합니다.
*   **결과 비교:** 원본 텍스트와 변환된 텍스트를 나란히 표시합니다.
*   **복사 기능:** 변환된 텍스트를 클립보드에 쉽게 복사할 수 있습니다.
*   **글자 수 카운터:** 입력 텍스트의 실시간 글자 수를 제공합니다.
*   **오류 처리:** API 지연 또는 실패에 대한 사용자 친화적인 메시지를 표시합니다.

## 아키텍처

이 프로젝트는 모듈화된 2계층 아키텍처를 따릅니다:

*   **프론트엔드 (`frontend/`):**
    *   **기술:** HTML5, Tailwind CSS, JavaScript (ES6+).
    *   **파일:** `index.html` (메인 진입점), `js/script.js` (클라이언트 측 로직, API 호출, DOM 조작) 및 사용자 지정 스피너를 위한 인라인 스타일.
    *   **스타일링:** 반응형, 현대적이며 시각적으로 매력적인 디자인을 위해 Tailwind CSS를 활용합니다.

*   **백엔드 (`backend/`):**
    *   **기술:** Python, Flask (RESTful API), `python-dotenv` (환경 변수용), `Flask-CORS`.
    *   **파일:** `app.py` (Flask 애플리케이션, Groq AI API 통합, 비즈니스 로직, 정적 파일 제공), `requirements.txt` (Python 종속성).
    *   **AI 통합:** Groq AI API와 `moonshotai/kimi-k2-instruct-0905` 모델을 사용하여 톤 변환을 수행하며, 선택된 페르소나 대상에 따라 프롬프트 엔지니어링을 적용합니다.

백엔드 Flask 애플리케이션은 정적 프론트엔드 파일을 직접 제공합니다.

## 빌드 및 실행

### 전제 조건

*   Python 3.x 설치됨.
*   `pip` (Python 패키지 설치 관리자) 설치됨.
*   프로젝트 루트에 `GROQ_API_KEY`가 포함된 `.env` 파일이 있어야 합니다.
    ```
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    ```
    *`"YOUR_GROQ_API_KEY"`를 실제 Groq API 키로 교체하세요.*

### 설정 및 설치

1.  **프로젝트 루트 디렉토리로 이동:**
    ```bash
    cd C:\gemini-biztalk
    ```

2.  **Python 가상 환경 생성 및 활성화:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **백엔드 종속성 설치:**
    ```bash
    pip install -r backend/requirements.txt
    ```

### 애플리케이션 실행

1.  **가상 환경이 활성화되었는지 확인하세요.**
2.  **Flask 백엔드 서버 실행:**
    ```bash
    python backend/app.py
    ```
    서버는 일반적으로 `http://127.0.0.1:5000/`에서 실행됩니다.

3.  **웹 브라우저를 열고** Flask 서버가 제공하는 주소(예: `http://127.0.0.1:5000/`)로 이동하여 BizTone Converter 프론트엔드에 액세스하세요.

## 개발 규칙

*   **환경 변수:** API 키와 같은 민감한 정보는 `.env` 파일을 통해 관리되며 백엔드에서 `python-dotenv`를 사용하여 액세스됩니다. 이러한 정보는 클라이언트 측에 노출되어서는 안 됩니다.
*   **CORS:** `Flask-CORS`는 개발 중에 모든 출처의 요청을 허용하도록 구성됩니다. 프로덕션 환경에서는 특정 도메인으로 제한해야 합니다.
*   **프론트엔드 스타일링:** Tailwind CSS는 `index.html`에 직접 적용된 클래스와 `script.js`의 동적 클래스 조작을 통해 모든 프론트엔드 스타일링에 사용됩니다.
*   **백엔드 API 엔드포인트:** `/api/convert` 엔드포인트는 JSON 요청 본문에 `text` 및 `target` (한국어 값: "상사", "동료", "고객")을 예상하는 텍스트 변환 요청을 처리합니다.
*   **Groq API:** `moonshotai/kimi-k2-instruct-0905` 모델은 AI 기반 텍스트 변환에 사용됩니다. 대상 페르소나에 따라 프롬프트 엔지니어링이 적용됩니다.