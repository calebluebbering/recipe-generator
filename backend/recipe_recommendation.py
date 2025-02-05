from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd
print("API2.1")
# Load train dataset
# Load the JSON file
with open('recipes_raw/recipes_raw_nosource_fn.json', 'r') as file:
    data = json.load(file)

# Reformat the JSON data
recipes = []
for recipe_id, recipe in data.items():
    # Check if 'ingredients' key exists
    if 'ingredients' in recipe:
        recipes.append({
            "id": recipe_id,
            "ingredients": recipe["ingredients"],
            "instructions": recipe.get("instructions", ""),  # Use .get() to handle missing keys
            "title": recipe.get("title", "Untitled")         # Default title if missing
        })


# Create a DataFrame
train_df = pd.DataFrame(recipes)

# Process the 'ingredients' column to convert lists into strings
train_df['ingredients'] = train_df['ingredients'].apply(lambda x: ' '.join(x))
print("API2.2")
# Initialize the TF-IDF vectorizer and vectorize ingredients
vectorizer = TfidfVectorizer(stop_words='english')
print("API2.3")
X_train = vectorizer.fit_transform(train_df['ingredients'])
print("API2.4")
# Define the recommendation function
def recommend_recipe(user_ingredients):
    print("API2.5")
    print(type(user_ingredients))  # Should print: <class 'list'>
    print(user_ingredients) 
    user_ingredients_str = ', '.join(user_ingredients)
    print("API2.6")
    # Vectorize the user’s input ingredients
    user_input_vec = vectorizer.transform([user_ingredients_str])
    print("API2.7")
    # Calculate cosine similarity between user input and recipe ingredients
    similarities = cosine_similarity(user_input_vec, X_train)
    print("API2.8")
    # Get the index of the most similar recipe
    best_match_index = similarities.argmax()
    print("API2.9")
    # Return the recommended recipe's cuisine and id
    return train_df.iloc[best_match_index]['title'], train_df.iloc[best_match_index]['ingredients'], train_df.iloc[best_match_index]['instructions']