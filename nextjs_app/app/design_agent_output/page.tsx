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
    <div style={{ padding: "1rem", color: "white", backgroundColor: "#222222", minHeight: "100vh", textAlign: "center" }}>
      <main style={{ marginTop: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>

        {/* Flex container for side-by-side layout */}
        <div className="flex-container">
          <EmpathyMap empathyData={data.empathy_map} />
          <CustomerJourney journeyData={data.customer_journey} />
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