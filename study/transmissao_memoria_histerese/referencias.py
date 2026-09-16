"""Extra independent references for active propagation and hysteresis trajectories."""
import json
import numpy as np
from core import *
from experimento import load_protocol, execute_case, setup


def main():
    p=load_protocol(); refs=[]
    primary={r['id']:r for r in map(json.loads,(ROOT/'resultados.jsonl').read_text().splitlines())}
    for case in p['all_conditions']:
        if case['stage']=='memory' and case['graph'] in ['original','interface_10pct','cut'] and case['amplitude_factor']==1.1 and case['restore_s']==.5:
            model,seg,threshold,t,y,_=execute_case(case,dict(method='Radau',rtol=1e-10,atol=1e-12,max_step=.0025))
            old=np.load(ROOT/(case['id']+'.npz'));err=float(abs(y[:N]-old['y'][:N]).max())
            m=metrics(model,t,y,seg,case['gap'],threshold);r=primary[case['id']]
            same=m['target_final_fraction']==r['target_final_fraction'] and m['target_ever_fraction']==r['target_ever_fraction']
            refs.append(dict(id=case['id'],kind='network_active',max_voltage_difference_V=err,classification_agrees=same,passed=bool(err<2e-5 and same)))
            np.savez_compressed(ROOT/('radau_active_'+case['id']+'.npz'),t=t,y=y)
    h=json.loads((ROOT/'histerese.json').read_text());lo,hi=h['current_range_A_m2'];old=np.load(ROOT/'histerese_trajetorias.npz')
    for name in ['kv','bistable']:
        for leg in [.2,1.,5.]:
            model=MODELS[name];rate=(hi-lo)/leg;drive=lambda t:np.array([lo+rate*t if t<=leg else hi-rate*(t-leg)])
            t,y,_=simulate(model,[(leg,np.zeros((1,1)),drive),(2*leg,np.zeros((1,1)),drive)],gap=0.,
                           y0=model.state(1,model.roots(lo)[0]),sample=leg/4000,method='Radau',rtol=1e-10,atol=1e-12,max_step=.002)
            err=float(abs(y[0]-old[f'{name}_{leg}'][:,2]).max())
            refs.append(dict(id=f'{name}_{leg}',kind='hysteresis',max_voltage_difference_V=err,passed=bool(err<2e-5)))
    # A stricter per-receptor event diagnostic, in addition to the frozen crossing metric.
    events=[]
    for case in p['all_conditions']:
        if case['model']!='excitable':continue
        z=np.load(ROOT/(case['id']+'.npz'));v=z['y'][:N][RIGHT];rest=MODELS['excitable'].roots()[0]
        strong=v.max(1)>-.01;recovered=abs(v[:,-1]-rest)<.001
        events.append(dict(id=case['id'],peak_above_minus10_fraction=float(strong.mean()),
                           recovered_strong_excursion_fraction=float((strong&recovered).mean()),
                           frozen_crossing_fraction=primary[case['id']]['target_ever_fraction']))
    out=dict(references=refs,strict_excursion_diagnostic=events,passed=all(x['passed'] for x in refs))
    (ROOT/'referencias_adicionais.json').write_text(json.dumps(out,indent=2)+'\n');print('Extra references',out['passed'],len(refs))
    assert out['passed']


if __name__=='__main__':main()
