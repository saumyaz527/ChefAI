import pandas as pd

# Keywords to find Indian food
INDIAN_KEYWORDS = ['curry', 'masala', 'paneer', 'dal', 'roti', 'chana', 'aloo', 'tarka', 'biryani', 'raita', 'naan']

try:
    df = pd.read_csv('RAW_recipes.csv')
    
    # Filter for recipes that mention Indian keywords in the name
    indian_df = df[df['name'].str.contains('|'.join(INDIAN_KEYWORDS), case=False, na=False)]
    
    # Take the top 500 Indian recipes
    mini_df = indian_df.head(500)
    
    mini_df.to_csv('mini_recipes.csv', index=False)
    print(f"✅ Success! Created 'mini_recipes.csv' with {len(mini_df)} Indian recipes.")
except Exception as e:
    print(f"❌ Error: {e}")