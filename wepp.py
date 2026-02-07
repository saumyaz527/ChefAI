import streamlit as st
import pandas as pd
import ollama
import os
from logic import apply_filters, find_recipes 

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="The Vidhushka Kitchen", page_icon="🥘", layout="wide")

# --- 2. HEADER ---
st.title("🥘 The Vidhushka Kitchen")
st.markdown("### *Custom Indian Recipes for Only ones who take care of me*")
st.divider()

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'RAW_recipes.csv'
    if os.path.exists(file_path):
        # Optimized: Loading only what we need
        return pd.read_csv(file_path, usecols=['name', 'ingredients', 'minutes', 'steps'])
    return None

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ App Controls")
    mode = st.radio("Cooking Mode", ["Vegetarian", "Eggetarian"])
    student_mode = st.toggle("🎓 Student Friendly (Under 30m)", value=True)
    st.divider()
    st.info("Built for a heartfelt apology by a asshole developer who hurts their loved ones | Feb 2026")

# --- 5. SEARCH SECTION ---
# Centering the search bar using columns
left_spacer, center_info, right_spacer = st.columns([1, 2, 1])
with center_info:
    user_input = st.text_input("🔍 What ingredients do you have?", placeholder="e.g., Paneer, Potato, Rice")

# --- 6. RESULTS SECTION ---
if df is not None and user_input:
    safe_df = apply_filters(df, mode, student_mode)
    results = find_recipes(safe_df, user_input)
    
    if not results.empty:
        # Dashboard Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Recipes Found", len(results))
        m2.metric("Quickest", f"{results['minutes'].min()} mins")
        m3.metric("Diet", mode.split('(')[0])
        
        st.divider()

        # Grid Layout (2 Recipes per row)
        for i in range(0, len(results), 2):
            col_left, col_right = st.columns(2)
            
            # Left Column Recipe
            with col_left:
                row = results.iloc[i]
                with st.expander(f"⭐ {row['name'].title()}", expanded=True):
                    st.write(f"⏱️ **Ready in:** {row['minutes']} mins")
                    st.info(f"**Ingredients:** {row['ingredients']}")
                    st.write("**Method:**")
                    st.write(row['steps'])
            
            # Right Column Recipe (if it exists)
            if i + 1 < len(results):
                with col_right:
                    row = results.iloc[i+1]
                    with st.expander(f"⭐ {row['name'].title()}", expanded=True):
                        st.write(f"⏱️ **Ready in:** {row['minutes']} mins")
                        st.info(f"**Ingredients:** {row['ingredients']}")
                        st.write("**Method:**")
                        st.write(row['steps'])
        
        # --- 7. AI CHEF ADVICE ---
        st.divider()
        st.subheader("🧙‍♂️ AI Chef's Secret Tip")
        if st.button("Generate Secret Tip"):
            with st.spinner("Analyzing ingredients..."):
                try:
                    persona = "student" if student_mode else "home cook"
                    prompt = f"I am a {persona}. Give me one pro tip for {results.iloc[0]['name']}."
                    response = ollama.generate(model='llama3.2', prompt=prompt)
                    st.success(response['response'])
                except:
                    st.error("Make sure Ollama is running with Llama 3.2!")
    else:
        st.warning("No recipes found. Try searching for simpler ingredients like 'Aloo' or 'Rice'.")