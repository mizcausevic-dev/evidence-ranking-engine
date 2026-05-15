from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.evidence_ranking_service import EvidenceRankingService


def main() -> None:
    payload = {
        "dashboard": EvidenceRankingService.summary(),
        "topEvidence": EvidenceRankingService.sample_evidence(),
        "sampleRank": EvidenceRankingService.evaluate(
            {
                "prompt": "Need access governance evidence for privileged review packet",
                "freshness_budget_days": 12,
                "minimum_trust_score": 72,
            }
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
