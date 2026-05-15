# Architecture

## Overview

Evidence Ranking Engine is a Python and FastAPI service for ranking decision-support evidence before it becomes briefing-safe advice. The goal is not generic search or retrieval. The goal is to keep evidence quality visible when an operator, analyst, or model needs to decide which packet should anchor a recommendation.

## Core surfaces

- `Overview`
  - summarizes evidence count, contested lanes, freshness watch, and average trust posture
- `Evidence Board`
  - shows the highest-priority evidence packets with trust, contradiction, and citation context
- `Conflicts`
  - exposes packets where contradiction pressure or age should block confident reuse
- `Owners`
  - groups evidence stewardship by owner lane so teams can see where refresh work belongs
- `Docs`
  - publishes the route surface and a sample ranking payload

## Ranking model

Each evidence packet carries:

- trust score
- confidence
- freshness days
- citation count
- contradiction count
- supporting sources
- stewardship owner

The ranking score blends those into one operator-facing value:

- trust score provides the base posture
- fresh evidence gets a bonus
- citation depth increases confidence in reuse
- contradiction pressure subtracts from the final rank
- confidence acts as a bounded supporting signal, not the only truth

This is deliberately simple enough to audit. The repo is about making the tradeoffs visible, not hiding them behind an opaque model.

## API design

The API favors small, legible routes:

- `GET /api/evidence`
- `GET /api/conflicts`
- `GET /api/owners`
- `POST /api/analyze/rank`

That keeps the repo easy to demo, test, and extend into a larger decision-intelligence stack later.

## Proof layer

`app/render.py` generates the real HTML proof surfaces used for screenshots. `scripts/render_readme_assets.py` renders those routes into PNG assets so the README reflects the actual application instead of mock images.
