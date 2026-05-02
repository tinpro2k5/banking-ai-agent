# Banking AI Agent

A FastAPI-based banking AI agent that processes customer requests using Ollama LLM and a multi-node processing pipeline.

## Project Structure

```
banking-ai-agent/
├── app/
│   ├── agent/
│   │   └── orchestrator.py       # Main orchestrator
│   ├── clients/
│   │   ├── base.py               # Base client interface
│   │   └── ollama_client.py       # Ollama LLM client
│   ├── core/
│   │   ├── schemas.py            # Pydantic request/response schemas
│   │   └── settings.py           # Application configuration
│   ├── data/
│   │   └── policies.py           # Banking policies and rules
│   └── nodes/
│       ├── intent_node.py        # Intent detection
│       ├── priority_node.py       # Priority assessment
│       ├── policy_node.py        # Policy validation
│       ├── draft_node.py         # Response generation
│       ├── validation_node.py    # Response validation
│       └── router_node.py        # Request routing
├── main.py                       # FastAPI app and routes
├── run.py                        # Entry point
├── examples/
│   └── sample_requests.json      # Sample banking requests
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
# Create .env file
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
DEBUG=False
```

3. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Welcome message
- `POST /process` - Process banking request
- `GET /health` - Health check

## Processing Pipeline

The agent uses a multi-node pipeline:

1. **Intent Node** - Detects user intent (transfer, balance check, etc.)
2. **Priority Node** - Assesses request priority
3. **Policy Node** - Validates against banking policies
4. **Draft Node** - Generates response
5. **Validation Node** - Validates response quality
6. **Router Node** - Routes to appropriate handler

## Example Usage

```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_text": "I want to transfer 5000 VND to my friend",
    "customer_id": "CUST001"
  }'
```

## Requirements

- Python 3.8+
- Ollama (for LLM inference)
- FastAPI
- Uvicorn
