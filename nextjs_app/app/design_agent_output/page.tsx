"use client";
import Link from 'next/link';
import EmpathyMap from '../components/EmpathyMap';
import CustomerJourney from '../components/CustomerJourney';
import CustomerPersona from '../components/CustomerPersona';
import { useRouter } from 'next/navigation';
import JSON5 from 'json5';
import { useEffect, useState } from "react";
import '../styles/agents.css';

interface CustomerPersona {
  name: string;
  demographics: {
    age: number;
    gender: string;
    occupation: string;
  };
  description: string;
}

interface ParsedData {
  customer_persona: CustomerPersona[];
  empathy_map: {
    says: string[];
    thinks: string[];
    does: string[];
    feels: string[];
  };
  customer_journey_map: {
    awareness: string;
    comparison: string;
    purchase: string;
    installation: string;
  };
  problem_statement: string;
}

const defaultPersona: CustomerPersona = {
  name: "Loading...",
  demographics: {
    age: 0,
    gender: "Loading...",
    occupation: "Loading..."
  },
  description: "Loading..."
};

const defaultEmpathyData = {
  says: ["Loading..."],
  thinks: ["Loading..."],
  does: ["Loading..."],
  feels: ["Loading..."]
};

const defaultJourneyMap = {
  awareness: 'Loading...',
  comparison: 'Loading...',
  purchase: 'Loading...',
  installation: 'Loading...',
};


export default function DesignThinkingAgentOutput() {
  const [loading, setLoading] = useState(false);
  const [parsedData, setParsedData] = useState<ParsedData | null>(null);
  const [persona, setPersona] = useState<CustomerPersona>(defaultPersona);
  const [originalPersona, setOriginalPersona] = useState<CustomerPersona | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function fetchLastMessage() {
      try {
        const response = await fetch("/api/design_input");
        if (!response.ok) {
          throw new Error("Failed to fetch last message");
        }
        const data = await response.json();
        console.log("Fetched data:", data);
  
        const parsed = JSON5.parse(data.result);
        setParsedData(parsed);
  
        // Load persona from API response
        if (parsed?.customer_persona?.length > 0) {
          setPersona(parsed.customer_persona[0]); // load the latest persona
        }
      } catch (error) {
        console.error("Error fetching last message:", error);
      }
    }
  
    fetchLastMessage();
  }, []);  

  console.log('Parsed Data:', parsedData)

  const handleProceed = async () => {
    setLoading(true); // show loading screen

    try {
      // make a GET request to the Next.js API route
      const response = await fetch("/api/viability", {
        method: "GET",
      });
      const data = await response.json();
  
      if (response.ok) {
        console.log("PRD from Flask server:", data);
        const encodedData = encodeURIComponent(JSON.stringify(data));
        router.push(`/product_viability_agent?data=${encodedData}`);
      } else {
        console.error("Failed to fetch data:", data);
      }
    } catch (error) {
      console.error("Error during the GET request:", error);
    } finally {
      setLoading(false); // hide loading screen
    }
  };  
  
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        color: "white",
        textAlign: "center",
      }}
    >
      {/* Loading Screen */}
      {loading && (
        <div className="loading-overlay" role="status" aria-busy="true">
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span className="spinner" />
            <p style={{ marginTop: '1rem' }}>Loading Product Viability Agent...</p>
          </div>
        </div>
      )}

      <main style={{ width: "80%" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>

        {/* Customer Persona Section */}
        <CustomerPersona persona={persona} onUpdatePersona={setPersona} />

        <div
          style={{
            display: "flex",
            justifyContent: "space-between", // space btwn the components
            gap: "1rem"
          }}
        >
          {/* Empathy Map */}
          <EmpathyMap empathyData={parsedData?.empathy_map || defaultEmpathyData} />

          {/* Customer Journey Map */}
          <CustomerJourney journeyData={parsedData?.customer_journey_map || defaultJourneyMap} />
        </div>

        {/* Navigation Buttons */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "2rem",
          }}
        >
          <button
            onClick={() => router.push("/design_agent_input")}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "var(--primary-color)",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Back to Product Ideation
          </button>
          <button
            onClick={handleProceed}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "var(--primary-color)",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Proceed to Product Viability Agent
          </button>
        </div>
      </main>
    </div>
  );
}