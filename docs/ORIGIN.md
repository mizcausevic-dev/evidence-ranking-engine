# Why We Built This

Enterprise teams talk a lot about “better evidence,” but most decision systems still flatten every citation into the same shape. A stale export, a high-quality telemetry trace, a manual review note, and a contradictory board packet all tend to arrive in one pile. Then a human or model is expected to infer which evidence deserves trust and which one is simply present.

That gap gets worse when retrieval and summarization layers become faster. The faster a system can retrieve evidence, the easier it becomes to carry weak or outdated support into confident language. At scale, the problem is not lack of information. The problem is that trust, freshness, contradiction pressure, and stewardship are rarely visible in the same place.

We built Evidence Ranking Engine to make that posture explicit.

The design starts from a simple premise: evidence should earn its place in a recommendation. That means ranking evidence packets by more than relevance alone. Trust score, freshness, citation depth, contradiction count, and owner stewardship all matter because they shape whether a packet is actually safe to carry into a release gate, executive memo, compliance review, or operating recommendation.

Existing tools usually miss the mark in one of three ways:

- they optimize for retrieval but not evidence quality
- they optimize for analytics but not contradiction review
- they optimize for audit storage but not operator usability

This repo aims at the intersection instead. The interface is operator-first, the logic is straightforward enough to audit, and the route surface is small enough to fit naturally into a CI-native decision stack.

What comes next is obvious: richer evidence provenance, domain-specific weighting, and tighter integration with MCP policy, warehouse contracts, fraud telemetry, and governance review lanes. But the foundation has to be right first. If the evidence board cannot show why one packet rose and another fell, the rest of the intelligence stack is standing on fog.
