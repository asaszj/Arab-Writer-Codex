# Installation

## Recommended: `$skill-installer`

Open Codex and invoke:

```text
$skill-installer
```

Ask:

```text
Install the skill from https://github.com/asaszj/Arab-Writer-Codex/tree/main/.agents/skills/arab-writer
```

After installation, use `/skills` or type `$arab-writer`.

If Codex does not show a newly installed skill, restart Codex.

## Manual personal installation

macOS / Linux / WSL:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R .agents/skills/arab-writer "$HOME/.agents/skills/arab-writer"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
Copy-Item -Recurse -Force ".\.agents\skills\arab-writer" "$HOME\.agents\skills\arab-writer"
```

## Repository-scoped installation

Copy:

```text
.agents/skills/arab-writer
```

into the target repository.

Codex can then discover it when working inside that repository.
