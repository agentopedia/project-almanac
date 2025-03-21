"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

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

          <div className="flex justify-center py-6">
            <button
              onClick={() => router.push("/generatedmvp")}
              className="bg-green-600 text-white px-6 py-2 rounded-lg mr-4 hover:bg-green-700"
            >
              View Generated MVP
            </button>
            
            <button
              onClick={() => router.push("/product_viability_agent")}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg mr-4 hover:bg-blue-700"
            >
              Back to Product Viability Agent
            </button>
            
            <button
              onClick={() => router.push("/")}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Back to Home
            </button>
          </div>
        </>
      )}
    </div>
  );
}