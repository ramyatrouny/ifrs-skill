---
status: accepted
---

# Feature reviews fan out one agent per standard

A Feature review runs in stages: a **locate** pass reduces the codebase to the files
where money is calculated, stored or rendered; one **review** agent per standard the
Trigger map fired on then reads only those files and only its own section of
`standards-reference.md`; Blocking findings go to a **verify** agent that tries to
disprove them against the code; the parent merges, dedupes and derives the Verdict.

The number of review agents is whatever the Trigger map produced — never fixed — and at
most six, one per Covered standard with IAS 1 and IFRS 18 sharing one. A standard is never
split across two agents.

## Why, and one reason that does not hold

The obvious argument is context size: `standards-reference.md` is 945 KB, roughly 236k
tokens. **That argument is wrong and should not be repeated.** The per-standard
sections a review actually reads are small — IAS 1 is 61 lines, IFRS 15 is 116, IFRS 9
is 341 — so all six together fit comfortably in one context. Fanning out to afford the
reference would be solving a problem that does not exist.

The reasons that do hold:

- **Attention.** One agent asked to check six standards at once checks each of them
  more shallowly than six agents checking one each. Depth per standard is the whole
  product here; a review that misses the real defect is worse than no review, because
  it will be trusted.
- **Codebase size.** The user's code is what is large, not the reference. The locate
  pass shrinks it, but on a substantial repository the located set is still the biggest
  thing any agent reads.
- **Independence.** An agent that checks its own finding is not checking it. Verification
  is only worth its cost when performed by an agent that did not produce the finding.

## Considered options

- **Split by code module instead of by standard.** Two agents reviewing different
  modules against the same standard produce the same finding twice, and reconciling
  duplicates costs more than the split saves. The locate pass removes the problem that
  motivated this option.
- **A standards x modules grid.** Multiplies agents without adding coverage.
- **Single agent, all six sections.** Affordable, and the option this decision rejects
  on attention grounds rather than cost grounds.
- **Locate, then split by standard.** Chosen.

## Consequences

Verifying Blocking findings roughly doubles the token cost of a review. That is the
price of a Verdict that can stop a release without being wrong, and it is the same
trade this repository already made when it built `scripts/check_citations.py` instead
of trusting that citations looked right. Because the cost is borne by whoever installs
the skill, `feature-review.md` states the agent count before a review starts.

Parallel execution is an optimisation, not the definition: the review is written as an
ordered procedure, so a host without subagents works the same list sequentially and
says so in its output. It must never silently narrow scope to fit a single context —
a review that skipped standards without saying so reads as approval.

Findings must carry enough context to be merged by a parent that did not read the code,
which constrains the schema each review agent returns.
