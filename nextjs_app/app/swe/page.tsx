// "use client";
// import React from "react";
// import '../globals.css';
// import SideNav from "../components/SideNav"; //side navigation menu

// const MVPPage: React.FC = () => {
//   return (
//     <div className="page-container">
//       <SideNav />

//       <main className="container">
//         <header className="header">
//           <h1 className="title">Title of MVP</h1>
//           <p className="subtitle">Sub caption</p>
//         </header>

//         <section className="swe-section">
//           <div className="swe-card">
//             <h2 className="cardTitle">Feature 1</h2>
//             <p className="cardText">Sub caption</p>
//           </div>

//           <div className="swe-card">
//             <h2 className="cardTitle">Feature 2</h2>
//             <p className="cardText">Sub caption</p>
//           </div>

//           <div className="swe-card">
//             <h2 className="cardTitle">Tutorials</h2>
//             <p className="cardText">Real world examples for the product</p>
//           </div>
//         </section>

//         <div style={{ marginTop: "2rem" }}>
//           <button className="button">Get Started</button>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default MVPPage;

"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import JSON5 from 'json5';

export default function SoftwareAgentPage() {
  const [loading, setLoading] = useState(true);
  const [mvpData, setMvpData] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>("overview");
  const router = useRouter();

  // Fetch MVP data when component mounts
  useEffect(() => {
    const fetchMVP = async () => {
      setLoading(true);
      try {
        const response = await fetch("/api/swe_model");
        if (!response.ok) {
          throw new Error("Failed to fetch MVP data");
        }
        
        const data = await response.json();
        setMvpData(data.result);
      } catch (err) {
        console.error("Error fetching MVP:", err);
        setError("Failed to load MVP data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchMVP();
  }, []);

  // Parse the MVP data if it exists; NOTE: currently not parsing. 
  console.log(mvpData)
  const parsedMVP = mvpData

  // Function to render code snippets with syntax highlighting
  const renderCodeBlock = (code: string, language: string) => {
    return (
      <pre className="code-block">
        <code className={`language-${language}`}>
          {code}
        </code>
      </pre>
    );
  };

  // Function to handle tab changes
  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
  };

  // Function to render the appropriate content based on active tab
  const renderTabContent = () => {
    if (!parsedMVP) {
      return <p>No MVP data available</p>;
    }

    switch (activeTab) {
      case "overview":
        return (
          <div className="tab-content">
            <h3>Project Overview</h3>
            <p>{parsedMVP.overview || "No overview provided"}</p>
            <h4>Architecture</h4>
            <p>{parsedMVP.architecture || "No architecture details provided"}</p>
          </div>
        );
      case "components":
        return (
          <div className="tab-content">
            <h3>React Components</h3>
            {parsedMVP.components && parsedMVP.components.map((component: any, index: number) => (
              <div key={index} className="component-card">
                <h4>{component.name}</h4>
                <p>{component.description}</p>
                {renderCodeBlock(component.code, "jsx")}
              </div>
            ))}
          </div>
        );
      case "api":
        return (
          <div className="tab-content">
            <h3>API Integration</h3>
            <p>{parsedMVP.api?.description || "No API description provided"}</p>
            <h4>Endpoints</h4>
            {parsedMVP.api?.endpoints && parsedMVP.api.endpoints.map((endpoint: any, index: number) => (
              <div key={index} className="endpoint-card">
                <h5>{endpoint.name}</h5>
                <p>{endpoint.description}</p>
                <p><strong>Method:</strong> {endpoint.method}</p>
                <p><strong>URL:</strong> {endpoint.url}</p>
                {endpoint.code && renderCodeBlock(endpoint.code, "javascript")}
              </div>
            ))}
          </div>
        );
      case "styles":
        return (
          <div className="tab-content">
            <h3>Styling</h3>
            <p>{parsedMVP.styles?.description || "No styling description provided"}</p>
            {parsedMVP.styles?.code && renderCodeBlock(parsedMVP.styles.code, "css")}
          </div>
        );
      case "demo":
        return (
          <div className="tab-content">
            <h3>Live Demo</h3>
            <p>Below is a preview of how your application would look:</p>
            <div className="demo-container">
              {/* Mock representation of the application */}
              <div className="mock-app">
                <div className="mock-header">
                  <h4>Application Preview</h4>
                </div>
                <div className="mock-content">
                  <p>This is a visual representation of your MVP. In a production environment, this would be an interactive demo.</p>
                </div>
              </div>
            </div>
          </div>
        );
      default:
        return <p>Select a tab to view content</p>;
    }
  };

  return (
    <div style={{ padding: "20px", minHeight: "100vh", backgroundColor: "#222", color: "white" }}>
      {loading ? (
        <div className="loading-overlay">Generating MVP code...</div>
      ) : error ? (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={() => router.push("/product_viability_agent")}>
            Back to Product Viability Agent
          </button>
        </div>
      ) : (
        <>
          <header style={{ textAlign: "center", marginBottom: "20px" }}>
            <h1 style={{ fontSize: "2.5rem" }}>Software Engineering Agent</h1>
            <p>Review your generated MVP code</p>
          </header>

          {/* Tab Navigation */}
          <div className="tab-navigation">
            <button 
              className={activeTab === "overview" ? "active" : ""} 
              onClick={() => handleTabChange("overview")}
            >
              Overview
            </button>
            <button 
              className={activeTab === "components" ? "active" : ""} 
              onClick={() => handleTabChange("components")}
            >
              Components
            </button>
            <button 
              className={activeTab === "api" ? "active" : ""} 
              onClick={() => handleTabChange("api")}
            >
              API Integration
            </button>
            <button 
              className={activeTab === "styles" ? "active" : ""} 
              onClick={() => handleTabChange("styles")}
            >
              Styles
            </button>
            <button 
              className={activeTab === "demo" ? "active" : ""} 
              onClick={() => handleTabChange("demo")}
            >
              Demo
            </button>
          </div>

          {/* Tab Content */}
          <div className="content-container">
            {renderTabContent()}
          </div>

          {/* Navigation Buttons */}
          <div className="navigation-buttons">
            <button onClick={() => router.push("/product_viability_agent")}>
              Back to Product Viability Agent
            </button>
            <button onClick={() => router.push("/")}>
              Back to Home
            </button>
          </div>
        </>
      )}
    </div>
  );
}