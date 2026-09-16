# Última validação dirigida: geometria, regime e mecanismo bistável

**Campanha encerrada após os três blocos definidos. Recomendação B: pronto para manuscrito, com conclusão restrita.** O efeito histórico reapareceu nas quatro variantes adicionais e em 24 dos 42 pontos do mapa. Não apareceu na formulação cúbica sob os estímulos fixados, embora sua bistabilidade tenha sido verificada. Não houve reajuste de parâmetros após consultar resultados.

## 1. Pergunta

Uma alteração temporária do acoplamento pode selecionar estados elétricos persistentes diferentes depois de restabelecer exatamente a mesma conectividade? A última validação testa se o achado anterior sobrevive a pequenas mudanças de geometria/fonte, ocupa mais de um ponto de parâmetros e reaparece com outra formulação bistável. São perguntas sobre modelos determinísticos sintéticos.

A teoria principal sobre coordenação por potencial de membrana motiva a pergunta, mas o experimento computacional termina no estado elétrico. Não testa decisões moleculares, anatomia ou tecido real. Esta etapa não inclui novos testes de reparo.

## 2. Protocolo congelado

Congelamento local em **2026-09-15T13:58:30.658348+00:00**, antes de consultar resultados das novas condições. SHA-256 de `protocolo_validacao.json`: **`a9d5d8078bfef94c02864a6c7753946882259e0846e44b8541cadb715deac4fb`**. O arquivo contém IDs, máscaras, arestas sorteadas, seeds, estímulos, solvers, critérios e limites de execução. Não é pré-registro externo nem avaliação cega: os resultados históricos eram conhecidos.

A auditoria prévia releu métodos e relatório, processou integralmente os arquivos estruturados, recalculou os 487 picos e frações finais arquivados e conferiu campos CSV/JSONL e contrastes de reparo. Erro de recomputação dos picos:0. Os 583 hashes do manifesto anterior conferiram. O estudo antigo teve seis falhas iniciais de precisão, já corrigidas separadamente; tanto falhas quanto correções foram preservadas. Não foi encontrado bug comprovado que exigisse alteração anterior.

| Bloco | Participações de condições de rede |
|---|---:|
| Geometria/fonte, com controles | 65 |
| Mapa gD × tempo, com intactas | 49 |
| Corrente alternativa, com controles | 24 |
| Total rotulado | 138 |
| **Condições distintas de rede** | **136** |
| Verificações isoladas distintas | 6 |

Duas condições idênticas pertencem aos blocos 1 e 2 e foram executadas uma vez. As 142 condições iniciais distintas não são 142 réplicas independentes. Refinamentos e referências repetem condições; não ampliam o conjunto científico.

Todos os grafos têm 226 nós e 622 arestas. Gj=1 S/m², C=0,01 F/m², GL=1 S/m²; corrente persistente histórica com Kv1.5 e tauK=14,8 ms. A fonte recebe um único pulso de 20 ms desde t=0. Referência absoluta preservada: **0.08237304687500 A/m²**. Fatores0,9/1/1,1 correspondem a 0.07413574219, 0.08237304688, 0.09061035156 A/m². Não houve ajuste de limiar por geometria, gD ou mecanismo.

No bloco 1, gD=4 e restauração 500 ms. Fontes alternativas: nós mais próximos dos alvos definidos por quantis x = 20/80% e mediana y, com receptores orientados para o interior. Geometrias novas: deslocamentos gaussianos com desvio 0,1×comprimento mediano da aresta original, seeds1701/2701; árvore geradora mínima nos candidatos Delaunay, completada pelas arestas restantes mais curtas até 622. Nenhuma geometria foi rejeitada ou substituída. Fonte central das geometrias novas: nó mais próximo do centroide.

Receptores: projeção horizontal orientada a mais de 0,1×distância mediana fonte–vizinho da fonte. A interface reúne todas as arestas entre os dois lados e reduz seus pesos a 10%. Um sorteio PCG64 por configuração, SeedSequence([20260915,1,índice]), reduz o mesmo número de arestas pelos mesmos 90%; coincidências com a interface são mantidas. As perdas são pareadas **dentro** de cada configuração, não iguais entre geometrias.

