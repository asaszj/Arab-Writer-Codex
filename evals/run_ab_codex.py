#!/usr/bin/env python3
"""Run the same evals through Codex baseline and Codex + $arab-writer.

Requires an authenticated `codex` CLI. No API key is stored by this repo.
Outputs JSONL plus a CSV review sheet. This evaluates the actual Codex skill path,
not merely an inlined prompt.
"""
from __future__ import annotations
import argparse, csv, json, shutil, subprocess, tempfile, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'.agents/skills/arab-writer'

def run_codex(workdir: Path, prompt: str, timeout: int, model: str|None):
    out=workdir/'last_message.txt'; out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['codex','exec','--ephemeral','--skip-git-repo-check','-s','read-only','-C',str(workdir),'--output-last-message',str(out)]
    if model: cmd += ['-m',model]
    cmd += [prompt]
    started=time.time()
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=timeout)
    text=out.read_text(encoding='utf-8') if out.exists() else ''
    return {"returncode":p.returncode,"seconds":round(time.time()-started,2),"output":text,"stderr":p.stderr[-4000:]}

def prompt_for(case, with_skill):
    parts=[]
    if with_skill: parts.append('$arab-writer')
    parts.append(case['task'])
    if case.get('input'): parts.append('\nالنص:\n'+case['input'])
    parts.append('\nأعد الناتج المطلوب فقط دون شرح منهجك، إلا إذا كانت المهمة تطلب تفسيرًا.')
    return '\n'.join(parts)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--evals',default=str(ROOT/'tests/evals.jsonl')); ap.add_argument('--out',default=str(ROOT/'evals/results')); ap.add_argument('--limit',type=int); ap.add_argument('--timeout',type=int,default=180); ap.add_argument('--model'); args=ap.parse_args()
    if not shutil.which('codex'): raise SystemExit('codex CLI not found on PATH')
    cases=[json.loads(x) for x in Path(args.evals).read_text(encoding='utf-8').splitlines() if x.strip()]
    if args.limit: cases=cases[:args.limit]
    outdir=Path(args.out); outdir.mkdir(parents=True,exist_ok=True); jsonl=outdir/'ab_results.jsonl'; csvp=outdir/'human_review.csv'
    rows=[]
    with jsonl.open('w',encoding='utf-8') as jf:
      for case in cases:
        with tempfile.TemporaryDirectory(prefix='aw-base-') as bd, tempfile.TemporaryDirectory(prefix='aw-skill-') as sd:
            base=Path(bd); cand=Path(sd); (cand/'.agents/skills').mkdir(parents=True); shutil.copytree(SKILL,cand/'.agents/skills/arab-writer')
            br=run_codex(base,prompt_for(case,False),args.timeout,args.model)
            cr=run_codex(cand,prompt_for(case,True),args.timeout,args.model)
            rec={"id":case['id'],"case":case,"baseline":br,"candidate":cr}
            jf.write(json.dumps(rec,ensure_ascii=False)+'\n'); jf.flush()
            rows.append({"id":case['id'],"task":case['task'],"input":case.get('input',''),"baseline":br['output'],"candidate":cr['output'],"preferred":"","fidelity_0_2":"","arabic_0_2":"","naturalness_0_2":"","tone_0_2":"","notes":""})
    with csvp.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else ['id']); w.writeheader(); w.writerows(rows)
    print(f'Wrote {jsonl} and {csvp}')
    return 0
if __name__=='__main__': raise SystemExit(main())
