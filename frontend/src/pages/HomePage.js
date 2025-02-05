import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import RandomImage from './RandomImage.js'

function HomePage() {
    const [ingredients, setIngredients] = useState([]);
    const [selectedIngredients, setSelectedIngredients] = useState([]);
    const [recommendedRecipe, setRecommendedRecipe] = useState(null);

    // Fetch ingredients from backend
    useEffect(() => {
        fetch('http://localhost:5000/api/ingredients')
            .then((response) => response.json())
            .then((data) => setIngredients(data.ingredients));
    }, []);

    // Handle ingredient selection
    const handleIngredientSelect = (ingredient) => {
        setSelectedIngredients((prev) => [...prev, ingredient]);
    };

    // Send selected ingredients to backend for recipe recommendation
    const handleRecommend = () => {
        // Simply call the recommendation endpoint without any ingredients
        fetch('http://localhost:5000/api/recommend')
            .then((response) => response.json())
            .then((data) => {
                console.log("Received recommendation:", data);
                setRecommendedRecipe(data); // Assuming you want to store the recommendation in state
            })
            .catch((error) => console.error('Error:', error));
    };

    return (
        <div>
            <h1>Home Page - Recipe Recommendation</h1>

            <button onClick={handleRecommend}>Get Recipe Recommendation</button>

            {recommendedRecipe && (
                <div>
                    <h2>{recommendedRecipe.title}</h2>
                    <RandomImage title={recommendedRecipe.title} />
                    <h3>Ingredients</h3>
                    <p>{recommendedRecipe.ingredients}</p>
                    <h3>Instructions</h3>
                    <p>{recommendedRecipe.instructions}</p>
                </div>
            )}
            <div>
                <Link to="/ingredients">Update Ingredients</Link>
            </div>
        </div>
    );
}

export default HomePage;
