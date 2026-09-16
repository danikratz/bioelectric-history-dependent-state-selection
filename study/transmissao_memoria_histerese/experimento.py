"""Frozen finite experiment. Main results and verification are separate commands."""
import csv
import datetime
import hashlib
import json
import platform
import sys
import scipy
from core import *


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def writejson(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')


def freeze():
    assert not (ROOT/'protocolo.json').exists(), 'Protocol already frozen; do not overwrite'
    development=json.loads((ROOT/'desenvolvimento.json').read_text())
    assert json.loads((ROOT/'verificacao_mecanismos.json').read_text())['passed']
    mask=np.eye(N)[CENTER]
    # Rank damaged edges using only a fixed ORIGINAL, graded reference trajectory.
    seg=protocol_segments(ORIGINAL,.02,mask,pulse=.02,end=.2)
    t,y,_=simulate(MODELS['kv'],seg)
    edges=np.argwhere(np.triu(ORIGINAL-GRAPHS['interface_10pct'])>0)
    assert len(edges)==32
    score=np.trapz(abs(y[edges[:,0]]-y[edges[:,1]]),t,axis=1)
    order=np.lexsort((edges[:,1],edges[:,0],-score))
    ranking=[dict(i=int(edges[k,0]),j=int(edges[k,1]),integral_abs_delta_V_s=float(score[k])) for k in order]
    repair_graphs={}; repairs=[]
    orders={'directed':order}
    for seed in [11,22,33]:
        rng=np.random.default_rng(np.random.SeedSequence([20260914,14,64,seed]))
        orders[f'random{seed}']=rng.permutation(32)
    for budget in [4,8,16]:
        for name,selection in orders.items():
            adj=GRAPHS['interface_10pct'].copy()
            for i,j in edges[selection[:budget]]:adj[i,j]=adj[j,i]=1.
            label=f'repair_{name}_{budget}'; repair_graphs[label]=adj
            repairs.append(dict(graph=label,strategy=name,budget_edges=budget,added_weight=budget*.9,
                                edges=edges[selection[:budget]].tolist()))
    np.savez_compressed(ROOT/'reparos.npz',**repair_graphs)
    writejson(ROOT/'selecao_reparos.json',dict(ranking_original_graded=ranking,repairs=repairs,
                                             rule='Ranking fixed before repaired outcomes; random controls restricted to the same 32 damaged edges'))
    cases=[]
    def add(**kw):
        kw['id']=f"case{len(cases):04d}";cases.append(kw)
    # 144 temporal conditions, equal charge and equal current are distinct questions.
    for tau in [.0148,.0592]:
        for gap in [1.,4.]:
            for graph in GRAPHS:
                for duration in [.001,.01,.1]:
                    for dose in ['equal_charge','equal_current']:
                        amp=.0001/duration if dose=='equal_charge' else .02
                        add(stage='temporal',model='kv',gd=0.,tau=tau,gap=gap,graph=graph,
                            pulse_s=duration,amplitude_A_m2=amp,restore_s=.2,end_s=1.,dose=dose)
    # Memory/excitable: identical pulses across all graph conditions.
    for model in ['bistable','excitable']:
        anchor=development['selected'][model]['threshold_upper_A_m2']
        for graph in GRAPHS:
            for factor in [.9,1.,1.1]:
                for restoration in [.02,.05,.2,.5]:
                    add(stage='memory',model=model,gd=4.,tau=.0148,gap=1.,graph=graph,pulse_s=.02,
                        amplitude_A_m2=anchor*factor,amplitude_factor=factor,restore_s=restoration,end_s=2.)
    # Reserved parameter sensitivity: same stimuli, no new threshold fitting.
    for gd in [3.6,4.4]:
        for graph in list(GRAPHS)[:5]:
            for factor in [.9,1.,1.1]:
                for restoration in [.05,.5]:
                    add(stage='sensitivity',model='bistable',gd=gd,tau=.0148,gap=1.,graph=graph,pulse_s=.02,
                        amplitude_A_m2=development['selected']['bistable']['threshold_upper_A_m2']*factor,
                        amplitude_factor=factor,restore_s=restoration,end_s=2.)
    # Repair is performed before stimulation; residual damage remains throughout.
    for model in ['kv','bistable','excitable']:
        anchor=.02 if model=='kv' else development['selected'][model]['threshold_upper_A_m2']
        for factor in [.9,1.,1.1]:
            for graph in ['interface_10pct','original']+list(repair_graphs):
                meta=next((x for x in repairs if x['graph']==graph),dict(strategy='full' if graph=='original' else 'none',budget_edges=32 if graph=='original' else 0,added_weight=28.8 if graph=='original' else 0.))
                add(stage='repair',model=model,gd=0. if model=='kv' else 4.,tau=.0148,gap=1.,graph=graph,pulse_s=.02,
                    amplitude_A_m2=anchor*factor,amplitude_factor=factor,restore_s=None,end_s=2.,
                    strategy=meta['strategy'],budget_edges=meta['budget_edges'],added_weight=meta['added_weight'])
    for model in MODELS:
        for graph in ['original','interface_10pct','cut']:
            add(stage='no_stimulus',model=model,gd=MODELS[model].gd,tau=.0148,gap=1.,graph=graph,pulse_s=.02,
                amplitude_A_m2=0.,restore_s=.2,end_s=2.)
        if model!='kv':
            for graph in ['interface_10pct','cut']:
                add(stage='never_restore',model=model,gd=4.,tau=.0148,gap=1.,graph=graph,pulse_s=.02,
                    amplitude_A_m2=development['selected'][model]['threshold_upper_A_m2']*1.1,
                    amplitude_factor=1.1,restore_s=None,end_s=2.)
    sources={str(p.relative_to(BASE)):digest(p) for p in [BASE/'primeiro_parametro_publicado/plano.json',BASE/'sorteio_independente_32/topologias.npz']}
    sources.update({str(p.relative_to(BASE)):digest(p) for p in [ROOT/'core.py',ROOT/'experimento.py',ROOT/'desenvolvimento.json',ROOT/'PLANO.md',ROOT/'reparos.npz',ROOT/'selecao_reparos.json']})
    protocol=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),registration='Local freeze after original-only development; not external preregistration',
                  all_conditions=cases,source_sha256=sources,primary_solver=dict(method='DOP853',rtol=1e-8,atol=1e-10,max_step=.005),
                  verification_solver=dict(method='DOP853',rtol=1e-10,atol=1e-12,max_step=.0025),
                  verification_rule='Every condition refined. Fixed Radau references: first condition of each model/stage, plus every case with differing classification or >0.02 mV voltage error.',
                  horizon_rule='Every memory/sensitivity case with final |dV/dt|>=1e-5 V/s extended to 5s; also fixed original/interface/cut representatives at factor0.9 and restoration0.5.',
                  sample_s=.001,voltage_tolerance_V=2e-5,stationary_dv_V_s=1e-5,
                  interpretation='All conditions retained; no seed/case replacement. Candidate model findings only; topology already known historically.')
    writejson(ROOT/'protocolo.json',protocol)
    print('FROZEN',len(cases),digest(ROOT/'protocolo.json'),flush=True)


