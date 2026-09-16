"""Render the final bounded-validation report from accepted outputs; no simulations."""
import sys
sys.dont_write_bytecode=True
import json,re
from modelo import *

def main():
    s=json.loads((ROOT/'resumo_validacao.json').read_text());q=json.loads((ROOT/'verificacao_numerica.json').read_text());a=json.loads((ROOT/'AUDITORIA_FINAL_VALIDACAO.json').read_text());m=json.loads((ROOT/'mecanismo_alternativo.json').read_text());rows=[json.loads(x) for x in (ROOT/'resultados_conferidos_validacao.jsonl').read_text().splitlines()]
    assert q['passed'] and a['passed'] and m['isolated_passed']
    byid={r['id']:r for r in rows};sha=digest(ROOT/'protocolo_validacao.json')
    gt=[]
    for g in P['geometries']:
        pair=next(r for r in s['geometry_pairs'] if r['geometry']==g['name'] and r['factor']==.9)
        edgechange=next(r for r in a['geometry_checks'] if r['name']==g['name'])['changed_undirected_edges_vs_original']
        gt.append(f"| {g['name']} | {g['source']} | {g['targets']} | {len(g['interface_edges'])} | {edgechange} | {pair['intact_target_high']} → {pair['restored_target_high']} |")
    geometry_table='\n'.join(gt)
    reg=[]
    for gd in P['gD_grid']:
        rr=sorted([r for r in s['regime_pairs'] if r['gd']==gd],key=lambda r:r['restore_s'])
        reg.append(f"| {gd:g} | {rr[0]['intact_category'].replace('_',' ')} | {sum(x['history_dependence'] for x in rr)}/6 | "+', '.join(str(int(r['restore_s']*1000)) for r in rr if r['history_dependence'])+' |')
    regime_table='\n'.join(reg)
    full=[r for r in rows if r['model']=='bistable' and r['history']=='interface' and 'never_restore' in r['controls']]
    never_table='\n'.join(f"| {r['geometry']} | {r['target_high']}/{r['target_count']} | {r['total_high']}/226 |" for r in full)
    alt=[r for r in rows if r['model']=='cubic' and r['factor']>0]
    geodiffs=[r['max_final_voltage_difference_V']*1000 for r in s['geometry_pairs'] if r['history_dependence']]
    eigenmax=max(r['max_real_eigen_s_inv'] for r in rows)
    isolated_refmax=max(r['radau_vs_refined_V'] for r in m['isolated_protocols'])
    regpositive=[r['max_final_voltage_difference_V']*1000 for r in s['regime_pairs'] if r['history_dependence']]
    alt_distance=max(r['max_final_voltage_difference_V'] for r in s['alternative_pairs'])
    text=f'''# Última validação dirigida: geometria, regime e mecanismo bistável

**Campanha encerrada após os três blocos definidos. Recomendação B: pronto para manuscrito, com conclusão restrita.** O efeito histórico reapareceu nas quatro variantes adicionais e em24 dos42 pontos do mapa. Não apareceu na formulação cúbica sob os estímulos fixados, embora sua bistabilidade tenha sido verificada. Não houve reajuste de parâmetros após consultar resultados.

## 1. Pergunta

Uma alteração temporária do acoplamento pode selecionar estados elétricos persistentes diferentes depois de restabelecer exatamente a mesma conectividade? A última validação testa se o achado anterior sobrevive a pequenas mudanças de geometria/fonte, ocupa mais de um ponto de parâmetros e reaparece com outra formulação bistável. São perguntas sobre modelos determinísticos sintéticos.

A teoria principal sobre coordenação por potencial de membrana motiva a pergunta, mas o experimento computacional termina no estado elétrico. Não testa decisões moleculares, anatomia ou tecido real. Esta etapa não inclui novos testes de reparo.

## 2. Protocolo congelado

Congelamento local em **{P['frozen_utc']}**, antes de consultar resultados das novas condições. SHA-256 de `protocolo_validacao.json`: **`{sha}`**. O arquivo contém IDs, máscaras, arestas sorteadas, seeds, estímulos, solvers, critérios e limites de execução. Não é pré-registro externo nem avaliação cega: os resultados históricos eram conhecidos.

A auditoria prévia releu métodos e relatório, processou integralmente os arquivos estruturados, recalculou os487 picos e frações finais arquivados e conferiu campos CSV/JSONL e contrastes de reparo. Erro de recomputação dos picos:0. Os583 hashes do manifesto anterior conferiram. O estudo antigo teve seis falhas iniciais de precisão, já corrigidas separadamente; tanto falhas quanto correções foram preservadas. Não foi encontrado bug comprovado que exigisse alteração anterior.

| Bloco | Participações de condições de rede |
|---|---:|
| Geometria/fonte, com controles | 65 |
| Mapa gD × tempo, com intactas | 49 |
| Corrente alternativa, com controles | 24 |
| Total rotulado | 138 |
| **Condições distintas de rede** | **136** |
| Verificações isoladas distintas | 6 |

Duas condições idênticas pertencem aos blocos1 e2 e foram executadas uma vez. As142 condições iniciais distintas não são142 réplicas independentes. Refinamentos e referências repetem condições; não ampliam o conjunto científico.

Todos os grafos têm226nós e622arestas. Gj=1S/m², C=0,01F/m², GL=1S/m²; corrente persistente histórica com Kv1.5 e tauK=14,8ms. A fonte recebe um único pulso de20ms desde t=0. Referência absoluta preservada: **{P['anchor_A_m2']:.14f}A/m²**. Fatores0,9/1/1,1 correspondem a {P['anchor_A_m2']*.9:.11f}, {P['anchor_A_m2']:.11f}, {P['anchor_A_m2']*1.1:.11f}A/m². Não houve ajuste de limiar por geometria, gD ou mecanismo.

No bloco1, gD=4 e restauração500ms. Fontes alternativas: nós mais próximos dos alvos definidos por quantis x20/80% e mediana y, com receptores orientados para o interior. Geometrias novas: deslocamentos gaussianos com desvio0,1×comprimento mediano da aresta original, seeds1701/2701; árvore geradora mínima nos candidatos Delaunay, completada pelas arestas restantes mais curtas até622. Nenhuma geometria foi rejeitada ou substituída. Fonte central das geometrias novas: nó mais próximo do centroide.

Receptores: projeção horizontal orientada a mais de0,1×distância mediana fonte–vizinho da fonte. A interface reúne todas as arestas entre os dois lados e reduz seus pesos a10%. Um sorteio PCG64 por configuração, SeedSequence([20260915,1,índice]), reduz o mesmo número de arestas pelos mesmos90%; coincidências com a interface são mantidas. As perdas são pareadas **dentro** de cada configuração, não iguais entre geometrias.

Classificação previamente definida: repouso se a diferença final em todos os nós for≤0,1mV; transiente sem persistência se houve cruzamento do nível de referência em algum nó e depois retorno; memória localizada para estado estacionário fora do repouso, com<50% dos receptores altos; coletivo se≥50%. “Localizada” é uma categoria relativa à região receptora, podendo incluir muitas células no lado da fonte. “Transiente” não implica potencial de ação: basta cruzamento do nível, inclusive em controles graduados.

O nível alto é a raiz instável isolada do mecanismo/gD efetivo; ablações usam a referência histórica gD4. Exigimos resíduo max|dV/dt|<10⁻⁵V/s, derivada dos gates<10⁻⁴s⁻¹ e maior parte real do Jacobiano completo<−10⁻⁶s⁻¹. Dependência da história exige ambos os estados aceitos e estáveis, mesmo grafo final e diferença máxima por nó>1mV. Foram mantidos também estados completos, contagens e diferenças contínuas.

## 3. Generalização de geometria/fonte

Com o pulso0,9×, o contraste ocorreu nas cinco configurações: a intacta manteve um nó alto e nenhum receptor alto; interface temporária seguida de restauração terminou com226nós altos. Diferença máxima entre estados finais: {min(geodiffs):.3f}–{max(geodiffs):.3f}mV. São cinco comparações determinísticas, incluindo o controle conhecido.

| Configuração | Fonte | Receptores | Arestas de interface | Diferença simétrica de arestas vs. original | Receptores altos: intacta → restaurada |
|---|---:|---:|---:|---:|---:|
{geometry_table}

A diferença simétrica conta remoções mais inclusões. As duas fontes alternativas usam o mesmo grafo histórico; as outras duas variantes modificam posições e arestas. Não são cinco topologias independentes nem uma amostra representativa de redes.

**Resultado negativo de sensibilidade ao estímulo:** nos fatores1,0 e1,1, todas as configurações intactas e restauradas terminaram coletivamente altas. Assim, cinco dos15 pares de geometria/fonte diferiram; todas as diferenças ocorreram em0,9×. Não houve configuração adicional que falhasse nessa amplitude específica, mas o contraste não sobreviveu ao aumento do estímulo.

![Figura A](fig_generalizacao_geometrias.png)

## 4. Mapa de regime

Rede histórica, pulso fixo0,9×, gD em3,4/3,6/3,8/4/4,2/4,4/4,6S/m²; tempos20/50/100/200/350/500ms. As42 interfaces restauradas terminaram coletivamente altas. A diferença entre histórias dependeu do estado alcançado pela intacta:

| gD (S/m²) | Intacta | Pares com dependência da história | Tempos positivos (ms) |
|---|---|---:|---|
{regime_table}

**24/42 pontos** exibiram dependência da história. A diferença final nos pares positivos foi{min(regpositive):.3f}–{max(regpositive):.3f}mV. EmgD3,4/3,6 a intacta apresentou excursão localizada e retornou ao repouso; em3,8/4 manteve memória localizada; em4,2/4,4/4,6 tornou-se coletivamente alta, igualando o desfecho restaurado.

Isso demonstra uma faixa **amostrada**, em quatro níveis de gD e seis tempos, em vez de um único ponto. Não determina a área de uma região contínua nem a posição exata de sua fronteira. Não foi detectada janela de restauração nesse intervalo para a variante persistente; os seis tempos deram o mesmo desfecho por gD. A janela histórica da variante excitável é outra pergunta e não foi reavaliada aqui.

![Figura B](fig_mapa_regime.png)

## 5. Mecanismo bistável alternativo

Foi definida uma corrente líquida cúbica escalar, substituindo leak+Kv+corrente sigmoidal:

\\[
\\dot V_i=\\frac{{(V_i-L)(V_i-U)(H-V_i)}}{{\\tau(H-L)^2}}-\\frac{{G_J}}{{C}}(\\mathcal L V)_i+\\frac{{I_i}}{{C}},
\\quad L=-50\\,\\mathrm{{mV}},\ U=-35\\,\\mathrm{{mV}},\ H=10\\,\\mathrm{{mV}},\ \\tau=3,125\\,\\mathrm{{ms}}.
\\]

A escolha preserva aproximadamente a escala de voltagem e a relaxação linear do repouso baixo do modelo anterior; não iguala corrente regenerativa máxima, altura de barreira ou limiar de recrutamento da rede. É uma lei fenomenológica de corrente total com dimensão de estado diferente, não um novo canal biológico.

**Antes de qualquer teste de rede**, as raízes−50/−35/+10mV apresentaram autovalores−80/+60/−240s⁻¹. As dobras ocorreram em−43,02776/−6,97224mV, com correntes+0,00263826/−0,01819381A/m². Quatro estados iniciais próximos dos repousos estáveis retornaram aos respectivos ramos sob o mesmo I=0. Duas rampas triangulares,1 e5s por sentido, comutaram para o ramo alto e retornaram ao baixo. Referências e refinamentos passaram; a bistabilidade se apoia nas raízes e estabilidade, não apenas na presença de laço.

Nos grafos conectados, os estados homogêneos baixo e alto também são equilíbrios: o Laplaciano anula vetores constantes. Seus Jacobianos escalares são F′(V*)I − Gj·Laplaciano/C; como o Laplaciano é positivo semidefinido, os dois ramos permanecem linearmente estáveis. Isso é uma consequência algébrica da formulação, não uma nova simulação. Portanto o resultado negativo não decorre da inexistência desses dois atratores homogêneos.

**Resultado da rede:** nenhum dos12 pares intacta/interface-restaurada manteve estados finais diferentes. Todos retornaram a−50mV; maior diferença final entre histórias≈{alt_distance:.3g}V. Nas21 condições cúbicas estimuladas, apenas a fonte cruzou a raiz instável isolada e nenhum receptor a cruzou. Os picos na fonte ficaram entre{min(r['peak_V'] for r in alt)*1000:.2f} e{max(r['peak_V'] for r in alt)*1000:.2f}mV, seguidos de recuperação. Cruzar a separatriz da célula isolada não garante comutação da célula acoplada, submetida à carga dos vizinhos.

Esse resultado **não generaliza positivamente o achado ao mecanismo alternativo**. Também não prova que correntes cúbicas sejam incapazes de exibir seleção por história em outros parâmetros: aqui se testou uma formulação e um protocolo fixados, sem recalibrar sua excitabilidade de rede. A bistabilidade isolada não foi suficiente para produzir o desfecho nessas condições. Não foram aumentados estímulos ou alteradas constantes para tentar obter um resultado positivo.

![Figura C](fig_mecanismo_alternativo.png)

## 6. Controles

Seis controles sem estímulo permaneceram no repouso, com maior desvio final{max(r['final_max_departure_V'] for r in rows if 'no_stimulus' in r['controls']):.3g}V. As12 condições sem corrente adicional retornaram ao repouso; alguns pulsos cruzaram transitoriamente o nível usado na classificação, sem persistência. Dez ablações usam o Kv histórico e duas usam leak puro: no cúbico, desligar Jadd=GL(V−EL)+C·F(V) deixa apenas o leak. Essas ablações não são mecanismos idênticos.

Nos cinco controles persistentes sem restauração, o desfecho dependeu da geometria:

| Configuração | Receptores altos | Nós altos |
|---|---:|---:|
{never_table}

Emgeometria1701, a interface enfraquecida já permitiu recrutamento coletivo sem reconectar. Nas outras quatro, houve persistência no lado da fonte e nenhum receptor alto. A restauração completa faz parte do teste principal, mas **não é necessária para recrutamento em toda geometria**. Sem restauração, os grafos finais diferem; esses controles não contam como pares de memória sob mesma estrutura.

Dos cinco sorteios persistentes em0,9×, quatro produziram o estado coletivo e um — fonte_direita — manteve ativação localizada. Nos fatores1/1,1, todos recrutaram coletivamente. Os três sorteios cúbicos estimulados retornaram ao repouso. Assim, a interface geométrica não é a única alteração capaz de selecionar outro estado; os controles pareados sustentam o papel da distribuição das conexões, com efeito dependente da configuração. Um sorteio por variante não caracteriza uma distribuição estatística.

## 7. Auditoria numérica

As136 trajetórias foram observadas até5s e refinadas. DOP853 principal: rtol10⁻¹⁰, atol10⁻¹², passo máximo2,5ms. Refinamento: rtol10⁻¹², atol10⁻¹⁴, passo máximo1ms. As{q['radau_count']} referências de rede previamente fixadas usaram Radau com Jacobiano analítico, rtol10⁻¹¹, atol10⁻¹³ e passo máximo2,5ms. Os seis protocolos isolados também foram refinados e comparados com Radau.

A tolerância de comparação permaneceu **0,02mV**, acompanhada de concordância da categoria e das contagens finais e de cruzamentos. Erro máximo principal–refinado: **{q['maximum_primary_refined_V']*1000:.9f}mV**; Radau–refinado: **{q['maximum_radau_refined_V']*1000:.9f}mV**. Maior erro Radau isolado: {isolated_refmax*1000:.3g}mV. Falhas iniciais: **{len(q['original_failed_ids'])}**; correções adicionais: **{len(q['corrected_ids'])}**; casos não resolvidos: **{len(q['unresolved_ids'])}**. Mudanças de classificação entre solvers: **{len(q['classification_changes'])}**.

Todos os estados finais foram estacionários e linearmente estáveis; maior parte real encontrada: {eigenmax:.6f}s⁻¹. Não houve mudança de categoria entre2 e5s; maior alteração de voltagem nesse intervalo: {max(r['max_voltage_change_2_to_5s_V'] for r in rows):.3g}V. A estabilidade foi calculada no Jacobiano completo de cada estado final, não apenas na célula isolada. Não foram acrescentados ensaios de ruído nem um censo global de atratores.

Os eventos de pulso/restauração delimitam segmentos exatos de integração. Picos e primeiros cruzamentos são medidas na grade de saída de1ms; o erro entre integradores também é avaliado nessa grade, não como garantia de máximo contínuo entre amostras. A função de classificação é operacional e não identifica potenciais de ação biológicos.

Os quatro Jacobianos de implementação passaram em diferenças finitas antes dos testes de rede. O verificador final recalculou contagens, picos, tempos do primeiro recrutamento e campos CSV/JSONL diretamente das trajetórias; erro nas métricas recomputadas:0. Conferiu{a['paired_comparisons_checked']} pares e seus grafos finais. Duas trajetórias históricas testemunhas foram reproduzidas contra os arquivos antigos dentro da tolerância. Os{a['previous_files_unchanged']} arquivos anteriores, incluindo o próprio manifesto, permaneceram idênticos por hash; o protocolo e o código executado também conferiram.

Ocorrências operacionais: o primeiro inventário externo tentou usar `.items()` em um JSON que era lista; corrigido o leitor, sem modificação anterior. Um comando de lançamento do verificador tinha caminho incorreto para o log e foi rejeitado pelo shell antes de iniciar a simulação; o caminho foi corrigido. Não foram falhas numéricas, ajustes de modelo ou condições excluídas. Nenhuma nova execução nativa BETSE ou validação de tecido foi realizada.

## 8. Resultados negativos

- A alternativa cúbica não exibiu memória de história em nenhum dos12 pares testados; nenhum receptor cruzou o nível alto em suas21 condições estimuladas.
- Nos fatores1/1,1 do bloco de geometria, as histórias convergiram ao mesmo estado coletivo nas cinco configurações.
- EmgD4,2/4,4/4,6, o mapa não diferenciou as histórias, pois ambas recrutaram toda a rede.
- As intactas emgD3,4/3,6 retornaram ao repouso; não se deve chamar toda resposta subcoletiva de memória localizada.
- A restauração não foi necessária para recrutamento na geometria1701; a interface não foi uma localização exclusiva de efeitos nos controles aleatórios.
- Não foi encontrada fronteira temporal no intervalo20–500ms dessa variante persistente.
- Não houve falha de integração ou precisão nos casos concluídos desta etapa. As seis reprovações numéricas antigas continuam preservadas no estudo anterior.

## 9. O que mudou em relação ao estudo anterior

A seleção por história deixou de depender apenas do nó61 e da configuração histórica: reapareceu nas quatro variantes objetivamente definidas. O mapa ampliou a sensibilidade antiga3,6/4/4,4 para sete níveis e seis tempos, mantendo o estímulo fixo. Isso fortalece uma conclusão condicionada ao regime e à família da corrente histórica.

A corrente cúbica, em contrapartida, restringe a generalização de mecanismo. Múltiplos atratores disponíveis não garantem que o protocolo de acoplamento e estímulo os selecione de forma diferente. O modelo de corrente, sua força regenerativa, o estímulo e a carga da rede continuam sendo parte da conclusão. A hipótese ampla de suficiência da bistabilidade isolada não foi sustentada por esta comparação.

O resultado antigo sobre reparo permanece **separado**: uma regra que elevou a transmissão graduada pode não favorecer a transição coletiva perto do limiar. Esta etapa não reavaliou esse resultado em novas geometrias ou mecanismos e não autoriza estender sua robustez. A regra anterior foi um ranking comparado a três ordens aleatórias, não uma prova de otimização global.

## 10. Conclusão mínima defensável

**Em redes sintéticas com a corrente persistente sigmoidal e Kv utilizadas aqui, mudanças temporárias de acoplamento podem selecionar estados elétricos estáveis diferentes após restauração da mesma conectividade. O efeito reapareceu em quatro variantes adicionais e em uma faixa amostrada de parâmetros, mas dependeu do estímulo e não foi reproduzido pela corrente cúbica sob o protocolo fixado.**

Formulação em inglês adequada ao alcance observado:

> In the synthetic conductance-based network family tested here, transient changes in intercellular coupling can select distinct stable electrical states despite identical final connectivity. This effect recurred across predefined geometry and source variants and sampled parameter ranges, but was absent in the alternative cubic model under the fixed stimulation protocol.

Respostas aos sete critérios de encerramento: (1) sim, em quatro variantes adicionais; (2) sim, em24 pontos de uma faixa amostrada, sem fronteira contínua estimada; (3) não, na alternativa fixada; (4) estímulo mais forte, gD≥4,2 nos níveis testados e o mecanismo alternativo eliminaram o contraste; (5) seleção de atrator elétrico condicionada ao modelo e protocolo; (6) manter o resultado principal, restringindo generalidade; (7) os dados fortalecem generalização de geometria/regime e restringem a de mecanismo. Não refutam o contraste histórico, que foi reproduzido.

## 11. Limitações

Variantes pequenas, derivadas de uma geometria comum; topologias e fontes correlacionadas; um único novo sorteio por configuração. Somente um valor de Gj, um tauK, um pulso e uma alternativa cúbica; sem calibração de limiar de rede equivalente entre mecanismos. A alternativa aproxima a relaxação do repouso, mas não todas as propriedades regenerativas da corrente histórica. Nenhuma frequência observada estima prevalência em redes ou sistemas biológicos.

Reservatórios/reversões permanecem fixos. Não há homeostase iônica, canal molecular identificado para a corrente adicional, expressão gênica, proliferação, morfogênese, anatomia, regeneração, eficácia terapêutica ou comunicação radiativa. Estabilidade linear é local;5s simulados não são uma escala de memória biológica. Prioridade inédita e adequação editorial a uma revista não foram estabelecidas nesta validação dirigida.

## 12. Implicações para o manuscrito

Apresentar o contraste sob mesmo grafo final como resultado principal computacional, acompanhado de generalização delimitada e do negativo cúbico. Evitar “bistabilidade implica memória de história”, “efeito universal de interface” ou “restauração necessária em todas as redes”. Incluir controles aleatórios e sem restauração junto aos resultados positivos, preservando seus denominadores.

Separar a previsão sobre seleção de estado da conclusão anterior sobre reparo. A teoria motivadora sobre organização celular permanece uma hipótese mais ampla do que a evidência elétrica aqui produzida. Não acrescentar novas simulações a esta campanha para tentar melhorar a narrativa.

## 13. Arquivos para reprodução

- Planejamento/procedência: `PLANO_VALIDACAO.md`, `protocolo_validacao.json`, `congelamento.json`, `auditoria_previa.json`, `originais_sha256.json`, `execucao_validacao.json` e `MANIFESTO_SHA256.json`.
- Geometrias e máscaras: `geometrias.npz`; fontes, regras e arestas no protocolo. A análise usa máscaras explícitas, sem reaproveitar RIGHT/CENTER/ORIGINAL fixos nas variantes.
- Resultados iniciais preservados: `resultados_validacao.jsonl` e `primarias/`.
- Dados efetivos para análise: `resultados_conferidos_validacao.jsonl`, `metricas_validacao.csv` e `refinadas/`; `correcoes/` seria usado apenas para reprovações. As métricas principais finais são derivadas do refinamento, com vínculo explícito aos originais.
- Comparações: `generalizacao_geometrias.csv`, `mapa_regime.csv/json`, `comparacao_mecanismos.csv`, `controles_validacao.csv`, `contrastes_aleatorios.csv`, `resumo_validacao.json` e figurasA–C.
- Mecanismo: `mecanismo_isolado_antes_rede.json` preserva a aceitação anterior à rede; `mecanismo_alternativo.json` acrescenta seus resultados. Trajetórias isoladas em `isolada/`.
- Verificação: `verificacao_numerica.json`, `verificacao_linhas.jsonl`, `radau/`, `AUDITORIA_FINAL_VALIDACAO.json` e logs.
- Código: `preparar.py` audita e congela, `modelo.py` reutiliza equações/Jacobiano históricos por leitura e implementa a corrente cúbica, `executar.py` executa as etapas, `analisar_validacao.py` agrega/figura, `auditar_validacao.py` reconfere dados e hashes, `gerar_relatorio.py` monta este relatório.

Ambiente: Python{P['environment']['python']}, NumPy{P['environment']['numpy']}, SciPy{P['environment']['scipy']}, `{P['environment']['platform']}`. Solvers SciPyDOP853/Radau, BLAS limitado a um thread nos comandos. O protocolo preserva o executável e parâmetros; `dependencias_ambiente.txt` registra pacotes. Unidades SI, salvo colunas/figuras explicitamente convertidas a mV ou ms.

Na raiz do repositório, para preparar uma nova pasta irmã sem executar simulações:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-betse130/bin/python research/bioeletricidade-vmem-2026-09-08/validacao_generalizacao_2026-09/reproduzir_validacao.py repeticao_validacao
```

A opção`--run` repete apenas o protocolo congelado e suas verificações, gerando tabelas/figuras e auditoria na cópia. Recusa destino existente. Requer as dependências históricas preservadas na mesma árvore. A preparação e a importação do protocolo foram conferidas em uma pasta irmã nesta entrega; não se executou uma segunda campanha integral em outra pasta. O relatório interpretativo e a inspeção visual não são automaticamente certificados pelo comando de reprodução.

## Recomendação para publicação

**B. Pronto, mas a conclusão precisa ser restringida.** Há evidência numérica consistente de seleção por história na família histórica, com generalização adicional de geometria/fonte e regime. O mecanismo cúbico deu resultado negativo, e a bistabilidade isolada não pode ser apresentada como garantia do fenômeno. A restrição é parte do resultado e deve integrar o manuscrito, sem esconder o teste que não generalizou.

Esta classificação significa prontidão para redigir um manuscrito computacional com esse alcance; não garante novidade, aceitação editorial ou validação biológica. **A campanha de simulação está encerrada.** Nenhum manuscrito anterior foi alterado e nenhum material foi publicado ou enviado externamente.
'''
    # Editorial spacing only, after rendering; no changes to scientific inputs.
    text=re.sub(r'\b(dos|nos|nas|as|As|Os|os|em|Em|por|com|até|aos)(?=\d)',r'\1 ',text)
    text=re.sub(r'(\d)(mV|ms|s|V|A/m²|F/m²|S/m²|nós|arestas)(?=[ ,.;/)—]|$)',r'\1 \2',text)
    text=text.replace('Emgeometria','Em geometria').replace('emgD','em gD ').replace('EmgD','Em gD ').replace('bloc o','bloco')
    text=text.replace('gD≥','gD ≥ ').replace('gD4','gD = 4').replace('gD3','gD 3')
    text=text.replace('com226','com 226').replace('um único novo sorteio','um único novo sorteio')
    for before,after in {'blocos1 e2':'blocos 1 e 2','não são142':'não são 142','têm226':'têm 226','e622':'e 622','de20':'de 20','bloco1':'bloco 1','restauração500':'restauração 500','x20/80%':'x = 20/80%','desvio0,1':'desvio 0,1','de0,1':'de 0,1','a10%':'a 10%','mesmos90%':'mesmos 90%','pulso0,9':'pulso 0,9','fatores1':'fatores 1','e1,1':'e 1,1','fixo0,9':'fixo 0,9','tempos20':'tempos 20','foi55':'foi 55','Nas21':'Nas 21','suas21':'suas 21','final6':'final 6','geometria1701':'geometria_1701','máximo2':'máximo 2','máximo1':'máximo 1','entre2 e5':'entre 2 e 5','de1 ms':'de 1 ms','Conferiu87':'Conferiu 87','intervalo20':'intervalo 20','nó61':'nó 61','antiga3':'antiga 3','local;5':'local; 5','figurasA':'figuras A','Python3':'Python 3','NumPy1':'NumPy 1','SciPy1':'SciPy 1','SciPyDOP':'SciPy DOP','opção`':'opção `','rtol10':'rtol 10','atol10':'atol 10'}.items():text=text.replace(before,after)
    text=text.replace('mV**',' mV**').replace('00A/m²','00 A/m²').replace('s⁻¹',' s⁻¹')
    (ROOT/'RESULTADOS_VALIDACAO.md').write_text(text)
    print('REPORT',len(text.split()),'words',flush=True)
if __name__=='__main__':main()
