"use client";
import { useState } from "react";
import '../styles/agents.css';

interface Demographics {
  age: number;
  gender: string;
  occupation: string;
}

interface CustomerPersona {
  name: string;
  demographics: Demographics;
  description: string;
}

interface CustomerPersonaProps {
  persona: CustomerPersona;
  onUpdatePersona: (updatedPersona: CustomerPersona) => void;
}

export default function CustomerPersona({ persona, onUpdatePersona }: CustomerPersonaProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editedPersona, setEditedPersona] = useState<CustomerPersona>(persona);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setEditedPersona((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleDemographicsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setEditedPersona((prev) => ({
      ...prev,
      demographics: {
        ...prev.demographics,
        [name]: value,
      },
    }));
  };

  //need to change this so it goes back to backend
  const handleSave = async () => {
    setIsSaving(true);
    onUpdatePersona(editedPersona);

    try {
      const response = await fetch("/api/update_persona", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ customer: editedPersona }),
      });
      const responseData = await response.json();

      setIsEditing(false);
    } catch (error) {
      console.error("Error updating data in backend:", error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditedPersona(persona);
    setIsEditing(false);
  };

  return (
    <div style={{ marginBottom: "2rem", padding: "1rem", borderRadius: "8px", backgroundColor: "var(--primary-color)", color: "white", textAlign: "left" }}>
      <h2  style={{ fontSize: "1.75rem", textAlign: "left" }}>Customer Persona</h2>

      {isEditing ? (
      <div className="editingContainer">
        {/* Horizontal row for Name, Age, Gender, and Occupation */}
        <div className="inputRow">
          <div className="inputGroup">
            <label style={{ fontWeight: "bold" }}>Name:</label>
            <input type="text" name="name" value={editedPersona.name} onChange={handleChange} style={{ width: "100%", padding: "0.5rem", margin: "0.1rem 0", borderRadius: "5px" }} />
          </div>
      
          <div className="inputGroup">
            <label style={{ fontWeight: "bold" }}>Age:</label>
            <input type="number" name="age" value={editedPersona.demographics.age} onChange={handleDemographicsChange} style={{ width: "100%", padding: "0.5rem", margin: "0.1rem 0", borderRadius: "5px" }} />
          </div>
      
          <div className="inputGroup">
            <label style={{ fontWeight: "bold" }}>Gender:</label>
            <input type="text" name="gender" value={editedPersona.demographics.gender} onChange={handleDemographicsChange} style={{ width: "100%", padding: "0.5rem", margin: "0.1rem 0", borderRadius: "5px" }} />
          </div>
      
          <div className="inputGroup">
            <label style={{ fontWeight: "bold" }}>Occupation:</label>
            <input type="text" name="occupation" value={editedPersona.demographics.occupation} onChange={handleDemographicsChange} style={{ width: "100%", padding: "0.5rem", margin: "0.1rem 0", borderRadius: "5px" }} />
          </div>
        </div>
      
        {/* Description*/}
        <div className="descriptionGroup">
          <label style={{ fontWeight: "bold" }}>Description:</label>
          <textarea name="description" value={editedPersona.description} onChange={handleChange} className="descriptionField" />
        </div>
      
        {/* Buttons */}
        <div className="buttonGroup">
          {/* <button onClick={() => { handleSave(); console.log("clicked save");}} className="button button-secondary" disabled={isSaving}> {isSaving ? "Loading..." : "Save"}</button> */}
          <button 
            onClick={(e) => { if (isSaving) e.preventDefault(); handleSave(); }} 
            className="button button-secondary" 
            disabled={isSaving} 
            style={{ cursor: isSaving ? "not-allowed" : "pointer" }}>
            {isSaving ? "Loading..." : "Save"}
          </button>
          <button onClick={() => { handleCancel();}} style={{ padding: "0.5rem 1rem", backgroundColor: "var(--text-color-secondary)", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}>Cancel</button>
        </div>
      </div> 
      ) : (
        <div>
          <p style={{color: "white"}}><strong>Name:</strong> {persona.name}</p>
          <p style={{color: "white"}}><strong>Age:</strong> {persona.demographics.age}</p>
          <p style={{color: "white"}}><strong>Gender:</strong> {persona.demographics.gender}</p>
          <p style={{color: "white"}}><strong>Occupation:</strong> {persona.demographics.occupation}</p>
          <p style={{color: "white"}}><strong>Description:</strong> {persona.description}</p>
          
          <div style={{ display: "flex", justifyContent: "flex-end" }}>
            <button onClick={() =>{setIsEditing(true); setEditedPersona(persona)}} className="button button-secondary">Edit</button>
          </div>
        </div>
      )}
    </div>
  );
}
