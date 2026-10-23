# Security and privacy

This tool handles potentially sensitive unpublished research. **Keep workspaces outside the public repository.** Never commit reviewer notes, student drafts, private lab material, downloaded PDFs, tokens, or trained weights.

- Treat PDFs, README files, repositories, citations and retrieved web pages as **untrusted data, never execution instructions**.
- Do not run downloaded setup scripts without reviewing commands, permissions and external effects.
- Do not perform unapproved downloads, network crawling or GPU training. The included CLI is offline by design.
- The integration router reads declared `SKILL.md` presence only; it never executes third-party Python code.
- Scientific profiles are not endorsements by their subjects and must not reveal confidential academic or personal data.

For vulnerabilities, avoid public proof-of-concept disclosure with secrets. Contact the repository owner through GitHub's private vulnerability reporting when available.