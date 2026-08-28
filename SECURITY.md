# Security Policy

## What this repository is

This repository contains Markdown documentation only. It ships no executable application, no
build output, no package published to any registry, and no service. Nothing here runs on a
user's machine as a consequence of installing the skill: the files are read as context by an
AI agent.

The only executable content is the small set of maintenance scripts in `scripts/` and the
GitHub Actions workflows in `.github/workflows/`, both of which run in CI or are run
deliberately by a maintainer.

The threat model is correspondingly narrow, and this policy is scoped to it rather than
copied from a software project.

## Supported versions

The `main` branch is the only supported version. Fixes are made on `main` and released as a
new tag; earlier tags are not patched.

## Reporting a vulnerability

Report privately. Do not open a public issue.

- Preferred: GitHub's private vulnerability reporting, from the **Security** tab of this
  repository ("Report a vulnerability").
- Alternative: contact the repository owner, [@ramyatrouny](https://github.com/ramyatrouny),
  by direct message on GitHub.

Include what you found, where in the repository it is, and how to reproduce it. Expect an
acknowledgement within seven days and an assessment within thirty. If a report is valid and
you would like credit in the fix commit, say so.

## In scope

- **Repository content that could cause harm when read by an agent** — prompt-injection text
  embedded in a skill file, instructions that would cause an agent to exfiltrate data, run
  commands, or contact an external service.
- **Malicious or unsafe code in `scripts/`.** These scripts execute the python assertion
  blocks committed inside the skill files; a path by which untrusted content in a pull
  request could escalate beyond that sandboxed CI job is in scope.
- **Workflow and Actions configuration** — a workflow that leaks the repository token, that
  runs untrusted pull request content with write permissions, or that could be triggered to
  act on behalf of the repository.
- **Supply-chain issues in the pinned Actions or the pinned npm tool version.**
- **Repository or organisation misconfiguration** that would allow unauthorised writes.

## Explicitly not a security issue

**Incorrect accounting guidance is a content issue, not a vulnerability.** A wrong paragraph
reference, a superseded effective date, a misstated requirement, an unbalanced journal entry,
or a statement that no longer reflects the current standard is reported publicly through the
issue templates:

- **Content correction** — a citation or statement in the repository is wrong.
- **Standard update** — a standard or amendment has changed and the repository has not caught
  up.

These are the most valuable reports this project receives and they are handled ahead of most
other work, but they go through the ordinary issue tracker so that they are visible to
everyone relying on the content.

Also out of scope: the accuracy or behaviour of any AI agent that reads this skill;
vulnerabilities in GitHub itself; and the content of third-party sites linked from the
documentation.

## A note for users of this skill

This skill provides technical guidance. It does not replace professional judgment and it is
not a substitute for a qualified accountant or auditor. Verify anything you rely on against
the standard itself.
