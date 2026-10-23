# Release checklist

- [ ] Standalone repository tree, not nested in a different project's skill directory
- [ ] SKILL.md frontmatter and relative links validated
- [ ] README.md and docs/README.zh-CN.md describe honest capabilities
- [ ] License and ATTRIBUTION.md included; third-party source text/code is not copied
- [ ] No credentials, private scholar dossiers, unpublished student ideas, or copyrighted paper PDFs
- [ ] `python scripts/check_skill.py` passes
- [ ] `python scripts/claim_graph.py validate assets/claim-graph.example.json` passes
- [ ] `python -m unittest discover -s tests -v` passes
- [ ] GitHub Actions green on the published commit (local tests do not prove this)
- [ ] Document versions, caveats, observed limitations and reproducibility evidence

Do not claim the system automatically read or reproduced all papers. Publishing a scaffold and validating the code do not establish academic correctness or user-study effectiveness.
