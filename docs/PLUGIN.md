# Codex Plugin Distribution

The repository remains the source of truth for the skill under `.agents/skills/arab-writer`.

A root `.codex-plugin/plugin.json` declares the plugin and points to the repository skill path. `tools/package_plugin.py` creates a normalized distributable plugin ZIP with:

```text
arab-writer-codex/
├── .codex-plugin/plugin.json
├── skills/arab-writer/...
├── LICENSE
└── README.md
```

The packaged manifest rewrites the skills path to `./skills/`.

This follows current Codex plugin conventions while avoiding duplicated source trees in Git.