Classificação previamente definida: repouso se a diferença final em todos os nós for≤0,1 mV; transiente sem persistência se houve cruzamento do nível de referência em algum nó e depois retorno; memória localizada para estado estacionário fora do repouso, com<50% dos receptores altos; coletivo se≥50%. “Localizada” é uma categoria relativa à região receptora, podendo incluir muitas células no lado da fonte. “Transiente” não implica potencial de ação: basta cruzamento do nível, inclusive em controles graduados.

O nível alto é a raiz instável isolada do mecanismo/gD efetivo; ablações usam a referência histórica gD = 4. Exigimos resíduo max|dV/dt|<10⁻⁵V/s, derivada dos gates<10⁻⁴ s⁻¹ e maior parte real do Jacobiano completo<−10⁻⁶ s⁻¹. Dependência da história exige ambos os estados aceitos e estáveis, mesmo grafo final e diferença máxima por nó>1 mV. Foram mantidos também estados completos, contagens e diferenças contínuas.

## 3. Generalização de geometria/fonte

Com o pulso 0,9×, o contraste ocorreu nas cinco configurações: a intacta manteve um nó alto e nenhum receptor alto; interface temporária seguida de restauração terminou com 226 nós altos. Diferença máxima entre estados finais: 58.500–58.517 mV. São cinco comparações determinísticas, incluindo o controle conhecido.

| Configuração | Fonte | Receptores | Arestas de interface | Diferença simétrica de arestas vs. original | Receptores altos: intacta → restaurada |
|---|---:|---:|---:|---:|---:|
| historica | 61 | 104 | 32 | 0 | 0 → 104 |
| fonte_esquerda | 50 | 168 | 28 | 0 | 0 → 168 |
| fonte_direita | 63 | 170 | 28 | 0 | 0 → 170 |
| geometria_1701 | 52 | 110 | 37 | 12 | 0 → 110 |
| geometria_2701 | 61 | 109 | 38 | 10 | 0 → 109 |

A diferença simétrica conta remoções mais inclusões. As duas fontes alternativas usam o mesmo grafo histórico; as outras duas variantes modificam posições e arestas. Não são cinco topologias independentes nem uma amostra representativa de redes.

**Resultado negativo de sensibilidade ao estímulo:** nos fatores 1,0 e 1,1, todas as configurações intactas e restauradas terminaram coletivamente altas. Assim, cinco dos 15 pares de geometria/fonte diferiram; todas as diferenças ocorreram em 0,9×. Não houve configuração adicional que falhasse nessa amplitude específica, mas o contraste não sobreviveu ao aumento do estímulo.

![Figura A](fig_generalizacao_geometrias.png)

## 4. Mapa de regime

Rede histórica, pulso fixo 0,9×, gD em 3,4/3,6/3,8/4/4,2/4,4/4,6 S/m²; tempos 20/50/100/200/350/500 ms. As 42 interfaces restauradas terminaram coletivamente altas. A diferença entre histórias dependeu do estado alcançado pela intacta:

| gD (S/m²) | Intacta | Pares com dependência da história | Tempos positivos (ms) |
|---|---|---:|---|
| 3.4 | transiente sem persistencia | 6/6 | 20, 50, 100, 200, 350, 500 |
| 3.6 | transiente sem persistencia | 6/6 | 20, 50, 100, 200, 350, 500 |
| 3.8 | memoria localizada | 6/6 | 20, 50, 100, 200, 350, 500 |
| 4 | memoria localizada | 6/6 | 20, 50, 100, 200, 350, 500 |
| 4.2 | recrutamento coletivo | 0/6 |  |
| 4.4 | recrutamento coletivo | 0/6 |  |
| 4.6 | recrutamento coletivo | 0/6 |  |

**24/42 pontos** exibiram dependência da história. A diferença final nos pares positivos foi 55.606–58.500 mV. Em gD 3,4/3,6 a intacta apresentou excursão localizada e retornou ao repouso; em 3,8/4 manteve memória localizada; em 4,2/4,4/4,6 tornou-se coletivamente alta, igualando o desfecho restaurado.

