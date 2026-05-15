# Changelog

## 1.0.0 - 2026-05-15

- packaged the public Evidence Ranking Engine repo
- shipped FastAPI routes, HTML proof surfaces, screenshots, docs, and CI
- added evidence packet ranking across trust, freshness, citation depth, and contradiction pressure
- exposed owner lanes and conflict review surfaces for operator use

## 0.1.0 - 2026-02-19

- stabilized the first working scoring model for evidence packets
- added contradiction-aware review ordering for high-risk domains
- tightened the operator API around ranking and conflict inspection

## Prototype - 2025-08-08

- tested a simple evidence packet format against governance, fraud, and platform cases
- proved that trust and freshness signals were more useful when surfaced together

## Design Phase - 2024-11-14

- mapped how evidence quality was getting lost between retrieval, analytics, and recommendation layers
- defined a minimal scoring model that stayed explainable for operators

## Idea Origin - 2023-07-03

- observed that recommendation systems often treated “retrieved” evidence as “decision-safe” evidence
- outlined a dedicated ranking layer to close that trust gap

## Background Signals - 2022-09-21

- growing pressure around RAG hallucination rates, weak citation chains, and OWASP LLM Top 10 style evidence failures
- more enterprise workflows beginning to depend on model-assisted synthesis without equivalent evidence governance
