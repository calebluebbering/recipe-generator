import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function IngredientsPage() {
  const [ingredients, setIngredients] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch ingredients from the backend
  useEffect(() => {
    fetch('http://localhost:5000/api/ingredients')  // Make sure the backend is running on localhost:5000
      .then(response => response.json())
      .then(data => {
        setIngredients(data.ingredients);  // Set ingredients to the state
        setLoading(false);  // Stop loading
      })
      .catch((error) => {
        console.error("Error fetching ingredients:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Ingredients List</h1>
      <ul>
        {ingredients.map((ingredient, index) => (
          <li key={index}>
            {ingredient.name} - {ingredient.category}
          </li>
        ))}
      </ul>
      <div>
        <Link to="/">Home</Link>
      </div>
    </div>
  );
}

export default IngredientsPage;
