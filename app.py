import os
import asyncio
import streamlit as st
from PIL import Image

from gpt import generate_response, API_KEY

st.set_page_config(page_title="🐚 GitaGPT")
image = Image.open("krishna.png")

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

with st.sidebar:
    st.title("🐚 GitaGPT")
    st.write("Gita GPT is a GPT-4 powered app that generates answers to your life issues from the Bhagavad Gita.")
    st.image(image)

    st.button('Clear Chat History', on_click=clear_chat_history)
    # if 'API_TOKEN' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     api_token = st.secrets['API_TOKEN']
    # else:
    #     api_token = st.text_input('Enter API token:', type='password')
    #     if not api_token.startswith('sk-'):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    #         st.success('Proceed to entering your prompt message!', icon='👉')
    # os.environ['API_TOKEN'] = api_token

    # st.subheader('Models')

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
if st.session_state.messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(generate_response(prompt))
            placeholder = st.empty()
            # full_response = ''
            # for item in response:
            #     full_response += item
            #     placeholder.markdown(full_response)
            placeholder.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)