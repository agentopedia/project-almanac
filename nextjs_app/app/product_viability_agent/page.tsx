"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";
import React from "react";

type ProductData = {
  introduction: string;
  goals: string;
  targetAudience: string;
  productFeatures: string;
  functionalRequirements: string;
  nonfunctionalRequirements: string;
  valuePropositions: string;
  channels: string;
  revenueStreams: string;
  keyActivities: string;
  costStructure: string;
};

const ProductViability = () => {
  const [activeSection, setActiveSection] = useState<string>("Introduction");
  const [parsedProductData, setParsedProductData] = useState<ProductData | null>(null); // parsed product data
  // const [parsedFromDesign, setParsedFromDesign] = useState<DesignAgentData | null>(null); // parsed design data
  const [loadingTimeoutReached, setLoadingTimeoutReached] = useState<boolean>(false); // track timeout state
  const router = useRouter();
  const searchParams = useSearchParams();
  const data = searchParams.get("data");
  // const fromDesign = searchParams.get("fromDesign");

  // parse product viability data
  useEffect(() => {
    if (data) {
      try {
        const parsedData = JSON.parse(decodeURIComponent(data));

        const productData =
          typeof parsedData.data === "string"
            ? JSON.parse(parsedData.data)
            : parsedData.data;

        setParsedProductData(productData);
      } catch (error) {
        console.error("Error parsing data:", error);
      }
    }
  }, [data]);

  // timeout to change `loadingTimeoutReached` after 3 seconds
  useEffect(() => {
    if (!parsedProductData) {
      const timeout = setTimeout(() => {
        setLoadingTimeoutReached(true);
      }, 3000); // 3 seconds

      return () => clearTimeout(timeout); // clear timeout if parsedProductData is loaded
    }
  }, [parsedProductData]);

  const sections = [
    { key: "introduction", label: "Introduction" },
    { key: "goals", label: "Goals" },
    { key: "targetAudience", label: "Target Audience" },
    { key: "productFeatures", label: "Product Features" },
    { key: "functionalRequirements", label: "Functional Requirements" },
    { key: "nonfunctionalRequirements", label: "Nonfunctional Requirements" },
    { key: "valuePropositions", label: "Value Propositions" },
    { key: "channels", label: "Channels" },
    { key: "revenueStreams", label: "Revenue Streams" },
    { key: "keyActivities", label: "Key Activities" },
    { key: "costStructure", label: "Cost Structure" }
  ];

  const handleBackToDesign = async () => {
    try {
      // Make a GET request to the Next.js API route
      const response = await fetch("/api/design_backtracking", {
        method: "GET",
      });
      const result = await response.json();
      
      if (response.ok) {
        console.log("Result from Flask server:", result);
        const encodedResult = encodeURIComponent(JSON.stringify(result));
        router.push(`/design_agent_output?result=${encodedResult}`);
      } else {
        console.error("Failed to fetch result:", result);
      }
    } catch (error) {
      console.error("Error during the GET request:", error);
    }

  };

  // version of getSectionData function that has no paragraph breaks - can delete
  // const getSectionData = (key: string): string => {
  //   const validKey = key as keyof ProductData;
  
  //   if (!parsedProductData) {
  //     return loadingTimeoutReached ? "No data available" : "Loading...";
  //   }
  //   const sectionData = parsedProductData[validKey];

  //   if (Array.isArray(sectionData)) {
  //     return sectionData.join("\n");
  //   }

  //   return parsedProductData[validKey] || "No data available";
  // };

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
    return <p>parsedProductData[validKey] || "No data available" </p>;
  };

  // const adjustSidebarHeight = () => {
  //   const productSection = document.querySelector(".product-section") as HTMLElement;
  //   const sidebar = document.querySelector(".sidebar") as HTMLElement;
  
  //   if (productSection && sidebar) {
  //     sidebar.style.maxHeight = `${productSection.offsetHeight}px`;
  //   }
  // };
  
  // useEffect(() => {
  //   adjustSidebarHeight();
  //   window.addEventListener("resize", adjustSidebarHeight);
  //   return () => window.removeEventListener("resize", adjustSidebarHeight);
  // }, []);
   
  
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
              onClick={() => {
                setActiveSection(section.label);
                // adjustSidebarHeight();
              }}
            >
              {section.label}
            </button>
          ))}
        </aside>

        {/* Active Section */}
        <div className="product-section" style={{ flex: 1 }}>
          <h2>{activeSection}</h2>
          {/* <p style={{ whiteSpace: "pre-line" }}> */}
            {getSectionData(activeSection.toLowerCase().replace(/ /g, "_"))}
          {/* </p> */}
        
          {/* Footer Buttons */}
          <div className="footer-buttons">
            <button
              onClick={() => {
                const currentIndex = sections.findIndex((s) => s.label === activeSection);
                if (currentIndex > 0) {
                  setActiveSection(sections[currentIndex - 1].label);
                  // adjustSidebarHeight(); 
                }
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
                if (currentIndex < sections.length - 1) {
                  setActiveSection(sections[currentIndex + 1].label);
                  // adjustSidebarHeight();
                }
              }}
              disabled={activeSection === "Cost Structure"}
              style={{
                opacity: activeSection === "Cost Structure" ? "0.5" : "1",
                pointerEvents:
                  activeSection === "Cost Structure" ? "none" : "auto",
              }}
            >
              Next
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="navigation-buttons">
        <button onClick={handleBackToDesign}>
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
