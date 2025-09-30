##Include the following at the top before writing any code

import streamlit as st
import pandas as pd
import google.generativeai as genai


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

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyBd9JV4aC7zN3byGKBeekNoHsbzKAg90-c"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

##Find the "get_gemini_response" function in your code and replace it with this function below

def get_gemini_response(prompt, persona_instructions):
    full_prompt = f"{persona_instructions}\n\nUser: {prompt}\nAssistant:"
    response = model.generate_content(full_prompt)
    return response.text

persona_instructions = """You are a female persona who is critical, cynical, and highly factual, with the sharp, analytical temperament of an INTP. You speak with dry wit and skepticism, preferring logic and evidence over sentiment. You challenge assumptions, point out flaws in reasoning, and avoid sugarcoating. While you’re not unkind, you rarely offer comfort — instead, you cut through illusions and present the blunt truth in a concise, precise manner."""

def main():
    st.title("Superbot")
    
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
        response = get_gemini_response(prompt)

        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
