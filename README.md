# Lead Scoring Agent

An AI-powered lead scoring and analysis agent that automates lead qualification, enrichment, and prioritization. Built with LangChain, MCP integrations, and Next.js 15.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)

## Problem Statement

Sales teams struggle with lead management:
- **Volume Overload**: Too many leads to manually research and qualify
- **Inconsistent Scoring**: Manual scoring leads to missed opportunities
- **Missing Context**: Lack of enriched data for informed outreach
- **Slow Response**: Delayed follow-up loses high-intent prospects

## Solution

Lead Scoring Agent provides intelligent lead scoring and enrichment:

1. **Lead Scoring**: AI-powered scoring based on multiple signals
2. **Data Enrichment**: Automatic company and contact enrichment
3. **Intent Analysis**: Behavioral and contextual intent signals
4. **Prioritization**: Smart lead routing and prioritization
5. **Insights Generation**: Actionable insights for sales outreach

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Next.js 15 Frontend                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Dashboard │  │  Leads   │  │ Scoring  │  │     Insights     │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │ REST API
┌─────────────────────────────▼───────────────────────────────────┐
│                     FastAPI Backend                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   LangChain Agent Core                       ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  ││
│  │  │Lead Scorer  │  │Enrichment   │  │Intent Analyzer      │  ││
│  │  │   Agent     │  │   Agent     │  │     Agent           │  ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    MCP Integrations                          ││
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────────────────┐ ││
│  │  │  CRM   │  │Clearbit│  │LinkedIn│  │   Email Provider   │ ││
│  │  │  MCP   │  │  MCP   │  │   MCP  │  │        MCP         │ ││
│  │  └────────┘  └────────┘  └────────┘  └────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - High-performance async API
- **LangChain 0.3+** - Agent orchestration
- **ChromaDB** - Vector storage for similarity search
- **Pydantic** - Data validation

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first styling
- **React Query** - Server state management

### MCP Integrations
- **CRM MCP** - Salesforce/HubSpot integration
- **Clearbit MCP** - Company/contact enrichment
- **LinkedIn MCP** - Professional data
- **Email MCP** - Email verification

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/VaibhavJeet/lead-scoring-agent.git
cd lead-scoring-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Configuration

### LLM Configuration

```env
# Remote LLM
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key

# Local LLM
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

## Features

### Lead Scoring
- Multi-factor scoring model
- Customizable scoring criteria
- Real-time score updates
- Score history tracking

### Data Enrichment
- Company firmographics
- Contact information
- Social profiles
- Technology stack detection

### Intent Analysis
- Website behavior tracking
- Email engagement signals
- Content interaction
- Buying stage prediction

## API Reference

### Leads
- `POST /api/leads` - Create new lead
- `GET /api/leads` - List leads
- `POST /api/leads/{id}/score` - Score a lead
- `POST /api/leads/{id}/enrich` - Enrich lead data

### Scoring
- `GET /api/scoring/models` - List scoring models
- `POST /api/scoring/batch` - Batch score leads

## Project Structure

```
lead-scoring-agent/
├── backend/
│   ├── app/
│   │   ├── agents/           # LangChain agents
│   │   │   ├── lead_scorer.py
│   │   │   ├── enrichment_agent.py
│   │   │   └── intent_analyzer.py
│   │   ├── mcp/              # MCP integrations
│   │   ├── models/           # Pydantic models
│   │   ├── api/              # FastAPI routes
│   │   └── core/             # Configuration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # React components
│   │   └── lib/              # Utilities
│   └── package.json
└── docker-compose.yml
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
