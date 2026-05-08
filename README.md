# Banking AI Agent

> **Project 3 — Applications of Natural Language Processing in Industry**
> University of Science, VNU-HCM · Faculty of Information Technology

---

## Objective

This project implements a simple **AI agentic pipeline** for automated customer support in the banking domain. The system receives a customer message, detects the banking intent using a fine-tuned model (from Project 2), retrieves relevant policy information, drafts a response using Ollama, validates it, and decides whether to reply automatically or escalate to a human agent.

---

## System Architecture

### Node & Data-Flow Diagram

```mermaid
flowchart TD
    Client(["👤 Client\n(HTTP POST /chat)"])

    subgraph API["🌐 FastAPI  ·  main.py"]
        EP["@app.post('/chat')\nchat(request: CustomerRequest)\n→ orchestrator.run(message)"]
    end

    subgraph ORCH["🎛️ Orchestrator  ·  app/agent/orchestrator.py"]
        direction TB
        O["Orchestrator.run(message: str)\n→ AgentResponse\n\nFinal Reply Builder:\n action == 'escalate' → human-agent message\n action == 'ask_more'  → clarification prompt (uses missing_info when available)\n action == 'reply'     → draft_result.draft"]
    end

    subgraph INTENT["1️⃣ Intent Node  ·  app/nodes/intent_node.py"]
        IN["IntentNode.run(message)\n\nrequests.POST\n  {INTENT_API_URL}\n  body: {message}\n\nRemote service: Lab 2 fine-tuned classifier\nexposed from Colab via Pinggy\n\n→ IntentResult(intent, confidence)"]
    end

    subgraph PRIORITY["2️⃣ Priority Node  ·  app/nodes/priority_node.py"]
        PN["PriorityNode.run(message, intent)\n\nRule-based keyword matching:\n• HIGH  → fraud / stolen / blocked / hack …\n• MED   → failed / refund / wrong amount …\n• LOW   → everything else\n\n→ PriorityResult(level, reason)"]
    end

    subgraph POLICY["3️⃣ Policy Node  ·  app/nodes/policy_node.py"]
        POL["PolicyNode.run(intent)\n\nPOLICIES.get(intent, DEFAULT_POLICY)\n(dict lookup in app/data/policies.py)\n\n→ PolicyResult(policy_text)"]
    end

    subgraph DRAFT["4️⃣ Draft Node  ·  app/nodes/draft_node.py"]
        DR["DraftNode.run(message, intent, priority, policy)\n\nBuilds structured prompt:\n  'Customer: {message}'\n  'Intent: {intent}'\n  'Priority: {priority}'\n  'Policy: {policy}'\n\nclient.generate(prompt)\n\n→ DraftResult(draft, missing_info)"]
    end

    subgraph OLLAMA_CLIENT["⚙️ Ollama Client  ·  app/clients/ollama_client.py"]
        OC["OllamaClient.generate(prompt)\n\nrequests.POST\n  {OLLAMA_BASE_URL}/api/generate\n  body: {model, prompt, stream:false}\n\n→ response.json()['response']"]
    end

    subgraph OLLAMA_EXT["☁️ External LLM  (Google Colab + Pinggy)"]
        EXT["Ollama /api/generate\ngpt-oss:20b\nhttp://xxxx.a.free.pinggy.link"]
    end

    subgraph VALID["5️⃣ Validation Node  ·  app/nodes/validation_node.py"]
        VN["ValidationNode.run(draft, intent, confidence)\n\nChecks:\n• len(draft) >= 30\n• confidence >= 0.5\n• banking keywords present\n\n→ ValidationResult(valid, issues)"]
    end

    subgraph ROUTER["6️⃣ Router Node  ·  app/nodes/router_node.py"]
        RN["RouterNode.run(priority, valid, intent, confidence, missing_info)\n\nLogic:\n• priority=='high' OR not valid → 'escalate'\n• missing_info is set           → 'ask_more'\n• intent=='unknown_intent'      → 'ask_more'\n• confidence < 0.6              → 'ask_more'\n• else                          → 'reply'\n\n→ RouterResult(action, reason)"]
    end

    %% Final Reply Builder is implemented inside the Orchestrator (see ORCH node)

    Client --> EP
    EP --> O
    O -->|"message"| INTENT
    INTENT -->|"IntentResult\n(intent, confidence)"| PRIORITY
    INTENT -->|"intent"| POLICY
    INTENT -->|"intent + confidence"| DRAFT
    INTENT -->|"confidence"| VALID
    INTENT -->|"confidence"| ROUTER
    PRIORITY -->|"PriorityResult\n(level, reason)"| DRAFT
    PRIORITY -->|"level"| ROUTER
    POLICY -->|"PolicyResult\n(policy_text)"| DRAFT
    DRAFT -->|"DraftResult\n(draft)"| VALID
    DRAFT -->|"draft"| O
    VALID -->|"ValidationResult\n(valid, issues)"| ROUTER
    DR -->|"prompt"| OC
    OC -->|"HTTP POST /api/generate"| EXT
    EXT -->|"response text"| OC
    OC -->|"generated text"| DR
    ROUTER -->|"RouterResult\n(action, reason)"| O
    EP -->|"JSON 200"| Client
```

