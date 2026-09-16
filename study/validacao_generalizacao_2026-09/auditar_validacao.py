"""Final read-only trajectory/contrast audit; writes only this validation folder."""
import sys
sys.dont_write_bytecode=True
import csv,json,datetime
import numpy as np
from modelo import *

def main():
    rows=[json.loads(x) for x in (ROOT/'resultados_conferidos_validacao.jsonl').read_text().splitlines()]
    primary=[json.loads(x) for x in (ROOT/'resultados_validacao.jsonl').read_text().splitlines()]
    csvrows=list(csv.DictReader((ROOT/'metricas_validacao.csv').open()))
    planned={r['id'] for r in P['conditions']};assert len(rows)==len(primary)==len(csvrows)==len(planned)==136
    assert {r['id'] for r in rows}=={r['id'] for r in primary}==planned
    checked={};errors=[]
    for r,c in zip(rows,csvrows):
        assert r['id']==c['id']
        for k,v in r.items():
            expected=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else '' if v is None else str(v)
            assert c[k]==expected,(r['id'],k)
        seg,right,source=setup(r)
        with np.load(ROOT/r['effective_source']/(r['id']+'.npz')) as z:
            v=z['y'][:226];t=z['t'];assert np.isfinite(z['y']).all() and t[0]==0 and t[-1]==5
            assert np.array_equal(z['y'][:,0],state(r,226))
            th=r['threshold_V'];assert int((v[right,-1]>th).sum())==r['target_high'];assert int((v[:,-1]>th).sum())==r['total_high']
            assert int((v[right]>th).any(1).sum())==r['target_ever_high'];assert int((v>th).any(1).sum())==r['total_ever_high']
            errors.append(abs(float(v.max())-r['peak_V']));errors.append(abs(float(v[right,-1].mean())-r['target_final_mean_V']))
            hits=np.where((v[right]>th).any(0))[0];assert (float(t[hits[0]]) if len(hits) else None)==r['first_target_recruitment_s']
            checked[r['id']]=v[:,-1]
    assert max(errors)==0
    with np.load(ROOT/'geometrias.npz') as z:
        geometrychecks=[]
        for g in P['geometries']:
            name=g['name'];adj=z[name+'_original'];cut=z[name+'_interface'];rnd=z[name+'_random'];right=z[name+'_right']
            assert adj.shape==(226,226) and np.array_equal(adj,adj.T) and np.count_nonzero(np.triu(adj))==622
            for altered in [cut,rnd]:
                assert np.array_equal(altered,altered.T);delta=np.triu(adj-altered)
                assert np.count_nonzero(delta)==len(g['interface_edges'])
                assert abs(delta.sum()-g['removed_weight'])<1e-12
            assert not right[g['source']]
            geometrychecks.append(dict(name=name,changed_undirected_edges_vs_original=int(np.count_nonzero(np.triu(adj!=old.ORIGINAL))),source=g['source'],targets=int(right.sum())))
    result=json.loads((ROOT/'resumo_validacao.json').read_text());lookup={r['id']:r for r in rows};comparisons=0
    for group in ['geometry_pairs','regime_pairs','alternative_pairs','random_pairs']:
        for pair in result[group]:
            a,b=lookup[pair['intact_id']],lookup[pair['id']]
            assert all(a[k]==b[k] for k in ['geometry','model','gd','factor','amplitude_A_m2','pulse_s','end_s'])
            assert np.array_equal(setup(a)[0][-1][1],setup(b)[0][-1][1]);err=float(abs(checked[a['id']]-checked[b['id']]).max());assert err==pair['max_final_voltage_difference_V']
            assert pair['history_dependence']==(pair['accepted_stable_pair'] and err>.001);comparisons+=1
    snapshot=json.loads((ROOT/'originais_sha256.json').read_text())
    actual={str(x.relative_to(OLD)):digest(x) for x in OLD.rglob('*') if x.is_file()};assert actual==snapshot,'Previous study modified'
    execution=json.loads((ROOT/'execucao_validacao.json').read_text())
    for k,v in execution['code_sha256'].items():assert digest(ROOT/k)==v,k
    # Historical witness regression against saved data, no new old simulation.
    regressions=[]
    for oldid,newid in [('case0147','v0000'),('case0159','v0001')]:
        with np.load(OLD/(oldid+'.npz')) as oldz, np.load(ROOT/lookup[newid]['effective_source']/(newid+'.npz')) as newz:
            mask=newz['t']<=2.;assert np.array_equal(newz['t'][mask],oldz['t']);err=float(abs(newz['y'][:226,mask]-oldz['y'][:226]).max());assert err<2e-5
            regressions.append(dict(old=oldid,new=newid,max_difference_V=err))
    audit=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),conditions=136,isolated_conditions=6,all_csv_jsonl_fields_equal=True,recomputed_high_counts_and_peaks_and_first_recruitment=True,max_metric_recomputation_error_V=max(errors),paired_comparisons_checked=comparisons,geometry_checks=geometrychecks,previous_files_unchanged=len(snapshot),frozen_protocol_unchanged=True,execution_code_unchanged=True,historical_regressions=regressions,passed=True)
    write('AUDITORIA_FINAL_VALIDACAO.json',audit)
    write('MANIFESTO_SHA256.json',{str(x.relative_to(ROOT)):digest(x) for x in sorted(ROOT.rglob('*')) if x.is_file() and x.name!='MANIFESTO_SHA256.json' and '__pycache__' not in x.parts})
    print('AUDIT',json.dumps(audit),flush=True)
if __name__=='__main__':main()
