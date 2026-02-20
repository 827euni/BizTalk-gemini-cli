
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# 모든 출처에서의 CORS 요청 허용. 실제 서비스에서는 특정 출처만 허용하도록 설정 권장.
CORS(app)

@app.route('/')
def health_check():
    return "BizTone Converter Backend is Running!"

@app.route('/convert', methods=['POST'])
def convert_text():
    data = request.get_json()
    user_input = data.get('text')
    target_tone = data.get('tone')

    if not user_input or not target_tone:
        return jsonify({"error": "텍스트와 변환 톤을 모두 제공해야 합니다."}), 400

    # TODO: Groq AI API 연동 로직 구현 (현재는 더미 응답)
    # 실제 Groq AI API 호출 및 응답 처리 로직이 여기에 들어갑니다.
    # 예시:
    # groq_api_key = os.getenv("GROQ_API_KEY")
    # if not groq_api_key:
    #     return jsonify({"error": "GROQ_API_KEY가 설정되지 않았습니다."}), 500
    #
    # try:
    #     client = Groq(api_key=groq_api_key)
    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": f"다음 텍스트를 '{target_tone}' 톤으로 변환해줘: {user_input}",
    #             }
    #         ],
    #         model="mixtral-8x7b-32768", # 또는 다른 적절한 모델
    #     )
    #     converted_text = chat_completion.choices[0].message.content
    #     return jsonify({"converted_text": converted_text})
    # except Exception as e:
    #     return jsonify({"error": f"API 호출 중 오류 발생: {str(e)}"}), 500

    # 더미 응답
    if target_tone == '상사':
        converted_text = f"상사 보고용으로 변환된 내용: {user_input}"
    elif target_tone == '타팀 동료':
        converted_text = f"동료 협업용으로 변환된 내용: {user_input}"
    elif target_tone == '고객':
        converted_text = f"고객 응대용으로 변환된 내용: {user_input}"
    else:
        converted_text = f"알 수 없는 톤으로 변환 시도: {user_input}"

    return jsonify({"converted_text": converted_text})

if __name__ == '__main__':
    # 개발 환경에서만 디버그 모드 활성화
    app.run(debug=True, port=5000)