---

###  Call-Flow Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant API as FastAPI<br/>main.py
    participant Orch as Orchestrator<br/>orchestrator.py
    participant INode as IntentNode<br/>intent_node.py
    participant PNode as PriorityNode<br/>priority_node.py
    participant PolNode as PolicyNode<br/>policy_node.py
    participant DNode as DraftNode<br/>draft_node.py
    participant Ollama as OllamaClient<br/>→ Pinggy → gpt-oss:20b
    participant VNode as ValidationNode<br/>validation_node.py
    participant RNode as RouterNode<br/>router_node.py

    User->>API: POST /chat  {message}
    API->>Orch: orchestrator.run(message)

    Orch->>INode: intent_node.run(message)
    Note over INode: POST to INTENT_API_URL<br/>remote Lab 2 classifier
    INode-->>Orch: IntentResult(intent, confidence)

    Orch->>PNode: priority_node.run(message, intent)
    Note over PNode: keyword matching<br/>high / medium / low
    PNode-->>Orch: PriorityResult(level, reason)

    Orch->>PolNode: policy_node.run(intent)
    Note over PolNode: POLICIES.get(intent)
    PolNode-->>Orch: PolicyResult(policy_text)

    Orch->>DNode: draft_node.run(message, intent, priority, policy)
    DNode->>Ollama: POST /api/generate {model, prompt, stream:false}
    Ollama-->>DNode: {response: "..."}
    DNode-->>Orch: DraftResult(draft, missing_info)

    Orch->>VNode: validation_node.run(draft, intent, confidence)
    Note over VNode: len check, confidence<br/>check, keyword check
    VNode-->>Orch: ValidationResult(valid, issues)

    Orch->>RNode: router_node.run(priority, valid, intent, confidence, missing_info)
    Note over RNode: missing_info / escalate / ask_more / reply
    RNode-->>Orch: RouterResult(action, reason)

    Note over Orch: Build final_reply from action and missing_info
    Orch-->>API: AgentResponse (full trace + final_reply)
    API-->>User: HTTP 200 JSON
```

---

###  Module Dependency Map

```mermaid
graph LR
    subgraph Entry
        run["run.py\nuvicorn.run()"]
        main["main.py\nFastAPI app\nPOST /chat"]
    end

    subgraph Core
        schemas["core/schemas.py\nCustomerRequest\nIntentResult\nPriorityResult\nPolicyResult\nDraftResult\nValidationResult\nRouterResult\nAgentResponse"]
        settings["core/settings.py\nOLLAMA_BASE_URL\nOLLAMA_MODEL\nINTENT_API_URL"]
    end

    subgraph Data
        policies["data/policies.py\nPOLICIES dict\nDEFAULT_POLICY"]
    end

    subgraph Clients
        base["clients/base.py\nBaseLLMClient (ABC)\n.generate(prompt)"]
        ollama["clients/ollama_client.py\nOllamaClient\n.generate(prompt)"]
    end

    subgraph Nodes
        i["nodes/intent_node.py\nIntentNode"]
        p["nodes/priority_node.py\nPriorityNode"]
        pol["nodes/policy_node.py\nPolicyNode"]
        d["nodes/draft_node.py\nDraftNode"]
        v["nodes/validation_node.py\nValidationNode"]
        r["nodes/router_node.py\nRouterNode"]
    end

    subgraph Agent
        orch["agent/orchestrator.py\nOrchestrator\n.run()"]
    end

    run --> main
    main --> orch
    orch --> i & p & pol & d & v & r
    i --> schemas & settings
    p --> schemas
    pol --> schemas & policies
    d --> schemas & ollama
    v --> schemas
    r --> schemas
    ollama --> base & settings
    main --> schemas
