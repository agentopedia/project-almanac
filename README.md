# 🧠 Project Almanac — Agents as the Backend

Welcome to the open-source repository of **Project Almanac**, a platform that turns product ideas into working web apps using autonomous AI agents.

> 📌 TL;DR: Agents don’t generate backend code here — they *are* the backend.  
> Agents act as live, intelligent, tool-connected services powering each phase of the product lifecycle.

---

## 🚀 What is Project Almanac?

Almanac is an agentic platform that lets users go from **idea to app** with zero code.  
Each major step — from customer research to product requirements to full-stack prototyping — is handled by a specialized agent that acts as the system backend, connected to APIs, search tools, and databases.

This repo contains the full source code for:
- 🌐 A Next.js frontend
- 🧪 A Flask + LangChain agent backend
- 🧠 Modular agents for Design Thinking, Product Viability, Business Model Generation, and Software Engineering
- 🧾 Persistent data storage using MongoDB Atlas

Want to see Almanac in action? Watch the walkthrough:

(https://www.youtube.com/watch?v=NsgrmdYgOOY)

---

## 🧩 How It Works

Almanac’s flow consists of a sequence of AI agents, each one specializing in a stage of product development. The frontend simply acts as the renderer — the agents are the logic layer.

### Agent Flow

1. **Product Ideation**  
   Input a product idea on the first screen.

2. **Design Thinking Agent**  
   Generates:
   - Customer Persona (name, age, job, context)
   - Empathy Map (says, thinks, does, feels)
   - Customer Journey Map (awareness → install)
   - Problem Statement

3. **Product Viability & Business Model Agents**  
   Generates:
   - 📝 PRD (Goals, Features, Functional/Non-Functional Reqs)
   - 💼 Business Model (Target Market, Revenue Streams, Channels)

4. **Software Engineering Agent**  
   Builds:
   - 🎯 Interactive MVP UI
   - 🧠 RAG-powered content using Tavily
   - 🎨 Dynamic pages with working buttons/forms

5. **Frontend**  
   Renders the JSON output from each agent as styled React pages with state syncing to MongoDB.

---

## 🧠 Philosophy: Agents *Are* the Backend

Almanac's core thesis:

> Instead of writing backend code that wraps APIs, stores logic, and moves data — let intelligent agents handle it **in real-time**.

- No YAML workflows.
- No prompt-chains.
- No server-side code generation.
- Just stateful, context-rich agents that act as backend services.

---

## 📁 Folder Structure

```bash
nextjs_app/
├── components/          # React components (e.g. EmpathyMap, JourneyMap)
├── pages/               # Each major agent page
├── styles/              # agents.css, mvp.css
├── api/                 # API routes for frontend-backend communication
├── flask_backend/       
│   ├── agent.py         # Base agent class
│   ├── design_agent.py
│   ├── business_model_agent.py
│   ├── viability_agent.py
│   ├── swe_agent.py
│   └── swe_verifier_agent.py
└── app.py               # Flask app routing backend agent services
