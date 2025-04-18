"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";
import React from "react";
import '../styles/agents.css';

type ProductData = {
  introduction: string;
  goals: string;
  targetAudience: string;
  productFeatures: string;
  functionalRequirements: string;
  nonfunctionalRequirements: string;
  //start business agent fields below
  valuePropositions: string;
  channels: string;
  revenueStreams: string;
  keyActivities: string;
  costStructure: string;
  targetMarket: string; 
  customerRelationships: string; 
  keyResources: string;
  keyPartnerships: string;
  customerSegments: string;
};

const ProductViability = () => {
  const [loadingMessage, setLoadingMessage] = useState("Loading...");
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState<string>("Introduction");
  const [parsedProductData, setParsedProductData] = useState<ProductData | null>(null); // parsed product data
  const [activeTab, setActiveTab] = useState<"ProductRequirements" | "BusinessAnalysis">("ProductRequirements");
  const [loadingTimeoutReached, setLoadingTimeoutReached] = useState<boolean>(false); // track timeout state
  const router = useRouter();
  const searchParams = useSearchParams();
  const data = searchParams.get("data");

  // Sections for each tab
  const productSections = [
    { key: "introduction", label: "Introduction" },
    { key: "goals", label: "Goals" },
    { key: "targetAudience", label: "Target Audience" },
    { key: "productFeatures", label: "Product Features" },
    { key: "functionalRequirements", label: "Functional Requirements" },
    { key: "nonfunctionalRequirements", label: "Nonfunctional Requirements" }
  ];
  const businessSections = [
    { key: "targetMarket", label: "Target Market" }, 
    { key: "customerSegments", label: "Customer Segments" }, 
    { key: "valuePropositions", label: "Value Propositions" }, 
    { key: "channels", label: "Channels" }, // 3. Channels
    { key: "customerRelationships", label: "Customer Relationships" }, 
    { key: "revenueStreams", label: "Revenue Streams" }, 
    { key: "keyResources", label: "Key Resources" }, 
    { key: "keyActivities", label: "Key Activities" }, 
    { key: "keyPartnerships", label: "Key Partnerships" }, 
    { key: "costStructure", label: "Cost Structure" },
  ];
  // Determine which sections to show based on the active tab
  const sections = activeTab === "ProductRequirements" ? productSections : businessSections;
  /*
  // parse business agent data
  useEffect(() => {
    if (activeTab === "BusinessAnalysis" && !parsedProductData?.valuePropositions) {
      // Fetch Business Model data only when switching to Business Analysis
      fetch("/api/business_model")
        .then(response => response.json())
        .then(data => {
          console.log("Fetched Business Model Data:", data);
          setParsedProductData(prevData => ({
            ...prevData,
            ...data.result // Merge new Business Model data into existing product data
          }));
        })
        .catch(error => console.error("Error fetching Business Model:", error));
    }
  }, [activeTab]);
*/
  // parse product viability data
  useEffect(() => {
    async function fetchViabilityData() {
      try {
        let viabilityData = null;
  
        if (data) {
          // parse data from URL
          viabilityData = JSON.parse(decodeURIComponent(data));
        } else {
          // fetch from backend if no URL data
          const response = await fetch("/api/viability");
          const fetched = await response.json();
          viabilityData = fetched;
  
          // mark as complete for Agents Page
          sessionStorage.setItem("productViabilityComplete", "true");
        }
  
        if (typeof viabilityData.viability_result === "string") {
          viabilityData.viability_result = JSON.parse(viabilityData.viability_result);
        }
        if (typeof viabilityData.business_result === "string") {
          viabilityData.business_result = JSON.parse(viabilityData.business_result);
        }
  
        console.log("Parsed PRD:", viabilityData.viability_result);
        console.log("Parsed Business Model:", viabilityData.business_result);
  
        setParsedProductData(prev => ({
          ...prev,
          ...viabilityData.viability_result,
          ...viabilityData.business_result,
        }));
      } catch (error) {
        console.error("Error loading viability data:", error);
        setLoadingMessage("Failed to load viability data.");
      }
    }
  
    fetchViabilityData();
  }, [data]);  

  // set loading to false once data is available
  useEffect(() => {
    if (parsedProductData) {
      setLoading(false);
    }
  }, [parsedProductData]);

  // timeout to change `loadingTimeoutReached` after 3 seconds
  useEffect(() => {
    if (!parsedProductData) {
      setLoading(true);

      const timeout = setTimeout(() => {
        setLoadingTimeoutReached(true);
        setLoading(false); // hide loading if timeout reached
      }, 3000); // 3 seconds

      return () => clearTimeout(timeout); // clear timeout if parsedProductData is loaded
    }
  }, [parsedProductData]);

  // Ensure active section updates correctly when switching tabs
  useEffect(() => {
    if (!sections.some((s) => s.label === activeSection)) {
      setActiveSection(sections[0].label);
    }
  }, [activeTab, sections]);

  const handleBackToDesign = async () => {
    setLoadingMessage("Returning to Design Thinking Agent...");
    setLoading(true);
    router.push(`/design_agent_output`);
  };

  const handleProceedToSWEAgent = async () => {
    setLoadingMessage("Loading Autonomous SWE Agent...");
    setLoading(true);

    try {
      const response = await fetch("/api/swe_model", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ action: 'generate' }),
      });

      if (!response.ok) {
        throw new Error('Failed to trigger MVP generation');
      }

      // MVP generation triggered, now navigate to SWE Agent page
      sessionStorage.setItem("sweComplete", "true"); // for Agents page (in navbar)
      router.push("/swe");

    } catch (error) {
      console.error("Error triggering MVP generation:", error);
      alert("Failed to proceed to Software Engineering Agent. Please try again.");
    } finally {
      setLoading(false); // Stop loading indicator
    }
  };

  const getSectionData = (key: string): JSX.Element => {
    const validKey = key as keyof ProductData;
  
    if (!parsedProductData) {
      return <p>{loadingTimeoutReached ? "No data available" : "Loading..."}</p>;
    }
  
    const sectionData = parsedProductData[validKey];
  
    if (Array.isArray(sectionData)) {
      return (
        <>
          {sectionData.map((item, index) => (
            <p key={index} style={{ marginBottom: "0px" }}>
              {item}
            </p>
          ))}
        </>
      );
    }
    return <p>{parsedProductData[validKey] || "No data available"}</p>;
  };

  return (
    <div style={{ padding: "20px", minHeight: "100vh", backgroundColor: "#222", color: "white" }}>
      {loading ? (
        <div className="loading-overlay" role="status" aria-busy="true">
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span className="spinner" />
            <p style={{ marginTop: '1rem' }}>{loadingMessage}</p>
          </div>
        </div>
      ) : (
        <>
          {/* Header */}
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

          {/* Tab Selection */}
          <div style={{ display: "flex", justifyContent: "center", marginBottom: "10px" }}>
            <button
              onClick={() => setActiveTab("ProductRequirements")}
              style={{
                padding: "10px 20px",
                backgroundColor: activeTab === "ProductRequirements" ? "#007bff" : "#444",
                color: "white",
                border: "none",
                cursor: "pointer",
                marginRight: "10px"
              }}
            >
              Product Requirements
            </button>

            <button
              onClick={() => setActiveTab("BusinessAnalysis")}
              style={{
                padding: "10px 20px",
                backgroundColor: activeTab === "BusinessAnalysis" ? "#007bff" : "#444",
                color: "white",
                border: "none",
                cursor: "pointer"
              }}
            >
              Business Analysis
            </button>
          </div>

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
              {getSectionData(activeSection.toLowerCase().replace(/ /g, "_"))}

              {/* Footer Buttons */}
              <div className="footer-buttons">
                <button
                  onClick={() => {
                    const currentIndex = sections.findIndex((s) => s.label === activeSection);
                    if (currentIndex > 0) setActiveSection(sections[currentIndex - 1].label);
                  }}
                  disabled={activeSection === sections[0].label}
                  style={{
                    opacity: activeSection ===  sections[0].label ? "0.5" : "1",
                    pointerEvents: activeSection === sections[0].label ? "none" : "auto",
                  }}
                >
                  Back
                </button>
                <button
                  onClick={() => {
                    const currentIndex = sections.findIndex((s) => s.label === activeSection);
                    if (currentIndex < sections.length - 1) setActiveSection(sections[currentIndex + 1].label);
                  }}
                  disabled={activeSection === sections[sections.length - 1].label}
                  style={{
                    opacity: activeSection === sections[sections.length - 1].label ? "0.5" : "1",
                    pointerEvents: activeSection === sections[sections.length - 1].label ? "none" : "auto",
                  }}
                >
                  Next
                </button>
              </div>
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="navigation-buttons">
            <button onClick={handleBackToDesign}>Back to Design Thinking Agent</button>
            {/* <button onClick={() => router.push("/generate_mvp")}>Proceed to Software Engineering Agent</button>  */}
            <button onClick={handleProceedToSWEAgent}>Proceed to Software Engineering Agent</button> 
          </div>
        </>
      )}
    </div>
  );
};

export default ProductViability;