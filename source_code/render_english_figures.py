"""English-only reexport of frozen figures. No integration or new scientific conditions.
Run in an extracted archive: python source_code/render_english_figures.py --study-root study --output english_reexport
The original Portuguese plotting blocks are reused; only Text artists are translated.
GitHub adaptation: optional endpoint cache reads the exact archived final voltage arrays.
The archived renderer without this option is retained under source_code/archived/.
"""
from pathlib import Path
import argparse, json, hashlib, textwrap, types
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from scipy.special import expit
parser=argparse.ArgumentParser();parser.add_argument('--study-root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--endpoint-cache',type=Path,help='Read the explicit frozen endpoint cache instead of full validation trajectories');args=parser.parse_args()
BASE=args.study_root;OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams['svg.fonttype']='none'
translations={
'Kv1.5: laço por atraso':'Kv1.5: kinetic lag',
'Extensão persistente: histerese':'Persistent extension: hysteresis',
'Corrente aplicada (A/m²)':'Applied current density (A/m²)',
'Voltagem (mV)':'Voltage (mV)',
'Diagnóstico sintético — a coexistência de repousos confirma a memória':'Synthetic local dynamics: finite-rate loops and coexisting resting states',
'Orig.':'Intact','Int.':'Interface','A11':'R11','A22':'R22','A33':'R33','Corte':'Cut',
'Restauração (ms)':'Restoration (ms)',
'Fração dos 104 receptores':'Fraction of 104 receivers',
'Acima: estado final aos 2 s. Abaixo: cruzamento de limiar até 2 s.\nValores nas células em %; cruzar o limiar não basta para provar uma excursão regenerativa.':'Top: final state at 2 s. Bottom: threshold crossing by 2 s.\nCell values are percentages; threshold crossing alone does not demonstrate a regenerative excursion.',
'Original':'Intact','Corte total':'Complete cut','Tempo (ms)':'Time (ms)',
'ΔV médio dos receptores (mV)':'Mean receiver ΔV (mV)',
'Exemplos fixados: protocolos distintos entre o braço graduado e as extensões':'Archived examples: graded and regenerative variants use different protocols',
'Arestas reparadas':'Repaired edges','Pico médio (mV)':'Mean peak (mV)',
'Fração final':'Final high-receiver fraction','Fração recrutada':'Fraction ever crossing threshold',
'Reparo antes do pulso, mesma condutância adicionada por orçamento\nConectar mais pode elevar a carga elétrica enfrentada pela fonte':'Repair before stimulation; equal added conductance at each budget\nAdditional connections can increase source loading',
'Repouso antes do pulso':'Rest before stimulation','Rede intacta durante o pulso':'Intact network during stimulation','Interface fraca até 500 ms':'Interface weakened until 500 ms',
'Histórias diferentes, mesmas conexões e parâmetros finais\nPulso de 20 ms no nó marcado; estímulo 0,9 × referência; estados aos 2 s':'Different histories; identical final connections and parameters\n20 ms pulse at the marked node; 0.9 × reference stimulus; states at 2 s',
'Voltagem final aos 5 s (mV)':'Final voltage at 5 s (mV)',
'A — Generalização de geometria e fonte | pulso fixo 0,9×\nTodas as configurações pré-definidas; mesmas conexões finais em cada par':'A — Geometry and source generalization | fixed 0.9× stimulus\nAll prespecified configurations; identical final connections within each pair',
'Intacta':'Intact','Referência':'Reference','Após restaurar a interface':'After interface restoration',
'Diferença final em relação à intacta':'Final difference from intact','Máx. |ΔV por nó| (mV)':'Max. |ΔV across nodes| (mV)',
'Repouso':'Rest','Memória localizada':'Localized memory','Coletivo persistente':'Persistent collective','Transiente':'Transient','Indeterminada':'Indeterminate',
'B — Mapa discreto | estímulo fixo 0,9× | estados aos 5 s\n* Par estável e diferença >1 mV; a grade não determina fronteiras contínuas':'B — Discrete grid | fixed 0.9× stimulus | states at 5 s\n* Stable pair with difference >1 mV; the grid does not define continuous boundaries',
'Equilíbrios estáveis':'Stable equilibria','Equilíbrio instável':'Unstable equilibrium',
'Corrente sigmoidal + Kv':'Sigmoidal current + Kv','Corrente líquida cúbica (escalar)':'Cubic net current (scalar)',
'Voltagem isolada (mV)':'Isolated-cell voltage (mV)','Corrente estacionária requerida (A/m²)':'Required steady current (A/m²)',
'Interface restaurada':'Restored interface',
'Mesmo estímulo absoluto ancorado no modelo anterior':'Same absolute stimulus, anchored to conductance model',
'Receptores altos aos 5 s (%)':'High receivers at 5 s (%)',
'Rede original; restauração 500 ms; números = receptores/104':'Original network; restoration at 500 ms; counts out of 104',
'C — Bistabilidade isolada e seleção de estado na rede são perguntas distintas':'C — Local bistability and network state selection are distinct questions',
'kv':'Graded Kv1.5','bistable':'Persistent','excitable':'Excitable',
}
replacements=[(' s por sentido',' s per ramp leg'),('Aleatório ','Random '),(' × limiar original',' × reference stimulus'),('estímulo ','stimulus '),('estímulo de referência','reference stimulus'),('bistable |','Persistent |'),('excitable |','Excitable |'),('kv |','Graded Kv1.5 |'),('historica\n','Original geometry\n'),('fonte_esquerda\n','Left source\n'),('fonte_direita\n','Right source\n'),('geometria_1701\n','Geometry 1701\n'),('geometria_2701\n','Geometry 2701\n'),('Interface → restauração 500 ms','Interface restored at 500 ms'),('Intacta\n','Intact\n'),('fonte ','source '),(' receptores altos',' high receivers'),(' receptores',' receivers'),(' arestas',' edges'),(' nós',' nodes'),('stimulus de referência','reference stimulus')]
def translate(s):
 if s in translations:return translations[s]
 for a,b in replacements:s=s.replace(a,b)
 return s.replace(" | stimulus "," | ").replace(" × reference stimulus"," × reference")

