from flask_cors import CORS
from flask import Flask, jsonify, request, g
from dotenv import load_dotenv
import mysql.connector
import os
import numpy as np

from recipe_recommendation import recommend_recipe  #recipe recommender function


app = Flask(__name__)
CORS(app)
load_dotenv()

#default route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Dynamic Recipe Generator API!"})

@app.route('/api/ingredients')
def get_ingredients():
    db = db_connect('ingredients')
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT name FROM ingredients WHERE available = 1"
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify({"ingredients": result})
    finally:
        cursor.close()

@app.route('/api/recommend', methods=['GET'])
def recommend():
    print("API1")
    db = db_connect('ingredients')
    cursor = db.cursor()
    try:
        query = "SELECT name FROM ingredients WHERE available = 1"
        cursor.execute(query)
        result = cursor.fetchall()
        ingredients_list = [ingredient[0] for ingredient in result]
    finally:
        cursor.close()
    user_ingredients = ingredients_list #from /api/ingredients route
    print("API2")
    # Call the recommendation function from the imported module
    title, ingredients, instructions = recommend_recipe(user_ingredients)
    print("API3")
    return jsonify({"title": title, "ingredients": ingredients, "instructions": instructions})


#connect to a table
def db_connect(table_name):
    if not hasattr(g, 'db_connections'):
        g.db_connections = {}

    if table_name not in g.db_connections:
        g.db_connections[table_name] = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
        )

    return g.db_connections[table_name]

#automatically close connections
@app.teardown_appcontext
def close_db_connection_recipes(exception=None):
    db_connections = getattr(g, 'db_connections', None)
    if db_connections:
        for conn in db_connections.values():
            conn.close()






if __name__ == '__main__':
    app.run(debug=True)

