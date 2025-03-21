import React from 'react';
import '../../public/globals.css';

interface CustomerJourneyMapProps {
  journeyData: {
    awareness: string;
    comparison: string;
    purchase: string;
    installation: string;
  };
}

const CustomerJourneyMap: React.FC<CustomerJourneyMapProps> = ({ journeyData }) => {
  return (
    <div className="journey-map-container">
      <h2 className="journey-map-heading">Customer Journey Map</h2>
      <div className="journey-map-grid">
        <div className="journey-map-section">
          <h4>Awareness</h4>
          <p className="journey-map-box">{journeyData.awareness}</p>
        </div>
        <div className="journey-map-section">
          <h4>Comparison</h4>
          <p className="journey-map-box">{journeyData.comparison}</p>
        </div>
        <div className="journey-map-section">
          <h4>Purchase</h4>
          <p className="journey-map-box">{journeyData.purchase}</p>
        </div>
        <div className="journey-map-section">
          <h4>Installation</h4>
          <p className="journey-map-box">{journeyData.installation}</p>
        </div>
      </div>
    </div>
  );
};

export default CustomerJourneyMap;