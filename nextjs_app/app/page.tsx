// import Image from "next/image";
import Navbar from "./navbar";
import Link from 'next/link';

export default function Home() {
  return (
    
    <main style={{ marginTop: "2rem" }}>
    <h1 style={{color: "white", fontSize: "4rem", marginLeft: "2rem" }}>AGENTVILLE</h1>
    <p style={{color: "white", fontSize: "2rem", marginLeft: "2rem", marginBottom: "1.5rem" }}>Automate the creation of MVPs</p>

    {/* Get Started Button */}
    <Link href="/design_agent_input">
      <button style={{
        backgroundColor: "#007bff",
        color: "white",
        border: "none",
        padding: "0.75rem 1.25rem",
        fontSize: "1.25rem",
        cursor: "pointer",
        borderRadius: "0.25rem",
        marginLeft: "2rem"
      }}>
        Get Started
      </button>
    </Link>
  </main>
      
  );
}
