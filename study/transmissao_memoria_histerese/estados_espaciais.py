"""Post-run stability check of the two history-dependent witness configurations."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core import *
from experimento import setup


def main():
    rows=[json.loads(x) for x in (ROOT/'resultados.jsonl').read_text().splitlines()]
    witnesses=[r for r in rows if r['stage']=='memory' and r['model']=='bistable' and r['amplitude_factor']==.9 and r['restore_s']==.5 and r['graph'] in ['original','interface_10pct']]
    results=[];states=[]
    for case in witnesses:
        model,seg,threshold=setup(case);z=np.load(ROOT/(case['id']+'.npz'));y=z['y'][:,-1]
        rhs,jac=functions(model,ORIGINAL,1.,np.zeros(N))
        eigen=np.linalg.eigvals(jac(0,y).toarray())
        rng=np.random.default_rng(np.random.SeedSequence([20260914,15,78]));yp=y.copy();yp[:N]+=rng.uniform(-.0001,.0001,N)
        t,yy,_=simulate(model,[(1.,ORIGINAL,np.zeros(N))],y0=yp,rtol=1e-10,atol=1e-12)
        error=float(abs(yy[:N,-1]-y[:N]).max())
        results.append(dict(id=case['id'],graph_history=case['graph'],same_final_graph='original',
                            final_voltage_min_V=float(y[:N].min()),final_voltage_max_V=float(y[:N].max()),
                            nodes_above_unstable_root=int((y[:N]>threshold).sum()),targets_above_unstable_root=int((y[:N][RIGHT]>threshold).sum()),
                            max_real_eigenvalue_s_inv=float(eigen.real.max()),final_voltage_residual_V_s=float(abs(rhs(0,y)[:N]).max()),
                            perturbation_return_error_V=error,passed=bool(eigen.real.max()<0 and error<1e-6)))
        states.append(y[:N])
    out=dict(witnesses=results,passed=all(x['passed'] for x in results),scope='Two inspected histories; not a global attractor census')
    (ROOT/'estados_espaciais.json').write_text(json.dumps(out,indent=2)+'\n')
    fig,axes=plt.subplots(1,3,figsize=(12,4.5),layout='constrained')
    rest=MODELS['bistable'].roots()[0]
    titles=['Repouso antes do pulso','Rede intacta durante o pulso','Interface fraca até 500 ms']
    for ax,voltage,title in zip(axes,[np.full(N,rest)]+states,titles):
        image=ax.scatter(XY[:,0],XY[:,1],c=voltage*1000,vmin=-52,vmax=8,cmap='viridis',s=22)
        ax.scatter(XY[CENTER,0],XY[CENTER,1],marker='*',s=100,facecolors='none',edgecolors='#e34a33',linewidths=1.2)
        ax.set(title=title,aspect='equal');ax.set_xticks([]);ax.set_yticks([])
    fig.colorbar(image,ax=axes,label='Voltagem (mV)')
    fig.suptitle('Histórias diferentes, mesmas conexões e parâmetros finais\nPulso de 20 ms no nó marcado; estímulo 0,9 × referência; estados aos 2 s')
    fig.savefig(ROOT/'05_estados_espaciais.png',dpi=180);plt.close(fig)
    print(json.dumps(out,indent=2));assert out['passed']


if __name__=='__main__':main()
