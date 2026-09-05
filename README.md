# Arab Writer for Codex

**Arab Writer** is a Codex-native Arabic writing and editing skill designed for high-quality real-world work: proofreading, rewriting, naturalization, voice preservation, executive communication, academic editing, financial and policy text, marketing, technical documentation, bilingual work, and Saudi/Gulf institutional Arabic.

It is intentionally **Codex-first**. This repository does not package a Claude skill or cross-agent compatibility layer.

## Why this version is different

The skill does more than rewrite sentences. It uses a fidelity-first workflow:

1. **Classify the writing task and risk level.**
2. **Protect facts before editing**: names, dates, amounts, percentages, IDs, standards, citations, URLs, conditions, and claim strength.
3. **Select only the relevant writing references.**
4. **Edit at the lightest effective level.**
5. **Run quality gates after editing.**
6. **Use deterministic QA helpers for high-fidelity work when needed.**

This reduces a common failure mode in AI editing: producing smoother prose while silently changing factual or evidentiary meaning.

## Capabilities

- Arabic proofreading without unnecessary rewriting
- Natural rewriting without generic "AI voice"
- Voice-preserving editing
- Shortening and expansion
- Professional and executive communication
- Academic and research editing
- Financial and business writing
- Policy, legal, and regulatory wording preservation
- Marketing and social content
- Technical and product documentation
- Arabic/English translation polishing
- Saudi/Gulf institutional register
- Dialect-sensitive editing
- RTL/Markdown/table preservation
- Protected-token QA for numbers, dates, IDs, standards, URLs, and citations

## Codex-native structure

```text
.agents/
└── skills/
    └── arab-writer/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        │   └── style-brief.md
        ├── references/
        │   ├── arabic-core.md
        │   ├── naturalness.md
        │   ├── tone-and-voice.md
        │   ├── professional-executive.md
        │   ├── academic-research.md
        │   ├── financial-business.md
        │   ├── policy-legal.md
        │   ├── marketing-social.md
        │   ├── technical-product.md
        │   ├── bilingual-translation.md
        │   ├── saudi-gulf.md
        │   ├── dialect-sensitive.md
        │   ├── formatting-rtl.md
        │   ├── quality-gates.md
        │   └── examples.md
        └── scripts/
            ├── arabic_lint.py
            ├── protected_tokens.py
            └── validate_skill.py
```

## Install in Codex

### Option A — Skill Installer

In Codex, invoke:

```text
$skill-installer
```

Then ask it to install the skill from:

```text
https://github.com/asaszj/Arab-Writer-Codex/tree/main/.agents/skills/arab-writer
```

### Option B — Personal skill

Copy `.agents/skills/arab-writer` to:

```text
$HOME/.agents/skills/arab-writer
```

Codex loads personal skills from `$HOME/.agents/skills`.

### Option C — Repository-scoped

Clone this repository or copy `.agents/skills/arab-writer` into another repository's `.agents/skills/` directory.

Codex scans repository-scoped `.agents/skills` locations automatically.

## Use

Explicit:

```text
$arab-writer راجع هذا الخطاب واجعله مهنيًا وطبيعيًا مع الحفاظ على الأرقام والتواريخ.
```

Implicit:

```text
دقق هذا النص العربي لغويًا فقط، ولا تعيد صياغته.
```

Academic:

```text
حرر هذه الفقرة أكاديميًا، وحافظ على المراجع وقوة الادعاءات كما هي.
```

Executive:

```text
حوّل هذه المذكرة إلى صيغة تنفيذية لمجلس الإدارة: القرار، الأثر، المخاطر، والتوصية.
```

Voice lock:

```text
حسّن النص لكن حافظ على أسلوبي ونبرة الكاتب قدر الإمكان.
```

## High-fidelity QA

For long or sensitive edits:

```bash
python .agents/skills/arab-writer/scripts/qa_pair.py before.txt after.txt
```

The scripts report potential issues; they do not auto-correct or decide semantic intent.

## Validate the skill

```bash
python .agents/skills/arab-writer/scripts/validate_skill.py
python -m unittest discover -s tests -v
```

## Design principles

- User instructions outrank skill defaults.
- Meaning outranks elegance.
- Evidence outranks rhetorical strength.
- Naturalness is a writing quality, not detector evasion.
- Correct text should not be rewritten merely to make the edit look substantial.
- High-stakes text requires stricter preservation than casual text.
- References are loaded progressively to keep Codex context efficient.

See [`docs/DESIGN.md`](docs/DESIGN.md) and [`docs/EVALUATION.md`](docs/EVALUATION.md).

## License

MIT.
