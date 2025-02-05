import React, { useEffect, useState } from 'react';

const RandomImage = ({ title }) => {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      const searchQuery = title.replace(/\s+/g, '+'); // Replace spaces with '+'
      const apiKey = process.env.REACT_APP_UNSPLASH_API_KEY;
      const response = await fetch(
        `https://api.unsplash.com/search/photos?query=${searchQuery}&client_id=${apiKey}`
      );
      const data = await response.json();

      if (data.results && data.results.length > 0) {
        setImageUrl(data.results[0].urls.regular); // Use the first image
      }
    };

    fetchImage();
  }, [title]);

  if (!imageUrl) {
    return <div>Loading...</div>;
  }

  return <img src={imageUrl} alt={title} style={{ width: '20%', height: 'auto' }} />;
};

export default RandomImage;
