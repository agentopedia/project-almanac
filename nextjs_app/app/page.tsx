"use client";
import Link from 'next/link';
import './styles/agents.css';

export default function Home() {
  return (
    <main style={{ marginTop: "2rem" }}>
      <h1 className="main-title">AGENTVILLE</h1>
      <p className="main-subtitle">Automate the creation of MVPs</p>

      {/* Get Started Button */}
      <Link href="/design_agent_input">
        <button className="button mt-8" style={{ fontSize: "1rem" }}>
          Get Started
        </button>
      </Link>
    </main>
  );
}