"use client";
import "../styles/agents.css";

export default function AboutPage() {
  return (
    <main className="about-page">
      <h1>About Almanac</h1>
      <div className="about-intro">
      <p>
        Almanac is an agentic AI system designed to help product managers — and anyone involved in building new products — move from idea to minimum viable product (MVP) quickly and efficiently. 
        Whether you're a PM, founder, designer, or developer, Almanac streamlines ideation, validation, and software generation using a powerful multi-agent architecture.
      </p>
      </div>

      <h2>How It Works</h2>
      <ul>
        <li><strong>Design Thinking Agent</strong> → Customer Persona + Empathy and Customer Journey Maps</li>
        <li><strong>Product Viability Agent</strong> → PRD + Business Analysis</li>
        <li><strong>SWE Agent</strong> → Fully Generated MVP</li>
        <li><strong>Customer Feedback Agent</strong> → Iterative Refinement</li>
      </ul>

      <h2>Meet the Team</h2>
      <ul>
      <li><strong>Karen Garcia</strong> – Database & Memory Logic</li>
        <li><strong>Ashley Hummel</strong> – Frontend & UI/UX</li>
        <li><strong>Neo Tyagi</strong> – LLM Engineering & SWE Agent</li>
        <li><strong>Aditi Kelwalkar</strong> – Agent Integration & Figma</li>
      </ul>
    </main>
  );
}
