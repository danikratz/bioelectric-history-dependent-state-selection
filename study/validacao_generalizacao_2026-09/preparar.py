"""Read-only previous-study audit, deterministic geometry construction and freeze.
No new dynamics are evaluated by this script.
"""
import sys
sys.dont_write_bytecode = True
import csv, json, hashlib, datetime, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import connected_components
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'transmissao_memoria_histerese'
sys.path.insert(0,str(OLD))
import core as old

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data): (ROOT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def audit():
    manifest=json.loads((OLD/'MANIFESTO_SHA256.json').read_text())
    for k,v in manifest.items(): assert sha(OLD/k)==v,k
    p=json.loads((OLD/'protocolo.json').read_text())
    for k,v in p['source_sha256'].items(): assert sha(ROOT.parent/k)==v,k
    rows=[json.loads(x) for x in (OLD/'resultados_conferidos.jsonl').read_text().splitlines()]
    csvrows=list(csv.DictReader((OLD/'metricas_conferidas.csv').open()))
    assert len(rows)==len(csvrows)==487
    errors=[]
    for r,c in zip(rows,csvrows):
        for k,v in r.items(): assert c[k]==('' if v is None else str(v)),(r['id'],k)
        path=OLD/'precisao_corrigida'/(r['id']+'.npz')
        if not path.exists(): path=OLD/(r['id']+'.npz')
        with np.load(path) as z:
            v=z['y'][:old.N]; rest=old.Model(r['model'],r['gd'],r['tau']).roots()[0]
            errors.append(abs(float(((v[old.RIGHT].mean(0)-rest)*1000).max())-r['peak_mV']))
            threshold=old.Model('bistable',r['gd'] if r['gd'] else 4).roots()[1]
            assert float((v[old.RIGHT,-1]>threshold).mean())==r['target_final_fraction']
    assert max(errors)==0
    for fn in ['correcao_numerica','verificacao_mecanismos','controles_adicionais','referencias_adicionais','estados_espaciais']:
        assert json.loads((OLD/(fn+'.json')).read_text())['passed']
    # Verify every stored contrast against the effective rows, including repair.
    contrast=json.loads((OLD/'contrastes.json').read_text()); byid={r['id']:r for r in rows}
    for c in contrast['memory']:
        r=byid[c['id']]
        assert c['target_final_fraction']==r['target_final_fraction']
    for c in contrast['repair']:
        metric=c['metric']; selected=[r for r in rows if r['stage']=='repair' and r['model']==c['model'] and r['amplitude_factor']==c['factor'] and r['budget_edges']==c['budget']]
        d=next(r for r in selected if r['strategy']=='directed')
        rr=[next(r for r in selected if r['strategy']==f'random{s}') for s in [11,22,33]]
        assert [d[metric]-r[metric] for r in rr]==c['difference_vs_each_random']
    # Include bytecode and manifest itself in the preservation snapshot.
    snapshot={str(p.relative_to(OLD)):sha(p) for p in sorted(OLD.rglob('*')) if p.is_file()}
    write('originais_sha256.json',snapshot)
    write('auditoria_previa.json',dict(utc=now(),conditions=487,manifest_files=len(manifest),all_old_files=len(snapshot),max_recomputed_peak_error_mV=max(errors),csv_jsonl_all_fields_equal=True,all_final_fractions_recomputed=True,repair_contrasts_recomputed=True,old_initial_precision_failure_preserved=True,passed=True,reuse=['core.Model','core.functions','core.lap','core.C/GL/EL/EK/GK/ED/f/a'],not_reused={'protocol_segments':'Hard-coded ORIGINAL and N; new graphs require explicit final graph.','metrics/compact':'Hard-coded RIGHT/CENTER; new masks require explicit arguments.'},proven_old_bug_found=False,scope='Archived trajectory reanalysis, no old reruns; all prior JSON and JSONL records parsed.'))

def topology(xy):
    candidates=set()
    for tri in Delaunay(xy).simplices:
        for i,j in [(tri[0],tri[1]),(tri[0],tri[2]),(tri[1],tri[2])]: candidates.add(tuple(sorted((int(i),int(j)))))
    edges=sorted(candidates,key=lambda e:(float(np.linalg.norm(xy[e[0]]-xy[e[1]])),e))
    assert len(edges)>=622, 'Geometry construction fails without resampling'
    parent=list(range(226))
    def find(i):
        while parent[i]!=i: parent[i]=parent[parent[i]];i=parent[i]
        return i
    selected=[]
    for i,j in edges:
        ri,rj=find(i),find(j)
        if ri!=rj: parent[ri]=rj; selected.append((i,j))
    chosen=set(selected)
    selected+= [e for e in edges if e not in chosen][:622-len(selected)]
    adj=np.zeros((226,226))
    for i,j in selected: adj[i,j]=adj[j,i]=1
    assert connected_components(scipy.sparse.csr_matrix(adj))[0]==1
    return adj

def main():
    assert not (ROOT/'protocolo_validacao.json').exists(), 'Never overwrite frozen protocol'
    audit()
    xy=old.XY.copy();adj=old.ORIGINAL.copy()
    edges=np.argwhere(np.triu(adj)>0)
    spacing=float(np.median(np.linalg.norm(xy[edges[:,0]]-xy[edges[:,1]],axis=1)))
    variants=[('historica',xy,adj,old.CENTER,1,None)]
    for label,q,direction in [('fonte_esquerda',.2,1),('fonte_direita',.8,-1)]:
        target=np.array([np.quantile(xy[:,0],q),np.median(xy[:,1])])
        source=int(np.argmin(((xy-target)**2).sum(1)))
        variants.append((label,xy,adj,source,direction,None))
    for seed in [1701,2701]:
        rng=np.random.default_rng(seed)
        coords=xy+rng.normal(0,.1*spacing,xy.shape)
        g=topology(coords); source=int(np.argmin(((coords-coords.mean(0))**2).sum(1)))
        variants.append((f'geometria_{seed}',coords,g,source,1,seed))
    geometries=[]; arrays={}
    for idx,(name,coords,g,source,direction,seed) in enumerate(variants):
        length=float(np.median(np.linalg.norm(coords[g[source]>0]-coords[source],axis=1)))
        right=direction*(coords[:,0]-coords[source,0])>.1*length
        cut=np.argwhere(np.triu(g*(right[:,None]!=right[None,:]))>0)
        weak=g.copy(); weak[right[:,None]!=right[None,:]]*=.1
        rng=np.random.default_rng(np.random.SeedSequence([20260915,1,idx]))
        all_edges=np.argwhere(np.triu(g)>0)
        random_edges=all_edges[rng.choice(len(all_edges),len(cut),replace=False)]
        rand=g.copy()
        for i,j in random_edges: rand[i,j]=rand[j,i]=.1
        if idx==0: assert np.array_equal(right,old.RIGHT) and np.array_equal(weak,old.GRAPHS['interface_10pct'])
        for key,val in dict(xy=coords,original=g,interface=weak,random=rand,right=right).items():arrays[name+'_'+key]=val
        geometries.append(dict(name=name,source=source,direction_x=direction,geometry_seed=seed,random_seed_sequence=[20260915,1,idx],nodes=226,edges=622,targets=int(right.sum()),interface_edges=cut.tolist(),random_edges=random_edges.tolist(),removed_weight=.9*len(cut),source_degree=int(g[source].sum()),degree_min=int(g.sum(1).min()),degree_max=int(g.sum(1).max()),median_edge_length=float(np.median(np.linalg.norm(coords[all_edges[:,0]]-coords[all_edges[:,1]],axis=1)))))
    np.savez_compressed(ROOT/'geometrias.npz',**arrays)
    anchor=json.loads((OLD/'desenvolvimento.json').read_text())['selected']['bistable']['threshold_upper_A_m2']
    cases=[];index={}; memberships=[]
    def add(block,geometry='historica',model='bistable',gd=4.,factor=.9,history='interface',restore=.5,control=None):
        # Restoration time has no physical meaning for the always intact graph.
        if history=='original':restore=None
        spec=dict(geometry=geometry,model=model,gd=gd,factor=factor,amplitude_A_m2=anchor*factor,history=history,restore_s=restore,pulse_s=.02,end_s=5.)
        key=json.dumps(spec,sort_keys=True)
        if key not in index:
            index[key]=len(cases); cases.append(dict(id=f'v{len(cases):04d}',**spec,blocks=[],controls=[]))
        c=cases[index[key]]
        if block not in c['blocks']:c['blocks'].append(block)
        if control and control not in c['controls']:c['controls'].append(control)
        memberships.append(dict(block=block,id=c['id'],control=control))
    for g in geometries:
        name=g['name']
        for factor in [.9,1.,1.1]:
            for history in ['original','interface','random']:add(1,geometry=name,factor=factor,history=history)
        add(1,geometry=name,factor=0.,control='no_stimulus')
        for history in ['original','interface']:add(1,geometry=name,model='kv',gd=0.,history=history,control='no_additional_current')
        add(1,geometry=name,restore=None,control='never_restore')
    for gd in [3.4,3.6,3.8,4.,4.2,4.4,4.6]:
        add(2,gd=gd,history='original')
        for restore in [.02,.05,.1,.2,.35,.5]:add(2,gd=gd,restore=restore)
    for factor in [.9,1.,1.1]:
        add(3,model='cubic',gd=0.,factor=factor,history='original')
        for restore in [.02,.05,.2,.5]:add(3,model='cubic',gd=0.,factor=factor,restore=restore)
        add(3,model='cubic',gd=0.,factor=factor,history='random')
        add(3,model='cubic',gd=0.,factor=factor,restore=None,control='never_restore')
    add(3,model='cubic',gd=0.,factor=0.,control='no_stimulus')
    for history in ['original','interface']:add(3,model='leak',gd=0.,history=history,control='no_additional_current')
    assert len(cases)==136 and len(memberships)==138
    refs=[]
    for c in cases:
        if (1 in c['blocks'] and c['model']=='bistable' and c['factor']==.9 and c['history'] in ['original','interface'] and not c['controls']) or (2 in c['blocks'] and c['gd'] in [3.4,4.,4.6] and (c['history']=='original' or c['restore_s'] in [.02,.1,.5])) or 3 in c['blocks']:refs.append(c['id'])
    inputs={str(p.relative_to(ROOT.parent)):sha(p) for p in [OLD/'core.py',OLD/'desenvolvimento.json',ROOT.parent/'primeiro_parametro_publicado/plano.json',ROOT.parent/'sorteio_independente_32/topologias.npz']}
    p=dict(frozen_utc=now(),scope='Final bounded validation: 3 blocks only; stop independent of sign. Local freeze, not external preregistration or blind validation.',geometries=geometries,geometry_rule='Original + two objective quantile sources + Gaussian jitter 0.1 median original edge length seeds1701/2701; Delaunay minimum spanning tree plus shortest remaining edges to 622; no rejection/resampling. Argmin ties use smallest node index.',receiver_rule='direction_x*(x-x_source)>0.1 median source-neighbour distance',interface_weight=.1,source_stimulus='Single source node',anchor_A_m2=anchor,amplitude_factors_block1_and3=[.9,1.,1.1],amplitude_factor_block2=.9,gD_grid=[3.4,3.6,3.8,4.,4.2,4.4,4.6],restoration_grid_s=[.02,.05,.1,.2,.35,.5],constants=dict(C=old.C,GL=old.GL,EL=old.EL,EK=old.EK,GK=old.GK,ED=old.ED,tauK=.0148,Gj=1.),alternative=dict(formula='dV/dt=(V-L)*(V-U)*(H-V)/(tau*(H-L)^2) - Gj*Laplacian(V)/C + I/C',L_V=-.05,U_V=-.035,H_V=.01,tau_s=.003125,interpretation='Scalar phenomenological NET membrane current, replaces leak+Kv+sigmoid. No channel identity; different state dimension. Low isolated slope -80/s chosen near historical -79.22/s before network tests. Zero-current roots chosen as rounded similar voltage scale; not fitting network.',ablation='Remove cubic additional current Jadd=GL*(V-EL)+C*cubic_drift(V), leaving pure leak. This ablation differs from Kv control. No retuning if negative.'),isolated_tests=dict(holds_initial_V=[-.0501,-.0499,.0099,.0101],hold_s=1.,ramp_legs_s=[1.,5.],ramp_current_rule='Analytic fold-current min-0.005 to max+0.005 A/m2; start lowest exact polynomial root; triangular sweep.',conditions=6,analytic_fold_and_linear_stability_before_network=True),primary_solver=dict(method='DOP853',rtol=1e-10,atol=1e-12,max_step=.0025),refined_solver=dict(method='DOP853',rtol=1e-12,atol=1e-14,max_step=.001),radau_solver=dict(method='Radau',rtol=1e-11,atol=1e-13,max_step=.0025),sample_s=.001,voltage_tolerance_V=2e-5,radau_fixed_ids=refs,numerical_rule='Every network trajectory refined; fixed Radau IDs and every failed refinement. Compare max voltage error on same sampled grid, final/ever high counts and category. All isolated tests also refined and Radau. Preserve failures. At most one correction per failed case: DOP853 rtol3e-14 atol3e-16 max_step0.0005 plus Radau rtol1e-12 atol1e-14 max_step0.001; compare with preceding refined and reference without relaxing criterion. Otherwise indeterminate.',classification=dict(high='V strictly above isolated middle root of actual bistable mechanism/gD; ablations use historical gD4 root',stationary_max_dV_V_s=1e-5,stationary_max_gate_derivative_s_inv=1e-4,stable_max_real_eigen_s_inv=-1e-6,rest_max_departure_V=1e-4,collective_min_target_fraction=.5,categories=['repouso','memoria_localizada','recrutamento_coletivo','transiente_sem_persistencia','indeterminada'],rule='Require finite valid state, stationary residual and stable full Jacobian. Within rest tolerance: transient if any node ever above high threshold, else rest. Otherwise collective if >=50% targets high, else localized; record all high counts and full state. Unresolved precision, instability or nonstationarity: indeterminate.',history_difference='Same final graph, both numerically accepted stationary stable states, max per-node final voltage difference >0.001V; report category and continuous differences separately.'),horizon_rule='All networks run to5s. Compare 2s/5s categories and states. No extension beyond5s; unresolved dynamics remain indeterminate.',conditions=cases,memberships=memberships,counts=dict(network_unique=136,block_memberships=138,by_block={'1':65,'2':49,'3':24},isolated=6,total_distinct_initial_conditions=142,fixed_network_Radau=len(refs)),source_sha256=inputs,geometry_sha256=sha(ROOT/'geometrias.npz'),environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),executable=sys.executable),no_pvalues=True,no_additional_blocks=True)
    write('protocolo_validacao.json',p)
    write('congelamento.json',dict(utc=now(),protocol_sha256=sha(ROOT/'protocolo_validacao.json'),network_results_exist=False))
    plan='''# Última validação computacional dirigida\n\nA auditoria leu o estudo anterior e recalculou os 487 picos/frações finais, conferiu CSV/JSONL e contrastes de reparo, fontes congeladas e 583 hashes. Nenhum bug comprovado requer alteração do estudo anterior. Um primeiro comando de inventário tentou tratar JSON-lista como dicionário e falhou; corrigida somente a leitura externa, sem tocar em dados ou rodar dinâmica.\n\n## Desenho congelado\n\n136 condições únicas de rede, 138 participações nos três blocos (65/49/24), mais 6 protocolos isolados. Controle histórico, duas fontes definidas por quantis x20/80% e mediana y, duas geometrias por jitter e Delaunay, sempre226nós/622arestas. Correntes0,9/1/1,1× referência histórica, sem recalibrar. Interface10%, aleatório pareado em número/perda por aresta, sem estímulo, sem restauração e sem corrente adicional. Mapa7gD×6tempos com0,9× e sete controles intactos. Mecanismo alternativo cúbico escalar com raízes−50/−35/+10mV e tau3,125ms; deriva de baixo−80/s. Substitui corrente total, não é canal biológico. Primeiro raízes, autovalores, dobras e6testes isolados, depois rede.\n\nTodos os detalhes, IDs, seeds, nós-fonte, arestas e tolerâncias constam no protocolo JSON, congelado antes de qualquer resultado novo. Reutilizar Model/functions/lap/constantes por importação somente leitura; usar montagem de segmentos e métricas com grafos/máscaras explícitos. Não usar as funções antigas com RIGHT/ORIGINAL fixos nas variantes.\n\n## Critérios e encerramento\n\nCada rede observada5s, refinada DOP853; subconjunto Radau fixo e casos que falharem. Tolerância0,02mV e concordância de classes/contagens. Uma correção de precisão no máximo, em arquivos separados; reprovação não autoriza ajustar parâmetros. Jacobiano completo e resíduo para estado persistente; diferença de história exige >1mV por nó e estados estáveis sob mesmo grafo final. Registrar2s versus5s. Sem inferência populacional, sem p, sem seleção de positivos. Encerrar após os três blocos, mesmo com alternativa negativa. Reparo anterior será discutido separadamente; não há novo bloco de reparo.\n'''
    (ROOT/'PLANO_VALIDACAO.md').write_text(plan+'\nSHA-256 do protocolo: `'+sha(ROOT/'protocolo_validacao.json')+'`.\n')
    write('MANIFESTO_SHA256.json',{str(x.relative_to(ROOT)):sha(x) for x in sorted(ROOT.rglob('*')) if x.is_file() and x.name!='MANIFESTO_SHA256.json'})
    print('FROZEN',sha(ROOT/'protocolo_validacao.json'),p['counts'],flush=True)
    print([(g['name'],g['source'],g['targets'],len(g['interface_edges'])) for g in geometries],flush=True)
if __name__=='__main__':main()