Isso demonstra uma faixa **amostrada**, em quatro níveis de gD e seis tempos, em vez de um único ponto. Não determina a área de uma região contínua nem a posição exata de sua fronteira. Não foi detectada janela de restauração nesse intervalo para a variante persistente; os seis tempos deram o mesmo desfecho por gD. A janela histórica da variante excitável é outra pergunta e não foi reavaliada aqui.

![Figura B](fig_mapa_regime.png)

## 5. Mecanismo bistável alternativo

Foi definida uma corrente líquida cúbica escalar, substituindo leak+Kv+corrente sigmoidal:

\[
\dot V_i=\frac{(V_i-L)(V_i-U)(H-V_i)}{\tau(H-L)^2}-\frac{G_J}{C}(\mathcal L V)_i+\frac{I_i}{C},
\quad L=-50\,\mathrm{mV},\ U=-35\,\mathrm{mV},\ H=10\,\mathrm{mV},\ \tau=3,125\,\mathrm{ms}.
\]

A escolha preserva aproximadamente a escala de voltagem e a relaxação linear do repouso baixo do modelo anterior; não iguala corrente regenerativa máxima, altura de barreira ou limiar de recrutamento da rede. É uma lei fenomenológica de corrente total com dimensão de estado diferente, não um novo canal biológico.

**Antes de qualquer teste de rede**, as raízes−50/−35/+10 mV apresentaram autovalores−80/+60/−240 s⁻¹. As dobras ocorreram em−43,02776/−6,97224 mV, com correntes+0,00263826/−0,01819381 A/m². Quatro estados iniciais próximos dos repousos estáveis retornaram aos respectivos ramos sob o mesmo I=0. Duas rampas triangulares,1 e5 s por sentido, comutaram para o ramo alto e retornaram ao baixo. Referências e refinamentos passaram; a bistabilidade se apoia nas raízes e estabilidade, não apenas na presença de laço.

Nos grafos conectados, os estados homogêneos baixo e alto também são equilíbrios: o Laplaciano anula vetores constantes. Seus Jacobianos escalares são F′(V*)I − Gj·Laplaciano/C; como o Laplaciano é positivo semidefinido, os dois ramos permanecem linearmente estáveis. Isso é uma consequência algébrica da formulação, não uma nova simulação. Portanto o resultado negativo não decorre da inexistência desses dois atratores homogêneos.

**Resultado da rede:** nenhum dos 12 pares intacta/interface-restaurada manteve estados finais diferentes. Todos retornaram a−50 mV; maior diferença final entre histórias≈6.94e-18 V. Nas 21 condições cúbicas estimuladas, apenas a fonte cruzou a raiz instável isolada e nenhum receptor a cruzou. Os picos na fonte ficaram entre-32.50 e-14.84 mV, seguidos de recuperação. Cruzar a separatriz da célula isolada não garante comutação da célula acoplada, submetida à carga dos vizinhos.

Esse resultado **não generaliza positivamente o achado ao mecanismo alternativo**. Também não prova que correntes cúbicas sejam incapazes de exibir seleção por história em outros parâmetros: aqui se testou uma formulação e um protocolo fixados, sem recalibrar sua excitabilidade de rede. A bistabilidade isolada não foi suficiente para produzir o desfecho nessas condições. Não foram aumentados estímulos ou alteradas constantes para tentar obter um resultado positivo.

![Figura C](fig_mecanismo_alternativo.png)

## 6. Controles

Seis controles sem estímulo permaneceram no repouso, com maior desvio final 6.94e-18 V. As 12 condições sem corrente adicional retornaram ao repouso; alguns pulsos cruzaram transitoriamente o nível usado na classificação, sem persistência. Dez ablações usam o Kv histórico e duas usam leak puro: no cúbico, desligar Jadd=GL(V−EL)+C·F(V) deixa apenas o leak. Essas ablações não são mecanismos idênticos.

Nos cinco controles persistentes sem restauração, o desfecho dependeu da geometria:

| Configuração | Receptores altos | Nós altos |
|---|---:|---:|
| historica | 0/104 | 122/226 |
| fonte_esquerda | 0/168 | 58/226 |
| fonte_direita | 0/170 | 56/226 |
| geometria_1701 | 110/110 | 226/226 |
| geometria_2701 | 0/109 | 117/226 |

