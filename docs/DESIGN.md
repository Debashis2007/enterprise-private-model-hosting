# Design: Enterprise Private Model Hosting

**Project:** `enterprise-private-model-hosting`  
**Parent system design:** `01-llm-inference-serving.md`

## 1. What this POC demonstrates

Dedicated pool semantics: pinned revision, region residency, ZDR-style flags.

## 2. Architecture (POC)

```text
Client → region allowlist → pinned revision MockLLM → private response metadata
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Pinned revision | Enterprises forbid surprise model swaps. | Constant `PINNED` revision id. |
| Residency gate | Data must not leave contracted regions. | `ALLOWED_REGIONS` check. |
| Dedicated pool flag | Signals isolation from public multi-tenant fleet. | Response `pool=dedicated`. |

## 4. Key endpoints

`GET /health`, `POST /infer`

## 5. Tradeoffs / POC limits

No real VPC/private-link — residency is a logical gate for the POC.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

