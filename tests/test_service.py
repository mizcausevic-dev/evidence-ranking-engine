from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.evidence_ranking_service import EvidenceRankingService


class EvidenceRankingEngineTests(unittest.TestCase):
    def test_summary_shape(self) -> None:
        summary = EvidenceRankingService.summary()
        self.assertEqual(summary["evidenceCount"], 6)
        self.assertIn("leadRecommendation", summary)

    def test_contested_packets_are_returned(self) -> None:
        conflicts = EvidenceRankingService.conflicts()
        self.assertGreaterEqual(len(conflicts), 2)
        self.assertGreater(conflicts[0]["reviewPressure"], 0)

    def test_rank_api(self) -> None:
        client = TestClient(app)
        response = client.post(
            "/api/analyze/rank",
            json={
                "prompt": "Need fraud evidence for LATAM payment release",
                "freshness_budget_days": 10,
                "minimum_trust_score": 80,
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn(body["status"], {"ready", "watch", "contested"})
        self.assertIn("topEvidence", body)


if __name__ == "__main__":
    unittest.main()