def load_protocol():
    p=json.loads((ROOT/'protocolo.json').read_text())
    for name,sha in p['source_sha256'].items():
        assert digest(BASE/name)==sha,name
    return p


def setup(case):
    model=Model(case['model'],case['gd'],case['tau'])
    graph=GRAPHS[case['graph']] if case['graph'] in GRAPHS else np.load(ROOT/'reparos.npz')[case['graph']]
    mask=np.eye(N)[CENTER]
    seg=protocol_segments(graph,case['amplitude_A_m2'],mask,pulse=case['pulse_s'],restore=case['restore_s'],end=case['end_s'])
    threshold=Model('bistable',case['gd'] if case['gd'] else 4.).roots()[1]
    return model,seg,threshold


def execute_case(case,solver):
    model,seg,threshold=setup(case)
    t,y,check=simulate(model,seg,gap=case['gap'],**solver)
    return model,seg,threshold,t,y,check


def run():
    p=load_protocol();rows=[];final={};traces={}
    output=ROOT/'resultados.jsonl'
    assert not output.exists(),'Existing results must be preserved'
    with output.open('w') as out:
        for index,case in enumerate(p['all_conditions']):
            model,seg,threshold,t,y,check=execute_case(case,p['primary_solver'])
            metrics_row=metrics(model,t,y,seg,case['gap'],threshold)
            row=dict(**case,**metrics_row,**check);rows.append(row)
            out.write(json.dumps(row,allow_nan=False)+'\n');out.flush()
            final[case['id']]=y[:,-1]
            traces[case['id']]=compact(model,t,y,threshold)
            # Full time courses retained for exact verification, then packed.
            np.savez_compressed(ROOT/(case['id']+'.npz'),t=t,y=y)
            if index%20==0:print(index+1,len(p['all_conditions']),case['stage'],flush=True)
    np.savez_compressed(ROOT/'estados_finais.npz',**final)
    np.savez_compressed(ROOT/'respostas_compactas.npz',**traces)
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (ROOT/'metricas.csv').open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rows)
    writejson(ROOT/'execucao.json',dict(conditions=len(rows),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,protocol_sha256=digest(ROOT/'protocolo.json')))
    print('FINISHED',len(rows),flush=True)