Em geometria_1701, a interface enfraquecida já permitiu recrutamento coletivo sem reconectar. Nas outras quatro, houve persistência no lado da fonte e nenhum receptor alto. A restauração completa faz parte do teste principal, mas **não é necessária para recrutamento em toda geometria**. Sem restauração, os grafos finais diferem; esses controles não contam como pares de memória sob mesma estrutura.

Dos cinco sorteios persistentes em 0,9×, quatro produziram o estado coletivo e um — fonte_direita — manteve ativação localizada. Nos fatores 1/1,1, todos recrutaram coletivamente. Os três sorteios cúbicos estimulados retornaram ao repouso. Assim, a interface geométrica não é a única alteração capaz de selecionar outro estado; os controles pareados sustentam o papel da distribuição das conexões, com efeito dependente da configuração. Um sorteio por variante não caracteriza uma distribuição estatística.

## 7. Auditoria numérica

As 136 trajetórias foram observadas até 5 s e refinadas. DOP853 principal: rtol 10⁻¹⁰, atol 10⁻¹², passo máximo 2,5 ms. Refinamento: rtol 10⁻¹², atol 10⁻¹⁴, passo máximo 1 ms. As 44 referências de rede previamente fixadas usaram Radau com Jacobiano analítico, rtol 10⁻¹¹, atol 10⁻¹³ e passo máximo 2,5 ms. Os seis protocolos isolados também foram refinados e comparados com Radau.

A tolerância de comparação permaneceu **0,02 mV**, acompanhada de concordância da categoria e das contagens finais e de cruzamentos. Erro máximo principal–refinado: **0.000214893 mV**; Radau–refinado: **0.000000011 mV**. Maior erro Radau isolado: 2.91e-10 mV. Falhas iniciais: **0**; correções adicionais: **0**; casos não resolvidos: **0**. Mudanças de classificação entre solvers: **0**.

Todos os estados finais foram estacionários e linearmente estáveis; maior parte real encontrada: -52.175594 s⁻¹. Não houve mudança de categoria entre 2 e 5 s; maior alteração de voltagem nesse intervalo: 2.6e-17 V. A estabilidade foi calculada no Jacobiano completo de cada estado final, não apenas na célula isolada. Não foram acrescentados ensaios de ruído nem um censo global de atratores.

Os eventos de pulso/restauração delimitam segmentos exatos de integração. Picos e primeiros cruzamentos são medidas na grade de saída de 1 ms; o erro entre integradores também é avaliado nessa grade, não como garantia de máximo contínuo entre amostras. A função de classificação é operacional e não identifica potenciais de ação biológicos.

Os quatro Jacobianos de implementação passaram em diferenças finitas antes dos testes de rede. O verificador final recalculou contagens, picos, tempos do primeiro recrutamento e campos CSV/JSONL diretamente das trajetórias; erro nas métricas recomputadas:0. Conferiu 87 pares e seus grafos finais. Duas trajetórias históricas testemunhas foram reproduzidas contra os arquivos antigos dentro da tolerância. Os 584 arquivos anteriores, incluindo o próprio manifesto, permaneceram idênticos por hash; o protocolo e o código executado também conferiram.

Ocorrências operacionais: o primeiro inventário externo tentou usar `.items()` em um JSON que era lista; corrigido o leitor, sem modificação anterior. Um comando de lançamento do verificador tinha caminho incorreto para o log e foi rejeitado pelo shell antes de iniciar a simulação; o caminho foi corrigido. Não foram falhas numéricas, ajustes de modelo ou condições excluídas. Nenhuma nova execução nativa BETSE ou validação de tecido foi realizada.

## 8. Resultados negativos

