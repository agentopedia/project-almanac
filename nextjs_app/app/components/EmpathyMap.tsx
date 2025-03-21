import React from 'react';
import '../../public/globals.css';

interface EmpathyMapProps {
  empathyData: {
    says: string[];
    thinks: string[];
    does: string[];
    feels: string[];
  };
}

const EmpathyMap: React.FC<EmpathyMapProps> = ({ empathyData }) => {
  return (
    <div className="empathy-map-container">
      <h2 className="empathy-map-heading">Empathy Map</h2>
      <div className="empathy-map-grid">
        <div className="empathy-map-section">
          <h4>Says</h4>
          {empathyData.says.map((text, index) => (
            <p key={index} className="empathy-map-box">{text}</p>
          ))}
        </div>
        
        <div className="empathy-map-section">
          <h4>Thinks</h4>
          {empathyData.thinks.map((text, index) => (
            <p key={index} className="empathy-map-box">{text}</p>
          ))}
        </div>
        
        <div className="empathy-map-section">
          <h4>Does</h4>
          {empathyData.does.map((text, index) => (
            <p key={index} className="empathy-map-box">{text}</p>
          ))}
        </div>
        
        <div className="empathy-map-section">
          <h4>Feels</h4>
          {empathyData.feels.map((text, index) => (
            <p key={index} className="empathy-map-box">{text}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EmpathyMap;