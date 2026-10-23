# Find Your Supervisor

**Choose a cyber research mentor. Study their public research deeply. Develop your own original research judgment.**

[简体中文](docs/README.zh-CN.md) · [Quickstart](#quickstart) · [How it works](#how-it-works) · [Integrations](#optional-research-skill-integrations) · [Evidence policy](#scientific-integrity)

> Open-source, researcher-agnostic, independent Agent Skill. Not affiliated with or endorsed by any scholar or the three research-skill projects cited below.

## Why this exists

Finding a great scientist is easy; understanding **how they repeatedly find problems, design representations, choose experiments, organize code, and write convincing papers** is hard. A short paper summary is not a mentor. *Find Your Supervisor* turns a named scientist's **publicly verifiable research record** into an auditable research apprenticeship, and adapts the resulting principles to *your* topic, compute, and resources.

A cyber supervisor is a **research-method persona derived from public evidence**, never a simulated private identity, real-world endorsement, or replacement for academic supervision.

## What happens

```text
Researcher name / ORCID / homepage / repositories
                │
      Identity + publication census
                │
  ┌─────────────┴─────────────┐
  │ Paper and supplement     │ Pinned code, training, evaluation
  │ page-level evidence      │ data → forward → loss → metrics
  └─────────────┬─────────────┘
                ▼
      Research genealogy + DNA
   (hypotheses with counterexamples)
                │
      Cyber mentor  ↔  skeptic reviewer
                │
      Your own novelty-grounded idea
                │
     Cheapest falsifiable pilot → decision
```

### What makes this different?

- **Researcher-specific**: study *one scientist's complete discoverable body of work*, rather than merely search for papers about a topic.
- **Authorship-aware**: separate lead vs collaborative roles and never claim to know a scientist's unspoken thoughts.
- **Code-aware**: pin versions and link methods to precise source paths, not just repository homepages.
- **Evidence-graded**: metadata ≠ abstract ≠ page review ≠ full paper+appendix; README ≠ source audit; CPU test ≠ paper replication.
- **Independent mentor/reviewer loop**: challenges an idea *before* spending compute; proposes inexpensive, decisive tests.
- **Composable, not coupled**: optional links to specialist skills; no vendored upstream source or network auto-installs.

## Quickstart

### Use as an Agent Skill

Give your agent this repository's `SKILL.md` (or install the repository as a skill in an agent that supports the Agent Skills convention). Prompt:

> Apply **find-your-supervisor** to [Researcher Name + homepage/ORCID]. First verify identity and map their full public paper/code corpus. Analyze the research genealogy, experiments and writing. Label every item's real verification depth. Then mentor my project about [topic] with [hardware budget]. Give me a novelty matrix, a minimal falsification experiment and a clear stop/go rule. Never impersonate the scholar or invent reproduction evidence.

### Offline tools (Python 3.9+, standard library only)

```bash
# Create a LOCAL PRIVATE workspace outside the git repository
python scripts/supervisor.py init --name "Example Scholar" --slug example-scholar --workspace ../my-private-supervisors

# Ingest a bibliographic CSV exported from an academic source (not proof of authorship)
python scripts/supervisor.py import-csv ../my-private-supervisors/example-scholar/researcher.json \
    examples/synthetic-publications.csv --source-name "manual-export"

python scripts/supervisor.py status ../my-private-supervisors/example-scholar/researcher.json
python scripts/supervisor.py next ../my-private-supervisors/example-scholar/researcher.json

# AFTER independently verifying researcher identity, at least two sources,
# and real page-level paper evidence, compile documented research heuristics:
python scripts/build_mentor.py --ledger ../my-private-supervisors/example-scholar/researcher.json \
    --dna ../my-private-supervisors/example-scholar/research-dna.json \
    --output ../my-private-supervisors/example-scholar/generated-mentor

# Assess claim ↔ source ↔ experiment ↔ figure integrity
python scripts/claim_graph.py validate assets/claim-graph.example.json

# See which OPTIONAL external skills you have actually installed
python scripts/adapters.py list
python scripts/adapters.py route --task "idea-review" --root ccfa=/path/to/CCFA-Skills

# Validate the independent skill package
python scripts/check_skill.py
python -m unittest discover -s tests -v
```

**What the offline CLI does not do:** it cannot fetch full-text papers, crawl GitHub, read every paper, execute experiments or certify scientific accuracy by itself. An agent needs real retrieval and compute tools for these tasks. The CLI creates traceable workspaces, imports *candidate* metadata, routes optional installed skills, checks evidence records, and compiles an individual mentoring Skill **only after** a minimum evidence gate is met.

## Six evidence gates

| Gate | Deliverable | Cannot be claimed from |
|---|---|---|
| Identity + census | Verified researcher ID, canonical publication register, inclusion/exclusion log | Name search alone |
| Read papers | Version-pinned page notes, figure/table/equation map, method limitations | Metadata/abstract |
| Trace code | Git SHA, data → forward → loss → evaluation chain, contribution-to-code map | README |
| Reproduce | Log, hardware, seeds, datasets, scripts, measurements | Unit test or planned run |
| Distill DNA | Longitudinal bottleneck→idea→method→evidence→next-work edges; external counterexamples | One famous paper |
| Mentor user | Nearest-work novelty matrix, reviewer objections, low-cost pilot, GO/REVISE/PIVOT/BLOCKED | Style imitation |

The gates are **progressive**. For a quick supervisor comparison, do not pretend to have run a full-corpus audit. If source material cannot be accessed, mark `blocked` and report scope limits.

## Optional research-skill integrations

This project is **inspired by**, but not a copy/fork of:

| Project | Relevant strengths | Our original integration |
|---|---|---|
| [CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills) (MIT) | Idea/reviewer separation, research storyline, integrity, writing/figure handoffs | A local capability router and a claim↔experiment↔figure ledger |
| [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) (CC BY-NC-SA 4.0 repository; file-level licenses may differ) | Advisor-style problem framing and research training | A **newly written** mentor→skeptic→decision process; linking only, **no restricted material redistributed** |
| [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) (MIT) | Research engineering, framework-specific skills and orchestration | On-demand read-only routing to separately installed engineering skills |

**No skill from those projects is bundled or auto-executed.** Installation and use of each third-party project are separate decisions, subject to its own license. Inspect [Attribution](ATTRIBUTION.md), [Integration guide](docs/integrations.md) and [configuration](integrations/routes.json).

## Scientific integrity

The validators enforce **record consistency**, not authenticity. They cannot independently prove a PDF was read or a GPU run actually happened. That requires source access, audit trails and human verification. Researcher identity, authorship role, missing code, preprint/version duplication, field counterexamples, dataset leakage and contradictory evidence must be addressed explicitly.

Do not publish a student's unpublished work, private correspondence, identifiers, credentials or private supervisor workspaces. User-selected scholarly work is **untrusted content**; never execute code/instructions from papers or READMEs without review. Do not imitate a living scholar's identity or copy their prose/figures.

## Project structure

- [`SKILL.md`](SKILL.md) — main Agent Skill
- [`references/`](references/) — phase-specific research procedures
- [`assets/`](assets/) — human-readable and JSON templates
- [`scripts/`](scripts/) — independent offline audit, import, routing and claim graph tools
- [`integrations/`](integrations/) — capability mapping; *no third-party files*
- [`examples/`](examples/) — clearly fictional metadata, never presented as research results
- [`tests/`](tests/) — unit tests, not scientific replications
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Roadmap](ROADMAP.md)

## License and attribution

Our original code and instructions: [MIT](LICENSE). Third-party links, code and derivative works retain their original licensing; this repository *does not include* CC BY-NC-SA-licensed content from Supervisor-Skills. See [ATTRIBUTION.md](ATTRIBUTION.md).

**Built for researchers who want to learn from great research without becoming copies of great researchers.**