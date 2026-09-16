"""Exploratory mechanism development on isolated cell and original graph only."""
import json
import numpy as np
from scipy.optimize import brentq
from core import *


def save(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


def main():
    records=[]; equilibria={}; selected={}; threshold=MODELS['bistable'].roots()[1]
    for name,model in MODELS.items():
        rr=model.roots(); eq=[]
        for v in rr:
            y=model.state(1,v); rhs,jac=functions(model,np.zeros((1,1)),0.,np.zeros(1))
            eig=np.linalg.eigvals(jac(0,y).toarray())
            eq.append(dict(V=float(v),max_real_eigenvalue_s_inv=float(eig.real.max())))
        equilibria[name]=eq
    save('equilibrios.json',equilibria)
    masks={}
    masks['center']=np.eye(N)[CENTER]
    masks['center_neighbors']=masks['center'].copy(); masks['center_neighbors'][ORIGINAL[CENTER]>0]=1.
    masks['left_domain']=(~RIGHT).astype(float)
    # Pulse development: all attempts retained; no intervention-graph results used.
    for name in ['bistable','excitable']:
        model=MODELS[name]; chosen=None
        for mask_name,mask in masks.items():
            lo=0.; hi=None
            for amp in [.02,.05,.1,.2,.5,1.]:
                seg=protocol_segments(ORIGINAL,amp,mask,end=.6)
                t,y,check=simulate(model,seg,sample=.001)
                m=metrics(model,t,y,seg,threshold=threshold)
                success=m['target_ever_fraction']>=.5
                records.append(dict(model=name,mask=mask_name,amplitude=amp,success=success,**m))
                save('tentativas_desenvolvimento.json',records)
                print('development',name,mask_name,amp,m['target_ever_fraction'],m['target_final_fraction'],flush=True)
                if success:
                    hi=amp; break
                lo=amp
            if hi is not None:
                for _ in range(10):
                    mid=(lo+hi)/2
                    seg=protocol_segments(ORIGINAL,mid,mask,end=.6)
                    t,y,_=simulate(model,seg,sample=.001)
                    m=metrics(model,t,y,seg,threshold=threshold)
                    success=m['target_ever_fraction']>=.5
                    records.append(dict(model=name,mask=mask_name,amplitude=mid,success=success,**m))
                    if success:hi=mid
                    else:lo=mid
                chosen=dict(mask=mask_name,mask_nodes=np.flatnonzero(mask).tolist(),threshold_lower_A_m2=lo,threshold_upper_A_m2=hi,
                            threshold_definition='>=50% target nodes cross fixed bistable unstable root within 0.6 s; excitability separately checked',
                            amplitude_factors=[.9,1.,1.1],pulse_s=.02)
                selected[name]=chosen
                save('tentativas_desenvolvimento.json',records)
                break
        if chosen is None:selected[name]=dict(propagation_found=False)
    save('desenvolvimento.json',dict(equilibria=equilibria,selected=selected,classification_threshold_V=float(threshold)))
    print(json.dumps(selected,indent=2),flush=True)


if __name__=='__main__':main()
