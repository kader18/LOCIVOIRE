import React, { useState } from 'react';

const ImageGallery = ({ images, primaryImage }) => {
  const [selectedImage, setSelectedImage] = useState(
    primaryImage || (images && images[0]) || null
  );
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);

  if (!images || images.length === 0) {
    return (
      <div className="image-gallery-placeholder">
        <i className="fas fa-home fa-5x"></i>
        <p>Aucune image disponible</p>
      </div>
    );
  }

  return (
    <div className="modern-image-gallery">
      <div className="main-image-container">
        <img
          src={selectedImage?.url || selectedImage}
          alt="Property"
          className="main-image"
          onClick={() => setIsLightboxOpen(true)}
        />
        <div className="image-overlay">
          <button className="zoom-button" onClick={() => setIsLightboxOpen(true)}>
            <i className="fas fa-expand"></i>
          </button>
        </div>
      </div>
      
      {images.length > 1 && (
        <div className="thumbnail-grid">
          {images.slice(0, 5).map((image, index) => (
            <div
              key={index}
              className={`thumbnail ${selectedImage === image ? 'active' : ''}`}
              onClick={() => setSelectedImage(image)}
            >
              <img src={image?.url || image} alt={`Thumbnail ${index + 1}`} />
            </div>
          ))}
          {images.length > 5 && (
            <div className="thumbnail-more">
              <span>+{images.length - 5}</span>
            </div>
          )}
        </div>
      )}

      {isLightboxOpen && (
        <div className="lightbox" onClick={() => setIsLightboxOpen(false)}>
          <button className="lightbox-close" onClick={() => setIsLightboxOpen(false)}>
            <i className="fas fa-times"></i>
          </button>
          <img src={selectedImage?.url || selectedImage} alt="Property" className="lightbox-image" />
        </div>
      )}
    </div>
  );
};

export default ImageGallery;

