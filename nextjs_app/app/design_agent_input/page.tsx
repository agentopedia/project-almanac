import Link from 'next/link';

export default function DesignThinkingAgentInput() {
  return (
    <div style={{ padding: "2rem", color: "white", backgroundColor: "#222222", minHeight: "100vh", textAlign: "center" }}>
      {/* Title/subtitle */}
      <main style={{ marginTop: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>Design Thinking Agent</h1>
        <p style={{ fontSize: "1.25rem", marginBottom: "2rem" }}>Understand users, generate empathy maps, and shape the product vision</p>

        {/* Input Field */}
        <textarea
          placeholder="Enter Product Description Here"
          style={{
            width: "60%",
            height: "150px",
            padding: "1rem",
            fontSize: "1.25rem",
            borderRadius: "0.25rem",
            border: "1px solid #ccc",
            marginBottom: "1.5rem"
          }}
        />

        {/* Submit Button */}
        <Link href="/design_agent_output">
            <div>
            <button style={{
                backgroundColor: "#007bff",
                color: "white",
                border: "none",
                padding: "0.75rem 1.5rem",
                fontSize: "1.25rem",
                cursor: "pointer",
                borderRadius: "0.25rem"
            }}>
                Submit
            </button>
            </div>
        </Link>
      </main>
    </div>
  );
}