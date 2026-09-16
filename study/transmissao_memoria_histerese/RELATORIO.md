# Transmissão, memória, histerese e recuperação em uma rede bioelétrica sintética

Execução principal em 14/09/2026; auditoria e fechamento em 15/09/2026.

**Resultado central:** a consequência de enfraquecer uma interface depende do mecanismo celular, do estímulo e do momento da restauração. No modelo graduado há atenuação e atraso. Na extensão excitável aparece uma janela temporal de transmissão. Na extensão persistente, uma interrupção temporária pode selecionar um estado elétrico que permanece depois da restauração completa. A regra de reparo que melhora o pico graduado pode impedir a ativação coletiva perto do limiar.

São resultados de modelos sintéticos. Não são evidência experimental própria, demonstração de memória anatômica, cura ou descoberta de um fenômeno universal. A bistabilidade foi introduzida deliberadamente como hipótese de mecanismo; observar dois repousos, por si só, não é novidade.

## 1. Pergunta e relação com a teoria principal

O programa investiga se potencial de membrana e acoplamento por junções podem contribuir para coordenação celular e organização de tecidos. Esta etapa testa a parte elétrica dessa cadeia: transmissão → persistência de estado → efeito de restaurar conexões. Não há camada de decisão molecular, proliferação ou morfogênese.

A v2 já utilizava gating não linear de Kv1.5, mas sem corrente despolarizante regenerativa. O presente trabalho mantém esse modelo como controle e acrescenta duas hipóteses de corrente, identificadas abaixo. A comunicação eletromagnética radiativa não foi simulada e não é sustentada por estes resultados.

## 2. Desenho, desenvolvimento e procedência

Reutilizamos a geometria de 226 nós, 622 conexões, fonte no nó61 e região receptora fixa de104 nós. A interface contém32 arestas reduzidas a10% do peso original. Os três controles aleatórios históricos reduzem também32 arestas em90%, retirando o mesmo peso28,8. Reutilizar esses grafos não cria novas réplicas nem apaga seu conhecimento prévio.

O desenvolvimento das novas correntes usou célula isolada e rede original, sem consultar respostas das interfaces alteradas. A inspeção inicial de raízes com gD1/2/4/8 está registrada em `PLANO.md`; todas as tentativas de limiar estão em `tentativas_desenvolvimento.json`. O protocolo de comparação foi congelado localmente em **14/09/2026,21:09:27UTC**, após esse desenvolvimento. SHA-256: `5cbb0be57d3d0a06bf0f8ff971c9db2ded15500a959596ed44f1eb7db40680ba`. Não é pré-registro externo, estudo cego ou avaliação independente de toda a exploração anterior.

| Bloco congelado | Condições rotuladas |
|---|---:|
| Transmissão temporal graduada | 144 |
| Memória e excitação com restauração | 144 |
| Sensibilidade da corrente persistente, sem reajustar o estímulo | 60 |
| Reparo antes de novo pulso | 126 |
| Controles sem estímulo | 9 |
| Controles sem restauração | 4 |
| **Total principal** | **487** |

Alguns controles originais reaparecem em diferentes tempos de restauração, embora o grafo original não mude. A contagem é de condições rotuladas, não de487 sistemas independentes. Não foram calculados valores de p ou inferência populacional. Controles interpretativos posteriores ao congelamento, incluindo36 condições de ablação da corrente adicionada, estão explicitamente separados em `CONTROLES_ADICIONAIS.md`.

## 3. Equações e três regimes

Para correntes aplicadas positivas para dentro:

\[
C\dot V_i=-G_J(LV)_i-G_L(V_i-E_L)-g_Km_i(V_i-E_K)
+g_Da_\infty(V_i)h_i(E_D-V_i)+I_i(t),
\qquad \tau_K\dot m_i=f(V_i)-m_i.
\]

Parâmetros preservados: C=0,01F/m², GL=1S/m², EL=−50mV, gK=2S/m², EK=−79,67507mV e f(V)=logística((V+0,76mV)/14,09mV). τK=14,8ms; no bloco graduado também59,2ms. Gj=1 ou4S/m² no graduado e1S/m² nas extensões.

