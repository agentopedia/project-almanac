"use client";
import React from 'react';

const FeaturesPage: React.FC = () => {
  return (
    <div>
      <header className="header">
        <h1 className="title">Our Features</h1>
        <p className="subtitle">Subtitle</p>
      </header>

      <section className="features-section">
        <div className="feature-card">
          <h2 className="feature-title">Feature 1</h2>
          <div className="feature-description">
            <p>Description of Feature 1</p>
          </div>
        </div>

        <div className="feature-card">
          <h2 className="feature-title">Feature 2</h2>
          <div className="feature-description">
            <p>Description of Feature 2</p>
          </div>
        </div>

        <div className="feature-card">
          <h2 className="feature-title">Feature 3</h2>
          <div className="feature-description">
            <p>Description of Feature 3</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default FeaturesPage;