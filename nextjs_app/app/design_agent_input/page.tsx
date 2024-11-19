"use client";
import Link from 'next/link';
// import { useRouter } from 'next/router';
import { useState } from 'react';
import React from 'react';
import { useRouter } from 'next/navigation';

export default function DesignThinkingAgentInput() {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // console.log('entered handle submit');
    // POST request to the API route with the input text
    const res = await fetch('/api/design_input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: inputText }),
    });

    const data = await res.json();
    console.log('API Response:', data);
    router.push(`/design_agent_output?result=${encodeURIComponent(JSON.stringify(data))}`);
  };

  return (
    <div style={{ padding: "1rem", color: "white", backgroundColor: "#222222", minHeight: "100vh", textAlign: "center" }}>
      <main style={{ marginTop: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Product Ideation</h1>
        <p style={{ fontSize: "1.25rem", marginBottom: "2rem" }}>Begin your journey of MVP generation</p>

        {/* Flex Container for Textarea and Button */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <form onSubmit={handleSubmit}>
            {/* Input Field */}
            <textarea
              placeholder="Enter product description..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              style={{
                width: "100%",
                height: "200px",
                padding: "1rem",
                fontSize: "1.25rem",
                borderRadius: "0.25rem",
                border: "1px solid #ccc",
                marginBottom: "1rem"
              }}
            />

            {/* Submit Button */}
              <button className="button mt-8" style={{ padding: "0.75rem 1.5rem", fontSize: "1rem", borderRadius: "0.25rem" }}>
                Submit
              </button>
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