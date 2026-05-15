from __future__ import annotations

import json
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import (
    render_conflicts,
    render_docs,
    render_evidence_board,
    render_overview,
    render_owners,
)
from app.services.evidence_ranking_service import EvidenceRankingService

app = FastAPI(
    title="Evidence Ranking Engine",
    version="0.1.0",
    description=(
        "Decision-intelligence service for ranking evidence packets by trust, "
        "freshness, citation density, and contradiction pressure."
    ),
)


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/evidence-board", response_class=HTMLResponse)
def evidence_board() -> str:
    return render_evidence_board()


@app.get("/conflicts", response_class=HTMLResponse)
def conflicts() -> str:
    return render_conflicts()


@app.get("/owners", response_class=HTMLResponse)
def owners() -> str:
    return render_owners()


@app.get("/docs", response_class=HTMLResponse)
def docs() -> str:
    return render_docs()


@app.get("/api/dashboard/summary")
def api_summary() -> dict:
    return EvidenceRankingService.summary()


@app.get("/api/evidence")
def api_evidence() -> list[dict]:
    return EvidenceRankingService.evidence_packets()


@app.get("/api/evidence/{evidence_id}")
def api_evidence_packet(evidence_id: str) -> dict:
    packet = EvidenceRankingService.evidence_by_id(evidence_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Evidence packet not found")
    return packet


@app.get("/api/conflicts")
def api_conflicts() -> list[dict]:
    return EvidenceRankingService.conflicts()


@app.get("/api/owners")
def api_owners() -> list[dict]:
    return EvidenceRankingService.owner_lanes()


@app.get("/api/sample")
def api_sample() -> dict:
    return EvidenceRankingService.sample_evidence()


@app.post("/api/analyze/rank")
def api_rank(payload: dict) -> dict:
    return EvidenceRankingService.evaluate(payload)


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5026"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
