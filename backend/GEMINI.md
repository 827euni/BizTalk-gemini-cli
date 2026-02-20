# 프로젝트: BizTone Converter - 백엔드 (`backend/`)

## 프로젝트 개요

이 디렉토리는 "BizTone Converter" 애플리케이션의 백엔드 부분을 포함합니다. Flask 웹 프레임워크를 기반으로 하며, 클라이언트의 요청을 처리하고, Groq AI API와 연동하여 텍스트의 톤을 변환하는 핵심 로직을 담당합니다. 또한, 빌드된 프론트엔드 정적 파일들을 서빙하는 역할도 수행합니다.

**주요 기능 및 책임:**
*   클라이언트(프론트엔드)로부터 텍스트 변환 요청 수신 및 처리
*   Groq AI API를 활용한 실제 업무 말투 변환
*   대상(상사, 동료, 고객)별 맞춤형 프롬프트 엔지니어링 적용
*   프론트엔드 정적 파일 (`index.html`, `js`, `css` 등) 서빙
*   API 키 등 민감 정보를 안전하게 관리 (환경 변수 사용)
*   CORS (Cross-Origin Resource Sharing) 설정 관리

## 기술 스택

*   **Python 3.x**: 백엔드 애플리케이션 개발 언어
*   **Flask**: 경량 웹 프레임워크 (RESTful API 엔드포인트 제공)
*   **Groq**: AI 기반 텍스트 변환 API 클라이언트
*   **Flask-CORS**: 교차 출처 요청 허용을 위한 Flask 확장
*   **python-dotenv**: `.env` 파일에서 환경 변수를 로드하기 위한 라이브러리

## 파일 구조

*   `app.py`: Flask 애플리케이션의 메인 엔트리 포인트. Groq AI API 연동 로직, API 엔드포인트 정의, 정적 파일 서빙 로직이 포함됩니다.
*   `requirements.txt`: 이 백엔드 서비스에 필요한 Python 패키지 의존성 목록입니다.

## 빌드 및 실행

### 전제 조건

*   Python 3.x 설치됨.
*   `pip` (Python 패키지 설치 관리자) 설치됨.
*   **환경 변수 설정**: 프로젝트의 루트 디렉토리 (`C:\gemini-biztalk`)에 `GROQ_API_KEY`를 포함하는 `.env` 파일을 생성해야 합니다.
    ```
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    ```
    *`"YOUR_GROQ_API_KEY"`를 실제 Groq AI API 키로 교체하세요.*

### 설정 및 설치

1.  **프로젝트 루트 디렉토리로 이동합니다:**
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

### 백엔드 서버 실행

1.  **가상 환경이 활성화되었는지 확인하세요.**
2.  **Flask 백엔드 서버를 실행합니다:**
    ```bash
    python backend/app.py
    ```
    서버는 기본적으로 `http://127.0.0.1:5000/`에서 실행되며, 프론트엔드 파일 (`index.html`, CSS, JS 등)과 `/api/convert` 엔드포인트를 제공합니다.

## API 엔드포인트

### `POST /api/convert`

사용자로부터 텍스트와 변환 대상을 받아 Groq AI API를 사용하여 텍스트의 톤을 변환합니다.

*   **요청 메서드**: `POST`
*   **요청 헤더**:
    *   `Content-Type: application/json`
*   **요청 본문 (JSON)**:
    ```json
    {
        "text": "변환할 내용입니다.",
        "target": "상사" // 또는 "동료", "고객"
    }
    ```
*   **응답 본문 (JSON)**:
    *   **성공 시 (200 OK)**:
        ```json
        {
            "original_text": "변환할 내용입니다.",
            "converted_text": "변환된 내용입니다.",
            "target": "상사"
        }
        ```
    *   **오류 시 (400 Bad Request 또는 500 Internal Server Error)**:
        ```json
        {
            "error": "오류 메시지"
        }
        ```

## Groq AI 통합

*   **모델**: `moonshotai/kimi-k2-instruct-0905`
*   **프롬프트 엔지니어링**: `app.py` 내의 `PERSONA_PROMPTS` 딕셔너리에 정의된 시스템 프롬프트를 사용하여 각 대상("Upward", "Lateral", "External")에 맞는 톤 변환을 유도합니다. 클라이언트에서 전달되는 한국어 대상("상사", "동료", "고객")은 이 영어 키로 매핑됩니다.
*   **API 키 보안**: `GROQ_API_KEY`는 `.env` 파일을 통해 로드되며, 서버 측에서만 사용되어 클라이언트에 노출되지 않도록 안전하게 관리됩니다.

## 개발 규칙

*   **환경 변수**: `GROQ_API_KEY`와 같은 중요한 설정은 `.env` 파일을 통해 관리합니다.
*   **CORS**: 개발 편의를 위해 모든 출처에서의 요청을 허용하도록 설정되어 있습니다. 프로덕션 배포 시에는 보안을 위해 특정 도메인으로 제한하는 것이 권장됩니다.
*   **로깅**: `app.logger.error`를 사용하여 Groq API 호출 실패와 같은 중요한 오류를 기록합니다.

## 디렉토리 구조

```
backend/
├── app.py
├── requirements.txt
└── GEMINI.md  (현재 파일)
```
