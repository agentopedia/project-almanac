"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";

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
  const router = useRouter(); // navigating btwn agents
  const searchParams = useSearchParams();
  const data = searchParams.get("data");

  let parsedData;
  if (data) {
    try {
      parsedData = JSON.parse(decodeURIComponent(data));
      if (parsedData.data) {
        parsedData.data = JSON.parse(parsedData.data);
      }
    } catch (error) {
      console.error("JSON not formatted correctly:", error);
    }
  }

  const sections = [
    { key: "introduction", label: "Introduction" },
    { key: "goals", label: "Goals" },
    { key: "targetAudience", label: "Target Audience" },
    { key: "productFeatures", label: "Product Features" },
    { key: "functionalRequirements", label: "Functional Requirements" },
    { key: "nonfunctionalRequirements", label: "Nonfunctional Requirements" },
  ];

  return (
    <div style={{ padding: "20px", minHeight: "100vh", backgroundColor: "#222" }}>
      <header style={{ textAlign: "center", marginBottom: "20px", color: "white" }}>
        <h1 style={{ fontSize: "2.5rem" }}>Product Viability Agent</h1>
        <p>Define your product requirements</p>
        <a
          href="/path-to-pdf"
          download="[Product Name].pdf"
          style={{ color: "var(--primary-color)", textDecoration: "underline" }}
        >
          [Product Name].pdf
        </a>
      </header>

      {/* Main Content */}
      <div style={{ display: "flex", gap: "20px" }}>
        {/* Sidebar */}
        <aside className="sidebar">
          {sections.map((section) => (
            <button
              key={section.key}
              className={activeSection === section.label ? "active" : ""}
              onClick={() => setActiveSection(section.label)}
            >
              {section.label}
            </button>
          ))}
        </aside>

        {/* Active Section */}
        <div className="product-section" style={{ flex: 1 }}>
          <h2>{activeSection}</h2>
          <p>
            {parsedData?.data?.[activeSection.toLowerCase().replace(/ /g, "_")] ||
              "No data available"}
          </p>

          {/* Footer Buttons */}
          <div className="footer-buttons">
            <button
              onClick={() => {
                const currentIndex = sections.findIndex((s) => s.label === activeSection);
                if (currentIndex > 0) setActiveSection(sections[currentIndex - 1].label);
              }}
              disabled={activeSection === "Introduction"}
              style={{
                opacity: activeSection === "Introduction" ? "0.5" : "1",
                pointerEvents: activeSection === "Introduction" ? "none" : "auto",
              }}
            >
              Back
            </button>
            <button
              onClick={() => {
                const currentIndex = sections.findIndex((s) => s.label === activeSection);
                if (currentIndex < sections.length - 1)
                  setActiveSection(sections[currentIndex + 1].label);
              }}
              disabled={activeSection === "Nonfunctional Requirements"}
              style={{
                opacity: activeSection === "Nonfunctional Requirements" ? "0.5" : "1",
                pointerEvents:
                  activeSection === "Nonfunctional Requirements" ? "none" : "auto",
              }}
            >
              Next
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="navigation-buttons">
        <button onClick={() => router.push("../design_agent_output")}>
          Back to Design Thinking Agent
        </button>
        <button onClick={() => router.push("")}>
          Proceed to Business Model Agent
        </button>
      </div>
    </div>
  );
};

export default ProductViability;