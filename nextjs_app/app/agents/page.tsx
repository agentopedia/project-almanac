"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import "../styles/agents.css";

export default function AgentsPage() {
  const [completionStatus, setCompletionStatus] = useState({
    productIdeation: false,
    designThinking: false,
    productViability: false,
    swe: false,
    mvp: false,
  });

  useEffect(() => {
    setCompletionStatus({
      productIdeation: sessionStorage.getItem("productIdeationComplete") === "true",
      designThinking: sessionStorage.getItem("designThinkingComplete") === "true",
      productViability: sessionStorage.getItem("productViabilityComplete") === "true",
      swe: sessionStorage.getItem("sweComplete") === "true",
      mvp: sessionStorage.getItem("generatedMVPComplete") === "true",
    });
  }, []);

  const agents = [
    {
      name: "Product Ideation",
      path: "/design_agent_input",
      isActive: completionStatus.productIdeation,
    },
    {
      name: "Design Thinking Agent",
      path: "/design_agent_output",
      isActive: completionStatus.designThinking,
    },
    {
      name: "Product Viability Agent",
      path: "/product_viability_agent",
      isActive: completionStatus.productViability,
    },
    {
      name: "Software Engineering Agent",
      path: "/swe",
      isActive: completionStatus.swe,
    },
    {
      name: "Generated MVP",
      path: "/generatedmvp",
      isActive: completionStatus.mvp,
    }
  ];

  return (
    <main className="agents-page">
      <h1 className="main-title">Agents</h1>
      <p className="main-subtitle">Finish each stage to unlock the next agent.</p>
      <div className="agent-button-grid">
        {agents.map((agent, index) =>
          agent.isActive ? (
            <Link key={index} href={agent.path}>
              <button className="agent-button">{agent.name}</button>
            </Link>
          ) : (
            <button key={index} className="agent-button disabled" disabled>
              {agent.name}
            </button>
          )
        )}
      </div>
    </main>
  );
}