def verify():
    p=load_protocol();rows=[];refs=[];extended=[];seen=set()
    original_rows={x['id']:x for x in map(json.loads,(ROOT/'resultados.jsonl').read_text().splitlines())}
    out=(ROOT/'verificacao.jsonl').open('w')
    for index,case in enumerate(p['all_conditions']):
        model,seg,threshold,t,y,check=execute_case(case,p['verification_solver'])
        old=np.load(ROOT/(case['id']+'.npz'))
        assert np.array_equal(t,old['t'])
        err=float(abs(y[:N]-old['y'][:N]).max())
        primary=original_rows[case['id']];m=metrics(model,t,y,seg,case['gap'],threshold)
        classification=(m['target_final_fraction']==primary['target_final_fraction'] and m['target_ever_fraction']==primary['target_ever_fraction'])
        # Both voltage and recruitment classifications must agree.
        passed=err<p['voltage_tolerance_V'] and classification
        rec=dict(id=case['id'],max_voltage_difference_V=err,classification_agrees=classification,passed=bool(passed),
                 refined_peak_mV=m['peak_mV'],refined_final_fraction=m['target_final_fraction'],refined_ever_fraction=m['target_ever_fraction'])
        rows.append(rec);out.write(json.dumps(rec)+'\n');out.flush()
        group=(case['stage'],case['model'])
        if group not in seen or not passed:
            seen.add(group)
            _,_,_,tr,yr,_=execute_case(case,dict(method='Radau',rtol=1e-9,atol=1e-11,max_step=.005))
            referr=float(abs(yr[:N]-y[:N]).max());rm=metrics(model,tr,yr,seg,case['gap'],threshold)
            classref=(rm['target_final_fraction']==m['target_final_fraction'] and rm['target_ever_fraction']==m['target_ever_fraction'])
            refs.append(dict(id=case['id'],max_voltage_difference_V=referr,classification_agrees=classref,passed=bool(referr<p['voltage_tolerance_V'] and classref)))
            np.savez_compressed(ROOT/('radau_'+case['id']+'.npz'),t=tr,y=yr)
        fixed=(case['stage']=='memory' and case['graph'] in ['original','interface_10pct','cut'] and case['amplitude_factor']==.9 and case['restore_s']==.5)
        if case['stage'] in ['memory','sensitivity'] and (m['final_dv_max_V_s']>=p['stationary_dv_V_s'] or fixed):
            adj=seg[-1][1]
            te,ye,_=simulate(model,[(3.,adj,np.zeros(N))],gap=case['gap'],y0=y[:,-1],**p['verification_solver'])
            me=metrics(model,te,ye,[(3.,adj,np.zeros(N))],case['gap'],threshold)
            extended.append(dict(id=case['id'],horizon_s=5.,final_fraction_2s=m['target_final_fraction'],final_fraction_5s=me['target_final_fraction'],
                                 final_dv_max_V_s=me['final_dv_max_V_s'],max_V_change_2_to_5s=float(abs(ye[:N,-1]-y[:N,-1]).max())))
            np.savez_compressed(ROOT/('extended_'+case['id']+'.npz'),t=te+2.,y=ye)
        if index%40==0:print('verification',index+1,len(p['all_conditions']),flush=True)
    out.close()
    result=dict(refinement=rows,radau=refs,extended=extended,passed=all(x['passed'] for x in rows+refs),
                maximum_voltage_difference_V=max(x['max_voltage_difference_V'] for x in rows),
                maximum_radau_difference_V=max(x['max_voltage_difference_V'] for x in refs))
    writejson(ROOT/'verificacao.json',result)
    print('VERIFIED',result['passed'],result['maximum_voltage_difference_V'],flush=True)


if __name__=='__main__':
    {'freeze':freeze,'run':run,'verify':verify}[sys.argv[1]]()
