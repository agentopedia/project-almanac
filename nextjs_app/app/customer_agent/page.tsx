"use client";
import { useState, useEffect } from "react";
import JSON5 from "json5";
import CustomerPersona from "../components/CustomerPersona";
import '../styles/agents.css';

interface CustomerPersona {
  name: string;
  demographics: {
    age: number;
    gender: string;
    occupation: string;
  };
  description: string;
}

interface CustomerFeedback {
  overview: string;
  usability: string;
  content: string;
  appearance: string;
  improvements: string[];
}

const defaultPersona: CustomerPersona = {
  name: "Loading...",
  demographics: {
    age: 0,
    gender: "Loading...",
    occupation: "Loading...",
  },
  description: "Loading...",
};

const defaultFeedback: CustomerFeedback = {
  overview: "Loading...",
  usability: "Loading...",
  content: "Loading...",
  appearance: "Loading...",
  improvements: ["Loading..."]
};

export default function CustomerFeedbackAgent() {
  const [activeTab, setActiveTab] = useState("Customer");
  const [persona, setPersona] = useState<CustomerPersona>(defaultPersona);
  const [feedback, setFeedback] = useState<CustomerFeedback>(defaultFeedback);
  const [editedFeedback, setEditedFeedback] = useState<CustomerFeedback>(defaultFeedback);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isEditingFeedback, setIsEditingFeedback] = useState<boolean>(false);
  const [feedbackFirstPress, setFeedbackFirstPress] = useState<boolean>(false);
  
  useEffect(() => {
    async function fetchPersona() {
      try {
        const response = await fetch("/api/design_input");
        if (!response.ok) {
          throw new Error("Failed to fetch persona data");
        }
        const data = await response.json();
        const parsed = JSON5.parse(data.result);
        
        if (parsed?.customer_persona?.length > 0) {
          setPersona(parsed.customer_persona[0]); // Load persona data
        }
      } catch (error) {
        console.error("Error fetching persona data:", error);
      }
    }

    fetchPersona();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setEditedFeedback((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleImprovementsChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const updatedImprovements = e.target.value.split("\n"); // Split input by newlines
    setEditedFeedback({
      ...editedFeedback,
      improvements: updatedImprovements, // Update the improvements array
    });
  };

  //call this function when the feedback tab is pressed - we make an api call
  const getFeedback = async () => {
    setFeedbackFirstPress(true);
    setIsFetching(true);
    //set up API route for customer feedback
    try {
      const response = await fetch("/api/customer_feedback");
      if (!response.ok) {
        throw new Error("Failed to fetch feedback data");
      }
      const data = await response.json();
      const parsed = JSON5.parse(data.result);
      console.log(parsed)
      setFeedback(parsed)
    } catch (error) {
      console.error("Error fetching feedback data:", error);
    }
    setIsFetching(false); 
  };

  const handleSave = async () => {
    setIsSaving(true);
    setFeedback(editedFeedback);
    try {
      const response = await fetch("/api/update_feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ feedback: editedFeedback }),
      });
      const responseData = await response.json();

      setIsEditingFeedback(false);
    } catch (error) {
      console.error("Error updating data in backend:", error);
    } finally {
      setIsSaving(false);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case "Customer":
        return (

        <main style={{ width: "60%" }}>
          <CustomerPersona persona={persona} onUpdatePersona={setPersona} />
        </main>
      );
      case "Feedback":
        return (
          <main style={{ width: "60%" }}>
            <div style={{ marginBottom: "2rem", padding: "1rem", borderRadius: "8px", backgroundColor: "var(--primary-color)", color: "white", textAlign: "left", display: "flex", flexDirection: "column"}}>
            <h2  style={{ fontSize: "1.75rem", textAlign: "center" }}>Customer Feedback</h2>
            {isEditingFeedback ? (
              <div className="editingContainer">
                {/* Input fields for editing feedback */}
                <div className="descriptionGroup">
                  <label style={{ fontWeight: "bold" }}>Overview:</label>
                  <textarea name="overview" value={editedFeedback.overview} onChange={handleChange} className="descriptionField" />
                </div>

                <div className="descriptionGroup">
                  <label style={{ fontWeight: "bold" }}>Functionality:</label>
                  <textarea name="usability" value={editedFeedback.usability} onChange={handleChange} className="descriptionField" />
                </div>

                <div className="descriptionGroup">
                  <label style={{ fontWeight: "bold" }}>Content:</label>
                  <textarea name="content" value={editedFeedback.content} onChange={handleChange} className="descriptionField" />
                </div>

                <div className="descriptionGroup">
                  <label style={{ fontWeight: "bold" }}>Appearance:</label>
                  <textarea name="appearance" value={editedFeedback.appearance} onChange={handleChange} className="descriptionField" />
                </div>

                <div className="descriptionGroup">
                  <label style={{ fontWeight: "bold" }}>Improvements:</label>
                  <textarea name="improvements" value={editedFeedback.improvements.join("\n")} onChange={handleImprovementsChange} className="descriptionField" />
                </div>

                
                {/* Buttons */}
                <div className="buttonGroup">
                <button 
                  onClick={(e) => { if (isSaving) e.preventDefault(); handleSave(); }} 
                  className="button button-secondary" 
                  disabled={isSaving}>
                  {isSaving ? "Saving..." : "Save"}
                </button>
                  <button onClick={() => { setEditedFeedback(feedback); setIsEditingFeedback(false);}} style={{ padding: "0.5rem 1rem", backgroundColor: "var(--text-color-secondary)", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}>Cancel</button>
                </div>
              </div>
            ) : (
              // Display the feedback information when not editing
              <div>
                {/* Information */}
                <p style={{color: "white", marginBottom: "0px"}}><strong>Overview:</strong></p>
                  <p style={{color: "white", backgroundColor: "#00aaff", borderRadius: "10px", padding: "10px"}}> {feedback?.overview}</p>
                <p style={{color: "white", marginBottom: "0px"}}><strong>Functionality:</strong></p>
                  <p style={{color: "white", backgroundColor: "#00aaff", borderRadius: "10px", padding: "10px"}}> {feedback?.usability}</p>
                <p style={{color: "white", marginBottom: "0px"}}><strong>Content:</strong></p>
                  <p style={{color: "white", backgroundColor: "#00aaff", borderRadius: "10px", padding: "10px"}}> {feedback?.content}</p>  
                <p style={{color: "white", marginBottom: "0px"}}><strong>Appearance:</strong></p>
                  <p style={{color: "white", backgroundColor: "#00aaff", borderRadius: "10px", padding: "10px"}}> {feedback?.appearance}</p>
                
                <p style={{color: "white", marginBottom: "0px"}}><strong>Improvements:</strong></p>
                  <div style={{backgroundColor: "#00aaff", borderRadius: "10px", padding: "10px"}}>
                    {feedback?.improvements.map((item, index) => (
                      <p key={index} style={{color: "white", marginBottom: "0px"}}>
                        {index+1}. {item}
                      </p>
                    ))}
                  </div>
                
                {/* Buttons */}
                <div className="buttonGroup" >
                  <button className="button button-secondary" onClick={getFeedback} disabled={isFetching}>Regenerate Feedback</button>
                  <button className="button button-secondary" onClick={() =>{setIsEditingFeedback(true); setEditedFeedback(feedback)}} disabled={isFetching}>Edit</button>
                </div>
              </div>
            )}
            </div>

          </main>
        );

      case "MVPs":
        return (
          <main style={{ width: "60%" }}>
            <div style={{ marginBottom: "2rem", padding: "1rem", borderRadius: "8px", backgroundColor: "var(--primary-color)", color: "white", textAlign: "left", display: "flex", flexDirection: "column"}}>
            <h2  style={{ fontSize: "1.75rem", textAlign: "center" }}>MVPs</h2>
              <p>Iterate through MVPs based on customer feedback</p>


            </div>
          </main>
        );

      default:
        return null;
    }
  };

  return (
    <div className="container">
      {/* Header */}
      <header style={{ textAlign: "center", color: "white" }}>
          <h1 style={{ fontSize: "2.5rem" }}>Customer Feedback Agent</h1>
          <p style={{ fontSize: "1.3rem" }}>Receive Feedback and Iterate through MVPs</p>
      </header>

      {/* Selection Tabs */}
      <div className="flex-container mb-4">
        {["Customer", "Feedback", "MVPs"].map((tab) => (
          <button
            key={tab}
            className={`button ${activeTab === tab ? "button-secondary" : ""}`}
            onClick={() => {
              setActiveTab(tab); 
              if (tab === "Feedback" && !feedbackFirstPress) {
                getFeedback();
              }
            }}
          >
            {tab}
          </button>
        ))}
      </div>
      {renderContent()}
    </div>
  );
}