```

---

## Node Reference

| # | Node | File | Method signature | Inputs | Output schema |
|---|------|------|-----------------|--------|---------------|
| 1 | **Intent** | `nodes/intent_node.py` | `IntentNode.run(message)` | raw text | `IntentResult(intent, confidence)` |
| 2 | **Priority** | `nodes/priority_node.py` | `PriorityNode.run(message, intent)` | text + intent label | `PriorityResult(level, reason)` |
| 3 | **Policy** | `nodes/policy_node.py` | `PolicyNode.run(intent)` | intent label | `PolicyResult(policy_text)` |
| 4 | **Draft** | `nodes/draft_node.py` | `DraftNode.run(message, intent, priority, policy)` | text + intent + level + policy | `DraftResult(draft, missing_info)` |
| 5 | **Validation** | `nodes/validation_node.py` | `ValidationNode.run(draft, intent, confidence)` | draft text + confidence | `ValidationResult(valid, issues)` |
| 6 | **Router** | `nodes/router_node.py` | `RouterNode.run(priority, valid, intent, confidence, missing_info)` | level + bool + intent + confidence + draft hints | `RouterResult(action, reason)` |

### Router decision logic

```
priority == "high"  OR  valid == False  →  action = "escalate"
missing_info is not None                 →  action = "ask_more"
intent == "unknown_intent"               →  action = "ask_more"
confidence < 0.6                          →  action = "ask_more"
otherwise                                 →  action = "reply"
```

---

## Project Structure

```
banking-ai-agent/
├── app/
│   ├── main.py                       # FastAPI app  (POST /chat, GET /health)
│   ├── agent/
│   │   └── orchestrator.py           # Main pipeline controller (Orchestrator.run)
│   ├── clients/
│   │   ├── base.py                   # Abstract LLM client (BaseLLMClient)
│   │   └── ollama_client.py          # Ollama HTTP client (OllamaClient.generate)
│   ├── core/
│   │   ├── schemas.py                # Pydantic I/O schemas for all nodes
│   │   └── settings.py               # OLLAMA_BASE_URL, OLLAMA_MODEL, INTENT_API_URL
│   ├── data/
│   │   └── policies.py               # BankingPolicies class + POLICIES dict + DEFAULT_POLICY
│   └── nodes/
│       ├── intent_node.py            # IntentNode  — remote Lab 2 classifier API
│       ├── priority_node.py          # PriorityNode — keyword rule engine
│       ├── policy_node.py            # PolicyNode  — delegates to BankingPolicies
│       ├── draft_node.py             # DraftNode   — Ollama prompt + generate
│       ├── validation_node.py        # ValidationNode — rule checks
│       └── router_node.py            # RouterNode  — escalation logic
├── examples/
│   └── sample_requests.json          # Test cases
├── run.py                            # Entry point  (uvicorn → app.main:app, port 6636)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/banking-ai-agent.git
cd banking-ai-agent
```

### 2. Create a virtual environment and install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama and the intent classifier on Google Colab

Open `Ollama-Pinggy.ipynb` in Google Colab and run the Ollama cells plus the Lab 2 intent classifier cells. The notebook starts two local services:

| Service | Local port | Purpose |
|---------|------------|---------|
| Ollama | `11434` | Draft response generation with `gpt-oss:20b` |
| Intent classifier | `8000` | Lab 2 fine-tuned intent prediction at `/predict` |

### 4. Expose both services with Pinggy

Create one Pinggy tunnel for Ollama and a second Pinggy tunnel for the intent classifier:

```bash
ssh -p 443 -R0:localhost:11434 qr@a.pinggy.io
ssh -p 443 -R0:localhost:8000 qr@a.pinggy.io
```

Copy both generated public URLs into `app/core/settings.py`. The app reads them through the `Settings` class, so these defaults can also be overridden from a local `.env` file.

```python
OLLAMA_BASE_URL = "http://xxxx.a.free.pinggy.link"
OLLAMA_MODEL    = "gpt-oss:20b"
INTENT_API_URL  = "http://yyyy.a.free.pinggy.link/predict"
```

Optional `.env` override:

```bash
OLLAMA_BASE_URL=http://xxxx.a.free.pinggy.link
OLLAMA_MODEL=gpt-oss:20b
INTENT_API_URL=http://yyyy.a.free.pinggy.link/predict
```

### 5. Run the server

```bash
python run.py
```

Server starts at `http://localhost:6636` — interactive docs at `http://localhost:6636/docs`.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat` | Process a customer message, returns full pipeline trace + final reply |
| `GET` | `/health` | Health check |

