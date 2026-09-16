"""Additional mechanism controls, documented after main protocol freeze."""
import json
import numpy as np
from core import *


def main():
    d=json.loads((ROOT/'desenvolvimento.json').read_text());rows=[];checks={};traces={}
    for source_model in ['bistable','excitable']:
        for factor in [.9,1.,1.1]:
            amp=d['selected'][source_model]['threshold_upper_A_m2']*factor
            for name,adj in GRAPHS.items():
                seg=protocol_segments(adj,amp,np.eye(N)[CENTER],pulse=.02,restore=.5,end=2.)
                t,y,_=simulate(MODELS['kv'],seg,rtol=1e-10,atol=1e-12,max_step=.0025)
                m=metrics(MODELS['kv'],t,y,seg,threshold=d['classification_threshold_V'])
                rows.append(dict(source_model=source_model,factor=factor,graph=name,amplitude_A_m2=amp,
                                 peak_over_minus10_fraction=float((y[:N][RIGHT].max(1)>-.01).mean()),**m))
            print('ablation',source_model,factor,flush=True)
    lambdas=np.linalg.eigvalsh(lap(ORIGINAL).toarray());stability=[]
    for gd in [3.6,4.,4.4]:
        model=Model('bistable',gd)
        for branch,v in [('low',model.roots()[0]),('high',model.roots()[-1])]:
            _,jac=functions(model,np.zeros((1,1)),1.,np.zeros(1));j=jac(0,model.state(1,v)).toarray()
            values=[]
            for eigen in lambdas:
                jl=j.copy();jl[0,0]-=max(eigen,0)/C;values.extend(np.linalg.eigvals(jl))
            stability.append(dict(gd=gd,branch=branch,voltage_V=float(v),max_real_eigenvalue_s_inv=float(np.real(values).max())))
    for branch,index in [('low',0),('high',-1)]:
        model=MODELS['bistable'];v=model.roots()[index]
        rng=np.random.default_rng(np.random.SeedSequence([20260914,15,77]))
        y0=model.state(N,v+rng.uniform(-.001,.001,N))
        t,y,_=simulate(model,[(1.,ORIGINAL,np.zeros(N))],y0=y0,rtol=1e-10,atol=1e-12)
        checks['perturbed_'+branch+'_returns']=bool(abs(y[:N,-1]-v).max()<1e-6)
        traces['perturbed_'+branch]=np.column_stack([t,y[:N].mean(0),y[:N].min(0),y[:N].max(0)])
    high=MODELS['bistable'].roots()[-1]
    t,y,_=simulate(MODELS['kv'],[(1.,ORIGINAL,np.zeros(N))],y0=MODELS['bistable'].state(N,high),rtol=1e-10,atol=1e-12)
    checks['gd_removal_erases_high_state']=bool(abs(y[:N,-1]-MODELS['kv'].roots()[0]).max()<1e-6)
    traces['washout']=np.column_stack([t,y[:N].mean(0)])
    checks['stable_homogeneous_branches']=all(x['max_real_eigenvalue_s_inv']<0 for x in stability)
    checks['no_regenerative_target_peak_when_gd_off']=all(x['peak_over_minus10_fraction']==0 for x in rows)
    checks['gd_off_returns']=all(x['final_max_departure_mV']<.001 for x in rows)
    result=dict(ablation_cases=rows,stability=stability,checks=checks,passed=all(checks.values()))
    (ROOT/'controles_adicionais.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(ROOT/'controles_trajetorias.npz',**traces)
    print(json.dumps(checks),flush=True);assert result['passed']


if __name__=='__main__':main()
