"use client";
import React from "react";
import '../styles/agents.css';

const SideNav: React.FC = () => {
  return (
    <nav className="sidenav">
      <ul>
        <li><a href="#home">Home</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#tutorials">Tutorials</a></li>
      </ul>
    </nav>
  );
};

export default SideNav;