def fingerprint(fig):
 """Hash numeric plotted artists and axis limits, excluding text and layout."""
 h=hashlib.sha256()
 def add(x):
  a=np.ma.asarray(x);h.update(str(a.shape).encode());h.update(str(a.dtype).encode());h.update(np.ascontiguousarray(a.data).tobytes());h.update(np.ma.getmaskarray(a).tobytes())
 for ax in fig.axes:
  add(ax.get_xlim());add(ax.get_ylim())
  for line in ax.lines:add(line.get_xdata());add(line.get_ydata())
  for collection in ax.collections:
   add(collection.get_offsets())
   if collection.get_array() is not None:add(collection.get_array())
   if hasattr(collection,'get_segments'):
    for segment in collection.get_segments():add(segment)
   if collection.get_clim()[0] is not None:add(collection.get_clim())
  for im in ax.images:add(im.get_array());add(im.get_clim());add(im.get_extent())
  for patch in ax.patches:
   if hasattr(patch,'get_width'):add([*patch.get_xy(),patch.get_width(),patch.get_height()])
 return h.hexdigest()
original_save=Figure.savefig;records=[]
def export(fig,path,**kwargs):
 fig.canvas.draw();before=fingerprint(fig);pairs=[]
 # Fixed tick formatters regenerate Text strings on each draw; translate the formatter too.
 for ax in fig.axes:
  for getlabels,setlabels in [(ax.get_xticklabels,ax.set_xticklabels),(ax.get_yticklabels,ax.set_yticklabels)]:
   labels=[x.get_text() for x in getlabels()];english=[translate(x) for x in labels]
   if labels!=english:
    pairs.extend([[a,b] for a,b in zip(labels,english) if a!=b]);setlabels(english)
 if Path(path).stem=='fig_mecanismo_alternativo':
  for ax in fig.axes:
   ax.title.set_fontsize(9);ax.xaxis.label.set_fontsize(9)
 for artist in fig.findobj(Text):
  old=artist.get_text();new=translate(old)
  if new!=old:artist.set_text(new);pairs.append([old,new])
 fig.canvas.draw();after=fingerprint(fig);assert before==after,(path,before,after)
 name=Path(path).stem
 for ext in ['png','svg']:original_save(fig,OUT/(name+'.'+ext),dpi=240)
 labels=sorted(set(a.get_text() for a in fig.findobj(Text) if a.get_text()))
 records.append(dict(figure=name,numeric_artists_before_sha256=before,numeric_artists_after_sha256=after,unchanged=True,translations=pairs,final_labels=labels))
 print('English export:',name,flush=True)
Figure.savefig=export

def block(path,start,end):
 source=path.read_text();text=source[source.index(start):source.index(end)]
 # First extracted line was at column 4 in main(); normalize all following lines.
 return textwrap.dedent('    '+text)
