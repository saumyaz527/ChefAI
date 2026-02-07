import pandas as pd
import ollama
import os

# 1. Setup - Tell Python to look for your new file
file_name = 'RAW_recipes.csv'

print("--- ChefAI: Initializing ---")

if os.path.exists(file_name):
    # We load the data. Note: RAW_recipes has columns: name, ingredients, steps, etc.
    print("Loading local cookbook...")
    df = pd.read_csv(file_name)
    print(f"Success! Loaded {len(df):,} recipes.")
else:
    print(f"Error: {file_name} not found.")
    exit()

def get_recommendation(user_input):
    # Step A: Filter the CSV for ingredients
    # We look for recipes that contain the words the user typed
    mask = df['ingredients'].str.contains(user_input, case=False, na=False)
    results = df[mask].head(3) # Get top 3 matches
    
    if results.empty:
        return "No recipes found with those ingredients. Try something else!"

    # Step B: AI Formatting
    # We take the raw text and send it to your local M4 AI to make it sound nice
    recipe_names = results['name'].tolist()
    
    prompt = f"""
    You are a professional chef. A user has these ingredients: {user_input}.
    I found these 3 recipes in my database: {', '.join(recipe_names)}.
    
    Briefly tell the user which one they should cook first and why. 
    Be encouraging!
    """
    
    print("Consulting the AI Chef (Llama 3.2)...")
    response = ollama.generate(model='llama3.2', prompt=prompt)
    return response['response']

# --- RUN THE APP ---
if __name__ == "__main__":
    ingredients = input("\nWhat is in your fridge? (e.g., chicken, eggs, onion): ")
    suggestion = get_recommendation(ingredients)
    
    print("\n--- CHEF'S SUGGESTION ---")
    print(suggestion)