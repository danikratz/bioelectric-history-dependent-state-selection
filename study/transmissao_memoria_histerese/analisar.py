"""Descriptive contrasts and exportable figures; no parameter fitting."""
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core import *


def main():
    datafile=ROOT/'resultados_conferidos.jsonl'
    if not datafile.exists():datafile=ROOT/'resultados.jsonl'
    rows=[json.loads(x) for x in datafile.read_text().splitlines()]
    assert len(rows)==len(json.loads((ROOT/'protocolo.json').read_text())['all_conditions'])
    def select(**kw):return [r for r in rows if all(r.get(k)==v for k,v in kw.items())]
    names=list(GRAPHS);labels=['Original','Interface 10%','Aleatório 11','Aleatório 22','Aleatório 33','Corte total']
    colors=['#3f5368','#c64b47','#228b8d','#519963','#a78328','#606060']
    temporal=[];memory=[];repair=[]
    for r in select(stage='temporal'):
        original=select(stage='temporal',graph='original',tau=r['tau'],gap=r['gap'],dose=r['dose'],pulse_s=r['pulse_s'])[0]
        temporal.append(dict(id=r['id'],graph=r['graph'],tau_s=r['tau'],gap=r['gap'],dose=r['dose'],pulse_s=r['pulse_s'],
                             peak_retained_percent=100*r['peak_mV']/original['peak_mV'],
                             area_retained_percent=100*r['positive_area_mV_s']/original['positive_area_mV_s'],
                             peak_delay_ms=1000*(r['time_peak_s']-original['time_peak_s']),
                             centroid_delay_ms=1000*(r['positive_centroid_s']-original['positive_centroid_s']) if r['positive_centroid_s'] is not None and original['positive_centroid_s'] is not None else None))
    for r in select(stage='memory'):
        original=select(stage='memory',graph='original',model=r['model'],amplitude_factor=r['amplitude_factor'],restore_s=r['restore_s'])[0]
        memory.append(dict(id=r['id'],model=r['model'],graph=r['graph'],factor=r['amplitude_factor'],restore_s=r['restore_s'],
                           target_final_fraction=r['target_final_fraction'],target_ever_fraction=r['target_ever_fraction'],
                           final_fraction_difference=r['target_final_fraction']-original['target_final_fraction'],
                           ever_fraction_difference=r['target_ever_fraction']-original['target_ever_fraction'],
                           final_voltage_difference_mV=r['final_mean_mV']-original['final_mean_mV']))
    for model in MODELS:
        metric='target_final_fraction' if model=='bistable' else 'target_ever_fraction' if model=='excitable' else 'peak_mV'
        for factor in [.9,1.,1.1]:
            for budget in [4,8,16]:
                d=select(stage='repair',model=model,amplitude_factor=factor,budget_edges=budget,strategy='directed')[0]
                random=[select(stage='repair',model=model,amplitude_factor=factor,budget_edges=budget,strategy=f'random{s}')[0] for s in [11,22,33]]
                repair.append(dict(model=model,factor=factor,budget=budget,metric=metric,directed=d[metric],
                                   random_min=min(x[metric] for x in random),random_max=max(x[metric] for x in random),
                                   difference_vs_each_random=[d[metric]-x[metric] for x in random]))
    summary=dict(temporal=temporal,memory=memory,repair=repair)
    (ROOT/'contrastes.json').write_text(json.dumps(summary,indent=2)+'\n')
    for name,data in [('contrastes_temporais',temporal),('contrastes_memoria',memory)]:
        with (ROOT/(name+'.csv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)

    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    hyst=np.load(ROOT/'histerese_trajetorias.npz')
    for ax,model,title in zip(axes,['kv','bistable'],['Kv1.5: laço por atraso','Extensão persistente: histerese']):
        for leg,color in zip([.2,1.,5.],['#c3ced8','#5a8cb2','#163a5b']):
            z=hyst[f'{model}_{leg}'];ax.plot(z[:,1],z[:,2]*1000,label=f'{leg:g} s por sentido',color=color)
        ax.set(xlabel='Corrente aplicada (A/m²)',ylabel='Voltagem (mV)',title=title);ax.grid(alpha=.15);ax.legend(fontsize=8)
    fig.suptitle('Diagnóstico sintético — a coexistência de repousos confirma a memória')
    fig.savefig(ROOT/'01_histerese.png',dpi=180);plt.close(fig)

    fig,axes=plt.subplots(2,3,figsize=(13,7),layout='constrained')
    for rownum,model in enumerate(['bistable','excitable']):
        field='target_final_fraction' if model=='bistable' else 'target_ever_fraction'
        for col,factor in enumerate([.9,1.,1.1]):
            matrix=np.array([[select(stage='memory',model=model,graph=name,amplitude_factor=factor,restore_s=duration)[0][field] for name in names] for duration in [.02,.05,.2,.5]])
            ax=axes[rownum,col];im=ax.imshow(matrix,vmin=0,vmax=1,cmap='YlGnBu',aspect='auto')
            ax.set_xticks(range(6),['Orig.','Int.','A11','A22','A33','Corte'],rotation=35,ha='right')
            ax.set_yticks(range(4),['20','50','200','500']);ax.set_ylabel('Restauração (ms)')
            ax.set_title(f'{model} | estímulo {factor:g} × limiar original')
            for i in range(4):
                for j in range(6):ax.text(j,i,f'{matrix[i,j]*100:.0f}',ha='center',va='center',color='white' if matrix[i,j]>.55 else '#20252b',fontsize=9)
    fig.colorbar(im,ax=axes,label='Fração dos 104 receptores')
    fig.suptitle('Acima: estado final aos 2 s. Abaixo: cruzamento de limiar até 2 s.\nValores nas células em %; cruzar o limiar não basta para provar uma excursão regenerativa.')
    fig.savefig(ROOT/'02_memoria_recrutamento.png',dpi=180);plt.close(fig)

    fig,axes=plt.subplots(1,3,figsize=(13,4),layout='constrained')
    compactdata=np.load(ROOT/'respostas_compactas.npz')
    for ax,model in zip(axes,['kv','bistable','excitable']):
        for name,label,color in zip(names,labels,colors):
            if model=='kv':r=select(stage='temporal',graph=name,tau=.0148,gap=1.,pulse_s=.01,dose='equal_charge')[0]
            else:r=select(stage='memory',model=model,graph=name,amplitude_factor=.9,restore_s=.5)[0]
            z=compactdata[r['id']];ax.plot(z[:,0]*1000,z[:,1],color=color,label=label,lw=1.3)
        ax.set(title=model,xlabel='Tempo (ms)',ylabel='ΔV médio dos receptores (mV)');ax.set_xlim(0,800 if model!='kv' else 300);ax.grid(alpha=.15)
    axes[0].legend(fontsize=7)
    fig.suptitle('Exemplos fixados: protocolos distintos entre o braço graduado e as extensões')
    fig.savefig(ROOT/'03_trajetorias.png',dpi=180);plt.close(fig)

    fig,axes=plt.subplots(3,3,figsize=(12,10),layout='constrained')
    for i,model in enumerate(MODELS):
        field='target_final_fraction' if model=='bistable' else 'target_ever_fraction' if model=='excitable' else 'peak_mV'
        for j,factor in enumerate([.9,1.,1.1]):
            ax=axes[i,j]
            for strategy,color in [('directed','#c64b47'),('random11','#228b8d'),('random22','#519963'),('random33','#a78328')]:
                entries=[select(stage='repair',model=model,amplitude_factor=factor,budget_edges=b,strategy=strategy)[0] for b in [4,8,16]]
                base=select(stage='repair',model=model,amplitude_factor=factor,strategy='none')[0]
                full=select(stage='repair',model=model,amplitude_factor=factor,strategy='full')[0]
                ax.plot([0,4,8,16,32],[base[field]]+[r[field] for r in entries]+[full[field]],'-o',ms=3,color=color,label=strategy)
            ax.set(title=f'{model} | {factor:g} × estímulo de referência',xlabel='Arestas reparadas',ylabel='Pico médio (mV)' if model=='kv' else 'Fração final' if model=='bistable' else 'Fração recrutada');ax.grid(alpha=.15)
    axes[0,0].legend(fontsize=7)
    fig.suptitle('Reparo antes do pulso, mesma condutância adicionada por orçamento\nConectar mais pode elevar a carga elétrica enfrentada pela fonte')
    fig.savefig(ROOT/'04_reparos.png',dpi=180);plt.close(fig)
    print('Contrasts and 4 figures saved',flush=True)


if __name__=='__main__':main()
