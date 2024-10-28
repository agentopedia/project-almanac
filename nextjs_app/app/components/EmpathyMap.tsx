import React from 'react';

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
    <div style={styles.container}>
      <h2 style={styles.heading}>Empathy Map</h2>
      <div style={styles.grid}>
        <div style={styles.section}>
          <h4>Says</h4>
          {empathyData.says.map((text, index) => (
            <p key={index} style={styles.box}>{text}</p>
          ))}
        </div>
        
        <div style={styles.section}>
          <h4>Thinks</h4>
          {empathyData.thinks.map((text, index) => (
            <p key={index} style={styles.box}>{text}</p>
          ))}
        </div>
        
        <div style={styles.section}>
          <h4>Does</h4>
          {empathyData.does.map((text, index) => (
            <p key={index} style={styles.box}>{text}</p>
          ))}
        </div>
        
        <div style={styles.section}>
          <h4>Feels</h4>
          {empathyData.feels.map((text, index) => (
            <p key={index} style={styles.box}>{text}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    maxWidth: '600px',
    margin: '20px auto',
    padding: '20px',
    borderRadius: '8px',
    backgroundColor: '#007bff',
  },
  heading: {
    textAlign: 'center',
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '20px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    borderRadius: '8px',
    padding: '10px',
    backgroundColor: '#222222',
  },
  box: {
    backgroundColor: 'white',
    padding: '8px',
    margin: '5px 0',
    borderRadius: '4px',
    textAlign: 'center',
    color: '#222222',
  },
};

export default EmpathyMap;