### Example request

```bash
curl -X POST http://localhost:6636/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I made a transfer 3 days ago but the recipient has not received the money."}'
```

### Sample requests

See [`examples/sample_requests.json`](examples/sample_requests.json) for test cases covering:

| Message | Detected intent | Priority | Routing |
|---------|----------------|----------|---------|
| Transfer with TXN/date provided | `transfer_not_received_by_recipient` | `low` | `ask_more` |
| Card blocked after OTP check | `declined_card_payment` | `high` | `escalate` |
| Unauthorized card payment with amount/reference | `card_payment_not_recognised` | `high` | `escalate` |
| Refund with order/return date provided | `Refund_not_showing_up` | `medium` | `reply` |
| Balance question in app | `balance_not_updated_after_bank_transfer` | `low` | `reply` |
| Unclear beeping issue | `unknown_intent` | `low` | `ask_more` |

---

## Testing & Demo Results

### Routing Outcomes

The system successfully demonstrates all three routing decisions:

#### 1. Auto-Reply
- **Case:** "I returned the product on 2026-05-02 and my refund for order 771245 still has not shown up in my account."
- **Intent detected:** `Refund_not_showing_up`
- **Priority:** `medium` → **Action:** `reply`
- **Output:** returns the drafted banking response as the final reply

- **Case:** "How do I check my account balance in the mobile app?"
- **Intent detected:** `balance_not_updated_after_bank_transfer`
- **Priority:** `low` → **Action:** `reply`

#### 2. Escalation
- **Case:** "My card was blocked after an OTP check, and I need help reactivating it to make a payment today."
- **Intent detected:** `declined_card_payment`
- **Priority:** `high` → **Action:** `escalate`

- **Case:** "Someone made an unauthorized card payment of $79.40 on my account ending 4432 yesterday."
- **Intent detected:** `card_payment_not_recognised`
- **Priority:** `high` → **Action:** `escalate`

#### 3. Ask More
- **Case:** "I made transfer TXN-48291 on 2026-05-05 for $250 to account 009182, but the recipient still has not received it."
- **Intent detected:** `transfer_not_received_by_recipient`
- **Priority:** `low` → **Action:** `ask_more`
- **Final reply:** asks for the specific missing details extracted from the draft

- **Case:** "My grandmother's debit card was linked to the app, but the card link keeps failing with an error code."
- **Intent detected:** `unknown_intent`
- **Priority:** `low` → **Action:** `ask_more`

All responses include the complete pipeline trace: `intent`, `priority`, `policy`, `draft`, `validation`, `routing`, and `final_reply`.

---

## Video Demo

**Demo URL:** [Insert your video link here]

### Recording Checklist

- [ ] Start the notebook on Kaggle,, explain that it runs both Ollama and Intent classifier and must use Kaggle 2T4 GPU for sufficient VRAM
- [ ] Start the server: `python run.py`
- [ ] Open Swagger UI at `http://localhost:6636/docs`
- [ ] Send 3–5 sample messages from `examples/sample_requests.json`
- [ ] Show the full JSON response for at least one auto-reply case
- [ ] Show an escalation case and its response
- [ ] Show the three routing decisions (reply, escalate, ask_more)
- [ ] Walk through one complete node trace (intent → priority → policy → draft → validation → routing)
**Video should cover:** System overview, architecture, sample inputs/outputs, and the three routing outcomes. Could show the Readme file

---

## Authors

| Student ID | Full Name |
|-----------|-----------|
| 23120371 | Lê Trung Tín |
