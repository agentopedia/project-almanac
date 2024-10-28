import Link from 'next/link';
import EmpathyMap from '../components/EmpathyMap';
import CustomerJourney from '../components/CustomerJourney';

// TODO just sample data for now
const data = {
  "empathy_map": {
    "says": ["What the persona verbally expresses about the problem."],
    "thinks": ["What the persona is thinking internally."],
    "does": ["Actions the persona takes to address the problem."],
    "feels": ["Emotions experienced by the persona."]
  },
  "customer_journey": {
    "awareness": "How the persona becomes aware of the product or problem.",
    "comparison": "How the persona evaluates different options.",
    "purchase": "Factors influencing the purchase decision.",
    "installation": "Persona's experience with setting up or using the product."
  }
};

export default function DesignThinkingAgentOutput() {
    return (
    <div style={{ padding: "2rem", color: "white", backgroundColor: "#222222", minHeight: "100vh", textAlign: "center" }}>
        {/* Title */}
        <main style={{ marginTop: "2rem" }}>
          <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>
          <p style={{ fontSize: "1.25rem", marginBottom: "2rem" }}>TODO Put output in text form</p>
          <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-6">
            <EmpathyMap empathyData={data.empathy_map}/>
          </div>
          <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-6">
            <CustomerJourney journeyData={data.customer_journey} />
          </div>
        </main>
    </div>
  );
}