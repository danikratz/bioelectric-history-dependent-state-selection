"""English figures from archived arrays only: no model imports or integration."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
PUB=Path(__file__).resolve().parents[1];BASE=PUB/'study'
MAIN=BASE/'transmissao_memoria_histerese';OUT=PUB/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':220})
with np.load(MAIN/'histerese_trajetorias.npz') as z:
    fig,axs=plt.subplots(1,3,figsize=(13,3.9),layout='constrained')
    for ax,name,title in zip(axs[:2],['kv','bistable'],['A  Graded potassium model','B  Persistent regenerative model']):
        for leg,color in zip([.2,1.,5.],['#B6BDC9','#548BB5','#102F43']):
            a=z[f'{name}_{leg}'];ax.plot(a[:,1],a[:,2]*1000,label=f'{leg:g} s / ramp leg',color=color,lw=1.5)
        ax.set(xlabel='Applied current density (A/m²)',ylabel='Membrane potential (mV)',title=title);ax.legend(fontsize=8)
    eq=json.loads((MAIN/'equilibrios.json').read_text())
    for x,name in enumerate(['kv','bistable']):
        for r in eq[name]:
            stable=r['max_real_eigenvalue_s_inv']<0
            axs[2].scatter(x,r['V']*1000,c='#0A716C' if stable else '#C56633',marker='o' if stable else 'x',s=75,zorder=3)
    axs[2].set(xticks=[0,1],xticklabels=['Graded','Persistent'],xlim=(-.5,1.5),ylabel='Zero-current equilibrium (mV)',title='C  Coexistence at identical input')
    axs[2].text(.04,.96,'● stable    × unstable',transform=axs[2].transAxes,va='top',fontsize=9)
    fig.suptitle('Local dynamics: finite-rate loops and equilibrium structure',fontsize=13)
    fig.savefig(OUT/'fig1_hysteresis_equilibria.png');fig.savefig(OUT/'fig1_hysteresis_equilibria.svg');plt.close(fig)
with np.load(BASE/'sorteio_independente_32/topologias.npz') as z:
    xy=z['xy'];adj=z['original'];right=z['right'];source=int(z['center'])
edges=np.argwhere(np.triu(adj)>0);segments=xy[edges]
fig=plt.figure(figsize=(12,7.2),layout='constrained');gs=fig.add_gridspec(2,3,height_ratios=[1,1.1]);a=fig.add_subplot(gs[0,:]);maps=[fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1])];b=fig.add_subplot(gs[1,2])
t=np.array([0,.499999,.5,2.]);a.step(t,[1,1,1,1],where='post',color='#345A80',label='Intact throughout',lw=2);a.step(t,[.1,.1,1,1],where='post',color='#BE7139',label='Interface weakened, then restored',lw=2)
a.axvspan(0,.02,color='#6D8B80',alpha=.25,label='Identical 20 ms stimulus');a.axvline(.5,color='.5',ls=':');a.set(ylim=(0,1.15),xlabel='Time (s)',ylabel='Interface edge weight',title='A  Different histories; all original weights restored at 0.5 s');a.legend(loc='lower right',fontsize=9)
for ax,case,label,color in zip(maps,['case0147','case0159'],['B  Intact: 0/104 receivers high','C  Restored: 104/104 receivers high'],['#345A80','#BE7139']):
    with np.load(MAIN/(case+'.npz')) as z:tt=z['t'];v=z['y'][:226]
    ax.add_collection(LineCollection(segments,colors='#CDD1D3',lw=.35,zorder=0));sc=ax.scatter(*xy.T,c=v[:,-1]*1000,cmap='viridis',vmin=-52,vmax=8,s=18);ax.scatter(*xy[source],marker='*',s=85,facecolors='none',edgecolors='black');ax.set_title(label,fontsize=10);ax.set_aspect('equal');ax.axis('off')
    b.plot(tt,v[right].mean(0)*1000,color=color,label='Intact' if case=='case0147' else 'Restored',lw=1.8)
b.axvline(.5,color='.5',ls=':');b.set(xlabel='Time (s)',ylabel='Mean receiver voltage (mV)',title='D  Distinct stable endpoints');b.legend(fontsize=9)
fig.colorbar(sc,ax=maps,shrink=.75,pad=.01,label='Final voltage (mV)');fig.suptitle('Identical final weighted graph, different final electrical state',fontsize=14)
fig.savefig(OUT/'fig2_identical_final_graph.png');fig.savefig(OUT/'fig2_identical_final_graph.svg');plt.close(fig)
print('Two figures regenerated from archived data; no simulations.')
