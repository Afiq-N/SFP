##Include the following at the top before writing any code

import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from openai import OpenAI  

DEEPSEEK_API_KEY = "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"


with st.sidebar:
    st.title("Sidebar") 
        
    st.radio("Radio-button select", ["Friendly", "Formal", "Funny"], index=0)
    st.multiselect("Multi-select", ["Movies", "Travel", "Food", "Sports"], default=["Food"])
    st.selectbox("Dropdown select", ["Data", "Code", "Travel", "Food", "Sports"], index=0)
    st.slider("Slider", min_value=1, max_value=200, value=60)
    st.select_slider("Option Slider", options=["Very Sad", "Sad", "Okay", "Happy", "Very Happy"], value="Okay")

user_emoji = "🍌" # Change this to any emojis you like
robot_img = "Robot.jpg" # Find a picture online(jpg/png), download it and drag to
												# your files under the Chatbot folder


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://openrouter.ai/api/v1"
) 

def get_deepseek_r1_response(prompt):
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",  # R1 reasoning model
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("SuperbotR1")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=robot_img):
                st.write(f"{message['content']}")
        else:
            with st.chat_message("user", avatar=user_emoji):
                st.write(f"{message['content']}")


    # Chat input
    if prompt := st.chat_input("What's on your mind"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get Gemini response
        response = get_deepseek_r1_response(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
