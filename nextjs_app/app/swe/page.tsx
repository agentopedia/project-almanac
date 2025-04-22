"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import '../styles/agents.css';

export default function SoftwareAgentPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {loading ? (
        <div className="flex justify-center items-center h-screen text-2xl">
          Loading content...
        </div>
      ) : (
        <>
          <div className="text-center py-6">
            <h1 className="text-4xl font-bold text-blue-500">Software Engineering Agent</h1>
            <p className="text-gray-300">Review your generated MVP</p>
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "1rem",
              marginTop: "1rem"
            }}
          >
            <button
              onClick={() => {
                sessionStorage.setItem("generatedMVPComplete", "true"); // for Agents page (in navbar)
                router.push("/generatedmvp")
              }}
              className="navigation-buttons"
            >
              View Generated MVP
            </button>
            {/* <button
              onClick={() => router.push("/customer_agent")}
              className="navigation-buttons"
            >
              Generate Customer Feedback
            </button> */}
            <div style={{ display: "flex", gap: "1rem" }}>
              <button
                onClick={() => router.push("/product_viability_agent")}
                className="navigation-buttons"
              >
                Back to Product Viability Agent
              </button>

              <button
                onClick={() => router.push("/")}
                className="navigation-buttons"
              >
                Back to Home
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}