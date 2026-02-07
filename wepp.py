import streamlit as st
import pandas as pd
import os
from logic import apply_filters, find_recipes 

# Try to import ollama, but don't crash if it's missing (important for web link)
try:
    import ollama
except ImportError:
    ollama = None

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Mom's Magic Kitchen", page_icon="🥘", layout="wide")

# --- 2. HEADER ---
st.title("🥘 Mom's Magic Kitchen")
st.markdown("### *Custom Indian Recipes for Mom & Me*")
st.divider()

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    # Use the mini file for the web link, fall back to big file for local
    if os.path.exists('mini_recipes.csv'):
        file_path = 'mini_recipes.csv'
    else:
        file_path = 'RAW_recipes.csv'
        
    if os.path.exists(file_path):
        return pd.read_csv(file_path, usecols=['name', 'ingredients', 'minutes', 'steps'])
    return None

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ App Controls")
    mode = st.radio("Cooking Mode", ["Mom (Strictly Veg)", "Me (Eggetarian)"])
    student_mode = st.toggle("🎓 Student Friendly (Under 30m)", value=True)
    st.divider()
    st.info("Built with ❤️ | Feb 2026")
    
    # Hidden Apology Trigger
    if st.text_input("Secret Code", type="password") == "sorry":
        st.balloons()
        st.write("✨ I'm really sorry. I hope this app shows you I'm trying.")

# --- 5. SEARCH SECTION ---
left_spacer, center_info, right_spacer = st.columns([1, 2, 1])
with