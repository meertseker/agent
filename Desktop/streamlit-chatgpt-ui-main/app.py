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
st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state['message_history'] = []

# generate a response
def generate_response(user_input):
    st.session_state['message_history'].append({"sender": "User", "message": user_input})

    prompt = ("Sen bir profesyonel eğitim danışmanısın. Müşterilerin kanadada almayı planladıkları sehirlerdeki en iyi eğitim merkezlerini, üniversiteleri ve dil okullarını önererek, onlara rehberlik ediyorsun. Fiyatlandırma, burs imkanları, başvuru süreçleri ve yaşam şartları hakkında detaylı bilgi sağlayarak musteriyi memnun ediyorsunmerha, müşterilerin en bilinçli kararı vermelerine yardımcı oluyorsun. Her bir müşteri sorusu geldiğinde, en doğru ve kapsamlı bilgiyi sağlamak için gerekli tüm ayrıntıları sorma ve müşteriyle etkileşimde bulunma sorumluluğuna sahipsin. Müşterilere açık, doğru ve yararlı yanıtlar ver, ve gerektiğinde daha fazla bilgi almak için ek sorular sor.  musteriyi hicbirsey bilmiyor olarak dusun ve sohbetin yonunu sen belirle sorular sorarak tum bildigini anlatmak siteyen biri gibi davran gibi konus ve SAKIN ben bir dil modeliyim deme her müşteri farklı ihtiyaçlara sahip olabilir, bu yüzden her birine özel bir yaklaşım benimsemek önemlidir. Musterinin mesajini/seninle mesaj gecmisini paylasiyorum : ")

    last_three_messages = st.session_state['message_history'][-2:]
    formatted_message = prompt + ' '.join([f"{msg['sender']}: {msg['message']}" for msg in last_three_messages])
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'ask_252fb9047ce742d3982e79de34cf0ad6'
    }

    data = [{"sender": "User", "message": formatted_message}]

    response = requests.post(
        'https://api.askyourpdf.com/v1/chat/56a35672-daa5-40da-9fd1-f5494d3a3a9f?model_name=GPT3',
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

    if submit_button and user_input:
        bot_message = generate_response(user_input)  # changed output to bot_message

        # Add this block to write bot's message when user submits a message
        ##st.write(f"Bot: {bot_message}")
if st.session_state['message_history']:
    with response_container:
        for i, msg in enumerate(st.session_state['message_history']):  # use the original message history order
            if msg['sender'] == 'User':
                st.markdown(f"<div style='text-align: right; background-color: #e1ffc7; margin: 5px; padding: 10px; border-radius: 10px;'>You: {msg['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; background-color: #e1f7ff; margin: 5px; padding: 10px; border-radius: 10px;'>Bot: {msg['message']}</div>", unsafe_allow_html=True)