- A alternativa cúbica não exibiu memória de história em nenhum dos 12 pares testados; nenhum receptor cruzou o nível alto em suas 21 condições estimuladas.
- Nos fatores 1/1,1 do bloco de geometria, as histórias convergiram ao mesmo estado coletivo nas cinco configurações.
- Em gD 4,2/4,4/4,6, o mapa não diferenciou as histórias, pois ambas recrutaram toda a rede.
- As intactas em gD 3,4/3,6 retornaram ao repouso; não se deve chamar toda resposta subcoletiva de memória localizada.
- A restauração não foi necessária para recrutamento na geometria_1701; a interface não foi uma localização exclusiva de efeitos nos controles aleatórios.
- Não foi encontrada fronteira temporal no intervalo 20–500 ms dessa variante persistente.
- Não houve falha de integração ou precisão nos casos concluídos desta etapa. As seis reprovações numéricas antigas continuam preservadas no estudo anterior.

## 9. O que mudou em relação ao estudo anterior

A seleção por história deixou de depender apenas do nó 61 e da configuração histórica: reapareceu nas quatro variantes objetivamente definidas. O mapa ampliou a sensibilidade antiga 3,6/4/4,4 para sete níveis e seis tempos, mantendo o estímulo fixo. Isso fortalece uma conclusão condicionada ao regime e à família da corrente histórica.

A corrente cúbica, em contrapartida, restringe a generalização de mecanismo. Múltiplos atratores disponíveis não garantem que o protocolo de acoplamento e estímulo os selecione de forma diferente. O modelo de corrente, sua força regenerativa, o estímulo e a carga da rede continuam sendo parte da conclusão. A hipótese ampla de suficiência da bistabilidade isolada não foi sustentada por esta comparação.

O resultado antigo sobre reparo permanece **separado**: uma regra que elevou a transmissão graduada pode não favorecer a transição coletiva perto do limiar. Esta etapa não reavaliou esse resultado em novas geometrias ou mecanismos e não autoriza estender sua robustez. A regra anterior foi um ranking comparado a três ordens aleatórias, não uma prova de otimização global.

## 10. Conclusão mínima defensável

**Em redes sintéticas com a corrente persistente sigmoidal e Kv utilizadas aqui, mudanças temporárias de acoplamento podem selecionar estados elétricos estáveis diferentes após restauração da mesma conectividade. O efeito reapareceu em quatro variantes adicionais e em uma faixa amostrada de parâmetros, mas dependeu do estímulo e não foi reproduzido pela corrente cúbica sob o protocolo fixado.**

Formulação em inglês adequada ao alcance observado:

> In the synthetic conductance-based network family tested here, transient changes in intercellular coupling can select distinct stable electrical states despite identical final connectivity. This effect recurred across predefined geometry and source variants and sampled parameter ranges, but was absent in the alternative cubic model under the fixed stimulation protocol.

Respostas aos sete critérios de encerramento: (1) sim, em quatro variantes adicionais; (2) sim, em 24 pontos de uma faixa amostrada, sem fronteira contínua estimada; (3) não, na alternativa fixada; (4) estímulo mais forte, gD ≥ 4,2 nos níveis testados e o mecanismo alternativo eliminaram o contraste; (5) seleção de atrator elétrico condicionada ao modelo e protocolo; (6) manter o resultado principal, restringindo generalidade; (7) os dados fortalecem generalização de geometria/regime e restringem a de mecanismo. Não refutam o contraste histórico, que foi reproduzido.

## 11. Limitações

Variantes pequenas, derivadas de uma geometria comum; topologias e fontes correlacionadas; um único novo sorteio por configuração. Somente um valor de Gj, um tauK, um pulso e uma alternativa cúbica; sem calibração de limiar de rede equivalente entre mecanismos. A alternativa aproxima a relaxação do repouso, mas não todas as propriedades regenerativas da corrente histórica. Nenhuma frequência observada estima prevalência em redes ou sistemas biológicos.

Reservatórios/reversões permanecem fixos. Não há homeostase iônica, canal molecular identificado para a corrente adicional, expressão gênica, proliferação, morfogênese, anatomia, regeneração, eficácia terapêutica ou comunicação radiativa. Estabilidade linear é local; 5 s simulados não são uma escala de memória biológica. Prioridade inédita e adequação editorial a uma revista não foram estabelecidas nesta validação dirigida.

## 12. Implicações para o manuscrito

