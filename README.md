# AI-Powered Customer Support Triage
> Multi-Agent RAG Pipeline with Pinecone & Gemini | Research PoC

---

## Overview

Customer support operations rely on inconsistent human judgement to triage, escalate, and resolve issues at scale. This project demonstrates an **agentic AI pipeline** that standardises escalation decisions and automates supervisor-level resolution recommendations — reducing agent involvement while ensuring a consistent, policy-aligned customer journey.

Built as a Research PoC for demonstrating technical feasibility of multi-agent RAG systems in a CCaaS/UCaaS support context.

---

## Architecture

```
User Query
     ↓
┌─────────────────────────────────────────┐
│         AGENT 1: RETRIEVAL              │
│  Searches namespace: support-docs       │
│  Searches namespace: action-logs        │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│         AGENT 2: EVALUATION             │
│  Severity score (1–5) · sentiment       │
│  Issue type · escalation flag           │
│  Repeat issue detection                 │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│         AGENT 3: RESPONSE               │
│  Customer-facing answer                 │
│  Tone adjusted to severity + sentiment  │
└─────────────────────────────────────────┘
     ↓ (severity ≥ 4 only)
┌─────────────────────────────────────────┐
│         AGENT 4: SUPERVISOR             │
│  Action · compensation · team assignment│
│  Priority level · internal notes       │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│         AGENT 5: AUDIT                  │
│  Logs full ticket to Pinecone           │
│  Builds institutional memory            │
└─────────────────────────────────────────┘
     ↓
① Customer-facing answer
② Internal action plan
③ Audit ticket stored in Pinecone
```

---

## Key Design Decisions

| Decision | Option Chosen | Trade-off |
|---|---|---|
| What to embed? | Customer questions, not answers | Misses answer-content matches |
| Severity scoring | LLM-based (Gemini) | Non-deterministic across runs |
| Past case retrieval | Cosine similarity threshold 0.81 | May miss edge cases below threshold |
| Low severity queries | Early exit after Agent 3 | Agents 4 & 5 skipped (~40% faster) |

### Decision in Practice

**Problem:** Similarity threshold of 0.75 caused unrelated past cases to influence severity scoring.  
**Decision:** Raised threshold to 0.81 based on observed similarity score distribution.  
**Result:** Unrelated past cases no longer affect evaluation output. ✅

---

## Institutional Memory

Every resolved case is embedded and logged to Pinecone's `action-logs` namespace. Future queries retrieve semantically similar past cases — enabling the pipeline to detect repeat issues and inform supervisor decisions.

**Demo:**
- Query 1: *"I was charged twice for my order"* → Past cases: 0
- Query 2: *"There are two identical charges on my account"* → Past cases: 1 (similarity: 0.82) ✅

The two queries share zero keywords — retrieved purely through semantic similarity.

---

## Evaluation Framework

20 labeled test cases spanning all 5 severity levels, including boundary cases and conflicting signals (e.g. calm tone with serious issue).

| Metric | Result |
|---|---|
| Severity MAE | 0.0 (exact match on structured test set) |
| Escalation Recall | 100% (zero missed escalations) |
| Escalation Precision | 89% (1 over-escalation out of 9) |

> **Limitation:** Test cases were deliberately distinct across severity levels. Real-world performance would require stress testing on sarcastic queries, multilingual input, and vague complaints where intent is ambiguous.

---

## Performance

| Scenario | Agents Run | Latency |
|---|---|---|
| Severity 1–2 (routine) | Agents 1–3 (Early Exit) | ~17s |
| Severity 4–5 (escalated) | Agents 1–5 (Full Pipeline) | ~29s |

---

## Tech Stack

| Component | Tool |
|---|---|
| Vector Database | Pinecone (serverless, cosine similarity) |
| LLM | Gemini 2.5 Flash |
| Embeddings | Google text-embedding-004 (3072 dimensions) |
| Dataset | [Bitext Customer Support](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) (26,872 rows, 27 intents) |
| Environment | Google Colab (Python) |

---

## Production Roadmap

**P0 — Must Have Before Handoff**
- PII redaction before embedding
- Per-agent error handling and fallback
- REST API (FastAPI) for concurrent multi-tenant requests

**P1 — Recommended for Production**
- Ticketing system integration (Zendesk / Freshdesk)
- Human feedback loop to improve prompt quality over time
- Monitoring dashboard (escalation rate, latency, data drift)

**P2 — Scale Optimisation**
- Multilingual support (embed in target language)
- Hybrid search (vector + keyword)
- Replace LLM severity scorer with fine-tuned classifier

---

## Setup

### Prerequisites
- Google Colab account
- Pinecone API key (free tier sufficient)
- Gemini API key ([Google AI Studio](https://aistudio.google.com))

### Running the Notebook

1. Open `Customer Support Triage.ipynb` in Google Colab
2. Add API keys to Colab Secrets:
   - `PINECONE_API_KEY`
   - `GEMINI_API_KEY`
3. Run all cells sequentially from top to bottom
4. On subsequent sessions, use the **Quick Restart Cell** to restore session variables without re-embedding

### Re-running After Session Restart

Pinecone vectors persist across sessions. After a kernel restart, only run:
- Quick Restart Cell (restores all variables)
- Agent function definition cells
- Then call `run_pipeline()` directly

---

## Repository Structure

```
ai-powered-customer-support-triage/
│
├── README.md
├── requirements.txt
│
├── notebook/
│   └── Customer Support Triage.ipynb
│
├── docs/
│   ├── architecture.png
│   └── evaluation_results.png
│
├── deck/
│   └── Customer_Support_Triage.pdf
│
└── data/
    └── test_cases.py
```

---

## Known Limitations

- Single-turn only — no multi-turn conversation support
- Severity scoring is LLM-based and non-deterministic
- Escalation actions are recommendations only — not connected to real ticketing systems
- No PII redaction — not suitable for real customer data without this
- Dataset uses template placeholders (e.g. `{{Order Number}}`) not real customer data
- English-only — no multilingual support in current PoC

---

*Built as a Research PoC to demonstrate technical feasibility of multi-agent RAG systems for customer support triage.*
