import json
import sys
import numpy as np
from scipy.optimize import brentq
from core import *


def main():
    checks={}; details={}
    # Analytical Jacobian checked against finite differences, all model families.
    for name,model in MODELS.items():
        adj=np.array([[0.,.1,0],[.1,0,1],[0,1,0.]])
        y=model.state(3,np.array([-.052,-.034,.005])); rhs,jac=functions(model,adj,4.,np.zeros(3))
        j=jac(0,y).toarray(); numerical=np.zeros_like(j)
        for k in range(len(y)):
            e=np.zeros(len(y)); e[k]=1e-7
            numerical[:,k]=(rhs(0,y+e)-rhs(0,y-e))/(2*e[k])
        err=float(abs(j-numerical).max()); checks[name+'_jacobian']=err<1e-4; details[name+'_jacobian_error']=err
    # Compare new continuous ODE to archived fine-step recurrence, same initial state.
    sys.path.insert(0,str(BASE/'pareamento_condutancia')); import nucleo as old
    v,m,_,_=old.initial(); model=MODELS['kv']
    t,y,_=simulate(model,[(.05,ORIGINAL,np.zeros(N))],y0=np.r_[v,m],sample=.0005)
    previous=np.load(BASE/'sorteio_independente_32/trajetorias.npz')['original_tau0.0148_gap1.0']
    err=float(abs(y[:N].T-previous[:,:N]).max()); checks['historical_ODE_regression']=err<.0001
    details['historical_max_error_V']=err
    # Pulse boundary test: exact integrated forcing time with smooth known leak-only solution.
    # For new models, no-stimulus equilibrium and coupling cancellation are checked directly.
    for name,model in MODELS.items():
        seg=[(.2,ORIGINAL,np.zeros(N))]
        t,y,_=simulate(model,seg)
        err=float(abs(y-model.state(N)[:,None]).max())
        checks[name+'_rest_stationary']=err<1e-8; details[name+'_rest_error']=err
    # Isolated excitability development: 2ms pulse, threshold depends only on isolated cell.
    model=MODELS['excitable']; adj=np.zeros((1,1)); threshold=MODELS['bistable'].roots()[1]
    def isolated(amp):
        return simulate(model,[(.002,adj,np.array([amp])),(1.,adj,np.zeros(1))],gap=0.,sample=.0001)
    lo,hi=0.,1.; trials=[]
    for _ in range(14):
        amp=(lo+hi)/2;t,y,_=isolated(amp)
        hit=bool(y[0].max()>-.01)
        trials.append(dict(amplitude_A_m2=amp,peak_V=float(y[0].max()),hit=hit))
        if hit:hi=amp
        else:lo=amp
    traces={}; singles=[]
    for factor in [.9,1.1]:
        t,y,_=isolated(factor*hi);traces[f'single_{factor}']=np.column_stack([t,y.T])
        peak=int(np.argmax(y[0])); singles.append(dict(factor=factor,peak_V=float(y[0,peak]),peak_time_s=float(t[peak]),final_error_V=float(abs(y[0,-1]-model.roots()[0]))))
    refr=[]
    for interval in [.02,.1,.5]:
        amp=1.1*hi
        seg=[(.002,adj,np.array([amp])),(interval,adj,np.zeros(1)),(interval+.002,adj,np.array([amp])),(interval+1.,adj,np.zeros(1))]
        t,y,_=simulate(model,seg,gap=0.,sample=.0001)
        crossings=np.flatnonzero((y[0,1:]>threshold)&(y[0,:-1]<=threshold))+1
        refr.append(dict(interval_s=interval,crossing_times_s=t[crossings].tolist(),number_of_upcrossings=len(crossings)))
        traces[f'paired_{interval}']=np.column_stack([t,y.T])
    checks['isolated_excitable_subthreshold']=singles[0]['peak_V']<-.01
    checks['isolated_excitable_postpulse_peak']=singles[1]['peak_time_s']>.002 and singles[1]['peak_V']>-.01
    checks['isolated_excitable_returns']=singles[1]['final_error_V']<1e-4
    checks['isolated_recovery_two_events']=refr[-1]['number_of_upcrossings']==2
    details.update(isolated_threshold_bracket_A_m2=[lo,hi],isolated_trials=trials,singles=singles,refractory=refr)
    np.savez_compressed(ROOT/'mecanismos_trajetorias.npz',**traces)
    out=dict(checks=checks,details=details,passed=all(checks.values()))
    (ROOT/'verificacao_mecanismos.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); assert out['passed']


if __name__=='__main__':main()