A corrente nova tem ED=+50mV e a∞(V)=logística((V+25mV)/4mV), com ativação instantânea. Seus parâmetros são inteiramente sintéticos; não representam um canal Na/Ca identificado ou uma parametrização de tecido.

| Variante | Corrente adicional | Comportamento verificado |
|---|---|---|
| Kv1.5 graduado | gD=0 | Repouso único em−51,49748mV |
| Persistente, chamada `bistable` nos arquivos | gD=4S/m²,h=1 | Repousos isolados estáveis em−50,97123 e+7,54715mV; raiz instável em−36,01657mV |
| Excitável | gD=4S/m²,dh/dt=(h∞−h)/100ms;h∞=logística(−(V+40mV)/4mV) | Repouso único em−51,00690mV, excursão regenerativa e recuperação |

As reversões e reservatórios iônicos permanecem fixos. Não simulamos bombas, depleção iônica, metabolismo, ruído de canais, crescimento ou meio extracelular. Somar correntes por área nos nós produz uma grandeza efetiva da redução, não a corrente total de um tecido sem especificar áreas.

Na célula isolada excitável, um pulso de2ms abaixo do limiar produziu pico−38,08493mV no fim do pulso. Acima dele, o pico foi+17,01571mV aos11,6ms, depois de retirar a corrente, seguido de retorno ao repouso. Dois pulsos separados por20 ou100ms produziram uma única excursão; com500ms produziram duas. Os números se referem a este protocolo sintético, não a um período refratário medido biologicamente.

Na rede intacta, pulsos de20ms somente no nó61 localizaram o limiar operacional de recrutamento de pelo menos50% dos receptores em até600ms: **0,08232422–0,08237305A/m²** na variante persistente e **0,12773438–0,12783203A/m²** na excitável. Usamos0,9/1,0/1,1 vezes o limite superior em todos os grafos, sem recalibrá-los.

## 4. Transmissão temporal: a proporção depende do protocolo

O modelo graduado partiu de seu repouso verdadeiro. Aplicamos pulsos de1,10,100ms com carga fixa0,0001C/m² ou corrente fixa0,02A/m². Restauramos todas as conexões aos200ms e observamos até1s. Pico e integral usam a média dos104 receptores em relação ao repouso sem estímulo.

Para **carga fixa**, a interface preservou:

| Duração do pulso | Pico preservado, faixa entre τ e Gj | Área positiva preservada |
|---|---:|---:|
| 1ms | 18,00–27,43% | 23,85–38,06% |
| 10ms | 19,82–31,72% | 23,86–38,06% |
| 100ms | 23,87–38,07% | 23,83–37,88% |

O centro temporal da resposta positiva atrasou aproximadamente2,38–2,75ms. A corrente fixa também mostrou atenuação, com picos preservados18,01–38,05%. Portanto o gargalo não é apenas um atraso, e um percentual único de pico não caracteriza todos os estímulos. Esses percentuais não substituem os17,56–26,17% da v2: houve mudança explícita de repouso inicial, forma do estímulo e horizonte.

## 5. Histerese: atraso cinético versus coexistência de estados

Fizemos varreduras triangulares de corrente em célula isolada, com0,2/1/5s por sentido. No Kv1.5, a área do laço caiu de0,00328215 para0,00067946 e0,00013636V·A/m², comportamento compatível com atraso que diminui em varredura lenta.

Na variante persistente, as dobras da curva estacionária ocorrem em **+0,00669280 e−0,17301836A/m²**. Há coexistência de repousos estáveis em I=0, demonstrada pelo Jacobiano e pela manutenção dos dois estados iniciais sob o mesmo I=0. O laço não depende apenas da velocidade: sua área foi0,02472259 e0,02385131V·A/m² nas varreduras de1 e5s. A rampa mais rápida não chegou a comutar; esse resultado negativo foi mantido.

As varreduras usam corrente entre−0,17801836 e+0,01169280A/m² e atingem tensões negativas fora de uma faixa fisiológica usual. Elas são um diagnóstico matemático do modelo, não um protocolo de bancada recomendado. A coexistência de equilíbrios e sua estabilidade, e não a área isolada do laço, sustentam a conclusão de memória.

