# Use Case: Enterprise Private Model Hosting

**Author fingerprint:** `DBHATT-Debashis2007-SystemDesignPOC-2026` — Debashis Bhattacharjee ([@Debashis2007](https://github.com/Debashis2007))

**YouTube walkthrough:** [Enterprise Private Model Hosting — System Design #Shorts](https://youtu.be/HTAHED5x_sw)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [01 — LLM Inference Serving](./01-llm-inference-serving.md)

## Users & problem

Enterprises need a dedicated or strongly isolated model fleet (data residency, custom fine-tune, stricter SLOs) rather than shared multi-tenant capacity.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Isolation | Dedicated pool or single-tenant cell |
| Residency | Region-pinned inference + logs |
| Availability | 99.95% (contractual) |
| Change control | Pinned revisions; scheduled upgrades |
| Data handling | ZDR / no training on prompts (policy) |

## Design (from parent)

```
Enterprise edge (private link / VPC) → Dedicated gateway
  → Dedicated router + quotas
  → Isolated GPU pool (no shared KV with public)
  → Private logging sink (residency-compliant)
```

Reuse parent: continuous batching, KV management, canaries—but **do not share workers or prefix caches** with the public fleet.

## Specializations

| vs public SaaS | Enterprise choice |
|----------------|-------------------|
| Pools | Dedicated replicas; optional customer-managed keys |
| Networking | Private connectivity; no shared egress path |
| Ops | Per-tenant runbooks, maintenance windows |
| Safety | Enterprise policy packs ([06](./06-safety-moderation-pipeline.md)) |

## Failure modes

- Capacity cliff on traffic spike → burst into reserved overflow pool, never public shared.
- Residency breach via logging → region-local audit only; block cross-region replicate.
- Upgrade surprise → pins + explicit promote; no silent `latest`.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Enterprise Private Model Hosting — System Design #Shorts](https://youtu.be/HTAHED5x_sw)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd enterprise-private-model-hosting
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/infer -H 'Content-Type: application/json' -d '{"prompt":"hi","region":"us-east"}' | jq

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

