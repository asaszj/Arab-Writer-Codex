#!/usr/bin/env python3
"""Arab Writer v1.3 release gate.

Structural mode is deterministic and CI-safe.
Empirical mode consumes a metrics JSON produced by benchmark/human review and
enforces non-regression thresholds before a release claim.
"""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod

def structural():
    errors=[]
    version=(ROOT/"VERSION").read_text(encoding="utf-8").strip() if (ROOT/"VERSION").exists() else "missing"
    if version!="1.3.0": errors.append(f"VERSION is {version}, expected 1.3.0")
    plugin=json.loads((ROOT/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if plugin.get("version")!=version: errors.append("plugin/version mismatch")
    bm=load_module(ROOT/"evals/benchmark_matrix.py","benchmark_matrix")
    cases=bm.load_cases(ROOT/"evals/benchmark_matrix.json")
    errors.extend(bm.validate(cases))
    required=[
        ".agents/skills/arab-writer/scripts/fidelity_graph.py",
        ".agents/skills/arab-writer/scripts/editorial_gain.py",
        ".agents/skills/arab-writer/scripts/numeral_policy.py",
        ".agents/skills/arab-writer/scripts/run_provenance.py",
    ]
    for p in required:
        if not (ROOT/p).exists(): errors.append(f"missing {p}")
    return {"mode":"structural","errors":errors,"passed":not errors}

def empirical(metrics):
    errors=[]
    required=["critical_fidelity_regressions","arabic_correctness_delta","human_preference_win_rate","overediting_regression_rate","false_positive_rate"]
    for k in required:
        if k not in metrics: errors.append(f"missing metric: {k}")
    if errors: return {"mode":"empirical","errors":errors,"passed":False}
    if metrics["critical_fidelity_regressions"]!=0: errors.append("critical fidelity regressions must be zero")
    if metrics["arabic_correctness_delta"]<0: errors.append("Arabic correctness regressed")
    if metrics["human_preference_win_rate"]<0.55: errors.append("human preference win rate below 55%")
    if metrics["overediting_regression_rate"]>0.10: errors.append("over-editing regression rate above 10%")
    if metrics["false_positive_rate"]>0.10: errors.append("false-positive rate above 10%")
    return {"mode":"empirical","errors":errors,"passed":not errors}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["structural","empirical"],default="structural")
    ap.add_argument("--metrics")
    args=ap.parse_args()
    if args.mode=="structural":
        result=structural()
    else:
        if not args.metrics: raise SystemExit("--metrics is required for empirical mode")
        result=empirical(json.loads(Path(args.metrics).read_text(encoding="utf-8")))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