def rows(path):return [json.loads(s) for s in path.read_text().splitlines()]
def selector(rr):return lambda **kw:[r for r in rr if all(r.get(k)==v for k,v in kw.items())]
M=BASE/'transmissao_memoria_histerese';V=BASE/'validacao_generalizacao_2026-09'
rr=rows(M/'resultados_conferidos.jsonl')
ns=dict(ROOT=M,np=np,plt=plt,select=selector(rr),MODELS=dict.fromkeys(['kv','bistable','excitable']),names=['original','interface_10pct','independent32_seed11','independent32_seed22','independent32_seed33','cut'],labels=['Original','Interface 10%','Aleatório 11','Aleatório 22','Aleatório 33','Corte total'],colors=['#3f5368','#c64b47','#228b8d','#519963','#a78328','#606060'])
exec(block(M/'analisar.py','plt.rcParams.update',"print('Contrasts"),ns)
equilibria=json.loads((M/'equilibrios.json').read_text());roots=np.array([r['V'] for r in equilibria['bistable']])
geo=np.load(BASE/'sorteio_independente_32/topologias.npz')
witnesses=[r for r in rr if r['stage']=='memory' and r['model']=='bistable' and r['amplitude_factor']==.9 and r['restore_s']==.5 and r['graph'] in ['original','interface_10pct']]
# The historical spatial plot used the original trajectories; retain exactly those inputs.
ss=[np.load(M/(r['id']+'.npz'))['y'][:226,-1] for r in witnesses]
ns.update(N=226,XY=geo['xy'],CENTER=int(geo['center']),states=ss,rest_frozen=roots[0])
code=block(M/'estados_espaciais.py','fig,axes=plt.subplots','print(json.dumps(out').replace("MODELS['bistable'].roots()[0]",'rest_frozen')
exec(code,ns)
rr=rows(V/'resultados_conferidos_validacao.jsonl');P=json.loads((V/'protocolo_validacao.json').read_text());summary=json.loads((V/'resumo_validacao.json').read_text())
A=P['alternative'];L,U,H=A['L_V'],A['U_V'],A['H_V'];DEN=A['tau_s']*(H-L)**2
Q=json.loads((BASE/'primeiro_parametro_publicado/plano.json').read_text())
def steady_current(v):return Q['G_leak_S_m2']*(v-Q['E_leak_V'])+2.*expit((v-Q['V_half_V'])/Q['slope_V'])*(v-Q['E_channel_V'])-4.*expit((v+.025)/.004)*1.*(.05-v)
def cubic(v):return (v-L)*(v-U)*(H-v)/DEN
if args.endpoint_cache:
 with np.load(args.endpoint_cache,allow_pickle=False) as cache:
  assert set(cache.files)=={r['id'] for r in rr}, 'Endpoint cache does not match the frozen validation cases'
  states={r['id']:cache[r['id']].copy() for r in rr}
  assert all(v.shape==(226,) and np.isfinite(v).all() for v in states.values())
else:
 states={r['id']:np.load(V/r['effective_source']/(r['id']+'.npz'))['y'][:226,-1] for r in rr}
ns.update(ROOT=V,P=P,select=selector(rr),byid={r['id']:r for r in rr},data=np.load(V/'geometrias.npz'),states=states,geometries=summary['geometry_pairs'],regime=summary['regime_pairs'],LineCollection=LineCollection,ListedColormap=ListedColormap,BoundaryNorm=BoundaryNorm,Patch=Patch,CATS=['repouso','memoria_localizada','recrutamento_coletivo','transiente_sem_persistencia','indeterminada'],LABELS=['Repouso','Memória localizada','Coletivo persistente','Transiente','Indeterminada'],COLORS=['#dce6ed','#ecad4b','#25887d','#b49aca','#de6471'],L=L,U=U,H=H,cubic=cubic,roots_frozen=roots,steady_current=steady_current,C_frozen=Q['cm_F_m2'])
code=block(V/'analisar_validacao.py','plt.rcParams.update',"print('ANALYZED").replace("old.Model('bistable',4.).roots()",'roots_frozen').replace("old.Model('bistable',4.).steady_current(v)",'steady_current(v)').replace('old.C','C_frozen')
exec(code,ns)
assert len(records)==8
(OUT/'ENGLISH_FIGURE_AUDIT.json').write_text(json.dumps(dict(scope='Rendering only; no ODE integration. Numeric-artist hashes exclude text and layout.',figures=records),indent=2,ensure_ascii=False)+'\n')
