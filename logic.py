import pandas as pd

# 1. Dietary Rules
MEAT_KEYWORDS = ['chicken', 'beef', 'pork', 'fish', 'meat', 'lamb', 'bacon', 'shrimp', 'turkey', 'lard']
EGG_KEYWORDS = ['egg', 'mayonnaise', 'meringue', 'custard']

# 2. Indian Cuisine Keywords (Specialized for Indian Student/Mom use case)
INDIAN_KEYWORDS = [
    'curry', 'masala', 'paneer', 'dal', 'roti', 'chana', 'aloo', 'tarka', 
    'biryani', 'raita', 'naan', 'cumin', 'turmeric', 'bhaji', 'korma', 'kadai'
]

def apply_filters(df, mode, student_mode=False):
    """Filters data based on diet, cuisine, and student time constraints."""
    if df is None:
        return pd.DataFrame()
        
    # Always remove meat for this specific app
    mask = df['ingredients'].apply(lambda x: not any(m in str(x).lower() for m in MEAT_KEYWORDS))
    filtered_df = df[mask]
    
    # Mom Mode: Remove Eggs
    if mode == "Mom (Strictly Veg)":
        egg_mask = filtered_df['ingredients'].apply(lambda x: not any(e in str(x).lower() for e in EGG_KEYWORDS))
        filtered_df = filtered_df[egg_mask]
    
    # Indian Filter: Keep only recipes with Indian keywords in the name
    indian_mask = filtered_df['name'].apply(lambda x: any(k in str(x).lower() for k in INDIAN_KEYWORDS))
    filtered_df = filtered_df[indian_mask]

    # Student Mode: Keep only recipes 30 minutes or under
    if student_mode:
        filtered_df = filtered_df[filtered_df['minutes'] <= 30]
        
    return filtered_df

def find_recipes(df, user_input):
    """Matches user ingredients to the filtered dataset."""
    if not user_input or df.empty:
        return pd.DataFrame()
    
    ingredients = [i.strip().lower() for i in user_input.replace(',', ' ').split()]
    mask = df['ingredients'].apply(lambda x: all(item in str(x).lower() for item in ingredients))
    return df[mask].head(6) # Showing top 6 for a balanced 2-column grid