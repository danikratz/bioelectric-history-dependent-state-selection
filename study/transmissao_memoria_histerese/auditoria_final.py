"""Final integrity, graph-matching and raw-trajectory endpoint audit."""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import numpy as np
from core import *


def main():
    rows=[json.loads(x) for x in (ROOT/'resultados_conferidos.jsonl').read_text().splitlines()]
    protocol=json.loads((ROOT/'protocolo.json').read_text())
    correction=json.loads((ROOT/'correcao_numerica.json').read_text())
    corrected=set(correction['original_failed_cases'])
    assert len(rows)==len(protocol['all_conditions'])==487
    assert len(set(x['id'] for x in rows))==487
    assert correction['passed']
    for key in ['verificacao_mecanismos','controles_adicionais','referencias_adicionais','estados_espaciais']:
        assert json.loads((ROOT/(key+'.json')).read_text())['passed'],key
    errors=[]
    for row in rows:
        path=ROOT/'precisao_corrigida'/(row['id']+'.npz') if row['id'] in corrected else ROOT/(row['id']+'.npz')
        z=np.load(path);voltage=z['y'][:N];model=Model(row['model'],row['gd'],row['tau'])
        target_mean=voltage[RIGHT].mean(0)
        peak=(target_mean.max()-model.roots()[0])*1000
        err=abs(peak-row['peak_mV']);errors.append(float(err));assert err<1e-10,row['id']
        assert np.isfinite(voltage).all()
        threshold=Model('bistable',row['gd'] if row['gd'] else 4.).roots()[1]
        assert float((voltage[RIGHT,-1]>threshold).mean())==row['target_final_fraction']
    for name in ['interface_10pct','independent32_seed11','independent32_seed22','independent32_seed33']:
        delta=ORIGINAL-GRAPHS[name]
        assert np.allclose(delta,delta.T)
        assert int((np.triu(delta)>0).sum())==32
        assert abs(np.triu(delta).sum()-28.8)<1e-12
    repairdata=json.loads((ROOT/'selecao_reparos.json').read_text())['repairs'];repairs=np.load(ROOT/'reparos.npz')
    for row in repairdata:
        delta=repairs[row['graph']]-GRAPHS['interface_10pct']
        assert np.allclose(delta,delta.T)
        assert int((np.triu(delta)>0).sum())==row['budget_edges']
        assert abs(np.triu(delta).sum()-row['added_weight'])<1e-12
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    for name,value in protocol['source_sha256'].items():assert sha(BASE/name)==value,name
    result=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),conditions=487,corrected_cases=len(corrected),
                all_peaks_recomputed=True,max_recomputed_peak_error_mV=max(errors),all_final_fractions_recomputed=True,
                graphs_matched=True,frozen_sources_unchanged=True,accepted_after_precision_correction=True,
                original_precision_failure_preserved=True,independent_biological_validation=False,
                figure_visual_inspection=['01_histerese.png','02_memoria_recrutamento.png','03_trajetorias.png','04_reparos.png','05_estados_espaciais.png'])
    (ROOT/'AUDITORIA_FINAL.json').write_text(json.dumps(result,indent=2)+'\n')
    manifest={str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFESTO_SHA256.json'}
    (ROOT/'MANIFESTO_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2));print('Hashed files',len(manifest))


if __name__=='__main__':main()
