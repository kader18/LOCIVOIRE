import React from 'react';
import ReactDOM from 'react-dom/client';
import PropertySearch from './components/PropertySearch';
import PropertyCard from './components/PropertyCard';

// Exposer les composants globalement pour utilisation dans les templates Django
window.PropertySearch = PropertySearch;
window.PropertyCard = PropertyCard;
window.React = React;
window.ReactDOM = ReactDOM;

// Auto-initialiser les composants React sur les pages
document.addEventListener('DOMContentLoaded', function() {
  // Initialiser PropertySearch si l'élément existe
  const searchContainer = document.getElementById('react-search-container');
  if (searchContainer) {
    const root = ReactDOM.createRoot(searchContainer);
    root.render(<PropertySearch />);
  }

  // Initialiser PropertyCard pour chaque propriété
  document.querySelectorAll('.react-property-card').forEach(card => {
    const propertyId = card.dataset.propertyId;
    const propertyData = JSON.parse(card.dataset.propertyData);
    const root = ReactDOM.createRoot(card);
    root.render(<PropertyCard property={propertyData} />);
  });
});
