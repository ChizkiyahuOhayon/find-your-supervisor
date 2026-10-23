# Find Your Supervisor｜选择你的赛博导师

**选择一位研究者，学习他/她公开论文、代码、实验与写作背后的研究方法，再帮助自己开展原创研究。**

这不是冒充学者，也不宣称拥有其私下想法。它是基于可验证公开证据的研究方法分析器。任何研究者的个人档案默认只保存在你的本地工作目录，不随开源软件上传。

## 快速开始

在仓库根目录执行：

```bash
python scripts/supervisor.py init --name "Example Scholar" --slug example-scholar --workspace ../private-mentors
python scripts/supervisor.py import-csv ../private-mentors/example-scholar/researcher.json examples/synthetic-publications.csv --source-name example
python scripts/supervisor.py status ../private-mentors/example-scholar/researcher.json
python scripts/supervisor.py next ../private-mentors/example-scholar/researcher.json
```

`examples/synthetic-publications.csv` 是虚构数据，不能作为真实学术证据。

阅读 `SKILL.md` 和 `references/`，按 G1 身份与论文来源、G2 逐页阅读、G3 源码审计、G4 实际复现、G5 研究方法归纳、G6 导师式决策的流程推进。

仅在身份、论文来源与可溯源的多篇论文证据充足时运行：

```bash
python scripts/build_mentor.py --ledger ../private-mentors/example-scholar/researcher.json --dna ../private-mentors/example-scholar/dna.json --output ../private-mentors/example-scholar/generated-skill
```

## 与其他开源项目的关系

项目受到 CCFA-Skills、Supervisor-Skills、AI-Research-SKILLs 启发；并不克隆它们的代码。第三方 Skills 可单独安装；`scripts/adapters.py` 仅检查本地文件可用性，不自动安装或执行。请尊重各上游许可证，特别是 Supervisor-Skills 的 CC BY-NC-SA 限制。

阅读 [英文 README](../README.md)、[架构](architecture.md)、[集成方式](integrations.md) 和 [安全与隐私](../SECURITY.md)。
