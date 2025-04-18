"use client";
import { useEffect } from 'react';
import Link from 'next/link';
import './styles/agents.css';

export default function Home() {
  useEffect(() => {
    sessionStorage.setItem("productIdeationComplete", "true");
  }, []);

  return (
    <main style={{ marginTop: "1rem" }}>
      <div className="home-container">
        <h1 className="main-title">ALMANAC</h1>
        <p className="main-subtitle">Automate the creation of MVPs</p>

        {/* Get Started Button */}
        <Link href="/design_agent_input">
          <button className="button mt-8" style={{ fontSize: "1rem" }}>
            Get Started
          </button>
        </Link>
      </div>
    </main>
  );
}