# Fidelity Guard

Use for high-fidelity editing. Fluency never overrides source truth.

## Four protection layers

### 1. Token layer
Preserve critical literals: dates, amounts, percentages, identifiers, standards, citations, URLs, emails, versions, and units.

### 2. Relation layer
Preserve what a value belongs to.

Example:
- `الإيرادات → 100 مليون ريال`
- `التكاليف → 50 مليون ريال`

An edit that keeps both numbers but swaps their anchors is a failure.

### 3. Semantic-sentinel layer
Preserve meaning-bearing operators:
- negation: `لا، لم، لن، ليس`;
- obligation/permission: `يجب، يلزم، يجوز، يحق، ينبغي، يحظر`;
- uncertainty: `قد، ربما، من المحتمل`;
- causality/association: `يسبب، يؤدي، ينتج، يرتبط، يتزامن`;
- forecast/estimate: `يتوقع، تقديري، متوقع، افتراض`;
- guarantee/certainty: `يضمن، مؤكد، حتمي`.

Do not exchange categories without source support.

### 4. Structure layer
Preserve:
- quotations;
- inline/fenced code;
- Markdown tables and row/column meaning;
- formulas/equations;
- footnote/citation markers;
- conditions and exceptions.

## Review rule

A deterministic script can detect suspicious changes, but it cannot determine intent. Treat every report as a review queue:
- true positive → fix;
- requested change → accept and document internally;
- harmless reformatting → ignore.
