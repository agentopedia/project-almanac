"use client";
import Link from 'next/link';
import EmpathyMap from '../components/EmpathyMap';
import CustomerJourney from '../components/CustomerJourney';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { resourceUsage } from 'process';

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
  const searchParams = useSearchParams();
  const result = searchParams.get('result'); // Get 'result' query parameter
  let parsedData;
  if (result) {
    try {
      parsedData = JSON.parse(decodeURIComponent(result)); // Decode the URL-encoded string and parse it as JSON
      if (parsedData.result) {
        parsedData.result = JSON.parse(parsedData.result);
      }
    } catch (error) {
      console.error('Json not formatted correctly:', error);
    }
  }
  // console.log('Raw Result:', result); 
  // console.log('Parsed Data:', parsedData)
  // console.log("result: ", parsedData.result)

  
  return (
    <div style={{ padding: "1rem", color: "white", backgroundColor: "#222222", minHeight: "100vh", textAlign: "center" }}>
      <main style={{ marginTop: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>

        {/* Flex container for side-by-side layout */}
        <div className="flex-container">
          <EmpathyMap empathyData={parsedData.result.empathy_map} />
          <CustomerJourney journeyData={parsedData.result.customer_journey_map} />
        </div>

        {/* Navigation Button */}
        <Link href="/business_model_agent">
          <button className="button mt-8" style={{ padding: "0.75rem 1.5rem", fontSize: "1rem", borderRadius: "0.25rem" }}>
            Proceed to Business Model Agent
          </button>
        </Link>
      </main>
    </div>
  );
}