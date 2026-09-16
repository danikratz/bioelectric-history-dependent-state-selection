"""Explicit graph/mask adapter and one frozen scalar cubic net-current model."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigvals
from scipy.sparse import diags
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'transmissao_memoria_histerese'
sys.path.insert(0,str(OLD))
import core as old

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def protocol():
    p=json.loads((ROOT/'protocolo_validacao.json').read_text())
    assert digest(ROOT/'protocolo_validacao.json')==json.loads((ROOT/'congelamento.json').read_text())['protocol_sha256']
    for k,v in p['source_sha256'].items():assert digest(ROOT.parent/k)==v,k
    assert digest(ROOT/'geometrias.npz')==p['geometry_sha256']
    return p
P=protocol(); A=P['alternative']; L,U,H=A['L_V'],A['U_V'],A['H_V']; TAU=A['tau_s']; DEN=TAU*(H-L)**2

def cubic(v):return (v-L)*(v-U)*(H-v)/DEN

def cubic_prime(v):return ((v-U)*(H-v)+(v-L)*(H-v)-(v-L)*(v-U))/DEN

def roots(case):
    if case['model']=='cubic':return np.array([L,U,H])
    if case['model']=='leak':return np.array([old.EL])
    return old.Model(case['model'],case['gd']).roots()

def state(case,n,voltage=None):
    if case['model'] in ['cubic','leak']:return np.full(n,roots(case)[0]) if voltage is None else np.broadcast_to(voltage,(n,)).copy()
    return old.Model(case['model'],case['gd']).state(n,voltage)

def funcs(case,adj,current):
    if case['model'] not in ['cubic','leak']:return old.functions(old.Model(case['model'],case['gd']),adj,P['constants']['Gj'],current)
    lap=old.lap(adj);gap=P['constants']['Gj']; n=len(adj)
    def rhs(t,v):
        drive=current(t) if callable(current) else current
        intrinsic=cubic(v) if case['model']=='cubic' else -old.GL*(v-old.EL)/old.C
        return intrinsic-gap*(lap@v)/old.C+drive/old.C
    def jac(t,v):
        slope=cubic_prime(v) if case['model']=='cubic' else np.full(n,-old.GL/old.C)
        return diags(slope)-gap*lap/old.C
    return rhs,jac

def integrate(case,segments,solver,y0=None,sample=None):
    n=len(segments[0][1]);y=state(case,n) if y0 is None else y0.copy(); sample=P['sample_s'] if sample is None else sample
    start=0.;ts=[np.array([0.])];ys=[y[:,None]];nfev=0
    for end,adj,current in segments:
        if end<=start+1e-13:continue
        rhs,jac=funcs(case,adj,current)
        grid=np.arange(np.floor(start/sample)+1,np.ceil(end/sample)+1)*sample
        grid=np.unique(np.r_[grid[(grid>start+1e-12)&(grid<end-1e-12)],end])
        kw=dict(jac=jac) if solver['method']=='Radau' else {}
        sol=solve_ivp(rhs,(start,end),y,t_eval=grid,**solver,**kw)
        if not sol.success:raise RuntimeError(sol.message)
        ts.append(sol.t);ys.append(sol.y);y=sol.y[:,-1];nfev+=sol.nfev;start=end
    t=np.concatenate(ts); y=np.concatenate(ys,axis=1)
    if not np.isfinite(y).all():raise ValueError('nonfinite solution')
    if len(y)>n and (y[n:].min() < -1e-7 or y[n:].max()>1+1e-7):raise ValueError('gate outside [0,1]')
    return t,y,dict(nfev=nfev,gate_min=float(y[n:].min()) if len(y)>n else None,gate_max=float(y[n:].max()) if len(y)>n else None,solver=solver)

def setup(c):
    with np.load(ROOT/'geometrias.npz') as z:
        name=c['geometry']; orig=z[name+'_original']; damaged=z[name+'_'+c['history']]; right=z[name+'_right']
    meta=next(g for g in P['geometries'] if g['name']==c['geometry']); source=meta['source']
    events=sorted(set([0.,c['pulse_s'],c['end_s']]+([c['restore_s']] if c['restore_s'] is not None else [])))
    seg=[]
    for t0,t1 in zip(events[:-1],events[1:]):
        adj=orig if c['restore_s'] is not None and t0>=c['restore_s']-1e-12 else damaged
        current=np.zeros(len(orig))
        if t0<c['pulse_s']-1e-12:current[source]=c['amplitude_A_m2']
        seg.append((t1,adj,current))
    return seg,right,source

def summary(case,t,y,seg,right):
    n=len(right);v=y[:n];r=roots(case);thr=float(r[1]) if len(r)==3 else float(old.Model('bistable',4.).roots()[1]);rest=float(r[0]);cl=P['classification']
    rhs,jac=funcs(case,seg[-1][1],np.zeros(n)); dy=rhs(t[-1],y[:,-1]); eigen=eigvals(jac(0,y[:,-1]).toarray()); maxeig=float(eigen.real.max())
    dv=float(abs(dy[:n]).max());dg=float(abs(dy[n:]).max()) if len(y)>n else 0.
    stationary=dv<cl['stationary_max_dV_V_s'] and dg<cl['stationary_max_gate_derivative_s_inv'];stable=maxeig<cl['stable_max_real_eigen_s_inv']
    high=v[:,-1]>thr;ever=(v>thr).any(1);departure=float(abs(v[:,-1]-rest).max());hits=np.where((v[right]>thr).any(0))[0]
    category='indeterminada'
    if stationary and stable:
        if departure<=cl['rest_max_departure_V']:category='transiente_sem_persistencia' if ever.any() else 'repouso'
        else:category='recrutamento_coletivo' if high[right].mean()>=cl['collective_min_target_fraction'] else 'memoria_localizada'
    junction=float(abs((old.lap(seg[-1][1])@v[:,::10]).sum(0)).max())
    return dict(category=category,stationary=bool(stationary),linearly_stable=bool(stable),max_real_eigen_s_inv=maxeig,final_dV_max_V_s=dv,final_gate_derivative_max_s_inv=dg,threshold_V=thr,rest_V=rest,target_count=n if right.all() else int(right.sum()),target_high=int(high[right].sum()),total_high=int(high.sum()),target_ever_high=int(ever[right].sum()),total_ever_high=int(ever.sum()),target_high_fraction=float(high[right].mean()),final_mean_V=float(v[:,-1].mean()),target_final_mean_V=float(v[right,-1].mean()),final_min_V=float(v[:,-1].min()),final_max_V=float(v[:,-1].max()),peak_V=float(v.max()),target_peak_V=float(v[right].max()),first_target_recruitment_s=float(t[hits[0]]) if len(hits) else None,final_max_departure_V=departure,threshold_margin_final_V=float(abs(v[:,-1]-thr).min()),junction_sum_sampled_max_A_m2=junction)

def execute(c,solver):
    seg,right,source=setup(c);t,y,info=integrate(c,seg,solver)
    m=summary(c,t,y,seg,right);idx=int(np.argmin(abs(t-2.)));assert abs(t[idx]-2.)<1e-12
    m2=summary(c,t[:idx+1],y[:,:idx+1],seg,right)
    m.update(category_2s=m2['category'],target_high_2s=m2['target_high'],max_voltage_change_2_to_5s_V=float(abs(y[:len(right),-1]-y[:len(right),idx]).max()))
    return t,y,dict(**c,**m,**info)

def agree(a,b):return all(a[k]==b[k] for k in ['category','target_high','total_high','target_ever_high','total_ever_high'])
