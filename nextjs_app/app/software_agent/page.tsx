"use client";
import React from "react";
import '../globals.css';
import SideNav from "../components/SideNav";

const Software_Agent: React.FC = () => {
  return (
    <div className="page-container">
      <SideNav />

      <main className="container">
        <header className="header">
          <h1 className="title">Title of MVP</h1>
          <p className="subtitle">Sub caption</p>
        </header>

        <section className="swe-section">
          <div className="swe-card">
            <h2 className="cardTitle">Feature 1</h2>
            <p className="cardText">Sub caption</p>
          </div>

          <div className="swe-card">
            <h2 className="cardTitle">Feature 2</h2>
            <p className="cardText">Sub caption</p>
          </div>

          <div className="swe-card">
            <h2 className="cardTitle">Tutorials</h2>
            <p className="cardText">Real world examples for the product</p>
          </div>
        </section>

        <div style={{ marginTop: "2rem" }}>
          <button className="button">Get Started</button>
        </div>
      </main>
    </div>
  );
};

export default Software_Agent;
