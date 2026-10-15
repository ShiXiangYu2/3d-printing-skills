"""Local stage runner: validate first, fingerprint inputs/outputs, resume unchanged work."""
import argparse,hashlib,json,os,subprocess,sys,time,uuid
from pathlib import Path

HERE=Path(__file__).resolve().parent
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def write_json(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=Path(str(path)+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');json.loads(tmp.read_text(encoding='utf-8'))
 subprocess.run(['powershell','-NoProfile','-File',str(HERE/'atomic_move.ps1'),'-Source',str(tmp),'-Destination',str(path)],check=True,capture_output=True,creationflags=0x08000000)
def bounded(root,path):
 p=(root/path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
 if not p.is_relative_to(root) or p==root:raise ValueError('Output escapes workspace: '+str(p))
 if p.exists() and not p.is_file():raise ValueError('Output must be a file: '+str(p))
 return p
def execute(command,cwd,timeout,log):
 if not isinstance(command,list) or not command or not all(isinstance(x,str) for x in command):raise ValueError('Command must be argv strings')
 with log.open('wb') as f:r=subprocess.run(command,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,creationflags=0x08000000)
 if r.returncode:raise RuntimeError(f'Command exit {r.returncode}; see {log}')
def run(planpath,until=None,force=False):
 planpath=planpath.resolve();plan=json.loads(planpath.read_text(encoding='utf-8'));root=Path(plan['workspace']).resolve();root.mkdir(parents=True,exist_ok=True);meta=root/'.pipeline';meta.mkdir(exist_ok=True)
 stages=plan['stages'];seen=set();producers={}
 for stage in stages:
  n=stage['id']
  if not n or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in n) or n in seen:raise ValueError('Bad/duplicate stage id')
  if not set(stage.get('depends_on',[]))<=seen:raise ValueError('Dependencies must appear earlier')
  seen.add(n)
  if not stage.get('validate'):raise ValueError('Each stage requires a validation command')
  if not stage.get('outputs'):raise ValueError('Each stage requires declared output files')
  for s in stage['outputs']:
   p=bounded(root,s)
   if str(p) in producers:raise ValueError('Shared output path between stages: '+str(p))
   producers[str(p)]=n
 if until is not None and until not in seen:raise ValueError('Unknown --until stage')
 cachepath=meta/'cache.json';cache=json.loads(cachepath.read_text(encoding='utf-8')) if cachepath.exists() else {};records=[];start=time.perf_counter();runid=time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
 try:
  for stage in stages:
   t=time.perf_counter();n=stage['id'];outputs=[bounded(root,s) for s in stage['outputs']];inputs={}
   for s in stage.get('inputs',[]):
    p=Path(s);p=(root/p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_file():raise FileNotFoundError('Missing declared input: '+str(p))
    inputs[str(p)]=sha(p)
   for dep in stage.get('depends_on',[]):
    for s in next(x for x in stages if x['id']==dep)['outputs']:
     p=bounded(root,s);inputs[str(p)]=sha(p)
   payload={'stage':stage,'inputs':inputs,'runner':sha(Path(__file__))}
   signature=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();old=cache.get(n,{})
   intact=old.get('validated') is True and old.get('signature')==signature and all(p.is_file() and sha(p)==old.get('outputs',{}).get(str(p)) for p in outputs)
   if intact and not force:records.append({'id':n,'status':'cached','seconds':round(time.perf_counter()-t,4)})
   else:
    # Preserve declared stale outputs, so old artifacts cannot pass a new successful exit.
    moves=[]
    for p in outputs:
     if p.exists():
      dst=meta/'history'/runid/n/p.relative_to(root);dst.parent.mkdir(parents=True,exist_ok=True);moves.append({'source':str(p),'destination':str(dst)})
    if moves:
     mp=meta/(n+'-moves.json');write_json(mp,moves);subprocess.run(['powershell','-NoProfile','-File',str(HERE/'batch_move.ps1'),'-Root',str(root),'-Plan',str(mp)],check=True,capture_output=True,creationflags=0x08000000)
    cwd=Path(stage.get('cwd',str(root))).resolve();log=meta/(n+'-'+runid+'.log.tmp');execute(stage['command'],cwd,stage.get('timeout_seconds',900),log)
    for p in outputs:
     if not p.is_file() or p.stat().st_size==0:raise RuntimeError('New nonempty output missing: '+str(p))
    vlog=meta/(n+'-'+runid+'-validation.log.tmp');execute(stage['validate'],cwd,stage.get('timeout_seconds',900),vlog)
    cache[n]={'signature':signature,'outputs':{str(p):sha(p) for p in outputs},'validated':True};write_json(cachepath,cache);records.append({'id':n,'status':'executed','seconds':round(time.perf_counter()-t,4),'log':str(log),'validation_log':str(vlog)})
   if n==until:break
  result={'ok':True,'seconds':round(time.perf_counter()-start,4),'stages':records,'note':'Cached outputs are unchanged previously validated results, not a new physical-fit test.'}
 except Exception as exc:
  result={'ok':False,'seconds':round(time.perf_counter()-start,4),'stages':records,'failed_stage':locals().get('n'),'error':str(exc)}
 write_json(meta/'last-run.json',result);write_json(meta/('run-'+runid+'.json'),result);return result
def main():
 p=argparse.ArgumentParser();p.add_argument('plan',type=Path);p.add_argument('--until');p.add_argument('--force',action='store_true');a=p.parse_args();r=run(a.plan,a.until,a.force);print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['ok'] else 1
if __name__=='__main__':raise SystemExit(main())
