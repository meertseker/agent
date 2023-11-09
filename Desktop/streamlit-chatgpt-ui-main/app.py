import streamlit as st
import requests
import json

# Setting page title and header
st.set_page_config(page_title="MCG", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>MCG - My Country Guide</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Sidebar
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your API Key", type="password")

clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state['message_history'] = []

# API Key Submit Button
api_key_submit = st.sidebar.button("Submit API Key", key="api_submit")

# Store the API key in session state
if api_key_submit:
    st.session_state["api_key"] = api_key

# generate a response
def generate_response(user_input, api_key):
    st.session_state['message_history'].append({"sender": "User", "message": user_input})

    # The prompt for the chatbot
    prompt = ("Sen bir profesyonel yurtdışı eğitim danışmanısın... [rest of the prompt]")

    last_three_messages = st.session_state['message_history'][-3:]
    formatted_message = prompt + ' '.join([f"{msg['sender']}: {msg['message']}" for msg in last_three_messages])
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    data = [{"sender": "User", "message": formatted_message}]

    response = requests.post(
        'https://api.askyourpdf.com/v1/chat/56a35672-daa5-40da-9fd1-f5494d3a3a9f?model_name=GPT4',
        headers=headers, data=json.dumps(data)
    )

    if response.status_code == 200:
        response_json = response.json()
        bot_message = response_json['answer']['message']
        st.session_state['message_history'].append({"sender": "Bot", "message": bot_message})
        return bot_message
    else:
        error_message = f"Error: {response.status_code}"
        try:
            response_json = response.json()
            error_message += f" - {response_json['error']['message']}"
        except:
            error_message += " - No additional error message"
        return error_message

response_container = st.container()

# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    # Check if API Key is available in session state
    api_key_in_session = st.session_state.get("api_key", "")

    if submit_button and user_input and api_key_in_session:
        bot_message = generate_response(user_input, api_key_in_session)

        # Display bot's message
        ##st.write(f"Bot: {bot_message}")

if st.session_state['message_history']:
    with response_container:
        for i, msg in enumerate(st.session_state['message_history']):
            if msg['sender'] == 'User':
                st.markdown(f"<div style='text-align: right; background-color: #e1ffc7; margin: 5px; padding: 10px; border-radius: 10px;'>You: {msg['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; background-color: #e1f7ff; margin: 5px; padding: 10px; border-radius: 10px;'>Bot: {msg['message']}</div>", unsafe_allow_html=True)
