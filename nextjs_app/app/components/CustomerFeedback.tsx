"use client";
import { useState } from "react";
import '../styles/agents.css';
import JSON5 from "json5";


interface CustomerFeedback {
    overview: string;
    usability: string;
    content: string;
    appearance: string;
    improvements: string[];
  }

const defaultFeedback: CustomerFeedback = {
  overview: "Loading...",
  usability: "Loading...",
  content: "Loading...",
  appearance: "Loading...",
  improvements: ["Loading..."]
};

export default function CustomerFeedback() {
    const [feedback, setFeedback] = useState<CustomerFeedback>(defaultFeedback);
    const [isFetching, setIsFetching] = useState<boolean>(true);
    const [feedbackFirstPress, setFeedbackFirstPress] = useState<boolean>(false);


    const getFeedback = async () => {
        setFeedbackFirstPress(true);
        setIsFetching(true);
        console.log("getting feedback");
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
    
    const testingDisabledButton = () => {
        console.log("button clicked");
    
    }

    return (
            <div style={{ marginBottom: "2rem", padding: "1rem", borderRadius: "8px", backgroundColor: "var(--primary-color)", color: "white", textAlign: "left", display: "flex", flexDirection: "column"}}>
            <h2  style={{ fontSize: "1.75rem", textAlign: "left" }}>Customer Feedback</h2>
              {/* Information */}
              <div >
                <p style={{color: "white", marginBottom: "0px"}}><strong>Overview:</strong></p>
                  <p style={{color: "white"}}> {feedback?.overview}</p>
                <p style={{color: "white", marginBottom: "0px"}}><strong>Usability:</strong></p>
                  <p style={{color: "white"}}> {feedback?.usability}</p>
                <p style={{color: "white", marginBottom: "0px"}}><strong>Content:</strong></p>
                  <p style={{color: "white"}}> {feedback?.content}</p>  
                <p style={{color: "white", marginBottom: "0px"}}><strong>Appearance:</strong></p>
                  <p style={{color: "white"}}> {feedback?.appearance}</p>
                <p style={{color: "white", marginBottom: "0px"}}><strong>Improvements:</strong></p>
                  {feedback?.improvements.map((item, index) => (
                    <p key={index} style={{color: "white", marginBottom: "0px" }}>
                      {index+1}. {item}
                    </p>
                   ))}
              {/* Buttons */}
              <div className="buttonGroup" >
                <button className="button button-secondary" onClick={testingDisabledButton} disabled={isFetching}>Regenerate Feedback</button>
                <button className="button button-secondary" onClick={testingDisabledButton} disabled={isFetching}>Edit</button>
              </div>
              </div>
            </div>
          
    );
}