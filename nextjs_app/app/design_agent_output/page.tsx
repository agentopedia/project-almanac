"use client";
import Link from 'next/link';
import EmpathyMap from '../components/EmpathyMap';
import CustomerJourney from '../components/CustomerJourney';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';

// TODO this is just sample data so that you can test out the UI design without using an API call
const data = {
  "customer_persona": [
    {
      "name": "Professor Annelise",
      "demographics": {
        "age": 45,
        "gender": "Female",
        "occupation": "Biology Professor"
      },
      "description": "Annelise is a dedicated biology professor with a passion for herpetology. She is always looking for engaging and reliable resources to use in her classes and for her own research. She values accuracy and up-to-date information, and appreciates user-friendly interfaces that make it easy to find what she needs.",
    }
  ],
  "empathy_map": {
    "says": [
      "I need a reliable source of information on frog species.",
      "My students need engaging learning materials.",
      "It's difficult to find all the information I need in one place."
    ],
    "thinks": [
      "This web app could save me a lot of time.",
      "I hope the information is accurate and up-to-date.",
      "Will this app be engaging enough for my students?"
    ],
    "does": [
      "Searches online for frog information.",
      "Looks through textbooks and journals.",
      "Prepares lectures and assignments using various resources."
    ],
    "feels": [
      "Frustrated by the lack of a comprehensive resource.",
      "Overwhelmed by the amount of information to sift through.",
      "Excited about the potential of a user-friendly web app."
    ]
  },
  "customer_journey_map": {
    "awareness": "Annelise hears about the web app from a colleague at a conference.", 
    "comparison": "She compares the web app to other online resources, checking for accuracy, comprehensiveness, and user-friendliness.",
    "purchase": "She decides to use the web app for its comprehensive information and engaging features, free of charge.",
    "installation": "She easily accesses the web app through her browser and finds the interface intuitive and easy to navigate."
  },
  "problem_statement": "Biology professors and students lack a comprehensive, accurate, and engaging online resource for learning about frog species, leading to frustration, time wasted on searching multiple sources, and a suboptimal learning experience."      
};

export default function DesignThinkingAgentOutput() {
  //if you want to use dummy data, comment out everything above const router = useRouter();
  const searchParams = useSearchParams();
  const result = searchParams.get('result'); // get 'result' query parameter from URL
  let parsedData;
  if (result) {
    try {
      parsedData = JSON.parse(decodeURIComponent(result)); // decode the URL-encoded string and parse it as JSON
      if (parsedData.result) {
        parsedData.result = JSON.parse(parsedData.result);
      }
    } catch (error) {
      console.error('Json not formatted correctly:', error);
    }
  }
  console.log('Raw Result:', result); 
  console.log('Parsed Data:', parsedData)
  console.log("result: ", parsedData.result)

  const router = useRouter();

  const handleProceed = async () => {
    try {
      // make a GET request to the Next.js API route
      const response = await fetch("/api/viability", {
        method: "GET",
      });
      const data = await response.json();
  
      if (response.ok) {
        console.log("Data from Flask server:", data);
        const encodedData = encodeURIComponent(JSON.stringify(data));
        router.push(`/product_viability_agent?data=${encodedData}`);
      } else {
        console.error("Failed to fetch data:", data);
      }
    } catch (error) {
      console.error("Error during the GET request:", error);
    }
  };  
  
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        color: "white",
        textAlign: "center",
      }}
    >
      <main style={{ width: "80%" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>

        {/* Customer Persona Section */}
        <div
          style={{
            marginBottom: "2rem",
            padding: "1rem",
            borderRadius: "8px",
            backgroundColor: "var(--primary-color)",
            color: "white",
            textAlign: "left",
          }}
        >
          <h2 style={{fontSize: "1.75rem", textAlign: "center" }}>
            Customer Persona
          </h2>
          <p>
            <span style={{ fontWeight: "bold", color: "white" }}>Name:</span>{" "}
            {parsedData?.result?.customer_persona[0].name || "N/A"}
          </p>
          <p>
            <span style={{ fontWeight: "bold", color: "white" }}>Demographics:</span>{" "}
            {`Age: ${parsedData?.result?.customer_persona[0].demographics.age || "N/A"}, `}
            {`Gender: ${parsedData?.result?.customer_persona[0].demographics.gender || "N/A"}, `}
            {`Occupation: ${parsedData?.result?.customer_persona[0].demographics.occupation || "N/A"}`}
          </p>
          <p>
            <span style={{ fontWeight: "bold", color: "white" }}>Description:</span>{" "}
            {parsedData?.result?.customer_persona[0].description || "N/A"}
          </p>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between", // space btwn the components
            gap: "1rem"
          }}
        >
          {/* Empathy Map */}
          <EmpathyMap empathyData={parsedData?.result?.empathy_map || {}} />

          {/* Customer Journey Map */}
          <CustomerJourney journeyData={parsedData?.result?.customer_journey_map || {}} />
        </div>

        {/* Navigation Buttons */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "2rem",
          }}
        >
          <button
            onClick={() => router.push("/design_agent_input")}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "var(--primary-color)",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Back to Product Ideation
          </button>
          <button
            onClick={handleProceed}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "var(--primary-color)",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Proceed to Product Viability Agent
          </button>
        </div>
      </main>
    </div>
  );
}