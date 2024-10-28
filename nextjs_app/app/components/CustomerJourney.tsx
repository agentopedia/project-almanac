import React from 'react';

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
    <div style={styles.container}>
      <h2 style={styles.heading}>Customer Journey Map</h2>
      <div style={styles.grid}>
        <div style={styles.section}>
          <h4>Awareness</h4>
          <p style={styles.box}>{journeyData.awareness}</p>
        </div>
        <div style={styles.section}>
          <h4>Comparison</h4>
          <p style={styles.box}>{journeyData.comparison}</p>
        </div>
        <div style={styles.section}>
          <h4>Purchase</h4>
          <p style={styles.box}>{journeyData.purchase}</p>
        </div>
        <div style={styles.section}>
          <h4>Installation</h4>
          <p style={styles.box}>{journeyData.installation}</p>
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

export default CustomerJourneyMap;