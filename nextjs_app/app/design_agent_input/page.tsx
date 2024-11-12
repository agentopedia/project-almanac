"use client";
import Link from 'next/link';
import { useState } from 'react';
import React from 'react';

export default function DesignThinkingAgentInput() {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    console.log('entered handle submit');
    // POST request to the API route with the input text
    const res = await fetch('/api/design_input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: inputText }),
    });

    const data = await res.json();
    setResponse(data.result);
  };

  return (
    <div style={{ padding: '2rem', color: 'white', backgroundColor: '#222222', minHeight: '100vh', textAlign: 'center' }}>
      <main style={{ marginTop: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Design Thinking Agent</h1>
        <p style={{ fontSize: '1.25rem', marginBottom: '2rem' }}>Understand users, generate empathy maps, and shape the product vision</p>

        <form onSubmit={handleSubmit}>
          <textarea
            placeholder="Enter Product Description Here"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            style={{
              width: '60%',
              height: '150px',
              padding: '1rem',
              fontSize: '1.25rem',
              borderRadius: '0.25rem',
              border: '1px solid #ccc',
              marginBottom: '1.5rem',
            }}
          />
          <br />
          {/* <Link href="/design_agent_output"> */}
            <button
              type="submit"
              style={{
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                padding: '0.75rem 1.5rem',
                fontSize: '1.25rem',
                cursor: 'pointer',
                borderRadius: '0.25rem',
              }}
            >
              Submit
            </button>
          {/* </Link> */}
        </form>

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