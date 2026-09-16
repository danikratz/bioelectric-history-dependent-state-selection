"""Descriptive paired contrasts and figures; no parameter search or simulations."""
import sys
sys.dont_write_bytecode=True
import csv,json,datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap,BoundaryNorm
from matplotlib.patches import Patch
from modelo import *

CATS=['repouso','memoria_localizada','recrutamento_coletivo','transiente_sem_persistencia','indeterminada']
LABELS=['Repouso','Memória localizada','Coletivo persistente','Transiente','Indeterminada']
COLORS=['#dce6ed','#ecad4b','#25887d','#b49aca','#de6471']

def csvwrite(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rows])

def main():
    rows=[json.loads(s) for s in (ROOT/'resultados_conferidos_validacao.jsonl').read_text().splitlines()]; assert len(rows)==136
    byid={r['id']:r for r in rows}; data=np.load(ROOT/'geometrias.npz'); states={}
    for r in rows:
        with np.load(ROOT/r['effective_source']/(r['id']+'.npz')) as z:states[r['id']]=z['y'][:226,-1]
    def select(**kw):return [r for r in rows if all(r.get(k)==v for k,v in kw.items())]
    def intact(r):return select(geometry=r['geometry'],model=r['model'],gd=r['gd'],factor=r['factor'],history='original')[0]
    def compare(r):
        a=intact(r); same=bool(np.array_equal(setup(r)[0][-1][1],setup(a)[0][-1][1]));distance=float(abs(states[r['id']]-states[a['id']]).max())
        valid=all(x['numerically_accepted'] and x['stationary'] and x['linearly_stable'] for x in [r,a])
        return dict(id=r['id'],intact_id=a['id'],geometry=r['geometry'],model=r['model'],gd=r['gd'],factor=r['factor'],history=r['history'],restore_s=r['restore_s'],same_final_graph=same,accepted_stable_pair=bool(valid),intact_category=a['category'],restored_category=r['category'],intact_target_high=a['target_high'],restored_target_high=r['target_high'],target_count=r['target_count'],intact_total_high=a['total_high'],restored_total_high=r['total_high'],max_final_voltage_difference_V=distance,target_fraction_difference=r['target_high_fraction']-a['target_high_fraction'],history_dependence=bool(same and valid and distance>.001))
    geometries=[compare(r) for r in rows if 1 in r['blocks'] and r['model']=='bistable' and r['history']=='interface' and not r['controls']]
    regime=[compare(r) for r in rows if 2 in r['blocks'] and r['history']=='interface']
    alternative=[compare(r) for r in rows if 3 in r['blocks'] and r['model']=='cubic' and r['history']=='interface' and not r['controls']]
    randoms=[compare(r) for r in rows if r['history']=='random']
    assert len(geometries)==15 and len(regime)==42 and len(alternative)==12
    controls=[r for r in rows if r['controls'] or r['history']=='random']
    for name,rr in [('metricas_validacao.csv',rows),('generalizacao_geometrias.csv',geometries),('mapa_regime.csv',regime),('comparacao_mecanismos.csv',alternative),('controles_validacao.csv',controls),('contrastes_aleatorios.csv',randoms)]:csvwrite(name,rr)
    write('mapa_regime.json',dict(gD=P['gD_grid'],restore_s=P['restoration_grid_s'],factor=.9,pairs=regime,no_interpolated_phase_boundary=True))
    result=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_pairs=geometries,regime_pairs=regime,alternative_pairs=alternative,random_pairs=randoms,network_classification_counts={k:sum(r['category']==k for r in rows) for k in CATS},history_dependence_counts=dict(geometry=sum(x['history_dependence'] for x in geometries),regime=sum(x['history_dependence'] for x in regime),alternative=sum(x['history_dependence'] for x in alternative)),geometries_with_difference=[g['name'] for g in P['geometries'] if any(r['geometry']==g['name'] and r['history_dependence'] for r in geometries)],control_counts={k:sum(k in r['controls'] for r in rows) for k in ['no_stimulus','no_additional_current','never_restore']},no_stimulus_max_departure_V=max(r['final_max_departure_V'] for r in rows if 'no_stimulus' in r['controls']),ablation_final_categories={r['id']:r['category'] for r in rows if 'no_additional_current' in r['controls']},classification_changes_2s_5s=[r['id'] for r in rows if r['category']!=r['category_2s']],max_change_2s_5s_V=max(r['max_voltage_change_2_to_5s_V'] for r in rows),no_pvalues=True)
    write('resumo_validacao.json',result)
    # Preserve isolated gate snapshot before augmenting the requested mechanism file.
    mechpath=ROOT/'mecanismo_alternativo.json';m=json.loads(mechpath.read_text())
    if not (ROOT/'mecanismo_isolado_antes_rede.json').exists():(ROOT/'mecanismo_isolado_antes_rede.json').write_bytes(mechpath.read_bytes())
    m.update(network_test_started=True,network_test_completed=True,network_pairs=alternative,network_history_dependence_count=sum(r['history_dependence'] for r in alternative));write('mecanismo_alternativo.json',m)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
    # A: every geometry at the prespecified 0.9 stimulus, no witness selection.
    fig,axes=plt.subplots(5,3,figsize=(12,15),layout='constrained')
    for i,g in enumerate(P['geometries']):
        name=g['name'];xy=data[name+'_xy'];adj=data[name+'_original'];ee=np.argwhere(np.triu(adj)>0);cut=np.array(g['interface_edges']);source=g['source']
        pair=next(r for r in geometries if r['geometry']==name and r['factor']==.9)
        for j,ax in enumerate(axes[i]):
            ax.add_collection(LineCollection(xy[ee],colors='#aab7be',linewidths=.35,alpha=.65))
            if j==0:
                ax.add_collection(LineCollection(xy[cut],colors='#bb454d',linewidths=1.1));ax.scatter(xy[:,0],xy[:,1],c=np.where(data[name+'_right'],'#cedce4','#6c889b'),s=10)
                title=f"{name}\nfonte {source}; {g['targets']} receptores; {len(cut)} arestas"
            else:
                key=pair['intact_id'] if j==1 else pair['id'];v=states[key]
                im=ax.scatter(xy[:,0],xy[:,1],c=v*1000,cmap='viridis',vmin=-52,vmax=10,s=17)
                r=byid[key];title=f"{'Intacta' if j==1 else 'Interface → restauração 500 ms'}\n{r['target_high']}/{r['target_count']} receptores altos; {r['total_high']}/226 nós"
            ax.scatter(*xy[source],marker='*',s=110,facecolors='#ee7147',edgecolors='black',linewidths=.5,zorder=5)
            ax.set_title(title,fontsize=10);ax.set_aspect('equal');ax.autoscale();ax.set_xticks([]);ax.set_yticks([])
    fig.colorbar(im,ax=axes[:,1:].ravel().tolist(),shrink=.65,label='Voltagem final aos 5 s (mV)')
    fig.suptitle('A — Generalização de geometria e fonte | pulso fixo 0,9×\nTodas as configurações pré-definidas; mesmas conexões finais em cada par',fontsize=14)
    fig.savefig(ROOT/'fig_generalizacao_geometrias.png',dpi=160);plt.close(fig)
    # B: discrete sampled map, no interpolation across unsampled parameters.
    gs=P['gD_grid'];times=P['restoration_grid_s'];mat=np.zeros((7,6),int);base=np.zeros((7,1),int);diff=np.zeros((7,6));hist=np.zeros((7,6),bool)
    for i,gd in enumerate(gs):
        for j,time in enumerate(times):
            r=next(r for r in regime if r['gd']==gd and r['restore_s']==time);mat[i,j]=CATS.index(r['restored_category']);base[i,0]=CATS.index(r['intact_category']);diff[i,j]=r['max_final_voltage_difference_V']*1000;hist[i,j]=r['history_dependence']
    fig,axes=plt.subplots(1,3,figsize=(12,5.7),gridspec_kw={'width_ratios':[1,5,5]},layout='constrained');cmap=ListedColormap(COLORS);norm=BoundaryNorm(np.arange(6)-.5,5)
    for ax,z in zip(axes[:2],[base,mat]):ax.imshow(z,cmap=cmap,norm=norm,aspect='auto',origin='lower');ax.set_yticks(range(7),[f'{g:g}' for g in gs]);ax.set_ylabel('gD (S/m²)')
    axes[0].set_xticks([0],['Intacta']);axes[0].set_title('Referência')
    axes[1].set_xticks(range(6),[str(int(t*1000)) for t in times]);axes[1].set(title='Após restaurar a interface',xlabel='Restauração (ms)')
    im=axes[2].imshow(diff,cmap='YlGnBu',aspect='auto',origin='lower',vmin=0);axes[2].set_xticks(range(6),[str(int(t*1000)) for t in times]);axes[2].set_yticks(range(7),[f'{g:g}' for g in gs]);axes[2].set(title='Diferença final em relação à intacta',xlabel='Restauração (ms)')
    for i in range(7):
        for j in range(6):axes[2].text(j,i,f'{diff[i,j]:.1f}'+('*' if hist[i,j] else ''),ha='center',va='center',fontsize=9,color='white' if diff[i,j]>diff.max()*.6 else '#172b36')
    fig.colorbar(im,ax=axes[2],label='Máx. |ΔV por nó| (mV)',shrink=.8)
    fig.legend(handles=[Patch(color=c,label=l) for c,l in zip(COLORS,LABELS)],loc='outside lower center',ncol=3,fontsize=9)
    fig.suptitle('B — Mapa discreto | estímulo fixo 0,9× | estados aos 5 s\n* Par estável e diferença >1 mV; a grade não determina fronteiras contínuas',fontsize=13)
    fig.savefig(ROOT/'fig_mapa_regime.png',dpi=180);plt.close(fig)
    # C: different current laws on their own current scales; equivalent network pulse.
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained');v=np.linspace(-.065,.02,900)
    for j,name in enumerate(['bistable','cubic']):
        rts=old.Model('bistable',4.).roots() if j==0 else np.array([L,U,H]);cur=old.Model('bistable',4.).steady_current(v) if j==0 else -old.C*cubic(v)
        ax=axes[0,j];ax.plot(v*1000,cur,color='#245e78');ax.axhline(0,color='#888',lw=.6)
        ax.scatter(rts[[0,2]]*1000,[0,0],c='#25887d',s=60,zorder=3,label='Equilíbrios estáveis');ax.scatter(rts[1]*1000,0,facecolors='white',edgecolors='#b44549',s=60,zorder=3,label='Equilíbrio instável')
        ax.set(title='Corrente sigmoidal + Kv' if j==0 else 'Corrente líquida cúbica (escalar)',xlabel='Voltagem isolada (mV)',ylabel='Corrente estacionária requerida (A/m²)');ax.legend(fontsize=8);ax.grid(alpha=.15)
        ax=axes[1,j];xx=np.arange(3);fa=[.9,1.,1.1]
        aa=[select(geometry='historica',model=name,gd=4. if j==0 else 0.,factor=f,history='original')[0] for f in fa]
        bb=[select(geometry='historica',model=name,gd=4. if j==0 else 0.,factor=f,history='interface',restore_s=.5)[0] for f in fa]
        ax.bar(xx-.18,[r['target_high_fraction']*100 for r in aa],.36,color='#718b9e',label='Intacta');ax.bar(xx+.18,[r['target_high_fraction']*100 for r in bb],.36,color='#25887d',label='Interface restaurada')
        for k,(a,b) in enumerate(zip(aa,bb)):ax.text(k,104,f"{a['target_high']} → {b['target_high']}",ha='center',fontsize=10)
        ax.set_xticks(xx,[f'{f:g}×' for f in fa]);ax.set(ylim=(0,118),xlabel='Mesmo estímulo absoluto ancorado no modelo anterior',ylabel='Receptores altos aos 5 s (%)',title='Rede original; restauração 500 ms; números = receptores/104')
    handles,labels=axes[1,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=2,fontsize=9)
    fig.suptitle('C — Bistabilidade isolada e seleção de estado na rede são perguntas distintas',fontsize=14)
    fig.savefig(ROOT/'fig_mecanismo_alternativo.png',dpi=180);plt.close(fig)
    print('ANALYZED',result['history_dependence_counts'],result['geometries_with_difference'],flush=True)
if __name__=='__main__':main()
