import React, { useState } from 'react';

const PropertySearch = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [city, setCity] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchQuery) params.append('search', searchQuery);
    if (propertyType) params.append('property_type', propertyType);
    if (city) params.append('city', city);
    if (minPrice) params.append('min_price', minPrice);
    if (maxPrice) params.append('max_price', maxPrice);
    
    window.location.href = `/properties/?${params.toString()}`;
  };

  return (
    <div className="modern-search-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-group">
          <i className="fas fa-search search-icon"></i>
          <input
            type="text"
            placeholder="Rechercher une propriété, une ville..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>
        <div className="search-filters">
          <select
            value={propertyType}
            onChange={(e) => setPropertyType(e.target.value)}
            className="filter-select"
          >
            <option value="">Tous les types</option>
            <option value="house">Maison</option>
            <option value="apartment">Appartement</option>
            <option value="residence">Résidence</option>
            <option value="villa">Villa</option>
            <option value="studio">Studio</option>
          </select>
          <input
            type="text"
            placeholder="Ville"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="filter-input"
          />
          <input
            type="number"
            placeholder="Prix min"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            className="filter-input"
          />
          <input
            type="number"
            placeholder="Prix max"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            className="filter-input"
          />
          <button type="submit" className="search-button">
            <i className="fas fa-search me-2"></i>Rechercher
          </button>
        </div>
      </form>
    </div>
  );
};

export default PropertySearch;

