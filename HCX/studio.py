from flask import Flask, request, jsonify, render_template
import hashlib
import hmac
import base64
import time
import requests
import json

app = Flask(__name__)

class CompletionExecutor:
    def __init__(self, user_question):
        self.user_question = user_question
        self.studio_host = 'https://clovastudio.stream.ntruss.com'
        self.studio_api_key = ''  
        self.studio_api_key_primary_val = ''
        self.studio_request_id = ''

    def send_question_to_studio_api(self):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self.studio_api_key,
            'X-NCP-APIGW-API-KEY': self.studio_api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self.studio_request_id,
            'Content-Type': 'application/json; charset=utf-8'
        }

        request_data = {
            'messages': [{"role": "system", "content": ""}, {"role": "user", "content": self.user_question}],
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1024,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        response = requests.post(self.studio_host + '/testapp/v1/chat-completions/HCX-003', headers=headers, json=request_data)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f"Studio API Error: {response.status_code}, Message: {response.text}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_question():
    data = request.json
    user_question = data.get('user_question')
    if not user_question:
        return jsonify({'error': '질문이 제공되지 않았습니다'}), 400

    integration = CompletionExecutor(user_question)
    response = integration.send_question_to_studio_api()
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
