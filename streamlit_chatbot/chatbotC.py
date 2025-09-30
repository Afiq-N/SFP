# app.py
import os
import re
import streamlit as st
import google.generativeai as genai

# -------- CONFIGURATION --------
import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
API_KEY = st.secrets["API"]

# Configure Gemini with the secret key
genai.configure(api_key=API_KEY)

# Create model handle
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

SYSTEM_PERSONA = (
    "When given a single-word mood (example: 'joy', 'melancholy', 'anxious'), "
    "you must return exactly one hexadecimal color code in the format #RRGGBB "
    "that best represents the mood otherwise choose color hex that correlates with the word."
)

FALLBACK_COLORS = {
    "happy": "#FFD54F",
    "joy": "#FFD54F",
    "sad": "#4A6FA5",
    "melancholy": "#375E7C",
    "angry": "#D93025",
    "fear": "#5C3C92",
    "calm": "#88C0A4",
    "relaxed": "#A8D5BA",
    "anxious": "#A46A6A",
    "romantic": "#E76E98",
    "bored": "#9E9E9E",
    "excited": "#FF7043",
    "confident": "#2E7D32",
    "lonely": "#6B7AA1",
    "nostalgic": "#C0905E",
    "hopeful": "#7CB342",
    "curious": "#5DA3FF",
    "neutral": "#BDBDBD"
}

HEX_RE = re.compile(r"#([0-9a-fA-F]{6})")

def parse_hex_from_text(text: str) -> str | None:
    if not text:
        return None
    m = HEX_RE.search(text)
    if m:
        return f"#{m.group(1).upper()}"
    return None

def fallback_for_word(word: str) -> str:
    key = word.strip().lower()
    return FALLBACK_COLORS.get(key, "#D41273")

def ask_gemini_for_hex(word: str) -> str | None:
    prompt = (
        SYSTEM_PERSONA + "\n\n"
        f"Input word: \"{word}\"\n\n"
        "Return only a single hex color in uppercase #RRGGBB format."
    )
    try:
        response = model.generate_content(prompt)
        response_text = getattr(response, "text", None) or str(response)
    except Exception:
        return None
    return parse_hex_from_text(response_text)

# -------- STREAMLIT UI --------
st.set_page_config(page_title="Color of THE Day", layout="centered")

st.title("🎨 Color of THE Day")
st.caption("Type exactly ONE word describing your mood; I will return a hex color code representing it.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form("mood_form", clear_on_submit=True):
    word_input = st.text_input("One word (mood):", value="", placeholder="e.g. joy, sad, anger")
    submitted = st.form_submit_button("Get your color")

if submitted:
    word = word_input.strip()
    if not word:
        st.error("Please type a word.")
    elif " " in word:
        st.error("Please enter exactly one word and no space(s).")
    else:
        with st.spinner("Gemini is thinking... Please wait..."):
            hexcode = ask_gemini_for_hex(word)

        used_fallback = False
        if not hexcode:
            used_fallback = True
            hexcode = fallback_for_word(word)

        # Save to session history
        st.session_state.messages.append({"word": word, "hex": hexcode, "fallback": used_fallback})

        # Show result
        st.success(f"✅ Found a color for **{word}**: `{hexcode}`")
        st.markdown(
            f"""
            <div style="margin-top:12px; padding:20px; border-radius:8px;
            background:{hexcode}; width:180px; height:100px; border:1px solid #ccc"></div>
            """,
            unsafe_allow_html=True,
        )
        

# Conversation history viewer
if st.session_state.messages:
    st.markdown("---")
    st.subheader("History")

    for i, m in enumerate(reversed(st.session_state.messages[-20:]), 1):
        with st.expander(f"{i}. {m['word']} → {m['hex']} {'(fallback)' if m['fallback'] else ''}"):
            # Show the hex code
            st.markdown(f"**Hex Code:** `{m['hex']}`")

            # Show color preview
            st.markdown(
                f"""
                <div style="margin-top:8px; padding:15px; border-radius:6px;
                background:{m['hex']}; width:150px; height:80px; border:1px solid #ccc"></div>
                """,
                unsafe_allow_html=True,
            )



# -------- Persist Theme Selection --------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"  # default

with st.sidebar:
    st.title("Settings")
    theme = st.radio(
        "Choose Theme:",
        ["Light", "Dark"],
        index=["Light", "Dark"].index(st.session_state.theme),
        key="theme"
    )

# Apply CSS based on theme
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e !important;
            color: #f5f5f5 !important;
        }
        .stTextInput > div > div > input {
            background-color: #333333 !important;
            color: #f5f5f5 !important;
        }
        /* Fix button contrast */
        div.stButton > button:first-child {
            background-color: #3a3a3a !important;
            color: #ffffff !important;
            border: 1px solid #777777 !important;
        }
        div.stButton > button:first-child:hover {
            background-color: #555555 !important;
            border: 1px solid #aaaaaa !important;
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:  # Light mode
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        /* Light button */
        div.stButton > button:first-child {
            background-color: #f5f5f5 !important;
            color: #000000 !important;
            border: 1px solid #cccccc !important;
        }
        div.stButton > button:first-child:hover {
            background-color: #e0e0e0 !important;
            border: 1px solid #999999 !important;
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