![Histerese nos dois modelos](01_histerese.png)

## 6. Memória espacial depois de restaurar a mesma rede

Um contraste particularmente claro ocorreu com o mesmo pulso de20ms e amplitude0,07413574A/m², equivalente a0,9vezes a referência persistente:

| História das conexões | Estado aos2s, com grafo final original |
|---|---|
| Rede intacta durante todo o protocolo | Uma célula acima da raiz instável; nenhum dos104 receptores no estado alto |
| Interface em10% até500ms; restauração completa | Todas as226 células e todos os104 receptores no estado alto |

No primeiro caso, a rede não voltou ao repouso homogêneo: manteve uma ativação **localizada**, com voltagem máxima−12,41690mV. No segundo, alcançou o estado alto homogêneo,+7,54715mV. Assim, o contraste é entre memória localizada e estado coletivo, não simplesmente entre “sem memória” e “com memória”.

Os dois estados foram estacionários, permaneceram até5s e apresentaram estabilidade linear da configuração inteira: maiores partes reais dos autovalores−59,81628 e−80,90642s⁻¹. Perturbações espaciais de até0,1mV retornaram às configurações; isso é uma verificação local, não um censo global de atratores ou teste abrangente de ruído.

A interface10% não recrutou os receptores coletivamente antes da restauração neste exemplo; a primeira passagem do limiar ocorreu aos502ms. Com corte completo, ocorreu aos503ms, **depois** de reconectar. Não houve transmissão através de um corte nulo. Sem restauração, o corte completo manteve os receptores sem recrutamento.

Os controles aleatórios11 e22 não produziram ativação coletiva no pulso0,9. O controle33 produziu quando restaurado aos50,200 ou500ms, mas não aos20ms. Portanto o efeito não é exclusivo de uma interface definida geometricamente.

![Estados dependentes da história](05_estados_espaciais.png)

## 7. Excitação transitória: a restauração tem uma janela

Na variante excitável, a interface10% com restauração aos20 ou50ms permitiu excursões nos104 receptores; restaurar aos200 ou500ms não produziu essas excursões nos estímulos examinados. Todos retornaram ao repouso ao fim da observação. A persistente, ao contrário, pôde manter a ativação do lado da fonte até a restauração tardia.

O desfecho congelado era cruzar−36,01657mV, e não uma classificação biofísica completa de potencial de ação. Em16 condições excitáveis, dois receptores cruzaram esse nível sem uma excursão grande. Por isso, acrescentamos e reportamos separadamente o diagnóstico: pico>−10mV e retorno final a menos de1mV do repouso. Esse critério retira as16 contagens pequenas; os contrastes entre recrutamento completo e ausência de excursão permanecem. Não interpretamos 2/104 cruzamentos como uma onda regenerativa confirmada.

![Todos os resultados de restauração](02_memoria_recrutamento.png)

## 8. Sensibilidade: o contraste não é universal

Nos60 cenários com gD3,6 ou4,4S/m², mantivemos o estímulo definido em gD4, sem reajuste por topologia. Com gD3,6, a interface seguida de restauração ativou coletivamente os receptores, enquanto original e os três controles aleatórios não o fizeram nas combinações testadas. Com gD4,4, **todos** os cinco grafos terminaram com ativação coletiva; o contraste nesse desfecho desapareceu.

Isso delimita uma dependência de regime. Não foi estimado um diagrama de fases contínuo, e variações de±10% não representam incerteza experimental nem robustez a qualquer parâmetro. A taxa de gating, o acoplamento das extensões, a fonte e a geometria continuam restritos aos cenários declarados.

## 9. Reparo: a melhor escolha depende do objetivo e do regime

O reparo foi feito **antes de um novo pulso**, mantendo a lesão restante durante a simulação. Dentro das mesmas32 arestas danificadas, restauramos4/8/16 conexões, com o mesmo acréscimo de peso0,9por aresta. A ordem dirigida veio da integral de|Vi−Vj| em uma trajetória original graduada fixada antes dos resultados reparados; foi comparada a três ordens aleatórias. Não é uma otimização global.

