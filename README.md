# mini-agent

A small LLM agent runtime, written by hand in Python. The goal is to learn how agents work (tool calls, validation, the loop, policy) and to build backend engineering skills along the way.

## Architecture

```
HTTP client -> FastAPI -> Agent loop <-> LLM (Ollama)
                              |
                              +-> Policy -> Runtime -> Tool registry -> Calculator
```

The model only proposes a decision. Everything else (validation, permissions, execution, limits) is plain code.

## Status

| Check | Status |
|---|---|
| Typed data contracts | Done |
| Tool specs and registered tools | Done |
| Runtime validates tool calls before execution | Done |
| Model output protocol (decision parsing) | Done |
| Ollama model adapter (structured output via JSON schema) | Done |
| Policy enforcement | Not started (next) |
| Agent loop | Not started |
| Context and state kept separate from tools | Not started |
| HTTP API (FastAPI) | Not started |
| Logging and metrics | Not started |
| Automated tests | Not started |

## Roadmap

| # | Stage | Status |
|---|---|---|
| 1 | Typed data contracts | Done |
| 2 | Tool specifications and registration | Done |
| 3 | Runtime validation and tool execution | Done |
| 4 | Model output protocol | Done |
| 5 | Ollama model adapter | Done |
| 6 | Policy enforcement and minimal agent loop | Next |
| 7 | Bounded execution, context and state | Not started |
| 8 | Evaluation, observability, reliability, HTTP API | Not started |
| 9 | Interoperability and frameworks (only when needed) | Not started |

## Concepts you will learn

- **Agent loop and bounded execution:** [`src/mini_agent/agent/`](src/mini_agent/agent/)
- **Typed contracts and runtime validation:** [`src/mini_agent/domain/`](src/mini_agent/domain/), [`src/mini_agent/runtime/`](src/mini_agent/runtime/)
- **Tool design and permissions:** [`src/mini_agent/tools/`](src/mini_agent/tools/), [`src/mini_agent/policy/`](src/mini_agent/policy/)
- **Model adapter and structured output:** [`src/mini_agent/llm/`](src/mini_agent/llm/)
- **Testing with fakes, no paid APIs:** [`script/`](script/) now, `tests/` later

## Engineering standards

The full list is in [AGENTS.md](AGENTS.md). The headlines:

- Treat model output as untrusted. Validate tool name, arguments and permission before running anything.
- Keep layers separate: orchestration, policy, tools and model adapter do not reach into each other.
- Use Pydantic at boundaries (model output, HTTP, settings). Use plain dataclasses inside.
- Handle expected failures explicitly. Do not hide bugs behind a broad `except Exception`.
- Bound execution: iteration limits, timeouts and output sizes.
- Keep secrets and tracebacks out of model context and API responses.
- Test behaviour with deterministic fakes. The core tests do not need a model or network.
- Start with the standard library. Add a dependency only when it clearly helps.

## How AI is used in this project

- **In the agent:** the LLM decides the next step (answer or call a tool) and writes the final answer. Nothing else is delegated to it.
- **In development:** the code is written by hand. AI assistance is limited to reviewing code, checking best practice, and low-effort work such as formatting, comments and log messages.

## Prerequisites

- Windows, Python 3.14+, [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/) with the `qwen3:4b` model

```powershell
ollama pull qwen3:4b
uv sync
```

There is no runnable entry point yet. It arrives in stage 8. Until then, the check scripts in `script/` run the pieces by hand.

## Known limitations

- Local use only. No authentication, TLS or rate limiting.
- The calculator is the only tool.
- A small local model sometimes picks the wrong tool or answers wrongly.
- Rejected model output can echo the rejected value in its error text. This must be fixed before the HTTP API is exposed.
- The Ollama client is not yet hardened: `is_ready` can still raise on an unexpected response, and DEBUG logs contain prompts and raw responses.
- No memory across requests and no streaming.
