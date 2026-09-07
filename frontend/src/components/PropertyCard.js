import React, { useState } from 'react';

const PropertyCard = ({ property }) => {
  const [isHovered, setIsHovered] = useState(false);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('fr-FR').format(price);
  };

  return (
    <div
      className="modern-property-card"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="property-image-container">
        {property.image_url ? (
          <img
            src={property.image_url}
            alt={property.title}
            className="property-image"
          />
        ) : (
          <div className="property-image-placeholder">
            <i className="fas fa-home"></i>
          </div>
        )}
        <div className={`property-overlay ${isHovered ? 'active' : ''}`}>
          <div className="property-badges">
            <span className="badge featured">{property.property_type}</span>
            {property.is_featured && (
              <span className="badge premium">
                <i className="fas fa-star"></i> Premium
              </span>
            )}
          </div>
        </div>
        <div className="property-price-tag">
          {formatPrice(property.price_per_room)} FCFA
        </div>
      </div>
      <div className="property-content">
        <h3 className="property-title">{property.title}</h3>
        <div className="property-location">
          <i className="fas fa-map-marker-alt"></i>
          <span>{property.city}</span>
        </div>
        <div className="property-features">
          <div className="feature">
            <i className="fas fa-bed"></i>
            <span>{property.number_of_rooms} pièces</span>
          </div>
          <div className="feature">
            <i className="fas fa-bath"></i>
            <span>{property.number_of_bathrooms} sdb</span>
          </div>
          {property.area && (
            <div className="feature">
              <i className="fas fa-ruler-combined"></i>
              <span>{property.area} m²</span>
            </div>
          )}
        </div>
        <a
          href={`/properties/${property.id}/`}
          className="property-link"
        >
          Voir les détails
          <i className="fas fa-arrow-right"></i>
        </a>
      </div>
    </div>
  );
};

export default PropertyCard;

