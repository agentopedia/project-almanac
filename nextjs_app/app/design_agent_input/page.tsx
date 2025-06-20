"use client";
import Link from 'next/link';
import { useState } from 'react';
import React from 'react';
import { useRouter } from 'next/navigation';
import '../styles/agents.css';

export default function DesignThinkingAgentInput() {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // console.log('entered handle submit');
    // POST request to the API route with the input text

    setLoading(true);

    try {
      const res = await fetch('/api/design_input', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify({ query: inputText }),
      });

      const data = await res.json();
      console.log('API Response:', data);

      sessionStorage.setItem("designThinkingComplete", "true"); // for Agents page (in navbar)
      sessionStorage.setItem("productViabilityComplete", "false");
      sessionStorage.setItem("sweComplete", "false");
      sessionStorage.setItem("generatedMVPComplete", "false");
      router.push("/design_agent_output")
    } catch (error) {
      console.error("Error submitting request:", error);
    } finally {
      setLoading(false); // hide loading overlay after API response
    }
  };

  return (
    <div style={{ padding: "1rem", color: "white", backgroundColor: "#222222", minHeight: "100vh", textAlign: "center" }}>
      {loading && (
        <div className="loading-overlay" role="status" aria-busy="true">
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span className="spinner" />
            <p style={{ marginTop: '1rem' }}>Loading Design Thinking Agent...</p>
          </div>
        </div>
      )}

      <main style={{ marginTop: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Product Ideation</h1>
        <p style={{ fontSize: "1.25rem", marginBottom: "2rem" }}>Begin your journey of MVP generation</p>

        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <form onSubmit={handleSubmit}>
            {/* Input Field */}
            <textarea
              placeholder="Enter product description..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="textarea"
            />

            {/* Navigation Buttons */}
            <div className="navigation-buttons">
              <button onClick={(event) => { 
                event.preventDefault();
                router.push("/");
              }}>
                Back to Home
              </button>
              <button onClick={handleSubmit}
                type="submit"
                disabled={!inputText.trim()} // disable button if inputText is empty/whitespace
                style={{
                  padding: "10px 20px",
                  backgroundColor: inputText.trim() ? "#007bff" : "#aaa", // button color based on state
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: inputText.trim() ? "pointer" : "not-allowed", // cursor style
                }}
              >
                Submit
              </button>
            </div>
          </form>
        </div>
        {response && (
          <div style={{ marginTop: '2rem', color: 'white' }}>
            <h2>Response:</h2>
            <p>{response}</p>
          </div>
        )}
      </main>
    </div>
  );
}
// export default page;