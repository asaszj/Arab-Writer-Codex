# Bibliography & Citation Consistency — v1.3

Do not invent missing bibliographic data.

## Internal schema
Where possible parse:
- source type;
- organization/author;
- title;
- year/date;
- publication;
- URL;
- DOI/identifier.

Missing data remains null and becomes a review item.

## Editing
- If the user specifies APA/Chicago/etc., apply it only from known metadata.
- Otherwise normalize the document's existing convention conservatively.
- Preserve citation-to-source identity.
- Do not create URLs, years, DOI values, authors, or publication details.

Use `scripts/bibliography_schema.py` for structured audit.
