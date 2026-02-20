import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# CORS 설정: 모든 도메인에서 오는 요청을 허용합니다.
# 실제 프로덕션 환경에서는 특정 도메인만 허용하도록 수정해야 합니다.
CORS(app)

# Groq 클라이언트 초기화 (API 키는 환경 변수에서 가져옵니다)
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 대상별 프롬프트 정의 (한국어)
PERSONA_PROMPTS = {
    "Upward": {
        "system": "당신은 상사에게 보고하는 어조로 텍스트를 변환하는 전문 비서입니다. 다음 텍스트를 명확하고 정중하며 격식 있는 보고체로 바꿔주세요. 결론부터 제시하고, 핵심 내용을 간결하게 전달해야 합니다.",
        "user_template": "{text}"
    },
    "Lateral": {
        "system": "당신은 타팀 동료와 협업하는 어조로 텍스트를 변환하는 전문 코치입니다. 다음 텍스트를 친절하고 상호 존중하는 어투로 바꿔주세요. 요청 사항과 마감 기한을 명확히 전달하며, 협조를 구하는 형태로 변환해야 합니다.",
        "user_template": "{text}"
    },
    "External": {
        "system": "당신은 고객에게 응대하는 어조로 텍스트를 변환하는 전문 상담사입니다. 다음 텍스트를 극존칭을 사용하며, 전문성과 서비스 마인드를 강조하는 형태로 바꿔주세요. 안내, 공지, 사과 등의 목적에 부합하게 변환해야 합니다.",
        "user_template": "{text}"
    }
}

@app.route('/')
def serve_index():
    """
    루트 URL 요청 시 frontend/index.html 파일을 제공합니다.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """
    frontend 폴더 내의 정적 파일들을 제공합니다 (css, js 등).
    """
    return send_from_directory(app.static_folder, path)


@app.route('/api/convert', methods=['POST'])
def convert_tone():
    """
    사용자로부터 텍스트와 변환 대상을 받아, Groq API를 사용하여 톤을 변환하는 API 엔드포인트입니다.
    """
    if not request.json:
        return jsonify({"error": "Request must be JSON"}), 400

    user_text = request.json.get('text')
    target_korean = request.json.get('target') # 클라이언트에서 넘어오는 한국어 대상

    if not user_text or not target_korean:
        return jsonify({"error": "Invalid request. 'text' and 'target' are required."}), 400

    # 한국어 대상을 영어 키로 매핑
    target_mapping = {
        "상사": "Upward",
        "동료": "Lateral",
        "고객": "External"
    }
    target_english = target_mapping.get(target_korean)

    if not target_english or target_english not in PERSONA_PROMPTS:
        return jsonify({"error": "Invalid target. Must be one of '상사', '동료', '고객'."}), 400

    prompt_config = PERSONA_PROMPTS[target_english]
    system_prompt = prompt_config["system"]
    user_prompt = prompt_config["user_template"].format(text=user_text)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            stop=None,
            stream=False
        )

        converted_text = chat_completion.choices[0].message.content.strip()

        return jsonify({
            "original_text": user_text,
            "converted_text": converted_text,
            "target": target_korean
        })

    except Exception as e:
        app.logger.error(f"Groq API Error: {e}")
        return jsonify({"error": "텍스트 변환 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 500

if __name__ == '__main__':
    # 디버그 모드로 Flask 앱을 실행합니다.
    app.run(debug=True, port=5000)