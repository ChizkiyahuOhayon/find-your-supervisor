# Five-minute tour (synthetic data only)

This guide demonstrates the CLI mechanics; it **does not** constitute a full-paper read or research replication.

```bash
python scripts/check_skill.py
python scripts/claim_graph.py validate assets/claim-graph.example.json
python scripts/supervisor.py init --name "Example Scholar" --slug example-scholar --workspace ../my-mentors
python scripts/supervisor.py import-csv ../my-mentors/example-scholar/researcher.json examples/synthetic-publications.csv --source-name sample
python scripts/supervisor.py status ../my-mentors/example-scholar/researcher.json
python scripts/supervisor.py next ../my-mentors/example-scholar/researcher.json
python scripts/adapters.py list
python -m unittest discover -s tests -v
```

Expected result: duplicate bibliography candidates are merged; paper and code review remain incomplete; `next` identifies evidence-gathering work; the generated-mentor gate blocks unverified identity or missing page notes.

For a real researcher, replace the sample with your own cross-checked bibliography and use exact PDF page references, commit hashes and experiment logs.

Do not put unpublished data or scholar-specific notes into this public Git repository.
