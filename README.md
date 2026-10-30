# Multi-Agent Enterprise Customer Helpdesk

An enterprise multi-agent customer support system built with DeepAgents, LangChain, LangGraph, LangSmith, and ChromaDB. It features supervisor orchestration, domain-specialized subagents, RAG over PDF technical manuals, SQL database tools, and policy guardrails with Human-in-the-Loop (HITL) escalation.

<p align="center">
  <img src="static/Agent.png" alt="Multi-Agent Helpdesk Architecture" />
</p>

---

## Table of Contents

- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [RAG Pipeline](#rag-pipeline)
- [Tools and Guardrails](#tools-and-guardrails)
- [Database Schema](#database-schema)
- [LangSmith Tracing & Observability](#langsmith-tracing--observability)
- [Example Queries](#example-queries)

---

## Technology Stack

- **DeepAgents**: Multi-agent orchestration and subagent routing.
- **LangChain**: Tool definitions (`@tool`), PDF parsing, and text splitting.
- **LangGraph**: Agent state graph coordination and thread memory (`MemorySaver`).
- **LangSmith**: Execution tracing and observability.
- **ChromaDB**: Persistent vector database for RAG embeddings.
- **SQLite / SQLAlchemy**: Relational order database and ORM operations.

---

## System Architecture

Incoming customer requests enter a root **Customer Support Orchestrator** that classifies intent and delegates execution to a specialized subagent.

<p align="center">
  <img src="static/SupportAgent.drawio.svg" alt="Multi-Agent Helpdesk Architecture" />
</p>

### Routing Logic

- **Order Operations (`order-ops`)**: Order status queries, cancellations, and refund requests.
- **Product Specialist (`product-specialist`)**: Hardware troubleshooting, error codes, and specs using RAG over product manuals.
- **General Support (`general-support`)**: Account questions, FAQ, navigation, and customer satisfaction discounts.

---

## RAG Pipeline

Technical support answers are strictly grounded in product PDF manuals to prevent hallucinations.

<p align="center">
  <img src="static/rag_pipeline.drawio.svg" alt="RAG Pipeline" />
</p>

---

## Tools and Guardrails

Below is the deterministic policy evaluation flowchart for automated cancellations and refunds:

<p align="center">
  <img src="static/tools_and_guardrails.drawio.svg" alt="Policy Guardrail Flow" />
</p>

### Tool Reference

| Tool | Subagent | Data Store | Function |
| :--- | :--- | :--- | :--- |
| `retrieve_manual_info` | `product-specialist` | ChromaDB | Semantic search (`k=3`) across embedded PDF manuals. |
| `get_order_status` | `order-ops` | SQLite | Returns order state (`Shipped`, `Pending`, `Cancelled`, `Refunded`). |
| `cancel_order` | `order-ops` | SQLite | Updates order status to `Cancelled`. |
| `process_refund` | `order-ops` | SQLite | Updates order status to `Refunded`. |
| `check_refund_eligibility` | `order-ops` | SQLite | Evaluates return window and price guardrails. |

---

## Database Schema

Relational data stored in SQLite (`orders.db`) managed via SQLAlchemy models in `database/models.py`.

<p align="center">
  <img src="static/database_schema.drawio.svg" alt="Database Schema" />
</p>

---

## LangSmith Tracing & Observability

Execution tracing, subagent delegations, tool calls, and LLM metrics are captured via **LangSmith** under the `Agentic-Helpdesk` project.

<p align="center">
  <img src="static/LangSmith Setup.png" alt="LangSmith Tracing and Observability" />
</p>

---

## Example Queries

### 1. RAG Technical Troubleshooting

<p align="center">
  <img src="static/RAG Technical Troubleshooting.png" alt="RAG Technical Troubleshooting" />
</p>

### 2. Automated Cancellation (Eligible)

<p align="center">
  <img src="static/Automated Cancellation (Eligible).png" alt="Automated Cancellation (Eligible)" />
</p>

### 3. Human Escalation

<p align="center">
  <img src="static/Human Escalation.png" alt="Human Escalation" />
</p>

### 4. General Support & Appeasement

<p align="center">
  <img src="static/General Support & Appeasement.png" alt="General Support & Appeasement" />
</p>
