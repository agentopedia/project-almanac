"use client";
import Link from 'next/link';
import EmpathyMap from '../components/EmpathyMap';
import CustomerJourney from '../components/CustomerJourney';
import { useRouter } from 'next/navigation';
import JSON5 from 'json5';
import { useEffect, useState } from "react";

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
  name: "",
  demographics: {
    age: 0,
    gender: "",
    occupation: ""
  },
  description: ""
};

const defaultEmpathyData = {
  says: [""],
  thinks: [""],
  does: [""],
  feels: [""]
};

const defaultJourneyMap = {
  awareness: '',
  comparison: '',
  purchase: '',
  installation: '',
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setPersona((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleDemographicsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPersona((prev) => ({
      ...prev,
      demographics: {
        ...prev.demographics,
        [name]: value
      }
    }));
  };

  const handleEdit = () => {
    setOriginalPersona({ ...persona }); // store current state before editing
    setIsEditing(true);
  };  

  const handleCancel = () => {
    if (originalPersona) {
      setPersona(originalPersona); // restore original data
    }
    setIsEditing(false);
  };  

  const handleSave = async () => {
    try {
      const response = await fetch("/api/update_persona", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(persona),
      });
  
      if (!response.ok) {
        throw new Error("Failed to save persona");
      }
  
      console.log("Persona updated successfully");
    } catch (error) {
      console.error("Error updating persona:", error);
    }
  
    setIsEditing(false);
  };    

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
      {loading && <div className="loading-overlay">Loading Product Viability Agent...</div>}

      <main style={{ width: "80%" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>

        {/* Customer Persona Section */}
        <div style={{ marginBottom: "2rem", padding: "1rem", borderRadius: "8px", backgroundColor: "var(--primary-color)", color: "white", textAlign: "left" }}>
          <h2 style={{ fontSize: "1.75rem", textAlign: "center" }}>Customer Persona</h2>

          {isEditing ? (
            <div>
              <label style={{ fontWeight: "bold" }}>Name:</label>
              <input
                type="text"
                name="name"
                value={persona.name}
                onChange={handleChange}
                style={{ width: "100%", padding: "0.5rem", margin: "0.5rem 0", borderRadius: "5px" }}
              />

              <label style={{ fontWeight: "bold" }}>Age:</label>
              <input
                type="number"
                name="age"
                value={persona.demographics.age}
                onChange={handleDemographicsChange}
                style={{ width: "100%", padding: "0.5rem", margin: "0.5rem 0", borderRadius: "5px" }}
              />

              <label style={{ fontWeight: "bold" }}>Gender:</label>
              <input
                type="text"
                name="gender"
                value={persona.demographics.gender}
                onChange={handleDemographicsChange}
                style={{ width: "100%", padding: "0.5rem", margin: "0.5rem 0", borderRadius: "5px" }}
              />

              <label style={{ fontWeight: "bold" }}>Occupation:</label>
              <input
                type="text"
                name="occupation"
                value={persona.demographics.occupation}
                onChange={handleDemographicsChange}
                style={{ width: "100%", padding: "0.5rem", margin: "0.5rem 0", borderRadius: "5px" }}
              />

              <label style={{ fontWeight: "bold" }}>Description:</label>
              <textarea
                name="description"
                value={persona.description}
                onChange={handleChange}
                style={{ width: "100%", padding: "0.5rem", margin: "0.5rem 0", borderRadius: "5px", minHeight: "100px" }}
              />
            </div>
          ) : (
            <div>
              <p><strong>Name:</strong> {persona.name}</p>
              <p><strong>Age:</strong> {persona.demographics.age}</p>
              <p><strong>Gender:</strong> {persona.demographics.gender}</p>
              <p><strong>Occupation:</strong> {persona.demographics.occupation}</p>
              <p><strong>Description:</strong> {persona.description}</p>
            </div>
          )}

          {/* Buttons */}
          <div style={{ textAlign: "right", marginTop: "1rem" }}>
          {isEditing ? (
            <>
              <button 
                onClick={handleSave} 
                style={{ padding: "0.5rem 1rem", backgroundColor: "var(--secondary-color)", color: "white", border: "none", borderRadius: "5px", cursor: "pointer", marginRight: "0.5rem" }}
              >
                Save
              </button>
              <button 
                onClick={handleCancel} 
                style={{ padding: "0.5rem 1rem", backgroundColor: "var(--text-color-secondary)", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}
              >
                Cancel
              </button>
            </>
          ) : (
            <button 
              onClick={handleEdit} 
              style={{ padding: "0.5rem 1rem", backgroundColor: "var(--secondary-color)", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}
            >
              Edit
            </button>
          )}
        </div>
        </div>

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