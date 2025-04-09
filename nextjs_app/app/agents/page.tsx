"use client";
import Link from "next/link";
import "../styles/agents.css";

export default function AgentsPage() {
  const agents = [
    {
      name: "Product Ideation",
      path: "/design_agent_input",
      isActive: true,
    },
    {
      name: "Design Thinking Agent",
      path: "/design_agent_output",
      isActive: true,
    },
    {
      name: "Product Viability Agent",
      path: "/product_viability_agent",
      isActive: true,
    },
    {
      name: "Software Engineering Agent",
      path: "/swe",
      isActive: true,
    },
    {
      name: "Generated MVP",
      path: "/generatedmvp",
      isActive: true,
    }
  ];

  return (
    <main className="agents-page">
      <h1 className="main-title">Agents</h1>

      <div className="agent-button-grid">
        {agents.map((agent, index) =>
          agent.isActive ? (
            <Link key={index} href={agent.path}>
              <button className="agent-button">{agent.name}</button>
            </Link>
          ) : (
            <button
              key={index}
              className="agent-button disabled"
              disabled
            >
              {agent.name}
            </button>
          )
        )}
      </div>
    </main>
  );
}
