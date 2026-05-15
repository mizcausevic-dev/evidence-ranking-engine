from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from app.data.sample_evidence_data import SAMPLE_DATA


class EvidenceRankingService:
    @staticmethod
    def summary() -> dict[str, Any]:
        return SAMPLE_DATA["dashboard"]

    @staticmethod
    def evidence_packets() -> list[dict[str, Any]]:
        return sorted(
            (
                {
                    **packet,
                    "rankScore": EvidenceRankingService._rank_score(packet),
                }
                for packet in SAMPLE_DATA["evidence"]
            ),
            key=lambda packet: (
                EvidenceRankingService._status_order(packet["status"]),
                -packet["rankScore"],
                packet["freshnessDays"],
            ),
        )

    @staticmethod
    def evidence_by_id(evidence_id: str) -> dict[str, Any] | None:
        return next(
            (
                packet
                for packet in EvidenceRankingService.evidence_packets()
                if packet["id"] == evidence_id
            ),
            None,
        )

    @staticmethod
    def conflicts() -> list[dict[str, Any]]:
        packets = [packet for packet in EvidenceRankingService.evidence_packets() if packet["contradictionCount"] > 0]
        conflicts = []
        for packet in packets:
            conflicts.append(
                {
                    "id": packet["id"],
                    "title": packet["title"],
                    "domain": packet["domain"],
                    "owner": packet["owner"],
                    "status": packet["status"],
                    "contradictionCount": packet["contradictionCount"],
                    "freshnessDays": packet["freshnessDays"],
                    "rankScore": packet["rankScore"],
                    "reviewPressure": round(
                        (packet["contradictionCount"] * 9) + max(packet["freshnessDays"] - 10, 0) * 1.6,
                        1,
                    ),
                }
            )
        return sorted(conflicts, key=lambda item: (-item["reviewPressure"], item["freshnessDays"]))

    @staticmethod
    def owner_lanes() -> list[dict[str, Any]]:
        lanes = []
        for owner in sorted({packet["owner"] for packet in SAMPLE_DATA["evidence"]}):
            owned = [packet for packet in EvidenceRankingService.evidence_packets() if packet["owner"] == owner]
            lanes.append(
                {
                    "owner": owner,
                    "evidenceCount": len(owned),
                    "contestedCount": len([packet for packet in owned if packet["status"] == "contested"]),
                    "averageTrustScore": round(mean(packet["trustScore"] for packet in owned), 1),
                    "focusPacket": max(
                        owned,
                        key=lambda packet: (
                            EvidenceRankingService._status_order(packet["status"]) == 0,
                            packet["contradictionCount"],
                            packet["freshnessDays"],
                        ),
                    )["title"],
                    "domains": sorted({packet["domain"] for packet in owned}),
                }
            )
        return lanes

    @staticmethod
    def sample_evidence() -> dict[str, Any]:
        return EvidenceRankingService.evidence_packets()[0]

    @staticmethod
    def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
        prompt = str(payload.get("prompt", "")).lower()
        freshness_budget = int(payload.get("freshness_budget_days", 14))
        minimum_trust_score = int(payload.get("minimum_trust_score", 75))
        domain_hits = Counter()
        ranked = []

        for packet in EvidenceRankingService.evidence_packets():
            keyword_hits = sum(
                1
                for token in (
                    packet["domain"].split()
                    + packet["title"].lower().split()
                    + packet["claim"].lower().split()
                    + [source.lower() for source in packet["supportingSources"]]
                )
                if token in prompt
            )
            freshness_penalty = max(packet["freshnessDays"] - freshness_budget, 0) * 1.8
            trust_delta = (packet["trustScore"] - minimum_trust_score) * 0.7
            contradiction_penalty = packet["contradictionCount"] * 6
            citation_bonus = packet["citationCount"] * 1.9
            score = (keyword_hits * 7) + trust_delta + citation_bonus - freshness_penalty - contradiction_penalty
            ranked.append(
                {
                    "id": packet["id"],
                    "title": packet["title"],
                    "domain": packet["domain"],
                    "status": packet["status"],
                    "score": round(score, 1),
                    "keywordHits": keyword_hits,
                    "trustScore": packet["trustScore"],
                    "freshnessDays": packet["freshnessDays"],
                    "contradictionCount": packet["contradictionCount"],
                }
            )
            domain_hits[packet["domain"]] += keyword_hits

        ranked.sort(key=lambda item: (-item["score"], item["contradictionCount"], item["freshnessDays"]))
        top = ranked[0]
        top_packet = EvidenceRankingService.evidence_by_id(top["id"])
        posture = "contested"
        if top["score"] >= 28 and top["contradictionCount"] == 0:
            posture = "ready"
        elif top["score"] >= 18 and top["trustScore"] >= minimum_trust_score:
            posture = "watch"

        return {
            "status": posture,
            "topEvidence": top,
            "dominantDomain": domain_hits.most_common(1)[0][0] if domain_hits else "unknown",
            "nextAction": {
                "ready": "Use the top evidence packet as the lead citation chain and keep the supporting sources attached to the decision note.",
                "watch": "Carry the evidence forward carefully, but refresh the packet before it becomes the sole basis for a recommendation.",
                "contested": "The evidence packet is too conflicted or stale. Re-rank the domain before turning it into a confident recommendation.",
            }[posture],
            "recommendedAction": top_packet["recommendedAction"] if top_packet else "",
            "supportingSources": top_packet["supportingSources"] if top_packet else [],
            "rankedEvidence": ranked,
        }

    @staticmethod
    def _rank_score(packet: dict[str, Any]) -> float:
        freshness_bonus = max(30 - packet["freshnessDays"], 0) * 0.8
        citation_bonus = packet["citationCount"] * 2.5
        contradiction_penalty = packet["contradictionCount"] * 7
        confidence_bonus = packet["confidence"] * 18
        return round(packet["trustScore"] + freshness_bonus + citation_bonus + confidence_bonus - contradiction_penalty, 1)

    @staticmethod
    def _status_order(status: str) -> int:
        return {"contested": 0, "watch": 1, "ready": 2}.get(status, 9)
