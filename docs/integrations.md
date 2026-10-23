# Optional research skill integrations

Find Your Supervisor runs without other skill families. The following projects are **optional independently installed additions**:

| Provider | Purpose | License |
| --- | --- | --- |
| [CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills) | Idea review, argument integrity, experiments, writing and visual composition | MIT |
| [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | Mentor-style idea evaluation and deep research | CC BY-NC-SA 4.0 at repository level; check each file |
| [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | PEFT, attention implementations and training-engineering skills | MIT |

No third-party code or skill is vendored. Installing external projects is the user's separate choice. `integrations/routes.json` lists example compatible files and can be audited or updated when third-party structures change.

```bash
python scripts/adapters.py list
python scripts/adapters.py route --task idea-review --root ccfa=/path/to/CCFA-Skills --root supervisor=/path/to/Supervisor-Skills --json
```

The adapter performs read-only file presence checks. **Presence does not equal execution permission or interoperability guarantee.** Follow each provider's license; do not copy text from NC/SA works into a separately licensed project. Verify citations and methodology independently.
