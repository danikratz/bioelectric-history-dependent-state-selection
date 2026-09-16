"""Preserve original failures; correct only numerical precision, never thresholds.

For each failed primary refinement check, compare two finer DOP853 solutions and
an independent Radau solution. Write a separately labelled effective dataset.
"""
import csv
import json
import numpy as np
from core import *
from experimento import load_protocol,execute_case,writejson


def main():
    p=load_protocol();v=json.loads((ROOT/'verificacao.json').read_text())
    failed={x['id'] for x in v['refinement']+v['radau'] if not x['passed']}
    cases={x['id']:x for x in p['all_conditions']}
    rows=[json.loads(x) for x in (ROOT/'resultados.jsonl').read_text().splitlines()]
    replacements={};records=[];folder=ROOT/'precisao_corrigida';folder.mkdir(exist_ok=True)
    for key in sorted(failed):
        case=cases[key]
        model,seg,thr,t,fine,_=execute_case(case,p['verification_solver'])
        _,_,_,th,high,check=execute_case(case,dict(method='DOP853',rtol=1e-12,atol=1e-14,max_step=.001))
        _,_,_,tr,radau,_=execute_case(case,dict(method='Radau',rtol=1e-11,atol=1e-13,max_step=.0025))
        err=float(abs(high[:N]-fine[:N]).max());erref=float(abs(high[:N]-radau[:N]).max())
        mh=metrics(model,th,high,seg,case['gap'],thr);mf=metrics(model,t,fine,seg,case['gap'],thr);mr=metrics(model,tr,radau,seg,case['gap'],thr)
        same=all(mh[k]==mf[k]==mr[k] for k in ['target_final_fraction','target_ever_fraction'])
        passed=err<p['voltage_tolerance_V'] and erref<p['voltage_tolerance_V'] and same
        records.append(dict(id=key,fine_vs_high_V=err,radau_vs_high_V=erref,classification_agrees=same,passed=bool(passed)))
        replacements[key]=dict(**case,**mh,**check,numerical_correction=True)
        np.savez_compressed(folder/(key+'.npz'),t=th,y=high,radau=radau)
        print('precision',key,passed,err,erref,flush=True)
    effective=[replacements.get(x['id'],x) for x in rows]
    allpass=all(x['passed'] for x in records) and all(x['passed'] for x in v['refinement']+v['radau'] if x['id'] not in failed)
    writejson(ROOT/'correcao_numerica.json',dict(original_failed_cases=sorted(failed),checks=records,passed=allpass,
               method='No tolerance relaxation, no changed model/stimulus/selection. Original outputs retained; corrected higher-precision outputs separately labelled.'))
    with (ROOT/'resultados_conferidos.jsonl').open('w') as f:
        for row in effective:f.write(json.dumps(row,allow_nan=False)+'\n')
    fields=list(dict.fromkeys(k for row in effective for k in row))
    with (ROOT/'metricas_conferidas.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(effective)
    print('Final precision acceptance',allpass);assert allpass


if __name__=='__main__':main()
