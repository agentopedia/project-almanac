"use client";
import Link from 'next/link';
import EmpathyMap from '../components/EmpathyMap';
import CustomerJourney from '../components/CustomerJourney';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import JSON5 from 'json5';
import { useState } from "react";

const parseWithJSON5 = (jsonStr: string) => {
  try {
    return JSON5.parse(jsonStr);
  } catch (error) {
    console.error('JSON5 parsing error:', error);
    return null;
  }
};

export default function DesignThinkingAgentOutput() {
  const [loading, setLoading] = useState(false);

  //if you want to use dummy data, comment out everything above const router = useRouter();
  const searchParams = useSearchParams();
  const result = searchParams.get('result'); // get 'result' query parameter from URL
  let parsedData;

  if (result) {
    try {
      const decodedResult = decodeURIComponent(result);
      const initialParse = JSON.parse(decodedResult);
      
      // Fix the inner result if it's a string
      if (typeof initialParse.result === 'string') {
        const fixedResult = parseWithJSON5(initialParse.result);
        if (fixedResult) {
          parsedData = { ...initialParse, result: fixedResult };
        }
      } else {
        parsedData = initialParse;
      }
    } catch (error) {
      console.error('Error parsing data:', error);
    }
  }

  console.log('Raw Result:', result); 
  console.log('Parsed Data:', parsedData)
  console.log("result: ", parsedData.result)

  const router = useRouter();

  const handleProceed = async () => {
    setLoading(true); // show loading screen

    try {
      // make a GET request to the Next.js API route
      const response = await fetch("/api/viability", {
        method: "GET",
      });
      const data = await response.json();
  
      if (response.ok) {
        console.log("Data from Flask server:", data);
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
        <div
          style={{
            marginBottom: "2rem",
            padding: "1rem",
            borderRadius: "8px",
            backgroundColor: "var(--primary-color)",
            color: "white",
            textAlign: "left",
          }}
        >
          <h2 style={{fontSize: "1.75rem", textAlign: "center" }}>
            Customer Persona
          </h2>
          <p>
            <span style={{ fontWeight: "bold", color: "white" }}>Name:</span>{" "}
            {parsedData?.result?.customer_persona[0].name || "N/A"}
          </p>
          <p>
            <span style={{ fontWeight: "bold", color: "white" }}>Demographics:</span>{" "}
            {`Age: ${parsedData?.result?.customer_persona[0].demographics.age || "N/A"}, `}
            {`Gender: ${parsedData?.result?.customer_persona[0].demographics.gender || "N/A"}, `}
            {`Occupation: ${parsedData?.result?.customer_persona[0].demographics.occupation || "N/A"}`}
          </p>
          <p>
            <span style={{ fontWeight: "bold", color: "white" }}>Description:</span>{" "}
            {parsedData?.result?.customer_persona[0].description || "N/A"}
          </p>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between", // space btwn the components
            gap: "1rem"
          }}
        >
          {/* Empathy Map */}
          <EmpathyMap empathyData={parsedData?.result?.empathy_map || {}} />

          {/* Customer Journey Map */}
          <CustomerJourney journeyData={parsedData?.result?.customer_journey_map || {}} />
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