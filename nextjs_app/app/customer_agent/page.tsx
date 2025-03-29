"use client";
import { useState, useEffect } from "react";
import JSON5 from "json5";
import CustomerPersona from "../components/CustomerPersona";
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
    occupation: "Loading...",
  },
  description: "Loading...",
};

export default function CustomerFeedbackAgent() {
  const [activeTab, setActiveTab] = useState("Customer");
  const [persona, setPersona] = useState<CustomerPersona>(defaultPersona);
  const [originalPersona, setOriginalPersona] = useState<CustomerPersona | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    async function fetchPersona() {
      try {
        const response = await fetch("/api/design_input");
        if (!response.ok) {
          throw new Error("Failed to fetch persona data");
        }
        const data = await response.json();
        const parsed = JSON5.parse(data.result);
        
        if (parsed?.customer_persona?.length > 0) {
          setPersona(parsed.customer_persona[0]); // Load persona data
        }
      } catch (error) {
        console.error("Error fetching persona data:", error);
      }
    }

    fetchPersona();
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case "Customer":
        return (
        <main style={{ width: "60%" }}>
          <CustomerPersona persona={persona} onUpdatePersona={setPersona} />
        </main>
      );
      case "Feedback":
        return (
          <div className="card">
            <h2 className="cardTitle">Customer Feedback</h2>
            <p className="cardText">[Display response from LLM, field is editable]</p>
            <button className="button mt-4">Generate MVP</button>
          </div>
        );

      case "MVPs":
        return (
          <div className="card">
            <h2 className="cardTitle">MVPs</h2>
            <p className="cardText">Takes you back to the SWE agent to view previous MVPs</p>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="container">
      <div className="flex-container mb-4">
        {["Customer", "Feedback", "MVPs"].map((tab) => (
          <button
            key={tab}
            className={`button ${activeTab === tab ? "button-secondary" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
      {renderContent()}
    </div>
  );
}
