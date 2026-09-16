# Transmissão, memória, histerese e recuperação

Autorização: pesquisadora solicitou executar a sequência completa, incluindo histerese, em 14/09/2026. Estudo mecanístico computacional, exploratório; não valida tecido ou novidade bibliográfica.

## Hipóteses e separação de desenvolvimento

- H1: reduzir uma interface altera amplitude, tempo do pico e integral da resposta, com dependência da duração do estímulo. O modelo Kv1.5 atual é o controle monostável.
- H2: uma corrente despolarizante persistente pode permitir duas condições elétricas estáveis. Sua presença será uma hipótese estrutural, não descoberta. Testaremos se interrupção temporária e localização das arestas modificam o estado após a restauração completa.
- H3: a histerese quase-estática deve ser distinguida de laços dependentes da velocidade. Confirmar ramos estáveis coexistentes, pontos de dobra e comportamento com varreduras progressivamente lentas.
- H4: sob igual número de arestas e condutância acrescentada, reparos selecionados pela geometria/corrente basal podem recuperar a transmissão de maneira diferente de reparos aleatórios. Seleção sem consultar desfechos reparados.
- Braço comparativo: despolarização com inativação lenta para uma excursão excitável. Verificar célula isolada e propagação original antes de comparar grafos. Falha desse gate será resultado reportado.

Desenvolvimento usa apenas célula isolada e grafo original. Antes dos resultados alterados, congelar JSON com parâmetros, estímulo, máscaras, tempos, grafos e critérios. Não chamar avaliação em grafos já conhecidos de validação biológica ou independente de toda exploração anterior. Preservar todas as tentativas, inclusive configurações sem propagação.

## Modelos

Reutilizar C, fuga, reversões e gate Kv1.5 da linha anterior; peso do canal K g=2 S/m² e τ=14,8 ms, com τ=59,2 ms como sensibilidade no braço graduado. Corrente adicional para dentro: gD*a_inf(V)*h*(ED−V), ED=+50 mV, a_inf=logística((V+25 mV)/4 mV). Ativação instantânea é hipótese de redução. h=1 no modelo persistente; no braço excitável, h_inf=1−logística((V+40 mV)/4 mV), τh=100 ms. Todos os parâmetros novos são sintéticos. Reservatórios iônicos/reversões são fixos; não há balanço metabólico ou morfogênese.

Uma inspeção algébrica inicial, anterior a este arquivo, avaliou gD=1,2,4,8 S/m². Todos produziram três raízes de corrente estacionária na variante persistente. Raízes em V: gD1=[−0,0513778344;−0,0219786973;−0,0197636693], gD2=[−0,0512509910;−0,0310956092;−0,0048816129], gD4=[−0,0509712278;−0,0360165716;0,0075471511], gD8=[−0,0502530976;−0,0409341830;0,0206123594]. Isso é desenvolvimento explícito, não avaliação reservada. Usar gD4 como candidato central por separação clara de raízes, sujeito a verificação de estabilidade e comportamento dinâmico.

## Execução delimitada

1. Verificar repousos/equilíbrios, regressão com núcleo anterior e propriedades do integrador. Simular histerese isolada com rampas ascendentes e descendentes em três velocidades; calcular dobras de equilíbrio e resposta de dois estados iniciais no mesmo I=0.
2. Modelo atual: original, interface10%, três grafos aleatórios anteriores e corte completo; pulsos de 1,10,100 ms com carga constante ou corrente constante; Gj1/4, τ14,8/59,2 ms. Restaurar conexões aos 200 ms e acompanhar até 1 s. Incluir controles sem estímulo. Não sortear novos grafos para o estudo antigo.
3. Desenvolvimento de propagação nas extensões: pulso de 20 ms, máscara inicial nó61; se necessário, máscara de nó61+vizinhos ou domínio esquerdo, com todas as tentativas registradas. Procurar limiar somente no original, depois congelar amplitudes abaixo/perto/acima. Se não houver limiar no intervalo declarado, reportar ausência sem ampliar a busca silenciosamente.
4. Memória: cinco grafos pareados e corte completo, restauração em 20,50,200,500 ms, estímulo idêntico, repouso próprio de cada modelo, observação até 2 s. Amplitudes 0,9/1,0/1,1 vezes o limiar encontrado na rede original. Controles sem estímulo e sem restauração. Refinar tempo/horizonte nos casos selecionados por regra e nos casos numericamente ambíguos. Persistência após restauração requer diferenças de estado sob as MESMAS equações finais, repouso residual pequeno e estabilidade do estado final.
5. Recuperação: grafo com interface10%; orçamento de 4,8,16 das32 arestas danificadas restauradas. Comparar ordem de maior diferença de voltagem integrada no original com três ordens aleatórias restritas às MESMAS32 arestas. Aumentos iguais de peso por orçamento. Aplicar reparo antes de um novo pulso: recuperação de transmissão em lesão persistente, distinta de apagar memória. Incluir reparo total e nenhum reparo. Não afirmar reparo ótimo. Escolher trajetória original de referência antes dos resultados reparados.

## Desfechos e checks

Pico e área positiva da média dos104alvos relativa ao controle sem estímulo; tempo do pico e centro temporal da resposta positiva. Classificação de estado pelas raízes do modelo persistente; fração acima da raiz instável, retenção final, corrente através da interface e recrutamento. No braço excitável, cruzamento do limiar só conta como excursão com recuperação posterior; não chamar resposta de uma célula de propagação na rede inteira.

Integração em trechos com fronteiras exatas de estímulo/corte/restauração. DOP853 com tolerâncias apertadas, refinamento de tolerância/passo máximo e referências Radau com Jacobiano esparso em condições representativas e perto das transições. Tolerância primária de voltagem entre soluções:0,02mV; classificação final deve concordar; estado final estacionário: máximo|dV/dt|<1e−5 V/s, refinando horizonte quando necessário. Frações e latências não usam denominadores de amplitude próximos de zero. Verificar cancelamento da corrente de junção e gates em[0,1]. Para ausência de chegada usar valor ausente, nunca latência zero.

Todas as condições permanecem no relatório, inclusive ausências de memória, reparos piores, falhas numéricas e restrições do braço excitável. Três sementes são cenários computacionais, não réplicas biológicas. Bibliografia focal orienta mecanismos; não reivindicar prioridade inédita para bistabilidade, histerese ou efeitos de comunidade já publicados.
