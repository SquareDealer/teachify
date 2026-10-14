# teachify

A Claude skill that turns Claude into a guard-railed tutor for learning **backend** and **ML**. It runs a full course: a diagnostic, a roadmap, and lessons built from *your* materials, each split into theory and practice.

The design follows what research says about learning with AI. Unrestricted AI help hurts retention; a tutor that withholds answers, gives hints step by step and works from a source of truth helps (Bastani et al., PNAS 2025; Kestin et al., 2025; Anthropic, 2026).

## Commands

| Command | What it does |
|---|---|
| `/teachify init [topic]` | Mission interview → adaptive diagnostic → target level → `roadmap.md` |
| `/teachify path/to/roadmap.md` | Due reviews → next lesson: asks for your material, builds theory + practice, tutors you through it |
| `/teachify learn <concept>` | One-off lesson on a concept, no roadmap (short prerequisite check first) |
| `/teachify review` | Spaced, interleaved quiz over everything learned so far |

## How a lesson works

1. **Your material is the source of truth.** You drop a chapter, docs page or lecture; it is converted to Markdown and every claim in the lesson cites it.
2. **Theory**: a short HTML lesson with an inline quiz (theory approach adapted from Matt Pocock's [`teach`](https://github.com/mattpocock/skills) skill). Then you write `notes.md` **from memory**, and a separate agent checks it against the source.
3. **Practice** (fixed four-step loop, ~45–60 min):
   - main task: from scratch in NumPy + reference check (ML), or the core of a service inside a scaffold with `TODO(human)` (backend), with a 4-rung hint ladder (question → concept → pseudocode → code on request only);
   - **bug hunt** in your own solution;
   - **teach-back**: explain it to a picky junior who keeps asking "why?";
   - 3 retrieval questions scheduled at +1/+3/+7 days.
4. Checkboxes in `roadmap.md`: Theory, Practice, and Mastered (≥80% on a delayed quiz).

## Architecture

Dialogue stays in the main thread (diagnostic, hint ladder, quizzes, teach-back). Subagents handle heavy work with no dialogue and independent checks:

| Subagent | Job |
|---|---|
| source-ingester | your files/URLs → clean Markdown (parallel, one per source) |
| curriculum-planner | concept map, diagnostic bank, roadmap, finding sources |
| theory-builder | `theory.html` + cheat sheets |
| practice-builder | tasks, tests, `TODO(human)` scaffolds, answer key with pre-written hints; verifies the tests |
| bug-injector | plants realistic bugs in your passing solution |
| fact-checker | audits the lesson and your notes against the sources (never the agent that wrote them) |

## Install

**Claude Code**: copy the skill folder into your skills directory:

```bash
git clone https://github.com/SquareDealer/teachify.git
mkdir -p ~/.claude/skills
cp -r teachify/teachify ~/.claude/skills/
```

Or per project: `.claude/skills/teachify/` in the repo.

**Claude apps**: upload `teachify/SKILL.md` as a custom skill.

## Course workspace

`/teachify init` creates one folder per course:

```
MISSION.md  PROFILE.md  CONCEPT-MAP.md  roadmap.md  RESOURCES.md  GLOSSARY.md
errors.md   reviews.md  NOTES.md  learning-records/  reference/  assets/
lessons/NNNN-slug/{sources/, lesson-plan.md, theory.html, notes.md, practice/, .keys/}
```

## Research basis

- Shen & Tamkin (Anthropic), *How AI assistance impacts the formation of coding skills*, 2026
- Bastani et al., *Generative AI without guardrails can harm learning*, PNAS 2025
- Kestin et al., *AI tutoring outperforms in-class active learning*, Scientific Reports 2025
- Lee et al., *The Impact of Generative AI on Critical Thinking*, CHI 2025
- Dunlosky et al., *Improving Students' Learning With Effective Learning Techniques*, 2013

## License

MIT. Portions adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
