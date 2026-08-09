"""Enterprise Private Model Hosting — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Enterprise Private Model Hosting"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(USE_CASE)


PINNED = "enterprise-r2026.04.01"
ALLOWED_REGIONS = {"us-east", "eu-west"}

class InferIn(BaseModel):
    prompt: str
    region: str = "us-east"

@app.post("/infer")
async def infer(body: InferIn):
    if body.region not in ALLOWED_REGIONS:
        raise HTTPException(400, detail="residency violation")
    llm.model = PINNED
    text = await llm.complete(body.prompt)
    return {"pool": "dedicated", "revision": PINNED, "region": body.region, "text": text, "zdr": True}
