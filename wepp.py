import streamlit as st
import pandas as pd
import os
from logic import apply_filters, find_recipes 

# Safe Ollama Import: This prevents the "ModuleNotFoundError" on the web
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
    # Priority: mini_recipes.csv (for web), then RAW_recipes.csv (for local)
    if os.path.exists('mini_recipes.csv'):
        file_path = 'mini_recipes.csv'
    elif os.path.exists('RAW_recipes.csv'):
        file_path = 'RAW_recipes.csv'
    else:
        return None
        
    return pd.read_csv(file_path, usecols=['name', 'ingredients', 'minutes', 'steps'])

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ App Controls")
    mode = st.radio("Cooking Mode", ["Mom (Strictly Veg)", "Me (Eggetarian)"])
    student_mode = st.toggle("🎓 Student Friendly (Under 30m)", value=True)
    st.divider()
    
    # Hidden Apology Feature
    pw = st.text_input("Secret Code", type="password", help="Try 'sorry'")
    if pw.lower() == "sorry":
        st.balloons()
        st.success("✨ I'm working hard to grow and improve. I hope this app shows that.")

# --- 5. SEARCH SECTION ---
user_input = st.text_input("🔍 Search for a dish", placeholder="e.g., Paneer, Dal, Aloo")

# --- 6. RESULTS SECTION ---
if df is not None and user_input:
    safe_df = apply_filters(df, mode, student_mode)
    results = find_recipes(safe_df, user_input)
    
    if not results.empty:
        # Metrics
        m1, m2 = st.columns(2)
        m1.metric("Recipes Found", len(results))
        m2.metric("Quickest", f"{results['minutes'].min()} mins")
        
        st.divider()

        # Simple List Display (Most stable for web)
        for i, (index, row) in enumerate(results.iterrows()):
            with st.expander(f"⭐ {row['name'].title()}", expanded=(i==0)):
                st.write(f"⏱️ **Time:** {row['minutes']} mins")
                st.info(f"**Ingredients:** {row['ingredients']}")
                st.write("**Method:**")
                st.write(row['steps'])
        
        # --- 7. AI CHEF