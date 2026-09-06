#!/usr/bin/env python3
"""Run identical evals through Codex baseline and Codex + $arab-writer.

v1.3 records configured model/reasoning separately from observed runtime values.
Requires an authenticated `codex` CLI. No credential is stored in the repo.
"""
from __future__ import annotations
import argparse, csv, json, shutil, subprocess, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'.agents/skills/arab-writer'

def git_commit():
    try: return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    except Exception: return 'unknown'

def codex_version():
    try: return subprocess.check_output(['codex','--version'],text=True,stderr=subprocess.STDOUT).strip()
    except Exception: return 'unknown'

def run_codex(workdir:Path,prompt:str,timeout:int,model:str|None,reasoning:str|None):
    out=workdir/'last_message.txt'; out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['codex','exec','--ephemeral','--skip-git-repo-check','-s','read-only','-C',str(workdir),'--output-last-message',str(out)]
    if model: cmd += ['-m',model]
    if reasoning: cmd += ['-c',f'model_reasoning_effort={reasoning}']
    cmd += [prompt]
    started=time.time()
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=timeout)
    text=out.read_text(encoding='utf-8') if out.exists() else ''
    return {
        'returncode':p.returncode,'seconds':round(time.time()-started,2),
        'output':text,'stderr':p.stderr[-4000:],
        'configured_model':model or 'un-pinned',
        'configured_reasoning':reasoning or 'un-pinned',
        'observed_model':'unknown',
        'observed_reasoning':'unknown',
        'runtime_verified':False,
    }

def prompt_for(case,with_skill):
    parts=[]
    if with_skill: parts.append('$arab-writer')
    parts.append(case['task'])
    if case.get('input'): parts.append('\nالنص:\n'+case['input'])
    parts.append('\nأعد الناتج المطلوب فقط دون شرح منهجك، إلا إذا كانت المهمة تطلب تفسيرًا.')
    return '\n'.join(parts)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--evals',default=str(ROOT/'tests/evals.jsonl'))
    ap.add_argument('--out',default=str(ROOT/'evals/results'))
    ap.add_argument('--limit',type=int); ap.add_argument('--timeout',type=int,default=180)
    ap.add_argument('--model'); ap.add_argument('--reasoning')
    args=ap.parse_args()
    if not shutil.which('codex'): raise SystemExit('codex CLI not found on PATH')
    cases=[json.loads(x) for x in Path(args.evals).read_text(encoding='utf-8').splitlines() if x.strip()]
    if args.limit: cases=cases[:args.limit]
    outdir=Path(args.out); outdir.mkdir(parents=True,exist_ok=True)
    metadata={
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'skill_version':(ROOT/'VERSION').read_text(encoding='utf-8').strip(),
        'skill_commit':git_commit(),
        'codex_cli_version':codex_version(),
        'configured_model':args.model or 'un-pinned',
        'configured_reasoning':args.reasoning or 'un-pinned',
        'observed_model':'unknown',
        'observed_reasoning':'unknown',
        'runtime_verification':'NOT VERIFIED unless separate runtime evidence is captured',
        'cases':len(cases),
    }
    (outdir/'run_metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    jsonl=outdir/'ab_results.jsonl'; csvp=outdir/'human_review.csv'
    rows=[]
    with jsonl.open('w',encoding='utf-8') as jf:
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='aw-base-') as bd, tempfile.TemporaryDirectory(prefix='aw-skill-') as sd:
                base=Path(bd); cand=Path(sd); (cand/'.agents/skills').mkdir(parents=True)
                shutil.copytree(SKILL,cand/'.agents/skills/arab-writer')
                br=run_codex(base,prompt_for(case,False),args.timeout,args.model,args.reasoning)
                cr=run_codex(cand,prompt_for(case,True),args.timeout,args.model,args.reasoning)
                rec={'id':case['id'],'case':case,'baseline':br,'candidate':cr}
                jf.write(json.dumps(rec,ensure_ascii=False)+'\n'); jf.flush()
                rows.append({
                    'id':case['id'],'task':case['task'],'input':case.get('input',''),
                    'baseline':br['output'],'candidate':cr['output'],
                    'preferred':'','fidelity_0_2':'','instruction_0_2':'','grammar_0_2':'',
                    'mechanics_0_2':'','naturalness_0_2':'','organization_0_2':'',
                    'voice_0_2':'','domain_precision_0_2':'','overediting':'','underediting':'','notes':''
                })
    with csvp.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else ['id']); w.writeheader(); w.writerows(rows)
    print(f'Wrote {jsonl}, {csvp}, and run_metadata.json')
    return 0
if __name__=='__main__': raise SystemExit(main())
