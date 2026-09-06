#!/usr/bin/env python3
"""Create reproducible execution metadata for Arab Writer runs.

v1.3 separates configured settings from observed runtime settings. A prompt that
requests a model/effort is never treated as runtime evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path

ENV_MODEL=("CODEX_MODEL","OPENAI_MODEL","MODEL")
ENV_REASONING=("CODEX_REASONING","OPENAI_REASONING_EFFORT","REASONING_EFFORT")

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def env_value(keys):
    for k in keys:
        if os.environ.get(k):
            return os.environ[k],f"env:{k}"
    return "unknown","unavailable"

def git_commit(cwd):
    try:
        return subprocess.check_output(["git","rev-parse","HEAD"],cwd=cwd,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"

def setting(configured,configured_source,observed=None,observed_source=None):
    obs=observed or "unknown"
    return {
        "configured":configured or "unknown",
        "configured_source":configured_source,
        "observed":obs,
        "observed_source":observed_source or ("unavailable" if obs=="unknown" else "explicit"),
        "verified":obs!="unknown",
        "effective_claim":obs if obs!="unknown" else "unknown",
    }

def build(source=None,output=None,model=None,reasoning=None,version_file=None,cwd=None,observed_model=None,observed_reasoning=None):
    cwd=Path(cwd or ".").resolve()
    if model is None: model,model_source=env_value(ENV_MODEL)
    else: model_source="cli/configured"
    if reasoning is None: reasoning,reasoning_source=env_value(ENV_REASONING)
    else: reasoning_source="cli/configured"
    version="unknown"
    if version_file and Path(version_file).exists():
        version=Path(version_file).read_text(encoding="utf-8").strip()
    elif (cwd/"VERSION").exists():
        version=(cwd/"VERSION").read_text(encoding="utf-8").strip()
    return {
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "skill_version":version,
        "skill_commit":git_commit(cwd),
        "model":setting(model,model_source,observed_model,"runtime-observation" if observed_model else None),
        "reasoning":setting(reasoning,reasoning_source,observed_reasoning,"runtime-observation" if observed_reasoning else None),
        "source_sha256":sha256(source) if source and Path(source).exists() else None,
        "output_sha256":sha256(output) if output and Path(output).exists() else None,
        "provenance_rule":"Configured settings and observed runtime settings are distinct. Unknown observed values remain unknown; prompt text is not evidence."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source"); ap.add_argument("--output")
    ap.add_argument("--model"); ap.add_argument("--reasoning")
    ap.add_argument("--observed-model"); ap.add_argument("--observed-reasoning")
    ap.add_argument("--version-file"); ap.add_argument("--cwd",default="."); ap.add_argument("--out")
    args=ap.parse_args()
    data=build(args.source,args.output,args.model,args.reasoning,args.version_file,args.cwd,args.observed_model,args.observed_reasoning)
    text=json.dumps(data,ensure_ascii=False,indent=2)
    if args.out: Path(args.out).write_text(text+"\n",encoding="utf-8")
    else: print(text)
    return 0
if __name__=="__main__": raise SystemExit(main())
