"use client"
import { useState } from "react";
import { useSearchParams } from 'next/navigation';

type ProductData = {
  introduction: string;
  goals: string;
  targetAudience: string;
  productFeatures: string;
  functionalRequirements: string;
  nonfunctionalRequirements: string;
};

type ParsedData = {
  data: ProductData;
};

const ProductViability = () => {
  const [activeSection, setActiveSection] = useState<string>("Introduction");

  const searchParams = useSearchParams();
  const data = searchParams.get('data'); 
  
  let parsedData;
  if (data) {
    try {
      parsedData = JSON.parse(decodeURIComponent(data)); // Decode the URL-encoded string and parse it as JSON
      if (parsedData.data) {
        parsedData.data = JSON.parse(parsedData.data);
      }
    } catch (error) {
      console.error('Json not formatted correctly:', error);
    }
  }

  console.log("Raw Data: ", data);
  console.log("Parsed Data: ", parsedData.data);

  const sections = [
    "Introduction",
    "Goals",
    "Target Audience",
    "Product Features",
    "Functional Requirements",
    "Nonfunctional Requirements",
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* Header */}
      <header
        style={{
          background: "#222",
          color: "#ffff",
          padding: "20px",
          textAlign: "center",
        }}
      >
        <h1 style={{ margin: "0", fontSize: "30px" }}>Product Viability</h1>
        <p style={{ margin: "5px 0", fontSize: "20px" }}>Define your product requirements</p>
        <a
          href="/path-to-pdf"
          download="[Product Name].pdf"
          style={{
            color: "#007bff",
            textDecoration: "none",
            fontSize: "20px",
          }}
        >
          [Product Name].pdf
        </a>
      </header>

      {/* Content Area */}
      <div style={{ display: "flex", flex: "1" }}>
        {/* Sidebar */}
        <aside
          style={{
            width: "180px", // Adjusted sidebar width
            background: "#222",
            color: "#fff",
            padding: "20px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {sections.map((section) => (
            <button
              key={section}
              onClick={() => setActiveSection(section)}
              style={{
                background: activeSection === section ? "#444" : "transparent",
                color: "#fff",
                border: "none",
                textAlign: "left",
                marginBottom: "10px",
                padding: "10px",
                cursor: "pointer",
                borderRadius: "5px",
              }}
            >
              {section}
            </button>
          ))}
        </aside>

        {/* Main Content */}
        <main
          style={{
            flex: 3, // Increased flex value for the main content area
            background: "#f4f4f4",
            padding: "40px", // Increased padding for better layout
          }}
        >
          <div
            style={{
              background: "#fff",
              padding: "20px",
              borderRadius: "5px",
              boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
            }}
          >
            <h2 style={{ color: "#333" }}>{activeSection}</h2>
            <p style={{ color: "#666" }}>
              {parsedData?.data?.[activeSection.toLowerCase().replace(/ /g, "_")]?.join("\n") || "No data available"}
            </p>
          </div>
        </main>
      </div>

      {/* Footer Buttons */}
      <footer
        style={{
          position: "absolute",
          bottom: "20px",
          left: "calc(180px + 40px)", // Adjusted for smaller sidebar
          display: "flex",
          gap: "10px",
        }}
      >
        <button
          style={{
            background: "#007bff",
            color: "#fff",
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
          onClick={() => {
            const currentIndex = sections.indexOf(activeSection);
            if (currentIndex > 0) setActiveSection(sections[currentIndex - 1]);
          }}
        >
          Back
        </button>
        <button
          style={{
            background: "#007bff",
            color: "#fff",
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
          onClick={() => {
            const currentIndex = sections.indexOf(activeSection);
            if (currentIndex < sections.length - 1)
              setActiveSection(sections[currentIndex + 1]);
          }}
        >
          Next
        </button>
      </footer>
    </div>
  );
};

export default ProductViability;
