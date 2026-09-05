---
name: arab-writer
description: Arabic writing and editing for Codex: proofread, rewrite, naturalize, shorten or expand, adapt tone, preserve author voice, and edit professional, executive, academic, financial, policy, marketing, technical, bilingual, Saudi/Gulf, or general Arabic. Use when Arabic output quality is the task. Do not trigger for coding, research-only, or single-word translation unless writing/editing is requested.
---

# Arab Writer

Treat the user's explicit instructions as the highest-priority writing constraints. Use this skill to improve Arabic writing quality without changing facts, evidence, intent, or the author's chosen voice unless the user asks for those changes.

## Mission

Produce Arabic that is:
- correct;
- natural;
- precise;
- context-aware;
- audience-appropriate;
- faithful to source facts and claim strength;
- consistent in terminology, punctuation, and formatting.

Do not optimize for AI-detector evasion. Do not claim that any phrase proves or disproves AI authorship. Treat "AI-like" patterns only as style heuristics.

## Default behavior

If the user does not specify a register, default to clear Modern Standard Arabic with moderate formality, direct wording, and minimal rhetorical padding.

Do not ask for a style brief when the request can be completed from context. Infer audience, medium, and tone from the text and request. Ask only when a missing choice would materially change the result and cannot be inferred.

## Step 1 — Classify the task

Choose one primary mode and any supporting modes.

Primary modes:
- `proofread`: correct errors only; preserve wording and structure as much as possible.
- `rewrite`: improve clarity, flow, and wording while preserving meaning.
- `naturalize`: reduce stiffness, repetition, generic phrasing, and mechanical structure.
- `voice-lock`: preserve the author's recognizable voice while repairing quality issues.
- `shorten`: reduce length by information priority, not by compressing every sentence.
- `expand`: add useful development only from user-provided facts or clearly labeled general explanation.
- `translate-polish`: translate and then make the target Arabic natural and domain-appropriate.

Context modes:
- `professional`
- `executive`
- `academic`
- `financial`
- `policy-legal`
- `marketing-social`
- `technical-product`
- `saudi-gulf`
- `dialect-sensitive`
- `bilingual`

Load only the references relevant to the selected modes.

## Step 2 — Set risk level

### Standard risk
Use for ordinary messages, posts, general writing, and low-stakes content.

### Elevated risk
Use for professional, public, customer-facing, marketing, or institutional content.

### High fidelity
Use for academic, legal, regulatory, financial, medical, technical specifications, policies, contracts, or any text containing critical numbers, dates, citations, standards, IDs, or compliance claims.

At high fidelity:
1. Build a protected-content ledger before editing.
2. Preserve all protected items exactly unless the user explicitly asks to change them.
3. Do not strengthen causal, legal, financial, medical, regulatory, or scientific claims.
4. Flag ambiguity instead of inventing a resolution.
5. For long files or dense numeric content, use `scripts/protected_tokens.py` before and after the edit when tools are available.

## Step 3 — Build the protected-content ledger

Before editing, identify and preserve as applicable:
- names and titles;
- dates and deadlines;
- amounts, percentages, quantities, units, and currencies;
- identifiers, license numbers, invoice numbers, manuscript IDs, ticket IDs;
- standards, regulations, article numbers, clauses, versions, model names;
- citations, references, DOI values, URLs, email addresses;
- quotations;
- formulas, equations, code, variables, and table values;
- contractual conditions and exceptions;
- claim strength: possibility, association, correlation, causation, obligation, estimate, forecast, or fact.

If the user explicitly requests a factual change, update only the affected protected item and keep the rest intact.

## Step 4 — Load the relevant references

Always consult:
- `references/arabic-core.md`
- `references/naturalness.md`
- `references/quality-gates.md`

Then load by task:
- tone or voice: `references/tone-and-voice.md`
- professional or executive: `references/professional-executive.md`
- academic: `references/academic-research.md`
- financial/business: `references/financial-business.md`
- policy/legal/regulatory: `references/policy-legal.md`
- marketing/social: `references/marketing-social.md`
- technical/product: `references/technical-product.md`
- bilingual/translation: `references/bilingual-translation.md`
- Saudi/Gulf context: `references/saudi-gulf.md`
- dialect: `references/dialect-sensitive.md`
- Markdown, tables, mixed-direction text: `references/formatting-rtl.md`

Use `references/examples.md` only when an example pattern helps resolve an editing decision.

## Step 5 — Edit at the lightest effective level

Follow this order:
1. Correct definite language errors.
2. Remove ambiguity.
3. Improve sentence architecture.
4. Remove redundant wording.
5. Repair transitions and paragraph flow.
6. Adjust tone and register.
7. Restructure only when the original structure is materially weaker or the user asks for restructuring.

Do not rewrite already-good sentences merely to make the edit look larger.

## Step 6 — Preserve voice

Unless the user requests a new voice:
- preserve the author's directness;
- preserve typical sentence length within reason;
- preserve domain vocabulary;
- preserve first/third person choices;
- preserve dialect or MSA preference;
- preserve intentional informality;
- preserve rhetorical intensity when appropriate.

Do not "professionalize" a personal message into bureaucratic Arabic.

## Step 7 — Naturalness rules

Prefer:
- concrete verbs over stacked abstract nouns;
- direct logical links over decorative transitions;
- varied but purposeful sentence length;
- specific claims over generic framing;
- one conclusion instead of repeated restatement;
- natural paragraph boundaries based on idea shifts.

Review, rather than mechanically ban:
- "في ظل"
- "في إطار"
- "من الجدير بالذكر"
- "من المهم الإشارة"
- "علاوة على ذلك"
- "يلعب دورًا محوريًا"
- "يشكل ركيزة أساسية"
- generic introductions and conclusions;
- forced three-part lists;
- repeated label-colon bullets;
- excessive bolding and headings.

Keep any of these when they are genuinely the best wording.

## Step 8 — Output discipline

Return the artifact the user asked for.

If the user asks for:
- a finished rewrite: return the finished rewrite;
- proofreading only: do not substantially rewrite;
- tracked changes or comparison: show the changes clearly;
- multiple options: make them meaningfully different;
- a short version: prioritize information and remove low-value detail;
- a professional version: make purpose, requested action, owner, deadline, or decision explicit when present in the source;
- an academic edit: preserve evidence, citations, terminology, and epistemic strength.

Do not append a generic explanation unless the user asks for rationale, change notes, or comparison.

## Step 9 — Quality gate

Before returning, run the checklist in `references/quality-gates.md`.

For high-fidelity edits, verify:
- every number;
- every date;
- every named entity;
- every citation/reference marker;
- every standard/ID;
- every exception and condition;
- every causal or obligation verb.

If the before/after text is available as files and tools are available, run:

```bash
python scripts/qa_pair.py before.txt after.txt
```

Fix any true-positive issues before final output.

## Non-goals

Do not use this skill to:
- fabricate evidence, citations, facts, sources, or quotes;
- bypass plagiarism or authorship-detection systems;
- disguise copied text as original work;
- convert uncertain evidence into certainty;
- add legal, financial, medical, or regulatory advice not present in the source merely to make writing sound stronger;
- translate a single isolated word when no writing/editing task exists;
- answer research-only or coding-only questions just because the final answer may contain Arabic.
