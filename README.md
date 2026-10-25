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
| Tool specs and registered tools | In progress |
| Runtime validates tool calls before execution | In progress |
| Policy enforcement | Stub |
| Agent loop with a fake model | In progress |
| Context and state kept separate from tools | Not started |
| Ollama model adapter | Not started |
| HTTP API (FastAPI) | Not started |
| Logging and metrics | Not started |
| Automated tests | Not started |

## Roadmap

| # | Stage | Status |
|---|---|---|
| 1 | Typed data contracts | In progress |
| 2 | Tool specifications and registration | In progress |
| 3 | Runtime validation and tool execution | In progress |
| 4 | Fake model and minimal agent loop | In progress |
| 5 | Policy enforcement and bounded execution | Not started |
| 6 | Context growth, result filtering, state | Not started |
| 7 | Evaluation, observability, reliability, Ollama integration | Not started |
| 8 | Interoperability and frameworks (only when needed) | Not started |

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

There is no runnable entry point yet. It arrives in stage 7.

## Learning path

- Step-by-step phases for Task 1: [`.docs/task1/00-overview.md`](.docs/task1/00-overview.md)
- Full spec: [`.docs/Implementation_task_1.md`](.docs/Implementation_task_1.md)

## Known limitations

- Local use only. No authentication, TLS or rate limiting.
- The calculator is the only tool.
- A small local model sometimes picks the wrong tool or answers wrongly.
- No memory across requests and no streaming.
