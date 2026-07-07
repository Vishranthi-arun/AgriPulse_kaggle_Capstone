# AgriPulse_kaggle_Capstone
# 🌾 AgriPulse – Agentic AI for Smart Farming

> An autonomous farming assistant built with **Google Antigravity**, **Gemini**, and the **Model Context Protocol (MCP)** that provides intelligent, grounded, and safe recommendations for irrigation, pest detection, crop scheduling, and market timing.

---

## 🚀 Overview

AgriPulse is an **Agentic AI application** designed to support farmers in making informed agricultural decisions.

Unlike a traditional chatbot, AgriPulse autonomously retrieves real-world weather and market information using MCP servers, reasons over the data using Gemini, and provides explainable recommendations while enforcing Human-in-the-Loop (HITL) safety for high-risk actions.

---

## ✨ Features

- 🌦️ Weather-aware irrigation recommendations
- 🐛 Pest risk detection using environmental conditions
- 📈 Market timing recommendations based on crop prices
- 📅 Crop calendar reminders
- 🤖 Autonomous scheduled workflows
- 🛡️ Human-in-the-Loop approval for high-risk decisions
- 🔒 Prompt injection protection
- 📚 Grounded responses using external MCP tools
- 💾 Lightweight memory for contextual recommendations

---

# 🏗️ System Architecture

```
                   Cloud Scheduler
                          │
                          ▼
                 AgriPulse Agent
          (Google Antigravity + Gemini)
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    Weather MCP     Market Price MCP   Google Developer
                                         Knowledge MCP
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                    Gemini Reasoning
                          ▼
          Irrigation • Pest • Market • Calendar
                          ▼
           Notification / Human-in-the-Loop
```

---

# 🧠 Agent Design

AgriPulse is driven by:

- **AGENTS.md**
  - Agent identity
  - Safety policies
  - Grounding rules
  - Prompt injection protection
  - Human-in-the-Loop guardrails

- **Skills**
  - Irrigation Advice
  - Pest Detection
  - Market Timing
  - Crop Calendar

- **MCP Tools**
  - Weather MCP
  - Market Price MCP
  - Google Developer Knowledge MCP

---

# 🌦️ Skills

## 💧 Irrigation Advice

Uses:

- Weather MCP

Provides:

- Weather-aware irrigation recommendations
- Farmer-friendly explanations
- Automatic notifications (LOW Risk)

---

## 🐛 Pest Detection

Uses:

- Weather MCP
- Google Developer Knowledge MCP

Provides:

- Pest and fungal disease risk analysis
- Organic preventive recommendations
- Human confirmation for MEDIUM Risk actions

---

## 📈 Market Timing

Uses:

- Market Price MCP

Provides:

- Price trend analysis
- Sell / Wait recommendations
- Human approval before financial decisions

---

## 📅 Crop Calendar

Uses:

- Google Developer Knowledge MCP

Provides:

- Seasonal reminders
- Sowing guidance
- Fertilizer reminders
- Harvest planning

---

# 🔌 MCP Integrations

## Weather MCP

Retrieves

- Temperature
- Humidity
- Wind Speed
- Rainfall Probability

Source:

Open-Meteo API

---

## Market Price MCP

Provides

- Crop prices
- Market trends

(Currently implemented with mock data.)

---

## Google Developer Knowledge MCP

Provides

- Agricultural best practices
- Technical documentation
- Grounded knowledge

---

# 🛡️ Human-in-the-Loop (HITL)

AgriPulse classifies actions into three categories.

| Risk Level |        Behaviour                              |
|------------|-----------------------------------------------|
| 🟢 LOW    | Automatically notify the farmer                |
| 🟡 MEDIUM | Ask for one-tap confirmation                   |
| 🔴 HIGH   | Pause execution and wait for explicit approval |

Examples of HIGH-risk actions:

- Chemical pesticide purchase
- Crop sale decisions
- Financial recommendations

---

# 🔒 Safety Features

- Prompt Injection Protection
- Grounded responses using MCP data
- Transparent handling of unavailable tools
- Human-in-the-Loop approval
- Never fabricates weather or market information

---

# ⏰ Autonomous Scheduling

AgriPulse supports autonomous execution.

### Every 6 Hours

```
Retrieve Weather
        ↓
Run Irrigation Skill
        ↓
Run Pest Detection Skill
        ↓
Notify Farmer
```

### Market Updates

```
New Market Price
        ↓
Run Market Timing Skill
        ↓
Wait for HITL Approval (if required)
```

---

# 📁 Project Structure

```
agripulse/
│
├── .agents/
│   └── skills/
│       ├── irrigation-advice/
│       ├── pest-detection/
│       ├── market-timing/
│       └── crop-calendar/
│
├── weather-mcp/
├── market-price-mcp/
│
├── agripulse/
│   ├── memory/
│   └── sub_agents/
│
├── AGENTS.md
├── config.py
└── README.md
```

---

# 🛠️ Technologies Used

- Google Antigravity
- Google Gemini
- Model Context Protocol (MCP)
- Python
- FastMCP
- Open-Meteo API
- Google Developer Knowledge MCP

---

# 📸 Demo

### Low Risk

Weather

↓

Irrigation Recommendation

↓

Auto Notification

---

### Medium Risk

High Humidity

↓

Pest Detection

↓

One-Tap Confirmation

---

### High Risk

Chemical Pesticide Purchase

↓

Explain Recommendation

↓

Wait for Human Approval

---

# 🚀 Future Improvements

- Cloud Run deployment
- Agent Runtime deployment
- Firestore memory backend
- IoT sensor integration
- Satellite imagery analysis
- Mobile application
- Regional language voice assistant

---

# 🎥 Demo Video

📺 YouTube

*Add your YouTube demo link here*