Apresentar o contraste sob mesmo grafo final como resultado principal computacional, acompanhado de generalização delimitada e do negativo cúbico. Evitar “bistabilidade implica memória de história”, “efeito universal de interface” ou “restauração necessária em todas as redes”. Incluir controles aleatórios e sem restauração junto aos resultados positivos, preservando seus denominadores.

Separar a previsão sobre seleção de estado da conclusão anterior sobre reparo. A teoria motivadora sobre organização celular permanece uma hipótese mais ampla do que a evidência elétrica aqui produzida. Não acrescentar novas simulações a esta campanha para tentar melhorar a narrativa.

## 13. Arquivos para reprodução

- Planejamento/procedência: `PLANO_VALIDACAO.md`, `protocolo_validacao.json`, `congelamento.json`, `auditoria_previa.json`, `originais_sha256.json`, `execucao_validacao.json` e `MANIFESTO_SHA256.json`.
- Geometrias e máscaras: `geometrias.npz`; fontes, regras e arestas no protocolo. A análise usa máscaras explícitas, sem reaproveitar RIGHT/CENTER/ORIGINAL fixos nas variantes.
- Resultados iniciais preservados: `resultados_validacao.jsonl` e `primarias/`.
- Dados efetivos para análise: `resultados_conferidos_validacao.jsonl`, `metricas_validacao.csv` e `refinadas/`; `correcoes/` seria usado apenas para reprovações. As métricas principais finais são derivadas do refinamento, com vínculo explícito aos originais.
- Comparações: `generalizacao_geometrias.csv`, `mapa_regime.csv/json`, `comparacao_mecanismos.csv`, `controles_validacao.csv`, `contrastes_aleatorios.csv`, `resumo_validacao.json` e figuras A–C.
- Mecanismo: `mecanismo_isolado_antes_rede.json` preserva a aceitação anterior à rede; `mecanismo_alternativo.json` acrescenta seus resultados. Trajetórias isoladas em `isolada/`.
- Verificação: `verificacao_numerica.json`, `verificacao_linhas.jsonl`, `radau/`, `AUDITORIA_FINAL_VALIDACAO.json` e logs.
- Código: `preparar.py` audita e congela, `modelo.py` reutiliza equações/Jacobiano históricos por leitura e implementa a corrente cúbica, `executar.py` executa as etapas, `analisar_validacao.py` agrega/figura, `auditar_validacao.py` reconfere dados e hashes, `gerar_relatorio.py` monta este relatório.

Ambiente: Python 3.9.6, NumPy 1.26.4, SciPy 1.13.1, `macOS-26.6.2-arm64-arm-64bit`. Solvers SciPy DOP853/Radau, BLAS limitado a um thread nos comandos. O protocolo preserva o executável e parâmetros; `dependencias_ambiente.txt` registra pacotes. Unidades SI, salvo colunas/figuras explicitamente convertidas a mV ou ms.

Na raiz do repositório, para preparar uma nova pasta irmã sem executar simulações:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-betse130/bin/python research/bioeletricidade-vmem-2026-09-08/validacao_generalizacao_2026-09/reproduzir_validacao.py repeticao_validacao
```

A opção `--run` repete apenas o protocolo congelado e suas verificações, gerando tabelas/figuras e auditoria na cópia. Recusa destino existente. Requer as dependências históricas preservadas na mesma árvore. A preparação e a importação do protocolo foram conferidas em uma pasta irmã nesta entrega; não se executou uma segunda campanha integral em outra pasta. O relatório interpretativo e a inspeção visual não são automaticamente certificados pelo comando de reprodução.

## Recomendação para publicação

**B. Pronto, mas a conclusão precisa ser restringida.** Há evidência numérica consistente de seleção por história na família histórica, com generalização adicional de geometria/fonte e regime. O mecanismo cúbico deu resultado negativo, e a bistabilidade isolada não pode ser apresentada como garantia do fenômeno. A restrição é parte do resultado e deve integrar o manuscrito, sem esconder o teste que não generalizou.

Esta classificação significa prontidão para redigir um manuscrito computacional com esse alcance; não garante novidade, aceitação editorial ou validação biológica. **A campanha de simulação está encerrada.** Nenhum manuscrito anterior foi alterado e nenhum material foi publicado ou enviado externamente.