No Kv1.5 graduado, o reparo dirigido aumentou mais o pico médio que cada alternativa aleatória nas27 comparações, com diferenças0,00810–0,04001mV. Na variante persistente, para estímulo0,9, reparar4,8 ou16 arestas pela mesma ordem dirigida deixou **0/104** receptores no estado alto, enquanto todas as três ordens aleatórias deixaram **104/104**. Nos estímulos1,0 e1,1, todas as estratégias recrutaram os104 receptores. A variante excitável também apresentou dependência da escolha das arestas perto do limiar.

Uma interpretação compatível com as equações é a alteração da carga elétrica que a fonte enfrenta. Isso não isola todo o mecanismo causal nem demonstra reparo ótimo. Restaurar o grafo integralmente pode ser útil para recuperar uma resposta graduada e, simultaneamente, impedir uma transição coletiva próxima do limiar. Se o objetivo fosse **evitar** essa transição, a classificação de melhor/pior mudaria. Nenhum desses estados foi rotulado saudável ou patológico.

Restaurar conexões depois que a memória foi escrita não necessariamente a apaga, como mostra a seção6. Já desligar a corrente sintética gD no estado alto devolveu o sistema ao repouso único do modelo original. Esse controle identifica a dependência no mecanismo adicionado, não uma terapia.

![Comparações de reparo](04_reparos.png)

## 10. Auditoria numérica e resultados negativos

Todos os487 cenários foram repetidos com maior precisão. A tolerância de comparação de voltagem foi **0,02mV**, sem relaxamento. Seis cenários falharam inicialmente (`case0148/0149/0150/0151/0405/0414`), com erro máximo0,03175610mV entre soluções, embora as classificações concordassem. Mantivemos os arquivos originais e repetimos somente esses casos em precisão superior e com Radau.

Após a correção, a maior diferença entre os dois níveis mais finos nesses seis casos foi **0,00021017mV**; a maior diferença para Radau foi **0,00000228mV**. Todos passaram. Os outros481 já haviam passado. Os estados finais e as classificações de recrutamento não mudaram.

Além do refinamento integral, foram feitas18 referências Radau no verificador principal,12 adicionais (seis de propagação ativa e seis de histerese) e seis nas correções. Seis trajetórias foram estendidas de2 para5s, preservando as classificações. Os dois estados testemunhas tiveram também Jacobiano completo e retorno após perturbação verificados.

Os36 controles sem a corrente despolarizante, sob os mesmos pulsos das extensões, não produziram picos regenerativos nos receptores e retornaram ao repouso. Os nove controles sem estímulo permaneceram estacionários; maior deslocamento final≈2,94×10⁻¹²mV. As correntes internas de junção cancelaram até≈1,10×10⁻¹⁴A/m² na execução inicial.

Foram preservados: falhas de desenvolvimento do teste de Jacobiano e da busca de raízes, ausência de comutação na rampa rápida, ausência de memória coletiva em certos parâmetros, falha tardia de transmissão excitável, reparos dirigidos que não recrutaram a rede e as seis reprovações de precisão. `verificacao.json` continua corretamente marcado como reprovação da precisão inicial; a aceitação após correção está em `correcao_numerica.json`. Isso não é uma falha ainda escondida nem alteração retrospectiva da tolerância.

Nenhum grafo ponderado foi declarado como nova execução nativa BETSE. A redução em SciPy reutiliza geometria e equações, com regressão histórica, Jacobianos por diferenças finitas e comparação entre integradores. Aprovação numérica não valida fisiologia.

## 11. Alcance, literatura e oportunidade de contribuição

