import streamlit as st
import requests
import datetime

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

st.set_page_config(page_title="Brickmate Chatbot Service", page_icon="🤖")

# Improved CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 0;
        margin: 0;
        display: flex;
        justify-content: center;
    }
    .chat-container {
        width: 100%;
        max-width: 800px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-bubble {
        border-radius: 10px;
        padding: 10px;
        display: inline-block;
        max-width: 70%;
        word-wrap: break-word;
        white-space: pre-wrap;
        position: relative;
    }
    .chat-bubble-user {
        background-color: #dcf8c6;
        align-self: flex-end;
        text-align: right;
    }
    .chat-bubble-bot {
        background-color: #f1f0f0;
        align-self: flex-start;
        text-align: left;
    }
    .chat-bubble::after {
        content: "";
        position: absolute;
        width: 0;
        height: 0;
        border-style: solid;
    }
    .chat-bubble-user::after {
        border-width: 0 0 15px 15px;
        border-color: transparent transparent #dcf8c6 transparent;
        top: 0;
        right: -15px;
    }
    .chat-bubble-bot::after {
        border-width: 15px 15px 0 0;
        border-color: #f1f0f0 transparent transparent transparent;
        top: 0;
        left: -15px;
    }
    .chat-input-container {
        display: flex;
        justify-content: space-between;
        align-items: center;

        background: white;
        box-shadow: 0 -4px 8px rgba(0,0,0,0.1);
        border-radius: 10px;
        width: 100%;
    }
    .chat-input {
        flex-grow: 1;
        padding: 40px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .send-button {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-left: 10px;
    }
    .send-button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
    .user-icon, .bot-icon {
        border-radius: 50%;
        width: 40px;
        height: 40px;
        margin: 5px;
    }
    .chat-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .chat-row.user {
        flex-direction: row-reverse;
    }
    .timestamp {
        font-size: 0.8em;
        color: #999;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-container'><h2 style='text-align: center;'>Brickmate Chatbot</h2></div>", unsafe_allow_html=True)

def send_question():
    user_question = st.session_state['user_input']
    if user_question:
        response = requests.post(
            'http://localhost:4000/send',
            json={'user_question': user_question}
        )
        if response.status_code == 200:
            response_data = response.json()
            bot_response = extract_bot_response(response_data)
            st.session_state['conversation'].append({"user": user_question, "bot": bot_response, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        else:
            st.session_state['conversation'].append({"user": user_question, "bot": "Error: Unable to get response from server.", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        st.session_state['user_input'] = ""  # Clear input field after sending

def extract_bot_response(response):
    try:
        if 'bubbles' in response and 'data' in response['bubbles'][0]:
            return response['bubbles'][0]['data'].get('description', "Sorry, I couldn't understand the response.")
        if 'result' in response and 'message' in response['result']:
            return response['result']['message'].get('content', "Sorry, I couldn't understand the response.")
        return "Sorry, I couldn't understand the response."
    except (IndexError, KeyError, TypeError) as e:
        return f"Error: {e}"

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display the conversation history
for chat in st.session_state['conversation']:
    st.markdown(f'''
    <div class="chat-row user">
        <div class="chat-bubble chat-bubble-user">{chat["user"]}</div>
        <img class="user-icon" src="https://www.gravatar.com/avatar?d=mp&s=40" alt="user icon">
    </div>
    <div class="timestamp" style="text-align: right;">{chat["timestamp"]}</div>
    <div class="chat-row bot">
        <img class="bot-icon" src="https://kr.object.ncloudstorage.com/bm-arnold/brickmate.gif" alt="bot icon">
        <div class="chat-bubble chat-bubble-bot">{chat["bot"]}</div>
    </div>
    <div class="timestamp">{chat["timestamp"]}</div>
    ''', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input field for user question and send button
st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
user_input = st.text_input("Your question:", key="user_input", placeholder="질문을 입력하세요.", label_visibility='collapsed')
send_button = st.button("Send", on_click=send_question, disabled=not user_input.strip())
st.markdown("</div>", unsafe_allow_html=True)
