"""Single-cell equilibrium folds versus finite-rate current sweep hysteresis."""
import csv
import json
import numpy as np
from scipy.optimize import brentq
from core import *


def slope(model,v):
    fv,av=f(v),a(v)
    return GL+GK*(fv+(v-EK)*fv*(1-fv)/Q['slope_V'])-model.gd*(av*(1-av)/.004*(ED-v)-av)


def main():
    model=MODELS['bistable']; xx=np.linspace(-.1,.05,2001)
    folds=[brentq(lambda v:slope(model,v),x,y) for x,y in zip(xx[:-1],xx[1:]) if slope(model,x)*slope(model,y)<0]
    currents=[float(model.steady_current(v)) for v in folds]
    low=min(currents)-.005; high=max(currents)+.005
    rows=[]; traces={}; restholds=[]; adj=np.zeros((1,1))
    for name in ['kv','bistable']:
        model=MODELS[name]
        for leg in [.2,1.,5.]:
            rate=(high-low)/leg
            drive=lambda t:np.array([low+rate*t if t<=leg else high-rate*(t-leg)])
            y0=model.state(1,model.roots(low)[0])
            t,y,_=simulate(model,[(leg,adj,drive),(2*leg,adj,drive)],gap=0.,y0=y0,sample=leg/4000,max_step=.002)
            current=np.array([drive(x)[0] for x in t]); v=y[0]
            up=np.interp(np.linspace(low,high,2001),current[t<=leg],v[t<=leg])
            down=np.interp(np.linspace(low,high,2001),current[t>=leg][::-1],v[t>=leg][::-1])
            area=float(np.trapz(abs(up-down),np.linspace(low,high,2001)))
            threshold=MODELS['bistable'].roots()[1]
            idxup=np.flatnonzero((v[1:]>threshold)&(v[:-1]<=threshold))+1
            idxdown=np.flatnonzero((v[1:]<threshold)&(v[:-1]>=threshold))+1
            rows.append(dict(model=name,leg_duration_s=leg,rate_A_m2_s=rate,loop_area_V_A_m2=area,
                             ascending_crossing_A_m2=float(current[idxup[0]]) if len(idxup) else None,
                             descending_crossing_A_m2=float(current[idxdown[-1]]) if len(idxdown) else None))
            traces[f'{name}_{leg}']=np.column_stack([t,current,v,y[1]])
        for label,v0 in [('low',MODELS['bistable'].roots()[0]),('high',MODELS['bistable'].roots()[-1])]:
            t,y,_=simulate(model,[(2.,adj,np.zeros(1))],gap=0.,y0=model.state(1,v0),sample=.001)
            restholds.append(dict(model=name,initial=label,initial_V=float(v0),final_V=float(y[0,-1])))
    with (ROOT/'histerese.csv').open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    np.savez_compressed(ROOT/'histerese_trajetorias.npz',**traces)
    result=dict(fold_V=folds,fold_current_A_m2=currents,current_range_A_m2=[low,high],rest_holds=restholds,
                scope='Synthetic current sweep, including voltages outside physiological range; equilibrium roots, not sweep area alone, establish bistability')
    (ROOT/'histerese.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(result=result,rows=rows),indent=2))


if __name__=='__main__':main()