Bistabilidade bioelétrica e memória de repouso já foram estudadas em modelos celulares. Nosso modelo não reproduz quantitativamente os canais e sistemas daquele trabalho. [Law e Levin,2015](https://link.springer.com/article/10.1186/s12976-015-0019-9).

Modelos de coletivos acoplados por junções já investigaram padrões e efeitos de condutâncias. A contribuição desta etapa precisa ser delimitada à comparação controlada e à dependência da história; não à descoberta de que redes bioelétricas podem ter padrões. [Cervera,Alcaraz e Mafe,2016](https://www.nature.com/articles/srep20403).

Melhora paradoxal de condução por desacoplamento parcial já foi observada experimentalmente em tecido cardíaco. Portanto a inversão geral “menos conexão pode permitir mais propagação” também não é inédita. [Rohr et al.,1997](https://pubmed.ncbi.nlm.nih.gov/9012353/).

Interfaces entre tecidos artificiais com propriedades distintas já apresentaram excitabilidade própria. Isso é um precedente próximo, mas não é o mesmo desenho deste estudo, que altera pesos de uma rede de células com parâmetros homogêneos. [Ori et al.,publicado online2022,volume2023](https://www.nature.com/articles/s41567-022-01853-z).

Em planárias, intervenções transitórias nas junções foram relacionadas experimentalmente a alterações persistentes da anatomia regenerada. Nossas simulações não identificam o mecanismo dessas observações nem reproduzem regeneração. [Durant et al.,2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5443973/).

**Conclusão defensável:** nesta família de modelos, a posição e a duração da perda de acoplamento podem selecionar estados elétricos distintos sob as mesmas condições finais; uma regra de reparo orientada pela resposta graduada não se transfere automaticamente ao controle de transições coletivas. Isso fornece uma previsão computacional delimitada e uma comparação de mecanismos. A prioridade inédita da combinação exata não foi estabelecida por esta busca focal.

O elo com a teoria principal foi aprofundado de transmissão para memória elétrica e recuperação dependente da história. Continuam em aberto a identificação de um sistema biológico que sustente essas correntes, a necessidade/suficiência da voltagem para uma decisão molecular e a transferência para anatomia. Um estudo posterior pode testar generalização entre geometrias/fontes e robustez com concentrações variáveis, antes de acoplar uma via molecular escolhida por evidência. Essas são novas etapas; a sequência computacional definida neste relatório está concluída.

## 12. Arquivos e reprodução

- **Resultados para análise:** `metricas_conferidas.csv` e `resultados_conferidos.jsonl`. Seis linhas usam as soluções corrigidas; as originais permanecem em `metricas.csv`/`resultados.jsonl`.
- **Trajetórias:** `caseNNNN.npz` contém t e estado y(V,m[,h]); `precisao_corrigida/` contém as seis soluções substitutas e referências. `respostas_compactas.npz` preserva os resumos iniciais, não incorpora as correções; para análises numéricas precisas usar os arquivos conferidos.
- **Comparações:** `contrastes.json`, `contrastes_temporais.csv`, `contrastes_memoria.csv` e cinco figurasPNG.
- **Procedência e checks:** `protocolo.json`, `execucao.json`, `verificacao*.json`, `correcao_numerica.json`, `referencias_adicionais.json`, `controles_adicionais.json`, `estados_espaciais.json` e `MANIFESTO_SHA256.json`.
- **Métodos:** `core.py`, `desenvolver.py`, `verificar_mecanismos.py`, `histerese.py`, `experimento.py`, `controles.py`, `referencias.py`, `estados_espaciais.py`, `refinar_falhas.py` e `analisar.py`.

Ambiente utilizado: Python3.9.6, NumPy1.26.4 e SciPy1.13.1, no ambiente existente `.venv-betse130`. O manifesto verifica as entradas reutilizadas e as saídas. Manuscritos e dados anteriores não foram alterados; não houve publicação ou envio externo.

Para reconstruir os resumos e figuras sem reexecutar simulações, na raiz do repositório:

```sh
.venv-betse130/bin/python research/bioeletricidade-vmem-2026-09-08/transmissao_memoria_histerese/analisar.py
```

Para preparar uma cópia isolada, com conferência das entradas e sem sobrescrever resultados, usar um nome novo de pasta irmã:

```sh
.venv-betse130/bin/python research/bioeletricidade-vmem-2026-09-08/transmissao_memoria_histerese/reproduzir.py repeticao_histerese
```

Acrescentar `--run` também executa os487 cenários, seu refinamento e eventuais correções numéricas nessa cópia. Isso consome tempo e espaço em disco; os resultados originais ficam preservados. O comando de preparação foi verificado; a repetição integral em uma segunda pasta não foi executada nesta entrega. As comparações de precisão e integradores relatadas acima já foram executadas no estudo principal.
