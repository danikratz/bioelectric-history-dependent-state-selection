"""Extract exact final voltage arrays from frozen trajectories; never integrate ODEs."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 root=a.study_root/'validacao_generalizacao_2026-09';rows=[json.loads(s) for s in (root/'resultados_conferidos_validacao.jsonl').read_text().splitlines()]
 assert len(rows)==136
 arrays={};sources={}
 for r in rows:
  f=root/r['effective_source']/(r['id']+'.npz')
  with np.load(f,allow_pickle=False) as z:v=z['y'][:226,-1].copy()
  assert v.shape==(226,) and np.isfinite(v).all()
  arrays[r['id']]=v;sources[r['id']]=dict(source=str(f.relative_to(a.study_root)),source_sha256=digest(f),array_sha256=hashlib.sha256(v.tobytes()).hexdigest(),shape=list(v.shape),dtype=str(v.dtype))
 a.output.parent.mkdir(parents=True,exist_ok=True);np.savez_compressed(a.output,**arrays)
 with np.load(a.output,allow_pickle=False) as z:
  assert all(np.array_equal(arrays[k],z[k]) for k in arrays)
 report=dict(scope='Exact y[:226,-1] extracted from each archived effective validation trajectory. Endpoints only; not sufficient to audit transients or solver convergence.',cases=136,cache_sha256=digest(a.output),source_trajectories=sources,no_ode_integration=True)
 a.output.with_suffix('.provenance.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: 136 final voltage arrays extracted exactly; no simulation')
if __name__=='__main__':main()
