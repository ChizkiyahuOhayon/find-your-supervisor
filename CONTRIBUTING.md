# Contributing

Welcome! We need better scholarly identity resolution, source fidelity, research evaluation, interoperability and reproducibility—not more unsupported "I read everything" claims.

## Contribution rules

1. Discuss changes in an issue or send a focused PR; attach tests for behavioral changes.
2. Keep the core Python standard-library-only and compatible with Python 3.9+.
3. Add real retrieval only behind explicit user opt-in, with timeouts/rate limiting, provenance and privacy safeguards.
4. Never vendor third-party licensed content, private researcher profiles, downloaded full papers or model weights.
5. Store only synthetic data under `examples/` and `tests/`. Label all sample measurements synthetic.
6. Every new "verified" stage needs a precise proof obligation. Passing a validator does not certify scientific truth.
7. Ensure English and Chinese usage documentation remain consistent for new capabilities.

Run before opening a PR:

```bash
python scripts/check_skill.py
python -m unittest discover -s tests -v
python scripts/claim_graph.py validate assets/claim-graph.example.json
```

Contributors retain rights to their own contributions and submit original material under this repository's MIT license.