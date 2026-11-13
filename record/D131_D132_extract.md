# Extrato do registro — D131 e D132 (registro de decisões do projeto; Etapa A)

Fonte: `docs/DECISOES.md` (cópia literal). Saíram os itens puramente operacionais (55, 61, 115, 116, 152, 153, 155, 160). Os 15 itens que estavam em dúvida FICAM (decisão do Martel, prompt 0021); as marcas de dúvida foram retiradas.

### D131 — TESTE DE IDENTIFICABILIDADE: VERDADE DE BASE (HAY 2011) VERIFICADA CONTRA DADOS + DESENHO DECLARADO (NÃO EXECUTADO)
**Data:** 2026-09-29 | **Status:** VIGENTE (verificação + desenho; teste NÃO executado; nada de código de produção) | 204/204 + 1 desabilitado
**Onde se aplica:** D51 (adendo de correção), D96, D123, D127, D130, P53 (pergunta 2), P54; `neuron/hay_profile.py`, `results/hay/`

**1. A VERDADE DE BASE NÃO PRECISA SER A CÉLULA-ALVO (distinção registrada ANTES de escolher o modelo, para não ser
relaxamento oportunista).** A regra da mesma preparação (D121 adendo, D123) protege a FIDELIDADE: o modelo de UM
neurônio real tem de usar âncoras daquela preparação. A IDENTIFICABILIDADE é outra pergunta: é propriedade do PAR
(ESTRUTURA do modelo + PROTOCOLO de medida) — "com estas medidas, nesta estrutura, os parâmetros são determinados?".
Para respondê-la basta um modelo com dendritos REALISTAS (atenuação, EPSP, bAP na faixa medida) e parâmetros
CONHECIDOS; não precisa ser 471129934 nem camundongo V1. A regra continua valendo sem exceção para a fidelidade: o que
o teste de identificabilidade disser NÃO vira configuração de nenhum neurônio.

**2. CANDIDATO: Hay, Hill, Schürmann, Markram & Segev 2011, PLoS Comput Biol 7:e1002107 (ModelDB 139653).**
Disponibilidade: VERIFICADA — ModelDB 139653 baixado (13 .mod, L5PCbiophys1–4, L5PCtemplate, morfologias cell1–3,
conjuntos de modelos com genoma/objetivos/erros); compila no NEURON 9.0.2 sem alteração. Usado: `L5PCbiophys3`
(restringido por disparo em degrau E por BAC — Fig. 4) + `cell1.asc`. **NÃO vendorizado** (código de terceiros; a
procedência é o ModelDB — instrução no REPRODUZIR).
**O que o restringiu (verificado no artigo e nos arquivos):**
- Dados: 11 PCs L5b de **rato Wistar adulto P36**, whole-cell a 33–35 °C (simulação a 34 °C — nenhum .mod lê
  `celsius`; o Q10 está fixo a 34 °C no código); BAC: estatística de Larkum et al. 2001 + traços de 5 células. cell1 é uma dessas células.
- Objetivos dendríticos (Tabela 1 — MEDIDOS): **bAP a 620 µm 45 ± 10 mV; a 800 µm 36 ± 9.33 mV**; Ca-spike pico
  6.73 ± 2.54 mV, largura 37.43 ± 1.27 ms; contagem somática no BAC 3 ± 0; ISI 9.9 ± 0.85 ms. O resto é somático
  (degraus: frequência, adaptação, AHPs, latência, largura).
- **NÃO restringido por:** atenuação estacionária, atenuação de EPSP, Rin dendrítica. Fixados à mão: c_m 1 (soma/
  axônio) e 2 µF/cm² (dendritos), R_i 100 Ω·cm, e_pas −90 mV; Ih apical com distribuição exponencial de Kole et al.
  2006 (fixa, normalizada pelo ramo mais longo); zona quente de Ca 685–885 µm (fixa). Livres no genoma: g_pas por
  região e as densidades ativas. O artigo diz ter "verificado" o efeito do Ih na atenuação ao longo do dendrito
  (declividade com Ih bloqueado "ligeiramente menos íngreme que a experimental") — verificação, não restrição.
- Axônio: substituído por 2 × 30 µm (d = 1 µm) — como o "truncated" do Allen.
Consequência: a atenuação estacionária e a do EPSP são PREDIÇÕES do Hay, não ajustes → o confronto abaixo é um teste
honesto (o modelo não foi puxado para esses números).

**3. CRITÉRIOS DE CONFRONTO — DECLARADOS ANTES DE RODAR** (mesmos pontos/métricas do D127/D130; dados do D130 +
Tabela 1 do Hay; o modelo é de RATO, então o confronto é contra os dados de RATO — Stuart & Spruston 1998 e Williams
& Stuart 2002 passam a ser da mesma espécie; Shai 2015 é camundongo → só reportado):
- **C1 estacionária soma→dendrito** (pulso −50 pA, 1 s, modelo ATIVO a partir do repouso — o protocolo do dado, com
  Ih ligado), no caminho apical mais longo, contra Stuart & Spruston 1998 Fig. 1F (controle): CAI se (a) razão a
  100 µm ∈ [0.6, 1.0]; (b) distância de 50% (interpolação linear no perfil de 100 em 100 µm) ∈ [250, 450] µm
  (medido ~332); (c) razão a 500 µm ∈ [0.05, 0.52] (lido 0.1–0.26, fator 2).
- ~~**C2 EPSP do tufo** (EPSC 10 pA, τr 0.5/τd 3 ms, na ponta apical; modelo ativo): CAI se atenuação local/soma ∈
  [20, 400]× — a MESMA ordem de grandeza dos >40× medidos (o critério com que o D130 julgou 1 091–1 868× "uma ordem
  acima"; a distância do registro de Williams & Stuart não foi verificada → banda larga, declarada).~~ **[MAL
  DECLARADO — D132: local errado (ponta fina, não registrável) e dado de distância não verificada. Redeclaração no
  local do dado tentada: distância NÃO obtida → C2 NÃO VERIFICÁVEL para o Hay.]**
- **C3 bAP** (protocolo e sítios do próprio Hay: 1.9 nA, 5 ms no soma → 1 PA; sítio de maior diâmetro a 620 e
  800 µm): CAI se amplitude (pico − repouso) ∈ média ± 2 DP da Tabela 1: [25, 65] mV a 620 e [17.3, 54.7] mV a 800;
  e o bAP no tronco é DECREMENTAL (não cresce de 100 até 800 µm).
- **Só reportados (não critério):** Rin somática (dado: 32 MΩ S&S; Hay reporta 41.9), Rin local (Shai: camundongo),
  gradiente de repouso dendrito–soma, sag, EPSP nos outros pontos, bAP no protocolo do D130 (2 nA, 2 ms).
- **Convergência:** rodado a Δ = 1 e 0.5 µm (nseg = max(regra do Hay, ⌈L/Δ⌉), biophys reaplicado); vale o veredito
  se não mudar entre os dois; diferenças reportadas.
- **Se NÃO cair: registrar e parar — nenhum parâmetro do Hay é ajustado.**

**4. RESULTADO (Hay biophys3 + cell1; Δ = 1 µm, 12 757 segmentos; Δ 0.5 µm, 25 407 segmentos: máx. diferença **0.27%** em TODAS as métricas, veredito idêntico; Δ 4 µm: ≤2.1%).** Repouso: soma
−77.3 mV (deriva <10⁻⁵ mV/ms após 3 s); Rin somática (−50 pA) **40.2 MΩ** (o artigo: 41.9); apical mais longo
1 300 µm (o caminho mais longo sai do tronco no nexo, ramificação a 627 µm, e termina numa ponta fina do tufo).
| ponto (caminho apical mais longo) | 100 | 200 | 300 | 400 | 500 | 600 | 800 | 1 000 | ponta 1 300 |
|---|---|---|---|---|---|---|---|---|---|
| soma→ponto, −50 pA 1 s (ativo) | 0.85 | 0.69 | 0.55 | 0.45 | 0.37 | 0.30 | 0.16 | 0.067 | 0.023 |
| idem, passivo (canais fora) | 0.92 | 0.84 | 0.76 | 0.70 | 0.65 | 0.60 | 0.48 | 0.36 | 0.30 |
| ponto→soma, −50 pA no ponto | 0.91 | 0.76 | 0.58 | 0.44 | 0.35 | 0.28 | 0.058 | 0.014 | 0.001 |
| Rin local (MΩ), −50 pA | 38 | 37 | 38 | 41 | 42 | 42 | 108 | 167 | 456 |
| EPSP 10 pA, atenuação local/soma | 1.3× | 1.9× | 3.1× | 4.5× | 6.1× | 7.4× | 44× | 140× | **1 226×** |
| bAP (1.9 nA, 5 ms), mV | 65.5 | 48.9 | 47.8 | 43.3 | 35.7 | 29.0 | 15.1 | 6.6 | 3.2 |
| repouso (mV) | −76.9 | −76.2 | −75.1 | −74.1 | −73.1 | −72.1 | −69.2 | −66.1 | −63.6 |
Sítios do próprio Hay (maior diâmetro): **bAP 27.9 mV a 620 µm e 18.7 mV a 800 µm**. Basal (ponta a 282 µm): soma→ponta
0.82, EPSP 152× (ponta fina, Rin 1 433 MΩ). O Ih pesa: a atenuação estacionária com canais é ~1.8× a passiva a 500 µm
e ~13× na ponta; o sag ((pico−estacionário)/pico) vai de 14% (1.16) no soma a 39% (1.64) na ponta do tufo. Comprimento
eletrotônico PASSIVO (Σ ℓ/λ): apical mais longo **1.73 λ** (1 300 µm), basal mais longo 0.52 λ.

**VEREDITO PELOS CRITÉRIOS DECLARADOS NO ITEM 3:**
- **C1 estacionária — CAI.** (a) 0.85 a 100 µm ∈ [0.6, 1.0]; (b) 50% a **351 µm** ∈ [250, 450] (medido ~332);
  (c) 0.37 a 500 µm ∈ [0.05, 0.52]. É PREDIÇÃO (não foi objetivo do ajuste).
- ~~**C2 EPSP do tufo — NÃO CAI.** Na ponta apical (o ponto declarado, critério anatômico do D127): **1 226×**, fora de
  [20, 400]×.~~ **[D132: critério mal declarado; C2 NÃO VERIFICÁVEL — ver D132.]**
- **C3 bAP — CAI, na borda.** 27.9 mV ∈ [25, 65] a 620 µm; 18.7 mV ∈ [17.3, 54.7] a 800 µm (−1.7 e −1.8 DP da média
  da Tabela 1 — o próprio alvo de ajuste do modelo, reproduzido perto do limite); decremental em todo o perfil.
  **[D132 item 10: NÃO convergido no tempo (Euler 0.025). No dt convergido (CVode): 35.1 / 25.4 mV — fora da borda —
  mas o perfil deixa de ser decremental (+1.2 mV de 200 a 300 µm) → C3 NÃO CAI pelo sub-critério estrito.]**
- **CONCLUSÃO: o Hay NÃO passa pelos critérios declarados (falha C2). Registrado e PARADO: nenhum parâmetro ajustado,
  nenhuma banda alargada, o teste de identificabilidade NÃO usa o Hay como verdade de base até decisão.** [D132: com o
  C2 mal declarado e não verificável, o Hay passa C1 e C3 e fica com a transferência de EPSP SEM VERIFICAÇÃO; seguir
  só com C1+C3 é decisão do usuário, com o risco escrito no D132.]

**DIAGNÓSTICO da falha (registrado, NÃO usado para aprovar):**
- A razão do EPSP na ponta é dominada pela impedância LOCAL da ponta fina com extremidade selada (Rin local 456 MΩ →
  EPSP local 5.2 mV), não pelo acoplamento: no mesmo modelo, o EPSP do tufo PROXIMAL / nexo dá 15× (700 µm), 44×
  (800), 67× (900), 140× (1 000), 204× (1 100) — dentro da banda; só a ponta e o penúltimo ponto (559× a 1 200 µm)
  saem. **O erro pode estar no CRITÉRIO que declarei:** comparei uma grandeza de PONTA (ponto que não se consegue
  registrar com patch) com um dado de registro (>40×, Williams & Stuart 2002) cuja DISTÂNCIA não verifiquei — texto
  completo inacessível (só o resumo: "local EPSP amplitude greatest in the apical tuft"). Decidir isso agora, com o
  número à vista, seria alargar a banda depois do dado. Fica para decisão explícita: redeclarar C2 no sítio do dado
  (exige a distância do Williams & Stuart 2002) ANTES de uma nova rodada, ou aceitar a falha.
- **Mesma observação vale RETROATIVAMENTE para o D130:** o "1 868× do perisomático, uma ordem acima" também era na
  PONTA. A conclusão do D130 sobre os ajustes do Allen NÃO muda: nos pontos de TRONCO o perisomático dá 125× (300 µm)
  e 1 091× (500 µm) contra 3.1× e 6.1× do Hay, e a estacionária já falhava por ~8×. Mas a frase "EPSP ~10× acima"
  do D130 deve ser lida como "na ponta" — registrado aqui, não reescrito lá.

**5. HIPÓTESE "o rato é o caso MAIS DIFÍCIL" — NÃO VERIFICADA (registrada como hipótese, com o que se mediu).**
Medido: o apical de cell1 tem **1 300 µm** (camundongo V1: 409 ± 64 µm, Galloni 2020; a célula-alvo 471129934:
540 µm) e **1.73 λ passivos**. Para comparar é preciso o comprimento ELETROTÔNICO do camundongo, que depende de R_m,
R_i e diâmetro do camundongo — exatamente a lacuna do item 6. Dois argumentos em sentidos opostos, ambos não
testados: (i) mais λ entre soma e tufo → mais atenuação → pontos distais menos VISÍVEIS do soma (mais difícil para
o D51/visibilidade); (ii) uma árvore eletrotonicamente COMPACTA dá pouca diferença entre pontos → parâmetros
REGIONAIS (R_m apical vs basal, Ih por região) se separam PIOR → pode ser mais difícil para a IDENTIFICABILIDADE.
"Mais difícil" depende de qual das duas perguntas; o teste (item 7) mede a segunda.

**6. A LACUNA DE DADOS (camundongo) — busca refeita.**
- **Beaulieu-Laroche et al. 2018 (Cell 175:643):** versão aberta ENCONTRADA (PMC6197488). É **rato vs humano**, sem
  camundongo. Rato: Sprague Dawley 3–7 meses, córtex temporal de associação (TEA), 34–36 °C, degraus de −500 pA
  estacionários: **50% soma→dendrito a 277 [248, 305] µm; dendrito→soma a 453 [406, 531] µm**; Rin do dendrito distal
  **15.7 [13.7–19.5] MΩ**; EPSP 50% a 408 [328, 470] µm. (Lido por extração automática da página; conferir no PDF antes
  de usar como critério.) Hay, para comparação (não critério declarado): 50% soma→dendrito a 351 µm; Rin 38–42 MΩ no
  tronco até 600 µm.
- **Beaulieu-Laroche et al. 2021 (Nature 600:274, "Allometric rules…"):** PDF aberto obtido. TEM **camundongo**
  (C57BL/6 machos, 12–28 semanas, **TEA**, 34–36 °C), com registros DENDRÍTICOS (distais a 280–400 µm, proximais a
  30–80 µm): Rin dendrítica, sag, espículas dendríticas, condutâncias HCN/Kv por outside-out — mas **registro em
  UM sítio** (sem razões de atenuação), números só nas figuras (não lidos).
- **Marti Mengual et al. 2020 (J Neurosci 40:8799, PMC7659461):** **camundongo** C57BL/6 machos 10–12 semanas, ACC
  e **S1**, 34–37 °C, **registro DUPLO soma–dendrito**: ACC estacionária soma→dendrito 0.58 ± 0.03 a ~193 µm
  (λ_S→D 392 µm), dendrito→soma 0.83; EPSP rápido (τ 0.5/2 ms) λ_D→S 252 µm (ACC) e **251 µm (S1)**.
- **Francioni et al. 2019 (eLife, V1):** imagem de Ca + patch somático — sem registro duplo.
**Continua sem dado de atenuação em camundongo V1.** O mais próximo: camundongo S1/ACC adulto (Marti Mengual 2020).
Importa para FIDELIDADE (o alvo 471129934), não para a identificabilidade.

**7. DESENHO DO TESTE DE IDENTIFICABILIDADE — DECLARADO, NÃO EXECUTADO.** Tudo abaixo é fixado ANTES de qualquer
ajuste; mudanças posteriores entram como adendo com motivo, nunca como retoque silencioso. Escrito sobre o Hay
(parâmetros, protocolos, sítios); vale para qualquer verdade de base que passe o item 3 — **com o Hay reprovado em
C2, o teste ESPERA** a decisão do item 8.

**7.1 Parâmetros (Θ, 30 — a "configuração" do D123; o catálogo fica FIXO: as 11 cinéticas do Hay, reversões
e_K −85 / e_Na 50, temperatura 34 °C).** Espaço de busca em log; limites = os do genoma do Hay onde existem, ×[0.1, 10]
em torno do valor verdadeiro onde o Hay fixou à mão.
| grupo | parâmetros | n |
|---|---|---|
| passivo por região | g_pas {soma, axônio, basal, apical}; c_m {soma+axônio, dendritos}; R_i (uniforme, como o Hay); e_pas | 8 |
| soma | NaTa_t, Nap_Et2, K_Pst, K_Tst, SKv3_1, SK_E2, Ca_HVA, Ca_LVAst, Ih; CaDynamics (γ, decay) | 11 |
| apical | NaTa_t, SKv3_1, SK_E2, Im, Ca_LVAst (zona), Ca_HVA (zona), CaDynamics (γ, decay); Ih (amplitude, escala de comprimento da exponencial) | 10 |
| basal | Ih | 1 |
| **total** | | **30** |
Nível 1 (esta declaração): FORMAS espaciais do Hay conhecidas (exponencial do Ih, zona de Ca 685–885 µm), amplitudes
livres — identificabilidade ESTRUTURAL com a estrutura certa. Nível 2 (depois, declarar antes): formas livres (densidade
por trecho entre pontos de penetração) — o caso realista em que a forma também é configuração.

**7.2 Medidas (o protocolo do HANU simulado).** Geometria do scan: morfologia (comprimentos, diâmetros, topologia).
Em cada ponto de penetração p:
- **M1 degrau local:** −50 pA e +50 pA, 1 s, em p → V(t) em p (Rin local, sag, τ, estado estacionário);
- **M2 transferência:** durante M1, V(t) em TODOS os outros pontos e no soma (matriz de transferência com dinâmica);
- **M3 bAP:** 1.9 nA, 5 ms no soma (o protocolo do Hay) → V(t) em p (amplitude, largura, atraso);
- **M4 despolarizante local:** corrente tipo EPSC (τr 0.5/τd 5 ms) em p em 3 amplitudes (sublimiar, limiar, 3× —
  o "CaBurst" do Hay) → V(t) em p e no soma;
- **M5 soma (sempre):** degraus 0.78 / 1.0 / 1.9 nA, 2 s (os do Hay) → V(t) no soma.
Resíduo: traços completos amostrados a 0.1 ms nas janelas dos protocolos, divididos por σ_V.

**7.3 Método de recuperação.** [**Refinado pelo D132 item 4:** dados do Hay COMPLETO convergido, ajuste da ÁRVORE
REDUZIDA do D126 com parâmetros por região — sem crime inverso.] (0) **Sensibilidade local** em Θ_verdadeiro: J = ∂(medidas normalizadas)/∂(log Θ)
por diferença central (passo 1%); SVD → direções mal determinadas (valor singular < 10⁻³·σ_max) — DIAGNÓSTICO,
não veredito; barato, roda por espaçamento antes dos ajustes. (1) **Ajuste:** mínimos quadrados não lineares
(scipy `least_squares`, trust-region, em log Θ, com limites), **20 partidas** log-uniformes nos limites (semente
fixa). (2) **Fase com ruído:** intervalo de 95% por **verossimilhança de perfil** para cada parâmetro.
Modelo direto = o MESMO do dado na fase 1 (crime inverso admitido e declarado: isola identificabilidade estrutural);
na fase 2 o dado vem do Hay a Δ 0.5 µm e o ajuste roda a Δ 1 µm (ou no reduzido do D126 SE antes verificado no Hay
pelos critérios do D129 — o Hay tem distribuições não uniformes que a redução ainda não carregou).

**7.4 Critério de "recuperado" (por parâmetro) e de SUFICIÊNCIA (funcional).**
- Fase 1 (dado perfeito): parâmetro RECUPERADO se TODAS as partidas que atingem o piso do custo (≤10⁻⁸ do custo
  inicial mediano) dão |θ̂/θ − 1| ≤ 1%.
- Fase 2 (ruído): RECUPERADO se o intervalo de perfil de 95% ⊂ [θ/(1+τ), θ·(1+τ)], com τ por classe: g_pas, c_m,
  R_i **10%**; e_pas **±1 mV**; Ih (amplitude e escala) **15%**; densidades de Na/K/Ca/SK/Im **25%**; CaDynamics
  (γ, decay) **50%** (só vistos pela voltagem através do SK). Os τ rotulam; NÃO decidem.
- **Decide a SUFICIÊNCIA — conjunto de teste funcional T, FORA do ajuste:** (a) EPSC de 10 pA em 30 pontos
  sorteados uniformemente por comprimento na árvore (semente fixa) + os pontos do D127 → pico e tempo de pico do EPSP
  no soma; (b) BAC do Hay (EPSP 0.5 nA a 620 µm + 1.9 nA no soma 5 ms antes) e CaBurst (3× EPSP) → contagem e tempo
  dos PA somáticos; (c) f-I somática nos degraus do Hay → taxa por ISI (métrica contínua, D130). Limiares: EPSP
  somático |Δ| ≤ 5% em TODO ponto; contagem idêntica e 1º PA ≤ 1 ms no BAC/CaBurst; taxa ≤ 2%.
- **PARÂMETRO FUNCIONAL** = aquele cuja faixa não determinada move T além dos limiares; **MAL DETERMINADO SEM
  CONSEQUÊNCIA** = não recuperado, mas todo Θ do conjunto-solução (as partidas no piso + os extremos dos perfis) passa
  T. O protocolo é **SUFICIENTE** num espaçamento se todo o conjunto-solução passa T — **identificabilidade parcial
  basta** quando só os sem consequência ficam soltos. Classificação a priori (±25% em cada θ, efeito em T) é
  reportada como descrição, não como critério.

**7.5 Sequência.** [**Fase 2 SUBSTITUÍDA pelo D132 item 3:** ruído vira SAÍDA — varredura por fonte até a falha;
os valores fixos abaixo ficam só como registro.] Fase 0 (sensibilidade) → **Fase 1: medidas PERFEITAS** (identificabilidade estrutural) → só
então **Fase 2: RUÍDO realista**, declarado: ruído de voltagem branco σ_V = 0.2 mV; offset desconhecido por
penetração U(−2, 2) mV (potencial de ponta/junção; parâmetro incômodo ajustado); ganho de corrente ±5% por ponto
(incômodo); posição do ponto ao longo do ramo σ = 5 µm; geometria do scan: diâmetro σ = 0.2 µm por seção
(resolução óptica) e comprimento 2%, mais fator de escala global de diâmetro ∈ {0.9, 1.0, 1.1} testado à parte.
Os valores de ruído são ESCOLHA DE DESENHO (ordem de grandeza de patch e de óptica), abertos à correção antes de rodar.
Fase 3 (depois): Nível 2 (formas livres).

**7.6 Variável de desenho — espaçamento.** Pontos a cada s µm de caminho em cada ramo:
- uniformes s ∈ {∞ (só soma — o que o Allen e o próprio Hay tiveram), 400, 200, 100, 50, 25}, em duas variantes:
  (a) ÁRVORE TODA, (b) só os caminhos do D127 (basal e apical mais longos);
- **critério do D51**: s = λ_local e s = λ_local/2, com o λ VERDADEIRO (oráculo — o D51 como se λ fosse conhecido);
- **protocolo ADAPTATIVO** (a hipótese do adendo ao D51): 1º passo 100 µm; depois s_{k+1} = α·λ̂_k, α ∈ {0.5, 1},
  com λ̂_k = −Δx / ln A_k (atenuação estacionária MEDIDA entre os dois últimos pontos do mesmo caminho) corrigido
  pelo diâmetro do scan (λ ∝ √d). **Observação analítica registrada (não testada):** Rin local + diâmetro NÃO dão λ —
  num cilindro Rin ∝ √(R_m·R_i)/d^{3/2}, só o PRODUTO; λ = √(R_m·d/4R_i) exige a RAZÃO. A versão "scan lê o diâmetro,
  a sondagem dá a resistência local" do adendo ao D51 não fecha sozinha: precisa de um segundo ponto (atenuação) ou de
  R_i/c_m assumidos. Por isso o adaptativo acima usa a atenuação entre pontos.
- **Reportar:** por espaçamento, quais parâmetros foram recuperados, se o protocolo é suficiente (T), e o número de
  penetrações; **s\*** = o maior espaçamento suficiente na fase 1 e na fase 2; onde caem o critério do D51 e o
  adaptativo em relação a s\* (em µm, em λ e em número de pontos).

**7.7 Custo (medido nesta verificação; rodadas concorrentes, então tempos pessimistas).** Hay a Δ 1 µm: degrau de
1 s (CVode) ~18 s por ponto; 100 ms em passo fixo ~25 s. A Δ 4 µm (3 260 segmentos; métricas a ≤2.1% de Δ 1):
~4 s e ~8 s. Um conjunto de medidas na árvore toda a s = 100 µm (~126 pontos) custa horas a Δ 1 — J por diferença
central (60 conjuntos) e 20 partidas × dezenas de iterações ficam em semanas a meses. Portanto: modelo direto a Δ 4
(verificado contra Δ 1 por protocolo antes) ou o reduzido do D126 (verificado no Hay antes), paralelismo, e a fase 0
decide quais espaçamentos/variantes seguem para ajuste completo — decisão registrada com motivo.

**8. PENDENTE (decisões do usuário, nada executado):** (a) C2: redeclarar no sítio do dado (requer a distância do
Williams & Stuart 2002 — texto completo não acessado) ANTES de rodar de novo, ou aceitar a reprovação do Hay e buscar
outra verdade de base; (b) com verdade de base aprovada: fase 0 → fase 1 → fase 2 do item 7; (c) valores de ruído
do 7.5 abertos à correção; (d) lacuna de atenuação em camundongo V1 segue aberta (fidelidade).

---


### D132 — C2 NÃO VERIFICÁVEL; RUÍDO VIRA SAÍDA (ESPECIFICAÇÃO DO SENSOR); PERGUNTA REALISTA (HAY COMPLETO → ÁRVORE REDUZIDA); REDUÇÃO DO D126 VERIFICADA NO HAY
**Data:** 2026-09-29 | **Status:** VIGENTE (decisão + desenho; teste de identificabilidade NÃO executado; nada de código de produção) | 204/204 + 1 desabilitado
**Onde se aplica:** D51 (adendo 2), D126, D128, D129, D130 (item 3 riscado), D131 (C2 riscado, item 7 refinado), P54; `neuron/hay_reduce.py`, `results/hay_reduce/`

**1. DUAS CORREÇÕES AO RACIOCÍNIO (registradas).**
(a) O adaptativo do D51 NÃO fecha com Rin local + diâmetro (dá √(R_m·R_i); λ exige a razão) → precisa da atenuação
entre DOIS pontos ou de c_m assumido → **no mínimo DOIS pontos POR REGIÃO**. Conferido: o M2 do D131 (transferência
entre todos os pares) cobre isso. Regra do 7.6 explicitada: em cada região (basal, tronco apical, tufo) o adaptativo
põe dois pontos antes de usar o λ̂ daquela região; até lá usa o λ̂ do pai × √(d/d_pai). (Adendo 2 no D51.)
(b) **O C2 foi MAL DECLARADO** — família "métrica no LOCAL ERRADO": comparou a atenuação do EPSP na PONTA FINA do tufo
(não registrável por patch; razão dominada pela impedância local, 456 MΩ) com um dado de distância não verificada.
**Vale para trás:** o "1 868×, uma ordem acima" do D130 era na ponta → RISCADO com o motivo; a conclusão do D130 sobre
o Allen se mantém pela estacionária, pelo bAP e pelo EPSP no TRONCO.

**2. DECISÃO DO C2 (do usuário): redeclarar no LOCAL DO DADO, com condição.** Argumento independente do resultado:
patch é feito no TRONCO, não em pontas finas. **CONDIÇÃO: a coordenada vem do ARTIGO, nunca da faixa onde o Hay passa
— o intervalo 700–1 100 µm JÁ FOI VISTO passando; escolhê-lo seria o padrão do 0.01.**
**Busca da distância de Williams & Stuart 2002 (Science 295:1907):** texto completo 403; Unpaywall "closed"; Semantic
Scholar sem PDF aberto; PubMed só com o resumo ("EPSPs generated at known dendritic sites… >40-fold" — sem distância);
citações em trabalhos abertos (Ramaswamy & Markram 2015 PMC4481152; Froemke et al. 2010 PMC3059711; 2025 PMC12213790;
Letzkus et al. 2006 PMC6674691; Atkinson & Williams 2009 PMC2724330) — nenhuma dá a distância do registro.
**→ DISTÂNCIA NÃO OBTIDA. Nenhum local escolhido. C2 = NÃO VERIFICÁVEL para o Hay.**
**Outras fontes de atenuação de EPSP com local declarado (busca pedida; NENHUMA aplicada como critério):**
| fonte | preparação | o que dá | por que não vira C2 aqui |
|---|---|---|---|
| Stuart & Spruston 1998 (PDF, Janelia) | rato Wistar 3 sem., S1, 35–37 °C | EPSP sináptico registrado a ~400 µm (Fig. 6) — só TRAÇOS; "Cs aumenta o pico somático 15 ± 4%" | sem razão numérica dendrito/soma |
| Atkinson & Williams 2009 (PMC2724330) | rato Wistar P9–42, 35–37 °C | local ANATÔMICO (58 ± 5 µm abaixo da borda L1–L2); transferência estacionária 2.9 ± 0.7 mV/nA vs 28.9 ± 3.2 somática (Fig. 3B, adultos) | o local é por CAMADA; a morfologia do Hay não traz as camadas → mapear exigiria escolher |
| **Beaulieu-Laroche et al. 2018** (manuscrito do autor, MIT DSpace — **conferido no PDF**) | rato Sprague Dawley 3–7 meses, TEA, 34–36 °C | EPSC injetado (forma na Fig. S4, não lida): 50% de atenuação do EPSP rumo ao soma a **408 [328, 470] µm** (n=13; ajuste logístico, IC por bootstrap); rumo ao dendrito 474 [442, 513] | fonte DIFERENTE da declarada, área/idade diferentes, forma do EPSC não conferida, eixo pode ser a SEPARAÇÃO entre eletrodos (registros multi-sítio) |
**Informação (NÃO critério — o número já existia nos dados do D131):** no Hay, o EPSP de 10 pA (τ 0.5/3 ms) cai a 50%
no soma a ~215 µm do caminho apical (1.9× a 200, 3.1× a 300 µm). Se a fonte de Beaulieu-Laroche fosse adotada, a
transferência de EPSP do Hay pareceria MAIS atenuada que a do rato TEA adulto (408 µm) — com todas as ressalvas da
tabela. Registrado para o risco, não para decidir.
**RISCO ESCRITO (a decisão de seguir só com C1 + C3 é do usuário):** o conjunto funcional do teste (D131 7.4) inclui o
EPSP somático de 30 locais sorteados; com o C2 não verificável, a transferência de EPSP da verdade de base fica SEM
verificação contra dado — o teste mediria a identificabilidade de uma transferência que pode não ser a fisiológica.
Isso não invalida a pergunta estrutural (identificabilidade é do par estrutura + protocolo), mas limita o alcance do
"s\*" e da especificação do sensor a dendritos com transferência como a do Hay.

**Conferência do Beaulieu-Laroche 2018 no PDF (antes de qualquer uso):** os números da extração automática BATEM
(estacionária rumo ao soma 453 [406, 531] µm; rumo ao dendrito 277 [248, 305] µm; Rin distal 15.7 [13.7–19.5] MΩ; EPSP
408 [328, 470] µm); preparação acrescentada: Sprague Dawley 3–7 meses, TEA, 34–36 °C, degraus de −500 pA, 50% por
ajuste LOGÍSTICO com IC por bootstrap. Ressalva nova: os registros são multi-sítio (inclusive dendrito–dendrito); o eixo
das Figs. 3E/F pode ser a separação entre eletrodos, não a distância ao soma.

**3. RUÍDO VIRA SAÍDA — VARREDURA (substitui a fase 2 de ruído fixo do D131 7.5).** Os níveis de ruído não são
escolhidos: o sensor não existe. **Assim como o espaçamento sai como s\*, o ruído sai como ESPECIFICAÇÃO DO SENSOR:**
"o elemento precisa medir voltagem com erro < X, posição < Y, diâmetro < Z" — derivado, não escolhido.
**Declarado antes de rodar:**
- Uma fonte por vez (as outras em zero), em grade crescente:
  | fonte | grade |
  |---|---|
  | ruído de voltagem branco por amostra (0.1 ms), σ_V | 0, 0.01, 0.03, 0.1, 0.3, 1, 3 mV |
  | offset por penetração (uniforme ±a; respostas usadas SUBTRAINDO a linha de base → só afeta leituras de repouso) | a = 0, 0.5, 1, 2, 5, 10 mV |
  | erro de ganho de corrente por ponto (multiplicativo, NÃO ajustado — calibração) | 0, 1, 2, 5, 10, 20% |
  | erro de posição do ponto ao longo do ramo, σ | 0, 1, 2, 5, 10, 20, 50 µm |
  | erro de diâmetro do scan por seção, σ absoluto | 0, 0.05, 0.1, 0.2, 0.5, 1.0 µm |
  | fator de escala global do diâmetro | 1, ±2%, ±5%, ±10%, ±20% (os dois sinais) |
  | erro de comprimento por seção (relativo) | 0, 1, 2, 5, 10% |
- ~~Em cada nível: **5 realizações** (sementes fixas); o nível é TOLERADO se o protocolo é SUFICIENTE (conjunto
  funcional do D131 7.4 dentro dos limiares) em **≥ 4 de 5**.~~ **[SUBSTITUÍDO pelo item 7, antes de rodar: 4/5 tem
  IC 95% de [0.28, 0.99].]** **Máximo tolerado** = o maior nível da grade tal que ele
  e todos os menores são tolerados (regra monotônica, como a de resolução do D128).
- Espaçamento: a varredura roda em s\* (o maior suficiente com medidas perfeitas) e em s\*/2 — espaçamento mais fino
  pode tolerar mais ruído; os dois reportados.
- **Verificação combinada:** todas as fontes a METADE dos seus máximos, simultâneas, 5 realizações; se falhar,
  reporta-se a interação (a especificação NÃO é apertada por fator escolhido depois).
- Saída: tabela "especificação do sensor" (X, Y, Z…) com o espaçamento a que vale.

**4. A PERGUNTA MAIS REALISTA (refina o D131 7.3).** Medidas simuladas no **Hay COMPLETO convergido** (a célula
"real"); ajuste da **ÁRVORE REDUZIDA do D126** a elas — a situação exata do implante (modelo reduzido parametrizado por
medidas de uma célula completa). A árvore reduzida tem parâmetros POR REGIÃO (os 30 do D131 7.1, formas de Ih e zona
de Ca como funções de distância por região); a verdade tem valores POR SEÇÃO/SEGMENTO → **a suficiência é decidida
pelo CONJUNTO FUNCIONAL fora do ajuste**, não parâmetro a parâmetro (como já declarado). A fase 1 "perfeita" passa a
ser: dados do Hay completo sem ruído, modelo direto = reduzido (não há mais crime inverso).
**PREMISSA (registrada):** confundir erro de redução com falta de identificabilidade é pouco provável — o erro do
método foi ~10⁻⁵ no Allen (D126/D129). **Verificada no Hay ANTES** (item 5).

**5. VERIFICAÇÃO DA REDUÇÃO DO D126 NO HAY — CRITÉRIOS DECLARADOS ANTES DE RODAR.**
Protocolos (P), idênticos no L0 e no reduzido, a partir do repouso (3 s, CVode; estado salvo):
P1 repouso nos pontos; P2 −50 pA no soma, 1 s (soma→ponto, Rin, sag); P3 −50 pA em cada ponto (ponto→soma, Rin local);
P4 EPSC 10 pA (τ 0.5/3) em cada ponto (pico local e somático); P5 bAP (1.9 nA, 5 ms); P6 f-I: degraus de 1 s
(atraso 300 ms, 1 500 ms, dt 0.025 — o protocolo do D128) a 0.2, 0.4, …, 2.0 nA, detector IPFX; P7 BAC (1.9 nA 5 ms
no soma + EPSP 0.5 nA τ 0.5/5 ms no sítio hay_620 5 ms depois), CaBurst (EPSP 1.5 nA sozinho) e EPSP 0.5 nA sozinho
— PAs no soma e pico/largura do Ca-spike no sítio. Pontos: os do D131 (critério do D127 + perfil a cada 100 µm +
sítios do Hay). No reduzido, ponto = pesos exatos sobre os compartimentos (junções por Kron, `point_C`).
Densidades no reduzido: cada compartimento recebe os valores do L0 FINO no seu centro (todos os parâmetros de cada
mecanismo + e_K/e_Na), sem média por região — isto verifica o MÉTODO; a parametrização por região é do teste.
- **Referência L0 convergida:** Hay a Δ 0.5 µm; convergência Δ 1 → Δ 0.5: P1–P5 ≤ 1%; P6 pelo critério do D128
  (mesma contagem, latência ≤ 2%, adaptação ≤ 2%); P7 mesma contagem e 1º PA ≤ 2%. Se não convergir: reportar e parar.
- **V1 — exatidão do método no limite (a premissa):** reduzido com n por seção = nseg do L0 a Δ 1 µm (soma com 1
  segmento nos dois, convenção do D126), densidades amostradas DESSE L0, contra esse L0: P1–P5 |erro| ≤ 10⁻³; P6 (em
  0.6, 1.2, 2.0 nA) e P7: mesma contagem, tempos de PA ≤ 0.05 ms.
- **V2 — nível A ("reproduz o modelo que recebe", critérios do D128/D129)** contra o L0 convergido, N por ramo ∈
  {1, 2, 4, 8, 16, 32}: portão em P2/P3/P4 (razões, Rin, EPSP) e P5 (bAP) ≤ 10%; P6 pelos critérios do D123
  (`compare_active.py`); P7 mesma contagem. Menor N = o menor com portão em N e em TODOS os N mais finos da grade.
- **V2 — nível B ("usável no teste sem confundir")**: erros ≤ 1/5 dos limiares funcionais do D131 7.4 — EPSP somático
  ≤ 1% em todo ponto; BAC/CaBurst mesma contagem e 1º PA ≤ 0.2 ms; taxa f-I (1/ISI médio, degraus com ≥2 PA) ≤ 0.4%;
  e as grandezas medidas pelo elemento (P2/P3 razões e Rin, P5 bAP) ≤ 1%. Menor N pela mesma regra monotônica. Se
  nenhum N ≤ 32 passar: a árvore reduzida NÃO serve de modelo direto sem confundir erro de redução com
  identificabilidade — reportado, nada ajustado.

**6. AJUSTE 1 (2026-09-29, do usuário) — SEGUIR COM C1 + C3; O C2 VIRA ANÁLISE DE SENSIBILIDADE.**
**Decisão:** o Hay é a verdade de base sob C1 e C3.
**Viés de SINAL MISTO (não "conservador"):** a única fonte com local declarado (Beaulieu-Laroche 2018, com as ressalvas
do item 2) sugere que o Hay ATENUA MAIS o EPSP que a célula real (50% a ~215 µm vs 408 µm). Isso é PESSIMISTA para o
espaçamento (pontos distais menos visíveis → s\* menor que o necessário) e pode ser OTIMISTA para a separação de
parâmetros por região (árvore menos compacta separa melhor).
**Sensibilidade:** o teste roda também numa VARIANTE do Hay com a transferência de EPSP deslocada para 50% a ~408 µm.
Os DOIS valores conhecidos (215 e 408) são os EXTREMOS — derivados, não escolhidos. **Declarado antes de construir a
variante:**
- d50 = distância no caminho apical mais longo (tronco) em que o EPSP de 10 pA (τ 0.5/3, o do D131) cai a 50% no soma
  (razão pico somático/pico local), interpolação linear entre pontos a cada 50 µm; alvo **408 ± 5 µm**, a Δ 1 µm,
  passo fixo 0.025 ms.
- **Família F1 (tentada primeiro): c_m dendrítico × k** (basal + apical; soma/axônio intactos), k por bisseção em
  [0.1, 1]. Motivo: c_m foi FIXADO À MÃO pelo Hay (2 µF/cm², correção de espinhas), e age só no transitório — a
  estacionária (C1, verificada) não muda. **Previsão analítica registrada ANTES:** com c_m → 0 a razão do EPSP tende à
  razão ESTACIONÁRIA ponto→soma, cujo 50% no Hay está a ~358 µm (D131) → F1 provavelmente NÃO alcança 408.
- **Família F2 (só se F1 não alcançar): R_i global × k** — o outro parâmetro passivo fixado à mão (100 Ω·cm); dado
  independente: 70–100 Ω·cm (Stuart & Spruston 1998). Reportar se o k necessário cai dentro dessa faixa.
- (F3, densidade do Ih apical, fixada à mão a partir de Kole 2006: registrada, não tentada.)
- A PRIMEIRA família que alcançar 408 ± 5 µm define a variante. **Na variante: C1 e C3 reavaliados** com as bandas
  originais. **Se não respeitar: é informação** — as duas fontes (Stuart & Spruston/Hay para C1–C3; Beaulieu-Laroche
  para o EPSP) seriam INCONSISTENTES dentro desta estrutura de modelo — registrar, sem ajustar.
- **Saída:** s\* e a especificação do sensor nos DOIS extremos. Parecidos → o C2 não importa para o resultado.
  Diferentes → a especificação carrega a incerteza, escrita com os dois números.

**7. AJUSTE 2 (2026-09-29, ANTES de executar a varredura) — A REGRA "4 EM 5" É FRACA DEMAIS PARA UMA ESPECIFICAÇÃO.**
Com n = 5, 4/5 tem IC 95% (Clopper–Pearson) de **[0.28, 0.99]** — não distingue sensor confiável de sensor que falha
em dois terços dos casos. **Substitui a regra do item 3:**
- **Taxa exigida p_req = 0.90, demonstrada com 95% de confiança** (limite INFERIOR unilateral de Clopper–Pearson ≥
  0.90). Justificativa: é um requisito de hardware por implante — "o protocolo dá um modelo suficiente em ≥ 90% das
  células"; 95% é a confiança usual; exigir 0.95 dobraria o custo (n ≥ 59 só com ZERO falhas).
- **Sequencial, com parada só por FUTILIDADE** (não infla a taxa de falso "passa"): olhadas em n = 5, 15, 30 —
  **FALHA** se o limite SUPERIOR unilateral de 95% < 0.90 (sucessos ≤ 2/5, ≤ 10/15, ≤ 23/30); parada também quando
  as falhas passam de 1 (a aprovação final fica impossível) → "NÃO DEMONSTRADO". **Decisão de PASSA só no n final
  = 60:** passa com ≤ 1 falha (LB 0.923); com 2 falhas LB = 0.899 → não demonstrado.
- **Poucas realizações LONGE do limiar, muitas PERTO:** a grade é percorrida por bisseção; um nível que PASSA implica
  os menores (monotonicidade assumida, declarada) — verificada por amostras de 5 realizações nos níveis inferiores;
  qualquer falha ali = monotonicidade violada → reportada. Níveis claramente acima do limiar param em 5 (futilidade).
- **Especificação COM INTERVALO:** (i) valor conservador = o maior nível da grade que PASSA; (ii) curva de sucesso
  logística em log(nível) ajustada a TODAS as realizações → o nível em que a taxa ajustada = 0.90, com **IC 95% por
  bootstrap paramétrico (1 000)**. Os dois reportados.
- Custo: um nível decisivo custa até 60 ajustes (cada um com as partidas do D131 7.3) — a fase 0 pode ter de reduzir
  fontes/espaçamentos; se isso acontecer, é decisão registrada com motivo.

**8. AJUSTE 3 (2026-09-29) — CONVERGÊNCIA TAMBÉM NO TEMPO (princípio do D127).**
**Registro de integrador/dt de cada número já reportado:**
| onde | grandeza | integrador |
|---|---|---|
| D130 `target_profile` (Allen) | passivo (razões, Rin) | Impedance (sem integração) |
| D130 | EPSP 10 pA | passo fixo 0.025 ms |
| D130 | bAP | passo fixo 0.025 ms |
| D131 `hay_profile` | repouso | CVode (tolerâncias padrão), 3 s |
| D131 | **C1** (−50 pA no soma) e B (−50 pA no ponto) | **CVode, atol 10⁻⁵** |
| D131 | "congelado"/passivo | Impedance |
| D131 | EPSP 10 pA (d50 ~215 µm) | passo fixo 0.025 ms |
| D131 | **C3** (bAP 1.9 nA 5 ms) | **passo fixo 0.025 ms** (NÃO CVode) |
| D132 `hay_reduce` | repouso; P2/P3 | passo fixo **0.1 ms** (os dois modelos) |
| D132 | P4–P7 | passo fixo 0.025 ms |
**Verificação declarada:** C1 e C3 do Hay (Δ 1 µm, mesmo repouso salvo) a passo fixo **0.1, 0.05, 0.025 ms** (+ o CVode
original como comparação). Convergido se 0.05 → 0.025 ≤ 1% em cada grandeza de C1 e C3; se não, acrescenta-se 0.0125.
Referência = o dt mais fino convergido. **O veredito de C1/C3 é o do dt convergido; se virar, registra-se — sem
alargar banda.** Também: a comparação da redução (item 5) em P2/P3 a 0.1 ms vale para o MÉTODO (mesmo dt nos dois
modelos); os números absolutos de P2/P3 herdam a convergência medida aqui.
**Extensão (registrada 16:40, ANTES de rodar; motivo: parcial da sequência declarada já mostra o bAP longe de
convergir — 620 µm: 17.0 mV a 0.1 ms, 23.2 a 0.05, 27.9 a 0.025 (D131), 35.1 com CVode):** só o C3 (150 ms simulados
por rodada, barato), Δ 1 µm, mesmo repouso: Euler implícito 0.025 / 0.0125 / 0.00625 / 0.003125 ms; Crank–Nicolson
(secondorder 2) 0.1 / 0.05 / 0.025 / 0.0125 ms (diagnóstico do custo do modelo direto — o reduzido não roda com
CVode); CVode atol 10⁻⁵ / 10⁻⁶ / 10⁻⁷. Mesmo critério: convergido quando dois níveis sucessivos diferem ≤ 1%; o
veredito do C3 é o do nível convergido. `neuron/hay_dt2.py`.

**9. ORDEM DE INTERPRETAÇÃO DA VARIANTE — DECLARADA ANTES DO RESULTADO (2026-09-29 16:24; a busca F1 rodava e ainda
não tinha produzido nenhuma avaliação).** Se NENHUMA variante válida (F1, ou F2 com R_i dentro da faixa medida,
respeitando C1 e C3) alcançar 408 µm:
1º **Resolver a ressalva do EIXO do Beaulieu-Laroche 2018** (registros multi-sítio: o eixo das Figs. 3E/F e S4 pode
   ser a SEPARAÇÃO entre eletrodos, não a distância ao soma). Se for separação → o extremo de 408 µm é MAL POSTO
   (família da métrica no LOCAL ERRADO) → a sensibilidade usa o extremo REINTERPRETADO (convertido para distância ao
   soma, se o artigo der o necessário) ou registra o extremo como INDISPONÍVEL.
2º **Só então**, se o eixo for mesmo distância ao soma: concluir que as duas fontes são INCONSISTENTES dentro desta
   estrutura de modelo.
**Ressalva do eixo RESOLVIDA (16:26, antes de qualquer resultado da variante além da base k = 1: d50 = 211.6 µm a
Δ 2, que só reproduz o Hay original):** na figura do manuscrito do autor (Fig. 3E e 3F, lidas na imagem), o eixo é
**"Electrode separation (µm)"** — NÃO distância ao soma. Os registros de rato são "multi-site dendritic OR
somato-dendritic" (misturados; a separação só é distância ao soma nos pares soma–dendrito, que a figura não
distingue). O EPSP (Fig. S4, suplementar — não acessada) muito provavelmente usa o mesmo eixo (não verificado).
**Consequência, pela ordem acima: o extremo de 408 µm é MAL POSTO como "distância ao soma"** — família da métrica no
LOCAL ERRADO. Reinterpretar exigiria as distâncias ao soma de cada registro (não publicadas no texto) → **extremo
superior INDISPONÍVEL** até se obter o suplementar/dados. Isso vale QUALQUER que seja o resultado da variante (F1/F2):
uma variante que alcance 408 µm "de distância ao soma" persegue um número definido em outro eixo. A busca em curso é
mantida até o fim (custo baixo) e reportada como registro, não como extremo válido.

**10. RESULTADO — CONVERGÊNCIA TEMPORAL DE C1 E C3 (item 8; `hay_dt.py`, `hay_dt2.py`; Δ 1 µm, mesmo repouso).**
- **C1 CONVERGE TRIVIALMENTE:** idêntico em 0.1 / 0.05 / 0.025 / 0.0125 ms e CVode (r100 0.8500; d50 350.70 µm; r500
  0.3666; Rin 40.239 MΩ) — medida de estado estacionário. **C1 CAI.**
- **C3 (bAP) NÃO converge com Euler implícito nos dt usados:**
  | integrador | 620 µm | 800 µm | PA no soma |
  |---|---|---|---|
  | Euler 0.1 / 0.05 / 0.025 / 0.0125 / 0.00625 / 0.003125 ms | 17.0 / 23.2 / 27.9 / 31.0 / 32.9 / 34.0 | 11.7 / 15.6 / 18.7 / 21.2 / 23.0 / 24.1 | 1 |
  | Crank–Nicolson 0.1 / 0.05 / 0.025 / 0.0125 ms | 25.8 / 32.4 / 34.4 / 34.9 | 17.3 / 22.5 / 24.6 / 25.2 | **5** / 1 / **2** / 1 |
  | CVode atol 10⁻⁵ / 10⁻⁶ / 10⁻⁷ | 35.10 / 35.09 / 35.09 | 25.37 / 25.36 / 25.36 | 1 |
  Pelo critério declarado (dois níveis sucessivos ≤ 1%): Euler NÃO convergiu nem a 0.003125 ms (3–5% entre níveis);
  Crank–Nicolson 0.025→0.0125 = 1.5% / 2.4% (não) e produz PA ESPÚRIOS em dt grosso; **CVode converge (≤ 0.05%) →
  referência = CVode atol 10⁻⁶: bAP 35.09 mV a 620 µm e 25.36 mV a 800 µm** (o Hay ajustou com CVode — BAC_firing.hoc).
- **VEREDITO DO C3 NO dt CONVERGIDO: NÃO CAI** — só pelo sub-critério "decremental": o bAP SOBE de 200 para 300 µm
  (50.05 → 51.25 mV, +1.2 mV, +2.4%). As amplitudes SAEM da borda (−1.0 e −1.1 DP da média, antes −1.7/−1.8) e o soma
  dá 1 PA. **O veredito VIROU** (a 0.025 ms passava porque o erro numérico suavizava o perfil). Registrado, banda não
  alargada. **Diagnóstico (não usado para aprovar):** o sub-critério foi declarado como monotonicidade ESTRITA (tolerância
  zero) sobre grandeza contínua — corte fixo, a família do D130 item 4; a fonte (Stuart et al. 1997) dá o bAP
  "decremental" como tendência, sem números acessados. Se o sub-critério está mal posto é decisão do usuário.
- **Consequência para os números já reportados:** o C3 do D131 (27.9/18.7 mV, Euler 0.025) NÃO estava convergido; a
  "borda" era erro numérico. Todos os P4–P7 do `hay_reduce` (Euler 0.025) valem para comparar o MÉTODO (mesmo dt nos
  dois modelos), NÃO como valores absolutos do Hay. **O modelo direto do teste precisa de CVode** (ou Crank–Nicolson
  ≤ 0.0125 ms, verificado contra CVode); o reduzido com LinearMechanism não roda com CVode (item 5).
- **Alerta para trás (registrado, não verificado):** o degrau ativo do Allen (D128/D129) e o bAP do D130 também usaram
  Euler 0.025 ms. A comparação reduzido × L0 do D129 era no MESMO dt (vale para o método); os valores absolutos
  (contagens perto do limiar, bAP) podem não estar convergidos no tempo — verificar quando o alvo voltar a ser o Allen.

**11. RESULTADO — VARIANTE (item 6).** F1 (c_m dendrítico × k, EPSP a Euler 0.025, Δ 2): d50 = 211.6 µm (k = 1) →
367.8 µm (k = 0.1) → **408 µm NÃO alcançável** (previsão de ~358 µm pelo limite estacionário confirmada na ordem de
grandeza). F2 (R_i × k): a primeira rodada tratou "não cruza 0.5 até 700 µm" como inalcançável (erro meu de código);
refeita com a bisseção corrigida e EPSP/bAP em CVode — **só como REGISTRO**, porque pelo item 9 o extremo de 408 µm é
MAL POSTO (eixo = separação entre eletrodos) → **extremo superior INDISPONÍVEL; a sensibilidade do C2 fica sem o
segundo extremo** até obter os dados por registro (distância ao soma) do Beaulieu-Laroche 2018 / Fig. S4.
Convergência temporal do EPSP (o lado de 215 µm): d50 com CVode 10⁻⁶ = 211.8 µm vs Euler 0.025 = 211.6 µm (Δ 2) —
o EPSP subliminar CONVERGE; o extremo inferior (Hay original) está de pé.
**F2 (só REGISTRO — o extremo é indisponível pelo eixo):** bisseção corrigida, EPSP/bAP em CVode: **R_i × 0.316
(≈ 32 Ω·cm, FORA da faixa medida 70–100 Ω·cm)** dá d50 = 412 µm (Δ 1). Nessa variante: **C1 NÃO CAI** (razão
estacionária 0.92 a 100 µm, 0.59 a 500 µm > 0.52; o 50% não ocorre até 600 µm) e **C3 NÃO CAI** (bAP 68.0 / 72.6 mV,
2 PA no soma, não decremental). Mesmo que o eixo fosse distância ao soma, nenhuma variante de um parâmetro (F1, F2)
alcança 408 µm respeitando C1/C3 e a faixa medida — dentro desta estrutura as fontes não se conciliam por esse
caminho. Como o eixo É separação (item 9), isso fica como registro, não como conclusão de inconsistência.

**12. CUSTO TOTAL (estimado ANTES de lançar a varredura; tempos MEDIDOS nesta máquina: 8 núcleos, 7.8 GB, 3
processos simultâneos por memória).**
Custo por passo: Hay completo Δ 1 µm (12 757 seg.) ~5 ms (ocioso); **reduzido do D126 no NEURON: N = 4 (781 comp.)
~2 ms, N = 16 (3 121) ~22 ms** — o LinearMechanism força o solver esparso geral, e o reduzido fica MAIS LENTO que o
completo (achado de custo). Pontos por espaçamento (árvore toda, grade ancorada no soma): s = 400/200/100/50/25 µm →
20/51/119/249/503. Avaliação direta (M1 2×1.15 s a dt 0.1 + M4 3×0.3 s + M3 + M5 3×2.3 s, no dt ativo):
| dt ativo | s = 100: horas por avaliação | ajuste (31 avaliações/iteração × 30 iterações × 20 partidas) |
|---|---|---|
| Euler 0.00625 ms | 29 h | 62 anos-CPU |
| 0.025 ms (Crank–Nicolson, se validado) | 10 h | 21 anos-CPU |
- **EXAUSTIVO** (7 fontes × ~125 realizações por fonte pela regra do item 7 × 2 espaçamentos + combinada ≈ 1 810
  ajustes): **~3×10⁷ avaliações diretas ≈ 2×10¹⁰ simulações ≈ 6×10⁴–2×10⁵ anos-CPU. INVIÁVEL por > 10⁴×.**
- **ETAPA A** (item 13): ~125 avaliações a s = 25 µm + 61 do conjunto funcional ≈ **0.6–1.7 anos-CPU (73–209 dias
  em 3 núcleos)** — no limite do viável.
- **ETAPA B** como declarada (960 ajustes completos a s = 100): **~2×10⁴–6×10⁴ anos-CPU — INVIÁVEL** nesta forma.
**ESCOLHA: caminho em DUAS ETAPAS** (o exaustivo é inviável). Mas **nada é lançado**: a Etapa A precisa de redução de
custo e a Etapa B, como declarada, é inviável — as alavancas (com fator estimado, a decidir pelo usuário):
| alavanca | fator | custo em fidelidade |
|---|---|---|
| modelo direto = NEURON nativo com nseg = N (solver de árvore; tem nós de junção explícitos) em vez do LinearMechanism | ~10–15× (N = 16) | HIPÓTESE: equivalente ao D126 — verificar (P1–P5, N = 4, ≤ 10⁻³) antes |
| CVode nas partes ativas do modelo nativo | ~8× vs Euler 0.003 no C3 | nenhum (é a referência convergida) |
| M4 com 1 amplitude e 100 ms | ~5× na avaliação | menos informação sobre excitabilidade dendrítica |
| Etapa B com Jacobiano reaproveitado da A (Gauss–Newton/Broyden) e 5 partidas | ~100× por ajuste | detecta menos mínimos múltiplos (justamente o que a B deve pegar) |
| B só para σ_V em s\* (2 níveis × 60) | ~7× | as outras fontes ficam só com a previsão da A |
| hardware (mais núcleos/memória; CoreNEURON/GPU; ou o simulador L2 próprio) | 10–100× | nenhum |

**13. ETAPAS DECLARADAS (antes de rodar; lançamento depende da decisão do item 12).**
**ETAPA A — PREVISÃO ANALÍTICA (Fisher / Cramér–Rao).**
- Modelo direto: árvore por ramo (N do nível B do item 5; se nenhum, o do nível A com a ressalva) parametrizada POR
  REGIÃO (os 30 do D131 7.1, formas do Hay); θ_verdadeiro = valores do biophys3 (a árvore em θ_verdadeiro reproduz o
  Hay a menos do erro de redução medido no item 5). Estacionário a dt 0.1; ativo com CVode atol 10⁻⁶ (ou
  Crank–Nicolson ≤ 0.0125 ms validado contra CVode).
- J = ∂y/∂log θ por diferença central (passo 1%), y = traços M1–M5 sem linha de base, amostra 0.1 ms, na grade de
  25 µm; espaçamentos maiores = SUBCONJUNTOS de linhas (grade ancorada no soma); D51-oráculo e adaptativo: pontos
  arredondados para a grade de 25 µm (≤ 12.5 µm — aproximação declarada).
- F (conjunto funcional, só partes CONTÍNUAS): pico do EPSP somático nos 30 locais sorteados + pontos do D127;
  tempo do 1º PA e pico do Ca-spike no BAC e no CaBurst; taxa f-I (1/ISI médio) nos degraus com ≥ 2 PA. G = ∂F/∂log θ.
  **Identidade de CONTAGEM não é linearizável → só a Etapa B a verifica.**
- Identificabilidade funcional: SVD de J ponderado; se G tem componente nas direções com valor singular < 10⁻⁶·σ_max
  (‖G·V₀‖ > 10⁻³‖G‖) → funcional NÃO identificável naquele espaçamento em qualquer ruído.
- Ruído → Cov_F: σ_V: σ_V²·G(JᵀJ)⁺Gᵀ; offset (respostas sem linha de base): só nas leituras de repouso, var a²/3;
  ganho (por ponto, não ajustado): D = ∂y/∂g_p (+1% nas injeções de cada ponto, ≈ 1 avaliação), Cov = σ_g²·G J⁺ D Dᵀ
  J⁺ᵀ Gᵀ; posição: idem com ∂y/∂x_p (+2 µm, ≈ 1 avaliação); diâmetro e comprimento por seção: Monte Carlo com 30
  perturbações unitárias cada (1 avaliação cada); escala global: ±1% (2). **Combinado = SOMA das covariâncias.**
- [**Item 26: acrescentado o VIÉS linearizado de especificação — critério passa a |δF_viés,i| + 1.645·σ_F,i ≤
  tolerância_i.**] Critério: nível tolerado se, para CADA grandeza funcional i, 1.645·√(Cov_F,ii) ≤ tolerância_i (EPSP 5%, 1º PA 1 ms,
  taxa 2% — D131 7.4; 1.645 = 90% bilateral, coerente com p_req = 0.90 POR grandeza; a probabilidade CONJUNTA não é
  garantida — limitação declarada). Previsão x̂ = maior nível tolerado (analítico: Cov ∝ x²). Saída: x̂ por fonte ×
  espaçamento, s\* (maior espaçamento com F identificável), e o combinado.
- **RESSALVA:** Cramér–Rao é LOCAL (linearização em θ_verdadeiro): não vê mínimos múltiplos nem parâmetros que só se
  separam longe da verdade, nem mudanças de CONTAGEM de PA → **a Etapa B é OBRIGATÓRIA**, mas pontual.
**ETAPA B — VALIDAÇÃO PONTUAL** [**SUBSTITUÍDA pelo item 16: sanidade, não certificação**]. Níveis: **0.7·x̂ e 1.4·x̂** (um pouco abaixo e acima, em escala log) por fonte, em
s\*; σ_V também em s\*/2. Ajuste completo do D131 7.3 (20 partidas); dado do Hay COMPLETO; regra do item 7 (n final
60, ≤ 1 falha; futilidade em 5/15/30). **CONFIRMADA** se 0.7·x̂ PASSA e 1.4·x̂ NÃO passa. Se 0.7·x̂ falha: a A foi
otimista (não linearidade) — a discrepância é o achado e a especificação passa a ser a da B. Se 1.4·x̂ passa: a A foi
pessimista — reportado. **Lançamento: só com a decisão do item 12** (como está, inviável).

**14. DECISÃO DO USUÁRIO SOBRE O C3 — tomada DEPOIS de ver o resultado (item 10), com argumento independente dele.**
O sub-critério "decremental ESTRITO" está MAL POSTO: um critério não pode exigir precisão maior que a dos dados que o
definem. O dado de bAP é ESPARSO (620 e 800 µm) com DP de ~10 mV (Tabela 1 do Hay); uma subida local de 1.2 mV entre
200 e 300 µm é INVISÍVEL para ele. **O C3 é avaliado NOS SÍTIOS DO DADO:** entre 620 e 800 µm o Hay decresce (35.09 →
25.36 mV, CVode) e as amplitudes ficam a −1.0 e −1.1 DP → **C3 CAI.** **Quarta aparição da família "tolerância zero
sobre grandeza contínua"** (fronteira de região no passivo — D127; borda da janela de 1 s — D128; alinhamento com
corte fixo — D126; e esta). **Também registrado:** o "C3 na borda" do D131 era ERRO NUMÉRICO do integrador (Euler
0.025 ms). **Estado da verdade de base: Hay sob C1 (cai) + C3 (cai, nos sítios do dado, CVode); C2 não verificável.**

**15. ALAVANCAS DE CUSTO — DECISÃO DO USUÁRIO.**
- **CVode nas partes ativas: OBRIGATÓRIO** (não alavanca) — única referência convergida (item 10).
- **NEURON nativo com nseg = N: ADOTADO SÓ depois da verificação de equivalência com o D126**, declarada agora, antes
  de rodar: Hay em N = 4 compartimentos por ramo, MESMAS amostras de densidade (Hay a Δ 0.5 µm no centro de cada
  compartimento, todos os parâmetros + c_m/g_pas/e_pas/e_K/e_Na) nos dois; protocolos P1–P5 e P7 do item 5 e P6 a
  0.6/1.2/2.0 nA, MESMO integrador nos dois (passo fixo 0.1 / 0.025 ms — o reduzido não roda com CVode).
  **EQUIVALENTE se P1–P5 |erro relativo| ≤ 10⁻³ e P6/P7 com contagens iguais e tempos de PA ≤ 0.05 ms** (os mesmos
  limiares do V1). Se não for equivalente: NÃO usar. `neuron/hay_native.py` (NATIVE × RED).
- **REJEITADAS:** Jacobiano reaproveitado + 5 partidas na Etapa B (a B existe para pegar o que a LINEARIZAÇÃO não vê —
  o atalho a transformaria de volta em linearização); M4 com 1 amplitude (muda o PROTOCOLO testado; "o protocolo
  reduzido basta?" é PERGUNTA SEPARADA, não alavanca).
- Custo da Etapa A com as duas alavancas adotadas: medido (modo TIMING, nativo, CVode) e reportado ANTES de lançar.

**16. ETAPA B = VERIFICAÇÃO DE SANIDADE, NÃO CERTIFICAÇÃO (substitui a B do item 13).** Um nível (**0.7·x̂**), só
**ruído de voltagem**, só em **s\***, ajuste completo com as **20 partidas** do D131 7.3, **n = 10 realizações**;
**FALHA GROSSEIRA da previsão se ≥ 3 das 10 falharem.** Justificativa (binomial): se a previsão vale (taxa ≥ 0.90), o
falso alarme é 7.0%; se a taxa real é ≤ 0.50 (falha grosseira), a detecção é ≥ 94.5%; a 0.70, 61.7% (não é o alvo —
certificar exigiria a regra do item 7). Comparados: n = 8 com ≥ 2 falhas (falso alarme 18.7%); n = 15 com ≥ 4 (5.6% /
98.2%, 1.5× o custo). ~~**Rótulo obrigatório da especificação: "PREVISTA pela Etapa A, CHECADA pela Etapa B, NÃO
CERTIFICADA".**~~ [**Substituído pelo item 22 — a B foi adiada (item 21): "CONDIÇÃO NECESSÁRIA".**] A certificação completa (item 7) fica para o L2 ou hardware dedicado.

**17. CONSEQUÊNCIA PARA O C++ (registrada também no D116, no P54 e no P24).**
**Ordem do integrador do HHNeuronModel — CONFIRMADA empiricamente** (driver fora da produção,
`neuron/hh_order.cpp`, modelo padrão SEM modificação; protocolo declarado no cabeçalho antes de rodar: repouso de
1 s a dt 0.0003125 ms copiado para cada dt; pulso de 5 ms no soma a 1.5× o limiar de 1 PA; referência dt 0.0003125):
- Leitura do código: divisão de Lie — portões com Euler EXPONENCIAL a V congelado; V com passo exponencial da equação
  linearizada a portões congelados; acoplamento axial EXPLÍCITO com varredura sequencial dos compartimentos → 1ª ordem.
- Medido: ordem observada no pico do compartimento distal **0.91 / 0.97 / 1.05 / 1.15** (dt 0.0125 → 0.0016 ms) —
  **1ª ORDEM**; em dt grosso, ordens aparentes 2–3 no soma são pré-assintóticas; perto da referência, o tempo do PA e o
  erro máximo ficam no ruído (~0.5 mV).
- **A dt = 0.1 ms (produção): 1º PA +1.06 ms atrasado, pico somático −2.7 mV**, erro máximo de trajetória no soma 91 mV
  (deslocamento do PA). No modelo de 4 compartimentos o "bAP" distal é só +2.3 mV (−51.5 → −49.2) — não há bAP ativo a
  reproduzir; o problema aparece quando houver dinâmica dendrítica ativa (L2).
- **Consequência:** com 1ª ordem, o C++ a 0.1 ms quase certamente NÃO reproduz o bAP (no NEURON, Euler 1ª ordem não
  converge o bAP nem a 0.003 ms). O L2 precisa de estudo de convergência em dt para dinâmica dendrítica e,
  provavelmente, de integrador de ordem maior ou adaptativo.
- **P24 (orçamento térmico):** calculado a dt = 0.1 ms. Mantido o método de 1ª ordem, o dt necessário para o bAP
  (≤ 0.003–0.006 ms, e ainda não convergido) multiplica os passos por **16–32× (1–1.5 ordens de grandeza)** — o
  orçamento pode estar SUBESTIMADO nessa proporção. Um método de ordem maior/adaptativo muda a conta (custo por passo
  maior, passos muito menos numerosos) — decidir com o estudo do L2.
- **ACHADO DE ESTRUTURA PARA O L2 (recomendação de desenho, hipótese a verificar quando o L2 for desenhado):** a árvore
  reduzida com LinearMechanism é MAIS LENTA que o Hay completo (item 12). Hipótese: a redução de Kron elimina os nós de
  junção acoplando IRMÃOS diretamente — a matriz deixa de ser uma árvore (cliques nas junções), e o NEURON cai no solver
  esparso geral; árvores se resolvem em tempo LINEAR (Hines). **Manter os nós de junção EXPLÍCITOS preserva a estrutura
  de árvore → recomendação: L2 com junções explícitas, não Kron** (o Kron do D126 foi instrumento de validação, não de
  implementação). A equivalência do item 15 testa exatamente essa troca no NEURON.

**18. ALERTA PARA TRÁS — D130 (registrado; refazer quando houver capacidade).** Os números ABSOLUTOS de bAP do D130
(Allen, all active e perisomático: "74 / 1.7 / 0.1 / 0 mV" e "121 / 16 / 5.2 / 1.4 mV") usaram Euler 0.025 ms →
**NÃO podem ser citados até refeitos com CVode.** A conclusão do D130 provavelmente sobrevive — apoia-se sobretudo na
atenuação ESTACIONÁRIA, passiva e idêntica em qualquer integrador. As comparações RELATIVAS do método (D128/D129, P4–P7
em curso) continuam válidas: os dois modelos usam o mesmo integrador e dt.

**19. RESULTADO — EQUIVALÊNCIA NEURON NATIVO × D126 (item 15).** 1ª rodada, pelo critério declarado: **NÃO
EQUIVALENTE** — P1, P2, P5, P6, P7 e o EPSP no SOMA idênticos a ~10⁻¹³ (contagens e tempos de PA idênticos), mas P3
(Rin local, ponto→soma) e P4 LOCAL divergem até 31% nos pontos cuja leitura envolve nó de JUNÇÃO/PONTA.
**Diagnóstico:** defeito da LEITURA do reduzido, não da dinâmica. O Kron dá V_J = P·V_C + G_JJ⁻¹·I_J; o `point_C`
(tree2_lib) só tem P·V_C — correto sem injeção no nó J, errado ao ler a tensão do PRÓPRIO ponto de injeção (falta a
queda I·R do meio-segmento até a ponta/junção). Evidência independente: Rin na ponta basal — Hay a Δ 1 µm 1 433 MΩ;
nativo N = 4 1 440; reduzido 1 102. **Correção (bug de leitura, critério inalterado):** somar I_J/G_JJ (G_JJ é
diagonal: nós J só tocam compartimentos). 2ª rodada: **P1–P5 pior 9.1×10⁻⁴ (P4 local na ponta basal — resíduo da
reconstrução temporal da corrente), P3 2×10⁻¹¹, PAs idênticos → EQUIVALENTE.** → **NEURON nativo com nseg = N
ADOTADO** como modelo direto (solver de árvore + CVode). E isto CONFIRMA, no NEURON, a hipótese do item 17: o mesmo
modelo, com junções explícitas (árvore), roda ~2× mais rápido já em N = 4 (335 vs 597 s) e ~15× em N = 16.
**Impacto e providência:**
- Allen (D127–D129) NÃO afetado: as métricas de ponto usaram `dc_red` (sistema completo com junções, exato) e o EPSP
  foi lido no SOMA.
- Fila da verificação (item 5): os jobs RED ainda não tinham começado → `hay_reduce.py` corrigido ANTES deles
  (fumaça ok). O **LIMIT (V1) já rodava com a leitura antiga** → declarado agora, antes do resultado: no V1, o P3 é
  corrigido offline pela fórmula exata (estado estacionário: V_ponto += c·I, c = Σ w_J² / G_JJ) e o P4-local do LIMIT
  é REFEITO depois da fila com a leitura exata; os demais P do V1 não dependem da leitura.

**20. CUSTO DA ETAPA A COM AS DUAS ALAVANCAS ADOTADAS (medido; nativo N = 16, 3 121 seg., CVode 10⁻⁶; máquina com
7 processos simultâneos → tempos pessimistas).** Por protocolo: M1 um degrau de 1.15 s 5.4 s (35.6 s a dt 0.1 fixo);
M4 300 ms 3.5 / 3.8 / 14.7 s (0.2 / 0.5 / 1.5 nA); M3 13.7 s; M5 (2.3 s, 1 nA) 264 s. Por ponto de penetração ≈ 33 s;
por avaliação ≈ 33 s × pontos + ~860 s (M5 × 3 + M3):
| s | pontos | avaliação direta |
|---|---|---|
| 25 | 503 | 4.8 h |
| 100 | 119 | 1.3 h |
| 400 | 20 | 0.42 h |
**Etapa A** (J 61 + ganho/posição ~3 + Monte Carlo de geometria 62 ≈ 125 avaliações a s = 25, e 61 avaliações do
conjunto funcional a ~0.5 h): **≈ 630 h-CPU ≈ 26 dias-CPU ≈ 9 dias em 3 núcleos** (com N = 16; se o V2 pedir N = 32,
~2×). Antes das alavancas: 73–209 dias em 3 núcleos. **Viável.** Lançamento só depois do V2 (define N) e com o
modelo nativo.
**Etapa B como sanidade (item 16), com o mesmo modelo:** 1 ajuste = 20 partidas × ~30 iterações × 31 avaliações
(Jacobiano por diferença) = 18 600 avaliações → a s = 400, **1 ajuste ≈ 7 800 h-CPU (~0.9 ano-CPU)**; 10
realizações ≈ 9 anos-CPU (s\* = 100: ~28 anos-CPU). **Nem a sanidade cabe nesta máquina**: o gargalo é o ajuste
completo (Jacobiano por diferença finita × 20 partidas), não o número de realizações. Registrado para decisão; as
alavancas que baratearia (Jacobiano reaproveitado, menos partidas) foram rejeitadas com razão (item 15). Sem gradiente
adjunto/automático ou hardware dedicado, a B fica para o L2.

**21. DECISÃO DO USUÁRIO — ETAPA B ADIADA.** Mesmo como sanidade não cabe (~0.9 ano-CPU por ajuste; ~9 anos-CPU as
10 realizações). As duas saídas baratas continuam REJEITADAS (item 15). **Status da B: PENDENTE DE GRADIENTE BARATO**
(item 23). A Etapa A segue: lançamento depois que o V2 definir o N.

**22. RÓTULO DA ESPECIFICAÇÃO DA ETAPA A (substitui o do item 16).** Cramér–Rao é LIMITE INFERIOR da incerteza dos
parâmetros — um estimador real, com não linearidade e mínimos múltiplos, pode fazer PIOR. O ruído tolerado previsto
pela A é um **TETO**: acima dele a identificabilidade CERTAMENTE falha; abaixo, PODE ainda falhar. **Rótulo:
"CONDIÇÃO NECESSÁRIA — o sensor precisa ser PELO MENOS tão preciso quanto isto."** A SUFICIÊNCIA fica NÃO TESTADA até
a B existir. (O rótulo anterior "prevista pela A, checada pela B" é retirado: a B não roda.)

**23. O CUSTO DA B É A PRÉVIA DO CUSTO DO APRENDIZADO IN VIVO (registrado também no P53 e no P54).** Ajustar um
modelo às medidas de uma célula é o que o HANU precisa fazer IN VIVO, por neurônio — a PERGUNTA 2 DO P53. A pergunta
"o ajuste por modelo direto escala?" (aberta desde o P54, 2026-09-17: mecanismo × ferramenta de laboratório) **agora
tem número: ~18 600 avaliações por ajuste com Jacobiano por diferenças finitas (30 parâmetros, 20 partidas), ~0.9
ano-CPU num computador de mesa, para UMA célula — com diferenças finitas, NÃO ESCALA.** Saída comum aos dois
problemas: **GRADIENTE BARATO** — derivação adjunta ou automática custa algumas simulações por gradiente,
independentemente do número de parâmetros.
**Mapeamento do estado da arte (NÃO adotado — só mapeado; conferido em código-fonte/PyPI em 2026-09-29):**
| simulador | o que é | integradores | canais / morfologia | gradiente | hardware | licença / versão |
|---|---|---|---|---|---|---|
| **Jaxley** (Deistler et al., Nature Methods 2025; jaxleyverse/jaxley) | simulador diferenciável de neurônios multicompartimentais em JAX | `bwd_euler` (padrão), `crank_nicolson`, `fwd_euler`, `exp_euler` (portões exp. Euler); **passo FIXO — sem adaptativo/CVode**; sistema do cabo por solver de árvore (`jaxley.dhs`, "similar ao NEURON, com nós terminais nas bifurcações") ou `jax.sparse` | HH e canais definidos em Python (biblioteca comunitária; Ca, K-Ca citados); Markov não enumerado; **sem importação de .mod** encontrada; I/O de SWC | autodiff reverso com checkpointing multinível; **gradiente 3–20× o custo da simulação** | CPU/GPU/TPU | **Apache-2.0**, v0.14.0 (2026-09-03) |
| **BrainCell** (chaobrain/braincell, ecossistema BrainX/BrainPy) | células biofísicas mono e multicompartimentais em JAX/brainstate | Euler explícito, RK2/3/4, implícito, Euler exponencial, "staggered cable solve"; adaptativo não declarado | biblioteca de canais Na/K/Ca/HCN/K-Ca; Ca intracelular; SWC/ASC/NeuroML2 | autodiff (JAX) | CPU/GPU | **Apache-2.0**, v0.1.0 (2026-06-18) — jovem |
| **BrainPy** (Wang et al., ICLR 2024 / eLife 2023) | simulador diferenciável de dinâmica cerebral (redes; foco em ponto/multiescala) | vários | — | autodiff | CPU/GPU | aberto |
Evidência de uso na PERGUNTA DESTE TESTE: Jaxley ajustou um L5 com 19–25 parâmetros (Allen) e 1 390 condutâncias
por ramo (sintético) por gradiente; "diferenças finitas levariam > 2 anos" no exemplo de rede; Tanoh, Deistler, Macke &
Linderman 2025 (arXiv 2506.20233) identificam parâmetros de HH multicompartimental a partir de registros extracelulares
de alta densidade (filtro de Kalman estendido + gradiente) — é a pergunta de identificabilidade com outra medida.
**Ressalva que vem DESTE trabalho:** o integrador padrão do Jaxley é de 1ª ordem (Euler implícito + portões exponenciais)
e sem passo adaptativo — no Hay, Euler implícito não converge o bAP nem a 0.003 ms e Crank–Nicolson dá PA espúrios em dt
grosso (item 10). Adotar qualquer um exige, antes, o MESMO estudo de convergência em dt contra CVode.
**CONEXÃO COM O L2 — REQUISITOS CANDIDATOS** (o L2 será reescrito de qualquer jeito — integrador de 1ª ordem, item 17):
(i) **DIFERENCIÁVEL desde o início** (gradiente adjunto/automático) — torna viáveis, com uma decisão de arquitetura, a
Etapa B, a pergunta 2 do P53 e o aprendizado in vivo; (ii) **junções EXPLÍCITAS** (árvore, solver linear — item 19);
(iii) **integrador de ordem maior ou ADAPTATIVO**, com estudo de convergência em dt para dinâmica dendrítica ativa.

**24. O INTEGRADOR DE 1ª ORDEM ATINGE A VERIFICAÇÃO (registrado também no P28 e no P54).** A dt = 0.1 ms o 1º PA sai
**+1.06 ms** e o pico somático −2.7 mV (item 17). Não é só fidelidade de bAP ou orçamento térmico:
- O ATRASO SINÁPTICO padrão é 1.5 ms, e a DISCRIMINAÇÃO do teste ativo (D111) depende de latência — um erro de
  temporização de ~1 ms é da MESMA ORDEM do sinal que ela mede.
- O DESMAME compara histogramas de ISI produzidos por esse integrador, e NUNCA foi exercitado com disparos do HH real
  (o harness injetava os spikes — P53/P28).
**A VERIFICAR (quando houver capacidade):** o erro de temporização é um DESLOCAMENTO CONSTANTE (cancela nos ISIs) ou
DISTORCE os intervalos (não cancela)? Decide se o desmame está comprometido ou só a latência absoluta. Protocolo a
declarar antes: trem sob degrau/ruído no HHNeuronModel a dt 0.1 vs referência fina (o driver `neuron/hh_order.cpp`
serve de base) → erro por PA (deslocamento) e erro por ISI (distorção).

**25. ACHADO DA EQUIVALÊNCIA (registro pedido; detalhes no item 19).** A leitura dos nós de junção e de ponta do
reduzido perdia o termo I_J/G_JJ; referência independente confirmou o nativo (Rin na ponta basal: completo 1 433,
nativo 1 440, reduzido 1 102 MΩ); nativo adotado; ~15× mais rápido em N = 16 — confirma no NEURON a recomendação de
junções explícitas para o L2.

**26. LEITURA DE TANOH, DEISTLER, MACKE & LINDERMAN 2025 (arXiv 2506.20233, v2 dez/2025; texto integral lido) —
ANTES da Etapa A.**
- **Método:** filtro de Kalman estendido (EKF; aproximações diagonal e bloco-diagonal da covariância) infere tensão e
  estados de canal; os parâmetros saem por MÁXIMA VEROSSIMILHANÇA MARGINAL com gradiente (Adam) através do Jaxley
  (v0.7.0; Euler implícito, Δt = 0.025 ms). Medida: registros EXTRACELULARES de alta densidade (Neuropixel/MEA).
- **Conclusões de identificabilidade:** (i) ramo único e 3 ramos (9 condutâncias + 18 coordenadas): condutâncias,
  posições e tensão recuperadas — com modelo CORRETO e dinâmica determinística; (ii) posições: sítios num plano dão
  ambiguidade por REFLEXÃO → precisaram de duas posições de sonda; (iii) CA1 (C10 de Cutsuridis; 24 condutâncias + 6
  de corpo rígido; 60 compartimentos; > 100 partidas, fica a de maior verossimilhança): **recupera a TENSÃO e a posição,
  e "a maioria das condutâncias, não todas" — DEGENERESCÊNCIA de parâmetros**; (iv) com modelo ERRADO (canais omitidos,
  cinética perturbada), o EKF com ruído de processo reconstrói a tensão; **a minimização de erro quadrático (MSE) FALHA**.
- **O que já responde parte da nossa pergunta:** confirma o esperado no D131 7.4 — parâmetros degenerados COM função
  recuperada; o critério de SUFICIÊNCIA FUNCIONAL (e não parâmetro a parâmetro) é o certo. Não responde espaçamento nem
  ruído do sensor para medida INTRACELULAR em pontos de penetração.
- **Armadilhas de método que mudam o nosso desenho:**
  (a) **ESPECIFICAÇÃO ERRADA:** a nossa pergunta realista (item 4) É especificação errada — verdade com densidades por
  seção, ajuste com parâmetros por região. Cramér–Rao supõe modelo CERTO e só dá variância; o VIÉS de especificação
  fica fora dele, e Tanoh mostra que MSE sob especificação errada pode falhar. **MUDANÇA NA ETAPA A (declarada antes
  de lançar):** acrescenta-se o **viés linearizado de especificação**: δθ_viés = J⁺·(y_Hay − y_red(θ_verd)) e δF_viés =
  G·δθ_viés + (F_Hay − F_red(θ_verd)); critério por grandeza funcional passa a ser **|δF_viés,i| + 1.645·σ_F,i ≤
  tolerância_i**. Custo: + 1 simulação do Hay completo convergido (CVode) com todos os protocolos na grade de 25 µm
  (~1 dia-CPU). Se o viés sozinho já estourar a tolerância em algum espaçamento, a especificação do sensor não existe
  naquele espaçamento (nenhum ruído basta) — é resultado.
  (b) **MÍNIMOS MÚLTIPLOS:** no caso de 3 ramos, as 40 repetições partiram da MELHOR solução achada num conjunto de
  dados — não testam multimodalidade de forma independente. Nossa B (quando existir) já exige partidas independentes
  por realização; **nota para a B: Tanoh usou > 100 partidas no CA1; as nossas 20 ficam registradas como mínimo, a
  revisar quando a B for viável.**
  (c) **DISCRETIZAÇÃO:** Euler implícito a 0.025 ms e 60 compartimentos no CA1, sem estudo de convergência — a
  identificabilidade deles é do MODELO NUMÉRICO (dados e ajuste pelo mesmo modelo); informativa para a estrutura, não
  para a fidelidade.
- **Não linearidade (o papel da nossa B):** tratada por (i) muitas partidas + maior verossimilhança marginal, (ii) ruído
  de processo no EKF (robustez a especificação errada). Nenhuma certificação estatística de taxa de sucesso.
- **Diferença registrada:** eles medem EXTRACELULARMENTE (indireto, muitos compartimentos por eletrodo); o HANU mede
  INTRACELULARMENTE em pontos de penetração (direto, local) + geometria pelo scan (sem ambiguidade de posição). O
  resultado NÃO substitui o nosso; a metodologia (EKF + verossimilhança marginal + gradiente) se aplica — candidata para
  a B e para o aprendizado in vivo quando houver gradiente barato.

**27. CANDIDATO PARA O L2 — ADJUNTO CONTÍNUO COM INTEGRADOR ADAPTATIVO (CVODES/SUNDIALS). Registrado, NÃO adotado.**
**A tensão:** os simuladores diferenciáveis (item 23) diferenciam ATRAVÉS de integradores de passo fixo — exatamente os
que falharam no Hay (item 10). DIFERENCIÁVEL × CONVERGIDO. **Saída possível:** o método ADJUNTO CONTÍNUO não exige
passo fixo — funciona sobre integrador ADAPTATIVO. **Verificado (documentação oficial):**
- **Disponibilidade/licença:** CVODES é parte do SUNDIALS (C, com interface C++), **BSD-3-Clause** — mesma família do
  CVODE que o NEURON usa (o NEURON NÃO expõe adjunto).
- **O que faz:** sensibilidade DIRETA (custa ∝ nº de parâmetros) e **ADJUNTA** sobre BDF/Adams de ordem e passo
  variáveis, com checkpoints e interpolação do trajeto direto; o gradiente de funcionais sai de UMA integração
  reversa, **independente do número de parâmetros** (~1 integração direta + 1 reversa + recomputação entre
  checkpoints). Estimativa para o nosso ajuste: por iteração, ~3–5 simulações em vez de 31 → um ajuste da B cai de
  ~18 600 para ~3 000 avaliações (~6×) — **ainda caro nesta máquina (~0.15 ano-CPU por ajuste a s = 400)**; o ganho
  cresce com o nº de parâmetros (in vivo, per-ramo: centenas a milhares).
- **Exigência: suavidade.** A documentação exige ∂g/∂y e ∂g/∂p existentes e limitados; eventos/raízes no modo adjunto
  não têm tratamento automático (descontinuidades exigem parar/reiniciar com condição de salto feita à mão).
**NÃO SUAVIDADES do modelo (onde estão; efeito no gradiente):**
| onde | o quê | efeito |
|---|---|---|
| C++ `CalciumDynamics::remove` | **piso duro [Ca] = baseline** (e `excess ≤ 0 → ca = baseline`) — ATIVO EM REPOUSO | gradiente nulo/descontínuo p/ tudo que passa pelo Ca perto do repouso — **precisa reformular (bomba suave) antes de diferenciar** |
| C++ `apply_influx` | retificação (só influxo > 0) | quina em I_Ca = 0 |
| C++ cinéticas | **10 clamps de τ** (max/min em τ_m, τ_h, τ_n, τ_d, τ_f, τ_p, τ_q, τ_y, τ_mp, τ_z) | quina quando o clamp ativa; efeito depende da faixa de V visitada — a verificar |
| C++ SK / BK | pow(max(1e-4, Ca)), log10(max(0.001, Ca/0.1)) | quina em Ca baixo |
| C++ acoplamento | clamp de g_c em [0, 200] mS/cm² | quina só em parâmetros extremos |
| C++ detector de PA (D122), desmame (ISIs) | limiares/contagens | **saída DISCRETA** — perda sobre contagem não é diferenciável; tempos de PA são diferenciáveis só com critério de cruzamento suave |
| C++ PSC sináptica | janelas por tempo desde o PA (0–500 ms), eventos | descontinuidades no tempo → eventos com condição de salto |
| Hay `K_Pst.mod` | τ definido por partes em v < −50 mV | quina real na dinâmica |
| Hay `SK_E2.mod` | piso de Ca (1e-7 mM) | quina em Ca baixo |
| Hay `NaTa_t`, `Nap_Et2`, `Ca_HVA`, `Ih`, `NaTs2_t` | `if (v == c)` | singularidade REMOVÍVEL (função suave) — inofensivo |
| estímulos (IClamp, epsp) | degraus/início | descontinuidades EXTERNAS no tempo → reinício com salto |
**Se se confirmar, uma escolha atende os três requisitos candidatos do L2 (item 23): diferenciável, convergido
(adaptativo, ordem variável) e em C/C++.** Pré-condição registrada: suavizar o modelo (a começar pelo piso de Ca) e
tratar eventos. Registrado no P54 como candidato.

**28. O AJUSTE DO JAXLEY NUM L5 DO ALLEN — ESCALA SIM, FIDELIDADE A VERIFICAR (registrado no P53).** Verificado no
texto integral (Deistler et al., Nature Methods 2025): **Euler implícito (tensão) + Euler exponencial (portões), passo
de 0.025 ms; NENHUM estudo de convergência em dt ou no espaço reportado**; o L5PC do ajuste sintético é o do BluePyOpt
(Van Geit 2016 — linhagem Hay 2011), o regime em que o Euler implícito a 0.025 ms NÃO converge o bAP (item 10); os 4
L5 do Allen foram ajustados nos primeiros 200 ms com perda de DTW. **Conclusão:** é evidência concreta de que o ajuste
por GRADIENTE ESCALA (19–25 parâmetros; 1 390 condutâncias por ramo) — resposta PARCIAL à pergunta "mecanismo ou
ferramenta" do P53; mas os parâmetros ajustados a dados REAIS (Allen) valem para o MODELO NUMÉRICO, não para o físico —
a mesma "terceira distância" do D128/D129 (ajuste sobre discretização não convergida). **LIÇÃO GERAL: demonstração de
ESCALA não é demonstração de FIDELIDADE — todo ajuste precisa ser feito sobre o modelo CONVERGIDO, no ESPAÇO e no
TEMPO.**

**29. VIÉS DE ESPECIFICAÇÃO — ACHADO CENTRAL DA LEITURA DE TANOH (registro).** A "pergunta realista" (verdade por
seção, ajuste por região) JÁ É modelo mal especificado: o Hay tem gradientes POR SEÇÃO (ex.: Ih exponencial ao longo do
apical, zona quente de Ca) que um ajuste por REGIÃO só representa se a forma for dada. Cramér–Rao dá só a variância; o
viés ficava fora. Critério adotado (item 26): **|viés| + 1.645·σ ≤ tolerância**. **Caso-limite registrado como
RESULTADO POSSÍVEL:** se o VIÉS SOZINHO estourar a tolerância num espaçamento, **NENHUM SENSOR BASTA ali** — o erro vem
da ESTRUTURA do modelo, não do ruído → o modelo por região precisa de mais graus de liberdade (ex.: gradientes
parametrizados), não de um sensor melhor.

**30. O PISO DE CÁLCIO É DEFEITO DE FIDELIDADE (registrado também no P54).** O piso duro no basal
(`CalciumDynamics::remove`: `excess ≤ 0 → ca = baseline`; `ca < baseline → ca = baseline`), ATIVO EM REPOUSO, não é só
obstáculo à diferenciação: o Ca real RELAXA EXPONENCIALMENTE ao basal, não bate num piso — o modelo passa o repouso
sobre uma quina que a biologia não tem. **Conserto candidato do L2 (NÃO executado):** relaxamento ao basal (ex.:
d[Ca]/dt = influxo − (SERCA + NCX)·f([Ca] − basal), contínuo e suave dos dois lados do basal) — corrige FIDELIDADE e
DIFERENCIABILIDADE de uma vez.

**31. APRENDER E JULGAR MEDEM COISAS DIFERENTES (registrado também no P53 e no P28).** As saídas do desmame (contagens
de disparo, histogramas de ISI) são DISCRETAS e não diferenciáveis. O aprendizado por gradiente NÃO PODE mirar o que o
veredito mede: otimizará grandezas CONTÍNUAS (traços de tensão, atributos suaves), e o veredito continua julgando
estatísticas discretas. Coerente com a arquitetura (quem aprende e quem julga já eram separados), mas escrito: **um
modelo bem ajustado no contínuo PODE FALHAR no veredito discreto — e isso é o veredito fazendo seu trabalho.** Mesma
regra do D130 item 4 (grandezas contínuas em vez de contagens com corte), agora por outro caminho.

**32. VERIFICAÇÕES DECLARADAS ANTES DO VEREDITO DO V2 (2026-09-29 21:41; prévia vista: só N = 16; N = 32 e N = 8 ainda
rodando; nenhuma decisão tomada sobre a prévia).**
**(a) Ponto→soma a 700 µm (medida LOCAL: injeção no próprio ponto).** Verificado: o ponto `apical_700` (apic[60],
L = 233.1 µm, arco 11.29 µm) **NÃO é nó** na discretização do V2: a 4.00 µm do nó mais próximo em N = 16 (passo 14.57
µm) e a 0.36 µm em N = 32 (passo 7.29); no L0 de referência, a 0.05 µm (Δ 0.5). O D127 mostrou que a auto-tensão em
ponto não-nó converge em 1ª ORDEM (métrica, não método) → **a falha em N = 16 pode ser convergência lenta de métrica
conhecida.** A decisão do D127 (ponto em nó) **NÃO estava declarada** para os pontos de perfil do V2 (item 5: "os pontos
do D131") → **reportado, NÃO mudado**: o veredito do V2 sai pelo critério declarado; esta ressalva acompanha. (Com a
leitura exata do item 19 já aplicada: os RED N = 16/32/8 começaram depois da correção, 18:14.) Mesma condição em
`apical_400` (4.5 µm em N = 16) e `hay_620` (0.9 / 3.0 µm em N = 16 / 32).
**(b) Tempo do 1º disparo do BAC.** Verificado: no V2, o P7 (BAC, CaBurst, EPSP) roda em **Euler implícito a passo fixo
0.025 ms NOS DOIS LADOS** (L0 e reduzido; o repouso e o P2/P3 a 0.1 ms) — o V2 foi enfileirado antes do achado do tempo
(item 10). O BAC depende do Ca-spike dendrítico, a dinâmica em que o passo fixo NÃO converge → **a diferença de
0.475 ms pode ser do INTEGRADOR, não da redução.** **Declarado:** o veredito do P7 é REFEITO com **CVode (atol 10⁻⁶) nos
DOIS lados** — L0 = Hay completo a Δ 0.5 µm; reduzido = NEURON nativo com nseg = N (≡ D126, item 19; aceita CVode) para
N ∈ {1, 2, 4, 8, 16, 32} — com os critérios INALTERADOS (nível A: mesmas contagens; nível B: mesmas contagens e 1º PA
≤ 0.2 ms). O veredito do P7 que vale é o de CVode; o de Euler 0.025 fica como registro. `hay_native.py`, protocolo
`P7cv`. **Observação (não decidida aqui):** P5 (bAP) e P6 (f-I) do V2 também rodaram em Euler 0.025 nos dois lados — a
mesma ressalva se aplica aos seus números do nível B; se refazer em CVode é decisão do usuário.

**33. DECISÃO DO USUÁRIO — P5 E P6 DO V2 REFEITOS EM CVODE NOS DOIS LADOS (2026-09-29 21:46; declarado ANTES de qualquer
resultado em CVode — nenhum P7cv/P5cv/P6cv existia; o L0 do P7cv ainda no repouso).** Critérios INALTERADOS.
- **P5 (bAP):** o passo fixo NÃO converge o bAP no Hay (0.025 ms → 27.9 mV; CVode → 35.09). O L0 é a REFERÊNCIA do
  V2; referência não convergida no TEMPO viola o princípio do D127 (a referência é a versão convergida no espaço E no
  tempo) → **o nível B do P5 a passo fixo NÃO pode ser usado.**
- **P6 (f-I):** contagens somáticas são mais robustas ao dt, mas o Hay tem RAJADAS ligadas ao Ca-spike e contagens
  perto de limiar viram com pequenos erros de tempo; o CVode é ~8× mais barato que o passo fixo convergido — refazer
  custa menos que verificar se precisa.
- **Desenho = o do BAC (item 32b):** L0 = Hay a Δ 0.5 µm; reduzido = NEURON nativo com nseg = N (≡ D126), N ∈ (1, 2, 4, 8, 16, 32); **CVode atol 10⁻⁶ nos dois lados**; P5 = bAP 1.9 nA 5 ms (amplitude = pico − repouso nos pontos do
  D131); P6 = degraus de 1 s (atraso 300 ms), 0.2…2.0 nA; PAs pelo detector IPFX sobre o traço interpolado a 0.025 ms.
  **O veredito de P5, P6 e P7 que VALE é o de CVode**; os de Euler 0.025 ficam como registro. P2/P3 (estado
  estacionário, dt 0.1 — convergido, item 10) e P4 (EPSP subliminar, Euler 0.025 — d50 convergido a 0.1%, item 11)
  seguem da fila (RED ≡ nativo, item 19). **O V2 final = P2/P3/P4 (fila) + P5/P6/P7 (CVode), pela regra do item 5.**
  `hay_native.py` protocolos `P5cv`, `P6cv`, `P7cv`; `hay_v2_final.py`.

**34. TESTE DE UMA PREMISSA — declarado ANTES do resultado do BAC em CVode (2026-09-29 21:46).** As comparações a passo fixo foram
aceitas com o argumento "mesmo dt nos dois lados ⇒ a comparação RELATIVA vale". Para EVENTOS REGENERATIVOS isso é
PREMISSA, não fato: o erro do integrador num disparo perto do limiar depende da dinâmica local, que muda com a
discretização espacial — mesmo dt não garante mesmo erro.
**Teste:** para cada N da grade, Δ_fixo(N) = t(1º PA do BAC, reduzido N) − t(1º PA do BAC, L0 Δ 0.5) em Euler 0.025
(fila) e Δ_cv(N) = a mesma diferença em CVode (nativo N × L0 Δ 0.5). **A premissa SE SUSTENTA para este evento se, em
TODO N em que as contagens do BAC coincidem nos dois integradores, |Δ_cv − Δ_fixo| ≤ 0.1 ms (metade da tolerância do
nível B, 0.2 ms) e o padrão de contagens (reduzido = L0 ou ≠) for o mesmo nos dois integradores.** Caso contrário a
premissa FALHA para eventos regenerativos → registrar e listar para revisão as comparações relativas que se apoiaram
nela: D128/D129 (Allen, degrau ativo, contagens 16/16 idênticas a Euler 0.025 — sugerem estar bem, mas a premissa que
as sustentava deixaria de ser garantida), V1/V2 P6–P7 a passo fixo, e o P6 do teste de equivalência nativo × D126
(item 19 — mesmo modelo nos dois lados, por isso não afetado pela premissa).

**35. REMISSÃO — LEVANTAMENTO DE SUBSTRATO (2026-09-30; detalhes, fontes e status MEDIDO/SIMULADO/ESTIMATIVA no P24).**
Consequências para esta linha de trabalho: (a) a decisão fidelidade × orçamento NÃO é principalmente sobre N — o
evento sináptico estoura o orçamento ~2 ordens no melhor silício existente antes de qualquer compartimento; (b) a
complexidade do modelo é requisito de HARDWARE, não só de fidelidade; (c) **o L2 é FERRAMENTA de projeto e validação,
não o que roda no implante** — os requisitos candidatos dos itens 17, 19, 23 e 27 (junções explícitas, integrador
adaptativo/de ordem maior, diferenciável) valem para a FERRAMENTA; num substrato analógico a dinâmica é física, sem dt;
(d) a pergunta decisiva do implante é a energia por evento sináptico (~0.03–0.3 pJ). Rota alternativa (computação fora
do corpo via cateter na transição) registrada como PERGUNTA ABERTA no P24; o D85 foi decidido sem avaliá-la com números
(não reabre, abre a pergunta).

**36. INCIDENTE DE EXECUÇÃO (registro de procedência).** Em 2026-09-29 às 22:38 a sessão gráfica caiu e o NEURON
abortou ("XIO fatal IO error" / "can't open DISPLAY"): perderam-se o **LIMIT (V1)** (tinha P2–P5; nada gravado — só
gravava no fim), o **RED N = 32** (idem) e a cadeia **P5cv/P6cv** (L0 Δ0.5 com 2 de 10 degraus; nativo N = 32 com 7 de
10; N = 16…1 sem nada). O **P7cv completou** para todos os N. O scratchpad (com o Hay baixado) também foi apagado.
Providências (2026-09-30): Hay rebaixado do espelho do ModelDB para `.cache/hay/` (fora do /tmp; sha256 do zip
aeeb87d9…e3555; biophys3 conferido); `hay_reduce.py`/`hay_native.py` passam a gravar o JSON a cada protocolo;
relançados, desacoplados da sessão (`setsid nohup`, sem DISPLAY, NEURON `-nogui`): LIMIT completo (P1–P5, P7, P6 a
0.6/1.2/2.0), RED N = 32 (P1–P4, o que o V2 final usa) e P5cv/P6cv (L0 Δ0.5 e nativo N = 32…1). **O LIMIT relançado já
usa a leitura exata (item 19)** — a correção offline do P3 e o refazer do P4-local declarados no item 19 ficam
dispensados. Critérios de todos inalterados.

**37. RESULTADO — TESTE DA PREMISSA (item 34), avaliado em 2026-09-30 com o P7cv completo.** Passo fixo = fila
(reduzido RED × L0 Δ0.5, Euler 0.025); CVode = nativo × L0 Δ0.5 (atol 10⁻⁶). N = 32 a passo fixo: JSON perdido na queda
(item 36) — só a contagem (2 PA, do log).
- **Pelo critério DECLARADO: SE SUSTENTA em todos os N — mas de forma VAZIA.** O "1º PA do BAC" sai em 100.000 ms em
  TODOS os casos (L0 e reduzidos, os dois integradores): é o INÍCIO do pulso somático de 1.9 nA — o detector (dV/dt >
  20 mV/ms) arma no degrau capacitivo do pulso. Δ ≡ 0 por construção. **Erro MEU na declaração: a métrica escolhida é
  fixada pelo estímulo e não mede o evento regenerativo** (família "métrica que não mede"; a mesma escolha está no nível
  B do item 5 — "1º PA ≤ 0.2 ms" do BAC também é vazio; o do CaBurst não). Não redefino o teste depois de ver os dados.
- **Descritivo (NÃO veredito) — as grandezas que medem o evento:** 2º PA do BAC (o disparo ligado ao Ca-spike) e 1º PA
  do CaBurst; L0: passo fixo 113.550 / 128.525 ms, CVode 112.950 / 128.050 ms (o passo fixo atrasa ~0.5–0.6 ms no
  absoluto). Diferença reduzido − L0:
  | N | BAC 2º PA: fixo / CVode / \|dif\| (ms) | CaBurst 1º PA: fixo / CVode / \|dif\| (ms) |
  |---|---|---|
  | 1 | +1.775 / +0.700 / **1.075** | +8.650 / +8.650 / 0.000 |
  | 2 | +0.200 / +0.075 / **0.125** | −1.325 / −1.150 / **0.175** |
  | 4 | +0.175 / +0.100 / 0.075 | +1.325 / +1.275 / 0.050 |
  | 8 | +0.075 / +0.050 / 0.025 | +1.600 / +1.475 / **0.125** |
  | 16 | 0.000 / −0.025 / 0.025 | −0.475 / −0.450 / 0.025 |
  | 32 | — / 0.000 | — / +0.150 |
  (resolução do detector: 0.025 ms.) Leitura: nas grandezas informativas a premissa vale em N = 16 (≤ 0.025 ms) e
  FALHA nos N grossos (1, 2, 8 acima de 0.1 ms) — o erro do integrador num evento regenerativo depende da
  discretização espacial, como se suspeitava. **Formalmente a lista de revisão do item 34 NÃO entra em vigor (o critério
  declarado passou); materialmente, o descritivo mostra que a premissa não é garantida em N grosso.** Os casos do
  Allen: D129 comparou N = 16 (piramidal) e N = 8 (interneurônio) — o N = 8 está na faixa em que o descritivo mostrou
  0.125 ms. **Decisão do usuário:** redeclarar o teste sobre o 2º PA do BAC e o 1º do CaBurst (e o nível B do P7 idem)
  — sabendo que os números já foram vistos — ou manter o resultado formal com esta ressalva.
- **Achado colateral (responde ao item 32b):** a diferença de 0.475 ms em N = 16 que fez a prévia falhar o nível B era
  do CaBurst, e **PERSISTE em CVode (0.450 ms)** → é da REDUÇÃO em N = 16, não do integrador. Em N = 32 (CVode) ela cai a
  0.150 ms (< 0.2).

**38. REMISSÃO — ROTA ALTERNATIVA REFINADA (P24, adendo 2 de 2026-09-30; pergunta aberta).** Forma HÍBRIDA: aprendizado
LOCAL nos HanuR (tensões, transitório, ≤ ~11% por vez) + operação FORA do corpo com só EVENTOS cruzando o cateter.
Ressalvas: sinapses elétricas contínuas, neuromodulação (D68) a revisar, e o risco central agravado (o canal carrega a
mente em OPERAÇÃO — falha = interrupção). Correções de números da rodada e o padrão "número de trecho de busca com
confiança acima da sustentada" registrados no P24.

**39. DECISÃO DO USUÁRIO — REDECLARAÇÃO DO TESTE DA PREMISSA E DO NÍVEL B DO BAC (2026-09-30 09:54).** Manter o resultado formal
do item 37 registraria um APROVADO SEM INFORMAÇÃO — o "verde que não prova". **Correção de registro:** a atribuição dos
0.475 ms ao BAC (relatório anterior; repetida no pedido) estava ERRADA — eram do CaBurst (1º PA). **Justificativa da
redeclaração (registrada):** (i) o argumento para trocar a métrica é INDEPENDENTE DOS NÚMEROS — o 1º PA do BAC é
artefato do estímulo, fato verificável sem olhar resultado; (ii) a redeclaração produz resultado DESFAVORÁVEL (a
premissa falha), o oposto do risco que a regra de não redeclarar existe para impedir; (iii) o limite de 0.1 ms fica
INALTERADO. **Métricas novas:** 2º PA do BAC (o ligado ao Ca-spike) e 1º PA do CaBurst; mesmo critério (em todo N em
que as contagens coincidem nos dois integradores, |Δ_cv − Δ_fixo| ≤ 0.1 ms, e mesmo padrão de contagens).
**VEREDITO: a premissa FALHA em N = 1, 2 e 8; vale em N = 16** (N = 32 sem passo fixo — item 36). O erro do integrador
num evento regenerativo DEPENDE da discretização espacial. **Consequência: a lista de revisão do item 34 ENTRA EM
VIGOR** (item 41). **Nível B do BAC (item 5) redeclarado sobre o 2º PA** pela mesma razão (o do CaBurst segue no 1º
PA; o do EPSP não tem PA); `hay_v2_final.py` ajustado antes do veredito do V2.

**40. REGISTROS (usuário).**
(a) **Achado colateral:** os 0.475 ms em N = 16 eram do CaBurst e PERSISTEM em CVode (0.450) — vêm da REDUÇÃO, não do
integrador; em N = 32 (CVode) 0.150 ms, abaixo do limite. **Se o V2 confirmar, o N do Hay será 32 e o custo da Etapa A
DOBRA: ~52 dias-CPU (~18 dias em 3 núcleos).**
(b) **Contraste (condicionado ao fechamento do V2):** no Allen, o N era decidido pelo TUFO DESCONECTADO (artefato do
ajuste — D127/D128). No Hay, seria decidido pelo SPIKE DE Ca DENDRÍTICO, que o modelo foi ajustado para reproduzir a
partir de dados reais — **seria o primeiro N do projeto ancorado numa grandeza dendrítica FISIOLÓGICA.** [~~RISCADO (D132 item 75):~~ histórico do risco desfeito — o N = 32 se apoiava no 1º PA do CaBurst, e o "1 disparo em ~128.5 ms" vinha do REPOUSO NÃO CONVERGIDO (3 s); com repouso convergido (~21.5 s) o CaBurst de 1.5 nA não produz disparo somático, no L0 nem no reduzido.] [**RISCO DESFEITO (D132 item 78):** o motivo do risco era artefato de um defeito meu (o CVode pulava o EPSC tardio); o CaBurst dispara com repouso convergido.]
(c) **REGRA NOVA — CONTROLE NEGATIVO DE MÉTRICA DE EVENTO:** toda métrica baseada em EVENTO precisa ser verificada
contra o ESTÍMULO SOZINHO (sem dinâmica ativa — modelo passivo) antes de virar critério. Mesmo princípio do controle
negativo `ModelIsSilentWithoutInput`, agora aplicado às métricas. **Declarado como se verifica:** para cada protocolo
com métrica de evento, roda-se o modelo PASSIVO (só `pas`) com o mesmo estímulo; se o detector IPFX **ARMA** (dV/dt >
20 mV/ms) na janela da métrica, os TEMPOS de PA dessa janela são suspeitos de artefato (a contagem pode estar certa —
o PA real vem depois do armamento — mas o tempo é o do estímulo); se além de armar ele CONTA (pico > −30 mV em 5 ms),
a contagem também é artefato. Aplicado retroativamente às métricas de evento do D132 (P5, P6, P7, C3, conjunto
funcional do D131 7.4) no Hay e às do degrau ativo do Allen (D128/D129). `neuron/event_negcontrol.py`.

**41. LISTA DE REVISÃO DO ITEM 34 EM VIGOR — DEGRAU ATIVO DO ALLEN EM CVODE, começando pelo INTERNEURÔNIO em N = 8
(declarado 2026-09-30 09:54, antes de rodar).** Critérios INALTERADOS (D123 via `compare_active.py`; convergência do L0 pelo do
D128). Desenho: CVode atol 10⁻⁶ nos DOIS lados; L0 = Allen all active (axônio truncated), nseg = max(regra do Allen,
⌈L/Δ⌉), Δ = 2 e 1 µm (convergência Δ2 → Δ1 pelo critério do D128; referência = Δ1; onde não convergir, Δ0.5); reduzido
= NEURON nativo com nseg = 8 (≡ D126, item 19 — o Allen tem densidades uniformes por região); **pré-condição barata:**
nativo N = 8 em Euler 0.025 reproduz o RED N = 8 do D128 (`results/active/pv_RED_amps.json`) nas contagens — se não,
parar e reportar. Protocolo do D128: degraus de 1 s (atraso 300, 1 500 ms) nas mesmas 14 amplitudes (330–600 pA) +
noise1 (21 s); detector IPFX no traço interpolado a 0.025 ms. **Reportar se o veredito do D129 (PASSA) muda.** Prioridade
à fila do V2 (processos com `nice 19`). Depois, o piramidal em N = 16. `neuron/active_cvode.py`.

**42. RESULTADOS (2026-09-30 10:35) — CONTROLE NEGATIVO DAS MÉTRICAS DE EVENTO (item 40c) E PRÉ-CONDIÇÃO DO ALLEN (item 41).**
**(A) Controle negativo** (`event_negcontrol.py`, modelo PASSIVO, mesmo estímulo, passo 0.025 ms; `results/negcontrol/`):
| protocolo | detector no PASSIVO | no modelo ATIVO (traço bruto × detector) | efeito na métrica |
|---|---|---|---|
| Hay P5 (1.9 nA 5 ms) e P7 BAC | ARMA no início do pulso (49 mV/ms) | 1º PA datado no início (100.000 / 50.000) | contagem ok; TEMPO do 1º PA = artefato (já tratado: BAC pelo 2º PA — item 39; C3 usa contagem e amplitude) |
| Hay P7 CaBurst, EPSP | não arma (≤ 0.8 mV/ms) | — | LIMPO |
| Hay P6 f-I 0.2–0.6 nA | não arma | — | LIMPO |
| **Hay P6 f-I 0.8–2.0 nA** | **ARMA no início do degrau** (21–52 mV/ms) | CVode, L0 Δ1: 1.2 nA 1º pico 6.3 ms → detector 5.93 (limite); **1.6 nA pico 4.03 ms → detector 0.0; 2.0 nA pico 2.85 → 0.0** | contagem ok nesses casos, mas **1º PA datado no início** → latência, 1º ISI, adaptação e taxa por ISI CONTAMINADOS; risco de ±1 no fio da navalha (item C) |
| **Allen PV, degraus 330–600 pA e noise1** | **ARMA no início** (25–46 mV/ms) | traço bruto, L0 Δ2: 410 pA pico 5.70 → detector 5.275; **420 pA pico 5.10 → detector NÃO vê (1º = 17.05 = o 2º PA); 450 pA pico 4.00 → idem** | **no D128/D129, de 420 a 600 pA as contagens estão 1 ABAIXO e a "latência" é a do 2º PA**; o critério de latência do D123 era avaliado em 420 pA (reobase + 40) — comparou 2ºs PA nos dois lados |
| Allen piramidal, degraus 250–500 pA e noise1 | não arma (≤ 5.8 mV/ms) | — | LIMPO |
**Mecanismo:** o detector de análise (`active_l1_detect.spikes`) arma na BORDA dV/dt > 20 e segue enquanto dV/dt > 0 até
5 ms; o salto capacitivo do degrau o arma no instante do estímulo; se o PA real atinge o pico dentro desses 5 ms, é
contado com o tempo do ESTÍMULO; se o pico cai logo depois, o PA é ENGOLIDO (a borda já passou). **O detector falha o
seu controle negativo nos protocolos com degrau somático grande.**
**(B) C++ (D122, `HHNeuronModel`) — lógica DIFERENTE, a verificar (não afirmado):** re-arma por NÍVEL a cada passo e
confirma no pico → não engole o PA; mas, se o tempo limite de 5 ms estourar no meio da subida com V > −30 mV, o PA pode
ser contado DUAS vezes (confirmação no limite + nova confirmação no pico).
**(C) Pré-condição do item 41 — FALHOU, e parei (como declarado).** Nativo N = 8 em Euler 0.025 × RED N = 8 do D128:
contagens iguais até 410 pA; **de 420 a 600 pA o nativo tem exatamente 1 PA a mais**. Diagnóstico: fora o 1º PA, os
tempos coincidem (< 0.05 ms) — as dinâmicas são idênticas; no nativo o 1º PA cai dentro dos 5 ms armados (contado, com
tempo 0.0); no RED do D128 cai logo depois (engolido). **A falha é do DETECTOR no fio da navalha, não da equivalência**
(item 19 segue de pé). A cadeia do Allen em CVode foi PARADA (nativo e L0 parciais em `results/active_cvode/`, só
registro). **Nenhum veredito do Allen em CVode ainda.**
**Proposta (NÃO adotada — decisão do usuário):** trocar o detector de ANÁLISE por um detector PICO-PRIMEIRO — achar picos
> −30 mV com proeminência ≥ 20 mV e só então procurar para trás o instante em que dV/dt cruzou 20 mV/ms (o tempo do PA)
—, imune ao salto do estímulo; ele próprio tem de passar o controle negativo (passivo: zero PA) e reproduzir os picos
brutos no ativo. Depois: refazer o Allen (D128/D129) e o P6 do V2 com ele. O detector do C++ (produção) fica para
verificação à parte (item B).

**43. DECISÃO DO USUÁRIO — DETECTOR NOVO DA ANÁLISE, VALIDAÇÃO OBRIGATÓRIA, E O DE PRODUÇÃO (2026-09-30 12:03; declarado antes de
validar). `neuron/detect_peak.py` (o `active_l1_detect.spikes` fica intacto — a fila do V2 o importa).**
**Regras do detector:** (1) candidato = pico local do V do soma com altura > −30 mV e proeminência ≥ 20 mV (traço a
0.025 ms); (2) a subida = o cruzamento de dV/dt > 20 mV/ms MAIS PRÓXIMO do pico, exigido a ≤ 5 ms do pico (max_interval
do IPFX) — **acréscimo meu, declarado:** sem ele o MÁXIMO DE FIM DE DEGRAU de um modelo passivo (no Hay passivo a 2 nA,
+67 mV com proeminência enorme) passaria como pico; (3) **AJUSTE (a) do usuário:** início = começo do trecho contínuo
com dV/dt > 20 que termina na subida; se esse trecho começa num instante de ESTÍMULO (sem intervalo com dV/dt abaixo do
limiar separando-o), o disparo é **AMBÍGUO: CONTA, sem data de início**; os ambíguos são contados por protocolo;
(4) **AJUSTE (b) do usuário — MARCAS:** **tempo do PICO** para toda comparação de MÉTODO (reduzido × L0; nativo × RED;
premissa do item 34/39; nível A/B do V2; critérios do D123 entre modelos) e para ISIs; **cruzamento de limiar** SÓ em
comparação com DADOS que usam a convenção do IPFX (latência nos registros do Allen) — hoje nenhum critério do D132.
**Validação obrigatória (regra para TODO detector futuro):** (i) CONTROLE NEGATIVO — modelo PASSIVO com os mesmos
estímulos de todos os protocolos (Hay: P5, P7 BAC/CaBurst/EPSP, P6 0.2–2.0 nA; Allen PV e piramidal: todos os degraus e
noise1): NENHUMA detecção; (ii) CONTROLE POSITIVO PERTO DO ESTÍMULO — modelo ATIVO em CVode, Hay f-I 1.2/1.6/2.0 nA e
PV 420/450 pA: os picos detectados coincidem (± 1 amostra) com TODOS os picos brutos > −30 mV da janela do degrau; o 1º
PA real é contado, com tempo de pico correto, início datado ou ambíguo. **Só com os dois passando o detector entra em
uso.** `neuron/validate_detector.py`.
**Produção (C++, `HHNeuronModel`, D122) — PRIORIDADE:** ele alimenta o ENGATE A → histogramas de ISI do DESMAME; contagem
dupla cria ISI curto falso; omissão funde dois ISIs (o P26 de novo, pelo detector). Os mesmos dois controles pelo
caminho de produção, SEM modificar o código, num driver separado (`neuron/hh_detector_check.cpp`): passivo = todas as
condutâncias ativas zeradas via `update_conductances()` (API pública); referência = picos brutos do V do soma. Reportar:
engole, conta em dobro, ou passa. **Não consertar nesta rodada.**
**Ordem depois da validação:** 1º pré-condição do Allen (nativo N = 8 × RED N = 8, passo fixo) com o detector novo → se
passar, Allen em CVode, interneurônio primeiro; 2º métricas de TEMPO do f-I do V2 (latência, 1º ISI, adaptação, taxa
por ISI) de 0.8 a 2.0 nA com o detector novo; 3º corrigir os números absolutos do interneurônio do D128/D129 e
VERIFICAR (não presumir) se a aprovação relativa sobrevive.

**44. RESULTADOS (2026-09-30 13:07) — VALIDAÇÃO DO DETECTOR NOVO E DIAGNÓSTICO DO DE PRODUÇÃO.** (`results/detector/`)
**Detector novo (`detect_peak`) — VALIDADO, entra em uso:**
- **Controle NEGATIVO — PASSA:** 0 detecções em 46 protocolos passivos (Hay: P5, P7 BAC/CaBurst/EPSP, P6 0.2–2.0 nA —
  14; Allen PV: 14 degraus + noise1 — 15; Allen piramidal: 16 degraus + noise1 — 17). O máximo de fim de degrau do
  Hay passivo (até +67 mV) é rejeitado pela regra 2 (subida a ≤ 5 ms do pico).
- **Controle POSITIVO — PASSA** (CVode atol 10⁻⁶): picos detectados = picos brutos, um a um:
  | caso | detectados / brutos | 1º PA: pico (após o início) | início datado | ambíguos |
  |---|---|---|---|---|
  | Hay f-I 1.2 nA | 18 / 18 | 6.300 ms | 5.930 ms | 0 |
  | Hay f-I 1.6 nA | 20 / 20 | 4.025 ms | 3.657 ms | 0 |
  | Hay f-I 2.0 nA | 20 / 20 | 2.850 ms | 2.479 ms | 0 |
  | PV 420 pA | 36 / 36 (o antigo via 34–35) | 4.875 ms | 4.491 ms | 0 |
  | PV 450 pA | 54 / 54 | 3.800 ms | 3.412 ms | 0 |
  Nenhum ambíguo nesses casos: o dV/dt cai abaixo de 20 mV/ms entre o salto do estímulo e a subida do PA.
**Detector de PRODUÇÃO (C++, D122) — diagnóstico, SEM conserto** (`neuron/hh_detector_check.cpp`; modelo padrão sem
modificação; passivo via `update_conductances()` com todas as condutâncias ativas zeradas):
- **Controle POSITIVO — PASSA** nos dois dt (0.1 = produção, e 0.025 ms), degraus de 2 a 500 µA/cm²: nenhum pico
  ENGOLIDO, nenhum EM DOBRO, nenhum ESPÚRIO; o evento sai 1 passo depois do pico. **A contagem dupla levantada como
  dúvida (item 42B) NÃO apareceu** nesses protocolos (não testado sob ruído).
- **Controle NEGATIVO — FALHA:** no modelo PASSIVO, `just_spiked()` dispara em degraus ≥ 75 µA/cm² (1 evento no início)
  e em pulsos de 5 ms de 80–300 µA/cm² (nos dois dt) — a subida puramente passiva passa de −30 mV com proeminência ≥ 20
  mV e é confirmada no limite de 5 ms (degrau) ou no fim do pulso (dV/dt ≤ 0). Pulsos ainda maiores (≥ 400 µA/cm²) não
  deram evento — provável acionamento do guard (D115), não verificado.
- **Consequência:** a produção não engole nem duplica; o risco é OUTRO — **estímulo forte sem dinâmica ativa vira
  "disparo"** no ENGATE A → entra nos histogramas de ISI do desmame como PA falso. Relevante sempre que o próprio HANU
  injeta corrente no modelo (estimulação) ou que uma entrada somática grande despolariza o soma acima de −30 mV sem PA.
  O detector novo da análise resolveria (exige subida a ≤ 5 ms do PICO local com proeminência); conserto é decisão do
  usuário (não nesta rodada).

**45. DECISÃO DO USUÁRIO — DETECTOR DE PRODUÇÃO: MEDIR O RISCO, DEPOIS UNIFICAR (2026-09-30 14:41; declarado antes de medir).**
**Registros:** o detector novo da análise passou nos dois controles (item 44); o reduzido dando 34 ou 35 PA a 420 pA
conforme minúcias de implementação confirma que o antigo estava no fio da navalha. Produção: POSITIVO passa (não engole,
não duplica — **a suspeita de contagem dupla estava ERRADA** [**CORRIGIDO no item 46:** errada só nos degraus do teste;
sob bombardeio de PSCs a produção conta EM DOBRO ~7% dos PAs]); NEGATIVO FALHA. **Pela regra do item 40c, um detector que
falha o controle negativo NÃO PODE alimentar critério — e este alimenta o ENGATE A e o desmame → correção
OBRIGATÓRIA, independentemente do tamanho do risco.**
**Escala das entradas de produção (medida no código, para comparar com as fronteiras):** soma do `HHNeuronModel` =
cilindro 20 × 20 µm (≈ 1 257 µm²) → **1 nA ≈ 79.6 µA/cm²** (conversão do D112, `na_to_ua_cm2_for_`); um PSC AMPA de
peso 1 (15 nS × 65 mV) ≈ 0.98 nA de pico ≈ **78 µA/cm²**, forma α (τ 0.5/3 ms) — ~3–5 ms de largura; controle
`hanu_control_level_ × 0.05` ≤ 5 µA/cm² DC. **O PSC unitário já cai na região em que a produção falha no passivo.**
**2. RISCO REAL (antes do conserto) — declarado:** modelo de PRODUÇÃO ATIVO (padrão, sem modificação), dt 0.1 ms
(produção); os DOIS detectores sobre os MESMOS traços do soma — o de produção (`just_spiked`, com o filtro de 2 ms do
ENGATE A aplicado como na produção) e o validado da análise (`detect_peak`, sobre o traço exportado). Cenários: (S1)
PAR DE PULSOS — um pulso forte provoca um PA; um 2º estímulo cai 2–15 ms depois do pico (refratário relativo), em forma
de degrau de 2 ms e de PSC α (τ 0.5/3), amplitudes 20–800 µA/cm²; (S2) BLOQUEIO — degraus de 75/150/300 µA/cm² por 300 ms
com pulsos superpostos a cada 20 ms; (S3) BOMBARDEIO — PSCs α de ~78 µA/cm² (e 0.5×, 2×) em taxas de 200–2 000 Hz por
2 s. Reportar TODA discordância com tempo e contexto (tempo desde o PA real anterior; dentro/fora de estímulo); em
destaque as detecções de produção 2–10 ms após um PA real (ISI curto inventado que passa pelo filtro de 2 ms).
**3. FRONTEIRA DE FALSO POSITIVO — declarado:** modelo PASSIVO de produção (condutâncias ativas zeradas via API), dt 0.1;
estímulo retangular amplitude (5–5 000 µA/cm², grade log) × duração (0.5–1 000 ms) e PSC α (τd 1/3/5/10 ms, mesma grade
de amplitude); para CADA detector, a menor amplitude que gera detecção em cada duração → fronteira; comparar com a faixa
de entradas acima (PSC unitário ~78 µA/cm², somas coincidentes, controle).
**4. UNIFICAR (depois do 2) — declarado:** UMA definição, na análise e na produção: **pico > −30 mV, proeminência ≥ 20 mV,
subida (último dV/dt > 20 mV/ms antes do pico) a ≤ 5 ms do pico.** Na produção: o detector passa a guardar o candidato a
pico e o vale anterior e **confirma quando V cai 20 mV abaixo do pico** (proeminência do lado direito), antes de outro pico
mais alto; o evento é EMITIDO nessa confirmação. **Convenção de tempo (declarada):** o TEMPO DO PA é o do PICO
(`last_spike_time_ms_` = tempo do pico); a EMISSÃO (just_spiked, ENGATE A, ELO 1) ocorre na confirmação, ~0.4 ms depois
(a medir); o registro no desmame e o `SpikeEvent` do ELO 1 passam a usar o TEMPO DO PICO, e o atraso sináptico do
D110/D111 conta a partir dele — a latência da discriminação fica na mesma convenção. Validar pelos dois controles pelo
caminho de produção; **rodar a suíte: todo teste que quebrar estava apoiado no artefato — REPORTAR, não ajustar.**

**46. RESULTADOS (2026-09-30 14:46) — RISCO REAL E FRONTEIRAS; A UNIFICAÇÃO COMO DECLARADA FICA SUSPENSA.**
(`neuron/hh_detector_risk.cpp` + `.py`; `results/detector/risk_prod_antes.json`, `risk_prod_classificado.json`)
**(2) Risco no modelo de produção ATIVO (dt 0.1; eventos após o filtro de 2 ms do ENGATE A; referência = detector da
análise sobre o mesmo traço; um evento "pertence" a um PA se cai entre 5 ms ANTES e 0.5 ms DEPOIS do seu pico):**
| cenário | PAs (análise) | 1 evento | perdidos | EM DOBRO | eventos sem PA | desses, 2–10 ms após um PA real |
|---|---|---|---|---|---|---|
| S1 par de pulsos (2º estímulo 2–15 ms após o pico; 20–800 µA/cm²; degrau 2 ms e α) | 366 | 366 | 0 | 0 | 0 | 0 |
| S2 bloqueio (degrau 75/150/300 + pulsos a cada 20 ms) | 284 | 278 | 6 | 0 | 7 | 0 |
| **S3 bombardeio de PSCs α (39/78/156 µA/cm², 200–2 000 Hz, 2 s)** | 939 | 787 | **84** | **68** | **184** | **44** |
**Leitura:** no refratário relativo e no bloqueio a produção quase não erra; **sob bombardeio de PSCs — a entrada real
de rede — ela perde ~9% dos PAs, conta ~7% em DOBRO e cria ~20% de eventos sem PA, 44 deles 2–10 ms depois de um PA
real (ISI curto INVENTADO que passa pelo filtro de 2 ms e entra no histograma do desmame).** **A suspeita de contagem
dupla (item 42B), dada como errada no item 45, estava CERTA para esta condição:** o limite de 5 ms estoura na subida
lenta sob PSCs e o PA é confirmado duas vezes. (Correção do registro do item 45.) **Ressalva:** a referência (detector
da análise) tem ela própria região de falso positivo nessas amplitudes (fronteira abaixo) — as discordâncias do S3 são
entre DOIS detectores imperfeitos; a classificação evento a evento exige um critério independente (abaixo).
**(3) Fronteira de falso positivo no PASSIVO de produção (menor amplitude com detecção, µA/cm²):**
| estímulo | produção | análise "validada" |
|---|---|---|
| degrau 0.5 / 1 / 2 / 3 ms | 199 / 158 / 100 / 100 | 199 / 158 / 100 / 100 |
| degrau 4 / 5 ms | 79 / 79 | 79 / 79 |
| degrau 6 / 7 / 8 ms | 79 / 79 / 79 | 199 / 251 / 316 |
| degrau ≥ 10 ms (até 1 s) | **79** | **nunca** |
| PSC α τd 1 / 3 / 5 / 10 ms | 158 / 126 / 100 / 100 | 158 / 126 / 100 / 158 |
**Faixa real de entrada:** PSC unitário ≈ 78 µA/cm² (α, τd 3); dois coincidentes ≈ 156. **Margem:** produção — nula
para degraus ≥ 4 ms (79 ≈ 78); **análise — também nula ou negativa para estímulos CURTOS (PSC α τd 3: 126 µA/cm² = 1.6
PSCs coincidentes).** **A premissa da unificação ("pico + proeminência + subida ≤ 5 ms separa o disparo do estímulo por
construção") é FALSA para estímulos curtos e fortes:** a resposta passiva a um pulso ≤ 5 ms que passa de −30 mV tem
pico, proeminência e subida curta — a definição não a distingue de um PA. **E a validação do item 44 passou nos modelos
do NEURON só porque os estímulos dos protocolos não levavam o soma PASSIVO acima de −30 mV** (o Hay tem soma grande e Rin
~40 MΩ; o soma do modelo de produção tem 1 257 µm² e sobe muito mais) — **passar nos protocolos usados não mostrou onde
o detector começa a falhar; a varredura mostrou** (exatamente a razão do item 3 do pedido).
**(4) UNIFICAÇÃO — SUSPENSA, código de produção NÃO alterado.** Unificar como declarado daria à produção um detector que
FALHA o controle negativo em entradas realistas — a regra do item 40c o proíbe. **Decisão do usuário.** Opções
(propostas, não adotadas): (i) **critério pela CORRENTE REGENERATIVA** — PA = pico da corrente de Na (ou de m³h·g_Na)
acima de um limiar; o modelo de produção conhece os próprios portões; um modelo passivo não tem I_Na → o controle
negativo passa POR CONSTRUÇÃO; na análise, gravar `ina` no NEURON; (ii) acrescentar à forma de onda um critério que a
resposta passiva não cumpre (dV/dt máximo da subida ≫ o de um PSC; largura a meia altura curta); (iii) manter a
convenção de TENSÃO (IPFX) só para comparação com DADOS (registros do Allen), onde não há acesso aos portões. Em qualquer
caso: validar pelos dois controles E pela varredura de fronteira contra a faixa real de entradas, antes de usar.
**Detector da análise em uso (item 44):** segue válido NOS protocolos em que foi validado (estímulos que não levam o
soma passivo acima de −30 mV) — Hay e Allen do D128–D132; **não vale** para protocolos com pulsos curtos fortes.

**47. DECISÃO DO USUÁRIO — CRITÉRIO DE DISPARO: DOIS PAPÉIS, DOIS CRITÉRIOS (2026-09-30 14:53; declarado antes de medir; nada no
código de produção — desenho e validação no harness).**
**Registros:** (a) a validação do item 44 passou por causa dos PROTOCOLOS, não do detector (nos modelos do NEURON a
resposta passiva nunca passava de −30 mV; o soma de produção sobe muito mais; a varredura revelou); (b) a unificação foi
recomendada antes de a fronteira estar mapeada — a suspensão estava certa; (c) correção do item 45: a contagem dupla
ACONTECE sob bombardeio (~7%); (d) o risco sob entrada de rede é ALTO no detector atual, mas a tabela do item 46 compara
dois detectores imperfeitos e NÃO dá o erro verdadeiro.
**Decisão:** **EMISSÃO (ELO 1)** — pergunta INTERNA ao modelo, que conhece a verdade → **(i) CORRENTE REGENERATIVA DE Na no
SEGMENTO INICIAL DO AXÔNIO** (local de saída; spike dendrítico que não chega lá não é saída). **COMPARAÇÃO (desmame,
validação, registros do Allen)** — o critério tem de ser O MESMO dos dois lados e a célula só expõe tensão → **(ii)
critério de FORMA DE ONDA sobre a tensão, idêntico nos dois lados e no MESMO LOCAL** (a tensão do modelo no ponto que o
elemento mede na célula — assumido o SOMA nesta rodada, registrado como premissa). Coerente com o P26. **(iii) ADOTADO:**
convenção de tensão do IPFX SÓ para comparação com registros do Allen.
**Declarado antes de medir:**
- **Leitura de (i) sem tocar a produção:** o driver reproduz os portões m e h do Na no AIS (compartimento 0) a partir da
  API PÚBLICA — `kinetics_at_V()` (as MESMAS fórmulas de `Na_kinetics`, que é interna) + Q10 = 3 documentado + a regra de
  atualização exponencial com o V do AIS no início de cada passo (a do `step`) — e calcula I_Na,AIS = g_Na·escala_AIS·m³h·
  (V − E_Na). Dependência registrada: se `Na_kinetics`/Q10 mudarem, o espelho tem de mudar junto.
- **Distribuição do pico de I_Na por evento** (todas as entradas: par de pulsos, bloqueio, bombardeio, e os degraus do
  item 43): evento = pico local da corrente de Na para dentro. **BIMODAL** se, no histograma do log₁₀ do pico, houver um
  intervalo de ≥ 1 década com < 1% dos eventos e ≥ 5% dos eventos de cada lado; **limiar = centro geométrico da maior
  lacuna assim.** Se não for bimodal: reportar e NÃO escolher número (outra formulação de (i), ex.: realimentação
  positiva — corrente para dentro crescendo com a tensão).
- **Gabarito:** PA = pico de I_Na,AIS acima do limiar derivado; tempo = tempo desse pico. Um detector acerta um PA se tem
  exatamente um evento em [t − 1, t + 3] ms; conta-se perdidos, em dobro e falsos, por detector e por cenário.
- **Detectores pontuados:** o de produção atual (após o filtro de 2 ms); o da análise (pico/proeminência/subida); e
  candidatos de (ii) sobre o V do SOMA: (C1) dV/dt máximo da subida (5 ms antes do pico) ≥ X; (C2) largura a meia altura
  (entre o vale dos 5 ms anteriores e o pico) ≤ Y; (C3) C1 e C2. **X e Y ancorados em DADO PRIMÁRIO, não no modelo:** as
  formas dos PAs MEDIDOS da célula 471129934 (CSVs vendorizados a 0.1 ms: long square 310/430 pA, short square 1 100 pA,
  noise1) e das flutuações SUBLIMIARES medidas (long square 150 pA, trechos sublimiares do noise1) — X e Y na lacuna entre
  as duas populações medidas; se não houver lacuna nos dados, reportar. (Ressalva: a 0.1 ms o dV/dt máximo do PA é
  subestimado — vale igualmente para o modelo a dt 0.1.)
- **Melhor candidato de (ii)** = o que mais se aproxima do gabarito nos traços ativos E passa na varredura de fronteira
  passiva (item 46) contra a faixa real de entrada (PSC unitário ~78 µA/cm²; dois coincidentes ~156).
- **Só depois** (próxima rodada): implementar (i) na emissão e (ii) no ENGATE A e na leitura biológica, validar pelos dois
  controles e pela fronteira, rodar a suíte (quebras = apoio no artefato; reportar, não ajustar).

**48. RESULTADOS (2026-09-30 14:58) — (i) NÃO É BIMODAL; (ii) TEM LACUNA NOS DADOS MEDIDOS, MAS O MODELO NÃO A CUMPRE.**
(`neuron/hh_na_truth.cpp`; `results/detector/na_peaks.json`, `allen_forma_pa.json`)
**(i) Pico de I_Na no AIS por evento** (7 573 eventos: par de pulsos 675, bloqueio 998, bombardeio 5 633, degraus 267):
modo largo em ~30–60 µA/cm², modo estreito em ~1 000–1 250 µA/cm² (os PAs completos) e **um CONTÍNUO entre eles**
(100–1 000 µA/cm²: par de pulsos 83, bloqueio 104, bombardeio 585, degraus 3) — **NÃO BIMODAL pelo critério declarado**
(nenhum intervalo de ≥ 1 década com < 1% dos eventos). **Nenhum limiar escolhido.** O contínuo vem exatamente dos casos
difíceis (ativação parcial, PA abortado no refratário e no bloqueio, somação sob bombardeio); nos degraus limpos a
separação é quase perfeita (3 intermediários em 267). **Consequência: (i) precisa de outra formulação** (proposta, não
adotada: condição REGENERATIVA no AIS — corrente iônica líquida para dentro e crescendo com a tensão, i.e. condutância
de inclinação negativa; os portões de K, leak e NaP do AIS também são espelháveis pela API pública). **Sem gabarito, a
pontuação dos detectores contra (i) NÃO foi feita.**
**(ii) Forma de onda — âncora em DADO PRIMÁRIO** (célula 471129934, CSVs medidos a 0.1 ms): 58 PAs (pico > 0 mV): dV/dt
máximo **197–431 mV/ms** (mediana 259), largura a meia altura 0.80–1.20 ms; 127 flutuações sublimiares (pico < −40 mV,
proeminência ≥ 2 mV): dV/dt máximo 0.47–91 mV/ms, largura 0.20–15.4 ms. **Lacuna em dV/dt: 91 → 197 → X = 134 mV/ms**
(centro geométrico); **em largura, SEM lacuna** (ruído sublimiar estreito) → C2 e C3 caem pelos dados; fica **C1 =
definição da análise + dV/dt máximo da subida ≥ 134 mV/ms.**
**Fronteira passiva de C1** (produção, µA/cm²): PSC α τd 1/3/5/10 → **397 / 500 / 500 / nunca** (antes 158/126/100/158);
degraus ≤ 5 ms → **251** (antes 79–199); ≥ 6 ms → nunca. **Margem contra dois PSCs coincidentes (~156): 1.6× (degrau
curto) a 3.2× (PSC α).**
**MAS o modelo de produção NÃO cumpre a forma medida:** nos degraus limpos, seus PAs (Na do AIS completo, 687–1 112
µA/cm²) sobem no SOMA a **82–~200 mV/ms (mediana 128)** — só 28% ≥ 134 → **C1 perderia ~72% dos PAs reais do modelo.** O PA
somático do modelo de 4 compartimentos é mais lento que o da célula medida (fidelidade — liga à pergunta 2 do P53/P54).
Critério "idêntico nos dois lados" + modelo com forma de PA errada = o veredito diferiria por causa da FORMA do PA do
modelo (o que é defeito do modelo, não do detector) — decisão do usuário: corrigir a forma do PA do modelo antes, ou
outra formulação de (ii).
**Releitura do item 46:** sob bombardeio, os "picos" do detector da análise têm dV/dt mediano de 41 mV/ms e Na do AIS
mediano de 46 µA/cm² — **em sua maioria NÃO são PAs** (picos de somação de PSCs acima de −30 mV). A linha S3 da tabela do
item 46 comparava dois detectores que contam não-PAs; como já ressalvado, não dá o erro verdadeiro.
**Nada implementado** (item 5 do pedido: só com (i) e (ii) validados).

**49. DECISÃO DO USUÁRIO — ANCORAR NA CÉLULA, VALIDAR NAS REFERÊNCIAS, NÃO DOBRAR PARA O MODELO DE PRODUÇÃO (2026-09-30 15:31;
declarado antes de medir; nada no código de produção).**
**(1) (ii) mantém a âncora na CÉLULA.** O modelo de produção perder ~72% dos próprios PAs é defeito de FIDELIDADE do
modelo; (ii) NÃO é reformulado para acomodá-lo (seria dobrar a régua; o desmame passaria a medir o detector).
**Limiar na resolução NATIVA (declarado):** as MESMAS varreduras dos CSVs (manifest: 38, 46, … — long square 150/310/430,
short square 1 100, noise1), lidas do NWB original (200 kHz, sem filtro); mesma separação de populações (PA: pico >
0 mV; sublimiar: pico < −40 mV com proeminência ≥ 2 mV); dV/dt máximo nos 5 ms antes do pico; lacuna e X (centro
geométrico) em 200 kHz e em taxas reduzidas por decimação com anti-alias (FIR polifásico, o do `extract_allen`): 100,
50, 20, 10, 5 kHz. **Taxa mínima de amostragem = a menor taxa em que ainda há lacuna (min dV/dt dos PAs > máx dos
sublimiares).** Requisito de hardware → P24/P54.
**(2) Antes de culpar a forma do PA:** dV/dt somático máximo dos PAs do modelo de produção em dt decrescente (0.1, 0.05,
0.025, 0.0125, 0.00625 ms …) nos degraus limpos, pelo driver separado; convergido quando dois níveis sucessivos diferem
≤ 2%. Entra na faixa medida da célula → defeito NUMÉRICO (integrador de 1ª ordem, já registrado para o L2); não entra →
defeito de ESTRUTURA (acoplamento AIS–soma, densidade de Na, invasão somática) → requisito da estrutura nova (D123).
**(3) (ii) nas REFERÊNCIAS convergidas (Hay, Allen PV e piramidal; CVode):** (a) os PAs (degraus do D128/P6) cumprem o
limiar ancorado na célula? (dV/dt no traço do CVode interpolado a 5 µs); (b) controle negativo e varredura de fronteira
no PASSIVO de cada referência — pulsos retangulares 0.5–1 000 ms e PSC α (τd 1/3/5/10) no soma, amplitude em nA numa
grade log de 0.01 a 50 nA; fronteira = menor amplitude detectada por C1 (e pela definição sem C1, para comparação);
comparada com as correntes dos próprios protocolos (EPSC 10 pA, EPSP 0.5 nA, CaBurst 1.5 nA, pulso de bAP 1.9 nA) — a
faixa FISIOLÓGICA de EPSC unitário somático fica a conferir em fonte primária (regra do P24), não citada aqui.
**(4) (i) EMISSÃO — reformular pela SAÍDA.** **Limitação registrada:** a condição regenerativa tem o mesmo problema da
distribuição do Na — um PA abortado ENTRA na região regenerativa e depois é interrompido; "entrou na região" não separa
abortado de completo. **HIPÓTESE (testar, não assumir):** quem torna o PA tudo-ou-nada é o AXÔNIO — eventos parciais no
AIS decaem passivamente; PAs completos se regeneram → medida num ponto DISTAL do axônio, a distribuição seria BIMODAL.
**Teste declarado:** nas referências que têm axônio com Na (Allen PV e piramidal — axônio "truncated" de 60 µm: 2 × 30
µm; o Hay biophys3 tem axônio PASSIVO — não serve; o biophys4, "iniciação no axônio", é candidato extra), sob par de
pulsos, bloqueio e bombardeio de PSCs α no soma: amplitude de cada evento (pico − linha de base local) no AIS (axon[0]
0.5) e no ponto distal (axon[1] 1.0). **Bimodal** se houver intervalo de ≥ 20 mV com < 1% dos eventos e ≥ 5% de cada
lado; limiar = centro do intervalo. Ressalva declarada: um axônio de 60 µm pode ser curto demais para o decaimento
passivo separar os modos — se não for bimodal, reportar e considerar a condição regenerativa com critério de
COMPLETUDE (atingir o pico de repolarização), declarada antes.
**(5) Modelo de produção — está sendo SUBSTITUÍDO (D123); não se investe em remendar o detector dele.** Registrado: o
detector de produção atual é CONHECIDAMENTE DEFEITUOSO no regime de bombardeio (e o risco medido no item 46 não é o erro
verdadeiro — a referência também errava); (i) e (ii), quando validados nas referências, são REQUISITOS da estrutura
nova; **a suíte passa porque os testes exercitam o REGIME FÁCIL — dívida conhecida; reabrir quando a estrutura nova
entrar.**

**50. RESULTADOS (2026-09-30 15:39) — LIMIAR NA RESOLUÇÃO NATIVA, TAXA MÍNIMA, E O dV/dt DO MODELO DE PRODUÇÃO CONVERGIDO.**
**(1) Lacuna de dV/dt na célula 471129934, do NWB original** (`neuron/allen_native_gap.py`; mesmas varreduras e janelas
dos CSVs; FIR polifásico do `extract_allen` para as taxas reduzidas):
| taxa | PAs: dV/dt máx (mV/ms) | sublimiares: máx | lacuna? | X (centro geom.) |
|---|---|---|---|---|
| **200 kHz (nativa, sem filtro)** | 225–525 (mediana 313) | 43.7 | **SIM** | **99.2** |
| 100 kHz | 216–521 | **701** | NÃO | — |
| 50 kHz | 211–509 | **429** | NÃO | — |
| 20 kHz | 210–477 | 180 | SIM | 194.6 |
| 10 kHz (a dos CSVs) | 197–431 | 91 | SIM | 134.2 |
| 5 kHz | 159–302 | 46 | SIM | 85.3 |
| **2 kHz** | 62–127 | 19 | **SIM** | 34.3 |
| 1 kHz | 26–52 (PAs perdidos: 52 de 58) | 57 | NÃO | — |
**A lacuna se mantém na resolução nativa (e fica MAIOR: 44 → 225), mas o LIMIAR NÃO: X depende da cadeia de aquisição
(34 a 195 mV/ms).** Não há um X válido em todas as taxas (as faixas não se sobrepõem). A 100 e 50 kHz a lacuna some por
ARTEFATO DE PROCESSAMENTO: a decimação com anti-alias oscila nos saltos de artefato do estímulo e cria "sublimiares"
de 400–700 mV/ms — não é fisiologia. **Consequência de desenho:** (ii) só é "o mesmo dos dois lados" se o traço do MODELO
passar pela MESMA cadeia de aquisição (taxa + filtro) que o elemento usa na célula; o critério é (limiar, cadeia), não
um número solto.
**REQUISITO DE HARDWARE (P24/P54):** detectar PAs da célula pela velocidade de subida exige amostragem **≥ ~2 kHz** com
anti-alias (a 1 kHz a lacuna some e PAs se perdem); a cadeia (taxa e filtro) tem de ser FIXADA e reproduzida no lado do
modelo; filtros com oscilação em transientes de estímulo invalidam o critério (visto a 50–100 kHz com FIR). Margem
confortável: 5–20 kHz.
**(2) dV/dt somático dos PAs do modelo de PRODUÇÃO em dt decrescente** (`neuron/hh_dvdt_conv.cpp`; degraus de 10/20/30
µA/cm²; PA = pico > 0 mV):
| dt (ms) | PAs (pico > 0) | dV/dt soma min / mediana / máx | dV/dt AIS mediana |
|---|---|---|---|
| 0.1 (produção) | **6** | 144 / 226 / 246 | 241 |
| 0.025 | 56 | 193 / 195 / 376 | 253 |
| 0.00625 | 56 | 200 / 201 / 392 (≤ 2% do anterior) | 268 |
| 0.0015625 | 56 | 201 / 202 / 393 | 269 |
**CONVERGIDO, o PA somático do modelo de produção sobe a 201–393 mV/ms — DENTRO da faixa medida da célula** (225–525
nativa; 197–431 a 10 kHz). **O defeito visto no item 48 era NUMÉRICO** (integrador de 1ª ordem a dt 0.1: achata a subida
e 50 dos 56 PAs nem passam de 0 mV), **não de estrutura** — já registrado para o L2 (itens 17, 23, 27). O pico dos PAs
convergidos é baixo (~+1 mV, a célula chega a +35) — nota de fidelidade, fora deste critério.

**51. DECISÃO DO USUÁRIO — TRÊS REGISTROS + UMA DECLARAÇÃO ANTES DO RESULTADO DO AXÔNIO (2026-09-30 21:28; a
declaração (4) é registrada ANTES de qualquer resultado da tarefa C — `pv_C`, `pyr_C`, `hay4_C` ainda não existem; nada
no código de produção; filas não interrompidas).**
**(1) O CRITÉRIO É A CADEIA DE MEDIDA.** "O mesmo detector nos dois lados" passa a ser **"a MESMA CADEIA DE MEDIDA nos
dois lados"**: o traço do modelo passa por uma EMULAÇÃO da aquisição do elemento — mesma taxa, mesmo filtro anti-alias,
mesmo LOCAL de medida — ANTES de qualquer detecção. O item 50 mostrou por quê: o mesmo detector com o mesmo limiar dá
respostas diferentes a 200 kHz e a 10 kHz (X 99.2 → 134.2 mV/ms), e um filtro que oscila no transiente do estímulo
inventa eventos. Vale para o DESMAME INTEIRO (toda comparação modelo × célula, não só (ii)). → P28 (requisito da
comparação), P54 (componente necessário da ferramenta do L2), P24 (artefato de estímulo no hardware).
**Artefato de estímulo no hardware:** o elemento ESTIMULA a própria célula que registra; o filtro anti-alias converte o
degrau de estímulo num transiente com a duração da resposta ao impulso do filtro (FIR de N coeficientes a f_s: ~N/f_s,
com oscilação de Gibbs). **Requisito:** bloqueio do registro (ou da detecção) nas janelas de estímulo, com duração
DERIVADA da resposta do filtro (não escolhida), como parte do protocolo do elemento — e a mesma janela aplicada ao traço
emulado do modelo (senão a cadeia não é a mesma).
**(2) O INTEGRADOR É CONDIÇÃO, NÃO REFINAMENTO.** A dt = 0.1 ms só 6 dos 56 disparos convergidos passam de 0 mV (item
50): o integrador de 1ª ordem da produção apaga a forma do PA a ponto de o critério da célula não reconhecê-lo. O
integrador de ordem maior/adaptativo do L2 é CONDIÇÃO para disparos reconhecíveis → D116 (adendo) e P54. O pico baixo dos
disparos CONVERGIDOS (~+1 mV contra ~+35 mV da célula) NÃO é numérico (persiste a dt 0.0016) — é defeito de FIDELIDADE do
modelo antigo → REQUISITO da estrutura nova (D123, adendo): o pico do PA somático entra como métrica de aceitação contra
a célula, na mesma cadeia de medida (1).
**(3) O TROPEÇO — lição de processo.** O que vive só na documentação se repete (a armadilha do `Vector.play` depois do
`SaveState.restore` foi registrada no D131 e reencontrada no `ref_ii`); o que vive em código compartilhado, com
autoteste, não. A injeção de estímulo com restauração de estado passa a uma função comum (`hay_common`), usada por todos
os scripts NOVOS (as rodadas em curso não são interrompidas), com o teste de um pulso contra passo fixo rodando
AUTOMATICAMENTE antes de qualquer rodada; rodada que não passa no autoteste não começa. Revisão das demais armadilhas
do D132 e a lista do que vira autoteste: item 52.
**(4) DECLARAÇÃO ANTES DO RESULTADO DO AXÔNIO.** Eventos parciais decaem ao longo do axônio na escala do comprimento
elétrico dele. **λ calculado do PASSIVO de cada modelo** (λ = √(R_m·d / 4R_i); parâmetros lidos dos modelos construídos;
ponto do AIS = axon[0](0.5), distal = axon[1](1.0), distância 45 µm; atenuação de tensão AIS → distal pelo `Impedance`
do NEURON no modelo passivo, que inclui a extremidade selada; `neuron/results/ref_ii/axon_lambda.jsonl`):
| modelo | axônio | diâm. | g_pas (S/cm²) | R_i (Ω·cm) | c_m (µF/cm²) | τ_m | **λ_DC** | λ a 1 kHz | **distância/λ_DC** | atenuação AIS→distal DC / 1 kHz |
|---|---|---|---|---|---|---|---|---|---|---|
| Allen PV 471077857 | 2×30 µm | 0.42 µm | 0.00682 | 76 | 9.98 | 1.46 ms | **45 µm** | 20 µm | **1.00** | 0.68 / 0.22 |
| Allen piramidal 471129934 | 2×30 µm | 0.39 µm | 0.0097 | 61 | 3.52 | 0.36 ms | **40 µm** | 31 µm | **1.11** | 0.65 / 0.50 |
| Hay biophys4 | 2×30 µm | 1.0 µm | 3×10⁻⁵ | 100 | 1.0 | 33 ms | **913 µm** | 89 µm | **0.05** | 0.999 / 0.98 |
**Regra declarada AGORA (antes do resultado):** "muito menor que λ" = distância/λ_DC < 0.2; "comparável ou maior" =
distância/λ_DC ≥ 0.5; entre os dois = tratado como "muito menor" (conservador). Num modelo "muito menor", um resultado NÃO
BIMODAL é **INCONCLUSIVO (limite de geometria), NÃO NEGATIVO** — o ponto distal está eletricamente no AIS e não há
comprimento para o parcial decair. Num modelo "comparável", um resultado não bimodal REFUTA a hipótese naquele modelo.
Um resultado bimodal é positivo em qualquer geometria. A atenuação DC/1 kHz é a verificação cruzada: se a classe por λ e
a atenuação discordarem (atenuação 1 kHz > 0.9 num modelo "comparável", ou < 0.5 num "muito menor"), o modelo vira
inconclusivo. **Classificação resultante, fixada antes do resultado:** Hay biophys4 → **"muito menor"** (0.05; atenuação
0.98–0.999) → não bimodal = INCONCLUSIVO. Allen PV e piramidal → **"comparável"** (1.00 e 1.11; atenuação 0.65–0.68 DC,
0.22–0.50 a 1 kHz) → não bimodal = REFUTA nesses modelos. Se nenhum modelo puder refutar (nenhum "comparável"), o teste é
registrado como inconclusivo e a hipótese como ABERTA — sem trocar de critério.
**Ressalva DECLARADA AGORA (não a posteriori):** o λ curto dos axônios do Allen (~40 µm, 20–50× menor que o do Hay) vem
de g_pas ≈ 0.007–0.010 S/cm² e c_m ≈ 3.5–10 µF/cm² do AJUSTE — parâmetros que NENHUM dado axonal restringe (o axônio do
Allen é um toco de 60 µm usado como dreno no ajuste somático; c_m de 10 µF/cm² não é membrana fisiológica). Logo uma
refutação no Allen refuta a hipótese **nessas referências** (que é o que o critério (i) precisa para escolher a régua
delas), não num axônio real; a pergunta biológica ("um axônio com λ real de centenas de µm separa parcial de PA?") fica
ABERTA enquanto não houver um modelo com axônio longo E passivo axonal restringido por dado. Verificação suplementar em
curso (antes do resultado): atenuação com o modelo ATIVO linearizado no repouso (condutâncias de repouso encurtam o λ
efetivo) — se mudar a classe de algum modelo, a classe vira inconclusivo.
**Suplemento (2026-09-30 21:38; ainda sem nenhum resultado da tarefa C):** atenuação AIS → distal com o modelo ATIVO
linearizado no repouso (`Impedance` estendido, após 2 s de CVode; `results/ref_ii/axon_atten_active_rest.jsonl`):
PV DC 0.81 / 1 kHz 0.21; piramidal DC **0.985** / 1 kHz 0.65; Hay4 DC 0.995 / 1 kHz 0.975. **Nenhuma classe muda** pela
regra declarada (comparáveis com atenuação a 1 kHz < 0.9; Hay4 > 0.5). Nota: no piramidal ativo o DC fica quase
isopotencial (0.985, contra 0.65 no passivo — o repouso ativo tem gradiente de −85.9 no AIS a −93.7 mV no ponto distal);
a separação que interessa a eventos de ~1 ms é a de 1 kHz (0.65), que mantém a classe.

**52. O TROPEÇO VIRA CÓDIGO: INJEÇÃO COMUM COM AUTOTESTE + REVISÃO DAS ARMADILHAS (2026-09-30 21:44; critérios do
autoteste declarados ANTES de rodá-lo nos modelos reais; filas em curso NÃO tocadas — os processos já carregaram o
código antigo; só rodadas NOVAS usam o comum).**
**Função comum:** `neuron/stim_common.py` (NEURON, qualquer modelo — Hay e Allen): `Injector(seg)` assenta o repouso em
CVode, salva o estado e, NO CONSTRUTOR, roda o **autoteste de um pulso contra passo fixo** no próprio modelo e ponto;
`run()` recusa rodar sem autoteste aprovado (`AutotestFailed`). **Critérios (declarados agora):** pulso retangular
sublimiar (padrão 0.2 nA, 1 ms, em t = 10 ms) pelo caminho do play (CVode) × o mesmo pulso por `IClamp` clássico em
passo FIXO 0.0025 ms (Euler implícito), do MESMO repouso: (a) V inicial = repouso salvo (≤ 10⁻³ mV) nos dois; (b) V
parado antes do pulso (≤ 0.01 mV); (c) deflexão do passo fixo entre 0.1 e 15 mV (senão o pulso de teste está mal
dimensionado e o autoteste falha dizendo isso); (d) deflexões concordam ≤ 2% e picos ≤ 0.1 ms; (e) t final = tstop
(≤ 10⁻⁶ ms) no repouso e em TODA rodada. **O autoteste tem de PODER FALHAR:** `neuron/stim_common_check.py` reintroduz
cada armadilha (mutação) e exige a recusa.
**Armadilhas — achados ao escrever o código (num compartimento passivo):**
- **T1 (D131, reencontrada no `ref_ii`): `SaveState.restore()` LIMPA a fila de eventos**, inclusive os que o
  `Vector.play` montou no `finitialize` → o estímulo some (0.000 mV × 15.656 do IClamp). **`restore(1)` mantém a fila
  e o play atua** (15.652 mV). A função comum usa `restore(1)`; a mutação com `restore()` é RECUSADA pelo autoteste.
- **T3 (NOVA): `h.cvode.active(1)` chamado do Python NÃO liga o `using_cvode_` do stdrun** → o `continuerun` não posta
  o evento de tstop: o CVode passa do fim (passivo puro: pedido 500 ms, parou em 4 400) ou para antes (−0.01 ms com
  play). Os scripts em curso (`active_cvode`, `hay_native`, `hay_common.Rest`, `ref_ii_axon`, `validate_detector`)
  usam essa chamada; **conferido: nenhum resultado depende disso** (janelas de análise terminam antes do tstop; o
  `Rest` usa TS = t real). A função comum usa `h.cvode_active(1)` e confere o t final; a mutação é RECUSADA.
- **T2 (registrada no `ref_ii`: "CVode passa por cima do pulso sem índices de descontinuidade") NÃO SE REPRODUZ:** no
  NEURON 9.0.2 o play contínuo sob CVode PARA em cada ponto do vetor de tempo, com ou sem índices (pulso de 0.1 a 1 ms
  em t = 10, 200 e 2 000 ms após repouso: deflexões idênticas nos três modos). **O diagnóstico anterior fica NÃO
  CONFIRMADO** (o conserto que funcionou no `ref_ii` foi o recomeço do zero, que contornava o T1); os índices ficam
  (inofensivos). A mutação passa porque não há defeito a pegar — não é autoteste vazio, é armadilha inexistente aqui; se
  aparecer noutra versão, o mesmo pulso a pega (perda de pulso muda a deflexão > 2%).
- **T6 (NOVA, custo): por parar em cada ponto, o play numa grade fina em TODO o intervalo (desenho do `ref_ii`, 5 µs)
  transforma o CVode em passo fixo de ~2.5 µs** (17 699 passos em 40 ms; o mesmo pulso só com pontos de quebra: 98
  passos). Resultado correto, custo ~2 ordens maior — causa PROVÁVEL (não medida no próprio pv_A) de o `pv_A` não ter gravado nenhum degrau em 6 h. A
  função comum usa só PONTOS DE QUEBRA (degrau = tempo duplicado com índice) e grade fina apenas onde há α ativo (até
  20·τd); os dois desenhos concordam a 0.02 mV num degrau + α (a diferença é a rampa de 5 µs do desenho antigo nas
  bordas). **As rodadas do `ref_ii` em curso NÃO são interrompidas** (corretas, só lentas) — decisão de relançar com a
  função comum fica com o usuário.
**Revisão das armadilhas do D131/D132 — o que VIRA autoteste (código comum, roda sozinho, bloqueia):**
| armadilha | autoteste | onde |
|---|---|---|
| T1 play depois do restore | pulso × passo fixo, no construtor | `stim_common.Injector` |
| T3 cvode ligado pelo Python | t final conferido no repouso e em toda rodada | `stim_common.Injector` |
| leitura dos nós de junção (V_J = P·V_C + I_J/G_JJ, item 19) | todo par (leitura, injeção) dos pontos usados: reduzido (Kron + `point_C` + correção) = DC EXATO do sistema com junções (erro relativo ≤ 10⁻⁸); mede também o erro SEM a correção | `tree2_lib.selftest_readout`, chamado por `hay_native`/`hay_reduce` (rodadas novas) com a correção na função comum `inj_read_correction` |
| detector contra estímulo sozinho (item 40c) | **portão**: o detector só roda em (modelo, protocolo) com controle negativo registrado PARA O HASH do código (`results/detector/VALIDADO.json`); detector alterado ou protocolo novo → recusa até o controle negativo rodar | `stim_common.require_validated_detector` |
| convergência da referência (itens 10, 24) | sentinela: um protocolo do modelo em atol e atol/10 — mesma contagem e picos ≤ 0.05 ms | `Injector.convergence_check` |
**O que NÃO vira autoteste (e por quê):** (1) o controle negativo EM SI e a varredura de fronteira — são simulações
caras por modelo/estímulo; viram PORTÃO (acima), não teste automático; (2) a sentinela de convergência cobre UM
protocolo — não prova convergência dos demais (cada referência nova roda a sua; o `Injector` não sabe escolher o
protocolo sentinela, então não a impõe); (3) a MESMA CADEIA DE MEDIDA (item 51(1)) — a emulação ainda não existe;
vira autoteste quando existir (resposta ao impulso do filtro conferida contra a declarada; janela de bloqueio derivada
dela); (4) juízo e processo: métrica de premissa vazia, número de literatura sem fonte primária, critério depois do
resultado, banda alargada — não são código; (5) operacionais: `pkill` que mata a própria sessão, sessão gráfica
(rodar sem tela), amplitudes erradas no lançador — moldes de lançador e log da tabela de protocolos, não autoteste;
(6) o detector de PRODUÇÃO (C++) — fora do harness (dívida do item 49).
**RESULTADO DOS AUTOTESTES (2026-09-30 21:58; `neuron/results/autotest/`):**
| modelo | versão correta (pulso 0.2 nA 1 ms; toy 0.05) | play × passo fixo | mutação T1 `restore()` | mutação T3 `cvode.active` |
|---|---|---|---|---|
| toy (1 compartimento) | PASSA | 3.7852 × 3.7859 mV | RECUSADA (0.000 mV) | RECUSADA (parou em 40.85) |
| Allen PV 471077857 | PASSA (16 s) | 4.5895 × 4.5870 mV, picos 11.000/11.000 | RECUSADA (0.000 mV) | RECUSADA (41.00) |
| Allen piramidal 471129934 | PASSA (38 s) | 1.7130 × 1.7123 mV | RECUSADA | RECUSADA (40.11) |
| Hay biophys3 | PASSA (392 s) | 1.4002 × 1.3998 mV | RECUSADA | RECUSADA (40.70) |
Repouso restaurado exato (V inicial = salvo) e sem deriva antes do pulso (≤ 3×10⁻⁶ mV) nos quatro. **Leitura dos nós de
junção (Hay, RED N = 4, todos os pares de pontos): erro relativo 1.4×10⁻¹³ com a correção; SEM ela 2.0×10⁻¹ — o
autoteste distingue.** Toy: os dois desenhos de forma de onda (só pontos de quebra × grade fina) concordam a 0.02 mV num
degrau + α, com metade dos passos (a diferença de custo cresce com a duração: a grade fina para a cada 5 µs o tempo todo).
**`ref_ii_axon.py` passa a usar a função comum (2026-09-30 22:15)** — vale para as rodadas da fila que AINDA NÃO
COMEÇARAM (cada uma é um processo novo: pv B/C, pyr A/B/C, hay3 A, hay4 C); `pv_A` e `hay3_B` seguem com o código que já
carregaram (desenho antigo, equivalente, lento) — fila não interrompida. O traço é gravado numa grade FIXA de 5 µs pela
interpolação do próprio CVode (não acrescenta passos; toy: dV/dt máx 290.12 × 290.13 mV/ms do desenho antigo; a
diferença de V de até 0.65 mV é deslocamento de ~2 µs dos PAs pela rampa de 5 µs do desenho antigo na borda do degrau).
Fumaça no PV (tarefa nova `T`: autoteste + degrau de 0.6 nA × 200 ms): 26 PA, dV/dt nativo 468–511 mV/ms, 591 s no total
(o `pv_A` antigo não gravou nenhum degrau de 1 s em 6 h). **Tarefa C ganhou o CONTROLE NEGATIVO do detector nos
estímulos que ela usa** (o detector só entra na busca dos limiares Ap/Aa e no pico do pulso 1): ao fim, a mesma célula
vira passiva (todos os mecanismos menos `pas`), novo repouso + autoteste, e o detector roda no estímulo SOZINHO (pulso
1 ms × Ap e × 1.5 Ap; α τd 3 × Aa e × 2 Aa); alguma detecção → `limiares_suspeitos` no resultado (a bimodalidade não
usa o detector). Motivo: o B do hay3 NÃO cobre o hay4 (passivo difere: g_pas soma 3.38×10⁻⁵ × 3×10⁻⁵, dendritos
5.89/4.67×10⁻⁵ × 6×10⁻⁵). Teste do caminho: no PV passivo um pulso de 3 nA × 1 ms JÁ é detectado (V máx −5.5 mV) — no
Hay4 passivo não (−68.9 mV). O caminho tinha um erro (o `uninsert` recusa os mecanismos internos `capacitance`/
`morphology`) — achado no teste antes de qualquer rodada usá-lo, corrigido.

**53. DECISÃO DO USUÁRIO — PARAR `pv_A` E `hay3_B` E RELANÇAR TUDO PELA FUNÇÃO COMUM, COM REGRESSÃO (2026-10-01 07:49; tolerância
declarada ANTES de rodar).** **Motivo:** (1) UM CAMINHO DE CÓDIGO SÓ — misturar números do código antigo com os da
função comum recria o problema dos dois detectores (o que foi autotestado não seria o que produziu parte dos números);
(2) a função comum é ~10× mais rápida e passa pelos autotestes automaticamente. **Regressão:** o que o `hay3_B` antigo já
gravou tem de ser REPRODUZIDO pela função comum antes de qualquer outra rodada: degrau de **0.5 ms → 15.8 nA** (exigido
pelo usuário) e degrau de **1 ms → 10 nA** (a 2ª fronteira, gravada antes da parada — mesma sobreposição, sem custo) nas
TRÊS variantes (definição sem C1; C1 nativo; C1 10 kHz). **Tolerância declarada:** a busca de fronteira anda numa grade
log de amplitudes com passo ×10^0.2 (≈ 1.585: … 6.31, 10.0, 15.85, 25.1 nA …) e devolve o 1º ponto com detecção — a
precisão da busca é UM PONTO DA GRADE; reproduzir = **o MESMO ponto da grade** em cada variante; ponto vizinho em
qualquer variante = NÃO reproduz → PARAR tudo e reportar a diferença antes de confiar no resto (o lançador só segue se a
regressão passar). Margem (pico e dV/dt máx no ponto da fronteira e no anterior) registrada só como diagnóstico, fora
do critério. O `pv_A` não gravou nada: relançado sem regressão.
**Execução:** lançadores antigos e os dois processos parados (logs guardados como `*_antigo.log`); `ref_ii_axon.py`
ganhou a tarefa `R` (o MESMO laço do B, restrito às duas formas; sai com código 1 se divergir); novo
`results/ref_ii/run.sh` roda `R` primeiro e só lança as duas cadeias se ela passar. **RESULTADO DA REGRESSÃO (2026-10-01
08:11): REPRODUZ** — degrau 0.5 ms → 15.8 nA e degrau 1 ms → 10 nA, o MESMO ponto da grade nas três variantes (autoteste
do estímulo no Hay: 1.4099 × 1.4095 mV). Margem (diagnóstico): o critério que decide é o pico > −30 mV, e o V máx fica a
−41.5 → −13.2 mV (0.5 ms; 10 → 15.8 nA) e −45.5 → −19.5 mV (1 ms; 6.3 → 10 nA) — a fronteira não está à beira do
corte, 11–16 mV de cada lado. Os dois caminhos concordam onde se sobrepõem; cadeias lançadas pela função comum (pv
A→B→C, pyr A→B→C ‖ hay3 B→A, hay4 C).

**54. DECISÃO DO USUÁRIO — RODAR AS ANÁLISES PRONTAS, COM DUAS VERIFICAÇÕES ANTES DO VEREDITO DO V2 (2026-10-01 16:43;
tolerância e achados declarados ANTES de rodar a regressão e antes de qualquer veredito).**
**(1) REGRESSÃO DO V2 CONTRA A FUNÇÃO COMUM.** As rodadas do V2 (P5cv/P6cv/P7cv, `hay_native.py`) injetam por `IClamp`
depois de `SaveState.restore()` (repouso de 3 s a passo fixo 0.1 ms) — caminho anterior à função comum. Ponto
reproduzido: **nativo N = 8**, mesmo modelo e mesmos pontos do `hay_native` (protocolo novo `REG`), injeção pelo
`stim_common.Injector` (repouso próprio de 3 s em CVode, autoteste automático): **degrau de 1.2 nA** (P6, 1 s) e **bAP**
(P5: 1.9 nA × 5 ms no soma), CVode atol 10⁻⁶, MESMO código de medida do P5cv/P6cv. **Tolerância (declarada agora):**
contagem de PA IGUAL (nos dois detectores, o antigo e o novo); tempos de PICO do detector novo |Δ| ≤ 0.05 ms (2 amostras
da grade de 0.025 ms do detector; = tolerância do item 52); amplitudes do bAP (soma e todos os pontos) |Δ|/valor ≤
0.05% (precisão do CVode registrada no item 10: atol 10⁻⁵ → 10⁻⁶ ≤ 0.05%; 10⁻⁶ → 10⁻⁷ < 0.01 mV). Bate → o V2 vale
como está; não bate → PARAR e reportar antes de qualquer veredito.
**(2) CONFERÊNCIA DO `hay_v2_final.py` (feita agora, ANTES de rodá-lo):**
- **P3 do LIMIT corrigido offline / P4-local do LIMIT refeito:** NÃO estão no script do V2 — o V2 não usa o LIMIT (usa
  RED N × L0 Δ0.5); o LIMIT é o V1 (`hay_reduce_compare.py`). E o item 36 já registrou que o LIMIT foi RELANÇADO
  (2026-09-30 09:18) com o `hay_reduce.py` JÁ corrigido (item 19, 2026-09-29) → a correção offline e o refazer ficaram
  DISPENSADOS. Conferência numérica no V1: P3/P4-local do LIMIT × L0S1 têm de sair no nível de máquina (leitura exata).
  Os RED N do V2 rodaram depois da correção (item 19: "corrigido ANTES deles").
- **Nível B do BAC sobre o 2º PA (item 39):** APLICADO (`IDX = {'BAC': 1, 'CaBurst': 0, 'EPSP': 0}`; a premissa também
  usa o 2º PA do BAC e o 1º do CaBurst).
- **CVode em P5/P6/P7:** APLICADO (P5cv, P6cv, P7cv; L0 Δ0.5 e nativos, atol 10⁻⁶).
- **Detector NOVO com marca no pico:** **NÃO APLICADO.** O script lê `P6cv` e `P7cv`, que guardam o detector ANTIGO
  (`active_l1_detect.spikes`, marca no limiar). O item 43 declarou o pico para as comparações de MÉTODO ("nível A/B do
  V2; critérios do D123 entre modelos"). Dados com pico existentes: P6 0.2–2.0 nA nos nativos (`P6cv_pk`) e 0.8–2.0 nA no
  L0 (`P6hi`); FALTAM o L0 a 0.2/0.4/0.6 nA e TODO o P7 (CVode e passo fixo — este último entra na premissa).
**Providência (dados ADITIVOS, critérios inalterados, mesmo caminho de código que produziu o V2 — validado pela
regressão (1)):** P7/P7cv passam a gravar também os PICOS do detector novo (como o `P6cv_pk`); rodadas novas: P7cv no L0
Δ0.5 e nativos N = 1…32; P7 a passo fixo no L0 Δ0.5 e RED N = 1…32 (premissa); P6cv do L0 a 0.2/0.4/0.6 nA. Depois, o
`hay_v2_final.py` usa os picos (P6 de `P6cv_pk`; P7 de `P7cv_pk`/`P7_pk`) — mesmos critérios, mesmas bandas. Se a
regressão (1) falhar, nada disso entra em veredito.
**RESULTADO DA REGRESSÃO (2026-10-01; `results/v2pk/REG_NATIVE_8.json` × `results/hay_native/P56cv_NATIVE_8.json`):
BATE.** bAP: 1 × 1 PA; amplitudes no soma e em todos os pontos dentro de **0.0081%** (pior: ponta apical; hay_620 34.878
× 34.877 mV; hay_800 25.061 × 25.059; soma 117.317 × 117.317) — tolerância 0.05%. Degrau de 1.2 nA: 18 × 18 PA nos dois
detectores; picos |Δ| máx **0.025 ms** (UMA amostra da grade do detector; média 0.003), 0 ambíguos nos dois — tolerância
0.05 ms. Autoteste da função comum no Hay N = 8: 1.4019 × 1.4014 mV. **O V2 vale como está** (o caminho IClamp +
`restore()` do `hay_native` entrega o estímulo; a armadilha do T1 era só do `Vector.play`).
**V1 — EXATIDÃO NO LIMITE (`hay_reduce_compare.py`, critérios do item 5 inalterados; LIMIT × L0S1, mesmo integrador):
PASSA.** P1–P5 pior **2.0×10⁻⁵** (P4-local na ponta basal; critério ≤ 10⁻³); P6 (0.6/1.2/2.0 nA) e P7 com contagens
iguais e máx |Δt| **0.000 ms** (≤ 0.05). A leitura exata está em vigor no LIMIT: com a leitura antiga, P3/P4-local
nos pontos de junção/ponta erravam até 31% (item 19) — aqui ficam em 2×10⁻⁵. (A seção V2 a passo fixo do mesmo script
para em `RED_N32` sem P5 — esperado: o V2 é o do `hay_v2_final.py`.) Convergência do L0 Δ1 → Δ0.5: P1–P5 2.7×10⁻³;
contagens P6/P7 iguais.
**MÉTRICAS DE TEMPO DA f-I (0.8–2.0 nA; detector NOVO, pico; CVode; nativo N × L0 Δ0.5; `hay_fi_time.py`,
`results/v2pk/fi_time.json`; bandas do V2 inalteradas — latência ±20% e adaptação ±25% nível A, taxa por ISI ≤ 0.4%
nível B; 1º ISI só registro):**
| N | contagens | latência | 1º ISI | adaptação | taxa por ISI | fora da banda |
|---|---|---|---|---|---|---|
| 32 | iguais | 0 | 3.0×10⁻³ | 3.6×10⁻³ | 7.7×10⁻⁴ | — |
| 16 | iguais | 0 | 3.0×10⁻³ | 3.3×10⁻³ | 4.9×10⁻⁴ | — |
| 8 | iguais | 8.8×10⁻³ | 5.0×10⁻³ | 5.5×10⁻³ | 7.0×10⁻⁴ | — |
| 4 | iguais | 8.8×10⁻³ | 5.0×10⁻³ | 8.6×10⁻³ | 1.25×10⁻² | taxa (B) |
| 2 | DIFERENTES | 2.6×10⁻² | 9.4×10⁻³ | 3.4×10⁻² | 1.1×10⁻¹ | contagem, taxa (B) |
| 1 | DIFERENTES | 9.7×10⁻² | 1.5×10⁻² | 7.4×10⁻² | 1.9×10⁻¹ | contagem, taxa (B) |
(erros relativos máximos sobre os 7 degraus). Referência L0: latência do 1º PICO 11.95 → 2.85 ms de 0.8 a 2.0 nA — o
detector antigo dava 0.0 a 1.6 e 2.0 nA (item 43). A latência é quantizada pela grade de 0.025 ms do detector: 8.8×10⁻³
= UMA amostra em 2.85 ms. **Pelas métricas de tempo, N ≥ 8 cumpre as bandas A e B em todos os degraus; N = 4 cumpre A e
falha só a taxa (B); N ≤ 2 falha contagem.**

**56. DECISÃO DO USUÁRIO — ANTES DE DIMENSIONAR A ETAPA A: TESTE BARATO DE NÓS NOS PONTOS DE MEDIDA (2026-10-02 09:45;
declarado ANTES de rodar o teste).**
**(1) Registros.** O nível A do V2 fecha em N = 8; o nível B falha em toda a grade até N = 32, decidido pelo P3. A
premissa (passo fixo × CVode) falha em N = 1, 2 e 8 — para eventos regenerativos no Hay, passo fixo não substitui CVode;
coerente com a avaliação anterior (item 40). **REGRA NOVA (mesma família do BAC vazio, item 37): AUSÊNCIA DE AVALIAÇÃO
NUNCA PODE SAIR COMO APROVAÇÃO** — zero avaliações → "NÃO AVALIADA", sempre, em todo veredito automático. Revisão dos
scripts de veredito do D132: item 57.
**(2) Diagnóstico do P3 (dados do V2, `results/v2pk/p3_diag.json`).** O P3 lê a razão ponto→soma e a Rin local no
PRÓPRIO ponto de injeção; os pontos não são nós da discretização (nós = centros dos compartimentos e extremos das
seções). Pior P3 por N e distância ao nó mais próximo:
| N | pior P3 | ponto | distância ao nó | fração do compartimento |
|---|---|---|---|---|
| 4 | 18.2% | apical_800 (razão →soma) | 23.86 µm | 0.41 |
| 8 | 9.3% | hay_800 (razão →soma) | 16.80 µm | 0.49 |
| 16 | 6.1% | apical_700 (razão →soma) | 4.00 µm | 0.27 |
| 32 | 2.1% | hay_800 (razão →soma) | 3.84 µm | 0.44 |
A ressalva (em N = 32 o ponto de 700 µm fica a 0.36 µm do nó) não pega o pior: em N = 32 o pior é o hay_800, quase no
MEIO do compartimento. **Separação independente:** os 4 pontos que JÁ são nós (pontas e ramificações, 8 medidas) têm
P3 4.6 → 1.25 → 0.32 → **0.08%** (N = 4 → 32; fator ~4 por dobra = 2ª ordem; passam de 1% desde N = 16); os 14 fora de
nó, pior 18 → 9.3 → 6.1 → 2.1% (mediana 4.1 → 2.6 → 1.2 → 0.29%). Compatível com o efeito fora de nó do D127 —
diagnóstico, não prova: o teste é que decide.
**(3) Teste declarado: NÓS NOS PONTOS DE MEDIDA.** Justificativa INDEPENDENTE deste resultado: é a decisão do D127
(pontos de medida em nós) e é escolha natural do desenho do implante — o HANU sabe onde estão seus elementos; o modelo
reduzido que ele ajusta pode ter um nó exatamente em cada ponto de penetração. **Registrado: a mudança é feita DEPOIS
de ver o resultado do V2, com esta justificativa; o resultado NÃO está garantido.** O QUE MUDA: só a DISCRETIZAÇÃO —
um nó a mais em cada ponto de medida, ALÉM dos N compartimentos por ramo: nó SEM membrana (tipo junção) no arco do
ponto, que divide a resistência axial do trecho em que cai; os N compartimentos (áreas, densidades amostradas) ficam
IDÊNTICOS; eliminado por Kron como as demais junções; leitura/injeção com peso 1 no nó (exata, com a correção de junção
generalizada para G_JJ não diagonal — o nó novo pode tocar uma junção — e coberta pelo autoteste da leitura). O QUE NÃO
MUDA: a faixa de 1% do nível B, o protocolo do P3 (o MESMO do V2: −50 pA × 1 s em cada ponto, modelo Hay completo com os
mecanismos amostrados, passo fixo 0.1 ms, estado estacionário — sem CVode), a referência (L0 Δ0.5, `L0_d05_P.json`) e
todos os outros critérios. Rodar N = 4, 8, 16, 32. **Declarado antes:** (a) PASSA se o pior P3 (razões e Rin, todos os
pontos) ≤ 1% em algum N E o erro cai com N (pior P3 monotonicamente decrescente em 4 → 8 → 16 → 32); (b) ordem observada
p = log2(e_N / e_2N) entre dobras sucessivas, reportada.
**(4) O que o resultado decide (declarado pelo usuário):** se PASSAR, o nível B fica no menor N em que TODOS os
critérios passam (pelos números atuais o 1º PA do CaBurst falha em N = 16 — 0.45 ms — e passa em N = 32 — 0.15 ms —,
provavelmente N = 32), registra-se a REGRA DE DESENHO "o modelo reduzido do HANU tem nós nos pontos de penetração dos
elementos" e a Etapa A é dimensionada por esse N (~52 dias-CPU em N = 32, no máximo dois processos pesados). Se NÃO
passar: reportar os custos de estender a grade (N = 64, 128) e de usar o Hay nativo convergido como modelo direto, antes
de decidir.

**57. REGRA "AUSÊNCIA DE AVALIAÇÃO ≠ APROVAÇÃO" APLICADA AOS SCRIPTS DE VEREDITO (2026-10-02).** Revisão de todos os
scripts de veredito do D132 em busca do padrão (nada comparado → passa). Encontrado e corrigido (tri-estado:
PASSA / falha / **NÃO AVALIADO**; um critério não avaliado nunca compõe uma aprovação; o menor N só conta níveis
efetivamente APROVADOS):
- `hay_v2_final.py` e `hay_reduce_compare.py`: adaptação "passava" quando a referência tinha < 3 PA; 1º PA do P7 =
  `or [0.0]` (nenhum par comparável → 0 ms → passa); taxa por ISI = `else 0.0`; contagem = `all()` sobre lista vazia;
  inclinação/latência sem dado davam `False` (falha onde deveria ser NÃO AVALIADO); V1: |Δt| = `else 0.0`; premissa:
  zero avaliações → "se sustenta" (já corrigido no item 55).
- `hay_native_compare.py`: |Δt| = `else 0.0`. `compare_active.py`: o critério de RUÍDO simplesmente SUMIA do veredito
  geral quando faltava o dado (GERAL podia dizer PASSA sem ele); critérios com NaN davam FALHA → agora NÃO AVALIADO.
  `l0_converged.py`: zero amplitudes em comum → "NÃO convergido: nada" (lia-se convergido). `validate_detector.py`:
  controle positivo com zero positivos → PASSA (explícito no código); negativo com zero protocolos → PASSA.
  `hay_variant.py`: "decremental" com < 2 pontos → verdadeiro. `hay_fi_time.py`: zero degraus → "todas as bandas ok".
**Verificação:** os vereditos JÁ reportados foram rodados de novo com os scripts corrigidos — V2 (A: N = 8; B: nenhum;
premissa falha), V1 (passa), convergência do L0, métricas de tempo da f-I: **todos inalterados e todos com avaliação
efetiva** (nenhum vira NÃO AVALIADO; todos os critérios do D123 avaliados em todos os N). Nenhuma aprovação anterior era
vazia. O veredito do Allen PV (D128/D129, `compare_active.py`) será rodado com a versão corrigida.

**58. RESULTADO — NÓS NOS PONTOS DE MEDIDA (item 56; `results/redx/`, `neuron/redx_p3.py`; mesma referência, mesmo
protocolo do P3, mesma faixa de 1%): PASSA.** Implementação: `tree2_lib.build(extra=…)` põe um nó sem membrana no arco
de cada ponto (os N compartimentos ficam idênticos — 781/1 561/3 121/6 241, os mesmos do RED), modo `REDX` no
`hay_reduce.py`; a leitura de junção foi generalizada para G_JJ não diagonal e o AUTOTESTE da leitura passou nos 4 N
(erro 10⁻¹³–10⁻¹²; sem a correção 2–20%).
| N | P3 pior SEM nó no ponto (V2) | P3 pior COM nó em cada ponto | onde |
|---|---|---|---|
| 4 | 18.2% | 4.64% | Rin na ponta apical (já era nó) |
| 8 | 9.28% | 1.25% | idem |
| 16 | 6.11% | **0.323%** | idem |
| 32 | 2.12% | **0.177%** | razão apical_1200 → soma |
**Critério declarado: ≤ 1% em algum N — SIM, desde N = 16; pior P3 monotonicamente decrescente — SIM. Ordem
observada p = 1.90 (4→8), 1.95 (8→16), 0.87 (16→32)** (sem nó no ponto: 0.97, 0.60, 1.53). Com o nó no ponto o pior
passa a ser o Rin da PONTA apical — que já era nó — com os MESMOS valores de antes (4.64 / 1.25 / 0.32%): o efeito
fora de nó SUMIU e sobra o erro de 2ª ordem da discretização. **Ressalva sobre o último p:** em N = 32 o erro (0.18%)
já está ABAIXO da diferença Δ1 → Δ0.5 do próprio L0 de referência (P1–P5 2.7×10⁻³, item 54) — o passo 16 → 32 mede o
limite da referência, não a ordem do método.
**Consequência, pela regra declarada pelo usuário no item 56(4):** nível B = menor N em que TODOS os critérios passam.
Com o P3 de nós alinhados, os demais critérios do nível B (números do V2): em N = 16, EPSP somático 0.05%, P2 0.06%,
P5 0.43%, taxa 0.05% — dentro; **1º PA do P7 0.45 ms — FORA** (≤ 0.2). Em N = 32, P3 0.18%, P2 0.013%, P5 0.54%, EPSP
somático 0.005%, 1º PA 0.15 ms, taxa 0.08%, contagens iguais — TODOS dentro. **→ NÍVEL B: N = 32.**
**REGRA DE DESENHO (registrada): o modelo reduzido do HANU tem NÓS NOS PONTOS DE PENETRAÇÃO DOS ELEMENTOS** (além dos N
compartimentos por ramo). Custo do nó extra: desprezível (um nó sem membrana por ponto, eliminado por Kron; no NEURON
nativo, o extremo de seção que a divisão no ponto cria). **Etapa A dimensionada por N = 32: ~52 dias-CPU** (item 20/23:
~26 dias-CPU a N = 16, ×2), com no máximo dois processos pesados (item 55).
**RESSALVA (registrada, não muda a regra declarada):** o "N = 32" combina o P3 da discretização COM nós (REDX) com P2,
P4, P5 e P7 medidos na discretização SEM o nó extra (V2). P2/P4/P5 já estão ≤ 0.54% sem o nó; o P7 (EPSP injetado no
hay_620, que também é ponto fora de nó; 1º PA 0.45 ms em N = 16) é o critério que decide entre 16 e 32 e NÃO foi medido
com o nó alinhado — o nó pode melhorá-lo (e baixar o nível B para N = 16) ou não. Verificar exige o P5/P7 em CVode no
NEURON nativo com as seções divididas nos pontos (o reduzido com LinearMechanism não roda CVode, item 5) — custo da
ordem do P7cv nativo (minutos a ~1 h por N). Decisão do usuário.

**59. DECISÃO DO USUÁRIO — VERIFICAR O NÍVEL B NA CONFIGURAÇÃO REAL (NÓS ALINHADOS) ANTES DA ETAPA A (2026-10-05 11:04;
declarado ANTES de rodar).** **Razão:** a Etapa A vai usar nós nos pontos de medida (regra de desenho do item 58); o
N = 32 do item 58 é veredito MISTO (P3 com nó; P5/P7 sem nó) — iniciar a Etapa A nele seria dimensioná-la por uma
discretização que ela não vai usar. Custo-benefício: horas de verificação contra a chance de cortar a Etapa A pela metade
(~26 dias-CPU).
**Registros:** (a) P3 com nó alinhado converge em SEGUNDA ORDEM (p ≈ 1.9); o último passo (0.87) é limitado pela
PRECISÃO DA REFERÊNCIA (erro em N = 32, 0.18%, abaixo da convergência do próprio L0 entre Δ1 e Δ0.5, 0.27%) — **a
referência passou a ser o limite.** (b) A ressalva sobre o ponto de 700 µm estava mal dirigida: o pior P3 em N = 32 era
o hay_800, no meio do compartimento. (c) Revisão dos vereditos (item 57): oito scripts podiam transformar "nada
comparado" em aprovação; corrigidos; nenhum veredito já reportado mudou.
**Configuração verificada (`NATIVEX` no `hay_native.py`):** o Hay NATIVO (NEURON, nseg por seção, CVode onde o V2 usa
CVode), N por ramo como no V2, e CADA seção que contém um ponto de medida no INTERIOR (pontos nos extremos — pontas e
ramificações — já são nós) é DIVIDIDA no arco do ponto: geometria 3D partida exatamente no arco (pontos 3D interpolados),
peças encadeadas, filhos religados no mesmo arco, cada peça com nseg = max(1, round(N·ℓ_peça/L_seção)); o ponto vira
EXTREMO de seção = nó SEM membrana do NEURON (o mesmo tipo de nó do REDX); injeção e leitura no próprio nó (peso 1).
Densidades e reversões AMOSTRADAS do Hay fino (Δ 0.5 µm) no centro de cada segmento, como no NATIVE. Diferença em relação
ao REDX (registrada): no nativo os segmentos vizinhos ao ponto são redistribuídos (não ficam idênticos) — é como o
NEURON representa um nó; o P3 é RECALCULADO nesta configuração. Pontos divididos: os do V2 incluindo **hay_620 (onde o
EPSP do P7 é injetado)** e hay_800.
**Protocolos — o veredito INTEIRO numa configuração só (barato no nativo):** P2, P3 (passo fixo 0.1 ms, estado
estacionário), P4 (passo fixo 0.025 ms, EPSP sublimiar) — como na fila do V2; P5cv, P6cv e P7cv (CVode atol 10⁻⁶;
tempos pelo detector de PICO). Referências INALTERADAS: L0 Δ0.5 (`L0_d05_P.json` para P2–P4; `P56cv_L0_0.5.json` para
P5; picos do L0 em `P6lo`+`P6hi`; `v2pk/P7cv_L0_0.5.json`). **Critérios e faixas INALTERADOS** (nível A e B do item 5,
pelo `hay_v2_final.py` com detector de pico e a regra do item 57). **N = 16 primeiro (decide), depois N = 32
(confirma).** Regra do menor N inalterada ("portão em N e em todos os mais finos" — na grade 16, 32): **N = 16 passa
TODOS os critérios do nível B E N = 32 também → a Etapa A dimensiona por N = 16. N = 16 falha e N = 32 passa → N = 32,
agora com veredito na configuração real. N = 32 falha → nenhum N ≤ 32 nesta configuração: reportar (custos de N = 64 e
do nativo convergido) antes de decidir.** Concorrência: `hay4_C` (prioridade 4; o `hay3_B` já tinha terminado)
SUSPENSO durante a verificação; `pv_C` segue (dois pesados).

**60. RESULTADO — VEREDITO DO ALLEN PV EM CVODE (item 41; detector de PICO; `compare_active.py` e `l0_converged.py`
corrigidos pelo item 57; 2026-10-05).** **Pré-condição** (nativo N = 8 × RED N = 8, Euler 0.025): contagens IGUAIS nas
14 amplitudes — passa. **Convergência do L0 Δ2 → Δ1 (CVode, critério do D128):** converge em 12 das 14 amplitudes e no
ruído (251 × 251); **NÃO converge em 410 pA** (adaptação 6.9% > 2%; contagens iguais, 25) **e em 600 pA** (121 × 120).
Pela regra declarada (item 41), nessas duas a referência seria o Δ0.5 — NÃO rodado (o Δ1 levou ~35 h de relógio sob
disputa). **D123, nativo N = 8 × L0 Δ1 (CVode nos dois lados):**
| critério | L0 Δ1 | N = 8 | |
|---|---|---|---|
| contagem por degrau (|Δ| ≤ máx(1, 15%)) | 400 pA: **9** | **11** | **FALHA** (demais 13 amplitudes ok) |
| reobase ±20 pA | 380 | 380 | passa |
| inclinação f-I ±25% | 0.5569 | 0.5616 Hz/pA (+0.8%) | passa |
| adaptação ±25% (600 pA) | 1.231 | 1.225 (−0.5%) | passa* |
| latência ±20% (420 pA) | 4.88 | 4.85 ms (−0.5%) | passa |
| ruído ±15% | 251 | 253 PA (+0.8%) | passa |
**GERAL: FALHA. O veredito do D129 (PASSA, Euler 0.025 nos dois lados, não convergido no tempo) MUDA para FALHA** —
por UM critério numa amplitude. A falha está numa amplitude CONVERGIDA (400 pA: 9 = 9 em Δ2 e Δ1) e é igual nos dois
detectores (pico e IPFX: 9 × 11) → não é do detector nem da referência. **Diagnóstico (não usado para aprovar):** a
400 pA a célula dispara em SALVAS de ~3 PA (picos do L0: 6, 21, 40 | 429, 448, 471 | 701, 722, 749 ms); o N = 8 adianta
a 2ª salva em 31 ms (397 × 429) e cabe uma 4ª salva parcial antes do fim do degrau → +2 PA de uma vez. A contagem por
degrau é QUANTIZADA pelas salvas nesse regime (um corte fixo sobre uma grandeza discreta — família do D130 item 4);
se a métrica está mal posta para regime de salvas é decisão do usuário — a banda NÃO foi alargada. *A adaptação é medida
a 600 pA, amplitude em que o L0 NÃO convergiu (121 × 120): esse "passa" se apoia numa referência não convergida.

**62. RESULTADO PARCIAL — NÍVEL B NA CONFIGURAÇÃO COM NÓS ALINHADOS (item 59; `results/nativex/`; 2026-10-05 16:10).**
Construção conferida: geometria partida EXATA (área total 31 192.170 µm² = fino, dif 9×10⁻¹⁴; comprimento idêntico),
todos os pontos caem em nó (extremo de seção, peso 1; hay_620 incluído); repouso a 0.0013 mV do L0; 3 122 (N = 16) e
6 242 (N = 32) segmentos (+1 pelo arredondamento das peças). O P3 nativo com nós em N = 16 dá **0.327%** (Rin
apical_1200) — reproduz o REDX (0.323%): o nó nativo (extremo de seção) e o nó sem membrana do reduzido concordam.
| N | P3 pior | P2 pior | P5 bAP hay_620 / hay_800 | P7 BAC 2º PA Δ | P7 CaBurst 1º PA Δ | nível B |
|---|---|---|---|---|---|---|
| 16 | 0.327% | 0.058% | 35.136 / 25.431 mV (0.13% / 0.28%) | −0.025 ms | **−0.425 ms (> 0.2)** | **FALHA** |
| 32 | (P2–P4, P6 rodando) | | 35.210 / 25.498 mV (0.34% / 0.54%) | 0.000 ms | **+0.150 ms** | P5/P7 dentro |
(referência L0 Δ0.5 CVode, pico: BAC 2º PA 113.35 ms; CaBurst 1º PA 128.45 ms; bAP 35.09 / 25.36 mV.) **O nó no
hay_620 quase não mexe no CaBurst** (sem nó, N = 16: −0.45 ms; com nó: −0.425): o erro do P7 em N = 16 não é efeito
fora de nó — é da discretização dos compartimentos (o Ca-spike dendrítico). **→ N = 16 NÃO passa o nível B nesta
configuração; pela regra declarada (item 59), a Etapa A fica em N = 32**, condicionado a N = 32 passar TODOS os
critérios na configuração real (P2, P3, P4, P6 de N = 32 em curso; o P3 do REDX em N = 32 deu 0.18%). Concorrência: o
P5/P7 de N = 32 rodou à parte (771 s) com o `pv_C` suspenso; `pv_C` retomado; inibidor de suspensão atrelado à fila
da verificação.

**63. DECISÃO DO USUÁRIO — TRÊS ITENS; ETAPA A AINDA NÃO INICIADA (2026-10-05 17:31; declarações ANTES de rodar).**
**(1) Registros.** (a) **Correção do diagnóstico de lentidão:** era SUSPENSÃO da máquina, não swap (item 61). A
comparação "259 s sem disputa × 15 856 s com disputa" (item 55), apresentada como prova de troca, estava provavelmente
contaminada pelos períodos de sono. A regra de dois processos pesados fica por PRUDÊNCIA (navegador com ~3.5–4 GB), SEM
a evidência que lhe foi atribuída. (b) **O N da Etapa A é 32, CONDICIONADO** a P2/P3/P4/P6 em N = 32 na configuração com
nós (em curso). O erro do CaBurst em N = 16 vem da discretização dos compartimentos via spike de Ca dendrítico, não do
ponto fora de nó (−0.45 → −0.425 ms com o nó).
**(2) Allen PV — CONVERGÊNCIA EM N ANTES DE QUESTIONAR A MÉTRICA.** A falha a 400 pA (L0 9 × N = 8 11) tem cara de
quantização por salva, MAS o 2º surto começa 31 ms antes no N = 8 — com salvas a cada ~300 ms, ~10% no ritmo: diferença
real de dinâmica. **Teste:** nativo do interneurônio em N = 16 e N = 32, 400 pA, CVode atol 10⁻⁶, detector de pico, mesma
referência (L0 Δ1, que convergiu a 400 pA: 9 = 9). **Declarado antes:** salva = grupo de picos separados por ISI > 50 ms
(no L0 os ISIs dentro da salva são ~15–23 ms e entre salvas ~230–390 ms); início da salva = 1º pico do grupo.
- Se a CONTAGEM convergir para 9 (N = 16 ou N = 32 dá 9) E o início da 2ª salva se APROXIMAR do L0 (|Δ| decrescente de
  N = 8 → 16 → 32) → **N = 8 não basta no regime de salvas; o veredito do D129 passa a ser o do menor N que passa** —
  confirmá-lo exige o protocolo INTEIRO do D123 (14 amplitudes + ruído) nesse N; reportado o custo antes de rodar.
- Se NÃO convergir → a pergunta passa a ser sobre a MÉTRICA.
A grandeza CONTÍNUA (intervalo entre salvas, início de cada salva) entra como DIAGNÓSTICO, não substitui o critério de
contagem do D123. Nenhuma faixa alargada.
**Reclassificação pela regra do item 56 (ausência de avaliação ≠ aprovação):** o L0 Δ1 NÃO convergiu a 410 e 600 pA
(item 60) — o que é medido contra ele nessas amplitudes NÃO é avaliação: **adaptação (medida a 600 pA) → NÃO AVALIADA**
(não "passa"); **contagem a 410 e a 600 pA → NÃO AVALIADAS**; **inclinação f-I** (ajuste sobre as contagens de TODAS as
amplitudes ≥ reobase, incluindo 410 e 600) → **NÃO AVALIADA** (a mesma inclinação só sobre as amplitudes convergidas
entra como diagnóstico). `compare_active.py` passa a ler `not_converged` da referência e aplicar isso. O L0 Δ0.5 a 410 e
600 pA (exigido pela regra do item 41) roda quando houver vaga — fora do caminho crítico.
**(3) PREPARAR A ETAPA A PARA EXECUÇÃO LONGA (vale em qualquer cenário):** inibidor de sono COM ESCOPO (atrelado ao
processo da Etapa A, expira com ele; a configuração global de energia NÃO é mudada); GRAVAÇÃO FREQUENTE a cada unidade
independente com RETOMADA do ponto em que parou (uma interrupção custa minutos, não dias) — testada matando e relançando
uma rodada curta antes da longa; LEVANTAMENTO DO PARALELISMO (unidades independentes e tempo de cada) — item 64.

**64. RESULTADOS (2026-10-05) — ALLEN PV EM N = 16/32 E PREPARAÇÃO DA ETAPA A.**
**(A) Allen PV a 400 pA (nativo, CVode atol 10⁻⁶, detector de pico; `results/etapaA_prep/`):**
| modelo | PA | salvas (PA por salva) | início das salvas (ms) | Δ início da 2ª salva × L0 Δ1 | intervalos entre salvas |
|---|---|---|---|---|---|
| L0 Δ2 | 9 | 3, 3, 3 | 6.25, 425.75, 698.5 | −2.9 ms | 419.5, 272.8 |
| **L0 Δ1 (referência)** | **9** | 3, 3, 3 | 6.25, 428.62, 701.35 | — | 422.4, 272.7 |
| N = 8 | 11 | 3, 3, 3, 2 | 6.2, 397.1, 668.7, 973.2 | **−31.5 ms** | 390.9, 271.6, 304.5 |
| N = 16 | **9** | 3, 3, 3 | 6.2, 424.7, 696.9 | **−3.9 ms** | 418.5, 272.2 |
| N = 32 | 10 | 3, 3, 2, 2 | 6.2, 433.8, 684.1, 838.2 | **+5.1 ms** | 427.5, 250.3, 154.1 |
**Pelo critério DECLARADO (item 63): contagem converge para 9 — SIM (N = 16); |Δ| do início da 2ª salva decrescente em
8 → 16 → 32 — NÃO (31.5 → 3.9 → 5.1 ms). → NÃO convergiu pelo critério declarado → pela regra declarada, a pergunta
passa a ser sobre a MÉTRICA.** Registro sem reinterpretação: (i) a 2ª salva do N = 8 (−31.5 ms) é diferença REAL de
dinâmica — ~10× a resolução da própria referência nessa grandeza (L0 Δ2 × Δ1: 2.9 ms); (ii) os desvios de N = 16 e
N = 32 (3.9 e 5.1 ms) são da MESMA ordem dessa resolução — a sub-condição de monotonicidade foi declarada sobre uma
grandeza que a referência só resolve a ~3 ms; (iii) o N = 32 muda a ESTRUTURA das salvas (3, 3, 2, 2 × 3, 3, 3; 3ª salva
17 ms antes) — 400 pA está perto de uma fronteira de regime (salvas de 3 ↔ 2), onde pequenas mudanças de discretização
mudam a composição; (iv) pela contagem do D123 a 400 pA, N = 16 (9) e N = 32 (10, |Δ| = 1 ≤ 1.35) passariam — o
veredito do D123 nesses N exige o protocolo inteiro (14 amplitudes + ruído), NÃO rodado. Decisão do usuário.
**(B) CUSTO MEDIDO NO MODELO DA ETAPA A (NATIVEX N = 32, nós nos pontos; um processo sozinho; CPU = relógio, sem sono;
`results/etapaA_prep/timing_NATIVEX32_semfino.json`):** M1 (um degrau de 1.15 s) 6.3 s em CVode (32.1 s a dt 0.1 fixo);
M4 0.2 / 0.5 / 1.5 nA 3.2 / 3.4 / 12.0 s; M3 11.1 s; M5 (2.3 s, 1 nA) 249 s. **≈ o mesmo que o item 20 mediu em N = 16**
(5.4; 3.5/3.8/14.7; 13.7; 264 s, com 7 processos) — o "×2 para N = 32" (52 dias) NÃO se confirma. **Defeito achado na
medida:** a 1ª medida deu ~10× mais (M1 50.7 s, M5 1 937 s) porque o NATIVEX mantinha VIVO o Hay fino (Δ0.5, 25 407
segmentos) usado só para amostrar — o NEURON o integrava junto (parado, desacoplado). Corrigido: apagado após a
amostragem (210 seções vivas = só o nativo). Os resultados já obtidos com ele vivo são válidos dentro da tolerância do
CVode (controle de erro sobre todos os estados; P2–P4 a passo fixo idênticos), mas, por UM CAMINHO DE CÓDIGO SÓ, o
veredito de N = 16 e N = 32 foi RELANÇADO sem o fino (o de antes fica em `nativex/comfino/` como verificação cruzada).
**(C) RETOMADA — TESTADA (`neuron/etapaA_runner.py`, `neuron/etapaA_resume_test.sh`):** unidade = ponto de injeção;
subpasso = avaliação θ, gravado por escrita atômica; retomada lê os subpassos prontos e pula as unidades prontas; o
processo se põe sob `systemd-inhibit` (escopo = ele mesmo; conferido: o inibidor existe enquanto roda e some no fim).
Teste com modelo NEURON pequeno (3 unidades × 9 subpassos): rodada MORTA com SIGKILL após 12 arquivos (nenhum
temporário órfão), relançada → 16 subpassos calculados, 2 lidos, 1 unidade pulada (27 = nenhum retrabalho) e resultado
**IDÊNTICO bit a bit** ao ininterrupto e ao de 2 workers (`--worker k/K`). **O modelo direto da Etapa A (30 parâmetros
por região do D131 7.1, formas do Hay, sobre o NATIVEX) AINDA NÃO EXISTE** — entra pela mesma interface; antes de
lançar: verificar que em θ_verdadeiro ele reproduz o NATIVEX (que amostra as densidades do Hay por segmento).
**(D) LEVANTAMENTO DO PARALELISMO (s = 25 µm, 503 pontos; custos de (B)).** Achado de desenho: a unidade NÃO pode ser a
avaliação θ — o M2 (todos os pontos durante cada M1) gera ~6×10⁹ amostras por avaliação, que não cabem em disco; a
unidade é o PONTO DE INJEÇÃO p, rodando TODAS as perturbações e gravando só os blocos reduzidos por ponto de leitura r
(JᵀJ 30×30, JᵀD, JᵀΔy da geometria: ~11 MB por p); espaçamentos = subconjuntos de blocos e ruído = analítico (nenhuma
simulação a mais). Em voo, uma unidade guarda suas colunas (~4–5 GB em float32) até reduzir — 172 GB livres.
| unidade | quantas | conteúdo | tempo de cada (1 núcleo) | total |
|---|---|---|---|---|
| ponto de injeção p | 503 | 125 avaliações (J 61 + ganho/posição ~2 + geometria 62) × (M1 ±50 pA 12.6 s + M4 ×3 18.6 s) | ~65 min (subpasso ~31 s) | ~545 h |
| global (soma) | 125 (uma por avaliação) | M3 + M5 ×3 | ~14 min | ~30 h |
| conjunto funcional F | 61 | EPSP nos 30 sítios + pontos do D127, BAC/CaBurst, f-I | ~0.45 h | ~27 h |
| viés de especificação (Hay L0 Δ0.5) | 503 + 1 | mesmos protocolos, 1 avaliação | ~1.7 min / ~45 min | ~17 h |
| **TOTAL** | **~1 190** | | | **≈ 620 h ≈ 26 dias-CPU** |
Execução: 2 processos locais (regra de prudência) → ~13 dias de relógio, sem suspensão; 4 núcleos físicos (memória
cabe — ~220 MB por processo — se o navegador sair) → ~7 dias; K núcleos fora → ~620/K h, limitado pela maior unidade
(~65 min): 64 núcleos → ~11 h. **Ressalvas:** custo por ponto medido num ponto só (apical_500) — pontos distais com
Ca-spike no M4 a 1.5 nA podem custar mais; M5 medido só a 1 nA (0.78 e 1.9 nA estimados pela mesma ordem); F estimado
do P6cv nativo sem disputa (1 395 s em N = 16) + EPSP/BAC.
**(E) Incidente de processo (registro):** ao parar a rodada antiga, `pgrep -f "nativex/run.sh"` casou com a PRÓPRIA linha
de comando do shell e o derrubou no meio (código 144) — armadilha JÁ registrada (usar o padrão `[x]...`), repetida.
Mesma lição do item 51: o que vive só em texto se repete. Nenhum dado perdido (o launcher antigo caiu, o processo de
N = 32 foi encerrado pelo PID). Para a Etapa A: parar/retomar SEMPRE por PID gravado em arquivo pelo próprio runner,
nunca por padrão de texto.

**65. RESULTADO — NÍVEL B NA CONFIGURAÇÃO REAL (NÓS ALINHADOS), VEREDITO INTEIRO NUMA CONFIGURAÇÃO SÓ (item 59;
2026-10-05 19:05; `hay_v2_final.py` modo NATIVEX, critérios e faixas do item 5 inalterados, detector de pico, regra do
item 57; `results/nativex/v2_nos.json`).** P2–P7 todos no NATIVEX sem o Hay fino vivo (item 64B):
| N | P2 | P3 | P4 local / soma | P5 (bAP) | P7 1º PA (CaBurst) | taxa f-I | f-I D123 / P7 contagens | nível A | nível B |
|---|---|---|---|---|---|---|---|---|---|
| 16 | 0.058% | 0.327% | 0.163% / 0.025% | 0.46% | **0.425 ms** | 0.049% | ok / ok | PASSA | **falha** (só o 1º PA) |
| 32 | 0.018% | 0.233% | 0.156% / 0.008% | 0.54% | **0.150 ms** | 0.077% | ok / ok | PASSA | **PASSA** |
**→ Nível B = N = 32, AGORA com veredito na configuração real (nós nos pontos de medida). A ETAPA A FICA EM N = 32.**
Verificação cruzada: N = 16 sem × com o Hay fino vivo — P3 idêntico, P5 a 1.5×10⁻⁴, picos do P7 idênticos, contagens
do P6 iguais. **Custo da Etapa A (item 64D): ≈ 620 h ≈ 26 dias-CPU** (não ~52: o ×2 para N = 32 não se confirmou na
medida sem o fino). **A Etapa A NÃO foi iniciada:** falta (1) o modelo direto com os 30 parâmetros por região (D131 7.1)
e a verificação de que em θ_verdadeiro ele reproduz o NATIVEX; (2) a decisão de ONDE rodar (2 processos locais ~13 dias;
4 núcleos ~7 dias se a memória permitir; K núcleos fora ~620/K h). Concorrência: `pv_C` e `hay4_C` retomados (dois
pesados).

**66. DECISÃO DO USUÁRIO — TRÊS ITENS; A ETAPA A AINDA NÃO COMEÇA (2026-10-05 21:47; declarações ANTES de rodar).**
**Registros.** (a) O `pgrep -f` matando a própria shell reapareceu apesar de registrado; agora o runner para e retoma SÓ
por PID gravado — mais uma armadilha que passou de texto para código. (b) O custo da Etapa A é ~620 h (~26 dias-CPU);
os ~52 anteriores vinham do NATIVEX mantendo o Hay fino vivo. (c) **Inibidor com escopo para as referências**
(`pv_C`, `hay4_C`): `systemd-inhibit … tail --pid=<PID>` — vive enquanto o processo vive; verificado com um processo de
teste (1 inibidor durante, 0 depois de sair).
**REGRA NOVA (generaliza o controle negativo por métrica, item 40c):** antes de usar uma métrica como critério,
verificar que ela é ESTÁVEL diante de perturbações MENORES que o efeito que ela quer detectar.
**(1) MODELO DIRETO COM 30 PARÂMETROS POR REGIÃO (`neuron/etapaA_model.py`, caminho crítico).** Hay nativo, N = 32 por
ramo, nó em cada ponto de medida (divisão exata da geometria, como o NATIVEX); densidades = FORMAS do Hay × θ (D131 7.1,
nível 1): passivo por região (g_pas soma/axônio/basal/apical; c_m soma+axônio e dendritos; R_i; e_pas), soma (9 canais +
γ/decay do Ca), apical (NaTa_t, SKv3_1, SK_E2, Im uniformes; Ca_LVAst e Ca_HVA = AMPLITUDE da zona 685–885 µm com a forma
do Hay — fora da zona ×0.01 e ×0.1 —; γ/decay; Ih = amplitude e ESCALA DE COMPRIMENTO da exponencial do Hay, expoente
3.6161/θ_escala), basal (Ih). O axônio do biophys3 é só passivo. **Convenção de distância das formas = a do CÓDIGO do
Hay:** `distribute_channels` chama `getLongestBranch("apic")`, que põe a origem em apic[0](0) — a zona de Ca e a
exponencial do Ih são medidas a partir de apic[0](0), não do soma. `split_section` e os pontos do V2 passam a viver só
nesta biblioteca (o `hay_native.py` importa daqui — um caminho de código).
**Validação (declarada; tolerância NÃO exata):** (V0) parâmetros por segmento em θ_verdadeiro × o Hay fino (Δ 0.5) no
mesmo lugar (o que o NATIVEX amostra): diferenças só onde a forma varia dentro de um segmento fino (≤ 0.25 µm: bordas da
zona de Ca, exponencial do Ih) — reportadas, não critério; (V1) protocolos do V2 (P2–P7) no modelo em θ_verdadeiro pelo
MESMO código de medida do V2 (`hay_native.py`, modo novo `REGION`) contra a MESMA referência (L0 Δ0.5): **PASSA se
cumpre TODOS os critérios do NÍVEL B** (o que o V2 certificou em N = 32) — não igualdade; (V2) conjunto funcional F da
Etapa A (D131 7.4: EPSC 10 pA τ 0.5/3 nos **30 pontos sorteados uniformemente por comprimento nos dendritos, semente
131** + pontos do D127/V2 → pico e tempo de pico do EPSP somático; BAC e CaBurst → 1º PA (BAC: 2º, item 39) e pico do
Ca-spike no hay_620; f-I nos degraus do Hay 0.78/1.0/1.9 nA × 2 s → taxa por ISI) calculado pelo código da Etapa A no
modelo em θ_verdadeiro E no Hay L0 Δ0.5; **resíduo r = F_red(θ_verd) − F_Hay = o TERMO DE VIÉS da Etapa A** (item 26:
δF_viés = G·δθ_viés + (F_Hay − F_red(θ_verd)) — a parcela direta é −r), pela MESMA função; PASSA se cada |r_i| cumpre a
faixa do NÍVEL B da sua classe (EPSP somático ≤ 1%; 1º PA ≤ 0.2 ms; taxa ≤ 0.4%); pico do Ca-spike e tempo de pico do
EPSP não têm faixa no nível B → reportados como NÃO AVALIADOS (não como aprovados). **Coerência (declarada):** nas
grandezas que (V1) e (V2) medem pelo MESMO protocolo (1º PA do BAC/CaBurst — P7; EPSP somático nos pontos do V2 — P4), o
termo de viés da Etapa A tem de REPRODUZIR o resíduo da validação do V2 (códigos independentes): 1º PA |dif| ≤ 0.05 ms
(2 amostras do detector), EPSP |dif| ≤ 10⁻³ relativo (o P4 do V2 é Euler 0.025, o da Etapa A CVode — diferença de
integrador num EPSP sublimiar convergido). Se não reproduzir: parar e reportar.
**Teste de unidade antes da execução longa:** UMA unidade completa de ponto de injeção (todas as perturbações) num ponto
DISTAL com spike de Ca (na zona 685–885 µm) — custo medido.
**(2) ALLEN PV — CONDICIONAMENTO DA MÉTRICA (baixa prioridade; quando houver vaga).** Teste independente do reduzido:
perturbar a REFERÊNCIA — L0 Δ1 a 400 pA × (1 ± 0.01) e × (1 ± 0.02) (396, 398, 402, 404 pA), CVode atol 10⁻⁶, detector de
pico. **Declarado:** se a CONTAGEM ou a ESTRUTURA DE SALVAS (PA por salva, ISI > 50 ms separa salvas) do L0 MUDA em
alguma dessas amplitudes → a contagem é MAL CONDICIONADA a 400 pA e NÃO é critério válido ali; o critério passa a ser a
grandeza CONTÍNUA (inícios de salva), com tolerância ligada à precisão da referência (L0 Δ2 × Δ1: 2.9 ms no início da 2ª
salva); se o L0 é ESTÁVEL nas quatro → a contagem está bem condicionada e a mudança de estrutura em N = 32 é FALHA REAL da
redução no regime de salvas.
**(1b) TESTE DE UNIDADE — DESENHO DECLARADO (antes de rodar; detalhes que o D131 7.2 deixou em aberto):** modelo =
`RegionModel` N = 32 com nó em TODOS os 503 pontos da grade de 25 µm; ponto distal p = o da grade a 800 µm do soma no
caminho apical mais longo (dentro da zona de Ca 685–885 µm a partir de apic[0](0)). Subpassos (125): base; θ ±1% em
log (60); ganho (+1% na corrente injetada EM p); posição (p deslocado +2 µm ao longo do ramo — nó movido); geometria
(30 amostras de diâmetro: σ = 0.2 µm por seção, independente; 30 de comprimento: 2% por seção; escala global de diâmetro
±1% — 2), semente fixa 131. Geometria alterada NO LUGAR (mesma estrutura: diâmetros por segmento; comprimento
pelos pontos 3D), θ e geometria devolvidos à base após cada subpasso. Protocolos em p: **M1** ±50 pA, 1 s (início
100 ms, 1 150 ms) lendo TODOS os 503 pontos + soma (M2); **M4** EPSC τ 0.5/5 ms a **0.2 / 0.5 / 1.5 nA** (as amplitudes
da medida de custo do item 20; "sublimiar, limiar do BAC, 3×" — FIXAS em todos os pontos), início 5 ms, 300 ms, lendo p
e soma; CVode atol 10⁻⁶; amostra 0.1 ms; traço − linha de base (V no instante do estímulo). **Repouso: assentado em
CADA subpasso** (3 s a passo fixo 0.1 ms, como no V2) — simples e correto; o custo do repouso e o dos protocolos são
medidos SEPARADOS. Redução por ponto de leitura r: J (30 colunas, diferença central), D (ganho), Δy (posição e 62 de
geometria, contra a base) → JᵀJ, JᵀD, JᵀΔy. Falta que o levantamento do item 64D NÃO contava: o repouso por subpasso
(cada perturbação muda o repouso) — a alternativa a medir (não adotada) é guardar os 125 repousos uma vez e reusá-los
em todas as unidades.

**67. RESULTADOS (2026-10-06) — MODELO DIRETO VALIDADO; COERÊNCIA DO VIÉS NÃO CONFIRMADA NO EPSP; CUSTO DO PONTO DISTAL.**
**(V0) Parâmetros por segmento em θ_verdadeiro × Hay fino (`etapaA_check_v0.py`):** 6 244 segmentos; TODOS os
parâmetros idênticos (R_i, c_m, g_pas, e_pas, reversões, todos os canais, Ca nas zonas) exceto o Ih apical: dif. máx
0.19% (a exponencial avaliada no centro do segmento nativo × no centro do segmento fino que o contém). As zonas de Ca
batem exatamente — **confirma a origem apic[0](0) das formas.** Grade de 25 µm: **503 pontos** (o levantamento usou 503).
**(V1) Protocolos do V2 no modelo direto (`hay_native.py` modo REGION, N = 32; `results/region/`):** **nível B PASSA**
(EPSP somático 6×10⁻⁵; medidas 0.54% — P5 na ponta apical; 1º PA 0.150 ms; taxa 0.077%; f-I D123 e contagens do P7 ok);
nível A passa. Defeito achado e corrigido NO CAMINHO: o `hay_v2_final.py` avaliava um P6 INCOMPLETO (8 de 10 amplitudes,
rodada ainda em curso) como se fosse completo — agora exige todas as amplitudes da referência ("incompleto" senão; regra
do item 57). Os vereditos anteriores (V2 original e NATIVEX) foram reconferidos: inalterados (eram completos).
**(V2) Conjunto funcional F pelo código da Etapa A (`etapaA_F.py`; resíduo = `vies()`, a MESMA função do termo de viés;
`etapaA_validate.py`):** EPSP somático nos 48 sítios pior −0.123% (apical_1200) ≤ 1% — passa; BAC 2 × 2 PA, Δ +0.025 ms;
CaBurst 1 × 1, Δ +0.125 ms ≤ 0.2 — passa; taxa f-I −0.050 / −0.052 / −0.075% ≤ 0.4% — passa; tempo de pico do EPSP
(pior +1.05 ms, ponta apical) e pico do Ca-spike (−0.15 / −0.17 mV) sem faixa no nível B → NÃO AVALIADOS. **→ O modelo
direto em θ_verdadeiro PASSA o nível B também no conjunto F.**
**COERÊNCIA (declarada no item 66): NÃO CONFIRMADA → parado e reportado.** 1º PA: BAC viés +0.025 × resíduo do V2
+0.000 ms; CaBurst +0.125 × +0.150 ms (|dif| 0.025 ≤ 0.05 — ok). **EPSP somático: |viés − resíduo do V2| máx 1.29×10⁻³
(apical_1200: −0.123% × +0.005%) > 10⁻³ declarado.** Diagnóstico (não muda a faixa): o EPSP somático desse sítio é de
**4.6 µV**; no MESMO modelo, CVode atol 10⁻⁶ (Etapa A) × Euler 0.025 ms (P4 do V2) já diferem até **0.15%** (L0:
+0.150% em apical_1200; reduzido: +0.021%) — a faixa de coerência de 10⁻³ foi declarada ABAIXO da precisão dos
integradores que produzem os dois resíduos em sinais de µV. Os dois caminhos usam a MESMA função de viés; a diferença está
no integrador do V2, não no código da Etapa A. Decisão do usuário (ex.: repetir os dois lados com o mesmo integrador, ou
atol menor, antes de declarar coerência).
**CUSTO DO PONTO DISTAL (unidade de teste g_apic[60]_32, 800 µm, zona de Ca; em curso, desenho (a) do item 66 1b):**
**~254 s por subpasso** (repouso ~82 s + protocolos ~172 s; 19 de 125 subpassos) → **~9 h por unidade** (o levantamento
do item 64D supunha ~31 s/subpasso e ~65 min/unidade); ~46 MB de disco por subpasso (~5.8 GB por unidade, como previsto).
**De onde vem (diagnóstico, `etapaA_cost_diag*.py`, `etapaA_rec_diag.py`):** (i) NÃO é o ponto distal nem a grade —
o M1 custa ~45 s no modelo com 503 nós (699 seções) E no modelo com só os 18 pontos do V2 (210 seções), no ponto distal
E a 500 µm; ler 504 pontos × 2 pontos: +5 s; (ii) **é a GRAVAÇÃO EM GRADE FIXA sob CVode**: `Vector.record(&v, tvec)`
(interpolação do CVode em cada um dos 11 501 instantes) — M1 46.7 s; gravar nos passos do CVode + interpolação linear
para a grade — **5.2 s (9× menos)**; `record(&v, Dt)` — 45.7 s. Precisão da opção barata: traço |Δ| máx 0.036 mV;
**coluna do Jacobiano (θ = g_pas apical ±1%) |Δ| 0.34% relativo**. (Este custo já aparecia no teste do item 52 — 0.03 ×
0.49 s — e foi lido só pela contagem de passos, que não muda.) (iii) **o REPOUSO por subpasso** (~70–85 s, 3 s a dt 0.1)
— a alternativa é guardar os 125 repousos uma vez. **Projeção (estimativa, não medida inteira):** gravação nos passos +
repousos guardados → ~17 s/subpasso → ~35 min/unidade → ~300 h nos pontos + o resto ≈ **~15 dias-CPU**; como está (a +
repouso por subpasso) → ~9 h/unidade → **~4 500 h (~190 dias-CPU)**. A escolha (precisão do Jacobiano × custo) e a
verificação do reuso de repouso são do usuário.

**68. RESULTADO — CONDICIONAMENTO DA MÉTRICA DO ALLEN PV A 400 pA (item 66 (2); L0 Δ1, CVode, detector de pico;
`results/allen_cond/`).** **Correção da declaração:** no item 66 escrevi "×(1 ± 0.01) e ×(1 ± 0.02) (396, 398, 402,
404 pA)" — esses números são ±0.5% e ±1%; rodei os quatro e também os ±2% pedidos (392, 408).
| amplitude | PA | salvas (PA por salva) | início das salvas (ms) |
|---|---|---|---|
| 392 pA (−2%) | 4 | 2, 2 | 7.2, 815.4 |
| 396 pA (−1%) | 6 | 2, 2, 2 | 6.7, 509.9, 711.7 |
| 398 pA (−0.5%) | 8 | 3, 3, 2 | 6.4, 549.6, 901.2 |
| **400 pA** | **9** | 3, 3, 3 | 6.2, 428.6, 701.4 |
| 402 pA (+0.5%) | 12 | 3, 3, 3, 3 | 6.1, 292.1, 540.9, 815.1 |
| 404 pA (+1%) | 16 | 4, 3, 3, 3, 3 | 5.9, 312.2, 482.8, 731.1, 906.8 |
| 408 pA (+2%) | 23 | 5, 3, 3, 3, 3, 3, 3 | 5.6, 207.7, 353.0, … |
**Pela regra declarada: a contagem e a estrutura de salvas do L0 MUDAM dentro da faixa (já a ±0.5%) → a CONTAGEM é MAL
CONDICIONADA a 400 pA e NÃO é critério válido ali.** (~1 PA por 0.25% de corrente; a diferença N = 8 × L0, 11 × 9,
equivale a deslocar a entrada em ~0.5% — menor que o passo em que a própria métrica muda.) **Aplicando a REGRA NOVA (item
66: a métrica tem de ser estável diante de perturbações menores que o efeito) também à substituta declarada:** os
inícios de salva NÃO são estáveis — o início da 2ª salva anda 815 → 510 → 550 → 429 → 292 → 312 → 208 ms (não monótono;
120–140 ms para ±0.5%, contra a precisão da referência de 2.9 ms). **→ A 400 pA nenhuma das duas métricas é critério
válido: a amplitude está numa FRONTEIRA DE REGIME (entrada no disparo em salvas repetitivas).** Consequência para o
veredito do item 60/63: a única FALHA (contagem a 400 pA) sai como NÃO AVALIADA; com inclinação e adaptação também NÃO
AVALIADAS (referência não convergida a 410/600 pA), o veredito do Allen PV em N = 8 fica **NÃO AVALIADO** — não PASSA (a
ausência de avaliação não é aprovação). Se outras amplitudes perto do limiar (380–410 pA) estão na mesma fronteira, e que
métrica usar nesse regime, é decisão do usuário. `pv_C` retomado (dois pesados: ele e a unidade de teste).

**69. DECISÃO DO USUÁRIO — COERÊNCIA PELO MESMO CÁLCULO; DOIS TESTES DE CUSTO; REGRAS (2026-10-06 09:06; declarado ANTES de
rodar).**
**Registros.** (a) **A tolerância de coerência (10⁻³) estava CERTA; a premissa de cálculo idêntico estava errada:** o
termo de viés (Etapa A, CVode) e o resíduo do V2 (P4 em Euler 0.025 ms) não eram calculados do mesmo jeito — a
tolerância declarada não foi violada por erro do modelo, mas por DOIS CAMINHOS DE CÁLCULO diferentes; mesma lição dos dois
detectores. (b) **REGRA NOVA: as AMPLITUDES DE TESTE também passam pelo condicionamento antes de entrar num critério** —
um ponto de operação numa fronteira entre regimes não serve para comparar modelos (Allen PV a 400 pA: contagem de 4 a 23
PA em ±2%; início da 2ª salva de 208 a 815 ms; reclassificação para NÃO AVALIADO confirmada). (c) **Defeito registrado:**
o script do V2 avaliava uma rodada de P6 INCOMPLETA como completa — agora recusa; mesma família da ausência de avaliação.
**(1) COERÊNCIA — IGUALAR O CÁLCULO, NÃO AFROUXAR A TOLERÂNCIA.** O lado do V2 é REFEITO com o MESMO integrador da Etapa A:
P4 (EPSP 10 pA τ 0.5/3 em cada ponto do V2, pico somático com a linha de base sem estímulo subtraída) em CVode atol 10⁻⁶
(protocolo novo `P4cv` no `hay_native.py`; linha de base INTERPOLADA no tempo do traço, porque sob CVode os dois traços
não têm os mesmos instantes) no modelo direto (REGION 32) e no L0 Δ0.5. **Tolerância INALTERADA:** |viés da Etapa A −
resíduo do V2| ≤ 10⁻³ relativo no EPSP somático (e 1º PA ≤ 0.05 ms, já CVode nos dois). Passa → coerência confirmada;
não passa → há incoerência real entre os dois cálculos: reportar a causa antes de seguir.
**(2a) GRAVAÇÃO NOS PASSOS DO SOLVER + INTERPOLAÇÃO — teste NA SAÍDA, numa mesma unidade (o ponto distal
g_apic[60]_32), só as 61 avaliações de θ.** (a) = gravação em grade fixa pelo CVode (a da unidade de teste em curso);
(b1) = passos do CVode + interpolação LINEAR; (b3) = passos do CVode + interpolação CÚBICA (spline de Hermite monótona,
PCHIP — ordem maior que a linear) — (b1) e (b3) das MESMAS simulações. Matriz por variante: JᵀJ da unidade (todas as
leituras). **Tolerância (declarada):** (i) os 5 MENORES valores singulares de J: diferença relativa ≤ 5% cada, e a
CONTAGEM de valores singulares abaixo de 10⁻³·σ_max e de 10⁻⁶·σ_max IDÊNTICA (as direções mal determinadas não podem
aparecer nem sumir); (ii) incerteza funcional prevista σ_F = √diag(G (JᵀJ)⁺ Gᵀ) (Cramér–Rao propagado, σ_V unitário):
diferença relativa ≤ 5% em CADA componente de F. G = ∂F/∂log θ por diferença central (passo 1%) no modelo direto,
COMUM às três variantes — F REDUZIDO para o teste: EPSP somático nos 48 sítios + 1º PA (BAC 2º, CaBurst 1º) + pico do
Ca-spike (a f-I fica fora: ~17 h só para G; registrado). Aceita a variante MAIS BARATA que cumprir (i) e (ii).
**(2b) REPOUSOS GUARDADOS.** O repouso depende de θ (e da geometria), NÃO do ponto de injeção: calculado UMA VEZ por
perturbação e reaproveitado nas 503 unidades. **Condições:** chave do cache = (θ, DISCRETIZAÇÃO) — hash de θ, da
geometria e da discretização (N, os 503 pontos, nseg de cada seção), nunca só θ; a restauração passa OBRIGATORIAMENTE pela
função comum (`stim_common`, com o autoteste) — território da armadilha que já reapareceu duas vezes. **Verificação
(declarada):** para 3 θ (base, g_pas_apical +1%, apic_Ca_LVAst_zona +1%) em 3 pontos (proximal ~100 µm, médio ~500 µm,
DISTAL g_apic[60]_32): estado guardado → carregado em OUTRO processo × assentado de novo: vetor de estados IDÊNTICO
(|Δ| máx ≤ 10⁻⁹ em cada estado) e resposta ao M1 +50 pA (1 s, CVode, lida em p e no soma) |Δ| máx ≤ 10⁻⁶ mV.

**70. RESULTADO — COERÊNCIA: COM SÓ O INTEGRADOR IGUALADO, NÃO PASSA; A CAUSA SÃO MAIS DOIS CAMINHOS DE CÁLCULO
DIFERENTES; COM O CÁLCULO INTEIRO IGUALADO, OS DOIS DÃO O MESMO NÚMERO (2026-10-06 09:41; `results/coer/`).**
**(1) Pela regra declarada (item 69: refazer o lado do V2 em CVode, tolerância 10⁻³ inalterada): NÃO PASSA** —
`P4cv` (CVode atol 10⁻⁶) no REGION 32 e no L0 Δ0.5: |viés da Etapa A − resíduo do V2| máx **1.25×10⁻³** (apical_1200:
V2 +0.0012% × Etapa A −0.1234%). → reportar a causa antes de seguir.
**(2) Causa — mais dois caminhos de cálculo diferentes, além do integrador:** (a) **MODELOS DIFERENTES:** o código do F
da Etapa A constrói o modelo direto com nós nos 48 sítios do F (30 sorteados + 18 do V2); o lado do V2 (REGION) só nos
18 pontos do V2 — duas discretizações; (b) **REPOUSOS DIFERENTES:** o `hay_native` assenta 3 100 ms (os 100 ms a mais
medem a deriva), o código do F 3 000 ms — **o repouso NÃO está convergido em 3 s** (Ih e Ca lentos): 100 ms a mais mudam o
EPSP somático em até 3.6×10⁻⁵ mV (0.05%) no MESMO modelo (L0, apical_100). **Prova:** com a MESMA discretização (nós nos
48 sítios, `P4cv,SITIOSF`) e o MESMO assentamento (3 100 ms nos dois caminhos), os dois caminhos dão valores IDÊNTICOS
(|Δ| = 0.0 mV no reduzido e no L0) → |viés − resíduo| = 0. Com só a discretização igualada (assentamentos 3 100 × 3 000),
ainda 1.71×10⁻³ (apical_900). **Mesma lição dos dois detectores, agora em três peças: integrador, discretização e
repouso — tudo o que define o número tem de vir do MESMO código.** **Providência proposta (não adotada sem o usuário):** um
único `Sim` (assentamento + injeção + leitura) compartilhado por TODO cálculo do desmame (validação, viés, Etapa A), com a
duração do assentamento e a discretização como parte da CHAVE do resultado (como a chave do cache de repouso, item 69 2b);
e registrar que 3 s de assentamento deixam o repouso não convergido no nível de 10⁻⁴ relativo no EPSP de µV.

**71. RESULTADOS (2026-10-06) — OS DOIS TESTES DE CUSTO (item 69 (2)).**
**(2b) REPOUSO GUARDADO × REASSENTADO — PASSA (`etapaA_cache_test.py`, `results/etapaA_cache/`):** modelo da Etapa A
(503 nós), 3 θ (base, g_pas_apical +1%, apic_Ca_LVAst_zona +1%), 3 pontos (proximal ~100 µm, médio ~500 µm, distal
g_apic[60]_32); repouso assentado e guardado num processo (chave = hash de θ + discretização + assentamento) e CARREGADO
em OUTRO processo pela função comum (`stim_common`: `fread` → `restore(1)` → conferência de t e V gravados → autoteste
pulso × passo fixo): **vetor de estados (47 471) |Δ| = 0.0 e resposta ao M1 nos 3 pontos |Δ| = 0.0 mV, nos 3 θ** —
idênticos bit a bit (critério: 10⁻⁹ e 10⁻⁶ mV). O cache vive no `stim_common` (`state_key`, `save_state`,
`load_state`, `move`). Custos: assentar pelo `stim_common` (CVode, 3 s) ~20 s; o autoteste ~40 s (uma vez por
processo); carregar = ler 47 mil números.
**(2a) GRAVAÇÃO — critério (i) FALHA para as duas variantes baratas (`etapaA_rec_test.py`; 61 avaliações θ da mesma
unidade distal; (b) é a MESMA simulação de (a) — o modo de gravação não muda os passos do CVode —, logo toda a diferença
é de INTERPOLAÇÃO):**
| variante | σ_máx de J | 5 menores σ | abaixo de 10⁻³·σ_máx | abaixo de 10⁻⁶·σ_máx | 5 menores × (a) |
|---|---|---|---|---|---|
| (a) grade fixa pelo CVode | 6 074 | 0.178, 0.291, 0.429, 0.653, 0.747 | 13 | 0 | — |
| (b1) passos + linear | 6 074 | 1.50, 1.60, 1.80, 2.04, 2.40 | 13 | 0 | **até +745%** |
| (b3) passos + PCHIP | 6 074 | 0.224, 0.254, 0.273, 0.332, 0.394 | 13 | 0 | **até 49%** |
→ **(i) FORA para as duas** (≤ 5% declarado); contagens abaixo dos limiares iguais. **Exatamente a amplificação
prevista pelo usuário:** 0.34% de erro numa coluna vira 745% nos menores valores singulares — a interpolação linear
CRIA informação falsa nas direções mal determinadas (o erro de interpolação, diferente entre θ+ e θ−, parece
sensibilidade). (ii) σ_F: aguarda o G (em curso), mas (i) já reprova as duas. **Ressalva registrada:** o menor σ de (a)
(0.18) é da ORDEM do piso numérico esperado do próprio Jacobiano (atol 10⁻⁶ ÷ passo 2·1% × √11.6 milhões de linhas ≈ 0.17)
— as direções mais fracas podem ser numéricas, não físicas; isso pede um teste próprio (Jacobiano com atol menor) antes de
se interpretar o fundo do espectro na Etapa A.
**(2a) critério (ii) — σ_F (Cramér–Rao propagado ao F reduzido; G = ∂F/∂log θ, 52 componentes × 30, todas finitas;
`results/etapaA_rec/G/G.npz`): FALHA para as duas** — linear até **88%** (EPSP no sorteio_29), PCHIP até **128%**
(EPSP no apical_300). **→ Nenhuma variante barata aceita; a gravação fica em (a).** Terceira opção testada:
`CVode.record(&v, vec, tvec, 1)` — dá EXATAMENTE (a) (|Δ| = 0.0), mas custa o MESMO (43.5 × 47.9 s): o custo de (a) está
nos 11 501 eventos de tempo fixo (o CVode reconstrói os ~47 mil estados em cada instante — por isso ler 2 ou 504 pontos
custa quase o mesmo), não no jeito de gravar. Não testado (registrado como candidato): limitar o passo do CVode
(`maxstep` ≤ 0.1 ms) e gravar nos passos.
**PROJEÇÃO DE CUSTO DEPOIS DOS DOIS TESTES (estimativa a partir das medidas; 1 núcleo):** subpasso = protocolos em (a)
~150 s sem disputa (M1 2 × ~47 s + M4 13.8/18.8/22.9 s) + repouso CARREGADO (~0 s; assentamento ~20 s UMA vez por
perturbação: 61 θ + 62 geometrias, globais; a posição é por unidade) → **~5.2 h por unidade × 503 ≈ 2 620 h**; G completo
(61 avaliações do F com f-I, ~25 min cada) ≈ 25 h; viés de especificação (Hay L0, 1 avaliação em todos os pontos, ~3.5× o
reduzido) ≈ 75 h; assentamentos + autotestes ≈ 5 h → **≈ 2 700 h ≈ 113 dias-CPU** (como estava, com repouso por
subpasso: ~190; o levantamento do item 64D dizia ~26 — supunha 31 s/subpasso, sem repouso e sem o custo da gravação).
Execução: 2 processos locais ~57 dias; 4 núcleos ~28 dias (se a memória deixar); K núcleos fora ~2 700/K h (64 → ~42 h,
limitado pela maior unidade, ~5 h). **Ressalvas:** (1) o fundo do espectro de J está no piso numérico do CVode
(atol 10⁻⁶) — se for preciso atol menor para as direções fracas, o custo SOBE; (2) M4 a 1.5 nA medido num ponto
distal só; (3) a unidade completa (125 subpassos, com posição e geometria) ainda não terminou (parou no subpasso 63 pelo
erro de nó corrigido no item 69 — a retomar).

**73. DECISÃO DO USUÁRIO — TRÊS AJUSTES ANTES DE LANÇAR A ETAPA A (2026-10-06 13:26; declarado ANTES de rodar).**
**(1) CÓDIGO ÚNICO — ADOTADO, COM ASSENTAMENTO POR CRITÉRIO.** Um só código de assentamento, injeção e leitura
(`stim_common`, com o autoteste) usado por TODO cálculo do desmame em CVode (Etapa A, viés, validação do V2), com a
DISCRETIZAÇÃO e o ASSENTAMENTO na chave do resultado. Tempo fixo de assentamento é número escolhido → **ASSENTAR ATÉ
CONVERGIR:** CVode atol 10⁻⁶ em blocos de 100 ms; para quando, entre dois blocos sucessivos, a mudança de CADA variável de
estado for |Δx_i| ≤ 10⁻⁸ (nas unidades da variável: mV, portões adimensionais, mM) — critério sobre o vetor de estados
inteiro (norma do máximo), não sobre o V só; teto de 60 s de simulação — não convergiu → AutotestFailed (a rodada não
começa). A chave do cache inclui o CRITÉRIO (bloco, tolerância, teto), nunca uma duração. Injeção: degraus e α (forma do
`epsp` do Hay, pico = amplitude) em VÁRIOS sítios ao mesmo tempo (BAC: soma + hay_620), com pesos (leitura/injeção fora
de nó no L0). **Revalidação da coerência com o código único** (tolerância 10⁻³ INALTERADA): EPSP somático nos pontos do V2
e 1º PA do BAC/CaBurst — o lado do V2 (`hay_native`) e o lado da Etapa A (`etapaA_F`) passando AMBOS pelo código único, no
MESMO modelo (nós nos 48 sítios) e no L0; |viés − resíduo| ≤ 10⁻³ (EPSP) e ≤ 0.05 ms (PA). Também: um bloco extra de 100 ms
depois da convergência muda o EPSP em menos de 10⁻⁶ relativo (o que motivou o ajuste: +100 ms mudavam até 5×10⁻⁴).
**(2) AS DIREÇÕES FRACAS — registro e verificação barata.** **Registro:** ruído numérico no Jacobiano INVENTA informação
nas direções fracas (infla os menores valores singulares) — o viés é sempre para o OTIMISMO; somado a Cramér–Rao (já
otimista), a especificação sairia otimista duas vezes; e o menor valor singular da referência (0.18) está no piso de
ruído do solver (≈ 0.17). **Verificação barata (dados existentes: J da unidade distal, 61 avaliações, gravação (a); G do
item 72, 52 componentes):** direções fracas = vetores singulares à direita v_k de J com σ_k ≤ 10 × 0.17 = 1.7 (a uma
década do piso). Efeito em F ao longo de cada uma: ΔF_k = |G v_k| × 2.3 (deslocamento máximo dentro dos limites do D131
7.1, ×[0.1, 10] em torno do verdadeiro = ±2.3 em log). **Critério:** F INSENSÍVEL se, para TODA direção fraca, ΔF_k fica
abaixo da tolerância funcional da Etapa A (D131 7.4): EPSP somático 5% (relativo ao F0 do sítio), 1º PA 1 ms; pico do
Ca-spike sem tolerância → reportado, NÃO AVALIADO. Insensível → o piso numérico não afeta a especificação; segue com
atol 10⁻⁶. Sensível → UMA unidade (a distal) com atol 10⁻⁸ nas 61 avaliações θ: se os menores valores singulares mudarem
> 5% → a Etapa A inteira precisa da tolerância apertada (recalcular o custo). **Limitação declarada:** J de UMA unidade
(um ponto de injeção), não o J da Etapa A inteira — as direções fracas de uma unidade são mais fracas que as do conjunto.
**(3) ORDEM ADAPTATIVA DE ESPAÇAMENTO.** Unidades em ordem do mais GROSSO ao mais FINO: s = 400 µm primeiro, avaliar a
especificação; descer para 200, 100, 50, 25 SÓ se o espaçamento atual não bastar (lógica da bissecção do ruído). O custo
passa a depender do s\* encontrado. **Condição para o reaproveitamento ser exato:** TODAS as unidades usam o MESMO modelo
(nós nos 503 pontos da grade de 25 µm, em qualquer espaçamento — a discretização é a chave), e cada unidade grava os blocos
POR ponto de leitura; o JᵀJ de um espaçamento s é a soma dos blocos (p, r) com p e r no subconjunto de s. **Verificação
(declarada):** na unidade distal completa, o JᵀJ do subconjunto de leituras de s = 400 obtido (A) somando os blocos
gravados e (B) recalculando J direto dos traços brutos só nessas leituras → |A − B| ≤ 10⁻¹² relativo (ordem de soma);
e os pontos de s = 400 são subconjunto exato dos de 25 µm.
**ONDE RODAR — pendente do Martel.** Preparar sem iniciar: dependências fixadas, memória por processo, volume por unidade,
e a confirmação de que a retomada bit a bit permite instâncias interrompíveis.
**CORREÇÃO DO MÉTODO DE ASSENTAMENTO (2026-10-06, achada no teste de fumaça, ANTES de qualquer resultado; tolerância
INALTERADA):** o declarado ("CVode atol 10⁻⁶ em blocos de 100 ms até |Δx| ≤ 10⁻⁸") é INATINGÍVEL — o próprio CVode a
atol 10⁻⁶ faz o estado oscilar entre blocos no nível de 10⁻⁷–10⁻⁶ (ruído do integrador): no modelo de teste (soma HH +
dendrito passivo) não convergiu em 60 s (resíduo 1.1×10⁻⁶); o mesmo erro de família da coerência — tolerância declarada
abaixo da precisão do integrador que a mede. Medido no mesmo modelo: CVode 10⁻⁶ só cruza 10⁻⁸ por acaso (8.5 s; 10⁻⁷ aos
3 s); CVode 10⁻⁹ em 300 ms; **Euler implícito dt 0.1 em 300 ms (1.3×10⁻¹²)**. **Adotado: assentar por EULER IMPLÍCITO
(dt 0.1 ms)** — o ponto fixo do Euler implícito É o equilíbrio verdadeiro (f(x) = 0 ⇒ x_{n+1} = x_n, qualquer dt), sem
tolerância de integrador no repouso — em blocos de 100 ms até |Δx_i| ≤ 10⁻⁸ em TODA variável; teto 60 s. Protocolos em
CVode atol 10⁻⁶ a partir desse repouso. A chave inclui o método (Euler dt 0.1, bloco, tolerância, teto).

**74. RESULTADOS (2026-10-06) — DIREÇÕES FRACAS, ORDEM ADAPTATIVA, CÓDIGO ÚNICO, PREPARO PARA RODAR.**
**(A) DIREÇÕES FRACAS — F é SENSÍVEL (critério do item 73 (2); `etapaA_weak_dirs.py`).** σ de J (unidade distal):
0.178 … 6 074; **10 direções fracas** (σ ≤ 1.7). Ao longo de CADA uma, |G v_k| × 2.3 move o EPSP somático de algum sítio
além de 5% (9–21%), e em 6 delas o 1º PA além de 1 ms (até 6.3 ms; CaBurst e BAC); pico do Ca-spike até 2 mV (NÃO
AVALIADO). As direções fracas são combinações de canais SOMÁTICOS (K_Tst, Ca_LVAst, K_Pst, Nap, Ca_HVA, γ do Ca, SK,
g_pas soma/axônio, Ih soma) — o que uma injeção distal mal vê. Ressalva: a extrapolação linear por ±2.3 em log (fator 10)
superestima ou subestima o efeito real (não linear). **→ Pela regra declarada: rodar UMA unidade com atol 10⁻⁸** — em
curso (unidade distal, 61 avaliações θ; ~350 s/subpasso → ~6 h).
**(B) ORDEM ADAPTATIVA — REAPROVEITAMENTO EXATO (`etapaA_subset_check.py`).** Os pontos de s = 400 / 200 / 100 / 50 µm
(20 / 51 / 119 / 249) são SUBCONJUNTO exato dos 503 da grade de 25 µm (mesmos nomes e arcos). JᵀJ do subconjunto de
s = 400 pela SOMA DOS BLOCOS gravados × recalculado DIRETO dos traços: |A − B| = **1.6×10⁻¹⁴** relativo (ordem de soma)
— **EXATO**. Condição registrada: TODAS as unidades no MESMO modelo (nós nos 503 pontos) em qualquer espaçamento; o custo
de uma unidade não depende de s (lê sempre os 503 pontos). **Custo por s\* (estimativa, unidades de ~5.2 h + G, viés e
repousos proporcionais):** s\* = 400 → 20 unidades ≈ 135 h (~6 dias-CPU); 200 → 51 ≈ 300 h (~12); 100 → 119 ≈ 660 h
(~27); 50 → 249 ≈ 1 340 h (~56); 25 → 503 ≈ 2 700 h (~113) — a confirmar com a decisão do atol (A).
**(C) CÓDIGO ÚNICO (`stim_common.CommonSim`):** assentamento por Euler implícito até |Δx| ≤ 10⁻⁸ por 100 ms (correção do
item 73); no modelo real **converge em 21.5 s simulados** (|Δx| 9.8×10⁻⁹), não em 3 s; injeção em vários sítios com
pesos; leitura ponderada; chave com discretização, critério de assentamento, atol e implementação do α. **α:** o play numa
grade de 5 µs faz o CVode parar em cada ponto (T6) — o P4 do V2 levou > 1 h; trocado pelo mecanismo `epsp` do Hay
(mesma forma, analítico), usado SÓ se, no próprio processo, o EPSP pelos dois caminhos concordar ≤ 0.1% no soma (medido:
0.496666 × 0.496607 mV, 1.2×10⁻⁴); com ele o P4 levou 1 310 s com o assentamento. `hay_native` (protocolos em CVode) e
`etapaA_F` passam pelo CommonSim; os protocolos a passo fixo do V2 (P2/P3/P4 histórico) não. **Bloco extra (declarado:
+100 ms depois de convergido muda o EPSP < 10⁻⁶ relativo): ~~FALHA por pouco~~ [→ **NÃO AVALIADO**, item 75 (1c): abaixo da resolução do integrador] — 1.2×10⁻⁶** (apical_1200: 0.0046297162 →
0.0046297218 mV, 5.6×10⁻⁹ mV). Registro: 10⁻⁶ de um EPSP de 4.6 µV é ~200× abaixo da tolerância absoluta do CVode no
protocolo (atol 10⁻⁶ mV) — TERCEIRA vez que uma tolerância declarada fica abaixo da precisão do integrador que a mede; não
alterada. Antes da convergência, os mesmos +100 ms mudavam até 5×10⁻⁴ (~400× mais).
**(D) ACHADO — O CaBURST MUDA COM O REPOUSO CONVERGIDO:** com o assentamento convergido, o CaBurst (EPSP 1.5 nA no hay_620)
deu **0 PA somático** no modelo direto, pelos DOIS caminhos (antes, com 3 s de repouso, 1 PA em ~128.5 ms em todos os
modelos); BAC inalterado (103.075 / 113.35 ms). O L0 sob o mesmo repouso convergido está rodando — se também mudar, os
vereditos do V2 que usaram o 1º PA do CaBurst foram computados num repouso NÃO convergido e o CaBurst a 1.5 nA está perto
de uma fronteira (regra do item 69: amplitude de teste também passa pelo condicionamento).
**(E) PREPARO PARA RODAR (sem iniciar) — dependências fixadas:** Python 3.14.7; NEURON 9.0.2 (pip `neuron==9.0.2`);
numpy 2.5.3; scipy 1.18.1; mecanismos do Hay compilados por `nrnivmodl` (gcc 16.2.1) a partir do zip sha256
aeeb87d9…e3555; Linux x86_64. **Memória por processo:** pico (VmHWM) ~190–230 MB (unidade da Etapa A, modelo de 503
nós); o Hay L0 Δ0.5 é ~4× maior em segmentos. **Volume por unidade:** em voo ~5.8 GB (125 subpassos × ~46 MB de traços
float32 — apagáveis depois da redução); resultado reduzido ~11 MB (JᵀJ, JᵀX, XᵀX por leitura); G (61 avaliações do F)
~17 kB. **Retomada para instâncias interrompíveis:** bit a bit CONFIRMADA no mesmo ambiente (toy: morta com SIGKILL,
relançada → idêntico; 2 workers → idêntico; a unidade real retomou no subpasso 63); entre máquinas/compilações
DIFERENTES o bit a bit NÃO é garantido (CPU, bibliotecas) → o runner agora grava a IMPRESSÃO DIGITAL (CPU, Python, numpy,
NEURON) em cada unidade e, se a retomada cair noutra impressão, DESCARTA os subpassos parciais daquela unidade e a
recomeça (custo ≤ 1 unidade; testado: descartou, recalculou, resultado idêntico). Corrigido no caminho: corrida entre
workers ao criar o diretório e um arquivo de PID por worker.
**(F) COERÊNCIA COM O CÓDIGO ÚNICO — CONFIRMADA (`results/coer2/`, `coer2_compare.py`; tolerância 10⁻³ inalterada):**
EPSP somático em 16 pontos do V2: |viés da Etapa A − resíduo do V2| = **0.0** (no mesmo modelo, os dois caminhos dão o
MESMO número, |Δ| = 0.0 mV, no reduzido e no L0); BAC 2º PA: |dif| **0.000 ms**; CaBurst: NÃO AVALIADO (sem PA nos dois
modelos — (G)).
**(G) O CaBURST SOB REPOUSO CONVERGIDO NÃO DISPARA — TAMBÉM NO L0.** Com o repouso convergido (21.5 s), o EPSP de 1.5 nA no
hay_620 dá **0 PA somático no L0 Δ0.5 e no modelo direto** (BAC inalterado: 103.075 / 113.35 ms). O "1 PA em ~128.5 ms" de
TODOS os vereditos anteriores era produto do repouso NÃO convergido de 3 s. **Consequência registrada (NÃO decidida):** o
nível B do V2 na configuração com nós (item 65) tinha N = 16 reprovado SÓ pelo 1º PA do CaBurst (0.425 ms) — critério
computado num repouso não convergido e que, sob repouso convergido, deixa de existir (sem PA); o N da Etapa A (32) foi
decidido por ele. O V2 (níveis A/B) precisa ser REFEITO pelo código único (repouso convergido) antes de fixar o N — e o
CaBurst a 1.5 nA está numa fronteira decidida pelo estado de repouso (regra do item 69: amplitude de teste passa pelo
condicionamento; e a f-I, o BAC e os demais protocolos ativos também foram computados sob 3 s).
**(H) ATOL — A ETAPA A INTEIRA PRECISA DE TOLERÂNCIA APERTADA (critério do item 73 (2)).** Unidade distal, 61
avaliações θ, gravação (a), atol 10⁻⁸ × 10⁻⁶: os 10 menores σ mudam **−95.7%, −90.1%, −39.3%, −43.7%, −16.1%, −5.9%,
−9.6%, −29.2%, −4.3%, −1.4%** (σ_mín 0.178 → **0.0077**; 0.291 → 0.029); os maiores, ~10⁻⁵. **O ruído numérico de atol
10⁻⁶ INVENTAVA informação nas direções fracas — o viés para o otimismo previsto pelo usuário, confirmado.** Não se sabe
ainda se 10⁻⁸ convergiu: piso estimado a 10⁻⁸ ≈ 0.0017 (o menor σ fica só ~4.5× acima) — proposta (não rodada): a mesma
unidade a 10⁻¹⁰; se os menores σ mudarem > 5% de novo, apertar mais. Custo medido a 10⁻⁸: protocolos ~214 s × ~172 s a
10⁻⁶ no mesmo regime de disputa (×1.24 — a gravação em grade fixa domina) → unidade ~6.5 h (com repouso guardado);
**por s\*: 400 → ~7 dias-CPU; 200 → ~15; 100 → ~34; 50 → ~70; 25 → ~140** (estimativas). Concorrência: `pv_C` e `hay4_C`
retomados; a unidade de teste antiga (atol 10⁻⁶, repouso de 3 s) fica suspensa — os parâmetros dela foram superados.

**75. DECISÃO DO USUÁRIO — REABERTURA: REPOUSO CONVERGIDO INVALIDA OS PROTOCOLOS ATIVOS; A ETAPA A NÃO COMEÇA (2026-10-06 21:01;
declarado ANTES de rodar).**
**(1) Registros.** [**(a) CORRIGIDO NO ITEM 76: premissa FALSA — o "não dispara" era artefato do meu código (o CVode pulava o α); sob repouso convergido o CaBurst de 1.5 nA DISPARA.**] ~~(a) O "1 disparo em ~128.5 ms" do CaBurst em todos os vereditos vinha do REPOUSO NÃO CONVERGIDO (3 s;
o real converge em ~21.5 s); com repouso convergido o CaBurst de 1.5 nA não dispara no soma, no L0 nem no reduzido; o
N = 32 se apoiava nisso — **a afirmação "o primeiro N ancorado numa grandeza dendrítica fisiológica" (item 40 b) foi
RISCADA com o motivo.**~~ (b) **A convergência da referência tem TRÊS eixos: espaço (Δ), passo de tempo (dt) e ESTADO
INICIAL (assentamento)** — registrado no princípio do D127. (c) **TOLERÂNCIA ABAIXO DA RESOLUÇÃO:** o teste "+100 ms
depois de convergido" (item 74 C) mediu 5.6×10⁻⁹ mV, ~200× abaixo do que o integrador resolve — um teste abaixo da
resolução do instrumento não carrega informação → **reclassificado NÃO AVALIADO** (extensão da regra da ausência de
avaliação, item 56), não aprovado nem reprovado. Terceira tolerância declarada abaixo da precisão. **REGRA NOVA: medir o
PISO NUMÉRICO do método ANTES de declarar uma tolerância, e declará-la ACIMA dele.** (d) **A regra de dois processos
perdeu o fundamento** (~200 MB por processo; item 61): o limite agora são os NÚCLEOS (4 físicos, 8 linhas).
**(2) REVALIDAR O HAY COMO VERDADE DE BASE — PRIMEIRO (declarado).** Pelo código comum (`stim_common.CommonSim`, repouso
por critério), Hay biophys3 a Δ 1 µm (o do D131/C1–C3), critérios e faixas INALTERADOS: **C1** (−50 pA × 1 s no soma;
razões soma→ponto no caminho apical a 100…600 µm em 1 099 × 99 ms): r100 ∈ [0.6, 1.0], d50 ∈ [250, 450] µm,
r500 ∈ [0.05, 0.52]; **C3** (1.9 nA × 5 ms no soma; amplitude = máx − valor a 49 ms; nos SÍTIOS DO DADO, item 14):
hay_620 ∈ [25, 65] mV, hay_800 ∈ [17.3, 54.7] mV, 1 PA somático (detector de pico) e decrescente de 620 para 800 µm.
**Spike de Ca dendrítico (definição declarada):** no hay_620, pico ≥ −20 mV E V ≥ −40 mV por ≥ 10 ms (o EPSP sozinho do
V2: pico −59.6 mV; o BAC de 3 s: +3.1 mV e 27 ms de meia largura). Protocolos: BAC do Hay (1.9 nA × 5 ms no soma + EPSP
0.5 nA τ 0.5/5 no hay_620 5 ms depois) e EPSP sozinho no hay_620 em amplitudes 1.5, 2, 3, 4, 6, 8 nA → LIMIAR do spike de Ca
dendrítico e do 1º PA somático (menor amplitude da grade que o produz). **Para comparação (registro), os MESMOS protocolos
com o assentamento PUBLICADO do Hay** (código de ModelDB 139653: `init()` em v_init −80 mV e estímulo a 295 ms no BAC — o
"repouso" das figuras é um TRANSITÓRIO de ~300 ms; 700 ms nos degraus, 250 ms na frequência crítica). **Se C1 OU C3
falhar com repouso convergido: a verdade de base cai — PARAR e reportar antes do V2.**
**(3) REFAZER O V2 PELO CÓDIGO COMUM — SÓ DEPOIS DE (2) PASSAR:** todos os protocolos ativos (f-I, BAC, CaBurst, bAP) com
repouso convergido, nós nos pontos de medida (NATIVEX), N = 8, 16, 32, contra o L0 Δ0.5 pelo MESMO código; critérios e
faixas inalterados; o CaBurst entra com o resultado que tiver — sem disparo somático no L0 → critério do 1º PA NÃO
AVALIADO nesse protocolo, não aprovado.
**(4) CHECAGEM DE TOLERÂNCIA 10⁻¹⁰ — em paralelo, a mesma unidade distal, 61 avaliações θ.** **Piso MEDIDO antes de
declarar:** ‖J(10⁻⁶) − J(10⁻⁸)‖₂ = **1.49** (Weyl: nenhum σ_k se move mais que isso por erro numérico) — 9× a estimativa
analítica anterior (0.17); supondo erro ∝ atol, piso(10⁻⁸) ≈ **0.015** e piso(10⁻¹⁰) ≈ **1.5×10⁻⁴**. Já se vê: os dois
menores σ a 10⁻⁸ (0.0077, 0.029) estão no piso de 10⁻⁸ ou perto dele. **Critério (acima do piso):** para cada σ_k com
σ_k(10⁻¹⁰) ≥ 10 × piso(10⁻¹⁰) = 1.5×10⁻³ (os de baixo ficam NÃO AVALIADOS — nem 10⁻¹⁰ os resolve), **10⁻⁸ basta se
|σ_k(10⁻⁸)/σ_k(10⁻¹⁰) − 1| ≤ 10%** para TODOS; também se mede ‖J(10⁻⁸) − J(10⁻¹⁰)‖₂ para conferir a suposição de erro
∝ atol (previsto ≈ 0.015).
**(5) NÚCLEOS:** (2), (3) e (4) em paralelo até os núcleos; faltando núcleo, `pv_C` e `hay4_C` são SUSPENSOS (SIGSTOP).

**76. ERRO MEU NO CÓDIGO COMUM — O "CaBURST NÃO DISPARA SOB REPOUSO CONVERGIDO" ERA ARTEFATO; RESULTADOS DO HAY VÁLIDOS
(2026-10-06 22:41).** **O defeito:** no `CommonSim`, o α é o mecanismo `epsp` do Hay (sem eventos). Quando o α é o ÚNICO
estímulo e começa TARDE (105 ms), nada avisa o CVode; partindo de um equilíbrio PERFEITO (o repouso convergido, todas as
derivadas ~0) ele dá UM passo gigante e PULA o EPSC inteiro — resposta zero. Com um degrau no mesmo protocolo (BAC), os
eventos do play forçam as paradas e o α é pego; com início cedo (1 ms no P4/F; 5 ms na conferência do próprio CommonSim)
o CVode ainda dava passos pequenos — por isso a conferência passava sem cobrir o caso que falhava. **Achado** quando a
varredura do CaBurst deu pico de EXATAMENTE −72.0 mV (o repouso) para 1.5, 2, 3 e 4 nA — fisicamente implausível;
reproduzido num modelo pequeno (α sozinho a 105 ms: resposta zero; com um degrau junto: resposta). **Invalida:** o "0 PA
no CaBurst" do item 74 (G) e do item 75 (no L0 e no reduzido, `results/coer2/`), a varredura do CaBurst da revalidação
convergida (`hay_reval/convergido_bug_alfa.log`) e, com eles, a PREMISSA de que o repouso convergido muda o CaBurst — a
reabertura do N = 32 pelo CaBurst fica SEM BASE até a verificação com o código corrigido. **Não invalida:** C1 e C3 (só
degraus), o BAC (degrau + α), a coerência do EPSP/BAC (α com início a 1 ms; degrau no BAC). **Correção:** (a) um degrau de
AMPLITUDE ZERO no início de cada α cria a descontinuidade (evento do play) que faz o CVode parar ali — testado: α sozinho
a 5 e a 105 ms dá a MESMA resposta, igual à do α com degrau junto; (b) a conferência epsp × play passou a usar início
TARDIO (105 ms) — e PEGOU o defeito na primeira tentativa de correção (`cvode.event` no início do α não bastou: pico 0;
caiu no play, correto). **Lição:** a conferência tem de cobrir o caso de uso (início tardio a partir do equilíbrio), não
um caso cômodo — mesma família do autoteste que precisa poder falhar (item 52).
**INCIDENTE DE MEMÓRIA (21:22):** o kernel ficou SEM MEMÓRIA e o OOM matou processos do VS Code (do usuário); 6.6 de 7.8 GB
de swap em uso. Os processos NEURON somavam ~150 MB residentes + ~800 MB em swap; a memória residente era sobretudo do
navegador (~1.5–2 GB) e do editor (~0.7 GB). A unidade de teste antiga (suspensa, parâmetros superados) foi encerrada.
**Correção do registro do item 75 (1d):** "o limite agora são os núcleos" vale para os processos do reduzido; com o
navegador e o editor abertos, a MEMÓRIA da máquina ainda é o limite — conferir a memória livre antes de cada lançamento.
**RESULTADOS VÁLIDOS DA REVALIDAÇÃO (critérios e faixas inalterados):**
| | C1: r100 / d50 / r500 / Rin | C3: bAP 620 / 800 µm, PA | BAC: spike de Ca no hay_620 |
|---|---|---|---|
| **convergido** (código comum; repouso em 21.5 s) | 0.850 / 350.7 µm / 0.367 / 40.23 MΩ — **PASSA** | 35.07 / 25.34 mV, 1 PA — **PASSA** | SIM (pico 4.7 mV, 29.6 ms ≥ −40) |
| **publicado** (init em −80 mV, protocolo a 295 ms) | 0.851 / 352.2 µm / 0.368 / 42.08 MΩ — PASSA | 36.07 / 26.64 mV, 1 PA — PASSA | SIM (5.8 mV, 30.8 ms) |
**→ O Hay SOBREVIVE como verdade de base com repouso convergido (C1 e C3 passam).** C1/C3 quase iguais aos de 3 s
(item 10: r100 0.8500, d50 350.70, bAP 35.09/25.36). **Protocolo publicado (ModelDB 139653, conferido no código):**
`init()` em v_init −80 mV e estímulo a 295 ms (BAC/CaBurst), 700 ms (degraus), 250 ms (frequência crítica) — os
comportamentos das figuras são de um TRANSITÓRIO de ~0.3–0.7 s após o início. No modo publicado: spike de Ca dendrítico E
1º PA somático já a 1.5 nA (o menor da grade), CaBurst de 1.5 nA → 1 PA (como no artigo). No modo convergido, a varredura
do CaBurst está sendo REFEITA com o código corrigido.

**77. RESULTADOS (2026-10-07 00:30) — CaBURST SOB REPOUSO CONVERGIDO, COM O CÓDIGO CORRIGIDO: DISPARA.** Revalidação
convergida refeita (conferência epsp × play com início TARDIO: 3.1×10⁻⁴ — passa): C1 e C3 idênticos aos do item 76
(PASSAM); BAC: spike de Ca (4.7 mV, 29.6 ms) e PA a 103.08 / 113.35 ms; **EPSP sozinho no hay_620: 1.5 nA → spike de Ca
(6.1 mV, 32.2 ms) + 1 PA somático; 2.0 nA → spike de Ca (26.0 mV) + 2 PA** — o MESMO comportamento do modo publicado
(1.5 nA: 6.8 mV, 1 PA; 2.0 nA: 26.5 mV, 2 PA). **Limiar do spike de Ca dendrítico e do 1º PA somático: ≤ 1.5 nA nos dois
modos** (o menor ponto da grade; abaixo disso não foi varrido). **→ O repouso convergido NÃO muda o CaBurst; o "não
dispara" era só o defeito do item 76.** V2 pelo código comum (nós nos pontos, repouso convergido), já completos no
reduzido: CaBurst 1 PA a **129.95 (N = 8), 128.025 (N = 16), 128.625 ms (N = 32)** — praticamente os de antes (128.025 e
128.6); bAP 34.88/25.07, 35.11/25.41, 35.19/25.47 mV. Falta a referência L0 Δ0.5 pelo mesmo código (assentando) para o
veredito e o N. Checagem de tolerância 10⁻¹⁰: 23 de 61 subpassos.

**78. DECISÃO DO USUÁRIO — TRÊS AJUSTES, SEM INTERROMPER O QUE RODA (2026-10-07 11:15; declarado ANTES de ver o resultado
da checagem de tolerância — a unidade distal a 10⁻¹⁰ terminou, os números NÃO foram olhados).**
**(1) Registros.** (a) A reabertura do CaBurst veio de um DEFEITO (o CVode, partindo do equilíbrio perfeito, pulava o EPSC
tardio); o CaBurst dispara com repouso convergido → **o risco do item 40 b ("o primeiro N ancorado numa grandeza
dendrítica fisiológica") foi DESFEITO** e a nota de que o N "se apoiava num artefato" removida (o histórico fica). (b) **Hay
revalidado com repouso convergido: C1, C3, BAC e CaBurst passam, iguais ao protocolo publicado** (que é um transitório de
~300 ms) — a verdade de base está FIRME; o terceiro eixo da convergência (estado inicial) vale como PRINCÍPIO, com efeito
pequeno aqui. (c) **A falta de memória das 21:22 decorreu da MINHA recomendação de que "o limite agora são os núcleos"**: os
~200 MB eram de uma unidade pequena (o reduzido), não do L0 com 25 000 segmentos. **REGRA: medir a memória POR TIPO DE
PROCESSO e conferir a memória livre antes de cada lançamento** (a conferência já é feita; a medida por tipo passa a ser
gravada pelos próprios scripts — pico de memória residente no fim de cada rodada).
**(2) A CHECAGEM DE TOLERÂNCIA — O OBJETO CERTO, declarado antes do resultado.** As direções fracas da unidade distal são
combinações de canais SOMÁTICOS que uma injeção distal mal enxerga; na Etapa A completa entram as unidades SOMÁTICAS
(M3/M5), que enxergam exatamente essas combinações — uma direção fraca numa unidade distal pode ser bem determinada no
problema inteiro. **A ANÁLISE QUE DECIDE a tolerância é sobre o GRAM COMBINADO** — no mínimo a unidade distal + a unidade
somática (soma das duas JᵀJ) —, o objeto que a Etapa A usa. **Mesmo critério do item 75:** 10⁻⁸ basta se todo σ do Gram
combinado acima de 10× o piso de 10⁻¹⁰ mudar ≤ 10% entre 10⁻⁸ e 10⁻¹⁰; **e também se testa 10⁻⁶** pelo mesmo critério
(se bastar, o custo da Etapa A volta a cair). O piso do Gram combinado é MEDIDO antes de aplicar o critério, do mesmo
jeito que o da unidade distal (‖J(10⁻⁶) − J(10⁻⁸)‖₂ escalado por atol). A análise de UNIDADE ÚNICA continua sendo
REPORTADA, como diagnóstico. **A unidade somática** (injeção no soma: M3 — 1.9 nA × 5 ms lendo os 503 pontos + soma;
M5 — 0.78 / 1.0 / 1.9 nA × 2 s lendo o soma; 61 avaliações θ; MESMO modelo, repouso e gravação das unidades distais) é
calculada nas três tolerâncias (10⁻⁶, 10⁻⁸, 10⁻¹⁰), com a memória conferida antes de lançar. **REGISTRO: a conclusão do
item 74 (H) ("a Etapa A inteira precisa da tolerância apertada") foi tirada de UMA unidade só e fica SUSPENSA até a
análise do Gram combinado.**
**(3) PARADA FORÇADA DO SOLVER PARA TODO ESTÍMULO.** O conserto do EPSC tardio é da mesma família do `Vector.play` depois
do restore: o solver pulando um estímulo. No `CommonSim`, TODO estímulo ganha descontinuidade (evento do play) no início e
no fim; o AUTOTESTE passa a cobrir INÍCIO TARDIO em todos os tipos: a resposta a cada estímulo com início em 10 ms e em
105 ms, a partir do repouso, tem de ser a MESMA forma deslocada no tempo (o sistema está em equilíbrio, é invariante no
tempo) — |Δ| máx ≤ 1% da deflexão (acima do piso numérico; um estímulo pulado erra 100%); falhou → a rodada não começa.

**79. RESULTADOS (2026-10-07) — NOVO N DO V2 PELO CÓDIGO COMUM; PARADA FORÇADA GENERALIZADA.**
**(A) V2 REFEITO PELO CÓDIGO COMUM** (repouso convergido, α corrigido, nós nos pontos — NATIVEX; referência L0 Δ0.5 pelo
MESMO código, `results/v2comum/`; critérios e faixas inalterados; `hay_v2_final.py` com a referência nova):
| N | nível A | nível B | o que reprova o B |
|---|---|---|---|
| 8 | PASSA (pior 1.4%, P5 na ponta apical) | falha | 1º PA 1.500 ms; medidas 1.4% |
| 16 | PASSA (pior 0.46%) | falha | **só o 1º PA do CaBurst, 0.425 ms** |
| 32 | PASSA (pior 0.54%) | **PASSA** | EPSP somático 0.09%; medidas 0.54%; 1º PA 0.175 ms; taxa 0.08% |
**→ Menor N: nível A = 8; nível B = 32. A Etapa A fica em N = 32, agora com veredito sob repouso convergido.** A
referência L0 pelo código comum: bAP 35.07 / 25.34 mV; BAC 103.08 / 113.35 ms; CaBurst 1 PA; f-I 0/5/11/14/16/18/19/20/21/20
— os mesmos números da referência de 3 s (o repouso convergido muda pouco aqui).
**(B) PARADA FORÇADA PARA TODO ESTÍMULO (`stim_common.CommonSim`):** marcador de amplitude ZERO (descontinuidade do play) no
início de CADA estímulo e no fim de cada degrau, qualquer que seja o tipo; **autoteste de INÍCIO TARDIO** (degrau e α, a 10
× 105 ms a partir do repouso; mesma forma deslocada, |Δ| ≤ 1% da deflexão) a cada CommonSim: no modelo de teste passa com
|Δ|/deflexão 3.9×10⁻⁸ (degrau) e 4.6×10⁻⁹ (α); **com a parada forçada desligada (o defeito do item 76 reintroduzido), o
autoteste RECUSA** ("estímulo pulado?") — o autoteste pode falhar.
**(C) Checagem de tolerância (item 78):** unidade distal a 10⁻¹⁰ completa (61/61; números NÃO olhados até a unidade somática
existir); **unidades SOMÁTICAS** (M3 lendo os 503 pontos + soma; M5 no soma) lançadas a 10⁻⁶, 10⁻⁸ e 10⁻¹⁰, mesmo modelo,
repouso e gravação das distais; memória conferida antes de cada lançamento; os scripts passam a gravar o pico de memória.

**80. MEDIDA (2026-10-07 12:05) — CUSTO DA UNIDADE SOMÁTICA; NADA MUDADO.** Primeiro subpasso (base) a 10⁻⁶: repouso 84 s,
M3 ~2 min, **M5 30 min** (3 degraus × 2.3 s com disparo, modelo de ~47 mil estados, CVode); total **~32 min por subpasso**.
A 10⁻⁸ o M5 do subpasso base passa de 40 min sem terminar (10⁻¹⁰ idem). Projeção com 61 subpassos e 1 processo por
tolerância: 10⁻⁶ ≈ 32 h; 10⁻⁸ ≥ 43 h; 10⁻¹⁰ maior (a medir). Memória por processo (tipo "unidade somática"): RSS 37–68 MB +
swap 18–29 MB → ~70–100 MB. Máquina: 8 núcleos, carga ~4.4; memória disponível 420–860 MB (o resto é navegador/editor),
swap ~5 GB em uso. **Nenhuma alteração feita** (regra: reportar o custo antes de mudar); a decisão de tolerância segue
NÃO AVALIADA até o Gram combinado existir. pv_C/hay4_C: não existem mais (a máquina reiniciou às 09:16 de hoje); não relançados.

**81. DECLARAÇÕES ANTES DO RESULTADO (2026-10-07 12:50) — PARALELIZAR OS SUBPASSOS DA CHECAGEM DE TOLERÂNCIA COM PORTÃO DE
MEMÓRIA (pedido do usuário).**
**(1) Memória — causa da queda, medida ANTES de acrescentar processos** (`mem_sample.py`, 30 min, a cada 60 s,
`results/memoria/amostra_1.tsv`): RSS + swap de CADA processo de simulação estável em ~70–90 MB (as páginas só trocam
entre RAM e swap; nenhuma subida monotônica — **sem sinal de vazamento em ~30 min, ~1 subpasso por processo**: evidência
fraca, por isso fica uma amostragem longa a cada 5 min, `amostra_longa.tsv`, até 48 h). Memória disponível sem tendência
(709–1 448 MB, ruído). **Causa da oscilação e da troca: o navegador** — grupo firefox 5.9–6.7 GB (RSS + swap) oscilando
~550 MB em 2 min; faltas maiores de página em 60 s: firefox **~1 900/s**, simulações 0.1/s, editor 0.8/s. Swap-in médio
265 páginas/s, rajadas até 2 677. Fechar o navegador é decisão do Martel.
**REGRA DE LANÇAMENTO DECLARADA (`mem_gate.py`, aplicada a TODO lançamento novo, inclusive verificações):** lança só se
(a) MemAvailable − orçamento do processo ≥ **piso 600 MB** (reserva para a oscilação do navegador) e (b) swap-in
(janela 60 s) ≤ **50 páginas/s**; orçamento por tipo = **250 MB** (pico medido ~80 MB na unidade somática, ~220 MB no
levantamento 64D, com folga). Fila (`mem_gate.py fila`): lança um por vez, reconfere a cada 5 min, e PAUSA novos
lançamentos enquanto o portão estiver fechado (nada em curso é parado); grava o PID REAL de cada lançamento.
LIÇÃO DE PROCESSO: o PID gravado com `$!` depois de `setsid nohup` era o do invólucro (que bifurca) — o amostrador agora
grava o próprio PID; os PIDs das simulações já eram gravados pelo próprio processo.
**(2) Paralelizar — `etapaA_runner.py --sub-worker k/K`** (subpassos de índice ≡ k mod K; cada um parte do mesmo
repouso e grava seu arquivo; a redução da unidade é gravada por quem achar todos prontos) **e `--de-tras`** (ajudante de
um serial JÁ EM CURSO, sem interrompê-lo: do fim para o começo, trava exclusiva por subpasso com PID, pula o que o serial
está fazendo; no encontro, no máximo um subpasso por ajudante feito em dobro — o serial antigo não lê travas). Lógica
conferida no modelo de brinquedo: 3 sub-workers e serial + 2 ajudantes simultâneos × serial — 171 de 171 arranjos
idênticos, nenhuma trava órfã. **VERIFICAÇÃO NO MODELO REAL, critério declarado: subpassos `base` e `g_pas_soma_mais` da
unidade somática a 10⁻⁶ pelo caminho paralelo (`--sub-worker 0/2` e `1/2`, cada subpasso o PRIMEIRO do seu processo; no
serial, `g_pas_soma_mais` veio depois de `base`) × o serial `soma_atol1e-6`: M3 e M5 IDÊNTICOS BIT A BIT**
(`etapaA_par_check.py`); qualquer diferença ou arquivo ausente → não confiar (NÃO AVALIADO). Só com IDÊNTICO os
ajudantes entram nas três checagens, pela fila com portão, na ordem do caminho crítico (10⁻¹⁰ primeiro).
**(3) Projeção refeita com o custo MEDIDO** (protocolos por avaliação; repouso guardado, como na Etapa A; medidas sob a
disputa de 3–4 processos e do navegador): unidade distal 132 / 181 / 228 s por subpasso a 10⁻⁶ / 10⁻⁸ / 10⁻¹⁰ →
4.6 / 6.3 / 7.9 h por unidade (125 subpassos); **parte somática 34 / 50 / 78 min por avaliação → 71 / 104 / 162 h**
(o levantamento 64D dizia ~14 min e ~30 h: subestimada **2.4× / 3.6× / 5.6×**). Total (unidades + somática + G 25 h + viés
75 h × razão distal + assentamentos 5 h):
| s\* | unidades | 10⁻⁶ | 10⁻⁸ | 10⁻¹⁰ |
|---|---|---|---|---|
| 400 | 20 | 268 h (11 dias-CPU) | 363 h (15) | 480 h (20) |
| 200 | 51 | 410 h (17) | 558 h (23) | 725 h (30) |
| 100 | 119 | 722 h (30) | 985 h (41) | 1 264 h (53) |
| 50 | 249 | 1 317 h (55) | 1 802 h (75) | 2 293 h (96) |
| 25 | 503 | 2 482 h (103) | 3 398 h (142) | 4 304 h (179) |
ESTIMATIVA: G e viés não remedidos (viés escalado pela razão distal). A parte somática é UMA unidade de 125 avaliações
independentes — paraleliza por subpasso; a maior unidade distal limita o relógio fora (~8 h a 10⁻¹⁰).
**Checagem de tolerância (61 subpassos, serial):** 10⁻⁶ ~37 h; 10⁻⁸ ~53 h; **10⁻¹⁰ ~80 h (caminho crítico)**.
**(4) pv_C/hay4_C:** perdidos no reinício das 09:16; fora do caminho crítico; relançar a partir do progresso gravado
quando houver vaga no portão.

**82. RESULTADOS (2026-10-07 13:45) — VERIFICAÇÃO PARALELO × SERIAL; AJUDANTES LANÇADOS PELO PORTÃO.**
**(A) Paralelo × serial (critério do item 81 (2)): IDÊNTICO BIT A BIT** — `base` e `g_pas_soma_mais` da unidade somática a
10⁻⁶ pelo caminho `--sub-worker 0/2` / `1/2` (cada um o primeiro subpasso do seu processo) × o serial: M3 (504 × 1 501) e M5
(3 × 23 001), float32, máx |Δ| = 0, mesmos bytes, nos quatro. O subpasso não herda estado do anterior no processo.
Pico de memória MEDIDO, tipo "unidade somática": **82 e 95 MB** (ru_maxrss) — o orçamento de 250 MB cobre com folga.
Verificação lançada pelo portão (12:43 e 12:49: disponível 1 041 / 1 158 MB, swap-in 10 / 18 pg/s).
**(B) Ajudantes (`--de-tras`, fila com portão, `results/etapaA_rec/FILA_AJUDANTES`), ordem do caminho crítico:** 10⁻¹⁰,
10⁻¹⁰, 10⁻⁸, 10⁻⁶ (no máximo 4 → 7 simulações em 8 núcleos). O 1º entrou às 13:42 (disponível 969 MB, swap-in 8 pg/s) e
reivindicou o último subpasso (`basal_Ih_menos`); os demais entram só com o portão aberto. Projeção da checagem COM os 4:
10⁻¹⁰ ~59 × 79 min / 3 ≈ 26 h; 10⁻⁸ ~60 × 52 / 2 ≈ 26 h; 10⁻⁶ ~58 × 36 / 2 ≈ 17 h (ESTIMATIVA — mais processos podem
deixar cada um mais lento; o portão pode segurar ajudantes) → **Gram combinado ~amanhã (08/10) à tarde**.
**(C) Referências:** `ref_ii_axon.py` não grava progresso parcial — pv_C (só os limiares somáticos estavam no log) e
hay4_C (só o autoteste) recomeçam do zero quando houver vaga no portão.

**83. DOIS AJUSTES (pedido do usuário, 2026-10-07 noite) + CORREÇÕES DE PROJEÇÃO.**
**(1) pv_C / hay4_C PELO RUNNER DA ETAPA A** (`ref_ii_C.py`; construção das células num caminho só, `ref_ii_cells.py`;
a tarefa C do `ref_ii_axon.py` agora remete ao runner). Unidade = a célula; subpassos EM ORDEM: `Ap`, `Aa` (bissecções;
cada sonda guardada em `sondas.json` por escrita atômica → a retomada repete a mesma trajetória sem resimular), `tpk`,
74 cenários (S1/S2/S3, rng 12345), 4 do controle negativo (célula passiva). **Declarado antes de rodar: a simulação passa
ao código ÚNICO `CommonSim`** (repouso convergido, parada forçada, autoteste de início tardio) em vez do `Injector` com
repouso fixo de 2 s — pv_A/pv_B/hay3_* ficam como estão (código anterior, registrados). **TESTE DE RETOMADA declarado**
(`ref_ii_C_retomada.py`, célula pequena toyC, MESMO código): rodada inteira × a mesma morta com SIGKILL (PID gravado pelo
runner) no meio da bissecção, no meio dos cenários e depois de a célula virar passiva, relançada a cada vez; critério:
JSON igual e todos os subpassos idênticos bit a bit; ponto de morte não atingido → NÃO AVALIADO. **Estado: NA FILA atrás
do portão** (fechado desde 21:31 — memória abaixo do piso e swap-in alto) → NÃO AVALIADO por enquanto. Relançar pv_C e
hay4_C só depois da checagem de tolerância e com o portão; orçamento de memória do tipo "ref" PROVISÓRIO 1 500 MB até a
medida (rodada só de construção + repouso, pico ru_maxrss).
**(2) A MÁQUINA TEM 4 NÚCLEOS FÍSICOS** (i5-8250U; os 8 são hyperthreading; ~2.6 GHz com todos ocupados). MEDIDO nos
subpassos somáticos: 3 processos → velocidade 1.0 cada; 5 → ~0.8; **7 → ~0.44 (10⁻⁶ 75 min, 10⁻⁸ 110, 10⁻¹⁰ 174 por
subpasso, contra 32 / 52 / 79)** — vazão 3.0 / ~4.0 / ~3.1: com 7 processos os ajudantes quase não rendiam. **Ação
(21:32): SUSPENSOS (SIGSTOP, PID gravado) o 2º ajudante de 10⁻¹⁰ e o de 10⁻⁶ → 5 rodando.** Portão ganha a regra (c):
**no máximo 5 simulações pesadas rodando** (suspensas não contam; tipo toy isento). `etapaA_tol_vigia.py` rebalanceia
pelo PID gravado (10⁻⁸ completa → retoma o ajudante de 10⁻¹⁰; 10⁻⁶ completa → encerra o ajudante de 10⁻⁶, redundante) e
roda o Gram combinado quando as três terminarem. **CORREÇÃO da projeção do item 82 (erro de conta: 53 × 99 / 2 = 44 h, não
26):** ~10 470 processo-min restantes a 5 processos → **≥ 35 h a partir de 21:32 → o Gram combinado fica para 09/10 de
manhã, não 08/10 à tarde.**
**(3) MEMÓRIA:** amostragem longa (9.3 h, ~10 subpassos por processo): as simulações NÃO vazam (RSS + swap ~80 MB, plano).
Disponível caiu de ~1.1 GB para ~0.54 GB: ~340 MB são os 4 ajudantes (dentro do orçamento), o resto principalmente o
navegador (~+400 MB); swap-in médio subiu de 166 para 917 páginas/s (troca ativa do navegador); swap livre ~1.8 GB, caindo.
Fechar o navegador é decisão do Martel.
**(4) PLANO DA ETAPA A — EXECUÇÃO LOCAL POR ESPAÇAMENTO GROSSO** (`etapaA_fila.py`; avaliação `etapaA_sstar.py`).
Estágios 400 → 200 → 100 µm locais; cada estágio lança só os pontos NOVOS (os anteriores são reaproveitados — subconjunto
exato), o viés de cada ponto e, no 1º, a unidade somática (a mais longa, primeiro; ajudantes no fim), o G com f-I e o termo
direto do viés; tudo pelo portão. **Fim de estágio → AVALIAÇÃO pelo critério JÁ DECLARADO (item 13 + 26): BASTA ⇔ F
identificável (‖G·V₀‖ ≤ 10⁻³‖G‖, V₀ = σ < 10⁻⁶σ_max) E o viés sozinho cabe em toda grandeza com tolerância (EPSP 5%,
1º PA 1 ms, taxa 2%; picos de Ca sem tolerância → só reportados). BASTA → s* = s, para; NÃO BASTA → desce; NÃO AVALIADO
(qualquer entrada faltando, inclusive a taxa f-I no G) → para, nunca desce nem aprova.** Abaixo de 100 µm a fila NÃO
desce: grava DECISAO_NUVEM_PENDENTE (a nuvem só entra se o s* exigir espaçamento fino; decisão do Martel).
Autotestes que PODEM falhar: critério (5 casos sintéticos; 2 mutações — identificabilidade e viés desligados — recusadas);
fila (5 cenários com trabalhos falsos: s* = 200; parada na decisão da nuvem; viés que falha para sem descer; G sem taxa →
NÃO AVALIADO; sem PORTE_OK → nada lançado; 2 mutações — descer em NÃO AVALIADO, descer abaixo de 100 µm — recusadas).
**Custo refeito para 4 núcleos (vazão ~4 processos-equivalentes):** s = 400 ≈ 11 / 15 / 20 dias-CPU (10⁻⁶ / 10⁻⁸ /
10⁻¹⁰) → **~3 / ~4 / ~5 dias de relógio** (não 2–3); descer a 200 acrescenta só as 31 unidades novas (~2–3 dias);
a 100, +68 (~4–6 dias). ESTIMATIVA, mais o repouso convergido por perturbação (a medir no porte).
**PRÉ-REQUISITOS DUROS da fila (faltam todos; sem eles nada é lançado):** TOLERANCIA (o Gram combinado);
**PORTE_OK** — a unidade da Etapa A ainda usa repouso próprio (3 s a passo fixo) e laço próprio; tem de passar ao
`CommonSim` (repouso convergido guardado por perturbação, parada forçada) e ser verificada; a REDUÇÃO da unidade
somática (M3/M5 em blocos por leitura) ainda não existe; **G_OK** — o G atual tem 52 grandezas, SEM a taxa f-I; **VIES_OK**
— o viés por ponto (Hay L0 nos mesmos protocolos → JᵀΔy por leitura) e o termo direto ainda não têm código.

**84. DECISÃO DO USUÁRIO — PREMISSA CONFIRMADA E DECLARAÇÃO ANTES DO RESULTADO DA TOLERÂNCIA (2026-10-07 22:17; o Gram
combinado ainda NÃO existe — `tol_gram_combinado.txt` ausente).**
**(1) PREMISSA (conferida no código e nos tempos de lançamento):** TODAS as unidades da checagem de tolerância — a
distal a 10⁻⁶ (05/10), 10⁻⁸ (06/10) e 10⁻¹⁰ (06–07/10) e as somáticas (serial + ajudantes, 07/10) — usam o **REPOUSO
FIXO DE 3 s** do código antigo da Etapa A (`EtapaAUnit._rest`: passo fixo 0.1 ms a partir de v_init −80 mV, 3 000 ms) e o
laço PRÓPRIO (`_run`), NÃO o `CommonSim`.
**(2) DECLARADO AGORA:** o repouso real converge em ~21.5 s; nas diferenças finitas, θ e θ+h partem cada um de um repouso
de 3 s ainda derivando, e o Jacobiano inclui a derivada dessa deriva em θ — sinal pequeno, mas as direções fracas são
feitas de sinais pequenos, e a Etapa A final usa repouso CONVERGIDO. **A decisão de tolerância que sair do Gram combinado
só VALE depois de CONFIRMADA na unidade migrada para o CommonSim.** A checagem NÃO é parada.
**CONFIRMAÇÃO (junto da verificação do pré-requisito 1):** a unidade DISTAL migrada (mesmo ponto, 61 avaliações θ) na
tolerância decidida X e na seguinte mais apertada X/100; menores valores singulares comparados com os da unidade ANTIGA.
**Critério:** para todo σ acima de 10× o piso (piso em X = ‖J_migr(X) − J_migr(X/100)‖₂, medido na migrada), |σ_migr(X) /
σ_antiga(X) − 1| ≤ 10% → a decisão TRANSFERE; senão, a checagem de tolerância é REFEITA na unidade migrada.
**(3) REGISTRADO:** 4 núcleos físicos (não 8); 5 processos dão a maior vazão medida (~4.0, contra 3.0 com 3 e ~3.1 com 7)
— **mantém-se 5**. Estimativa local da Etapa A refeita: s = 400 µm ≈ **3 / 4 / 5 dias** de relógio a 10⁻⁶ / 10⁻⁸ / 10⁻¹⁰.

**85. OS QUATRO PRÉ-REQUISITOS DA ETAPA A — ESCRITOS; VERIFICAÇÕES DECLARADAS E NA FILA ATRÁS DO PORTÃO (2026-10-07 22:31).**
Nenhuma verificação rodou ainda: o portão está fechado (5 simulações da checagem de tolerância; swap-in do navegador) →
todas **NÃO AVALIADAS** até rodarem. Critérios declarados ANTES:
**(1) Unidade no CommonSim** (`etapaA_unit.py` reescrita; a antiga guardada só como registro): repouso CONVERGIDO pelo
`CommonSim` (construído na 1ª avaliação, com os autotestes de código; a cada subpasso `resettle` — repouso guardado pela
chave automática, compartilhado entre unidades e processos, e conferência de deriva ≤ 0.01 mV em 1 ms), laço comum
(`CommonSim.run`: play + parada forçada), DOIS modelos no mesmo código ('region' e 'hay' = Hay L0 Δ 0.5 µm). Mudança no
`stim_common` (código comum): `resettle`, grampos criados antes do assentamento, e a chave do repouso passa a contar só
os pontos de processo que INJETAM no repouso (amp ≠ 0) — os grampos de amplitude zero faziam a chave depender da história
do processo (regressão `stim_common_check toy`: T1 e T3 seguem recusadas, a correta passa).
**VERIFICAÇÃO (`etapaA_porte_check.py`): com o MESMO repouso (o de 3 s refeito), o caminho novo reproduz os traços
GRAVADOS pelo antigo no subpasso base da unidade distal: máx |Δ| ≤ 10 × piso(X), piso(X) = máx |y_antigo(X) −
y_antigo(X/100)|, em X = 10⁻⁶ e 10⁻⁸, por família (M1, M4).** O repouso convergido × antigo sai como diagnóstico.
A CONFIRMAÇÃO do item 84 (`etapaA_conf_check.py`, Grams acumulados por pedaços — o J inteiro tem ~1.2×10⁷ linhas) roda
quando houver a tolerância decidida X: unidade distal migrada em X e X/100 × a antiga em X.
**(2) Redução da unidade somática** (M3 em blocos por leitura + M5@soma; com JᵀX dos subpassos extras e JᵀΔy do viés).
**VERIFICAÇÃO (`etapaA_soma_reduce_check.py`): bloco × traço nas leituras de s = 400 µm (+ soma, + M5@soma), |A − B| /
|B| ≤ 10⁻¹²** — nos dados da unidade somática a 10⁻⁶ da checagem quando ela completar (só numpy).
**(3) G com a taxa da f-I** (`etapaA_G.py`; F pela função ÚNICA `etapaA_F.fvec`, a mesma do termo direto do viés):
taxa_0.78, taxa_1.0, taxa_1.9; **condicionamento declarado: grandeza de PA (1º PA, taxa) só é condicionada se a contagem
for a MESMA em θ, θ+h e θ−h para os 30 parâmetros** — senão `condicionado = False` e a avaliação do espaçamento dá NÃO
AVALIADO nela (autoteste do critério com o caso; mutação "condicionamento ignorado" recusada). **VERIFICAÇÃO
(`etapaA_G_check.py`): (1) as três taxas presentes e finitas; (2) contagens iguais no par soma_SK_E2 ±; (3) coluna finita;
(4) base de novo depois do resettle IDÊNTICA bit a bit.**
**(4) Viés por ponto pelo MESMO código** (unidade 'hay' ou '--referencia' → só 'base'; a redução da unidade 'region' ESPERA
os traços da referência e grava JᵀΔy por leitura — os brutos só vivem até a redução) e **termo direto** F_Hay − F_red
(`etapaA_vies_F.py`, mesma `functional_set` + `fvec`, F_red = o F0 do G no mesmo atol). **VERIFICAÇÃO
(`etapaA_vies_check.py`): (i) nulo por ponto — referência = o próprio modelo direto → base idêntica bit a bit (JᵀΔy = 0);
(ii) nulo do termo direto → dF = 0 exato; (iii) Hay L0 num ponto pelo mesmo código: roda, finito, MEDE memória/tempo (o
orçamento do tipo "hay" sai daí; até lá 1 500 MB provisório); (iv) controle positivo (com a unidade migrada em X):
referência = g_pas_apical × 1.02 → δlog recuperado dentro de 10% de log 1.02.**
**Fila e avaliação atualizadas:** a avaliação do espaçamento (`etapaA_sstar.py`) exige nomes do termo direto = nomes do G e
honra o condicionamento; teste da fila (5 cenários) e autoteste do critério (7 casos) passam; mutações recusadas.
**LIÇÃO DE PROCESSO:** rodei a regressão `stim_common_check toy` (3 s, ~40 MB) com o portão dizendo NÃO LANÇAR (encadeei com
`;`). Desde então toda conferência do portão é `|| exit` — o portão fechado PARA o comando. O supervisor `etapaA_tol_vigia`
era contado como simulação (6 em vez de 5) — excluído.

**86. INSTRUÇÃO CONDICIONAL DO USUÁRIO (2026-10-07 23:12; plano sem mudanças).** SE a tolerância decidida pelo Gram combinado for
**10⁻¹⁰**: ANTES de rodar a confirmação do item 84 a 10⁻¹² (a "seguinte mais apertada"), **medir o custo de UM subpasso a
10⁻¹²** (unidade distal migrada, mesmo ponto) e REPORTAR. **A confirmação completa NÃO é lançada sem esse número.** Se for
inviável, trazer as OPÇÕES antes de qualquer mudança no critério declarado no item 84 (o critério não muda sozinho).

**87. DECISÃO DO USUÁRIO — PREEMPÇÃO: VERIFICAÇÕES CURTAS DOS PRÉ-REQUISITOS ANTES DE UM AJUDANTE DA TOLERÂNCIA (2026-10-08 08:45).**
**Estado do portão às 08:41:** o navegador foi fechado à noite mas **foi REABERTO às ~08:27** (processos com 14–15 min) e
já ocupa ~4.3 GB RSS + ~1.4 GB swap; disponível 960–1 700 MB; swap-in 90–1 220 páginas/s (vmstat: rajadas de ~13 MB/s)
→ portão FECHADO por memória/swap-in, além do limite de 5 simulações. Swap usado caiu de ~5.9 para ~3.4 GB durante a noite.
**Preempção (`preempcao.py`):** suspende (SIGSTOP, PID gravado, comando conferido) o ajudante de **10⁻⁸** (pid 59204;
10⁻⁸ está em 29/61, 10⁻¹⁰ em 20/61 — o 10⁻¹⁰ é o caminho crítico e fica com os dois processos) SÓ quando a parte de
memória do portão passa para o próximo trabalho; cada trabalho passa pelo portão completo; um por vez, na ordem do usuário
(1) porte → (4) nulos do viés e Hay L0 num ponto → (3) G com f-I → nulo do termo direto; um trabalho barrado por memória
(o Hay L0, 1 500 MB provisório) não trava os seguintes; sem nada que caiba, o ajudante é RETOMADO; no fim, SIGCONT (ou
SIGTERM, se a unidade de 10⁻⁸ já tiver completado — trabalho redundante). As duas filas de verificação anteriores
(nada lançado) foram encerradas pelo PID gravado. A (2) (redução somática, só numpy) roda quando a unidade somática a
10⁻⁶ completar.

**88. RESULTADO (2026-10-08 10:30) — VERIFICAÇÃO DO PORTE (pré-requisito 1): NÃO CONFERE pelo critério declarado; causa localizada.**
Lançada pela preempção às 09:17 (portão: disponível 1 062 MB, swap-in 5 pg/s; ajudante de 10⁻⁸ suspenso). Construção do
CommonSim no modelo da unidade: **2 176 s** (repouso convergido em 21 600 ms simulados, ~16 min; autotestes de código ~20
min — α por epsp aprovado); pico **236 MB**. Resultado, máx |novo − antigo| com o MESMO repouso de 3 s:
| X | M1 (piso) | M1 mesmo repouso | M4 (piso) | M4 mesmo repouso |
|---|---|---|---|---|
| 10⁻⁶ | 3.05×10⁻⁵ mV | **0.25 mV (8 193×) FALHA** | 3.3×10⁻⁴ | 2.6×10⁻⁴ (0.8×) PASSA |
| 10⁻⁸ | 1.53×10⁻⁵ mV | **0.25 mV (16 386×) FALHA** | 1.5×10⁻⁵ | 1.5×10⁻⁵ (1.0×) PASSA |
**→ PORTE NÃO CONFERE (critério do item 85, sem alargar).** **Diagnóstico:** a falha está numa ÚNICA leitura de 504 — o
PRÓPRIO ponto de injeção (leitura 378), que é um nó de FIM DE SEÇÃO (área zero, sem capacitância): ali a voltagem SALTA
I·R no instante do degrau (0.05 nA × 2.5 MΩ = 0.125 mV). O caminho ANTIGO (IClamp direto) gravou no instante da borda
(t = 100.0 e 1 100.0 ms) o valor DEPOIS do salto e usou a amostra de t = 100.0 como LINHA DE BASE → o traço inteiro nessa
leitura ficou deslocado 0.125 mV (Δ = −0.125 antes, −0.25 em t = 1 100.0); o caminho NOVO grava o valor ANTES do salto
(linha de base = repouso). Nas outras 503 leituras, novo × antigo = **0.5–1.5× o piso** nas duas tolerâncias e nos dois
sinais. Diagnóstico (não decide): repouso convergido × antigo fora da leitura 378 = 3.4×10⁻⁴ mV (11–22× o piso) — o efeito
da deriva do repouso de 3 s, o objeto da confirmação do item 84.
**Consequência para os dados ANTIGOS:** a unidade distal da checagem de tolerância tem esse deslocamento na leitura do ponto
de injeção, no M1, em TODO subpasso; o tamanho do salto depende de θ (R axial local: Ra, diâmetros) → componente espúria
no J antigo nessa leitura. É determinística (a mesma nas três tolerâncias) — não distorce a COMPARAÇÃO entre tolerâncias da
mesma forma que o ruído, mas muda o OBJETO; a confirmação do item 84 (antiga × migrada) a inclui.
**Decisão pendente (do Martel):** o critério declarado falhou; a causa é a convenção de amostragem na borda de um
estímulo num nó sem capacitância. Opções na resposta. **Orçamento de memória do tipo "distal" no portão: 250 → 500 MB**
(pico medido 236 MB × ~2; a unidade migrada pesa mais que a antiga por causa do CommonSim e dos 504 vetores de gravação).

**89. DECISÃO DO USUÁRIO (2026-10-08 11:39) — RE-BASELINIZAÇÃO APROVADA COMO TESTE DO MECANISMO; DUAS DECLARAÇÕES ANTES DE RESULTADOS.**
**(1) REDEFINIÇÃO APÓS O RESULTADO (rotulada).** Justificativa independente do resultado: linha de base definida no
INSTANTE de uma descontinuidade é mal posta (depende de o amostrador ver antes ou depois do salto); a definição sem
ambiguidade é a ÚLTIMA AMOSTRA ANTES DO ESTÍMULO (t = delay − 0.1 ms). **Condição que a torna TESTE:** re-baselinizados os
dois lados a partir dos arquivos gravados, a concordância novo × antigo tem de ficar no nível do piso em TODAS as 504
leituras, INCLUSIVE a de injeção; sobrando discrepância → a explicação estava incompleta: reportar, não seguir.
**Conferir a conta:** salto I·R = 0.125 mV × diferença medida 0.25 mV — de onde vem o fator 2. Corrigir o código novo
(linha de base na amostra pré-estímulo, em todos os protocolos) e REFAZER a checagem do porte, critério inalterado (o lado
antigo re-baselinizado da mesma forma, pela redefinição aprovada).
**(2) DECLARADO ANTES DO GRAM COMBINADO — a leitura de injeção nos dados antigos:** o deslocamento na leitura de injeção
(M1, todo subpasso, dependente de θ pela resistência axial) é componente ESPÚRIA no J antigo — igual nas três tolerâncias,
mas pode INFLAR alguma direção. Os blocos são por leitura: **o veredito de tolerância roda COM e SEM a leitura de injeção
(linha do ponto de injeção no M1; o M4 no ponto é α contínuo e passou no porte — fica). Mesmo veredito → o defeito não
importa para a decisão (registrar). Veredito diferente → VALE A VERSÃO SEM a leitura** (a que corresponde ao objeto
migrado). **Confirmação do item 84: antiga × migrada COM e SEM a leitura de injeção** (separa o efeito do salto do efeito
do repouso convergido).
**(3) TRABALHADORES DE VIDA LONGA NA ETAPA A:** a construção custa ~36 min por processo (16 de repouso + 20 de autotestes);
um processo por unidade daria ~16 dias-CPU só de sobrecarga. Cada trabalhador constrói UMA vez e PUXA várias unidades da
fila (reivindicação por trava); o repouso por perturbação segue no cache compartilhado. **Verificação:** uma unidade
rodada no SEGUNDO turno de um trabalhador dá resultado IDÊNTICO (bit a bit) à rodada num processo novo.

**90. RESULTADOS (2026-10-08 11:48) — RE-BASELINIZAÇÃO: O TESTE NÃO PASSA (sobra discrepância); FATOR 2 NÃO É O DOS DOIS SINAIS;
itens (2) e (3) do item 89 escritos.**
**(1) Re-baselinização (dos arquivos gravados, os dois lados e o piso na amostra pré-estímulo — M1 t = 99.9 ms, M4 t =
4.9 ms):** M4 concorda no piso (0.8× e 2.0×); **M1 NÃO: sobra 0.125 mV na leitura de injeção (4 096× / 8 193× o piso)
→ pela condição declarada, a explicação estava INCOMPLETA: reportado, NÃO seguido (código não corrigido, porte não
refeito).** Localização exata do que sobra: SÓ DUAS AMOSTRAS da leitura de injeção — os INSTANTES das descontinuidades
(t = 100.0 e 1 100.0 ms), nas duas tolerâncias e nos dois sinais; fora delas, a leitura de injeção concorda a 0.5–0.8× o
piso e as outras 503 leituras em todo instante. A amostra NO instante do salto é ela mesma mal posta (o antigo grava o
valor depois do salto, o novo o de antes): a re-baselinização tirou o deslocamento da linha de base, não essas amostras.
**Conta do fator 2:** NÃO vem dos dois sinais do degrau — cada sinal sozinho dá 0.25 mV em t = 1 100.0: +0.125 do
deslocamento da linha de base (tomada depois do salto de ligar) + 0.125 da amostra no instante de desligar (o antigo
grava depois do salto, o novo antes). Salto medido no dado antigo: −0.1250 (ligar) e +0.1250 (desligar) no M1m; sinais
opostos no M1p; R = 0.125 mV / 0.05 nA = 2.5 MΩ (inferido do dado; o R axial calculado da geometria ainda NÃO foi conferido).
Somática antiga sem o defeito (soma(0.5) tem área: maior salto na borda 7.6×10⁻⁶ mV).
**(2) Escrito** (`etapaA_tol_gram.py`): veredito COM e SEM a linha de injeção do M1 (índice achado pelo NOME na grade e
conferido no DADO: a única leitura com salto > 10⁻³ mV na borda — 378 nas três tolerâncias; a 2ª maior, 7.6×10⁻⁶) e a
regra declarada (mesmo veredito → não importa; diferente → vale o SEM); também corrigido: o veredito era gravado fora do
laço por tolerância e não tratava "nenhum σ acima de 10× o piso" (→ NÃO AVALIADO). `etapaA_conf_check.py`: antiga ×
migrada COM e SEM a leitura de injeção.
**(3) Escrito** (`etapaA_runner.py --fila-unidades`, `run_queue`): trabalhador constrói uma vez e puxa unidades por
trava (PID; trava órfã retomada); redução sem a referência do viés é ADIADA (o trabalhador não bloqueia). Brinquedo: 2
trabalhadores simultâneos dividiram 3 unidades (1 + 2), 27 subpassos sem duplicata, 171/171 arranjos idênticos ao serial.
Verificação no modelo real (`etapaA_worker_check.py`: 2º turno × processo novo, bit a bit) na fila da preempção, depois
dos testes nulos (o processo novo é o do teste nulo). O porte refeito AGUARDA a decisão do item (1).

**91. DECISÃO DO USUÁRIO (2026-10-08 11:54) — AMOSTRAS NOS INSTANTES DE SALTO: EXCLUIR, PELA REGRA DE BLOQUEIO JÁ REGISTRADA.**
**A exclusão APLICA UMA REGRA ANTERIOR** (D132 itens 51–52, cadeia de medida → P24/P28/P54: BLOQUEIO DO REGISTRO NAS
JANELAS DE ESTÍMULO, com a MESMA janela no traço do modelo — decidido por causa dos artefatos que o elemento produz ao
estimular, ANTES deste resultado); as amostras no instante exato de um salto caem dentro de qualquer janela de bloqueio.
**A re-baselinização funcionou como TESTE:** achou a segunda metade do mecanismo (a amostra no instante do DESLIGAMENTO).
**Aplicado agora — a parte mínima e independente de convenção:** (a) linha de base na ÚLTIMA amostra ANTES do estímulo;
(b) EXCLUÍDAS as amostras nos INSTANTES DE DESCONTINUIDADE do estímulo (salto no VALOR da corrente: ligar e desligar de
cada degrau — M1 t = 100.0 e 1 100.0; M3 50.0 e 55.0; M5 150.0 e 2 150.0 ms; o α do M4 é contínuo em valor → nada a
excluir), nos DOIS lados de toda comparação E no JACOBIANO (o objeto da Etapa A inclui a cadeia de medida).
**Declarado agora, antes do Gram combinado:** a análise de tolerância aplica a MESMA regra aos dados ANTIGOS (linha de
base pré-estímulo recalculada dos arquivos + exclusão das amostras de descontinuidade, nas unidades distal e somática),
e mantém o COM/SEM leitura de injeção do item 89 (2) por cima. Idem na confirmação do item 84.
**PENDÊNCIA:** a janela de bloqueio COMPLETA (duração derivada da resposta do filtro da cadeia) entra quando a emulação da
cadeia existir (P24/P28).
**Fechar o mecanismo de forma independente:** R no nó de injeção calculado da GEOMETRIA e do passivo do modelo (resistências
axiais do nó de área zero aos nós vizinhos com capacitância, em paralelo — NEURON `ri()`); tem de dar 2.5 MΩ (0.125 mV /
0.05 nA); se não bater, a explicação segue incompleta — reportar.
**Código novo:** linha de base pré-estímulo + exclusão na redução; **porte refeito, critério inalterado**, mesma exclusão
nos dois lados. O teste "2º turno × processo novo" segue válido (mesmo código dos dois lados).
**FIDELIDADE (registrado, não consertar agora):** o salto instantâneo existe porque a injeção está num NÓ DE ÁREA ZERO
(ponta de seção); um eletrodo real injeta em MEMBRANA, com capacitância — a tensão sobe rápido, mas contínua. Com o
bloqueio, o artefato não entra nas medidas. **Refinamento possível:** injetar e ler em nós COM área (centro de segmento),
mantendo a convergência de segunda ordem.

**92. RESULTADOS (2026-10-08 12:53) — MECANISMO FECHADO PELA GEOMETRIA; PORTE REFEITO: CONFERE (pré-requisito 1 verificado).**
**R pela geometria (independente dos traços):** o nó de injeção é `apic[60]_x4(1)`, área 0.0 (fim de peça da divisão nos
pontos); dois caminhos axiais até nós com capacitância — última metade de `apic[60]_x4` 5.0006 MΩ e 1ª metade do filho
`apic[60]_x5` 5.0006 MΩ — em paralelo **R = 2.5003 MΩ → I·R = 0.12502 mV**; salto medido no dado antigo 0.12502 mV →
**erro 0.00% (critério ≤ 1%) → o mecanismo FECHA.**
**Porte refeito (critério inalterado; regra da cadeia de medida nos dois lados e no piso; TODAS as 504 leituras):**
| X | M1 (piso) | M1 mesmo repouso | M4 (piso) | M4 mesmo repouso |
|---|---|---|---|---|
| 10⁻⁶ | 3.05×10⁻⁵ mV | 4.6×10⁻⁵ (1.5×) PASSA | 3.2×10⁻⁴ | 2.6×10⁻⁴ (0.8×) PASSA |
| 10⁻⁸ | 1.53×10⁻⁵ mV | 7.6×10⁻⁶ (0.5×) PASSA | 7.6×10⁻⁶ | 7.6×10⁻⁶ (1.0×) PASSA |
**→ PORTE CONFERE** (pico 306 MB; construção com o repouso CARREGADO do cache: 1 294 s — quase tudo autotestes de código,
uma vez por trabalhador). Diagnóstico (não decide): repouso convergido × antigo = 3.4×10⁻⁴ mV no M1, 4.3×10⁻³ mV no M4 —
o efeito da deriva do repouso de 3 s, objeto da confirmação do item 84. `PORTE_OK.json` gravado na raiz da fila.
**LIÇÃO DE PROCESSO:** um teste sintético em tamanho real (~10 GB) foi escrito em /tmp, que aqui é tmpfs (RAM): a quota
estourou e a memória dos processos ficou pressionada até eu apagar (nada caiu). Dados grandes de teste vão para /home, ou
ficam pequenos.

**93. RESULTADOS (2026-10-08 21:07) — VERIFICAÇÕES PELA PREEMPÇÃO; FALHA DO TESTE DE RETOMADA DE ONTEM.**
**(4)(i) Nulo do viés por ponto:** referência = o próprio modelo direto, processo separado → base M1m, M1p, M4 **IDÊNTICOS
bit a bit** (JᵀΔy = 0 exato). Picos 258 / 249 MB.
**(4)(iii) Hay L0 num ponto pelo mesmo código:** roda, finito; **pico 305 MB** (orçamento do tipo "hay" no portão: 600 MB,
sai do provisório de 1 500); **repouso convergido do Hay L0: 10 114 s (~2.8 h)** — guardado no cache e compartilhado por
todos os pontos (mesma chave); protocolos 2 191 s. Diagnóstico: máx |y_Hay − y_red| = 0.011 mV no M1, 0.40 mV no M4.
**(3) Trabalhador de vida longa: 2º turno × processo novo — IDÊNTICO bit a bit** (M1m, M1p, M4). Verificado.
**G com f-I:** em curso (lançado 17:53). Nulo do termo direto: depois dele. (2) redução somática: quando a unidade
somática a 10⁻⁶ completar (42/61).
**FALHA não vista (ontem 22:43):** o teste de retomada da tarefa C (célula pequena toyC) morreu em 5 s — o autoteste do
CommonSim RECUSOU, corretamente: o pulso de 0.2 nA faz o toyC disparar (deflexão 104 mV > 15). O script não tratava a
falha da rodada inteira e seguiu ("pontos de morte não atingidos"). Corrigido: pulso do autoteste por modelo (toyC 0.005
nA) e o script dá FALHA se a rodada inteira não produzir resultado; relançado pela fila com portão. Log da falha guardado.

**94. RESULTADOS E CORREÇÕES (2026-10-09 09:10) — G COM f-I: NÃO CONFERE (contagem muda no par); custos; teste de retomada pausado.**
**Verificação do G (critério do item 85 (3)):** (1) taxas presentes e finitas — SIM (12.94 / 15.25 / 20.99 Hz em 0.78 /
1.0 / 1.9 nA); **(2) contagens iguais no par soma_SK_E2 ± 1% — NÃO: a 1.9 nA, 42 PA na base e em +1%, 43 em −1%**; (3)
coluna finita — SIM (−5.6 / −6.4 / −8.3 Hz por unidade de log); (4) base idêntica bit a bit depois do resettle — SIM.
**→ G NÃO CONFERE.** Consequência pela regra declarada: a taxa a 1.9 nA sairia NÃO condicionada → a avaliação do
espaçamento daria NÃO AVALIADO nela (nunca aprovação). Causa: a taxa por "1/ISI médio na janela de 2 s" é DESCONTÍNUA em θ
quando um PA entra ou sai da janela — com ~40 PA, uma perturbação de 1% já basta. Decisão de métrica pendente (do Martel).
**Custo medido:** uma avaliação do conjunto funcional COM f-I ≈ 63 min (4 avaliações em 4.2 h, sob disputa) → o G completo
(61 avaliações) ≈ 64 h de CPU por tolerância — não é ~25 h como estimado.
**Teste de retomada da tarefa C:** a rodada inteira do toyC levou **37 356 s (10.4 h)** — a gravação a 200 kHz nos cenários
de 1.1 s não é barata nem numa célula pequena; o portão isentava o tipo "toy" do limite de CPU → era uma 6ª simulação.
Duas mortes atingidas (meio da bissecção, meio dos cenários); a 3ª (depois de passiva) pendente. **PAUSADO (SIGSTOP, PID
gravado) às 09:08** — a checagem de tolerância (caminho crítico) tem prioridade; retoma quando ela terminar.
**Supervisor da preempção:** depois do SIGSTOP o portão completo re-amostrava o swap-in por 60 s (ajudante parado) e quase
sempre recusava → SIGSTOP/SIGCONT a cada 3 min, o ajudante de 10⁻⁸ parado ~1/3 do tempo. Corrigido: depois do SIGSTOP só o
limite de simulações (instantâneo). Resta 1 trabalho (nulo do termo direto).
**Checagem de tolerância às 09:08:** 10⁻⁶ 55/61, 10⁻⁸ 54/61, **10⁻¹⁰ 44/61**. ESTIMATIVA refeita: Gram combinado na
**madrugada de 10/10** (incerteza grande: navegador/swap, disputa). Atraso em relação a "manhã de 09/10": a troca do
navegador, a preempção oscilante e o teste de retomada como 6ª simulação.

**95. DECISÃO DO USUÁRIO (2026-10-09 09:21) — TAXA DA f-I CONTÍNUA; G SÓ NA TOLERÂNCIA DECIDIDA.**
**(1) REDEFINIÇÃO APÓS O RESULTADO (rotulada), com argumento independente dele:** o G entra na Etapa A pela propagação de
Cramér–Rao, que usa DERIVADAS do conjunto funcional em θ; uma taxa por contagem em janela fixa é função EM DEGRAUS de θ —
por diferenças finitas, derivada ~0 ou enorme quando um disparo cruza a borda. Nunca foi compatível com esse uso (mesma
constatação de "aprender × julgar", item 31: gradiente só mira grandeza contínua).
**Nova métrica:** taxa_K = 1 / média dos primeiros K ISIs = **K / (t_{K+1} − t_1)**. **K por REGRA declarada agora** (não
escolhido olhando contagens): **K = contagem na base − 2, por amplitude** (base = modelo direto em θ_verd, no MESMO cálculo
do G; o K fica gravado no G e é o MESMO usado no termo direto do viés — o Hay com menos de K+1 disparos → NÃO AVALIADO).
**Condicionamento adaptado:** os K+1 primeiros disparos EXISTEM e NÃO TROCAM DE IDENTIDADE em θ, θ+h e θ−h, para os 30
parâmetros e as três amplitudes. **Definição operacional (declarada agora):** o disparo i (i = 1…K+1) mantém a identidade
se |t_i(θ±h) − t_i(θ)| < ½ · min(ISI adjacentes na base) — nenhum disparo inserido ou removido antes do (K+1)-ésimo desloca
a numeração (um deslocamento de numeração faz t_i saltar ~1 ISI). Falhou em algum → aquela componente é NÃO AVALIADO.
Faixa de 2% inalterada. **Refazer a verificação do G** com a nova métrica (critérios do item 85 (3), com (2) = a condição
de identidade acima).
**AJUSTE DO CRITÉRIO DE IDENTIDADE (2026-10-09 09:42, ANTES do resultado do G2 — o G2 ainda não rodou; pedido do usuário).** O critério
acima compara tempos ABSOLUTOS; uma mudança SUAVE de taxa acumula deslocamento ao longo do trem (a 1.9 nA, ~21 Hz, ½ ISI
≈ 24 ms: 1% desloca o 41º disparo ~19 ms). O teste sintético anterior só tinha DESLOCAMENTO UNIFORME. **Teste de ESCALA
com o critério anterior** (trem de 42 disparos, ISI 47.6 ms, K = 40, sem inserção): escala 1.01 → mantida (pior razão
0.80); **1.02 → RECUSADA (1.60); 1.03 → RECUSADA (2.40)** — falso positivo confirmado. **Critério TROCADO:** deslocamentos
CONSECUTIVOS — com Δt_i = t_i(θ±h) − t_i(θ): |Δt_1| < ½·ISI_1 e |Δt_i − Δt_{i−1}| < ½·ISI_i (base), i = 2…K+1. Uma deriva
suave é RAMPA em Δt; uma inserção/remoção é SALTO de ~1 ISI (as duas diferenças em torno do disparo somam 1 ISI → uma
delas ≥ ½ ISI → recusa). **Todos os testes sintéticos com o critério novo:** deslocamento 2 ms → mantida (0.08); escala
1.01 / 1.02 / 1.03 → mantida (0.02 / 0.04 / 0.06); inserção no meio → recusada (1.29); inserção 5 ms depois / antes de
um disparo → recusada (1.79 / 1.79); remoção no meio → recusada (2.00); escala 1.03 + inserção → recusada (1.73);
disparo extra depois do (K+1)-ésimo → mantida (0.00); menos de K+1 disparos → recusada. **Todos como esperado.**
**(2) O G é calculado UMA vez, na tolerância decidida** — o critério de tolerância usa os valores singulares do Gram das
MEDIDAS, não o conjunto funcional. Projeção da Etapa A atualizada com o custo medido (item 96).

**96. PROJEÇÃO DA ETAPA A REFEITA COM OS CUSTOS MEDIDOS (2026-10-09 09:24; o G uma vez, na tolerância decidida — item 95 (2)).**
Medidas (sob disputa de 4–7 processos — ESTIMATIVA): protocolos da unidade distal 132 / 181 / 228 s por subpasso (10⁻⁶ /
10⁻⁸ / 10⁻¹⁰); repouso convergido ~16 min por perturbação (123 globais, em cache COMPARTILHADO por todas as unidades — a
chave já não conta grampos de amplitude zero — + 1 "posição" por ponto); somática 34 / 50 / 78 min por subpasso; conjunto
funcional com f-I 63 min por avaliação (G = 61 avaliações, UMA vez); Hay L0: protocolos 2 191 s por ponto, repouso 2.8 h
uma vez; o custo do Hay escala pela razão medida Hay/reduzido (~16.6×) no termo direto e no viés somático; construção ~0.6 h
por trabalhador. As tolerâncias mais apertadas escalam o G e o viés pela razão distal medida (ESTIMATIVA).
| atol | por ponto | fixo (repousos + somática + G + viés direto/somático + trabalhadores) | s = 400 | s = 200 | s = 100 |
|---|---|---|---|---|---|
| 10⁻⁶ | 5.5 h | 203 h (G 64) | 13.0 dias-CPU → **3.3 dias** | 20.1 → 5.0 | 35.5 → 8.9 |
| 10⁻⁸ | 7.4 h | 271 h (G 88) | 17.5 dias-CPU → **4.4 dias** | 27.0 → 6.8 | 47.9 → 12.0 |
| 10⁻¹⁰ | 9.2 h | 366 h (G 111) | 23.0 dias-CPU → **5.7 dias** | 34.9 → 8.7 | 61.1 → 15.3 |
(dias de relógio com vazão ~4 processos-equivalentes, 5 processos em 4 núcleos físicos). A unidade somática (71–162 h) é
UMA unidade: no relógio ela só não limita se for repartida (ajudantes --de-tras / trabalhadores ociosos no fim do estágio).

**97. RESULTADOS (2026-10-09 19:07) — G COM A TAXA CONTÍNUA: G_OK; CHECAGEM DE TOLERÂNCIA COMPLETA (61/61 nas três).**
**Verificação do G (item 95, critério de identidade ajustado):** K pela regra = **24 / 29 / 40** (0.78 / 1.0 / 1.9 nA;
disparos na base 26 / 31 / 42 — o K previsto). (1) taxas contínuas presentes e finitas (12.95 / 15.26 / 20.97 Hz);
**(2) identidade dos K+1 primeiros no par soma_SK_E2 ± 1%: MANTIDA — pior razão 0.047 / 0.039 / 0.111** (inclusive a 1.9 nA
com 43 disparos em −1%: o disparo a mais fica DEPOIS do (K+1)-ésimo — o caso que reprovava a métrica antiga), contagens de
BAC/CaBurst iguais; (3) coluna finita; (4) base idêntica bit a bit depois do resettle (F e disparos). **→ G_OK**
(`G_OK.json` gravado na raiz da fila). Unidade da taxa no código: 1/ms (o critério de 2% é relativo).
**DEFEITO MEU (sem custo de simulação):** a 1ª execução (12:17–15:03) completou as 4 avaliações (gravadas) mas caiu na
montagem — `assemble` exigia os 30 parâmetros e a verificação só tem o par. Corrigido (monta só os parâmetros presentes);
o veredito foi REFEITO dos arquivos gravados (`--de-arquivos`), nenhuma simulação repetida.
**Checagem de tolerância:** 10⁻⁶, 10⁻⁸ e 10⁻¹⁰ completas (61/61); o vigia encerrou o ajudante redundante de 10⁻⁶ (14:03),
retomou o de 10⁻¹⁰ (15:08) e roda o Gram combinado (COM e SEM a leitura de injeção, com a regra da cadeia de medida).
O teste de retomada da tarefa C foi RETOMADO (SIGCONT, 18:56) — a tolerância, que tinha prioridade, terminou.

**98. RESULTADO (2026-10-09 19:09) — GRAM COMBINADO: 10⁻⁸ BASTA, 10⁻⁶ NÃO (critério do item 78); MESMO veredito COM e SEM a leitura de
injeção; VALE SÓ DEPOIS DA CONFIRMAÇÃO (item 84). Ressalvas do diagnóstico registradas.**
(`results/etapaA_rec/tol_gram_combinado.txt`; regra da cadeia de medida aplicada aos dados antigos — item 91.)
| objeto | piso: ‖J6−J8‖ / ‖J8−J10‖ (razão; ∝ atol prevê 100) | σ avaliados | 10 menores σ a 10⁻¹⁰ | 10⁻⁸ × 10⁻¹⁰ | 10⁻⁶ × 10⁻¹⁰ |
|---|---|---|---|---|---|
| **COMBINADO (decide)** | 5.3×10³ / 116 (46) | 30 de 30 | 92 194 345 432 1.19e3 … | **0.3% → BASTA** | **41.7% → NÃO** |
| distal sozinha (diagnóstico) | 0.80 / 0.20 (**4**) | 29 de 30 | 0.0043 0.026 0.24 0.38 0.63 … | **12.6% → NÃO** | 506% → NÃO |
| somática sozinha (diagnóstico) | 5.3×10³ / 116 (46) | 30 de 30 | 82 177 206 421 554 … | 0.2% → BASTA | 37.1% → NÃO |
**COM × SEM a leitura de injeção: vereditos IDÊNTICOS** ({10⁻⁸: basta, 10⁻⁶: não} nos dois) → pela regra do item 89 (2), o
defeito da leitura de injeção NÃO importa para a decisão. **Tolerância decidida: 10⁻⁸ — CONDICIONADA à confirmação do item
84** (unidade distal migrada em 10⁻⁸ e 10⁻¹⁰; lançada às ~19:10 pela fila com portão). Instrução do item 86 (custo a 10⁻¹²)
não se aplica.
**RESSALVAS (não decidem; registradas para decisão do Martel):**
(a) **O combinado é dominado pela unidade SOMÁTICA**: σ_min combinado 92 ≈ somática sozinha 82; TODOS os σ da distal (≤ 1.44)
ficam abaixo de 10× o piso do combinado (12) — o critério do combinado não "vê" as direções da distal. A distal SOZINHA, a
10⁻⁸, muda 12.6% no σ = 0.026 (não basta, como diagnóstico).
(b) **O piso NÃO escala com o atol como suposto**: razão ‖J6−J8‖/‖J8−J10‖ = 46 (somática) e **4 (distal)**, não 100 → a
estimativa piso(10⁻¹⁰) = ‖J8−J10‖/100 não se sustenta (na distal, provavelmente subestimada; 10⁻¹⁰ pode não ser convergido
ali). Fonte provável na distal: algo que não é proporcional ao atol (ex.: a deriva do repouso de 3 s dos dados antigos).
(c) **HIPÓTESE (não testada):** o M5 (degraus de 2 s com 26–42 PA) por diferença central a 1% está FORA do regime linear — os
PA tardios se deslocam muito mais que a largura de um PA, e a diferença de traços vira "PA × sem PA"; isso inflaria os σ da
somática e explicaria a razão 46. É a mesma família da taxa por contagem (item 95). Teste barato possível: tempos de PA no
par ± dos dados gravados (deslocamento dos PA tardios × largura do PA).

**99. DIAGNÓSTICOS PÓS-RESULTADO DO GRAM COMBINADO (2026-10-09 19:44; NÃO decidem — rotulados; decisão do Martel).**
**(c) do item 98 TESTADA nos traços gravados (somática a 10⁻¹⁰): CONFIRMADA.** Largura do PA ~1.3–1.6 ms; deslocamento de
PA no M5 entre θ+1% e θ−1%: até **45 ms** (e_pas, soma_SKv3_1, soma_Ca_HVA, soma_gamma, soma_decay); > 1 ms em 58% dos
pares (parâmetro, amplitude), > 5 ms em 38%; contagem diferente no par em 8 de 90 → o M5 como traço de voltagem está FORA
do regime linear.
**O piso do combinado vem de UM parâmetro no M3:** ‖J8 − J10‖ = 115 é quase todo **e_pas** (‖ΔJ‖ 115.4; o 2º maior, Ra, 2.7):
com e_pas ± 1% o M3 tem um SEGUNDO PA no soma em **63.8 ms (+1%) × 74.4 ms (−1%)** — a diferença central atravessa um PA que
se move 10 ms; as bases do M3 em 10⁻⁸ e 10⁻¹⁰ são idênticas. O critério avalia só σ ≥ 10 × esse piso (12).
**Gram combinado SEM o M5** (`tol_gram_semM5_DIAGNOSTICO.txt`, dos arquivos gravados): o piso continua 115 (é do M3); σ_min
cai de 92 para **0.76**; só 25 de 30 σ ficam acima de 10× o piso e os 5 menores (0.76, 1.17, 1.32, 2.05, 10.1) NÃO são
avaliados; nos avaliados, 10⁻⁸ e até 10⁻⁶ "bastam" (0.0% / 0.1%) — o critério só olha as direções fortes.
**Distal — o piso por protocolo:** M1 (sublimiar, ±50 pA): ‖J6−J8‖/‖J8−J10‖ = 2.05/0.43 (razão **4–5**), espalhado em
condutâncias LENTAS (basal_Ih, soma_Ca_LVAst, soma_SK_E2) — não é PA; hipótese: o repouso de 3 s ainda derivando (Ih/Ca
lentos) — a confirmação na unidade MIGRADA (repouso convergido; em curso) testa isso diretamente. M4 (α até 1.5 nA, com PA
dendrítico): razão 18.
**Leitura (não decide):** o veredito "10⁻⁸ basta" do item 98 foi tomado sobre um objeto em que (i) os σ da somática são
inflados por PAs fora do regime linear (M5), (ii) o piso que filtra os σ avaliados é um artefato de UM PA que se move 10 ms
(M3, e_pas), e (iii) as direções fracas reais (distal, e o combinado sem M5) ficam abaixo do piso — não avaliadas.

**100. RESULTADOS (2026-10-12 15:41) — CONFIRMAÇÃO DO ITEM 84: NÃO TRANSFERE; pré-requisitos verificados; teste de retomada IDÊNTICO.**
(Tudo terminou ANTES do reinício da máquina de 10/10 10:17; nada perdido.)
**Confirmação (item 84; `etapaA_conf/conf_check.json`; regra da cadeia de medida nos dois lados):** unidade distal MIGRADA
(CommonSim, repouso convergido) em 10⁻⁸ e 10⁻¹⁰ × a ANTIGA em 10⁻⁸. piso(10⁻⁸) = ‖J_migr(10⁻⁸) − J_migr(10⁻¹⁰)‖ = 0.086;
21 de 30 σ avaliados. **Pior |σ_migr/σ_antiga − 1| = 39.3% (COM a leitura de injeção) / 39.1% (SEM) → NÃO TRANSFERE**
(mesmo veredito com e sem — o salto não explica; o efeito é do REPOUSO). Na migrada, 10⁻⁸ × 10⁻¹⁰ = 0.00% nos avaliados.
10 menores σ — migrada: 0.0060 0.047 0.077 0.23 0.37 0.71 0.72 0.74 0.74 1.29; antiga: 0.0077 0.029 0.26 0.37 0.63 0.73
0.76 0.79 1.20 1.44 → a deriva do repouso de 3 s INFLAVA direções fracas (ex.: 0.26 → 0.077, ×3.3) — "informação inventada",
o risco previsto no item 84. **Pela regra declarada: a checagem de tolerância tem de ser REFEITA na unidade migrada.**
**Pré-requisitos:** (1) porte — CONFERE (item 92); (2) redução somática — bloco × traço **1.9×10⁻¹⁶ → EXATO** (a 1ª rodada
deu 1.9×10⁻⁵ "FORA" porque o lado direto do script não aplicava a regra da cadeia de medida que a redução aplica desde o
item 91 — corrigido no script, critério inalterado); (3) G com a taxa contínua — G_OK (item 97); (4) viés por ponto —
(i) nulo por ponto IDÊNTICO, (ii) nulo do termo direto dF = 0 EXATO (55 grandezas), (iii) Hay L0 finito → **CONFERE**;
(iv) controle positivo: referência (g_pas_apical × 1.02, 10⁻⁸) na fila com portão. Trabalhador de vida longa: IDÊNTICO.
**Teste de retomada da tarefa C (pv_C/hay4_C pelo runner): RETOMADA IDÊNTICA nos 3 pontos de morte** (meio da bissecção,
meio dos cenários, depois de passiva): JSON igual, 232 arranjos idênticos, 710 eventos. Custo: rodada inteira do toyC 10.4 h.

**101. DECISÃO DO USUÁRIO (2026-10-12 16:51) — REFAZER A CHECAGEM DE TOLERÂNCIA NA ORDEM CERTA; DIAGNÓSTICOS DO PISO.**
**(1) REGISTRADO:** confirmação do item 84 = NÃO TRANSFERE (pior σ 39%; igual com e sem a leitura de injeção → efeito do
REPOUSO, não do salto); o repouso de 3 s, ainda derivando, INFLAVA direções fracas (σ 0.26 → 0.077). **O veredito de
tolerância da unidade antiga (item 98) fica ANULADO.** A confirmação, DECLARADA ANTES (item 84), foi o que impediu
dimensionar a Etapa A sobre um objeto que superestimava a identificabilidade. Pré-requisitos (1)–(3) conferem; (4) confere
em (i)–(iii) e **(iv) controle positivo PASSA** (δlog g_pas_apical 0.01985 × 0.01980 esperado, erro 0.3%; maior vazamento
para outro parâmetro 0.0037) → `VIES_OK.json`. Teste de retomada do pv_C/hay4_C verificado (item 100).
**(2) DECISÃO 1 — PROTOCOLOS COM DISPARO: APROVADA.** Disparos pelos TEMPOS (contínuos, identidade do item 95); voltagem só
em trechos SUBLIMIARES com bloqueio em volta dos disparos. Justificativa independente (do usuário): Cramér–Rao é
linearização; durante um disparo ΔV ≈ (dV/dt)·Δt com dV/dt de centenas de mV/ms — as diferenças finitas sobre essas amostras
só valem para deslocamentos minúsculos e DOMINAM o Gram (mesma família da taxa por contagem). Condições: (a) ruído
convertido, σ_t ≈ σ_V / |dV/dt| no ponto de detecção; (b) janela de bloqueio DERIVADA (largura do disparo + resposta do
filtro da cadeia); (c) UM caminho só (Jacobiano, viés, comparações); verificação com o rigor dos pré-requisitos.
**REGRAS DECLARADAS AGORA (antes de implementar):** disparo = evento com dV/dt ≥ 20 mV/ms (critério do detector do D122) e
proeminência ≥ 20 mV, no traço da cadeia de medida (linha de base pré-estímulo). Início = 1ª amostra da subida com dV/dt ≥ 20
mV/ms; fim = 1ª amostra depois do pico com V de volta ao valor do início. **Tempo do disparo** = cruzamento ascendente do
NÍVEL fixado na BASE (V_início + ½ (V_pico − V_início), por disparo), por interpolação linear; o mesmo nível em todas as
avaliações. **(a)** a linha do tempo entra multiplicada por |dV/dt| da base no cruzamento (unidade "mV equivalente") — com
o MESMO σ_V das amostras de voltagem, isso é exatamente σ_t = σ_V/|dV/dt|. **(b)** janela = [início, fim] de cada disparo,
UNIÃO sobre TODAS as avaliações da unidade (base, θ ± h, extras e a referência do viés — o disparo se move entre avaliações;
derivada, não escolhida) + resposta do filtro da cadeia (= 0 até a emulação existir — PENDÊNCIA); as amostras de voltagem
usadas são as MESMAS em todas as avaliações. Identidade (item 95) dos disparos da base em toda avaliação; falhou → os tempos
daquela leitura saem (contados e reportados), a voltagem fora da máscara fica. **Diagnóstico de linearidade nas amostras
que sobram** (não decide): índice |y₊ + y₋ − 2y₀| / |y₊ − y₋| — trechos entre disparos de um trem podem estar deslocados
em fase mesmo fora das janelas; se estiverem, é reportado.
**(3) DECISÃO 2 — O PISO: DIAGNÓSTICO BARATO FEITO (dos arquivos):** a hipótese do M4 NÃO se sustenta — piso da distal
migrada: M1+M4 0.0858; **só M1 0.0855**; só M4 0.0073. Localizado: no M1 (sublimiar), TODOS os parâmetros contribuem igual
(‖ΔJ‖ 0.065–0.070) e as maiores diferenças são EXATAMENTE 3.83×10⁻⁴ e 7.67×10⁻⁴ mV/log = 1 e 2 passos de float32 a 32–64 mV
(7.63×10⁻⁶ mV) / 2h. **Comprovado: 99.7% das diferenças 10⁻⁸ × 10⁻¹⁰ do M1 são EXATAMENTE zero, o resto ±1 passo de
float32.** Causa: a unidade convertia para float32 ANTES de tirar a linha de base (em ~−75 mV; depois dela, em ~6 mV, o passo
seria 16× menor). **→ O piso de 0.086 é QUANTIZAÇÃO DO ARMAZENAMENTO, não o solver; os 9 σ "não avaliados" estavam abaixo de
um piso de armazenamento.** Isso vale também para TODOS os dados antigos (anulados). Corrigido: traços em FLOAT64 (linha de
base em float64). A unidade distal migrada é REFEITA em float64 a 10⁻⁸ e 10⁻¹⁰ (repousos em cache: só protocolos) para
medir o piso do SOLVER; depois, com a decisão 1, conta-se de novo quantos dos 30 σ ficam acima de 10× o piso. **10⁻⁸ NÃO é
concluído com σ não avaliados** — são as direções mais fracas, o que a Etapa A mede.
**(4) SÓ ENTÃO:** proposta da checagem refeita na unidade SOMÁTICA migrada (tolerâncias e custo), considerando se 10⁻⁶ basta
no objeto migrado, com critério paralelo declarado antes.

**102. RESULTADOS (2026-10-12 16:56) — VERIFICAÇÃO DA DECISÃO 1: FALHA NA JANELA (a representação NÃO é usada); buraco na identidade
achado e corrigido; G2 continua G_OK; float64 refeito na fila.**
**Verificação sintética (`etapaA_rep_check.py`; PA gaussiano de 100 mV, σ 0.25 ms, sobre fundo lento independente de θ):**
(V1) nulo → J = 0 exato: ok; (V2) tempos: J = |dV/dt|·dt/dlogθ com erro ≤ 0.06%: ok; **(V2) voltagem fora da máscara → J = 0
exato: FALHOU — até 30 mV/log em 59 amostras** (a regra início = dV/dt ≥ 20 mV/ms / fim = volta a V_início deixa de fora o
"pé" e a cauda do disparo — no sintético a janela começa com o PA já 6.6 mV acima do fundo); (V3) |dV/dt| usado 239.4 ×
analítico 235.5 mV/ms (1.7%): ok; (V4) escala 1.02: ok; (V5) mutação sem máscara pega: ok.
**Buraco na IDENTIDADE (item 95) achado pelo (V5):** uma inserção no ÚLTIMO intervalo comparado passava (170 ms entre 120 e
200: razão 0.75; no ponto médio, 1 − ε) — o argumento "as duas diferenças somam 1 ISI" só vale se o disparo seguinte também
for comparado. **Corrigido (para cumprir o propósito declarado):** + condição de CONTAGEM — até o horizonte t_último(base) +
Δt_penúltimo + ½·ISI_último (acompanha a deriva) a avaliação tem exatamente o número de disparos comparados (um horizonte
fixo recusava as escalas 1.02/1.03 — testado e descartado). Todos os casos sintéticos certos (deslocamento, escalas
1.01–1.03, inserção no meio / no último intervalo / no ponto médio / com escala, remoção no meio / do último, extra depois,
menos de K+1). **G2 reavaliado dos arquivos com o critério corrigido: continua G_OK** (razões 0.047 / 0.039 / 0.111).
**Diagnóstico nos traços REAIS (somática a 10⁻¹⁰, e_pas / soma_SKv3_1 / g_pas_apical), sem decidir:** depois de mascarar
os disparos (união das janelas), as amostras de voltagem que SOBRAM continuam fora do regime linear — M3 (soma): |J_V| até
22–70 mV/log, índice |y₊ + y₋ − 2y₀|/|y₊ − y₋| > 0.1 em 91–97% delas; M5: |J_V| 560–880 mV/log, índice > 0.1 em 23–98%.
**Entre disparos e depois de um disparo, a trajetória INTEIRA herda o deslocamento de tempo** — "voltagem sublimiar fora das
janelas" não basta. E o fim de janela "volta a V_início" falha nos trens rápidos (1.9 nA: a voltagem não volta ao nível →
1 disparo detectado, 20 mil amostras bloqueadas). **→ A representação, como declarada no item 101, NÃO passa na verificação
e NÃO é usada. Decisão pendente (do Martel).**
**Unidade distal migrada em float64 (10⁻⁸ e 10⁻¹⁰):** na fila com portão (fechado por swap-in do navegador).

**103. DECISÃO DO USUÁRIO (2026-10-12 19:22) — DUAS DECISÕES + UM TESTE DE CUSTO.**
**(1) REGISTRADO:** o piso de 0.086 era QUANTIZAÇÃO DE FLOAT32 (conversão antes de tirar a linha de base, em −75 mV), não o
solver nem o disparo do M4 — **a hipótese do M4 fica REFUTADA**. **CONSEQUÊNCIA PARA TRÁS:** a conclusão "10⁻⁶ inventa
informação nas direções fracas" (item 74 H) veio de dados em float32 — ali não dá mais para separar solver de
armazenamento; os dados antigos já estão anulados e **a atribuição ao solver fica INCERTA**. Buraco no critério de
identidade (inserção no último intervalo comparado) e correção com horizonte que acompanha a deriva (item 102); G2 refeito
continua G_OK.
**(2) REPRESENTAÇÃO DOS PROTOCOLOS COM DISPARO — APROVADA COMO BASE:** voltagem só ANTES do primeiro disparo de cada leitura;
disparos pelos TEMPOS; nenhuma amostra de voltagem depois do primeiro disparo; a janela de bloqueio da cadeia de medida
continua nas descontinuidades do estímulo. **ACRÉSCIMO — atributos por disparo identificado (item 95):** voltagem no LIMIAR,
voltagem no PICO e o VALOR mínimo da pós-hiperpolarização (só o valor; o instante de um mínimo é mal condicionado); ruído
σ_V, sem conversão. Justificativa (do usuário): a base descarta a FORMA depois do disparo, onde ficam os sinais de K e de
adaptação; as direções fracas da Etapa A são combinações de canais somáticos — sem isso elas podem sair artificialmente
inidentificáveis e a especificação do sensor mais exigente do que precisa. Verificar com o mesmo rigor (nulo, caso
conhecido, linearidade nos traços reais de M3 e M5); atributo que falhar na linearidade fica FORA, com a perda registrada.
Um caminho só (Jacobiano, viés, comparações).
**(3) TESTE DE 10⁻⁶ NO OBJETO MIGRADO EM FLOAT64 — CRITÉRIO DECLARADO AGORA (antes dos dados):** a unidade distal migrada em
float64 roda a 10⁻⁶, 10⁻⁸ e 10⁻¹⁰ (repousos em cache); **10⁻⁶ BASTA se todo σ acima de 10× o piso de 10⁻⁸ (‖J8 − J10‖)
mudar ≤ 10% entre 10⁻⁶ e 10⁻⁸.** Se bastar, a unidade somática pode rodar a 10⁻⁶.
**ORDEM:** float64 distal (10⁻⁶, 10⁻⁸, 10⁻¹⁰) → piso remedido → representação implementada e verificada → proposta da checagem
somática com custos, ANTES de lançar.

**104. RESULTADOS (2026-10-12 19:27) — VERIFICAÇÃO DA REPRESENTAÇÃO (base do item 103 + atributos): LIMIAR, PICO E AHP FICAM FORA;
tempos e voltagem pré-disparo passam na linearidade real; resta o "pé" do disparo.**
Implementação (`etapaA_unit`: `disparos`, `representar`): segmentação por subidas com dV/dt ≥ 20 mV/ms (a regra antiga de fim
"volta a V_início" falhava nos trens rápidos); voltagem só antes do 1º disparo MAIS CEDO entre as avaliações (mesmas amostras
em todas); tempo = cruzamento interpolado do nível da base × |dV/dt|; limiar = V no instante interpolado de dV/dt = 20; pico e
mínimo da AHP por parábola nos extremos (janela da AHP até a subida seguinte; no último disparo, um ISI da base).
**(V6) LINEARIDADE NOS TRAÇOS REAIS (somática a 10⁻¹⁰, M3 + M5, 30 parâmetros; índice |y₊ + y₋ − 2y₀|/|y₊ − y₋| > 0.1;
critério: tipo FORA se > 10%):** voltagem pré-disparo 2.5% (127 211 entradas) → PASSA; **tempo 6.3%** (10 437) → PASSA;
**limiar 39.2% → FORA; pico 24.6% → FORA; AHP 16.5% → FORA.** Atributos fora por identidade: 593 de 10 290 leituras ×
parâmetros (5.8%). **PERDA REGISTRADA:** sem os atributos de forma (limiar, pico, AHP), o sinal de K e de adaptação que eles
carregariam NÃO entra no J — as direções fracas que dependem dele podem sair artificialmente inidentificáveis e a especificação
do sensor mais exigente do que precisa (o risco que o usuário apontou no item 103) — a quantificar quando o J existir.
**Sintético (PA de suporte compacto):** (V1) nulo exato; tempos 0.72% (≤ 2%); AHP 0.00%; escala 1.02 mantida; mutações pegas
(voltagem depois do 1º disparo; disparo inserido). Falhas: limiar 460% e pico 13% (referência analítica contínua × definição
amostrada a 0.1 ms; irrelevantes — os dois saem pela linearidade real); (V3) |dV/dt| 78.2 × "55.5" era ERRO DO TESTE (nível
½A → s = W1/2 → 78.5 analítico; 0.4%) — corrigido no teste. **Voltagem pré-disparo NÃO é exata: sobra 1 amostra — o PÉ do
disparo mais cedo** (suporte do PA começa em 49.5 ms; a detecção por dV/dt ≥ 20 marca 49.7; na amostra 49.6, erro 27.8 mV/log
× J do fundo 1.4). Mesmo mecanismo da falha do item 102, reduzido a uma amostra; nos traços reais a voltagem pré-disparo passa
no critério de linearidade (2.5%). **Decisão pendente (do Martel):** aceitar o pé (passa no critério real) ou cortar a
voltagem pré-disparo por uma regra que alcance o pé.
**Unidade distal migrada em float64:** 10⁻⁸ 38/61, 10⁻¹⁰ 20/61, 10⁻⁶ começando (repousos da cache de 10⁻⁸ pela opção
`--repouso-chave-atol`: o repouso é Euler implícito, sem CVode — 61 repousos IDÊNTICOS byte a byte nas caches de 10⁻⁸ e 10⁻¹⁰).

**105. DECISÃO DO USUÁRIO (2026-10-12 19:47) — CORTAR O PÉ DO DISPARO; CRITÉRIO DE PESO NA VERIFICAÇÃO; PERDA DOS ATRIBUTOS.**
**(1) PÉ:** excluir a ÚLTIMA amostra de voltagem antes do início detectado. Argumento (do usuário): o pé não traz informação
própria — carrega o INSTANTE de início, que já está no tempo do disparo; mantê-lo conta o mesmo tempo duas vezes, uma na forma
não linear. **Regra derivada:** o detector marca o início com atraso de ATÉ UMA AMOSTRA (dV/dt cruza o limiar entre duas
amostras) → corte = a última amostra antes do início detectado, na taxa de amostragem em uso (acompanha a taxa). O sintético
refeito tem de dar a voltagem pré-disparo EXATA.
**(2) CRITÉRIO DE PESO — LIMITES DECLARADOS AGORA (antes de calcular):** a fração de entradas não lineares não vê o PESO (o Gram
soma J²). Acrescentado a TODA verificação de representação, sobre o Gram da representação montado com TODAS as avaliações
juntas (mesmas amostras): (a) fração do TRAÇO do Gram (Σ J²) vinda das entradas não lineares (índice > 0.1) ≤ **10%**; (b)
para cada uma das **5 direções mais fracas** v (autovetores dos 5 menores σ do Gram), ‖J_nl v‖² / (‖J_lin v‖² + ‖J_nl v‖²)
≤ **10%** (J_nl = só as entradas não lineares; J_lin = o resto). Componente que passa na fração mas falha no peso NÃO passa.
Aplicado à representação aprovada (voltagem antes do 1º disparo, sem o pé; tempos).
**(3) PERDA DOS ATRIBUTOS, quando o J existir:** Gram COM limiar, pico e mínimo da AHP (apesar da não linearidade) = LIMITE
OTIMISTA do que acrescentariam; comparar os menores σ com e sem — quase não muda → perda pequena (registrar); muda → é a MEDIDA
do risco (direções somáticas artificialmente inidentificáveis), registrar com números e trazer.
**Depois:** ligar a redução da Etapa A ao caminho único de representação.

**106. RESULTADOS (2026-10-12 21:12) — PÉ CORTADO: voltagem pré-disparo EXATA no sintético; CRITÉRIO DE PESO: (a) passa, (b) é MAL POSTO
como declarado (cancelamento); diagnóstico por linhas contaminado por float32.**
**Pé (item 105 (1)):** corte = última amostra antes do início detectado → no sintético a voltagem antes do 1º disparo fica
EXATA (corte em 49.6 ms; antes 49.7; suporte do PA mais cedo em 49.50). Demais casos sintéticos mantidos.
**Critério de peso na representação aprovada** (somática a 10⁻¹⁰, M3 + M5, 61 avaliações juntas por leitura — dados ANTIGOS em
float32): linearidade por fração — voltagem 2.3%, tempo 6.3% (passam); **(V7a) peso no traço do Gram das entradas não lineares
2.8% ≤ 10% → PASSA; (V7b) nas 5 direções mais fracas (σ 2.44, 4.77, 11.8, 20.5, 22.6): 50.0%, 50.0%, 50.0%, 50.0%, 50.1% → "FALHA"
— mas o critério (b), COMO DECLARADO, É MAL POSTO:** nas direções fracas Jv é pequeno por definição e as partes linear e não
linear são 10⁴–5×10⁴ vezes MAIORES que ele e se ANULAM (‖J_lin v‖² ≈ ‖J_nl v‖² ≈ 3×10⁴ × ‖Jv‖² = 5.9 na direção 1) → a razão
declarada dá ~50% para qualquer dado. Zerar ENTRADAS também não serve: quebra os cancelamentos e INVENTA informação (σ_min sobe
de 2.44 para 8.27). Erro meu ao declarar o critério.
**Diagnóstico por LINHAS (medidas inteiras; não decide):** linha "não linear" = alguma entrada com índice > 0.1 → 141 835 de
418 666 linhas (33.9%) — 141 789 de voltagem, 46 de tempo. SEM essas linhas, os 5 menores σ caem para 0.0044 0.105 0.11 0.118
0.152 (≈ 100× menores) → a informação das direções fracas viria quase toda de linhas marcadas. **Ressalva:** os traços são os
ANTIGOS em float32 (passo 7.6×10⁻⁶ mV); com o limiar |y₊ − y₋| > 10⁻⁴ mV, a quantização sozinha já dá índice ~0.1 → a marcação
"não linear" das linhas de voltagem é SUSPEITA de ser ruído de armazenamento. Também: só voltagem pré-disparo dá σ_min 0.137,
só tempos 0.20, juntos 2.44 (a combinação informa).
**Decisão pendente (do Martel):** redefinir (b) em nível de LINHA (medidas inteiras) e avaliá-lo em dados FLOAT64 (a unidade
distal migrada em float64 tem M4 com disparo; a somática em float64 ainda não existe).

**107. RESULTADOS (2026-10-12 23:30) — PISO EM FLOAT64; CRITÉRIO DE 10⁻⁶: "BASTA" pelo critério declarado, mas 10⁻⁶ INFLA as 7 direções
mais fracas (não avaliadas); perda dos atributos na distal.**
(Unidade distal migrada em FLOAT64 a 10⁻⁶, 10⁻⁸, 10⁻¹⁰, repouso convergido; representação aprovada — voltagem antes do 1º disparo
sem o pé + tempos; `etapaA_piso64.py`, `piso64.json`.)
**Piso em float64:** ‖J8 − J10‖ = **0.0037** (era 0.086 em float32 — 23× menor); ‖J6 − J8‖ = 0.325 → **razão 87** (≈ 100: o erro
ESCALA com o atol, o que nos dados antigos não acontecia — razão 4). σ acima de 10× o piso: **23 de 30**. Diagnóstico: só M1,
17 de 30; só M4 (com a representação) 23 de 30 — e no M4 sozinho 10⁻⁶ × 10⁻⁸ = 276% (traço inteiro: 78.5%).
**CRITÉRIO DECLARADO (item 103): 10⁻⁶ × 10⁻⁸ nos 23 σ avaliados — pior 1.8% → "10⁻⁶ BASTA".** 10⁻⁸ × 10⁻¹⁰ nos avaliados: 0.02%.
**MAS, nas 7 direções mais fracas (abaixo de 10× o piso — NÃO avaliadas pelo critério):**
| k | σ(10⁻⁶) | σ(10⁻⁸) | σ(10⁻¹⁰) | 10⁻⁶ × 10⁻⁸ | 10⁻⁸ × 10⁻¹⁰ | avaliável contra 10⁻¹⁰ (10× ≈ 4.2×10⁻⁴)? |
|---|---|---|---|---|---|---|
| 1 | 0.0027 | 0.00015 | ~0 | **18×** | — | não |
| 2 | 0.0053 | 0.00028 | 1.9×10⁻⁵ | **18×** | — | não |
| 3 | 0.0058 | 0.00031 | 0.00028 | **18×** | 11% | não |
| 4 | 0.0086 | 0.00051 | 0.00048 | **16×** | 7.3% | sim |
| 5 | 0.0087 | 0.0010 | 0.00098 | **8.5×** | 4.0% | sim |
| 6 | 0.0098 | 0.0036 | 0.0036 | **2.7×** | 0.24% | sim |
| 7 | 0.0246 | 0.0234 | 0.0234 | 5.2% | 0.02% | sim |
(piso(10⁻¹⁰) estimado = ‖J8 − J10‖ / 87 = 4.2×10⁻⁵, pela razão medida.) **Leitura (não decide):** 10⁻⁶ INVENTA informação nas
direções fracas (σ_min 18× maior que a 10⁻⁸) — a conclusão do item 74 (H), que o item 103 tornara incerta por causa do
float32, fica RESTABELECIDA em float64 com repouso convergido: a atribuição ao SOLVER é sólida agora. 10⁻⁸ fica a ≤ 7.3% de
10⁻¹⁰ em TODAS as direções avaliáveis contra 10⁻¹⁰ (σ ≥ 4.2×10⁻⁴); σ3 (11%) e σ1–2 abaixo da resolução. **O critério
declarado de 10⁻⁶ mede só as direções fortes — a mesma cegueira apontada no item 99; decisão do Martel.**
**Perda dos atributos (item 105 (3)) — na DISTAL (o J que existe; o M4 tem disparo em 2 leituras):** Gram COM limiar, pico e AHP
(limite otimista, 6 linhas a mais) × SEM: razão nos 10 menores σ = 1.01 1.10 1.16 1.24 1.27 1.06 1.02 1.08 1.09 1.02 → até
**+27%** numa direção fraca com só 6 medidas a mais. Na somática (onde ficam K e adaptação) tende a pesar mais — a medir quando
existir o J somático em float64.

**108. DECISÃO DO USUÁRIO (2026-10-13 09:14) — SOMÁTICA A 10⁻⁸; PESO POR LINHA; CONTROLE DE CRITÉRIO; A ORDEM.**
**(1) TOLERÂNCIA DA SOMÁTICA: 10⁻⁸.** O "10⁻⁶ basta" do item 107 é APROVAÇÃO VAZIA: o critério avalia só as direções acima de 10× o
piso, e é FORA delas — nas 7 mais fracas — que 10⁻⁶ infla os σ de 3 a 18×; as direções fracas são o que a Etapa A mede.
**REGRA (extensão do item 56): uma avaliação PARCIAL não pode virar aprovação geral quando a parte não avaliada é a que
importa.** Leitura correta: passa nas direções avaliáveis, infla nas outras → **10⁻⁶ REPROVADO.** Reportar quantos dos 30 σ
são avaliáveis entre 10⁻⁸ e 10⁻¹⁰ (acima de 10× o piso de 10⁻¹⁰ em float64); os que ficarem abaixo mesmo a 10⁻¹⁰ são
RESULTADO: direções indistinguíveis de zero na melhor precisão disponível — inidentificáveis por este protocolo, não defeito
do solver.
**(2) CRITÉRIO DE PESO (b) REDEFINIDO POR LINHA:** um critério que dá 50% para QUALQUER dado não contém informação — é mal posto,
não reprovado. Peso de cada linha (medida) r numa direção v = (J_r·v)² — não negativo e somável. Classificação de linha não
linear declarada ANTES de avaliar (item 109). Avaliado em dados float64.
**(3) REGRA NOVA — CONTROLE DE CRITÉRIO:** quarta vez que um critério sai mal posto (razão perto de troca de sinal; tolerância
abaixo da resolução; fração sem peso; cancelamento). Como os detectores têm controles negativo e positivo, **TODO CRITÉRIO NOVO
é testado em dados SINTÉTICOS COM RESPOSTA CONHECIDA antes de ser usado.** Para o peso: dados inteiramente lineares → perto de
0%; uma linha não linear plantada e dominante → alto.
**(4) A ORDEM:** a unidade somática é onde estão os disparos (M3, M5); se rodar antes de a redução usar o caminho único de
representação, o Gram soma as amostras não lineares excluídas. 1º ligar a redução ao caminho único (voltagem antes do 1º disparo
sem o pé; tempos) e verificar (nulo; redução × representação das análises iguais); 2º peso redefinido, com o controle sintético,
nos dados float64; 3º proposta da checagem somática a 10⁻⁸ com custos — antes de lançar.

**109. DECLARADO ANTES DE AVALIAR (2026-10-13 09:30) — CRITÉRIO DE PESO POR LINHA E SEUS CONTROLES SINTÉTICOS.**
**Classificação de uma linha (medida) r como NÃO LINEAR:** para cada parâmetro p com |y₊ − y₋| > 10⁻⁶ (mV ou mV equivalente — bem
acima da resolução de float64), índice_rp = |y₊ + y₋ − 2y₀| / |y₊ − y₋|; a linha é não linear se máx_p índice_rp > 0.1.
**Peso:** de cada linha r numa direção v, (J_r·v)² (não negativo, somável). (a) fração do traço do Gram (Σ_r ‖J_r‖²) vinda das
linhas não lineares ≤ 10%; (b) para cada uma das 5 direções mais fracas v do Gram, Σ_{r não lineares} (J_r·v)² / Σ_r (J_r·v)² ≤ 10%.
**CONTROLES SINTÉTICOS (regra do item 108 (3)), com resposta conhecida, ANTES dos dados reais:** (C1) linhas INTEIRAMENTE
lineares em log θ, com direções fracas criadas por linhas quase colineares (o cancelamento que derrubou a versão anterior) →
(a) e (b) perto de 0%; (C2) uma linha NÃO linear plantada que DOMINA a direção mais fraca → (b) alto (> 50%) nessa direção;
(C3) uma linha não linear plantada, pequena e fora das direções fracas → (b) baixo nas direções fracas (o critério não marca
tudo). O critério só é aplicado aos dados reais se os três controles derem o esperado.
**Dados reais:** unidade distal migrada em float64 a 10⁻⁸ (M1 + M4, representação aprovada), única J em float64 que existe.

**110. RESULTADOS (2026-10-13 09:53) — σ AVALIÁVEIS 10⁻⁸ × 10⁻¹⁰; REDUÇÃO LIGADA E VERIFICADA; PESO POR LINHA (controles passam; dados
reais FALHAM por eventos dendríticos lentos); PROPOSTA DA SOMÁTICA.**
**(1) σ avaliáveis entre 10⁻⁸ e 10⁻¹⁰ (distal migrada, float64, representação):** piso(10⁻¹⁰) estimado = ‖J8 − J10‖ / 87 (razão medida)
= 4.2×10⁻⁵ → 10× = 4.2×10⁻⁴ → **27 de 30 avaliáveis; pior |σ8/σ10 − 1| = 7.3%** (em σ = 4.8×10⁻⁴) → 10⁻⁸ ≤ 10% em TODOS os
avaliáveis. **RESULTADO (regra do item 108 (1)):** os 3 restantes — σ(10⁻¹⁰) ≈ 0, 1.9×10⁻⁵, 2.8×10⁻⁴ — ficam abaixo do piso MESMO a
10⁻¹⁰, os dois primeiros também abaixo da resolução numérica da decomposição (σ ≳ 9×10⁻⁵; autovalores crus −4.6×10⁻⁹ e 3.6×10⁻¹⁰):
**direções indistinguíveis de zero na melhor precisão disponível — inidentificáveis por este protocolo (UMA unidade distal), não
defeito do solver.**
**(2) Redução ligada ao caminho único** (`EtapaAUnit.reduce` por `representar`, todas as avaliações juntas por leitura; M4/M5 em
linhas por amplitude, somadas no bloco do local). Verificação (`etapaA_reduce_check.py`, distal float64 a 10⁻⁸): (R1) Σ blocos ×
Gram das análises: **1.6×10⁻¹⁵ → IGUAIS**; (R2) nulo do viés: **JᵀΔy = 0 exato**; (R3) pedaços de 2 × 7 leituras: **idênticos bit
a bit** → **PASSA.**
**(3) Critério de peso por linha (item 109).** Controles sintéticos: (C1) linear com cancelamento → 0.00%; (C2) linha não linear
plantada → 90% na direção que domina; (C3) pequena fora das fracas → 0.000% → **PASSAM** (e a demonstração: o critério ANTIGO por
entrada dá 50% em dados LINEARES). **Dados reais (distal float64, 10⁻⁸, M1 + M4):** linhas não lineares 2.7%; **(a) traço 5.3% →
PASSA; (b) direções fracas 1–5: 3.7%, 45.1%, 5.0%, 30.1%, 39.5% → FALHA nas direções 2, 4 e 5.** **Origem:** o M4 a 1.5 nA (linhas no
ponto e no soma) — 44% / 29% / 38% do peso nessas direções; o M1 ≤ 4.7%. No ponto, o evento dendrítico é detectado e o seu tempo
tem índice 17 (apic_Ih_escala); no SOMA, o evento dendrítico chega ATENUADO, sem passar de dV/dt ≥ 20 mV/ms — não é marcado como
disparo e a voltagem dele se desloca no tempo com θ (cm_dend, apic_Ca_LVAst_zona). **O mesmo vale para a somática:** no M3, o bAP
chega às leituras dendríticas lento e sem cruzar o limiar de disparo. **Decisão pendente (do Martel):** como representar eventos
LENTOS (dendríticos/atenuados) — ou tirar a amplitude supralimiar do M4.
**(4) PROPOSTA DA CHECAGEM SOMÁTICA A 10⁻⁸ (nada lançado):** unidade somática migrada (CommonSim, float64, redução pela
representação), 61 avaliações θ a 10⁻⁸ e a 10⁻¹⁰; repousos REAPROVEITADOS da cache da distal (mesmo modelo → mesma chave; opção
`--repouso-chave-atol`). Custo pelo medido (somática antiga: 50 / 78 min por subpasso a 10⁻⁸ / 10⁻¹⁰, sob disputa): **51 h + 79 h
= 130 h de CPU** + construção (~0.4 h por processo); com 5 processos (2 a 10⁻⁸, 3 a 10⁻¹⁰) ≈ **33 h de relógio (~1.4 dia)**.
**Reaproveitamento:** os 61 subpassos θ a 10⁻⁸ SÃO os da unidade somática da Etapa A (mesmo código e configuração) — guardados
sem apagar os brutos, a Etapa A só precisa dos 63 extras (ganho + 62 geometrias) → economiza ~51 h depois. **A simulação NÃO
depende da decisão sobre eventos lentos:** os traços brutos ficam guardados e a redução pode ser refeita sem simular. Saídas: piso
somático, σ avaliáveis 10⁻⁸ × 10⁻¹⁰, Gram COMBINADO (distal + somática) em float64, critério de peso e perda dos atributos
(item 105 (3)) no J somático.

**111. DECISÃO DO USUÁRIO (2026-10-13 10:10) — SOMÁTICA LANÇADA; REGISTROS; EVENTOS LENTOS: MÁSCARA DE LINHAS + DUAS ESPECIFICAÇÕES.**
**(1) SOMÁTICA LANÇADA** (fila com portão, 10:09): unidade somática migrada, float64, redução pela representação, 10⁻⁸ (serial + 1
ajudante) e 10⁻¹⁰ (serial + 2 ajudantes), 61 avaliações θ, repousos da cache da distal (mesmo modelo; chave de 10⁻⁸). **Traços
brutos em `results/etapaA_conf/soma64_1e-8` e `soma64_1e-10`, em /home (btrfs, /dev/sda3 — disco real; NUNCA /tmp, que é RAM);
temporários da gravação atômica no mesmo diretório.** Volume: 6.6 MB por subpasso (M3 504 × 1 501 + M5 3 × 23 001, float64) × 122
≈ **0.81 GB**; livre 141 GB. Os 61 subpassos a 10⁻⁸ ficam guardados para a Etapa A (só os 63 extras faltarão).
**(2) REGISTRADO:** 27 de 30 σ avaliáveis entre 10⁻⁸ e 10⁻¹⁰, 10⁻⁸ dentro dos 10% em todos; **os 3 restantes são indistinguíveis de
zero COM UMA ÚNICA UNIDADE DISTAL — o Gram combinado dirá se a somática os determina.** Redução ligada ao caminho único e verificada
(R1–R3). Critério de peso por linha: controles sintéticos passam; nos dados reais o traço passa (5.3%) e as direções fracas 2, 4 e 5
falham, por eventos dendríticos LENTOS do M4 a 1.5 nA (no ponto de injeção, tempo muito não linear; no soma, evento atenuado
abaixo de 20 mV/ms, não detectado, deslocando-se no tempo).
**(3) EVENTOS LENTOS — DUAS ESPECIFICAÇÕES EM VEZ DE UMA ESCOLHA.** NÃO remover a amplitude supralimiar do M4 (sonda a
excitabilidade dendrítica; removê-la muda o protocolo e pode tornar inidentificáveis por construção as direções dos canais ativos
dendríticos). NÃO criar detectores por tipo de evento lento (cada um exigiria verificação própria; a somática traz outro tipo — o
bAP lento nas leituras dendríticas). **ADOTADO:** MÁSCARA DE LINHAS por regra declarada antes, testada com controles sintéticos; a
especificação calculada DUAS vezes — **(i) só com as linhas lineares** (o que Cramér–Rao certifica; conservadora) e **(ii) com
todas** (limite OTIMISTA — a linearização das excluídas não vale); a verdade fica entre as duas; se forem parecidas, os eventos
lentos não importam; se diferentes, a distância é o tamanho do que só uma análise NÃO LINEAR (Etapa B, adiada) resolveria. Reportar
também a fração do peso nas direções fracas que a máscara remove. Mesma lógica da perda dos atributos (item 105); igual na distal e
na somática.
**REGRA DA MÁSCARA, DECLARADA AGORA (antes dos controles e dos dados):** índice da LINHA ρ_r = ‖s_r‖ / ‖d_r‖, com s_r,p = y₊ + y₋ − 2y₀
(segunda ordem) e d_r,p = y₊ − y₋ (primeira ordem), normas euclidianas sobre os 30 parâmetros — pondera pelo tamanho do efeito de
cada parâmetro (um parâmetro de efeito desprezível e curvatura relativa grande não derruba a linha). **Linha EXCLUÍDA se ρ_r >
0.1**; linha com ‖d_r‖ ≤ 10⁻⁶ (sem sinal) fica (não pesa). **Controles sintéticos:** (K1) linha linear em log θ → ρ = 0 → MANTIDA;
(K2) evento (bump) deslocado no tempo por θ, deslocamento ≫ largura → linhas do evento EXCLUÍDAS, linhas da linha de base mantidas;
(K3) o mesmo evento com deslocamento ≪ largura (regime linear) → MANTIDAS — a regra não exclui por excesso.

**112. RESULTADOS (2026-10-13 10:22) — MÁSCARA DE LINHAS: CONTROLES PASSAM, MAS A REGRA DECLARADA (ρ por norma) É CEGA ÀS DIREÇÕES FRACAS;
com a classificação por índice máximo, (i)/(ii) = 0.59–0.96.**
Implementação (UM caminho): `EtapaAUnit.reduce` grava os blocos completos (ii) e só com as linhas lineares (`JtJ_lin`, `JtX_lin`,
`XtX_lin`, `JtDy_lin` — (i)); `linhas_lineares` = a regra do item 111. (Os processos somáticos lançados antes desta edição têm a
redução anterior; os brutos ficam — a redução é refeita offline.)
**Controles sintéticos (`etapaA_mascara_check.py`):** (K1) sem evento → 2 000 de 2 000 mantidas; (K2) evento deslocado ≫ largura →
95% das linhas do evento excluídas, base 100% mantida; (K3) deslocamento ≪ largura → 100% mantidas → **PASSAM**. (Na 1ª rodada o
(K2) "falhou" por ERRO DO CONTROLE: a "base" a > 30 ms ainda tinha a cauda do evento deslocado ±10 ms — a máscara excluía com razão;
traço alongado para 200 ms e base a > 40 ms ≥ 6σ do centro deslocado; regra inalterada.)
**Dados reais (distal float64, 10⁻⁸, M1 + M4), regra DECLARADA (ρ_r por norma sobre os parâmetros > 0.1):** exclui **1 linha** de 11.6
milhões; (i) = (ii) nos 10 menores σ; peso removido nas 5 fracas 0.0–0.4%. **Contradiz o critério de peso** (item 110: linhas não
lineares com 30–45% do peso nas direções 2, 4, 5). **Causa:** a norma sobre os parâmetros é dominada pelos de efeito GRANDE; nas
direções fracas pesam justamente os de efeito pequeno, cuja não linearidade a norma dilui — a regra é cega ao caso que importa, e os
controles K1–K3 não testaram "não linearidade num parâmetro de efeito pequeno que domina uma direção fraca" (o C2 do critério de peso
testava). **Com a classificação por ÍNDICE MÁXIMO por parâmetro (a do critério de peso, item 109):** excluídas 311 301 linhas
(2.68%); 10 menores σ — (ii) todas: 0.000151 0.000284 0.000314 0.000511 0.00102 0.00359 0.0234 0.119 0.149 0.206; (i) sem as não
lineares: 0.000145 0.000169 0.000291 0.000391 0.000728 0.00309 0.0199 0.0828 0.132 0.193; **(i)/(ii) = 0.96 0.59 0.93 0.77 0.71 0.86
0.85 0.69 0.89 0.94** → a distância entre as especificações chega a 41% numa direção fraca: é o tamanho do que só uma análise NÃO
LINEAR (Etapa B) resolveria, nesta unidade. **Decisão pendente (do Martel):** trocar a regra da máscara pela classificação por
índice máximo (coerente com o critério de peso), com um controle a mais (K4: não linearidade num parâmetro de efeito pequeno que
domina uma direção fraca — a regra por norma tem de FALHAR nele, a por índice máximo tem de pegar).

**113. DECISÃO DO USUÁRIO (2026-10-13 12:39) — REGRA DA MÁSCARA TROCADA PARA O ÍNDICE MÁXIMO; K4/K5; VERIFICAÇÃO DIRETA AO LONGO DAS DIREÇÕES
FRACAS; A ESPECIFICAÇÃO É UM INTERVALO.**
**(1) REDEFINIÇÃO APÓS O RESULTADO (rotulada):** linha EXCLUÍDA se o índice de não linearidade MÁXIMO por parâmetro > 0.1 (a MESMA
classificação do critério de peso, item 109). Justificativa independente (do usuário): a máscara existe para remover o que o
critério de peso apontou — as duas têm de classificar nos MESMOS termos; a norma sobre os parâmetros é dominada pelos de efeito
grande e as direções fracas são feitas dos de efeito pequeno. **Os controles ORIGINAIS (K1–K3, pedidos pelo usuário) não cobriam
esse caso.** **K4:** não linearidade num parâmetro de efeito pequeno que domina uma direção fraca — a regra por norma tem de FALHAR,
a de índice máximo tem de PEGAR.
**(2) PONTO CEGO DO ÍNDICE MÁXIMO:** ele perturba UM eixo por vez; uma resposta que depende do PRODUTO de dois parâmetros é linear em
cada eixo e não linear ao longo da diagonal (a derivada cruzada não aparece em teste por eixo); se isso escapar, a especificação (i)
carrega linhas não lineares e deixa de ser conservadora. **K5 (documenta o limite):** linha linear em cada eixo, não linear ao longo
de uma combinação → o índice máximo FALHA — limite conhecido. **VERIFICAÇÃO DIRETA na distal:** com o J, as k = 10 direções mais
fracas v; simular θ ± h·v (2k subpassos) e calcular a linearidade de cada linha AO LONGO de v. **CRITÉRIO DECLARADO AGORA:** em cada
direção fraca, a fração do peso (J_r·v)² nas linhas que a verificação direta classifica como NÃO lineares mas o índice máximo
MANTÉM ≤ 10% → o índice máximo basta; senão, a máscara passa a usar a linearidade ao longo das direções. Rodar quando houver vaga,
sem atrasar a somática.
**(3) RESULTADO DO INTERVALO (registrado):** com o índice máximo, (i)/(ii) nos 10 menores σ vai de 0.59 a 0.96 — até 41% de distância
numa direção fraca. É o PRIMEIRO número sobre quanto a LINEARIZAÇÃO deixa sem resolver. **A especificação da Etapa A será um
INTERVALO entre (i) e (ii), não um número.** Registrado no P53/P54 como o argumento concreto a favor do simulador DIFERENCIÁVEL
(Etapa B pendente de gradiente barato): é ele que fecharia essa distância.

**114. RESULTADOS (2026-10-13 12:43) — MÁSCARA PELO ÍNDICE MÁXIMO (UM caminho) COM K1–K5; VERIFICAÇÃO DIRETA ENFILEIRADA; P53/P54.**
**Implementação:** `etapaA_unit.linhas_lineares` = índice máximo por parâmetro > 0.1 (a regra por norma fica como
`linhas_lineares_norma`, só para o K4); o critério de peso (`etapaA_peso.classifica`) passa a CHAMAR a mesma função — uma
classificação só para a máscara e para o critério (controles do critério de peso re-rodados: passam).
**Controles da máscara (`etapaA_mascara_check.py`):** (K1) 2 000 de 2 000 mantidas; (K2) evento ≫ largura: 95% excluído, base 100%
mantida; (K3) evento ≪ largura: 99.4% mantidas (> 99%); **(K4) curvatura num parâmetro de efeito pequeno numa linha dominada por
parâmetros lineares fortes: a regra por NORMA MANTÉM (falha), a por ÍNDICE MÁXIMO EXCLUI (pega)**; **(K5) y = L·x + c·x_a·x_b (linear em
cada eixo): o índice máximo MANTÉM a linha, ao longo da diagonal o índice é 3.52 → não linear — LIMITE CONHECIDO, documentado.**
**Verificação direta (item 113 (2)) — ENFILEIRADA** (`run_dirs.sh` pela fila com portão; entra quando um processo somático liberar
vaga): (a) as 10 direções mais fracas v do Gram completo da distal (float64, 10⁻⁸); (b) 20 subpassos θ·exp(±h·v) (`etapaA_runner unit
--direcoes`; os repousos desses θ NÃO estão em cache — ~16 min cada → ~7 h num processo); (c) `etapaA_dir_check.py --analise`: critério
do item 113 (peso nas linhas não lineares ao longo de v que o índice máximo mantém ≤ 10% por direção) + base bit a bit.
**P53/P54:** registrado o primeiro número sobre o que a linearização deixa sem resolver (até 41%), a especificação como INTERVALO
entre (i) e (ii), e o argumento concreto a favor do simulador diferenciável.
**Somática (13/10 12:38):** 5 processos desde 10:09–10:39; 10⁻⁸ 2/61, 10⁻¹⁰ 0/61 (1º subpasso no M5); protocolos de um subpasso a 10⁻⁸
sob 5 processos: 60–68 min (estimado 50) → término previsto na MANHÃ DE 15/10.

**117. RESULTADOS (2026-10-16 09:30) — SOMÁTICA COMPLETA (10⁻⁸ e 10⁻¹⁰, 61/61) E VERIFICAÇÃO DIRETA AO LONGO DAS DIREÇÕES: FALHA.**
(1) **Somática:** soma64_1e-8 completa 15/10 23:56, soma64_1e-10 16/10 04:36 (p_soma.npz = só a nota; a redução é feita fora,
item 69 2a — PENDENTE: redução com as máscaras, piso/σ 10⁻⁸ × 10⁻¹⁰, Gram combinado distal + somática). Sem alertas do vigia.
(2) **Verificação direta (item 113 (2), critério declarado: em CADA uma das 10 direções mais fracas do Gram completo (ii) da distal,
fração do peso nas linhas não lineares AO LONGO de v que o índice máximo MANTÉM ≤ 10%):** base da rodada de direções IDÊNTICA bit a bit
à da unidade; 21 subpassos. σ das 10 direções: 0.000152 0.0003 0.000303 0.000509 0.00102 0.00359 0.0234 0.119 0.149 0.206.
Ponto cego por direção (%): 0.00 0.00 0.00 0.00 4.77 0.00 0.00 **17.90** **37.77** 8.36 (não linear ao longo de v: 0.00 0.00 0.08
0.00 4.77 0.00 0.06 23.77 47.20 9.91). **Direções 8 e 9 FALHAM → VEREDITO: o índice máximo NÃO basta** — pela regra declarada, a
máscara passa a usar a linearidade AO LONGO das direções (especificação a decidir). As 7 mais fracas passam (≤ 4.77%); a falha está
nas direções 8–9 (σ ~0.12–0.15) — registrado como fato, NÃO como atenuante (critério vale para as 10).
(3) **Supervisor — defeito observado:** um ajudante --de-tras lançado FORA do supervisor (adotado) que sai com código 0 sem a unidade
pronta não tem a saída observada → o supervisor o vê como FALTA e o relança uma vez. Ocorreu 2× na 10⁻¹⁰ (02:53: saiu em 5 min;
02:59: recalculou soma_decay_mais em dobro com o serial — 1 vaga por ~1.5 h; o encontro serial × ajudante já admite ≤ 1 subpasso em
dobro, resultado idêntico, item 81). Nenhum atraso na conclusão. Correção proposta: trabalho adotado que some sem ficar pronto e cujo
log termina numa linha FIM (o runner a imprime ao sair normalmente) depois do início do processo → tratado como saída 0.

**118. DECISÃO DO USUÁRIO (2026-10-16 ~09:35) — TRÊS DECISÕES; DECLARADO ANTES DOS RESULTADOS (10:00).**
**(1) REDUÇÃO DA SOMÁTICA JÁ.** A decisão de tolerância (piso e σ 10⁻⁸ × 10⁻¹⁰, critério dos itens 75/78) e a especificação (ii) usam
TODAS as linhas — não dependem da máscara; e a máscara nova precisa das direções do GRAM COMBINADO → a redução está no caminho crítico.
Só a (i) espera. **DECLARADO:** objeto = Gram COMBINADO (ii) = distal migrada p_g_apic[60]_32 (M1m + M1p + M4) + somática p_soma (M3 +
M5), float64, representação aprovada (UM caminho, `representar`, as avaliações das DUAS tolerâncias juntas por leitura, base = 10⁻⁸),
blocos somados por linha. piso(10⁻⁸) = ‖J8 − J10‖₂ do combinado; **piso(10⁻¹⁰) = piso(10⁻⁸)/87** — a razão MEDIDA na distal em float64
(item 107; a somática não tem rodada a 10⁻⁶, razão não medida). Usar 87 é CONSERVADOR para o veredito: se a razão real da somática for
menor, o piso real é maior e o conjunto avaliado inclui σ cuja comparação é mais ruidosa → falha espúria, não aprovação espúria.
Avaliável: σ(10⁻¹⁰) ≥ 10 × piso(10⁻¹⁰). **10⁻⁸ BASTA se |σ8/σ10 − 1| ≤ 10% em TODOS os avaliáveis**; os não avaliáveis são RESULTADO
(item 108 (1)). Nota (Weyl): |σ8 − σ10| ≤ piso(10⁻⁸) → acima de 10 × piso(10⁻⁸) o critério passa sozinho; a faixa INFORMATIVA é
[10·piso(10⁻¹⁰), 10·piso(10⁻⁸)] — reportar quantos σ caem nela. Diagnóstico (não decide): distal e somática sozinhas. **Especificação
(ii)** = os menores σ do combinado na tolerância decidida; a parte FUNCIONAL (σ_F = √(gᵀ(JᵀJ)⁻¹g)) precisa do G na tolerância decidida.
**(2) MÁSCARA AO LONGO DAS DIREÇÕES — DIREÇÕES POR RELEVÂNCIA, EXCURSÃO NA ESCALA DA TOLERÂNCIA.** **Registrado:** as direções 8 e 9
falharam com σ 0.12–0.15 — não são as mais fracas; o que decide não é a fraqueza da direção, mas o PESO dela na incerteza do conjunto
funcional. **Direções:** as v_i do Gram combinado (ii); por componente funcional g, c_i = (g·v_i)²/s_i² (independe do ruído); testar em
ordem decrescente de max_g c_i até cobrir ≥ 99% da soma. **Escala:** δ_i = tolerância/|g·v_i| (o g que dá o menor δ_i), com TETO em
log-parâmetro — limite SUPERIOR da escala relevante (conservador); condição clássica de validade da linearização: curvatura medida na
escala da região de confiança. **Critério da linha:** não linear se o índice de 2ª diferença ao longo de v_i, na excursão δ_i, passar de
0.1 em QUALQUER direção testada → excluída. **Controles antes (item 108 (3)):** K1–K5 continuam passando; **K6** — não linearidade de
INTERAÇÃO ao longo de uma direção relevante → PEGA; **K7** — não linearidade só em excursão GRANDE ao longo de uma direção IRRELEVANTE
→ NÃO exclui. **Custo** (repousos novos em θ·exp(±δ_i v_i), compartilhados entre unidades; 2 subpassos por direção por unidade) para a
distal, a somática e a Etapa A — reportado ANTES de rodar.
**DECLARADO (interpretação, antes dos números):** (a) **g = componentes COM tolerância declarada** (D131 7.4: EPSP somático 5% de F0;
tempos de 1º/2º PA 1 ms; taxa f-I 2% de F0); picos de Ca sem tolerância → fora (reportados, como no s*). (b) **NORMALIZAÇÃO:** as c_i de
componentes diferentes têm unidades diferentes (mV², ms², Hz²) — max_g sobre c_i crus mistura unidades. Usa-se a FRAÇÃO por componente,
f_gi = c_gi / Σ_j c_gj (adimensional, independe do ruído e da unidade); ordem decrescente de max_g f_gi; para no MENOR prefixo em que
Σ_{i escolhidas} f_gi ≥ 0.99 para TODO g. (c) **Teto:** δ_i·max_p |v_ip| ≤ ln 2 (nenhum parâmetro sai do fator 2); **piso:** δ_i ≥
h = ln 1.01 (abaixo de h a 2ª diferença fica no piso numérico — o passo por eixo já validado; maior excursão é conservadora). (d) Linha
sem sinal ao longo de v_i (|y₊ − y₋| ≤ D_MIN) não conta naquela direção (como no índice por eixo). (e) **O G na tolerância decidida NÃO
existe** (o único G.npz é de 06/10: repouso de 3 s, taxa por contagem — objeto anulado). Pelo item 95 (2) ele é calculado UMA vez na
tolerância decidida; o conjunto de direções DECISIVO depende dele. Antes dele, uma contagem com o G velho é só ESTIMATIVA (rotulada).
(f) **Etapa A:** as direções vêm do Gram da Etapa A INTEIRA → só existem depois dos subpassos θ de todas as unidades → os 2·n_dir
subpassos por unidade são uma SEGUNDA passada.
**(3) CORREÇÃO DO SUPERVISOR — APROVADA:** adotado que some sem ficar pronto, com o log terminando em FIM = saída normal, não relançar;
registrar no log; testar com o caso ocorrido.

**119. RESULTADOS (2026-10-16 10:25) — TOLERÂNCIA DECIDIDA PELO GRAM COMBINADO: 10⁻⁸; CONTROLES K1–K7 PASSAM; DIREÇÕES (ESTIMATIVA) E
CUSTO; SUPERVISOR CORRIGIDO.**
**(1) Redução e tolerância** (`etapaA_comb64.py`, `comb64_grams.npz`, `comb64.json`; 5 min, pico 110 MB; lançada pelo supervisor quando a
porta abriu). Somática: 419 527 linhas; 343 leituras com disparo, **195 com os tempos FORA por identidade** (bAP nas leituras dendríticas;
fica a voltagem antes do 1º disparo). Distal: 11 603 097 linhas.
| objeto | piso(10⁻⁸) | avaliáveis (faixa informativa) | 10 menores σ (10⁻⁸) | pior |σ8/σ10 − 1| | veredito |
|---|---|---|---|---|---|
| **COMBINADO (decide)** | 6.0 | **30 de 30** (5) | 14.6 17.3 21.9 25.5 39 67.9 122 205 249 259 | **0.69%** (k = 2) | **10⁻⁸ BASTA** |
| distal sozinha | 0.0037 | 27 de 30 (4) | 0.00015 0.00028 0.00031 0.00051 0.0010 0.0036 0.023 0.12 0.15 0.21 | 7.26% (k = 4) | basta (diagn.) |
| somática sozinha | 6.0 | 30 de 30 (6) | 2.15 3.33 15.0 15.4 24.3 38.4 63 113 172 221 | 3.80% (k = 1) | basta (diagn.) |
**Conferência com resposta conhecida:** a distal sozinha reproduz o item 110 (27 de 30; 7.26% ≈ 7.3%). **TOLERÂNCIA DECIDIDA: 10⁻⁸.**
**Diagnósticos (não decidem):** (a) o piso somático (6.0) mora nas direções FORTES; ao longo das 2 mais fracas da somática SOZINHA o erro
numérico ‖ΔJ·v‖ é 0.59 / 0.53 = **28% / 16% do σ** (o σ quase não muda porque o erro entra em 2ª ordem) — a somática sozinha não resolve
bem as suas direções fracas a 10⁻⁸; (b) **no COMBINADO: ‖ΔJ·v_k‖/σ_k ≤ 4.4% nas 10 mais fracas e as direções v_k ficam a ≤ 1.05° entre
10⁻⁸ e 10⁻¹⁰** — as direções da máscara são estáveis na tolerância decidida; (c) como no item 98 (a), o combinado é dominado pela
somática (σ_min 14.6; a distal ≤ 1) — as direções fracas da distal são bem determinadas pela somática; (d) a razão 87 (distal) foi
usada para a somática, não medida (sem rodada a 10⁻⁶) — conservador para o veredito (item 118 (1)).
**Especificação (ii)** (todas as linhas, 10⁻⁸): σ = 14.6 17.3 21.9 25.5 39 67.9 122 205 249 259 … (por unidade de ruído σ_V); a
parte funcional (σ_F por componente) espera o G na tolerância decidida.
**(2) Máscara ao longo das direções** (`etapaA_unit.direcoes_relevantes / excursoes / linhas_lineares_direcoes` — a mesma regra do
índice, aplicada às direções). **Controles** (`etapaA_mascara_check.py --controles`): K1–K5 continuam passando; **K6** (interação pura
x_0·x_1, índice ao longo de u = 0.50; u de σ INTERMEDIÁRIO, a mais fraca w irrelevante): seleção pega u e deixa w; por eixo MANTÉM (cego),
por direções EXCLUI; 399 de 399 lineares mantidas; **K7** (não linear só além de 0.3 ao longo de w, a mais FRACA e irrelevante): MANTÉM —
contraprova: índice ao longo de w no teto 5 246 (uma regra pelas mais fracas a excluiria); **K7b** (ao longo da relevante u, só além de
0.2 > δ_u = 0.05): MANTÉM — contraprova no teto 1 839. **→ PASSAM.** Defeito do controle corrigido antes do resultado: a 1ª versão do
K6 punha o índice em 20 (fácil demais); refeito com 0.50, perto do limiar.
**Direções — ESTIMATIVA (G VELHO de 06/10: 48 EPSP + BAC_PA2 + CaBurst_PA1 com tolerância; SEM a taxa f-I; objeto anulado):** **21 de 30
direções** cobrem ≥ 99% de toda componente (pior: CaBurst_PA1 99.14%); escolhidas: v_5 v_4 v_1 v_3 v_2 v_6 v_16 v_10 v_8 v_22 v_7 v_11 v_21
v_12 v_19 v_9 v_14 v_18 v_13 v_23 v_15 — as 6 mais fracas e 15 de σ 122–7 160; **excursões δ = 0.04–0.99 em log** (uma no teto: v_2;
nenhuma no piso h) — 4 a 100× o passo por eixo (h = 0.01): as tolerâncias funcionais são largas. Picos de Ca não mudam a contagem.
**O conjunto DECISIVO precisa do G a 10⁻⁸** (item 95 (2)). **RISCO (não medido):** a excursões de até fator 2 numa combinação, o modelo
pode não ter repouso estável (disparo espontâneo) → repouso não converge → aquela direção NÃO AVALIADA (nunca aprovada).
**Custo (ESTIMATIVA, 1 direção = 2 subpassos; medidos nesta semana sob disputa de 5 processos: subpasso distal de direção 14.9 min COM
repouso novo → repouso ≈ 12 min, protocolos ≈ 3 min (item 96); subpasso somático 71–77 min):** por direção: repousos 0.4 h (uma vez,
compartilhados), distal 0.1 h, somática 2.5 h. Com 21 (30) direções: **distal ≈ 10.5 h (15 h) de CPU com os repousos; somática ≈ 52 h
(74 h); Etapa A a s = 400 (20 unidades distais + somática) ≈ 102 h (146 h) ≈ 26 h (37 h) de relógio** — +24–35% sobre os 17.5 dias-CPU
do item 96; s = 200: +107 h nas distais; s = 100: +250 h. **Pré-requisito: o G a 10⁻⁸** — 61 avaliações; medido no G2 (10⁻⁶): 32–37
min por avaliação com repouso novo (o modelo do G tem nós nos sítios funcionais → repousos próprios) → ×1.37 a 10⁻⁸ ≈ 45–50 min →
**~46–51 h de CPU (o item 96 estimava 88 h)**, ~12 h de relógio com 5 processos. **Observação:** os subpassos de direção desta checagem
(distal + somática) NÃO servem à Etapa A (as direções da Etapa A vêm do Gram dela inteira — item 118 (2f)); a somática da checagem
(~52 h) só se paga se a máscara for decidida também aqui, antes da Etapa A.
**(3) Supervisor:** adoção ESTÁVEL + saída normal de adotado pelo FIM no stdout REAL (/proc/<pid>/fd/1). **Teste com o caso ocorrido**
(dois ajudantes de linha idêntica lançados fora; A sai com FIM, B some depois sem FIM): 1ª versão FALHOU no teste — o trabalho de A,
ao perder o processo, "herdou" B, e o de B foi relançado (a troca de 16/10); corrigido (o processo adotado fica RESERVADO ao dono);
refeito: A → "SAÍDA NORMAL … termina em FIM → não relançado"; B fica com o MESMO trabalho até sumir → "SUMIU SEM FIM → relançável" →
relançado (3×, e para). Controles anteriores passam; serviço reiniciado com o código novo.

**120. DECISÃO DO USUÁRIO (2026-10-16 ~10:40) — G A 10⁻⁸ AGORA; MÁSCARA POR DIREÇÕES SÓ NA DISTAL, DEPOIS DO G; OS 195 bAPs SEM TEMPO.**
**(0) REGISTRADO: TOLERÂNCIA DECIDIDA PELO GRAM COMBINADO = 10⁻⁸** (30 de 30 σ avaliáveis, pior |σ8/σ10 − 1| = 0.69%; item 119).
**Fecha a linha 4 da tabela do preprint.** Supervisor: correção aprovada como está; o teste que pegou o defeito da 1ª versão fica no
repositório (`hanu_supervisor_teste_adotado.sh`).
**(1) G A 10⁻⁸ — LANÇADO pelo supervisor** (pré-requisito, item 95 (2), da contagem decisiva de direções e da Etapa A): `etapaA_runner.py G
results/etapaA_G8 --atol 1e-8 --cache results/etapaA_G8/cache --sub-worker k/5` (k = 0…4; repartição FIXA dos subpassos em vez de
ajudantes --de-tras: o serial não vê as travas dos ajudantes no G, que não grava parcial; cada processo com linha distinta); tipo da
porta 'distal' (500 MB; pico do G ainda não medido — gravado no FIM). Estimativa ~46–51 h de CPU, ~12 h de relógio.
**(2) MÁSCARA POR DIREÇÕES: SÓ NA DISTAL, DEPOIS DO G.** As direções e os δ dependem do G; o atual é de 06/10, sem a taxa da f-I. ORDEM:
G → máscara na DISTAL (~10.5 h) com as direções e δ FINAIS. Entrega: (a) quanto a especificação (i) encolhe com a máscara correta;
(b) teste REAL do risco de repouso instável em excursão de fator 2 — depende só de θ, não da unidade → a distal o cobre inteiro.
Direções sem repouso estável: NÃO AVALIADAS, reportar quantas. A somática NÃO roda a máscara nesta checagem (tolerância já decidida;
a Etapa A rodará a máscara com as direções dela).
**(3) OS 195 bAPs SEM TEMPO** (amplitude e tempo do bAP nos dendritos = a informação sobre canais dendríticos). (a) DIAGNÓSTICO sem simular:
nessas leituras, a dV/dt máxima do bAP na base × o limiar de detecção (20 mV/ms), e quantas mudam de "detectado" para "não detectado"
entre θ e θ ± h. HIPÓTESE (não conclusão): limiar fixo, calibrado para o disparo somático, perto da subida máxima de um bAP atenuado —
artefato da definição do detector. Reportar antes de propor correção. (b) VERIFICAR se os tempos descartados por identidade ficam fora
também da especificação (ii); se sim, a (ii) não é o limite de cima. PROPOSTA: na (ii), incluir as linhas BRUTAS de voltagem dessas
leituras (coerente com a (ii), que já aceita linearização inválida); reportar o efeito nos σ do combinado ANTES de adotar.

**121. DECLARADO ANTES DA RODADA (2026-10-16 16:30) — MÁSCARA POR DIREÇÕES NA DISTAL: CÓDIGO, STATUS "NÃO AVALIADA", ANÁLISE; CADEIA NO
SUPERVISOR.** (1) **Código** (`etapaA_unit`): `--direcoes <npz>` aceita as direções E as excursões δ_i do `etapaA_dir_rel` (o `.npy` antigo
segue com o passo h); componentes do G NÃO condicionadas ficam fora da relevância (reportadas). **Subpasso de direção sem repouso/autoteste**
(AutotestFailed: repouso não converge em 60 s pela Euler implícita, deriva > 0.01 mV em 1 ms no reassentamento, ou autoteste do construtor) →
gravado `nao_avaliado` com o motivo, a rodada SEGUE (nos outros subpassos a regra continua sendo PARAR). **Features:** corte (1º disparo) e
identidade definidos SÓ por base + eixos (`representar_extra`) — as excursões, que podem adiantar disparos, NÃO mudam as features do Gram;
um atributo cuja identidade falha na excursão → NaN → linha EXCLUÍDA (sem isso, NaN passaria por "sem sinal": controle K8). Refatoração
de `representar` (extração por avaliação em `_feat_disparos`, usada pelos dois caminhos) — **controle: Gram somático refeito = comb64 BIT A
BIT; `representar_extra` com cópias = `representar` (0 diferenças em 504 leituras) → PASSA.** Controles da máscara K1–K8 PASSAM; caminho
NÃO AVALIADA testado (direção → gravado; base → continua parando).
(2) **STATUS por direção (declarado):** NÃO AVALIADA se um dos dois subpassos (a) gravou `nao_avaliado`, ou (b) mostra repouso instável no
trecho PRÉ-ESTÍMULO do M1 (100 ms sem estímulo): |V − V_pré| > 0.1 mV ou disparo detectado em qualquer leitura (a Euler implícita pode
convergir para um equilíbrio INSTÁVEL; a deriva de 1 ms do reassentamento pode não ver). Reportar quantas e por quê.
(3) **Máscara (decide, como especificado no item 118 (2)):** linha excluída se não linear (índice > 0.1 na excursão δ_i, ou NaN) em QUALQUER
direção AVALIADA. Especificações da distal: (ii), (i)_eixo (em uso), (i)_dir (decide), (i)_dir ∧ eixo (diagnóstico). Direções NÃO
AVALIADAS → a (i)_dir não está certificada nelas (registrado, nunca aprovado). **Teste da análise com resposta conhecida** (rodada de 10
direções de 13/10, passo h): base idêntica; 10 de 10 avaliadas; (ii) = a distal do comb64 (3 algarismos); (i)_eixo/(ii) = 0.59–0.96
(item 113) → confere.
(4) **Cadeia no supervisor:** G a 10⁻⁸ (5 processos `--sub-worker`) → `dirrel` (direções e δ FINAIS, rótulo DECISIVO) → `mask_s0…4`
(unidade distal p_g_apic[60]_32, `--direcoes direcoes_rel.npz`, cache de repousos compartilhada `cache_1e-8`) → `mask_analise`.

**122. RESULTADOS (2026-10-16 16:30) — OS 195 bAPs SEM TEMPO; LINHAS BRUTAS NA (ii); SUSPENSÃO → BOOT FRIO DE NOVO; PORTA VIOLADA (meu erro).**
**(1) Diagnóstico dos bAPs** (`etapaA_bap_diag.py`, `etapaA_bap_extra.py`, sem simular; 193 do M3 + 2 do M5 = 195): **a hipótese do limiar NÃO
se sustenta.** As leituras com tempos fora são PROXIMAIS (25–175 µm, mediana 100; as mantidas: 150–417 µm); o bAP na base tem dV/dt máx
31 / 84 / 367 mV/ms (p5/p50/p95; limiar 20) e proeminência 38 / 52 / 91 mV — longe do limiar. Causa: **IDENT_A_MAIS em 189 de 193** (MENOS:
3; NÍVEL: 1) — um **2º DISPARO REAL** aparece em exatamente **2 das 60** avaliações θ ± h (**cm_dend e apic_NaTa_t**), ~15 ms depois do
estímulo (64.6–65.5 ms no traço), dV/dt 23 / 58 / 207 mV/ms; **na base, na mesma janela, NADA** (dV/dt ≤ 0.8 mV/ms, proeminência 2–7 mV).
A base está PERTO DO LIMIAR DE UM 2º DISPARO; ±1% nesses dois parâmetros o cria. Nas leituras distais o 2º bAP não passa do detector → o
1º fica. Com K = 1, a regra de contagem até o horizonte (item 102: tb + ½·min(tb, T − tb) ≈ 78 ms) RECUSA a leitura inteira, embora o 1º
disparo não mude de identidade. **(2) (ii) — VERIFICADO: os tempos descartados ficam fora também da (ii)** (`representar` devolve só a
voltagem antes do corte para as duas especificações) → **a (ii) NÃO é o limite de cima**. **Efeito da proposta nos σ do combinado (controle:
variante sem bruta = comb64 bit a bit):** M3 bruta inteira (193 linhas) → razão 1.04–1.22 nos 12 menores (piso 6.0 → 6.9; 10⁻⁸ × 10⁻¹⁰ pior
0.64%); **M3 bruta só até 63 ms (1º bAP inteiro, SEM o 2º disparo) → 1.02–1.09** — ~metade do ganho da bruta inteira vem do 2º disparo
(diferença "PA × sem PA" em 2 colunas, artefato de contagem); M3 + M5 bruta (os 2 trens de 2 s no soma) → 6–47× (diagnóstico: é a
diferença "PA × sem PA" que o item 101 tirou da representação). NÃO adotado — decisão do Martel.
**(3) SUSPENSÃO → BOOT FRIO (2ª vez):** 16/10 10:53:19 suspensão pedida pela sessão (logind; máquina OCIOSA — o G esperava a porta, nada
rodava) → boot frio 27 s depois (fsck), igual a 14/10 11:54; as suspensões de 14/10 16:51 e 15/10 00:42 voltaram normalmente; a da tela de
login 16/10 11:09 → 15:51 também. Causa NÃO determinada; configuração de energia do GNOME NÃO tocada (decisão do Martel). **Primeiro teste
REAL da retomada:** sem linger, o supervisor só voltou no login (15:52, 5 h depois — a máquina ficou na tela de login) e então retomou a
fila (G8 lançado 16:15, com a porta). **(4) ERRO MEU — PORTA VIOLADA:** o 1º diagnóstico dos bAPs rodou com a porta FECHADA (swap-in 186
pg/s) — `check; comando` em vez de `check && comando` (o mesmo erro já registrado). Processo leve (análise, ~100 MB), mas a regra vale para
todo lançamento; os seguintes passaram a esperar a porta (`until check; do sleep; done`). E um script MEU (espera_brutas.sh) foi EDITADO
enquanto rodava (o bash lê por deslocamento) → parado pelo PID gravado e relançado limpo.

**123. DECISÃO DO USUÁRIO (2026-10-16 ~16:45) — QUATRO ITENS (não interromper o G) — E RESULTADOS (2026-10-17 09:20).**
**(1) IDENTIDADE SÓ NO TRECHO DAS GRANDEZAS USADAS.** Hipótese do limiar de 20 mV/ms REFUTADA (item 122). **REGRA, com argumento
independente:** um disparo POSTERIOR à última grandeza usada não pode alterar as grandezas usadas; a verificação cobre SÓ o trecho delas.
Em `representar` as grandezas são os tempos dos K disparos da base (+ a voltagem antes do 1º) → `_identidade`: (a) deslocamentos como
antes (K = 1: |d_1| < ½·min(tb_1, T − tb_1); K ≥ 2: consecutivos, item 95); (b) NENHUMA INSERÇÃO até o K-ésimo — para i = 1…K, o
disparo da avaliação mais próximo da posição prevista tb_i + d_{i−1} (acompanha a deriva) é o casado; (c) NADA depois do K-ésimo (a
contagem até o horizonte do item 102 saiu). Nas leituras da taxa f-I do G (`etapaA_F.identidade`) continua cobrindo os K+1 primeiros —
inalterado. **Controles** (`etapaA_ident123_check.py`, 15 casos + ponta a ponta por `representar`): K = 1 com 2º disparo 13 ms DEPOIS →
MANTIDA (a regra anterior recusava); inserção 5 ms ANTES do 1º → RECUSADA; trem K = 40: escala 1.01/1.03 e deslocamento 2 ms → MANTIDA;
extra 10 ms depois do K-ésimo → MANTIDA (anterior: recusava); inserção no meio, 5 ms antes de um usado, dupleto antes do K-ésimo, remoção,
menos de K → RECUSADA; **escala 1.03 + inserção no meio → RECUSADA — a regra ANTERIOR a MANTINHA (buraco achado pelo controle)**;
ponta a ponta: 2º disparo depois → tempos ENTRAM, disparo antes → SAEM → **PASSAM**. K1–K8 continuam passando. `etapaA_rep_check`:
V1, V3, V4, V5 (inserção → atributos saem) ok; V2 limiar 460% / pico 13% FALHAM como já registrado no item 104 (atributos fora) —
inalterado. **CONDICIONAMENTO (registrado):** a M3 está perto do limiar de um 2º disparo (cm_dend e apic_NaTa_t a ±1% o criam) —
grandezas depois do 1º bAP seriam mal condicionadas ali; a representação já as exclui.
**(2) ESPECIFICAÇÃO (ii) — DEFINIÇÃO:** a (ii) é o limite superior DENTRO DA REPRESENTAÇÃO. Voltagem bruta depois de um disparo,
linearizada, não é informação utilizável (o 6–47× do M5 mostra isso); a forma depois do disparo, excluída de propósito, tem medida
própria (item 105 (3)). **Linhas brutas NÃO adotadas.** **VERIFICAÇÃO com a regra nova** (`comb64_v123_grams.npz`, lançado pela porta
quando a 1ª vaga do G abriu, 09:07): tempos FORA na somática **195 → 6**; σ do combinado com os tempos recuperados / atual =
**1.02 1.01 1.06 1.04 1.01 1.04 1.01 1.02 1.02 1.02 1.03 1.00** × M3 bruta até 63 ms / atual = 1.04 1.02 1.08 1.04 1.02 1.08 1.03 1.09
1.02 1.09 1.05 1.04 → tempos / bruta-63 = **0.93–1.00** (8 de 12 ≥ 0.98) → **os tempos capturam quase toda a informação do 1º bAP**.
Distal idêntica (bit a bit). Tolerância com a identidade nova (diagnóstico): 30 de 30 avaliáveis, pior 0.71% → **10⁻⁸ segue**. As
direções da máscara passam a vir do combinado NOVO (`comb64_v123_direcoes.npz`; trabalho `dirrel` reapontado antes de começar).
**(3) INIBIDOR DURANTE A ESPERA.** O boot frio de 16/10 aconteceu porque, com a porta fechada, nada rodava e nenhum inibidor estava
ativo. O supervisor segura um inibidor próprio (`systemd-inhibit --what=sleep:idle --who=HANU-supervisor … sleep infinity`, sessão
própria, PID gravado) SEMPRE QUE HOUVER TRABALHO PENDENTE: rodando, por lançar (não desistido), ou esperando algo que ainda pode chegar;
com a chave de pausa e nada rodando, ou com a fila vazia, LIBERA; libera no SIGTERM e numa queda; inibidor velho de uma queda é recolhido
na partida. **Teste** (`hanu_supervisor_teste_inibidor.sh`): pendente → 1 na lista; pausa sem nada rodando → 0; pausa retirada → 1; fila
vazia → 0; pendente de novo → 1; SIGTERM → 0 e nenhum processo do grupo → **PASSA**. Serviço real reiniciado (o G NÃO foi interrompido:
os 5 processos vivos antes e depois, readotados): "INIBIDOR ATIVO (5 rodando, 0 por lançar, 7 esperando)". **Registrado: segundo boot
frio após suspensão em 2 dias, causa não determinada; configuração de energia do GNOME: decisão do Martel, não mexer.**
**(4) A PORTA EM CÓDIGO, NÃO EM TEXTO.** O erro do ";" se repetiu apesar do registro e da memória — ambos texto. **PONTO ÚNICO:**
`neuron/lancar.py <tipo> [--esperar] -- <comando>` confere a porta; fechada → NÃO lança (código 75) ou espera; aberta → HANU_PORTA = o
próprio PID e exec (registro em results/porta/lancamentos.log). **Guarda** `neuron/porta.py`, importada por etapaA_model, stim_common e
etapaA_runner (todo processo pesado e todo diagnóstico que lê/simula com eles): recusa (código 77) processo que não descende de um
lançamento pelo ponto único. As filas (supervisor, mem_gate fila, etapaA_fila, preempcao, ref_ii_C_retomada) lançam CADA processo por
`lancar.via_porta` (que só volta depois do exec ou da recusa — nunca vários esperando juntos); o supervisor não confere mais a porta por
conta própria. Tipo `teste_fechada` (orçamento 10⁹ MB) só para testar a recusa. **Teste com a porta fechada** (`porta_teste.sh`): (T1)
lancar com a porta FECHADA → 75, o script NÃO rodou; (T2) lançamento direto → 77; **(T3) o erro do ";" (check fechada; comando) → 77**;
(T4) HANU_PORTA de processo não ancestral → 77; (T5) porta aberta → roda (K1–K8 passam); (T6) runner pela porta (re-execução sob o
inibidor = descendente) → roda; (T7) passo de um script bash lançado pela porta → roda → **PASSA**. **LIMITES (registrados):** um
processo lançado pela porta pode rodar passos EM SÉRIE como descendentes (por desenho: run_dirs.sh, o vigia); filas que lançam em
PARALELO usam via_porta para cada um; um HANU_PORTA forjado com o PID de um ancestral passaria (a guarda é contra o erro, não contra
forja deliberada). Ordem ESTRITA do supervisor: o 1º trabalho recusado pela porta segura os seguintes (desenho; o teste foi ajustado).
**G a 10⁻⁸ (não interrompido):** 57 de 61 subpassos em 17/10 09:10; ~2 h por subpasso (1º com construção ~2 h; a estimativa de ~50 min
a partir do G2 a 10⁻⁶ estava errada) → previsão revista ~20–26 h de relógio; `G8_s1` terminou a sua parte às 09:06 → "SAÍDA NORMAL de
adotado (FIM no log) → não relançado" — a correção do item 118 funcionando em uso real.

**124. RESULTADOS (2026-10-17 09:40) — G A 10⁻⁸ E AS DIREÇÕES DECISIVAS DA MÁSCARA.** **G** (`results/etapaA_G8/G.npz`): 61 subpassos em 5
processos (`--sub-worker`), 16/10 16:15 → 17/10 09:26 (~17 h de relógio; ~2 h por subpasso — a estimativa de ~50 min estava errada); pico
~150–160 MB por processo (o orçamento 'distal' de 500 MB cobre); os 5 encerrados como "SAÍDA NORMAL de adotado" pelo FIM. 55 componentes
(48 EPSP, BAC_PA2, CaBurst_PA1, 2 picos de Ca, 3 taxas); K = 24 / 29 / 40 (= item 97). **54 condicionadas; `taxa_1.9` NÃO condicionada**
(identidade dos K+1 = 41 primeiros: pior razão 8.5): quebra em **cm_dend_mais (8.50) e apic_NaTa_t_menos (8.20)** — 43 disparos × 42 —
os MESMOS dois parâmetros que criam o 2º disparo na M3 (item 122): o modelo em θ_verd está perto de uma BIFURCAÇÃO de contagem nesses
dois; e_pas_mais também (1.54). → `taxa_1.9` = NÃO AVALIADO no s* e fora da relevância das direções. (Rótulo enganoso no etapaA_dir_rel:
"não finitas FORA" listava também as não condicionadas — corrigido para "não finitas ou não condicionadas".) **Direções DECISIVAS** (`direcoes_rel.npz`, combinado NOVO do item 123):
**25 de 30**, cobertura ≥ 99.23% em toda componente (pior EPSP_sorteio_29); entram agora as taxas a 0.78 e 1.0 nA e o BAC_PA2 (o G velho
não as tinha); **7 no TETO (fator 2; δ 1.03–1.29 em log)**, 18 pela tolerância (δ 0.03–0.83), nenhuma no piso h. Custo na distal: 50
subpassos (~12.5 h de CPU, ~3 h de relógio com 5 processos) — lançados pelo supervisor.

**125. RESULTADOS (2026-10-17 16:30) — MÁSCARA POR DIREÇÕES NA DISTAL: 25 DE 25 AVALIADAS (repouso estável até o fator 2); A (i) COLAPSA
— 91% DAS LINHAS EXCLUÍDAS.** Rodada `dirsrel64_1e-8` (50 subpassos θ·exp(±δ_i v_i), 5 processos pela porta, 17/10 09:33 → 14:08;
análise 14:10). **(1) Status:** **25 de 25 AVALIADAS, 0 NÃO AVALIADAS** — repouso convergido e trecho pré-estímulo estável em TODAS,
inclusive as 7 no teto (fator 2): o risco de repouso instável (depende só de θ) NÃO se materializou na escala das excursões. Base
idêntica à da unidade (bit a bit). **(2) Máscara (decide, item 118 (2)):** linhas excluídas **10 580 013 de 11 603 097 (91.2%)** — M1m
5.28 M, M1p 5.28 M (~91% de cada), M4 11 766; **(i)_dir: 10 menores σ = 0, 1.1e-7 … 4.3e-7 → razão (i)/(ii) ≈ 0 em TODAS** (a (i) por eixo,
em uso: 2.68% excluídas, razão 0.59–0.96). Linhas não lineares por direção: as de δ pequeno (v12, v19, v20, v22, v24, v25: δ ≤ 0.19)
excluem 18 k–124 k; as de δ grande, ~7–10.5 M (v1–v4, v6, v7 no teto; v5 δ 0.67: 10.4 M; v9 0.54: 7.9 M; v10 0.31: 7.4 M; v11 0.83:
7.6 M; v14 0.60: 7.4 M). **Diagnóstico (não decide) `--sem-teto`** (só as 18 limitadas pela tolerância): 91.1% excluídas — **o colapso
NÃO vem do teto**, vem das excursões que a própria tolerância permite (δ 0.2–0.8 em log = 20–120% nos parâmetros). **Leitura (não
decide):** para uma dependência suave y ∝ e^{a·x} ao longo de v, o índice de 2ª diferença é tanh(aδ/2) → com δ = 0.5 passa de 0.1 para
qualquer sensibilidade logarítmica a > 0.4 (o M1 sublimiar escala com a resistência de entrada, a ~ 1). Na escala da tolerância o índice
POR LINHA recusa toda dependência física comum — inclusive a não linearidade de PARÂMETRO (curvatura que uma reparametrização da
grandeza, ex.: log da amplitude, removeria), que não é a mesma coisa que a curvatura INTRÍNSECA da superfície de expectativa (a que
invalida a linearização do estimador; Bates & Watts 1980). **Conclusão registrada:** com a regra declarada, a especificação (i) na escala
da tolerância é VAZIA — a Etapa A não pode ser certificada por Cramér–Rao linear nas direções relevantes; o intervalo (i)–(ii) vira
[0, (ii)]. Decisão do Martel sobre o próximo passo (o critério, a escala, ou o método não linear — P53/P54, simulador diferenciável).
**(3) Reinícios de 17/10 14:10:59 e 14:16:42:** "The system will reboot now!" — reinício PEDIDO, seguido de regeneração do initramfs
(dracut, kernel 7.2.8 → 7.2.11) e novo reinício: ATUALIZAÇÃO DO SISTEMA, não queda; a análise gravou às 14:10, antes; o supervisor
parou ordenadamente (inibidor liberado) e voltou no login (16:08); nada pendente na fila.

**126. DECISÃO DO USUÁRIO (2026-10-19) — TROCAR O ÍNDICE POR LINHA PELA CURVATURA INTRÍNSECA RELATIVA (Bates & Watts), SEM SIMULAR DE
NOVO; DECLARADO ANTES DOS NÚMEROS.**
**(1) REGISTRADO:** a máscara por direções na escala da tolerância excluiu 91% das linhas e zerou a (i). Causa: o índice POR LINHA, numa
excursão de 20–120% nos parâmetros, recusa qualquer dependência suave — MISTURA curvatura de PARAMETRIZAÇÃO (removível por
reparametrização, não invalida a estimativa) e curvatura INTRÍNSECA (a que invalida a linearização). **A combinação escala-da-tolerância
+ índice-por-linha foi pedida pelo Martel; o critério estava MAL POSTO → CRITÉRIO INVÁLIDO, não resultado sobre o neurônio** (o item 125
fica como registro do critério inválido; a "(i) vazia" NÃO vale como conclusão). O repouso foi estável até o fator 2 em 25 de 25 direções:
o risco não se materializou. taxa_1.9 NÃO AVALIADO (identidade 8.5; quebra em cm_dend e apic_NaTa_t): o modelo no θ verdadeiro está perto
de uma bifurcação na contagem de disparos a 1.9 nA — os mesmos parâmetros do 2º disparo da M3. Os reinícios de 17/10 foram atualização
do kernel; o supervisor parou e voltou em ordem — segundo teste real.
**(2) DECLARADO — CURVATURA INTRÍNSECA RELATIVA POR DIREÇÃO** (dados gravados: unidade distal migr64_1e-8 + rodada dirsrel64_1e-8; 25
direções relevantes v_i com excursões δ_i): por linha r, aceleração a_r = (y₊ + y₋ − 2y₀)/δ_i² ao longo de v_i (features pelo UM caminho,
`representar_extra`, corte e identidade de base + eixos); parte INTRÍNSECA = componente de a fora do plano tangente (espaço das colunas
de J): ‖a_N‖² = ‖a‖² − (Jᵀa)ᵀ(JᵀJ)⁻¹(Jᵀa); curvatura intrínseca K^N_i = ‖a_N‖ / ‖J v_i‖²; relativa γ^N_i = K^N_i · ρ, ρ = σ√p (Bates &
Watts). **LIMITE (declarado agora, fonte):** γ^N_i · √F(p, ν; 0.95) ≤ **0.3** para TODA direção relevante — "relative curvatures
multiplied by sqrt(F) … if either exceeds some threshold (0.3 has been suggested) the curvature is unacceptably high for the planar
assumption" (documentação de `rms.curv`, pacote MASS, Venables & Ripley, implementando Bates & Watts 1988 §7.3) — **fonte SECUNDÁRIA
conferida; a primária (B&W 1980 / 1988) NÃO foi acessada**; o 1/(2√F) que eu lembrava do artigo de 1980 NÃO foi conferido e NÃO é usado.
p = 30; ν = n − p ≈ 1.2×10⁷ → F = 1.4591, √F = 1.2079 (calculado). **σ_lin = 0.3 / (√F · √p · max_i K^N_i)** — o MAIOR ruído (mV, por
linha) com a curvatura intrínseca relativa abaixo do limite em TODAS as 25 direções; por direção, σ_lin,i. Diferenças em relação a B&W
(registradas): (a) B&W usam o RMS (ou o máximo) sobre TODAS as direções; aqui o MÁXIMO sobre as 25 RELEVANTES (as outras não importam para
o funcional; o máximo é mais exigente que o RMS); (b) a aceleração é a 2ª diferença na excursão δ_i (secante, inclui ordens mais altas),
não a derivada local — sem simular de novo; (c) **a SOMÁTICA não tem rodada de direções (item 120 (2)): a parte somática da aceleração
NÃO é medida.** Dois números: (A) DISTAL SOZINHA (plano tangente e ‖Jv‖ da distal) — curvatura completa desse subproblema; (B)
COMBINADO PARCIAL (plano tangente e ‖Jv‖ do Gram combinado distal + somática, aceleração somática tomada como ZERO) — rotulado PARCIAL.
Linhas com NaN numa excursão (identidade de disparo falhou: descontinuidade) ficam fora e são CONTADAS por direção. Também reportada (não
decide) a curvatura de PARÂMETRO K^T = ‖a_T‖/‖Jv‖². **σ*** (Cramér–Rao linear, item 13/26, `etapaA_sstar` x̂_V): σ* = min_g tol_g /
(1.645 · σ_F,g(σ = 1)), σ_F,g = √(gᵀ(JᵀJ)⁻¹g), Gram combinado (ii), G a 10⁻⁸, as 52 componentes com tolerância e condicionadas — SEM o
termo de viés (não existe na tolerância decidida) → é um limite de CIMA de σ*. σ* ≤ σ_lin → especificação linear CERTIFICADA no próprio
nível que exige; σ* > σ_lin → exigência real entre σ_lin e σ* (só análise não linear fecha). **Controles antes (item 108 (3)), pelo mesmo
código:** K9 — duas linhas iguais a θ² (curva das respostas = reta) → K^N = 0 → APROVA (e K^T ≠ 0: a curvatura de parâmetro é ignorada);
K10 — linhas θ e θ² (parábola) → K^N = curvatura analítica 2/(1 + 4θ₀²)^{3/2} → REPROVA para σ acima de σ_lin e aprova abaixo; K10b —
a parábola ao longo de UMA direção dentro de 30 parâmetros com linhas lineares → K^N só nela.
**(3) A SEGUNDA LINEARIZAÇÃO (o funcional): NÃO RODAR** — reportar o custo (direções × pontos × custo de uma avaliação de F) e quais
direções dominam σ_F. O ajuste não linear (simulador diferenciável) segue registrado no P53/P54 como caminho de longo prazo.

**127. RESULTADOS (2026-10-19) — CURVATURA INTRÍNSECA RELATIVA: CONTROLES PASSAM; σ_lin × σ*; CUSTO DA VERIFICAÇÃO DO FUNCIONAL.**
**(1) Controles** (`etapaA_curv_check.py`, o mesmo código da análise): **K9** (θ² e θ² — reta) K^N = 0 → σ_lin = ∞ → APROVA (K^T = 0.354 ≠ 0,
ignorada); **K10** (θ e θ² — parábola, θ₀ = 0.5) K^N = 0.7071 = analítica 0.7071; σ = 0.9·σ_lin → γ√F = 0.270 APROVA, 1.1·σ_lin → 0.330
REPROVA; **K10b** (parábola ao longo de u em 30 parâmetros) K^N(u) = analítica (5.97×10⁻⁴), K^N(w ⟂ u) = 2.5×10⁻¹⁷ → **PASSAM.**
**(2) Dados reais** (`etapaA_curv_dir.py`, `curv_dir.json`; 11.6 M linhas da distal; 0 linhas com NaN em todas as 25 direções):
**(A) DISTAL SOZINHA: σ_lin = 5.2 mV** (limitante v_1, K^N = 0.0087; depois v_2 6.6, v_3 17.8, v_4 22.4 mV; as 21 restantes ≥ 44 mV). As
direções que limitam são as 4 mais fracas (v_1–v_4), justamente as de excursão no TETO (δ ≈ 1.03–1.09) — a curvatura delas é a SECANTE
numa excursão de fator ~2 (inclui ordens altas). Curvatura de parâmetro K^T 5–60× a intrínseca em todas (a maior parte da não linearidade
é de PARAMETRIZAÇÃO — o que o índice por linha confundia, item 126 (1)). **(B) COMBINADO PARCIAL: σ_lin = 1.45 mV** (v_1; v_2 1.58; v_3
3.06) — MENOR que a distal sozinha: no plano tangente do combinado, absorver a aceleração da distal exige mudar linhas da somática, cuja
aceleração foi posta em ZERO (não medida) → sobra mais componente normal. **(B) NÃO é limite em nenhum sentido** (a aceleração somática real
pode tornar o total mais OU menos tangente); o combinado DECISIVO precisa da rodada de direções na somática (50 subpassos × ~75 min ≈ 62 h
de CPU, ~16 h de relógio — não rodada, item 120 (2)).
**σ* (Cramér–Rao linear, SEM viés — limite de cima; 52 componentes, Gram combinado distal + somática): 8.52 mV** (limitante CaBurst_PA1).
**σ* > σ_lin nos dois → a exigência real de ruído fica ENTRE σ_lin e σ* — (A) [5.2, 8.5] mV; (B, parcial) [1.45, 8.5] mV; só análise não
linear fecha.** Ressalvas: σ* é do objeto desta checagem (UMA unidade distal + a somática), não da Etapa A inteira; o ruído real por amostra
dos registros é outro número (não avaliado aqui) — se for menor que σ_lin, a especificação linear vale para ele.
**(3) A segunda linearização (o funcional) — NÃO RODADA:** 21 direções do Gram combinado somam ≥ 90% da variância de TODA componente (v_3 v_16
v_4 v_6 v_22 v_1 v_5 v_8 v_9 v_10 v_2 v_20 v_21 v_7 v_12 v_19 v_15 v_13 v_14 v_17 v_11; a mais pesada, v_3, carrega 63% de uma componente).
Raio da região de confiança em σ* ao longo delas: v_1 3.81, v_2 3.22, v_3 2.44, v_4 2.13, v_5 1.43 em log (**ALÉM do fator 2** — θ·e^{±3.8v}:
avaliar F aí é sair do físico; o próprio Cramér–Rao linear em σ* abrange regiões não físicas nessas direções), as demais 0.02–0.8 (dentro).
**Custo** (2 pontos ±raio por direção; 1.39 h de CPU por avaliação de F a 10⁻⁸, MEDIDO no G: 61 avaliações ≈ 85 h): 21 dominantes → **59 h de
CPU (~15 h de relógio com 5 processos)**; as 25 → 70 h (~17 h). Nas 5 de raio além do fator 2 o raio teria de ser limitado (teto) — decisão
do Martel.

**128. DECISÃO DO USUÁRIO (2026-10-19) — ANTES DE QUALQUER SIMULAÇÃO NOVA, O MODELO DE RUÍDO; DEPOIS, SÓ O FUNCIONAL QUE NÃO DEPENDE
DELE. DECLARADO ANTES DOS NÚMEROS.**
**(1) REGISTRADO:** σ_lin (distal) = 5.2 mV contra σ* = 8.52 mV → exigência real no intervalo; só análise não linear fecha. Critério
γ^N·√F ≤ 0.3 (fonte secundária conferida, MASS rms.curv / Bates & Watts 1988 §7.3), máximo sobre as 25 direções. Curvatura de parâmetro
5–60× a intrínseca: confirma que o índice por linha media sobretudo a parametrização. O (B) combinado parcial não é limite em nenhum
sentido. **Direções na somática: NÃO RODAR nesta checagem** (o objeto não é a Etapa A; o método já está demonstrado; σ* depende do modelo de
ruído).
**(2) O MODELO DE RUÍDO EM USO (do código):** Fisher = JᵀJ/σ_V² — ruído INDEPENDENTE por amostra, o MESMO σ_V em todas as linhas (voltagens
e tempos × |dV/dt|, σ_t = σ_V/|dV/dt|), BRANCO na taxa de amostragem 1/DT = **10 kHz**; **12 022 813 linhas** no Gram combinado (distal 11 603
097 — quase tudo M1: 2 × 504 leituras × ~11 500 amostras — e somática 419 716). **RISCO (Martel):** com ~10⁷ amostras supostas independentes,
a informação de Fisher cresce com o número de amostras e o σ* por amostra fica generoso; o ruído real (sobretudo in vivo) inclui flutuação
sináptica de fundo de alguns mV, CORRELACIONADA no tempo (dezenas de ms) e ENTRE PONTOS da mesma célula, que não se cancela na média.
**DECLARADO (execução, sem simular):** (a) ruído AR(1) / Ornstein–Uhlenbeck no TEMPO, por leitura (cada traço de cada protocolo é uma série;
leituras diferentes independentes), variância marginal σ², φ = e^{−DT/τ}, τ = 1, 10 e 50 ms (e τ = 0 = o modelo atual, referência do mesmo
cálculo). Fisher generalizada Jᵀ Σ⁻¹ J pelo BRANQUEAMENTO exato do AR(1): w_0 = x_0, w_t = (x_t − φ x_{t−1})/√(1 − φ²), aplicado às
colunas de J na parte de VOLTAGEM de cada traço (amostras consecutivas; as 2 amostras retiradas pela cadeia de medida nas descontinuidades
são tratadas como contíguas — aproximação registrada); os TEMPOS de disparo seguem como linhas independentes com a variância marginal.
Representação pelo UM caminho com as 61 avaliações a 10⁻⁸ (identidade do item 123). σ*(τ) = min_g tol_g/(1.645·σ_F,g), σ_F,g = √(gᵀ G_τ⁻¹ g),
Gram combinado (distal + somática), 52 componentes, SEM viés. σ_lin(τ) da DISTAL SOZINHA pela mesma curvatura do item 126 com J e a
aceleração BRANQUEADOS (a curvatura relativa com ruído não branco se calcula no espaço branqueado). **Controle antes (item 108 (3)):** o
branqueamento = Jᵀ Σ⁻¹ J com a Σ AR(1) densa explícita (série curta, resposta conhecida); τ → 0 = iid; a curvatura branqueada = a com Σ
densa. (b) **Densidade espectral** (para comparar com eletrodos reais): branco a fs = 10 kHz → √S = σ/√(fs/2) (unilateral; 1 mV ↔ 14.1
µV/√Hz); OU → √S(f→0) = σ·√(4τ) (unilateral), e a forma 4σ²τ/(1 + (2πfτ)²). (c) **Correlação ENTRE pontos** (ruído compartilhado): só o
modelo e o custo, NÃO rodar. **Se σ*(τ) cair abaixo de σ_lin(τ), a especificação linear passa a valer no próprio nível que exige —
registrar.**
**(3) FUNCIONAL NAS 5 DIREÇÕES DE RAIO ALÉM DO FATOR 2 — INDEPENDENTE DO RUÍDO.** Nas direções v_1…v_5, NÃO marcar NÃO AVALIADO nem escolher
teto; pergunta: o funcional fica dentro da tolerância em TODA a faixa fisiológica ao longo delas? **Avaliar F em θ·exp(±log 2 · v_i), i =
1…5** (10 avaliações; a base do G a 10⁻⁸ é reaproveitada). F dentro da tolerância nos DOIS extremos → essas direções NÃO precisam ser
determinadas pelos dados (o limite fisiológico basta); F fora → a especificação FALHA nelas, com ou sem linearização. **PREMISSA declarada:
"faixa fisiológica = fator 2" é SUPOSIÇÃO, a confirmar na literatura de variabilidade de densidades.** Nota (registrada antes): com v_i
unitário, θ·exp(±ln 2·v_i) tem norma ln 2 em log-parâmetro — o parâmetro mais carregado muda por 2^{max|v_i|} (< 2), não pelo fator 2
inteiro (que seria δ = ln 2/max|v_i|, o "teto" do item 118). O restante da verificação do funcional (direções com raio dentro do fator 2)
ESPERA o item 2.

**129. RESULTADOS (2026-10-19) — O MODELO DE RUÍDO: COM RUÍDO CORRELACIONADO NO TEMPO O INTERVALO [σ_lin, σ*] SE ALARGA.**
**Controles** (`etapaA_ruido_check.py`): (R1) branqueamento AR(1) = Jᵀ Σ⁻¹ J com a Σ densa (|Δ| ≤ 4×10⁻¹³); (R2) φ = 0 = iid exato; (R3)
curvatura branqueada = a com a métrica Σ⁻¹ densa (≤ 1.3×10⁻¹³); (R4) sinal constante num traço de 400 amostras: Fisher 400 (iid) → 20.9 /
2.99 / 1.40 (τ = 1 / 10 / 50 ms) = analítico → **PASSAM**. **Dados** (`etapaA_ruido.py`, `ruido.json`; J gravado, 61 avaliações a 10⁻⁸;
voltagem branqueada por traço, tempos de disparo independentes):
| ruído | σ* (mV, marginal; limitante) | σ_lin distal (mV; limitante) | σ* ≤ σ_lin? | √S de σ* | √S de σ_lin (µV/√Hz) |
|---|---|---|---|---|---|
| iid (atual) | 8.52 (CaBurst_PA1) | 5.2 (v_1) | não | 120 (branco, 10 kHz) | 73.5 |
| OU τ = 1 ms | 3.64 | 1.15 (v_1) | não | 230 (f → 0) | 72.5 |
| OU τ = 10 ms | 2.19 | 0.257 (v_1) | não | 438 | 51.5 |
| OU τ = 50 ms | 2.56 | 0.091 (v_1) | não | 1 140 | 40.6 |
**Leitura:** a linha iid reproduz o item 127 (8.52 / 5.2 — conferência). O ruído correlacionado REDUZ σ* (2.3–3.9×) mas reduz σ_lin MUITO mais
(4.5–57×): a informação perdida está nas direções FRACAS (o traço da Fisher quase não muda, 0.98 — dominado por tempos de disparo e
transientes rápidos), onde a região de confiança cresce e a curvatura passa a pesar. **σ* NUNCA cai abaixo de σ_lin → a especificação
linear NÃO passa a valer no próprio nível; o intervalo SE ALARGA: iid [5.2, 8.5] → τ 10 ms [0.26, 2.2] → τ 50 ms [0.09, 2.6] mV.** Em
densidade espectral em baixa frequência, σ_lin fica em 40–74 µV/√Hz nos quatro modelos (a comparar com eletrodos reais — números de
eletrodos NÃO citados aqui: fonte primária a conferir). Não monotonia de σ* entre 10 e 50 ms (2.19 → 2.56): com ruído lento, o
branqueamento valoriza as feições rápidas — plausível, registrada. Aproximações registradas: tempos de disparo tratados como
independentes da voltagem; as 2 amostras das descontinuidades tratadas como contíguas; σ* SEM viés e do objeto desta checagem.
**(c) Correlação ENTRE pontos — modelo e custo, NÃO rodado:** Σ = σ²·C_pontos ⊗ R_τ (separável). (c1) componente COMPARTILHADA de peso c entre
as R leituras da mesma célula: C = (1 − c)I + c·11ᵀ, inversa por Sherman–Morrison → Fisher = [Σ_r (WJ_r)ᵀ(WJ_r) − c/(1 − c + Rc)·(Σ_r WJ_r)ᵀ(Σ_r
WJ_r)]/(1 − c): basta acumular a SOMA sobre as leituras de W·J por instante (T × 30) — uma passada como esta (~10 min, memória trivial) por
valor de c (c a varrer: 0.1, 0.5, 0.9 — o valor real não é conhecido). (c2) correlação que decai com a distância entre pontos, C_rr' =
e^{−d_rr'/λ}: precisa de C⁻¹ (504 × 504) e de todas as leituras de um protocolo ao mesmo tempo, por blocos de tempo (~0.5–1 GB, ~1 h por
(λ, τ)). Em (c1) e (c2) as leituras com disparo têm cortes diferentes (alinhar por instante).
**ADENDO AO ITEM 129 — REGISTRO E DECLARAÇÃO ANTES DO RESULTADO DO FUNCIONAL (decisão do Martel, 2026-10-19 ~17:30).** (1) Ruído correlacionado
no tempo (OU, τ = 1/10/50 ms): σ* cai para 3.6/2.2/2.6 mV, σ_lin para 1.15/0.26/0.09 mV; o intervalo ALARGA (iid [5.2; 8.5] → τ = 50 ms
[0.09; 2.6]); causa: o ruído lento tira informação das direções fracas; o traço da Fisher quase não muda (0.98). σ_lin em densidade
espectral de baixa frequência fica em 40–74 µV/√Hz nos quatro modelos — FORMA COMPACTA do limite de linearização. (2) **REGRA DECLARADA
(antes do resultado):** o σ_lin é limitado por v_1…v_4, as mesmas direções cujo raio em σ* passa do fator 2. Se F fica dentro da tolerância
nos DOIS extremos da faixa fisiológica ao longo de v_i → v_i é "DETERMINADA PELA FAIXA FISIOLÓGICA": sai do máximo que define σ_lin e da
variância propagada para F — recalcular σ_lin e σ* sobre as direções restantes, nos quatro modelos de ruído. Se F sai da tolerância em
algum extremo → v_i continua na conta; a especificação depende dela. **Forma do recálculo (declarada):** σ_lin = mínimo de σ_lin,i sobre as
direções RESTANTES (mesma curvatura por direção do item 126/129); σ* com os componentes ao longo das v_i determinadas tomados como
CONHECIDOS: σ_F,g² = g_Pᵀ (P G_τ P)⁺ g_P, P = projetor no complemento das v_i determinadas.

**130. DECISÕES DO USUÁRIO (2026-10-19 ~17:30) — FATOR 2; REPETIÇÃO; CORRELAÇÃO ENTRE PONTOS; FILA AJUSTADA; DEFEITO DO PONTO ÚNICO.**
**(1) FATOR 2 = o PARÂMETRO MAIS CARREGADO no fator 2 (borda da caixa fisiológica): excursão δ_i = ln 2 / max|v_i|.** A fila JÁ tinha
lançado (16:09–16:40) com θ·exp(±ln 2·v_i) (o mais carregado a 1.55–1.59×) — **PARADA pelos PIDs gravados** (pausa → --parar-trabalhos →
15 processos encerrados) e relançada com δ_i = ln 2/max|v_i| em diretório NOVO (`etapaA_Gdir2`, `dirF_fator2.npz`; o parcial de ln 2 em
`etapaA_Gdir` não se mistura), base do G a 10⁻⁸ reaproveitada. Perda: ~1.5 h × 5 processos de simulação parcial. **(2) DEFEITO DO PONTO
ÚNICO (achado no log):** "TERMINOU Gdir_s4 código 75" — o lançador RECUSOU (porta fechada), mas entre a saída e o poll o /proc/<pid>/cmdline
do processo zumbi fica VAZIO e `via_porta` leu isso como exec → o supervisor registrou "LANÇADO" e contou uma tentativa (nada rodou por
fora da porta). Corrigido: cmdline vazio volta ao poll; e o supervisor não conta término com código 75 como lançamento. Teste: 3 recusas
seguidas com a porta fechada → None nas 3. **(3) REPETIÇÃO COMO PARÂMETRO DE PROJETO — só conta** (item 131). **(4) CORRELAÇÃO ENTRE PONTOS —
versão barata** (componente compartilhada, Sherman–Morrison, c = 0.1/0.5/0.9, τ = 10 ms, pela porta) (item 131); a de decaimento por
distância só se esta mudar a conclusão.

**131. RESULTADOS (2026-10-19) — REPETIÇÃO COMO PARÂMETRO DE PROJETO (só conta) E CORRELAÇÃO ENTRE PONTOS (versão barata).**
**(1) Repetições** (`repeticoes.txt`): n = (σ_fundo/σ)² (arredondado para cima, mínimo 1), σ_fundo = 1, 2, 4 mV **ILUSTRATIVOS (suposição
declarada, NÃO medida in vivo)**; tempo = n × duração dos protocolos (distal 3.20 s por repetição para σ_lin; distal + somática 10.25 s para
σ*), SEM o intervalo entre repetições.
| ruído | σ_lin | σ* | n_lin (tempo), σ_fundo 1 / 2 / 4 mV | n* (tempo), σ_fundo 1 / 2 / 4 mV |
|---|---|---|---|---|
| iid | 5.2 | 8.52 | 1 / 1 / 1 (3 s) | 1 / 1 / 1 (10 s) |
| OU 1 ms | 1.15 | 3.64 | 1 (3 s) / 4 (13 s) / 13 (42 s) | 1 / 1 / 2 (20 s) |
| OU 10 ms | 0.257 | 2.19 | 16 (51 s) / 61 (3.3 min) / 242 (12.9 min) | 1 / 1 / 4 (41 s) |
| OU 50 ms | 0.091 | 2.56 | 122 (6.5 min) / 485 (26 min) / 1 940 (104 min) | 1 / 1 / 3 (31 s) |
**Leitura:** σ* (a exigência linear) quase não pede repetição (≤ 4); quem pede é a LINEARIZAÇÃO (σ_lin) com ruído lento — até ~2 000 repetições
(~1.7 h só de estímulo por ponto, mais os intervalos) com τ = 50 ms e fundo de 4 mV. **LIMITAÇÕES (registradas):** exige ESTACIONARIEDADE da
célula entre repetições; estimulação repetida pode ALTERAR a célula (plasticidade, rundown); exige fundo INDEPENDENTE do estímulo; o
intervalo entre repetições tem de ser ≫ τ (e deixar a célula voltar ao repouso) — não contado. σ_lin e σ* são os de ANTES da regra do
funcional (item 129, adendo); a tabela é refeita se v_1…v_4 saírem da conta.
**(2) Correlação ENTRE pontos — componente compartilhada** (`etapaA_ruido_pontos.py`, `ruido_pontos.json`; τ = 10 ms; Σ = σ²·C ⊗ R_τ, C = (1 −
c)I + c·11ᵀ entre as leituras de um MESMO ensaio, Sherman–Morrison): **c = 0 reproduz o OU 10 ms (2.19 / 0.257 — conferência)**; c = 0.1: σ*
1.99, σ_lin 0.272; c = 0.5: 2.18 / 0.266; c = 0.9: 2.72 / 0.266 mV. **A componente compartilhada NÃO muda a conclusão** (σ* > σ_lin em todos;
σ_lin praticamente igual); com c alto σ* até SOBE — o ruído comum se cancela nas DIFERENÇAS entre pontos, que carregam a informação (rejeição
de modo comum). → a versão com decaimento por distância NÃO é rodada (a regra do Martel: só se esta mudasse a conclusão). Aproximações:
cortes diferentes por leitura (R_t presentes por instante); tempos de disparo fora da partilha.

**132. RESULTADOS (2026-10-19 21:50) — O FUNCIONAL NAS 5 DIREÇÕES (FATOR 2 NO PARÂMETRO MAIS CARREGADO) E A REGRA DO ITEM 129 APLICADA.**
**(1) Funcional** (`etapaA_Fdir.py`, `Fdir2.json`; rodada `etapaA_Gdir2`, δ_i = ln 2/max|v_i| = 1.064 / 1.031 / 1.090 / 1.092 / 1.046; 10
avaliações em 5 processos pela porta, 18:02 → 21:43; base do G a 10⁻⁸ reaproveitada; 53 componentes com tolerância, inclusive a taxa_1.9):
**v_1: DENTRO nos dois extremos** (pior ΔF/tol 0.05 / 0.20); **v_2: DENTRO** (0.33 / 0.22) → **v_1 e v_2 DETERMINADAS PELA FAIXA FISIOLÓGICA**.
**v_3: FORA** (+: CaBurst_PA1 ΔF/tol = 1.70); **v_4: FORA** (−: CaBurst_PA1 1.25); **v_5: FORA** (−: CaBurst_PA1 2.53) — em CADA uma, UMA
componente só, sempre **CaBurst_PA1** (o tempo do 1º PA do CaBurst, tolerância 1 ms; contagens de PA inalteradas); todas as outras dentro
(pior 0.95). → v_3, v_4, v_5 CONTINUAM na conta: a especificação depende delas (e, nelas, de CaBurst_PA1 — a mesma componente que limita σ*
em todos os modelos de ruído). (Rótulo do print corrigido: dizia "exp(±ln2·v)", a rodada usou o δ do arquivo do fator 2.)
**(2) Regra aplicada** (`etapaA_ruido.py --determinadas 1,2`, dos acumulados; v_1, v_2 tomadas como CONHECIDAS na variância e fora do
máximo de σ_lin):
| ruído | σ* (mV) | σ_lin distal (mV; limitante) | σ* ≤ σ_lin? | √S σ* / σ_lin (µV/√Hz) |
|---|---|---|---|---|
| iid | 9.03 | 17.8 (v_3) | **SIM → CERTIFICADA** | 128 / 251 |
| OU 1 ms | 3.71 | 3.91 (v_3) | **SIM → CERTIFICADA** (margem 5%) | 234 / 247 |
| OU 10 ms | 2.26 | 0.809 (v_4) | não → [0.81; 2.26] | 452 / 162 |
| OU 50 ms | 2.69 | 0.827 (v_4) | não → [0.83; 2.69] | 1 200 / 370 |
**Leitura:** tirar v_1, v_2 sobe σ_lin 3.4–9× (as duas eram as de maior curvatura relativa) e σ* só 3–6% (contribuíam pouco à variância de F
— coerente com F dentro da tolerância ao longo delas). **Com ruído branco ou rápido (τ ≲ 1 ms) a especificação linear passa a valer no
próprio nível que exige**; com ruído lento (τ = 10–50 ms) a exigência real fica entre ~0.8 e ~2.3–2.7 mV e só análise não linear fecha.
**Repetições refeitas** (`repeticoes.txt`; σ_fundo 1/2/4 mV ilustrativos): n_lin iid 1/1/1; OU 1 ms 1/1/2; OU 10 ms 2/7/25 (até 80 s); OU 50
ms 2/6/24 (até 77 s) — **antes 1 940 (104 min) no pior caso**; n* ≤ 4 em todos. Ressalvas mantidas: premissa "faixa fisiológica = fator 2"
(SUPOSIÇÃO, a confirmar na literatura de variabilidade de densidades); σ* sem viés e do objeto desta checagem; limitações das repetições
(item 131).

**133. DECISÃO DO USUÁRIO (2026-10-20 ~09:10) — PREMISSA DO FATOR 2 (literatura) E CHECAGEM DE ROBUSTEZ; PLANO DA ETAPA A; taxa_1.9.
DECLARADO ANTES DOS NÚMEROS.**
**(1) LITERATURA (fontes conferidas pelo MARTEL, por busca — NÃO conferidas por mim nas primárias; rótulo: LITERATURA, secundária para
este registro):** densidade de um mesmo canal num tipo celular identificado varia 2–6× (Goaillard 2009; Ransdell 2013 — citados em Frontiers
Cell Neurosci 2020); 3–4× em neurônios do STG de caranguejo; 3–9× em mRNA no gânglio cardíaco; piramidais de CA3 de mamífero com passivo
variando até 5× e grande variância em Ih; expressão de canais FORTEMENTE CORRELACIONADA, com padrão específico por tipo celular (Schulz 2007;
Goaillard 2009). **Leitura:** "fator 2 para cada lado" = faixa total de 4× — no MEIO da literatura, não no extremo; faixas de 5–6× ≈
2.2–2.45 para cada lado. **Nota:** a covariância entre canais pode reduzir a variabilidade real ao longo de algumas direções, mas não há dado
de covariância para L5 → NÃO usada.
**CHECAGEM DECLARADA:** F em v_1 e v_2 na excursão que leva o parâmetro mais carregado a √6 ≈ 2.45 (faixa de 6×), δ_i = ln √6 / max|v_i|,
nos dois sentidos — 4 avaliações (base do G a 10⁻⁸ reaproveitada). **F dentro da tolerância nos 4 → a certificação (item 132) vale até o
extremo da literatura; se não → registrar a faixa máxima para a qual vale (2 ≤ fator < 2.45) e que acima dela a certificação cai.**
**(2) PLANO DA ETAPA A EM s = 400 — montar e reportar com custos, SEM lançar** (item 134).
**(3) taxa_1.9 fica NÃO AVALIADO:** uma componente em 55; quem limita a especificação é o CaBurst_PA1; pelo critério de "basta", não muda a
conclusão.

**134. PLANO DA ETAPA A EM s = 400 — COM CUSTOS, NÃO LANÇADO (2026-10-20).** Custos MEDIDOS nesta semana sob 5 processos (já incluem a
disputa) salvo onde marcado ESTIMATIVA; relógio ≈ CPU/5 com a máquina cheia.
**(1) Unidades (20 pontos + somática).** s = 400 = pontos da grade de 25 µm a distância múltipla de 400 µm: **20, TODOS APICAIS** (8 a 400 µm,
3 a 800, 9 a 1 200; nenhum ramo basal chega a 400 µm → em s = 400 os parâmetros basais só entram pelas leituras do soma e pela somática —
registrado). **Reaproveitamento:** g_apic[60]_32 (61 subpassos θ da distal migrada a 10⁻⁸, mesma configuração) e a somática (61 θ de
soma64_1e-8) → só os extras. Subpasso distal a 10⁻⁸: mediana 388 s (34 medidos); somático 71–77 min; repouso novo ~12 min.
| parte | subpassos | CPU |
|---|---|---|
| 19 pontos novos × 125 (61 θ + ganho + posição + 62 geometrias) | 2 375 | 257 h |
| g_apic[60]_32: 64 extras | 64 | 7 h |
| somática: 63 extras (ganho + 62 geometrias) | 63 | 78 h |
| repousos novos compartilhados (62 geometrias + 20 posições) | 82 | 16 h |
**(2) VIÉS (referências do Hay a 10⁻⁸):** unidade do Hay (L0 Δ 0.5) por ponto, 20 × ~51 min (protocolos medidos a 10⁻⁶ ×1.37) + repouso do
Hay ~2.8 h uma vez → ~20 h; viés SOMÁTICO no Hay (M3 + M5) ~20.5 h e termo DIRETO F_Hay ~23 h — ESTIMATIVAS (razão Hay/reduzido 16.6×,
item 96), cada um UM processo serial (caminho crítico ~1 dia, em paralelo com as unidades). G a 10⁻⁸: PRONTO. → ~64 h.
**(3) CURVATURA — 2ª passada com as direções do Gram COMPLETO de s = 400** (curvatura intrínseca relativa, item 127; as direções por relevância
com o G a 10⁻⁸): n_dir ESTIMADO 25 (como no objeto da checagem; até 30). Em TODAS as 21 unidades (a lição do (B) parcial do item 127: a
aceleração somática é necessária): distal 20 × 50 × 6.5 min = 108 h; somática 50 × 74 min = 62 h; repousos das direções 50 × 12 min = 10 h
→ **~180 h (30 direções: ~216 h)**. Só começa depois de TODAS as unidades da 1ª passada (o Gram completo define as direções).
**(4) FUNCIONAL nas direções cujo raio passe da faixa fisiológica** (como no item 132): ~5 direções × 2 × 1.39 h (medido no G) = **~14 h**
(+ a checagem de robustez a 2.45 se repetida: 4 × 1.39 h).
**(5) ANÁLISE FINAL** (σ*, σ_lin, intervalo, repetições, nos 4 modelos de ruído; componente compartilhada): passadas por unidade (~10 min
cada) × 21 unidades × ~3 passadas → **~10 h** (paralelizáveis).
**TOTAL ≈ 358 + 64 + 180 + 14 + 10 ≈ 626 h de CPU (~26 dias-CPU) → relógio: fase 1 (unidades + viés) ~85 h; fase 2 (curvatura) ~36 h;
fases 3–4 ~7 h → ~5.3 dias com a máquina cheia; realista 6–7 dias** (porta fechada por swap, voltas da fila, reinícios). (Item 96 previa 4.4
dias sem a curvatura.)
**RESTRIÇÃO DE DISCO:** a 2ª passada precisa dos traços θ de TODAS as unidades até o Gram completo existir: 20 × 5.3 GB ≈ 106 GB (+ 0.4 GB
da somática); traços de geometria/ganho/posição podem sair depois da redução da unidade; os da 2ª passada (~4.3 GB por unidade) são
processados e apagados unidade a unidade → **pico ≈ 110 GB contra 134 GB livres hoje (~82%) — viável, apertado.** Margem possível: apagar os
dados da checagem de tolerância que não servem mais (migr64_1e-6/1e-10, migr_* em float32, etapaA_rec: ~30 GB) — decisão do Martel.
**FALTA ANTES DE LANÇAR (código, a verificar):** (a) `etapaA_pontos.py` (citado no PLANO_EXEMPLO, NÃO existe) → pontos.json, conferido contra
o subset_check (20 pontos); (b) PLANO.json e TOLERANCIA.json (10⁻⁸) na raiz; reaproveitamento dos θ de g_apic[60]_32 e da somática (cópia dos
subpassos com a mesma IMPRESSAO); (c) `--apagar-brutos` hoje apaga TUDO depois da redução → opção que guarda os θ até a 2ª passada; (d) as
análises (Gram combinado, ruído, curvatura, componente compartilhada, funcional) generalizadas de 1 distal para 20 + somática; (e) lançamento
pela fila do SUPERVISOR (TRABALHOS gerados por estágio: adoção, retomada, inibidor e porta já testados) em vez da etapaA_fila antiga; (f) a
regra de PARADA em s (descer para 200 µm?) reescrita com σ*, σ_lin e o funcional — hoje o etapaA_sstar usa o critério antigo (item 13 + 26).

**135. DECISÃO DO USUÁRIO (2026-10-20 ~09:40) — NÃO LANÇAR A ETAPA A AINDA; TRÊS ANÁLISES ANTES. DECLARADO ANTES DOS NÚMEROS.**
**REGISTRADO:** em s = 400 µm os 20 pontos são todos apicais; o basal só entra pelo soma — o s* MISTURA espaçamento e COBERTURA de ramos curtos:
reportar SEMPRE o s* junto com a cobertura por região. Disco: decisão adiada até o plano estar fechado. O código (a)–(f) do item 134 fica para
depois destas três análises.
**(1) SOMA SOZINHO — sem simular.** A "unidade somática" injeta no soma mas REGISTRA EM TODOS OS PONTOS — não é "soma sozinho" (afirmação 5 do
preprint: nunca calculada). Linhas: SÓ a leitura SOMÁTICA com injeção somática — M3 na leitura 'soma' e M5 (os 3 degraus; lidos só no soma).
σ* nos quatro modelos de ruído, com a regra do item 132 (v_1, v_2 resolvidas pela faixa fisiológica, tomadas como conhecidas). **σ_lin do soma
sozinho NÃO é calculável sem simular** (a somática não tem rodada de direções — item 128 (1)) → NÃO AVALIADO, registrado. **DECLARADO:** o
soma sozinho CUMPRE a especificação num modelo de ruído se σ*_soma ≥ o nível em que o objeto combinado (distal + somática) é certificado
nesse modelo, min(σ*_comb, σ_lin,comb) do item 132 (iid 9.03; OU 1 ms 3.71; OU 10 ms 0.809; OU 50 ms 0.827 mV) — i.e., o soma sozinho
atinge a tolerância com o mesmo ruído em que o combinado é certificado. **Se o soma sozinho CUMPRE: a afirmação central do preprint é FALSA
para este conjunto funcional → PARAR e reportar** (com a ressalva de que a linearização do soma sozinho não foi verificada).
**(2) DENSIDADE DE LEITURA — sem simular.** Com as duas injeções existentes (soma + g_apic[60]_32) e leitura nos 504 pontos, restringir as
LEITURAS às grades de 400, 200 e 100 µm (subconjuntos exatos: pontos da grade de 25 µm a distância múltipla de s, + a leitura do soma; o M4@ponto
conta como leitura em g_apic[60]_32, o M4@soma e o M5 como leituras do soma). σ* e σ_lin por grade nos quatro modelos de ruído, com a regra do
item 132; σ_lin = o da DISTAL (a única com acelerações), no subconjunto de leituras. Cobertura por região em cada grade: tronco apical, oblíquos,
tufo e basal — **definição declarada:** basal = seções 'dend'; tronco = cadeia de 'apic' a partir de apic[0] seguindo o filho de MAIOR
comprimento de subárvore até o primeiro ramo em que o 2º filho tem subárvore ≥ 30% do 1º (o "nexo"); oblíquos = 'apic' que saem do tronco
antes do nexo; tufo = 'apic' depois do nexo.
**(3) VIÉS — termo DIRETO, F_Hay − F_red(θ_verd)** (`etapaA_vies_F.py`, Hay L0 Δ 0.5, a 10⁻⁸; F_red = o F0 do G a 10⁻⁸; ~23 h ESTIMATIVA, UM
processo, tipo 'hay' da porta) — independe da grade (o erro sistemático do reduzido no funcional, que NÃO diminui com mais pontos). O termo
PROPAGADO (G·(JᵀJ)⁺·JᵀΔy) depende das unidades e das referências do Hay por ponto — fora desta rodada. **DECLARADO:** reportar |viés| por
componente como fração da tolerância; **se |viés| no CaBurst_PA1 (o gargalo) passar SOZINHO da tolerância (|dF|/tol > 1), nenhum espaçamento
cumpre a especificação — a Etapa A espera uma redução melhor.**

**136. RESULTADOS (2026-10-20 11:50) — FATOR 2.45; SOMA SOZINHO; DENSIDADE DE LEITURA.**
**(1) Fator 2.45 (√6; faixa de 6×, extremo da literatura)** (`Fdir3.json`; δ = 1.375 / 1.333; 4 avaliações pela porta, 09:17 → 11:36): **v_1 e
v_2 DENTRO da tolerância nos dois extremos** (pior ΔF/tol 0.10 / 0.33 e 0.48 / 0.30) → pela regra declarada (item 133), **a certificação do
item 132 vale até o EXTREMO da literatura (6×)**. A premissa "faixa fisiológica = fator 2" deixa de ser limitante para v_1, v_2.
**(2) SOMA SOZINHO** (`etapaA_leituras.py`, `leituras2.json`; SÓ a leitura do soma com injeção somática: M3 no soma + M5; regra do item 132):
**σ* = 0.292 / 0.287 / 0.287 / 0.289 mV** (iid / OU 1 / 10 / 50 ms; limitante CaBurst_PA1) — quase independente de τ (a informação do soma vem
de feições rápidas e dos tempos de disparo). Fisher no complemento de v_1, v_2: inversível mas MUITO mal condicionada (cond 4.6×10¹²; 2 direções
quase não determinadas). Contra o nível certificado do combinado (9.03 / 3.71 / 0.809 / 0.827 mV): **NÃO CUMPRE em nenhum modelo** → **a afirmação
central do preprint NÃO é falsificada para este conjunto funcional.** O soma sozinho exigiria ruído 31× (iid) a 2.8× (OU 10–50 ms) menor que o
nível certificado do combinado; em repetições, 960× a 8× mais. σ_lin do soma sozinho: NÃO AVALIADO (sem direções na somática). Ressalva: o
combinado aqui é UMA injeção dendrítica + a somática, não a Etapa A.
**(3) DENSIDADE DE LEITURA** (as duas injeções existentes; leituras restritas às grades; regra do item 132; Fisher com posto completo, 28 de 28,
em todas as grades):
| leituras | cobertura (tronco / oblíquo / tufo / basal) | σ* iid / 1 / 10 / 50 ms | σ_lin iid / 1 / 10 / 50 ms | certificada? |
|---|---|---|---|---|
| 400 µm (21) | 1 / 7 / 12 / **0** | 4.30 / 1.52 / 0.967 / 1.19 | 20.5 / 4.21 / 0.745 / 0.972 | iid, 1 ms SIM; 10 ms [0.75; 0.97]; 50 ms [0.97; 1.19] |
| 200 µm (52) | 3 / 18 / 21 / 9 | 7.08 / 2.56 / 1.47 / 1.88 | 18.8 / 4.09 / 0.721 / 0.880 | iid, 1 ms SIM; 10 ms [0.72; 1.47]; 50 ms [0.88; 1.88] |
| 100 µm (120) | 6 / 33 / 37 / 43 | 7.54 / 2.77 / 1.60 / 2.02 | 18.9 / 4.03 / 0.742 / 0.858 | iid, 1 ms SIM; 10 ms [0.74; 1.60]; 50 ms [0.86; 2.02] |
| todas (504) | 25 / 132 / 143 / 203 | 9.03 / 3.71 / 2.26 / 2.69 | 17.8 / 3.91 / 0.809 / 0.827 | = item 132 (conferência exata) |
(+ a leitura do soma em todas; nexo = apic[36].) **Leitura:** a exigência linear σ* melhora com a densidade, com retorno decrescente (400 → 200
µm: +46–65%; 200 → 100: +6–9%; 100 → 25: +20–41%); σ_lin quase não muda com a grade (~19 / ~4 / ~0.73–0.81 / ~0.83–0.97) — o limite de
linearização vem da física das direções fracas, não da densidade de leitura. **A 400 µm não há NENHUMA leitura basal** (só o soma), e o tronco
tem 1 — o s* precisa vir junto com a cobertura (item 135). Ressalvas: só 2 injeções (soma + g_apic[60]_32), não a Etapa A com injeção em cada
ponto da grade; σ_lin da distal (a somática sem direções); sem viés (item 135 (3), rodando).

**137. DECISÃO DO USUÁRIO (2026-10-20 ~12:00) — REGISTROS E PLANO CONDICIONAL AO VIÉS. DECLARADO ANTES.**
**REGISTRADO:** fator 2.45 (faixa 6×): v_1 e v_2 dentro da tolerância (pior 0.48) — a certificação vale até o extremo da literatura. **Soma
sozinho:** Fisher inversível mas mal condicionada (4.6×10¹²); σ* ≈ 0.29 mV nos 4 modelos; falha onde o combinado certifica; desvantagem de 2.8×
(ruído lento) a 31× (iid) — **LIMITES INFERIORES da desvantagem** (σ_lin do soma não avaliado); **a afirmação do preprint passa a ser QUANTITATIVA,
não "inidentificável".** **Densidade de leitura (2 injeções):** σ* melhora com retorno decrescente; σ_lin NÃO muda com a grade; com ruído lento o
nível certificado fica preso no σ_lin — mais LEITURA não ajuda; o gargalo são as direções fracas.
**PLANO, SÓ DEPOIS DO VIÉS:** SE |viés| no CaBurst_PA1 passar sozinho da tolerância → PARAR (nenhum espaçamento cumpre); reportar. SE NÃO →
**PILOTO** antes da Etapa A completa. **Pergunta:** injetar em MAIS pontos (diversidade de estímulo) move o σ_lin? (a análise de densidade só
variou a LEITURA). **Pontos** (~4 novos da grade de 400 µm, por regra declarada — um no tronco, um oblíquo, dois no tufo, os mais distantes entre
si dentro de cada região — + as 2 unidades existentes; g_apic[60]_32 é TUFO, 800 µm). **Aplicação da regra (registrada antes de simular):**
tronco = **g_apic[36]_16** (único candidato; 400 µm, no nexo apic[36]); oblíquo = **g_apic[9]_16** (para escolha de UM ponto, declarado: o mais
distante, pelo caminho, da injeção existente — 818 µm); tufo = **g_apic[44]_48 e g_apic[64]_48** (o par mais distante entre si, 1 156 µm;
ambos a 1 200 µm). **Conjuntos:** 2 injeções = soma + g_apic[60]_32; 4 = + tronco + oblíquo; 6 = + os dois do tufo (a ordem da regra).
**Análise:** direções relevantes do Gram COMBINADO das 6 unidades (G a 10⁻⁸); a regra do item 132 refeita nessas direções (funcional ao longo
das de raio além da faixa fisiológica); curvatura intrínseca (item 127) — σ_lin da parte DISTAL (as unidades distais do conjunto; a somática
sem direções, como até aqui), σ* do combinado; os TRÊS conjuntos nas MESMAS direções; 4 modelos de ruído. **DECLARADO:** se σ_lin(6 injeções)
≥ 1.5 × σ_lin(2 injeções) com ruído LENTO (τ = 10 E 50 ms) → a diversidade de injeção é uma ALAVANCA e a Etapa A completa em s = 400 se justifica;
abaixo disso → o gargalo é a física das direções fracas; a Etapa A completa fica SUSPENSA e o próximo passo é repetição / análise não linear.
**Custo (a confirmar antes de lançar):** 4 unidades novas × 61 subpassos θ × 6.5 min ≈ 26 h; funcional ao longo das ~5 direções de raio além da
faixa (regra do item 132) ≈ 14 h; direções nas 5 unidades distais (2 × ~25 cada, inclusive refazer g_apic[60]_32 nas direções novas) ≈ 27 h +
repousos das direções ≈ 10 h; análise ≈ 2 h → **~79 h de CPU, ~17 h de relógio com 5 processos (~1 dia com as esperas da porta)**; disco ~43 GB.
**APROVADO PELO MARTEL (2026-10-20 ~12:15):** o critério do oblíquo (o mais distante da injeção existente → g_apic[9]_16) e o custo do piloto
(~79 h de CPU, ~1 dia, ~43 GB). **AUTORIZAÇÃO CONDICIONAL:** quando o viés sair, se |viés| no CaBurst_PA1 ficar DENTRO da tolerância
(|dF|/tol ≤ 1), LANÇAR o piloto direto pela fila do supervisor, sem nova confirmação; se passar da tolerância, PARAR e reportar.
**Implementação da condição (em código, não em texto):** o trabalho `vies_avalia` (requer vies_F8.npz) reporta |dF|/tol por componente e grava
`piloto_ok.json` SÓ se CaBurst_PA1 ≤ 1 (senão grava `PARAR_vies.json`); todos os trabalhos do piloto REQUEREM `piloto_ok.json`.
**Cadeia montada e testada (2026-10-20 ~13:00; `etapaA_vies_avalia.py`, `etapaA_piloto.py`, `results/etapaA_piloto/cadeia_piloto.py`):** 18 trabalhos no
supervisor — vies_avalia → 4 unidades θ (g_apic[36]_16, g_apic[9]_16, g_apic[44]_48, g_apic[64]_48; mesma configuração da distal migrada:
--so-theta, 10⁻⁸, cache_1e-8; diretório de saída próprio por unidade) → pil_dirs (Gram combinado das 6 → direções e as de raio além do fator 2)
→ funcional ao longo delas (5 processos, base do G reaproveitada) → pil_Fdir; e direções nas 5 distais → pil_analise (2/4/6 injeções, 4 modelos,
regra). **Testes com resposta conhecida:** avaliador do viés — rodada NULA (dF = 0) → piloto_ok; viés sintético de 2 ms no CaBurst_PA1 → PARAR_vies
(marcas num diretório de teste); `--analise` com as 2 unidades e as direções antigas → reproduz o item 132 EXATAMENTE (9.03/17.8, 3.71/3.91,
2.26/0.809, 2.69/0.827); `--direcoes` com as 2 unidades → as MESMAS 25 direções (índices iguais), σ iguais, σ* 8.52 e as mesmas 5 além do fator 2.

**138. RESULTADO (2026-10-20 14:35) — TERMO DIRETO DO VIÉS: DENTRO EM TODAS AS COMPONENTES; PILOTO AUTORIZADO PELO CÓDIGO.** (`etapaA_vies_F.py`
com o Hay L0 Δ 0.5 a 10⁻⁸, F_red = F0 do G a 10⁻⁸; `vies_F8.npz`, `vies_avalia.json`.) **|viés|/tolerância: CaBurst_PA1 0.15** (Hay 128.45 ×
reduzido 128.60 ms, dF = −0.15 ms) — **DENTRO** → `piloto_ok.json` gravado pelo avaliador → a cadeia do piloto foi liberada (autorização condicional
do item 137). Demais: taxas f-I 0.026–0.037; todos os 48 EPSP ≤ 0.005 (máx |dF| relativo 2.4×10⁻⁴); BAC_PA1/PA2 0.0; **0 de 53 componentes acima
da tolerância.** Contagens de PA do Hay = as do reduzido (BAC 2, CaBurst 1, f-I 26/31/42). Picos de Ca (sem tolerância): BAC_Ca dF 0.147,
CaBurst_Ca 0.174. **Conclusão (pela regra declarada):** o erro sistemático da redução (N = 32, nós nos pontos) no conjunto funcional é pequeno
diante das tolerâncias — o gargalo NÃO é a redução. Ressalva: é o termo DIRETO; o termo PROPAGADO (G·(JᵀJ)⁺·JᵀΔy) depende das unidades e das
referências do Hay por ponto — não calculado. **CORREÇÃO DE CUSTO (minha estimativa errada):** a avaliação do funcional no Hay levou ~3.8 h (13 689 s;
EPSP 6.3×, f-I 2.8× o reduzido), não ~23 h — a razão de 16.6× do item 96 (medida em protocolos de unidade) NÃO vale para o conjunto funcional; o custo
do viés no plano do item 134 (~64 h) está SUPERESTIMADO — a refazer com esta medida quando o plano for revisto.

**139. PEDIDO DO USUÁRIO (2026-10-21 ~09:00) — ANÁLISE DE SENSIBILIDADE À TOLERÂNCIA DO CaBurst_PA1, SEM MUDAR O CRITÉRIO. DECLARADO ANTES.**
O CaBurst_PA1 decide σ*, o soma sozinho e a direção v_4 em todas as análises: a especificação inteira depende da tolerância dessa componente.
**ORIGEM DA TOLERÂNCIA (conferida no registro — CORREÇÃO da premissa do pedido):** a tolerância DECLARADA da especificação é **1 ms** — D131 7.4
("contagem idêntica e 1º PA ≤ 1 ms no BAC/CaBurst"; limiares do conjunto funcional de SUFICIÊNCIA), retomada no critério da Etapa A ("EPSP 5%,
1º PA 1 ms, taxa 2% — D131 7.4", com o viés do item 26) e usada pelo código (etapaA_sstar.TOL['PA'] = 1 ms) em TODAS as análises até aqui. Os
**0.2 ms** são o "NÍVEL B" do V2 (D131/D132, validação da REDUÇÃO: "erros ≤ 1/5 dos limiares funcionais do D131 7.4 … 1º PA ≤ 0.2 ms") — um
critério de ACEITAÇÃO do modelo reduzido, não a tolerância da especificação. **NÃO alterada.** **DECLARADO:** ANÁLISE DE SENSIBILIDADE (rótulo),
para 6 injeções e os 4 modelos de ruído, com a tolerância do CaBurst_PA1 em **0.2 (nível B do V2), 0.5 e 1.0 ms (DECLARADA, D131 7.4)**: σ*, σ_lin,
nível certificado (σ* se σ* ≤ σ_lin; senão o intervalo [σ_lin; σ*]) e a componente que limita; a REGRA do item 132 refeita em cada tolerância com
os dados JÁ simulados — tolerância menor → σ* menor → raio menor → as direções além da faixa são um SUBCONJUNTO das 4 já avaliadas, e o "dentro/fora"
é reavaliado nos valores de F gravados. Conferência: a linha de 1.0 ms tem de reproduzir a análise principal. Nota: com 0.2 ms, o |viés|/tol do
CaBurst_PA1 (item 138) passa de 0.15 a 0.75 — ainda dentro.

**140. RESULTADOS (2026-10-21 22:35) — PILOTO: A DIVERSIDADE DE INJEÇÃO NÃO MOVE O σ_lin → ETAPA A COMPLETA SUSPENSA (regra do item 137);
SENSIBILIDADE À TOLERÂNCIA DO CaBurst_PA1.**
**Execução** (cadeia do supervisor, toda pela porta, sem quedas nem alertas): 4 unidades θ (20/10 14:38 → ~00:30); Gram das 6 unidades → **26 direções
relevantes**, σ* (iid, sem viés, sem regra) **13.4 mV** (2 injeções: 8.52); 4 direções de raio além do fator 2 → funcional ao longo delas: **v_1, v_2, v_3
DENTRO** nos dois extremos (pior 0.70), **v_4 FORA (CaBurst_PA1 2.53 / 1.05)** → determinadas v_1, v_2, v_3; direções nas 5 distais (2 × 26 + base
por unidade; 00:50 → 22:04); análise 22:05 → 22:33. **Custo real ~32 h de relógio (estimado ~1 dia):** cada subpasso de direção levou ~23 min (plano:
~7 min) — cada direção exige repouso NOVO e as 5 unidades chegam à mesma direção quase juntas; a cache de repousos não tem trava → o MESMO repouso é
calculado até 5× em paralelo. **Lição para a 2ª passada da Etapa A: calcular os repousos das direções UMA vez, antes (trabalho só de repousos), e só
então as unidades** — senão o custo da curvatura do item 134 (~180 h) está subestimado.
**Resultado (as MESMAS 26 direções nos três conjuntos; determinadas v_1, v_2, v_3; σ_lin = parte distal; σ* = combinado com a somática):**
| conjunto | σ* iid / 1 / 10 / 50 ms | σ_lin iid / 1 / 10 / 50 ms (limitante) | certificada? |
|---|---|---|---|
| 2 injeções (soma + g_apic[60]_32) | 8.93 / 3.71 / 2.30 / 2.71 | 21.1 / 4.43 / 0.83 / 0.63 (v_5) | iid, 1 ms SIM; 10 ms [0.83; 2.30]; 50 ms [0.63; 2.71] |
| 4 (+ tronco g_apic[36]_16 + oblíquo g_apic[9]_16) | 9.59 / 3.93 / 2.38 / 2.73 | 21.7 / 4.35 / 1.11 / 0.854 (v_4/v_5) | iid, 1 ms SIM; 10 ms [1.11; 2.38]; 50 ms [0.85; 2.73] |
| 6 (+ tufo g_apic[44]_48 + g_apic[64]_48) | 13.7 / 4.78 / 2.56 / 2.89 | **8.73 / 1.91 / 0.568 / 0.67 (v_4)** | **NENHUMA**: iid [8.73; 13.7]; 1 ms [1.91; 4.78]; 10 ms [0.57; 2.56]; 50 ms [0.67; 2.89] |
**σ_lin(6)/σ_lin(2) = 0.41 / 0.43 / 0.68 / 1.06** (iid / 1 / 10 / 50 ms) — abaixo de 1.5× com ruído lento → **pela REGRA declarada no item 137: o
gargalo é a FÍSICA das direções fracas; a Etapa A completa em s = 400 fica SUSPENSA; próximo passo: repetição / análise não linear.** Limitante de σ*:
CaBurst_PA1 em todos. **Leitura (não decide):** mais injeções sobem σ* (iid +53%; ruído lento +7–11%) mas BAIXAM σ_lin — o tronco e o oblíquo quase não
mudam a curvatura (4 injeções: σ_lin 10 ms 0.83 → 1.11), e os dois pontos do TUFO a 1 200 µm trazem curvatura intrínseca ao longo de v_4 (a direção
que falha no funcional pelo CaBurst_PA1) maior que a informação que acrescentam → com 6 injeções nada fica certificado, nem com ruído branco. A
diversidade de injeção não é alavanca para a linearização; no tufo distal ela expõe a não linearidade (eventos dendríticos). Ressalva: curvatura
pela secante na excursão δ_i (item 126 (b)); em v_4, δ (0.69) < raio em σ* (1.75) — a curvatura medida está DENTRO da região de confiança.
**SENSIBILIDADE à tolerância do CaBurst_PA1 (rótulo — o critério NÃO mudou; 1.0 ms = declarada, D131 7.4; 0.2 ms = nível B do V2), 6 injeções:**
| tol CaBurst_PA1 | além da faixa → DENTRO no funcional → determinadas | σ* iid / 1 / 10 / 50 ms | σ_lin iid / 1 / 10 / 50 ms (limitante) |
|---|---|---|---|
| **1.0 ms (declarada)** | v_1, v_2, v_3, v_4 → v_1, v_2, v_3 → v_1, v_2, v_3 | 13.7 / 4.78 / 2.56 / 2.89 | 8.73 / 1.91 / 0.568 / 0.67 (v_4) |
| 0.5 ms | v_1, v_2, v_3 → v_1, v_3 → v_1, v_3 | 6.79 / 2.38 / 1.28 / 1.43 | 3.52 / 0.78 / 0.259 / 0.364 (v_2) |
| 0.2 ms (nível B do V2) | v_1 → (v_3) → nenhuma | 2.68 / 0.944 / 0.504 / 0.559 | 1.44 / 0.316 / 0.098 / 0.136 (v_1, v_3) |
**Limitante de σ*: CaBurst_PA1 nas três tolerâncias** (σ* cai exatamente na proporção da tolerância: 13.7 → 6.79 → 2.68). Nenhuma certificada com 6
injeções; o intervalo [σ_lin; σ*] encolhe em valor absoluto com a tolerância, mas σ_lin cai também (menos direções resolvidas pela faixa fisiológica).
**Conferência:** a linha de 1.0 ms reproduz a análise principal; no teste com 2 injeções (direções do item 127), a linha de 1.0 ms reproduz o item 132
(9.03/17.8, 3.71/3.91, 2.26/0.809, 2.69/0.827); ali, 0.5 ms → [0.81; 1.13] a 10 ms (determinadas v_1, v_2) e 0.2 ms → nenhuma direção além da faixa,
certificada em 1.70 (iid) e 0.73 (1 ms), intervalos [0.26; 0.44] e [0.09; 0.51] (10 / 50 ms).

**141. DECISÃO DO USUÁRIO (2026-10-21 ~23:00) — TRÊS ITENS, NESTA ORDEM; NADA DE ETAPA A COMPLETA. DECLARADO ANTES DOS NÚMEROS.**
**REGISTRADO:** piloto — regra do 1.5× não atingida (0.68 / 1.06); Etapa A completa suspensa; com 6 injeções nada certifica, nem em ruído branco.
**LIÇÃO DE CUSTO:** a cache de repousos não tem trava; 5 unidades calcularam o mesmo repouso em paralelo → pôr TRAVA na cache, ou calcular os repousos
das direções ANTES de lançar qualquer 2ª passada.
**(1) CONDICIONAMENTO DO CaBurst — HIPÓTESE, NÃO CONCLUSÃO.** O CaBurst_PA1 domina σ*, o soma sozinho, a direção v_4 e a curvatura do piloto. O limiar
do spike de Ca no CaBurst está registrado como "≤ 1.5 nA" porque 1.5 nA era o MENOR ponto da grade (item 77: 1.5 nA → spike de Ca de 6.1 mV e 1 PA;
2.0 nA → 26 mV e 2 PA) — a distância do protocolo ao limiar NUNCA foi medida; a regra de condicionamento (itens 66/68: a métrica tem de ser estável
diante de perturbações menores que o efeito) nunca foi aplicada a esta componente. **Hipótese:** o protocolo está logo acima do limiar do evento de
Ca; perto de um limiar, a latência do disparo é extremamente sensível a parâmetros que movem o limiar. **Protocolo (o MESMO do conjunto funcional,
etapaA_F):** α do Hay (`epsp`, τ 0.5/5 ms) no hay_620, início 105 ms, 400 ms; PA pelo detector de PICO (D122); spike de Ca dendrítico pela definição
do item 75 (no hay_620: pico ≥ −20 mV E V ≥ −40 mV por ≥ 10 ms contíguos); CVode a 10⁻⁸; repouso convergido (caches do G e do viés); reduzido N = 32
(o modelo do G) e Hay L0 Δ 0.5 (a referência do viés). **Testes:** (a) varredura da amplitude de 0.50 a 1.60 nA (passo 0.05) e bisseção até 0.25%
relativo → limiar do spike de Ca e do 1º PA somático; distância relativa do protocolo ao limiar, (1.5 − A_lim)/A_lim; (b) latência do 1º PA (pico −
105 ms) em 1.5 × (1 ± 0.005, 0.01, 0.02) nA → d(latência)/d(amplitude) por 1% (diferença central a ±1%) e a contagem de PA em cada ponto (o critério
de contagem do item 68, reportado); (c) cargas de v_4 (Gram das 6 unidades do piloto) sobre cm_dend, apic_NaTa_t e os parâmetros de Ca da zona quente,
e o limiar no reduzido em θ·exp(±δ v_4) (os extremos do funcional do piloto, δ = ln 2/max|v_4|; repousos já em cache) — e, como CONTROLE, em
θ·exp(±δ v_1) (direção que ficou DENTRO). **CRITÉRIO DECLARADO:** o CaBurst_PA1 é MAL CONDICIONADO por escolha de protocolo se, no REDUZIDO (o modelo
que define G e σ*), **o protocolo estiver a menos de 10% acima do limiar** (o mais próximo entre o do spike de Ca e o do 1º PA) **E a latência do 1º
PA mudar ≥ 1 ms (a tolerância inteira) por 1% de amplitude** — pela regra do item 66: a perturbação pequena é 1% (o passo do Jacobiano) e o efeito a
detectar é a tolerância. O Hay é reportado ao lado (se discordar, registrar como discrepância da redução perto do limiar). Mal condicionado → pela regra
do item 68, propor uma amplitude que passe no condicionamento, POR REGRA DECLARADA, e reavaliar — SEM mexer na tolerância. Se não → a hipótese cai;
registrar.
**(2) DIAGNÓSTICO POR PONTO DO TUFO (sem simular):** σ_lin com cada ponto do tufo separadamente (g_apic[44]_48, g_apic[64]_48) — conjuntos 2 + cada um
e 4 + cada um, nas MESMAS 26 direções; qual traz a curvatura em v_4 e se ela é LOCALIZADA: a energia da aceleração ao longo de v_4 (Σ a²) por protocolo
(M1m, M1p, M4) e por região das leituras, e as linhas cuja identidade de disparo falha na excursão (NaN, hoje zeradas na aceleração — CONTADAS); cruzar
com o item 1: o M4 nos pontos a 1 200 µm dispara evento perto do limiar?
**(3) REPETIÇÕES COM OS NÚMEROS DO PILOTO (só conta):** n = (σ_fundo/σ)² com σ_lin e σ* de 2, 4 e 6 injeções, σ_fundo 1/2/4 mV ILUSTRATIVOS; tempo por
repetição = soma dos protocolos (distal 3.2 s por unidade, somática 7.05 s).

**142. RESULTADOS (2026-10-21 23:30) — ITENS 141 (2) E (3): DIAGNÓSTICO POR PONTO DO TUFO E REPETIÇÕES COM OS NÚMEROS DO PILOTO.**
**(2a) σ_lin por conjunto** (`etapaA_piloto.py --analise`, as MESMAS 26 direções, v_1–v_3 determinadas; conferência: 2/4/6 injeções = piloto, exato):
| conjunto | σ_lin iid / 1 / 10 / 50 ms (limitante) | σ* iid / 10 ms |
|---|---|---|
| 2 injeções | 21.1 / 4.43 / 0.83 / 0.63 (v_5) | 8.93 / 2.30 |
| 2 + g_apic[44]_48 | **5.3 / 1.18 / 0.365 / 0.395 (v_5)** | 11.5 / 2.39 |
| 2 + g_apic[64]_48 | 8.1 / 1.70 / 0.507 / 0.66 (v_4) | 11.5 / 2.46 |
| 4 injeções | 21.7 / 4.35 / 1.11 / 0.854 (v_4/v_5) | 9.59 / 2.38 |
| 4 + g_apic[44]_48 | 8.27 / 1.80 / 0.53 / 0.53 (v_4/v_5) | 11.9 / 2.45 |
| 4 + g_apic[64]_48 | 10.5 / 2.23 / 0.714 / 0.821 (v_4/v_6) | 12.1 / 2.51 |
| 6 injeções | 8.73 / 1.91 / 0.568 / 0.67 (v_4) | 13.7 / 2.56 |
**Os DOIS pontos do tufo baixam σ_lin**; o g_apic[64]_48 pela direção v_4, o g_apic[44]_48 (o que mais baixa) sobretudo por v_5.
**(2b) Localização** (`etapaA_tufo_diag.py`, energia da aceleração Σa² ao longo da direção, por protocolo e região da leitura): ao longo de **v_4**:
g_apic[44]_48 Σa² = 304, **95.6% no M1p lido no tufo**; g_apic[64]_48 Σa² = 2 301, **99.0% no M1p no tufo**; as outras 3 unidades: 6.6–72 (g_apic[60]_32 e
o oblíquo dominados pelo M4 lido no soma; o tronco espalhado no M1 basal/oblíquo). Ao longo de **v_5**: g_apic[44]_48 **87.8%** e g_apic[64]_48 **99.2% no M1p
no tufo**. Nenhuma linha com identidade de disparo falhando na excursão (0 NaN). **→ A curvatura trazida pelo tufo é LOCALIZADA: o degrau DESPOLARIZANTE
do M1 (+50 pA × 1 s) lido no próprio tufo.** **Cruzamento com o item 1:** NÃO é o mesmo evento de Ca perto do limiar — no M1p dos pontos do tufo NÃO há
disparo (o único "disparo" detectado é o artefato do degrau na própria leitura do ponto de injeção, início em 99.9 ms; o M1m tem o mesmo em 1 099.8 ms: a
subida passiva numa ponta de alta impedância passa de 20 mV/ms); o que há é DESPOLARIZAÇÃO GRANDE: deflexão máxima do M1p **31.4 mV (g_apic[44]_48) e 38.3
mV (g_apic[64]_48), contra 6.5 mV em g_apic[60]_32** — +50 pA a 1 200 µm recrutam condutâncias ativas (não linearidade SUBLIMIAR ativa); o M1m (−50 pA,
~5 mV) quase não contribui. **Mesma FAMÍLIA do item 1: amplitude de protocolo FIXA, nunca condicionada POR SÍTIO** — o "sublimiar" de 50 pA foi pensado
para o ponto de 800 µm. **Achados colaterais (registrados, não decidem):** (i) o M4 no PRÓPRIO ponto dá deflexões não fisiológicas a 1.5 nA — **481 mV
(g_apic[64]_48), 418 mV (g_apic[44]_48), 651 mV no oblíquo g_apic[9]_16**, 151 mV em g_apic[60]_32, 34 mV no tronco — e 0.2 nA já dispara evento no
tufo e no oblíquo: as amplitudes do M4 também não foram condicionadas por sítio; (ii) o artefato do degrau faz o detector cortar a voltagem da
leitura do PRÓPRIO ponto de injeção em 99.9 ms nas unidades do tufo — a representação descarta, na prática, o M1 lido no ponto de injeção ali.
**(3) REPETIÇÕES COM OS NÚMEROS DO PILOTO** (`repeticoes_piloto.txt`; n = (σ_fundo/σ)², σ_fundo 1/2/4 mV ILUSTRATIVOS; certificar exige σ_efetivo ≤
min(σ*, σ_lin) → n_cert; duração por repetição 10.25 / 16.65 / 23.05 s para 2 / 4 / 6 injeções, sem o intervalo entre repetições):
| ruído | n_cert 2 inj (1/2/4 mV) | n_cert 4 inj | n_cert 6 inj |
|---|---|---|---|
| iid | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| OU 1 ms | 1 / 1 / 2 | 1 / 1 / 2 | 1 / 2 / 5 |
| OU 10 ms | 2 / 6 / 24 (4.1 min) | **1 / 4 / 13 (3.6 min)** | 4 / 13 / **50 (19.2 min)** |
| OU 50 ms | 3 / 11 / 41 (7.0 min) | **2 / 6 / 22 (6.1 min)** | 3 / 9 / 36 (13.8 min) |
**Resultado curioso (registrado): para a certificação linear, 4 injeções exigem MENOS repetições que 6 (e que 2)** — os dados do tufo carregam
informação (σ* sobe), mas em forma NÃO LINEAR (σ_lin desce); com ruído branco, 1 repetição basta nos três conjuntos (σ_fundo ≤ 4 mV).

**143. RESULTADO (2026-10-22 01:20) — ITEM 141 (1): CONDICIONAMENTO DO CaBurst — PELO CRITÉRIO DECLARADO A HIPÓTESE CAI (por margem estreita).**
(`etapaA_caburst_cond.py`, 6 varreduras pela fila do supervisor; `etapaA_caburst_aval.py`, `caburst_aval.json`; CVode 10⁻⁸; repousos da cache.)
**Conferências (resposta conhecida): EXATAS** — reduzido em 1.5 nA e θ_verd: 1º PA 128.6000 ms e pico de Ca 5.9067 mV = os F0 do G a 10⁻⁸; Hay: 128.4500 /
6.0803 = os do termo de viés.
| | limiar do spike de Ca | limiar do 1º PA | protocolo acima do mais próximo | d(latência)/d(amplitude) | contagem em ±2% |
|---|---|---|---|---|---|
| **reduzido (decide)** | 1.278 nA (17.4% abaixo de 1.5) | **1.384 nA** | **8.4%** (< 10% ✔) | **−0.825 ms por 1%** (< 1 ms ✘) | estável |
| Hay | 1.275 nA | 1.381 nA | 8.6% | −0.812 ms por 1% | estável |
Latência do 1º PA (reduzido) em 1.5 × 0.98 / 0.99 / 0.995 / 1 / 1.005 / 1.01 / 1.02: 25.38 / 24.45 / 24.00 / 23.60 / 23.20 / 22.80 / 22.05 ms (Hay: 25.20 … 21.95).
**CRITÉRIO DECLARADO (item 141): a < 10% do limiar — SIM; |d latência| ≥ 1 ms por 1% — NÃO (0.825) → o CaBurst_PA1 NÃO é mal condicionado pelo critério
declarado; a HIPÓTESE CAI; nenhuma amplitude nova é proposta.** Registrado ao lado (sem reinterpretar): a sensibilidade fica em 83% do limite; o protocolo
está perto do limiar do 1º PA SOMÁTICO (8.4%), não do spike de Ca (17.4%) — a hipótese tal como formulada ("logo acima do limiar do evento de Ca")
não se confirma; o Hay concorda com o reduzido nos dois limiares (≤ 0.25%, a resolução da bisseção).
**(c) v_4 e o limiar:** cargas de v_4 (Gram das 6 unidades): **apic_SKv3_1 +0.787, soma_K_Pst −0.444, soma_Ih −0.270, g_pas_axon +0.232, apic_decay −0.184,
apic_SK_E2 +0.097**; cm_dend 0.000 e apic_NaTa_t 0.000 (os parâmetros do 2º disparo da M3 NÃO carregam v_4); Ca da zona quente pequeno (LVAst −0.038, HVA
+0.051). Nos extremos θ·exp(±(ln 2/max|v_4|)·v_4) (δ = 0.880): **limiar do spike de Ca INALTERADO (1.278 nos dois); limiar do 1º PA 1.419 (+2.5%) e 1.378
(−0.5%)**; latência em 1.5 nA 26.13 / 22.55 ms (θ_verd 23.60: +2.53 / −1.05 ms — exatamente as razões ΔF/tol 2.53 / 1.05 do funcional do piloto). Controle
v_1 (ficou DENTRO): limiar do 1º PA 1.381 / 1.394 (−0.2% / +0.7%), latência 23.48 / 23.85 ms (−0.13 / +0.25). **Leitura (não decide):** v_4 é sobretudo K
apical (Kv3.1) contra K somático (K_Pst) — move o limiar do PA SOMÁTICO disparado pelo spike de Ca, não o do spike de Ca; a latência do CaBurst_PA1 funciona
como medida da DISTÂNCIA ao limiar do PA (≈ −0.8 ms por 1% de folga), o que explica a dominância da componente e a falha ao longo de v_4 — sem que, pelo
critério declarado, isso a torne mal condicionada.

**144. DECISÃO DO USUÁRIO (2026-10-22 ~01:30) — PARAR AS CONCLUSÕES DO PILOTO ATÉ MEDIR A CONTAMINAÇÃO POR DADOS NÃO FISIOLÓGICOS. DECLARADO ANTES DOS NÚMEROS.**
**(1) REGISTRADO:** hipótese do CaBurst **REFUTADA** pelo critério declarado (latência −0.825 ms por 1%, abaixo de 1 ms); o protocolo está a 8.4% do limiar do PA
SOMÁTICO, não do spike de Ca (17.4%); v_4 = K apical (Kv3.1) contra K somático (K_Pst), move o limiar do PA somático; o CaBurst_PA1 funciona como medida da
distância a esse limiar. Tabela de repetições do piloto: 4 injeções exigem menos repetições que 2 e que 6.
**(2) CONTAMINAÇÃO POR DADOS NÃO FISIOLÓGICOS — sem simular, primeiro.** O M4 a 1.5 nA no próprio ponto produz 418–481 mV no tufo e 651 mV no oblíquo; respostas
fisicamente impossíveis, mudando com θ, viram INFORMAÇÃO APARENTE no Gram. **FAIXA FISIOLÓGICA DECLARADA: [−110, +60] mV** — justificativa: num neurônio a
membrana fica entre as reversões das condutâncias que a dominam; no Hay (biophys3) E_Na = +50 mV, E_K = −85 mV, e_pas = −90 mV, E_h = −45 mV (E_Ca ~ +130 mV
pela Nernst com cai mínimo de 10⁻⁴ mM, mas as correntes de Ca são pequenas e não sustentam a membrana lá contra o K — platôs de Ca dendríticos ficam perto de
0 mV); teto = E_Na + 10 mV (margem para o pico do PA perto de E_Na); piso = e_pas − 20 mV (margem para injeções hiperpolarizantes). Acima de +60 mV só a corrente
injetada além do que a membrana conduz explica (os casos de 418–651 mV). **VOLTAGEM ABSOLUTA** = deflexão gravada + repouso daquela leitura naquele θ (os
traços são deflexões — a cadeia subtrai o valor pré-estímulo); o repouso vem dos estados SALVOS na cache (carregados sem simular e CONFERIDOS contra o
gravado: t e V no soma — `etapaA_vrest.py`). **LINHA NÃO FISIOLÓGICA (declarado):** uma linha de VOLTAGEM (amostra) é não fisiológica se a voltagem absoluta
naquela amostra sair da faixa em θ ou em QUALQUER perturbação usada (os ±1% por eixo e, para a curvatura, as excursões das direções); uma linha de TEMPO de
disparo é não fisiológica se o PICO absoluto daquele disparo sair da faixa em θ ou em qualquer perturbação usada. **Execução:** (a) fração de linhas e fração do
traço do Gram (iid) vindas de linhas não fisiológicas, por unidade e por protocolo; (b) σ*, σ_lin e nível certificado SEM essas linhas, para o soma sozinho, o
combinado da checagem (2 injeções, item 132) e o piloto (2, 4 e 6 injeções), nos 4 modelos de ruído — as direções DETERMINADAS pela faixa ficam as das análises
originais (v_1, v_2 na checagem; v_1–v_3 no piloto), para isolar o efeito de tirar as linhas (se o conjunto "além da faixa" mudaria, reportado ao lado);
(c) a unidade g_apic[60]_32 (800 µm): voltagens absolutas que o M4 atinge ali. **CONTROLE (resposta conhecida):** com a faixa (−∞, +∞) a análise tem de
reproduzir EXATAMENTE os números anteriores (piloto, item 132, soma sozinho). **LEITURA DECLARADA:** se σ* OU σ_lin mudarem MAIS DE 10% em ALGUM caso (conjunto ×
modelo de ruído) — o mesmo limiar das comparações de σ dos itens 75/78 —, os resultados com esses protocolos estão CONTAMINADOS e precisam ser refeitos com
protocolos condicionados (item (3)), INCLUSIVE a comparação do soma sozinho (afirmação 5 do preprint). **Nota (antes):** o M1p no tufo (deflexão 31–38 mV
sobre repouso ~−70 mV → ~−32 a −39 mV absolutos) deve ficar DENTRO da faixa — grande e ativo, mas não impossível; a regra da faixa não o retira; a não
linearidade dele é assunto do condicionamento (item (3)).
**(3) CONDICIONAMENTO DOS PROTOCOLOS POR PONTO — PROPOR, NÃO RODAR (regras derivadas da física, declaradas antes):** **M1:** amplitude por ponto tal que a
despolarização ESTACIONÁRIA no próprio ponto seja **ΔV_alvo = 5 mV** → I = ΔV_alvo / R_in(ponto), com R_in medida por um degrau de ±10 pA × 1 s no ponto
(estado estacionário, média dos últimos 50 ms; ±10 pA para ficar no regime linear) — sublimiar por construção; 5 mV = o regime em que o M1 já era razoável
no ponto de 800 µm (50 pA → 6.5 mV) e o maior sinal dentro da faixa sugerida (2–5 mV); M1m com −I (simétrico). **M4:** amplitudes por ponto em relação ao
LIMIAR LOCAL de evento (bisseção por ponto): **0.5×, 0.9× e 1.2× o limiar**, com TETO de voltagem explícito: a voltagem absoluta em qualquer leitura não passa de
+60 mV (a faixa declarada) — se 1.2× passar, usa-se a maior amplitude ≤ 1.2× que respeita o teto (bisseção); **limiar local de evento (declarado):** a menor
amplitude do α no ponto cuja deflexão de pico NO PONTO excede em 50% a predição LINEAR (escalada de uma amplitude pequena, 0.02 nA) — supralinearidade
regenerativa, não o critério de dV/dt (que dispara com a carga passiva numa ponta de alta impedância — item 142). **Soma:** M3 e M5 (protocolos do Hay no
soma) fora destas regras — inalterados. **Registrado:** um dispositivo real faria isso — medir R_in e o limiar local antes de escolher amplitudes; **o protocolo
condicionado é o que o HANU executaria.** NÃO lançar antes do resultado do item (2).

**145. RESULTADOS (2026-10-22 11:50) — CONTAMINAÇÃO POR DADOS NÃO FISIOLÓGICOS: PELO LIMIAR DECLARADO, OS RESULTADOS DO PILOTO ESTÃO CONTAMINADOS
(um caso: +15.6%); SOMA SOZINHO E A CHECAGEM, NÃO.**
**Repouso absoluto** (`etapaA_vrest.py`, `vrest.npz`): 163 estados de repouso (base, 60 eixos, 50 direções da checagem, 52 do piloto) carregados da cache sem
simular e CONFERIDOS (t e V no soma = os gravados); repouso na base: soma −77.2 mV, leituras de −78.0 a −63.6 mV (tufo mais despolarizado, Ih); em todos os θ:
−78.9 a −62.2 mV. **Controles (faixa infinita): reproduzem EXATAMENTE** o soma sozinho (0.292/0.287/0.287/0.289), o item 132 e o piloto.
**(a) Linhas fora da faixa [−110, +60] mV** — SÓ linhas de TEMPO do M4 no próprio ponto (pico do disparo acima de +60 mV); nenhuma de voltagem; M1, M3, M5: 0:
| unidade | linhas fora (M4) | do traço do Gram do M4 |
|---|---|---|
| g_apic[60]_32 (800 µm) | 1 | 0.46% |
| g_apic[36]_16 (tronco) | 0 | 0 |
| g_apic[9]_16 (oblíquo) | 2 | 48.5% |
| g_apic[44]_48 (tufo) | 2 | 17.3% |
| g_apic[64]_48 (tufo) | 2 | 45.6% |
| somática | 0 | 0 |
**(b) σ* e σ_lin sem essas linhas (direções determinadas fixas, como nas análises originais):** soma sozinho — IGUAL (0 linhas); checagem (2 injeções, direções
do item 127) — σ* igual, σ_lin −0.9% / +0.2% (10 / 50 ms); piloto (direções do Gram das 6) — σ* IGUAL em todos; σ_lin: 2 injeções iid +4.3%, 1 ms +3.2%, 10 ms
+9.8%, **50 ms +15.6% (0.63 → 0.728)**; 4 injeções +3.2 / +7.4 / 0.0 / +1.4%; 6 injeções +0.1 / +1.6 / +5.1 / +2.8%. **LEITURA DECLARADA (item 144): uma mudança
> 10% em algum caso → os resultados com esses protocolos estão CONTAMINADOS e precisam ser refeitos com protocolos condicionados — inclusive a comparação do
soma sozinho** (o soma sozinho em si não muda; a comparação é contra o nível certificado do combinado, que vem desses protocolos). Registrado ao lado (não
decide): a regra do piloto não muda (σ_lin(6)/σ_lin(2) = 0.66 / 0.95 com 10 / 50 ms, abaixo de 1.5×); a queda do σ_lin com o tufo vem do M1p (fisiológico) e
não do M4.
**(c) Voltagem absoluta máxima do M4 no próprio ponto (base):** g_apic[60]_32 −53 / +1 / **+82** mV (0.2 / 0.5 / 1.5 nA); tronco −70 / −64 / −40; oblíquo +55 /
**+166 / +575**; tufo g_apic[44]_48 +20 / **+96 / +352**; g_apic[64]_48 +19 / **+113 / +417**; no soma sempre ≤ −60 mV. O M1p no próprio ponto chega no máximo a
−26 mV (tufo) — dentro da faixa.
**INCIDENTE (registrado): 3ª suspensão → boot frio (22/10 09:20:56 → 09:21:26), causa não determinada.** Matou as duas análises do piloto, que EU tinha lançado
direto pelo shell (fora do supervisor → SEM inibidor; a fila estava vazia, o inibidor do supervisor liberado). Relançadas pela fila. **Regra prática: toda rodada
de mais de alguns minutos — inclusive análise — vai pela fila do supervisor.**
**(3) CUSTO DE REFAZER O PILOTO COM PROTOCOLOS CONDICIONADOS (regras do item 144; NÃO lançado):** medidas de condicionamento nas 5 distais (R_in por ±10 pA ×
1.15 s; limiar local do M4 por bisseção com a predição linear de 0.02 nA; teto por bisseção) ~20 min de CPU; CÓDIGO: amplitudes por ponto na unidade (arquivo
de protocolos), conferido com as amplitudes antigas → subpasso idêntico bit a bit; 5 unidades × 61 subpassos θ × ~6.5 min ≈ 33 h (repousos θ em cache; a
somática INALTERADA, M3/M5 do Hay — reaproveitada); Gram das 6 → ~26 direções; REPOUSOS das direções calculados ANTES, uma vez (lição do item 140) ≈ 10 h de CPU
(~2 h de relógio); funcional ao longo das ~4 de raio além da faixa ≈ 11 h (o G não muda — independe dos protocolos de medida); direções nas 5 distais 5 × 53 × ~7
min ≈ 31 h; análises (piloto, contaminação, sensibilidade) ≈ 2 h → **~88 h de CPU, ~18 h de relógio com 5 processos (~1–1.5 dia com as esperas da porta).**
Estimativa das amplitudes condicionadas (a confirmar pelas medidas): g_apic[60]_32 — M1 ≈ 38–40 pA (hoje 50; deflexão 6.5 mV a 50 pA), M4 ≈ 0.15–0.25 / 0.27–0.45 /
0.36–0.6 nA (limiar entre 0.2 e 0.5 nA; hoje 0.2 / 0.5 / 1.5 — a de 1.5 nA, a não fisiológica, cai); tufo — M1 ≈ 7–8 pA (deflexão 31–38 mV a 50 pA), M4 abaixo de
0.2 nA (0.2 já dispara); soma — inalterado.

**146. DECISÃO DO USUÁRIO (2026-10-22 ~12:00) — LANÇAR O PILOTO CONDICIONADO, COM CONDIÇÕES. DECLARADO ANTES DE QUALQUER MEDIDA.**
**REGISTRADO:** (i) contaminação: só tempos de disparo do M4 no próprio ponto saem da faixa; σ* inalterado; σ_lin muda até +15.6% (um caso, por UMA linha);
pela regra, piloto CONTAMINADO; σ_lin(6)/σ_lin(2) < 1.5× mesmo sem essas linhas. (ii) **A CONCLUSÃO DO PILOTO ESTÁ CONFUNDIDA por outro motivo:** a curvatura
que baixou o σ_lin com o tufo veio do M1 a 50 pA (31–38 mV na ponta do tufo, recrutando condutâncias ativas) — o piloto testou a diversidade de injeção com
um protocolo que INTRODUZ a não linearidade medida. **"Gargalo físico" fica SUSPENSO até o piloto condicionado.** (iii) Seção 3.2 do preprint (soma sozinho):
usa a checagem (contaminação < 1%) → FICA DE PÉ.
**CONDIÇÕES ANTES DE RODAR — PROPOSTAS DECLARADAS AQUI (antes de medir), sobre as regras do item 144.** Tudo no θ base, pelo MESMO código das unidades
(`EtapaAUnit._run`, mesmo repouso da cache, CVode 10⁻⁸; M1: degrau 100 ms → 1100 ms, 1150 ms; M4: α início 5 ms, τ 5 ms, 300 ms).
**(a) M4 PERTO DO LIMIAR.** Limiar local (item 144): menor amplitude cuja deflexão de pico NO PONTO excede em 50% a predição linear de 0.02 nA — grade
geométrica 0.02 × 1.25^k até 3 nA, bisseção até 0.25% relativo (a resolução do item 141). Sem limiar até 3 nA → ficam as amplitudes antigas (0.2/0.5/1.5),
com o teto e o teste abaixo. **Teto:** voltagem absoluta ≤ +60 mV no ponto e no soma; 1.2× acima do teto → a maior amplitude que o respeita (bisseção 0.25%),
que tem de ficar ACIMA de 1.0× o limiar (senão a amplitude é omitida). **Teste de condicionamento de CADA amplitude A:** rodadas em A × (0.98, 0.99, 1, 1.01,
1.02), leituras no ponto e no soma, pela cadeia e pela `representar` (as 5 amplitudes no papel das avaliações): **PASSA se** (i) IDENTIDADE: em cada leitura
a contagem do detector é a MESMA nas 5 e, havendo disparos, a identidade da representação vale nas 5; (ii) LATÊNCIA (item 141): CADA tempo de disparo usado
(os K da base; K = 1 → a latência do 1º) muda **< 1 ms por 1%** de amplitude (diferença central em ±1%). Aplicado a TODAS as amplitudes, não só às a < 10% do
limiar (o evento do detector não coincide com o limiar de supralinearidade — item 142). **PASSO DECLARADO se falhar:** afastar do limiar em 0.1× o limiar
(0.9 → 0.8 → 0.7 → 0.6; 1.2 → 1.3 → 1.4 → 1.5; 0.5 → 0.4 → 0.3 → 0.2), no máximo 3 passos, cada um com teto e teste; para cima nunca além do teto; sem amplitude
que passe → a amplitude é OMITIDA naquele ponto (registrada).
**(b) M1 LINEAR POR VERIFICAÇÃO.** R_in = (V̄₊ − V̄₋)/20 pA com ±10 pA (média 1050–1100 ms) no ponto; I = ΔV_alvo/R_in, ΔV_alvo = 5 mV. **Simetria:**
ρ_I = máx_t |y₊ + y₋| / máx_t |y₊ − y₋| no traço do próprio ponto (deflexões pela cadeia; a resposta sem estímulo é 0) **≤ 0.1** — o MESMO índice e o
MESMO limite (RHO_MAX) da 2ª diferença por linha (itens 111/113), aplicado ao eixo da amplitude; o mesmo índice nas 504 leituras é reportado (não decide).
**Falhou → reduzir à METADE o alvo naquele ponto** (5 → 2.5 → 1.25 mV; uma não linearidade quadrática tem ρ_I ∝ ΔV) e repetir; falhou a 1.25 mV → a cadeia
PARA e reporto.
**(c) BORDAS DO DEGRAU.** Nas amplitudes finais do M1 (±I), leituras nos 503 pontos + soma, cadeia + detector: **PASSA se nenhum disparo é detectado em
nenhuma leitura** (em particular no ponto de injeção: a voltagem entra até o fim, nada é cortado no salto); e as amostras retiradas pela cadeia são exatamente
os instantes de liga/desliga (100 e 1100 ms). Reportado ao lado (não decide): no protocolo ANTIGO (50 pA, traços gravados do piloto, as 61 avaliações) a
leitura do ponto foi cortada?
**Regressão:** amplitudes por ponto num arquivo lido pela unidade; com as amplitudes forçadas às antigas, os traços de base e de um subpasso de eixo
(apic_Ca_HVA_zona_mais) de g_apic[36]_16 têm de ser IDÊNTICOS bit a bit aos gravados do piloto (decide); a base de g_apic[60]_32 contra o migr64 é reportada.
**Testes com resposta conhecida antes do uso** (sintéticos): R_in de um compartimento passivo (1/(g·área)); ρ_I num traço com termo quadrático conhecido e
num passivo (≈ 0); limiar e teto por bisseção em respostas modelo com limiar conhecido; latência/identidade com disparos sintéticos de tempo conhecido
(aparece a ±2% → falha; longe → passa); o passo e a omissão; detector de borda com salto de 25 mV (detecta) e de 5 mV (não).
**Portão:** a cadeia só segue (unidades, direções) se TODOS os pontos passarem em (b) e (c), a regressão for idêntica e cada ponto tiver ≥ 1 amplitude do M4.
**DECISÃO (do usuário, declarada antes): a regra do item 137** — σ_lin(6) ≥ 1.5× σ_lin(2) com τ = 10 E 50 ms → a diversidade de injeção é alavanca e a Etapa A
completa se justifica (com protocolos condicionados); abaixo → gargalo físico, próximo passo repetição/não linear. **Proposto (declarado):** calculada na
análise COM a faixa [−110, +60] mV (linhas não fisiológicas em qualquer perturbação usada fora, item 144); a sem faixa reportada ao lado.
**Execução, tudo pela fila:** condicionamento (5 pontos) → avaliação/portão + regressão → 5 unidades (61 subpassos) → Gram das 6 → direções → REPOUSOS das
direções calculados ANTES, uma vez (partição disjunta entre processos) → funcional ao longo das direções além da faixa → repouso absoluto (vrest) → rodadas
de direções → análise (com e sem faixa). A somática é reaproveitada.

**147. RESULTADOS (2026-10-22 15:24) — CONDICIONAMENTO POR PONTO: OS 5 PONTOS PASSAM (a)–(c); REGRESSÃO IDÊNTICA BIT A BIT; PORTÃO ABERTO.**
**Testes com resposta conhecida (antes do uso, `etapaA_condiciona_teste.py`): 19/19 OK** — R_in de um compartimento passivo = 1/(g·área) (795.774715 MΩ
nos dois); ρ_I passivo 8.5×10⁻¹²; ρ_I com termo quadrático exato; regra da metade (5 ✘ → 2.5 ✔; c = 0.1/mV: nenhum); limiar por bisseção (degrau em 0.7 nA;
supralinear suave 0.33651 × 0.33636 analítico; sublinear → nenhum); teto 1.2988 (1.3); latência sintética −0.0802 × −0.0800 ms por 1%, falha pela latência
(−4.45 ms por 1%) e pela identidade (disparo aparece em +1%); passo/omissão/teto nos 4 casos; detector de borda (25 mV detecta no liga do M1p e no desliga do
M1m; 5 mV nada). **Regressão** (amplitudes forçadas às antigas): g_apic[36]_16 base e apic_Ca_HVA_zona_mais × piloto — M1m, M1p, M4 **IDÊNTICOS bit a bit**;
g_apic[60]_32 base × migr64 também idêntico (reportado). (`etapaA_condiciona.py`, 5 trabalhos da fila; 35–50 simulações e 48–87 min por ponto — a
estimativa de ~20 min estava baixa.)
| ponto | R_in (MΩ) | M1 (5 mV): I | ρ_I no ponto | (c) | limiar local M4 | M4 (fator do limiar) | V máx M4 | antigo 50 pA: ponto |
|---|---|---|---|---|---|---|---|---|
| g_apic[60]_32 (800 µm) | 113.1 | 44.2 pA (era 50) | 0.033 | passa | 0.409 nA | 0.204 / 0.368 / 0.490 (0.5/0.9/1.2×) | −52 / −31 / 0 mV | inteira |
| g_apic[36]_16 (tronco) | 42.2 | 118.5 pA | 0.059 | passa | 1.809 nA | 0.905 / 1.628 / 2.171 | −55 / −33 / +31 | inteira |
| g_apic[9]_16 (oblíquo) | 597.9 | 8.4 pA | 0.020 | passa | 0.084 nA | 0.042 / 0.075 / 0.100 | −57 / −38 / +8 | **CORTADA** |
| g_apic[44]_48 (tufo) | 368.6 | 13.6 pA | 0.071 | passa | 0.110 nA | 0.055 / **0.088 (0.8×)** / 0.131 | −50 / −37 / −6 | **CORTADA** |
| g_apic[64]_48 (tufo) | 437.4 | 11.4 pA | 0.073 | passa | 0.075 nA | 0.038 / 0.068 / 0.090 | −52 / −35 / −17 | **CORTADA** |
Nenhum ponto precisou reduzir o alvo do M1 (todos a 5 mV). **(a):** 14 de 15 amplitudes passaram de primeira; **g_apic[44]_48 a 0.9× FALHOU a identidade**
(o evento no ponto aparece/some dentro de ±2%) → o passo declarado levou a 0.8×, que passa; nenhuma omitida; os tempos usados mudam ≤ 0.02 ms por 1% (g60).
**(c):** zero disparos nas 504 leituras em ±I, nos 5 pontos; amostras retiradas = 100.0 e 1100.0 ms. Reportado (não decide): ρ_I máximo nas 504 leituras
passa de 0.1 em leituras distantes (tronco 0.122 em g_apic[44]_51; g44 0.113 em g_dend[68]_3; g64 0.112) — a decisão é no ponto, como declarado.
**ACHADO DO PROTOCOLO ANTIGO (reportado ao lado, não decide):** no oblíquo e nos dois pontos do tufo, a 50 pA a leitura do PRÓPRIO ponto foi **CORTADA PELO
DETECTOR NO SALTO DO DEGRAU, nas 61 avaliações** — M1p na amostra 998 (liga, 100 ms), M1m na 10997 (desliga, 1100 ms): a voltagem do ponto ficou fora e
entrou no lugar um "tempo de disparo" que é o cruzamento do salto do degrau. Em g60 e no tronco, inteira. Os dados do ponto de injeção no piloto antigo,
nos 3 pontos de alta impedância, não eram voltagem. Registrado também: o R_in nesses pontos foi medido com ±10 pA que já dão 4–6 mV (assimétrico: g44
+3.92/−3.45 mV) — a premissa "±10 pA = regime linear" do item 144 vale só aproximadamente; o que decide é a simetria na amplitude final (passou).
Comparação com as amplitudes antigas (item 144 pediu): g60 M1 44 pA (≈ 50), M4 topo 0.49 nA (era 1.5, a não fisiológica); o TRONCO SOBE (M1 118 pA, M4 até
2.17 nA — o 1.5 nA antigo estava a 0.83× do limiar, sublimiar); oblíquo e tufo descem ~4–6× no M1 e ~4–15× no M4. A cadeia segue (unidades → direções →
repousos → funcional → rodadas de direções → análise).
**Andamento (2026-10-23 08:30):** 5 unidades prontas; Gram combinado das 6 → **24 direções relevantes** (antigo: 26); **σ* iid (sem viés, sem regra) =
3.57 mV** (antigo 13.4); 3 direções além do fator 2 (v_1, v_3, v_4) → funcional; 48 repousos das direções calculados ANTES em partição disjunta (0
falhas, nenhum em dobro); rodadas de direções em curso.

**148. DECISÃO DO USUÁRIO (2026-10-23 ~08:40) — ACRÉSCIMOS À ANÁLISE DO PILOTO CONDICIONADO, SEM SIMULAÇÃO NOVA. DECLARADO ANTES DOS NÚMEROS.**
**REGISTRADO:** (i) σ* iid (6 unidades): **13.4 mV (antigo) → 3.57 mV (condicionado)** — quase três quartos da informação aparente do piloto antigo vinham de
amplitudes não fisiológicas, leituras cortadas e respostas grandes demais. (ii) **LIÇÃO: a especificação é RELATIVA AO ESTÍMULO.** Todo "ruído máximo
tolerável" é reportado JUNTO com as amplitudes aplicadas; o limite real inclui o quanto o dispositivo pode empurrar a célula sem sair do regime linear e
fisiológico — PARÂMETRO DE PROJETO, não só o sensor. (iii) **Todos os números de especificação feitos com protocolos NÃO condicionados (checagem/item 132,
item 136, piloto antigo) ficam como HISTÓRICO; o preprint usará os condicionados.** Reportar junto com o resultado da regra do item 137.
**(1) SOMA SOZINHO × COMBINADO CONDICIONADO (implementação declarada):** o soma sozinho (só a leitura do soma com injeção somática: M3 no soma + M5;
`etapaA_piloto.py --so-soma`, o caminho que reproduziu EXATAMENTE o item 136 no controle do item 145) refeito com a regra do item 132 nas direções do
piloto CONDICIONADO (Gram das 6; DETERMINADAS = as além do fator 2 com o funcional DENTRO nos dois extremos, do Fdir condicionado) — a somática não
mudou, mas as direções conhecidas sim; contra o conjunto "2 injeções" condicionado do piloto (soma + g_apic[60]_32), nas MESMAS direções, 4 modelos
de ruído. **Desvantagem = nível do combinado / σ*_soma**, com a convenção do item 136: nível = σ* se certificado; senão o extremo INFERIOR do intervalo
(σ_lin) — e também contra o superior (σ*), reportado. Versão que decide: COM a faixa [−110, +60] (como no item 146); sem a faixa ao lado. "Antes" =
item 136 (31× / 12.9× / 2.8× / 2.9×; combinado com direções do próprio Gram de 2) e, como referência do MESMO método, o "2 injeções" do piloto antigo.
**(2) PISO NUMÉRICO COM SINAIS MENORES (implementação declarada):** piso(10⁻⁸) do Gram combinado = ‖J8 − J10‖₂ = √λmax(Σ_u D_u) (a definição dos
itens 110/118; piso(10⁻¹⁰) = piso(10⁻⁸)/87, a razão medida), com **D da somática MEDIDO** (a unidade é a mesma: comb64_v123) e **D de cada distal
condicionada ESTIMADO pelo D medido da distal** (itens 110/118, protocolo antigo, ‖·‖₂ = 3.7×10⁻³ — o único piso distal medido; ESTIMATIVA: erro
absoluto do solver ∝ atol, não ∝ amplitude). Reportado para cada uma das 24 direções relevantes: σ_i/piso e, mais fino, o piso PROJETADO na direção,
√(v_iᵀ D v_i). **Checagem exata da parte somática, sem simular** (os traços da somática a 10⁻¹⁰ existem): σ_i com a somática a 10⁻⁸ × a 10⁻¹⁰ (Grams
do comb64, os mesmos cortes) mantendo as distais — |Δσ/σ| ≤ 10% (limite do item 118); a parte distal continua ESTIMADA (avaliação parcial, não aprova o
todo). **REGRA (do usuário):** algum σ relevante a menos de 10× o piso → PROPOR uma unidade a 10⁻¹⁰ e o custo; NÃO rodar sem confirmação. **"A de menor
amplitude" (declarado):** a distal condicionada com o MENOR traço do Gram (iid) — a de menos sinal, onde um erro absoluto pesa mais; as amplitudes
aplicadas reportadas ao lado.

**149. DECISÃO DO USUÁRIO (2026-10-23 ~09:10) — AJUSTE NA CHECAGEM DE TOLERÂNCIA (item 148 (2)). DECLARADO ANTES DOS NÚMEROS.**
A norma global ‖J8 − J10‖₂ é o erro na PIOR direção possível; o deslocamento de σ_i depende, em 1ª ordem, só da projeção do erro na própria direção:
δσ_i ≈ u_iᵀ (J8 − J10) v_i. Evidência no registro: item 118, σ mínimo 14.6 a ~2.4× do piso global 6.0 e mudança real ≤ 0.69% entre 10⁻⁸ e 10⁻¹⁰. **A
regra do 10× com o piso GLOBAL é condição SUFICIENTE, não necessária.** **DECIDIR POR:** (a) piso PROJETADO por direção, |u_iᵀ (J8 − J10) v_i| / σ_i, onde
houver J10; (b) a troca EXATA da somática (10⁻⁸ → 10⁻¹⁰) e a mudança real de cada σ_i. **Critério (o do item 75): 10⁻⁸ basta se cada σ relevante muda ≤
10%.** A parte distal continua só ESTIMADA; se a projeção estimada da distal passar de 10% em alguma direção relevante → propor a unidade de menor sinal a
10⁻¹⁰ com custo. A regra global reportada ao lado, como referência.
**Implementação (declarada):** (a) sem guardar J: com u_i = J v_i/σ_i, a contribuição de cada unidade é (J_u v_i)ᵀ E_u v_i / σ_i e, como só a parte
simétrica entra numa forma quadrática, **v ᵀJ8ᵀ(J8 − J10) v = ½ vᵀ(G8 − G10 + D) v EXATAMENTE** → (a) da somática = ½ v_iᵀ(S8 − S10 + D_s) v_i / σ_i² (Grams
do comb64_v123), relativo; (b) = |σ_i(distais + S8)/σ_i(distais + S10) − 1| (autovalores ordenados nos índices das direções relevantes). **Distal
(estimada):** sem J10 das condicionadas, o LIMITE de Cauchy–Schwarz |u_dᵀE_d v| ≤ ‖J_d v‖·‖E_d v‖/σ_i com ‖E_d v‖² = vᵀ D_old v (D medido da distal antiga —
ESTIMATIVA: erro ∝ atol), somado nas 5 distais → Σ_d √(vᵀG_d v)·√(vᵀD_old v) / σ_i² — um LIMITE SUPERIOR da projeção (o alinhamento real entre u e E v é
desconhecido). **Validação antes do uso:** (i) sintética — J8, J10 = J8 + E pequeno, aleatórios: a fórmula de 1ª ordem × a mudança exata de σ e o limite ≥
a projeção; (ii) nos dados do item 118 (distal antiga + somática, J10 medidos): a 1ª ordem por direção × as mudanças reais (pior 0.69–0.71%), e o limite de
Cauchy–Schwarz da distal × a projeção medida dela.
**Validação (antes do uso):** **(ii) dados do item 118: 1ª ordem pior 0.711% × real 0.714%; |1ª ordem − real| ≤ 0.009 ponto percentual nas 30 direções;
limite de CS da distal ≥ a projeção medida em todas (folga mínima 11.8×)** → a fórmula reproduz as mudanças reais. **(i) Sintético — a 1ª versão do teste
FALHOU em dois pontos, registrados:** (2) exigia |1ª ordem − exata| ≤ 1% do valor com E grande — MAL ESPECIFICADO: com σ pequeno o termo de 2ª ordem
(~‖Ev‖²/σ) não é desprezível (resíduo 1.8×10⁻⁴ sobre mudança 9.5×10⁻⁴); (4) exigia 10⁻¹² absoluto, abaixo do arredondamento de G8 − G10 (Grams ~10⁸).
**Corrigido para o que a teoria garante:** (2a) o resíduo é de 2ª ORDEM — cai **3.99–4.00×** quando E cai à metade; (2b) resíduo ≤ vᵀDv/σ²; (4) tolerância
de arredondamento ε‖G‖/σ² (6.9×10⁻¹¹) → **5/5 OK**. **Consequência para o critério:** a estimativa da distal passa a ser **CS da 1ª ordem + o termo de 2ª
ordem Σ_d vᵀD_old v/σ_i²** (sem ele o "limite" não limitava) — mudança de implementação feita ANTES dos números do piloto condicionado.

**150. RESULTADOS (2026-10-23 14:00) — PILOTO CONDICIONADO: PELA REGRA DO ITEM 137, A DIVERSIDADE DE INJEÇÃO É ALAVANCA (2.23× / 2.45×); SOMA SOZINHO
CONTINUA EM DESVANTAGEM (3.8× a 39×); 10⁻⁸ BASTA.** (cadeia de 36 trabalhos da fila, 22/10 13:38 → 23/10 14:00; nenhuma suspensão.)
**Funcional (Fdir):** v_1 DENTRO nos dois extremos (pior 0.08 / 0.15) → DETERMINADA pela faixa; **v_3 e v_4 FORA** — num extremo de cada, o CaBurst_PA1
DESAPARECE (contagem 1 → 0). **Faixa fisiológica: 0 linhas fora em TODAS as unidades, protocolos e perturbações (inclusive as excursões das direções)** →
as análises com e sem a faixa são IDÊNTICAS (o teto funcionou além do θ base).
| conjunto | iid: σ* / σ_lin | OU 1 ms | OU 10 ms | OU 50 ms |
|---|---|---|---|---|
| 2 inj. (soma + g60) | 3.22 / 5.62 → CERT. 3.22 | 0.863 / 1.18 → CERT. 0.863 | [0.322; 0.412] | [0.310; 0.455] |
| 4 inj. (+ tronco, oblíquo) | 4.63 / 4.72 → CERT. 4.63 | [1.29; 1.66] | [0.695; 1.18] | [0.581; 1.42] |
| 6 inj. (+ 2 do tufo) | 4.63 / 4.72 → CERT. 4.63 | [1.37; 1.66] | [0.717; 1.18] | [0.759; 1.42] |
**σ_lin(6)/σ_lin(2): iid 0.84, 1 ms 1.16, 10 ms 2.23, 50 ms 2.45 → REGRA DO ITEM 137 (τ = 10 E 50 ms ≥ 1.5×): A DIVERSIDADE DE INJEÇÃO É ALAVANCA → a Etapa A
completa se justifica, COM PROTOCOLOS CONDICIONADOS** (NÃO lançada: precisa de plano e custo novos — condicionamento em cada ponto da grade). O veredito do
piloto ANTIGO ("gargalo físico", 0.68 / 1.06) se INVERTE — coerente com o item 146 (ii): com o M1 condicionado, o tufo SOBE o σ_lin (4 → 6 inj.: 0.581 → 0.759
a 50 ms), em vez de baixá-lo. **Registrado ao lado (não muda o veredito):** (i) a razão vem sobretudo do σ_lin BAIXO da injeção única condicionada (0.32 /
0.31 mV); com 6 injeções o σ_lin (0.72 / 0.76) fica perto do da checagem ANTIGA (0.81 / 0.83) — o ganho é relativo ao conjunto condicionado; (ii) com ruído
lento, mesmo 6 injeções dão INTERVALO, não certificação — σ_lin segue limitante (v_3, uma das direções FORA); (iii) σ* de 4 e 6 injeções IGUAIS (3 algarismos)
— o tufo não acrescenta informação ao σ* (traço do Gram: tufo 8×10⁶ e oblíquo 3×10⁶ contra tronco 1.1×10⁹), só ao σ_lin; (iv) σ_lin da parte distal (a
somática sem direções), como antes. **Especificação relativa ao estímulo (item 148):** estes números valem para as amplitudes do item 147.
**(1) SOMA SOZINHO × "2 INJEÇÕES" (desvantagem = nível do combinado / σ*_soma; mesmas direções; convenção do item 136):**
| | σ*_soma (iid / 1 / 10 / 50 ms) | desvantagem iid / 1 / 10 / 50 ms |
|---|---|---|
| item 136 (checagem, não condicionada; v_1, v_2 conhecidas) | 0.292 / 0.287 / 0.287 / 0.289 | 31× / 12.9× / 2.8× / 2.9× |
| piloto antigo, "2 inj." (mesmo método; v_1–v_3 conhecidas) | 0.168 / 0.158 / 0.161 / 0.174 | 53× / 23× / 5.2× (14×) / 3.6× (16×) |
| **CONDICIONADO, "2 inj." (v_1 conhecida)** | **0.083 / 0.079 / 0.079 / 0.082** | **39× / 10.9× / 4.1× (5.2×) / 3.8× (5.5×)** |
(entre parênteses: contra o extremo superior do intervalo, σ*.) **O soma sozinho NÃO cumpre em nenhum modelo de ruído; a afirmação 5 do preprint FICA, com
desvantagem ≥ 3.8×** (antes ≥ 2.8×). O combinado condicionado cai 2.5–4.3× (9.03 → 3.22; 3.71 → 0.863; 0.809 → 0.322; 0.827 → 0.310 — "estava inflado"
CONFIRMADO), mas o σ*_soma cai junto. **FRAGILIDADE registrada:** o σ*_soma depende fortemente de QUAIS direções a regra do item 132 torna conhecidas (0.29 /
0.17 / 0.08 mV com {v_1, v_2} da checagem / {v_1–v_3} do piloto antigo / {v_1} condicionado) — a Fisher do soma é muito mal condicionada (item 136: 4.6×10¹²) e
quase todo o seu σ* vem de direções quase não determinadas; a comparação é justa (mesmas direções nos dois lados), mas o número absoluto do soma não é robusto.
**(2) TOLERÂNCIA (regra do item 149):** (b) troca EXATA da somática 10⁻⁸ → 10⁻¹⁰: **pior 1.93% (v_1, σ = 3.0)**; (a) 1ª ordem 2.03%; demais ≤ 0.61%; distal
(limite ESTIMADO com o D da distal antiga, CS + 2ª ordem): **pior 0.007%** → **10⁻⁸ BASTA (≤ 10% em todas as 24 direções relevantes); nenhuma unidade a 10⁻¹⁰
proposta.** Referência (regra global): 6 de 24 σ a < 10× o piso global 6.0 (v_1 a 0.5×) — a regra global teria pedido 10⁻¹⁰ sem necessidade. Menor sinal:
g_apic[9]_16 (traço 3.0×10⁶). Conferências: σ recalculados dos Grams × arquivo de direções 7.8×10⁻⁹; Gram somático do piloto × comb64 7.9×10⁻¹⁷. Ressalva:
a parte distal é ESTIMADA (premissa erro ∝ atol), não medida.

**151. DECISÃO DO USUÁRIO (2026-10-23 ~16:00) — ETAPA A EM s = 400 EM LOTES, COM PARADA DECLARADA (plano e custo; NÃO lançar) + AVAL DO MARTEL PARA O DISCO.**
**REGISTRADO:** (i) regra do item 137 satisfeita (2.23 / 2.45): a diversidade de injeção é alavanca COM PROTOCOLOS CONDICIONADOS; veredito do piloto antigo
invertido. (ii) A razão vem sobretudo do σ_lin baixo da injeção única condicionada; de 4 para 6 injeções: σ* igual; σ_lin 0.695 → 0.717 (10 ms), 0.581 → 0.759
(50 ms) — **indício de retorno decrescente.** (iii) Afirmação 5 de pé com protocolos condicionados: desvantagem do soma de 3.8× a 39×; σ* absoluto do soma é
frágil (depende das direções fixadas pela faixa); comparação com as mesmas direções dos dois lados. (iv) Tolerância 10⁻⁸ basta com os sinais condicionados (pior
1.93%, somática medida; distal estimada).
**DISCO — AVAL DO MARTEL (condições):** apagar SÓ os traços brutos das rodadas ANULADAS (checagem em float32, piloto antigo não condicionado); ANTES, confirmar e
registrar que nenhuma figura, número do preprint ou verificação pendente depende deles — só dos reduzidos, que ficam TODOS; registrar a lista exata e o tamanho
liberado; nada fora da lista.
**CONFIRMAÇÃO DE DEPENDÊNCIAS (feita ANTES de apagar):** **Quais são:** (a) checagem de tolerância em FLOAT32 — anulada no item ~101 (o piso era quantização do
armazenamento: "isso vale também para TODOS os dados antigos (anulados)"): `etapaA_rec/atol1e8`, `etapaA_rec/atol1e10` (distal antiga), `etapaA_rec/soma_atol1e-6`,
`soma_atol1e-8`, `soma_atol1e-10` (somática antiga), `etapaA_conf/migr_1e-8`, `migr_1e-10` (distal migrada em float32) — dtype conferido arquivo a arquivo:
TODOS float32; (b) piloto antigo não condicionado: `etapaA_piloto/unid_*` (4 unidades θ) e `etapaA_piloto/dirs_*` (5 rodadas de direções) — float64.
**Preprint:** o documento não está no repositório; pelo registro, os números do preprint são: linha 4 da tabela (tolerância 10⁻⁸, do comb64 — float64, migr64 +
soma64, Grams reduzidos guardados; nada da lista), afirmação 5/seção 3.2 (soma sozinho — agora dos condicionados, item 150; os históricos do item 136 vêm de
migr64/soma64, fora da lista) e, pelo item 148 (iii), os números de protocolos não condicionados são HISTÓRICO, citáveis pelos REDUZIDOS guardados (piloto.json,
Fdir_piloto*.json, direcoes_piloto.npz, dirF_piloto.npz, Gdir/G.npz, contam_*.json, tufo_*.json, caburst_*.json, repeticoes, tol_gram_combinado.txt…). **Não há
figura gerada destes traços no repositório** (Martel confere do lado dele as figuras do preprint). **Fila do supervisor:** 17 trabalhos citam esses diretórios —
TODOS FEITO, e os "feito" deles são .npz/.json (FICAM) → nada é relançado. **Verificações pendentes:** nenhuma declarada sobre esses traços. **Scripts que os
leem** (só reprodução de resultados PASSADOS, já registrados): etapaA_tol_gram*.py / etapaA_tol_vigia.py (checagem anulada), cadeia_piloto.py, etapaA_tufo_diag /
contaminação (itens 142/145, feitos), **etapaA_rep_check.py (verificação da representação, itens 101/103: lê `etapaA_rec/soma_atol1e-10`)** e
**etapaA_condiciona_aval.py (regressão bit a bit do item 147: lê 6 arquivos de `unid_g_apic[36]_16`)**. **EXCEÇÕES (ficam, mais restrito que o aval):**
`etapaA_rec/soma_atol1e-10` inteiro (0.20 GB — entrada da verificação da representação) e os 6 arquivos da referência da regressão do item 147 (base e
apic_Ca_HVA_zona_mais × M1m/M1p/M4 de g_apic[36]_16, 0.19 GB). Apaga-se SÓ `.npy` (traços brutos); diretórios, `.npz`, `.json`, logs e PIDs ficam.
**APAGADO (2026-10-23 ~16:20; manifesto arquivo a arquivo com bytes e dtype: `neuron/results/limpeza/apagados_2026-10-23.txt`):** 2 497 arquivos `.npy`,
**58.83 GB** — float32 (checagem anulada): etapaA_rec/atol1e8 (183 arq., 2.833 GB), etapaA_rec/atol1e10 (183, 2.833), etapaA_rec/soma_atol1e-6 (122, 0.201),
etapaA_rec/soma_atol1e-8 (122, 0.201), etapaA_conf/migr_1e-8 (183, 2.833), etapaA_conf/migr_1e-10 (183, 2.833); piloto antigo: unid_g_apic[36]_16 (177 —
6 da exceção ficam —, 5.480), unid_g_apic[44]_48 / [64]_48 / [9]_16 (183 cada, 5.666 cada), dirs_g_apic[36]_16 / [44]_48 / [60]_32 / [64]_48 / [9]_16 (159
cada, 4.923 cada). Conferido: 0 restantes da lista; exceções presentes; nenhum processo do harness rodando no momento; a fila do supervisor continua
inteira FEITO (nada relançado). Disco: 39 → **83 GB livres**. **NÃO apagados (fora da lista; candidatos para decisão futura do Martel):** migr64_1e-6 e
migr64_1e-10 (float64, 5.67 GB cada — checagem em float64), migr64_1e-8 (5.67 — distal antiga, base do comb64 e do item 132), etapaA_unit/teste (3.07,
float32 — testes da unidade), etapaA_verif (0.60, float32 — verificações do porte), etapaA_rec/passos (0.24, float64), etapaA_rec/verif_paralelo (0.01).
**PLANO EM LOTES (do usuário) — implementação declarada antes de qualquer simulação; NADA lançado.** **Pontos:** a grade de 400 µm tem **20 pontos, todos
apicais** (item 134: 8 / 3 / 9 a 400 / 800 / 1 200 µm); a somática é FORA deles; feitos: g_apic[60]_32, [36]_16, [9]_16, [44]_48, [64]_48 → **restam 15 (não 14)**
→ lotes 5 / 5 / 5. **Seleção** (`etapaA_lotes.py`, `results/etapaA_lotes/lotes.json`; regra fixada no código ANTES de rodar): amostragem do mais distante —
a cada passo, o ponto com a MAIOR menor-distância PELO CAMINHO (h.distance) até as injeções já feitas (somática + feitos + os já escolhidos); empate → nome.
Conferências (resposta conhecida): 20 pontos 8/3/9 ✔; g9↔g60 818.3 µm (item 137: 818) ✔; g44↔g64 1 156.4 µm (1 156) ✔. Região pela definição do item 135.
| lote | pontos (região, distância ao soma; menor distância às injeções anteriores) |
|---|---|
| 1 | g_apic[70]_48 (tufo, 1200; 397 µm), [77]_48 (tufo, 1200; 363), [37]_32 (tufo, 800; 359), [19]_16 (oblíquo, 400; 292), [17]_16 (oblíquo, 400; 260) |
| 2 | g_apic[51]_32 (tufo, 800; 224), [67]_48 (tufo, 1200; 207), [29]_16 (oblíquo, 400; 163), [33]_16 (oblíquo, 400; 159), [76]_48 (tufo, 1200; 139) |
| 3 | g_apic[63]_48 (tufo, 1200; 135), [30]_16 (oblíquo, 400; 128), [71]_48 (tufo, 1200; 69), [35]_16 (oblíquo, 400; **20**), [41]_48 (tufo, 1200; **12**) |
(nenhum tronco resta: a grade de 400 µm só tem um ponto no tronco, g_apic[36]_16, feito.) **Por lote:** condicionamento (itens 146/147, mesmos critérios e
passos) → portão → unidades θ (61 subpassos) → Gram ACUMULADO (todas as unidades até o lote + somática) → direções relevantes → repousos das direções ANTES
(partição disjunta) → rodadas de direções em TODAS as distais acumuladas (as direções mudam a cada lote) → funcional nas de raio além da faixa (regra do
item 132) → repouso absoluto → análise COM a faixa (decide) e sem; σ*, σ_lin nos 4 modelos; soma sozinho e piso (item 149) ao lado. **PARADA (formalizada
agora):** PARAR depois do lote b se, para τ = 10 E τ = 50 ms, σ*_b < 1.10·σ*_(b−1) E σ_lin_b < 1.10·σ_lin_(b−1) (os quatro ganhos < 10%; uma queda conta como
ganho < 10%); senão seguir até os 20. Cada lote nas SUAS direções (Gram acumulado); **referência do lote 1 = o piloto condicionado de 6 injeções** (σ* 1.18 /
1.42, σ_lin 0.717 / 0.759 mV, com a faixa). **NÃO incluídos nos lotes** (Etapa A do item 134, a decidir depois da parada): extras por unidade (ganho, posição,
62 geometrias) e o viés por ponto (referências do Hay com as amplitudes condicionadas).
**CUSTO POR LOTE (base MEDIDA no piloto condicionado, 5 processos com disputa; faixas = 24–30 direções e 3–5 além da faixa):** condicionamento 0.9–1.5 h por ponto
(6 h de CPU por lote); unidade θ 8.0–8.5 h (41 h por lote); repousos das direções 48 em 3.0 h com 5 processos (18.6 min cada → 15–19 h); rodada de direções
6.6–7.6 h por unidade (7.0–8.7 h com 30 direções) EM TODAS AS DISTAIS ACUMULADAS; funcional 1.67 h por avaliação (7–11 → 12–18 h); análise ~0.21 h por distal por
passada (com e sem faixa); Gram/direções, Fdir, vrest, soma, piso ≤ 5 min cada.
| lote | distais | CPU | relógio | disco NOVO (GiB) — pico com rodadas de direções apagadas unidade a unidade |
|---|---|---|---|---|
| 1 | 10 | 150–175 h | 32–37 h (~1.3–1.6 d) | +26.5 (θ, fica) + ≤ 21.5–27 em voo → pico 48–54 |
| 2 | 15 | 185–220 h | 40–47 h (~1.7–2.0 d) | +53 acumulado + em voo → pico 75–80 |
| 3 | 20 | 220–265 h | 48–57 h (~2.0–2.4 d) | +79.5 acumulado + em voo → pico 101–107 |
**Total (se não parar): ~555–660 h de CPU, ~5–6 dias de relógio (realista 6–8 com porta/memória).** O custo cresce por lote porque as rodadas de direções
são refeitas em TODAS as distais (as direções vêm do Gram acumulado). **DISCO:** livres 83 GiB. SEM apagar rodadas de direções, o lote 1 sozinho pede 70–81
GiB e o lote 2 é impossível → **a cadeia precisa de redução POR UNIDADE (acumulados G, Jᵀa, aᵀa gravados por unidade e conferidos) e de apagar os traços da
rodada de direções de cada unidade logo depois** (os reduzidos ficam). Com isso: lote 1 cabe (pico 48–54 de 83); lote 2 pede também os traços das rodadas de
direções do piloto condicionado (21.5 GiB; reduzidos guardados) → 104.5 livres; lote 3 pede ainda migr64_1e-6/1e-10 (10.6 GiB, checagem em float64) → 115
(margem 8–14) ou + dirsrel64/dirs64 (6.2) → 121. No fim ficam os θ das 20 unidades (~106 GiB) até a análise final e os extras/viés. **Tudo isso depende de
AVAL do Martel (não está na lista aprovada).** **Código antes de lançar:** (a) acumulação POR UNIDADE gravada + análise a partir dos acumulados — regressão:
nos dados do piloto condicionado, os números de piloto_fis.json BIT A BIT; (b) apagar por unidade SÓ depois de (a) conferido; (c) gerador da cadeia por lote +
avaliador da PARADA (teste sintético de resposta conhecida) gravando SEGUIR/PARAR — o lote seguinte REQUER SEGUIR (ou aval do Martel por lote, a escolher).

**154. DECISÕES DO MARTEL SOBRE O PLANO EM LOTES E O DISCO (2026-10-23 ~16:45). DECLARADO ANTES DE QUALQUER RESULTADO DOS LOTES.**
**(1) APAGAMENTO POR UNIDADE: APROVADO**, só depois da regressão bit a bit dos acumulados contra os números de referência (piloto_fis.json no lote 1);
registrar cada apagamento. **Implementação (declarada):** (a) ANTES do lote 1, regressão do CÓDIGO NOVO: acumulados por unidade das 5 distais + somática do
piloto condicionado, gravados, e a análise feita SÓ a partir deles → TODOS os números de piloto_fis.json (e piloto_inf.json) iguais bit a bit; (b) em cada
lote, por unidade: acumulados (com e sem a faixa) gravados → RELIDOS e comparados bit a bit com os da memória (integridade) → SÓ ENTÃO os traços da rodada de
direções DAQUELA unidade (apenas os .npy de dirs_<ponto>) são apagados, com manifesto (arquivos, bytes) por unidade; os θ ficam.
**(2/3) Traços de direções do piloto condicionado (21.5 GiB, antes do lote 2) e migr64_1e-6/1e-10 (10.6 GiB, antes do lote 3): APROVADOS para remoção
local.** ANTES: com o HD conectado e com espaço, cópia para uma pasta de ARQUIVO FRIO no HD (separada do backup versionado), conferida por soma de
verificação (sha256 arquivo a arquivo); sem HD → apagar e registrar que NÃO houve arquivamento. (Motivo do Martel: se a regra de representação mudar,
esses dados precisariam ser reduzidos de novo.) Com o HD sob suspeita (item 153), a cópia só depois do SMART.
**(4) ENTRE LOTES: a fila SEGUE SOZINHA pela regra de parada declarada (item 151).** Relatório ao fim de cada lote: σ*, σ_lin, ganho sobre o lote
anterior, veredito da parada, disco.
**(5) PONTOS REDUNDANTES (declarado antes de qualquer resultado):** no lote 3, pontos a < 25 µm (um passo da grade fina, pelo caminho) de uma injeção JÁ
FEITA ficam FORA, registrados como redundantes. **Aplicado (geometria, sem resultado de simulação):** **g_apic[35]_16 — 20.2 µm de g_apic[36]_16 (piloto);
g_apic[41]_48 — 11.8 µm de g_apic[44]_48 (piloto) → REDUNDANTES, FORA.** Os outros do lote 3: [63]_48 a 135.3 µm, [30]_16 a 128.1, [71]_48 a 68.7 (ficam);
dentro do próprio lote 3 nenhum par < 25 µm. **Lotes: 5 / 5 / 3 → no fim 18 distais + somática.**
**Antes de lançar:** as três peças de código (acumulação por unidade + regressão; apagamento por unidade; cadeia por lote e avaliador da parada com teste
sintético). Lançar o lote 1 quando verificadas.
**AS TRÊS PEÇAS — FEITAS E VERIFICADAS (2026-10-23 ~17:15; testes com resposta conhecida ANTES do uso):** **(1) acumulação por unidade** (`etapaA_piloto.py
--acumular <unidade> <direções> <prefixo>`: o MESMO `acumula`, com e sem a faixa; grava, RELÊ e confere bit a bit; versão do código — commit e sha256 — no
arquivo; `--acumulados … --variante` faz a análise SÓ a partir deles, conferindo o sha256 do arquivo de direções). **Regressão contra o piloto condicionado
(piloto_fis.json / piloto_inf.json, números e texto): NA FILA** (trabalhos rg154_*, `etapaA_regr154.py` → regr154_ok.json só se idêntica) — é o portão do
lote 1. **(2) apagamento por unidade** (`--apagar-direcoes`: só depois dos acumulados relidos idênticos; só .npy de dirs_*; manifesto por unidade) —
`etapaA_apagar_teste.py`, unidade sintética: (A) 147 .npy apagados, manifesto = arquivos e bytes, θ intactos, .npz ficam; (B) diretório que não é dirs_*
RECUSADO, nada apagado → **2/2 OK**. Arquivo frio (`etapaA_arquivo_frio.py`: cópia → sha256 relido do HD → só então apaga; sem HD: apaga e registra NÃO
ARQUIVADO) — testado sem HD (sintético): OK; o caminho COM HD fica para depois do SMART. **(3) cadeia e parada:** `etapaA_lote_aval.py` (a forma declarada:
PARAR se σ*_b < 1.10·σ*_ref E σ_lin_b < 1.10·σ_lin_ref em τ = 10 E 50) — **6/6 casos sintéticos OK** (inclusive "exatamente 10% → SEGUE" e "queda conta como
< 10%"); `etapaA_condiciona_lote.py` (portão do lote + mescla das amplitudes) — com os 5 pontos do piloto e amplitudes vazias REPRODUZ o amplitudes.json do
item 147; `etapaA_disco_guarda.py` — OK / INSUFICIENTE nos dois casos; `results/etapaA_lotes/cadeia_lotes.py` — ensaio numa CÓPIA da fila: 177 trabalhos
(lote 1: 51, lote 2: 61, lote 3: 63, + 2 de arquivo frio), todo pré-requisito com produtor, nomes únicos. Funcional com zero direções além da faixa: só a base,
lista vazia (robusto). **NA FILA (2026-10-23 17:15): os 177 trabalhos, TODOS esperando regr154_ok.json** — o lote 1 começa sozinho se a regressão for
idêntica; se não, nada começa e reporto. Lote 2 espera lote1/SEGUIR.json + o arquivo frio/apagamento dos traços de direções do piloto condicionado; lote 3
espera lote2/SEGUIR.json + o de migr64_1e-6/1e-10; todo lote começa pela guarda de disco (63.5 / 63.5 / 53 GiB).
**REGRESSÃO DO ITEM 154 (1a) — IDÊNTICA BIT A BIT (2026-10-23 18:25):** acumulados das 5 distais + somática do piloto condicionado gravados e RELIDOS
idênticos (com e sem a faixa); a análise feita SÓ a partir deles reproduz **piloto_fis.json e piloto_inf.json — números IGUAIS e TEXTO IGUAL** (regr154_ok.json).
→ o portão do lote 1 abriu; a fila começa pela guarda de disco.
**SMART DO HD EXTERNO (item 153; saída enviada pelo Martel, 2026-10-23 17:10):** Seagate/Samsung SpinPoint M8 ST500LM012, **overall-health PASSED**;
**Reallocated_Sector_Ct 0, Current_Pending_Sector 0, Offline_Uncorrectable 0, Reallocated_Event_Count 0, Raw_Read_Error_Rate 0** (superfície sem defeito
registrado); **UDMA_CRC_Error_Count 0** (enlace SATA interno limpo); log de erros SMART vazio; 2 testes curtos sem erro; **Power_On_Hours 32** (quase sem
uso); G-Sense_Error_Rate 1 (um choque registrado); Multi_Zone_Error_Rate bruto 40 (VALUE 100, sem limite — anotado para acompanhar; pode vir das escritas
interrompidas). **Leitura:** a queda das 16:12 é mais compatível com alimentação/cabo/conexão USB (ou um esbarrão) do que com falha do disco. **Antes de usar:**
teste LONGO de superfície (~112 min) e correção do NTFS sujo (escritas perdidas às 16:12); a cópia manual HANU_PROJECT/HANU_V8 do HD é NÃO confiável. Uso só
ligado direto numa porta do computador, sem hub, sem mexer no HD durante o uso; nada de varredura do HD durante outra transferência.
**DECISÃO DO MARTEL (2026-10-23 ~17:20) — AVALIAÇÃO DO HD, DECLARADA ANTES DO RESULTADO DO TESTE LONGO:** (1) além da linha do autoteste, reportar os
atributos 5 (Reallocated_Sector_Ct), 197 (Current_Pending_Sector) e 198 (Offline_Uncorrectable), valor BRUTO — **qualquer um > 0 → o disco NÃO serve como
backup, mesmo com o autoteste "Completed without error"; recomendar troca** (no SMART de 17:10: 0 / 0 / 0); (2) **ANTES de qualquer escrita (ntfsfix,
formatação): perguntar ao Martel se há no HD dados que só existem nele;** se houver, copiá-los primeiro (só leitura) e conferir a cópia — a instrução de rodar
o ntfsfix depois do teste foi RETIRADA até essa resposta; (3) disco aprovado e só para backup do projeto → PROPOR ext4 (não fazer sem aval: apaga tudo); se o
Martel usar o HD no Windows, manter NTFS; (4) **a NUVEM é a prioridade do esquema de backup — não depender do HD.** **Respostas do Martel (17:25):** HÁ no HD dados que só existem nele; o HD é usado SÓ neste Fedora → se aprovado, proposta de ext4 (com aval), DEPOIS de
copiar e conferir os dados únicos. Sequência: fim do teste longo (19:04) → atributos 5/197/198 + linha do autoteste → montagem SÓ LEITURA e lista das pastas
de 1º nível com tamanhos → o Martel indica as únicas → cópia (só leitura) para destino com espaço (disco interno ou nuvem, conforme o tamanho e a Etapa A em
curso) conferida por sha256 → só então a proposta de formatação.
**RESULTADO DO TESTE LONGO (19:05; saída enviada pelo Martel):** **Extended offline — Completed without error** (32 h de uso); **atributos 5 / 197 / 198 =
0 / 0 / 0 (bruto)** → **pela regra declarada, o HD está APROVADO.** Anotados: nenhuma queda durante as ~2 h do teste; às 19:05:22 uma desconexão/reconexão
(Power_Cycle_Count 77 → 78: o disco PERDEU alimentação — se não foi o Martel, foi o adaptador/porta USB) — reforça cuidado com a conexão; Throughput_Performance
252 → 56 (252 = "nunca medido" nesse modelo; medido no teste; limite 0); Multi_Zone_Error_Rate continua 40 (não subiu); temperatura 38 °C (máx. 46).
**NTFS DO HD NÃO MONTA (19:07):** "$MFTMirr does not match $MFT (record 0)" — a tabela mestra e o espelho divergem (escritas perdidas na queda das 16:12);
o ntfs-3g recusa até SÓ LEITURA; desde 16:20 TODAS as tentativas (inclusive as automáticas do GNOME) falharam → ninguém escreveu no HD depois da queda.
**Montado SÓ LEITURA pelo driver do kernel (ntfs3, opção ro conferida)** e listado (tamanhos aparentes): Martel 42 GB, HANU 32 GB, $RECYCLE.BIN 24 GB,
MIchelly 6.6 GB, pc 2.7 GB, Aulas de Inglês 2.3 GB, .Trash-1000 0.3 GB, HANU_PROJECT 0.24 GB (+ arquivos do fabricante); ocupado 109 GB (o ntfs-3g dizia
148 GB às 16:08). As cópias do PROJETO no HD trocaram de tamanho (HANU 4.5 MB → 32 GB; HANU_PROJECT 30 GB → 0.24 GB) sem ninguém ter escrito → **tabela
inconsistente; essas cópias NÃO são confiáveis** (o projeto está no computador e na nuvem). HD desmontado de novo depois da lista. **Martel: pastas ÚNICAS =
Martel, MIchelly, pc (~51 GB); destino = disco do computador DEPOIS do lote 1.** **Proteção posta:** os trabalhos de arquivo frio (lt_frio_pcond, lt_frio_migr64)
passam a REQUERER `etapaA_lotes/hd_pronto.json` — sem isso, com o HD não gravável, eles apagariam SEM arquivar; o marcador só é criado quando o HD estiver
pronto (ou por decisão do Martel de seguir sem ele).

**156. LOTE 1 PARADO NO CONDICIONAMENTO DE g_apic[70]_48 (2026-10-24 08:40) — DIAGNÓSTICO; DECISÃO PENDENTE DO MARTEL.**
g_apic[70]_48 (tufo, 1 200 µm): **R_in 986 MΩ** (a ponta de impedância mais alta até agora; os outros: 369–598 MΩ); M1 aprovado (5.1 pA, ρ_I 0.031). A busca
do limiar local do M4 ficou **13 h a 99% de CPU sem terminar**. **Diagnóstico** (`etapaA_condiciona_diag.py`, a mesma grade 0.02·1.25^k pelo mesmo código; em
paralelo, sem decidir): razão à predição linear **1.000 / 1.04 / 1.17 / 1.315 / 1.314 / 1.24 / 1.16 / 1.09 / 1.05 …** (0.02 → 0.12 nA) e depois ~1.07 → 0.97
até 2.17 nA — **NUNCA chega a 1.5** (a supralinearidade de 50% do item 144 não existe nesta ponta); a resposta é quase proporcional, e a voltagem absoluta no
ponto sobe sem limite: −47.8 mV (0.02 nA), +8 (0.076), +38 (0.119), **+66.6 mV a 0.149 nA (passa do teto)**, +656 (0.89), +1 660 mV (2.17 nA); **a 2.71 nA a
simulação não termina** (o CVode a 10⁻⁸ com a membrana a milhares de mV) — é onde o condicionamento travou. Cada simulação até 2.17 nA levou 17–37 s.
**Pela regra declarada (item 146):** sem limiar até 3 nA → as amplitudes antigas (0.2 / 0.5 / 1.5 nA) com o teto → todas acima do teto → OMITIDAS → o ponto
fica com 0 amplitudes do M4 → **o portão do lote FALHA (exige ≥ 1) → o lote 1 PARA** (e o condicionamento nem termina, por causa da simulação a 2.71 nA).
**Opções (a decidir; nada mudado):** (A) **limiar procurado só dentro da faixa fisiológica** (a grade para quando a V absoluta passa de +60 mV) e, **sem evento
local na faixa, M4 em frações da amplitude-teto A_teto** (a maior com V ≤ +60 mV; aqui ≈ 0.13 nA): 0.25× / 0.5× / 0.9× A_teto (≈ 0.033 / 0.067 / 0.12 nA),
com o MESMO teste (a) de identidade/latência e passo de 0.1× A_teto para baixo; (B) ponto só com M1 (portão aceita 0 amplitudes do M4 quando não há evento
na faixa); (C) tirar o ponto do lote (muda a amostragem declarada); (D) manter a regra → o lote 1 para. O processo travado (PID 172068, do supervisor) fica
como está até a decisão (matá-lo agora faria a fila relançá-lo e travar de novo).
**DECISÃO DO MARTEL (2026-10-24 ~08:45): OPÇÃO A.** **Implementado** (`etapaA_condiciona.py`): em cada amplitude da grade a razão à predição linear é testada
PRIMEIRO (como antes); sem evento, a grade PARA quando a V absoluta passa de +60 mV → "SEM evento local na faixa fisiológica"; a amplitude-teto A_teto (a maior
com V ≤ +60 mV) por bisseção (0.25%); M4 = **0.25 / 0.5 / 0.9 × A_teto**, o MESMO teste (a) de identidade/latência, passo de 0.1 × A_teto para BAIXO (≤ 3), sem
amplitude que passe → omitida. **Compatível:** nos 9 pontos já condicionados o limiar está DENTRO da faixa (a maior amplitude usada fica ≤ +30.5 mV) → resultado
idêntico, nada refeito. **Testes (antes do uso): 23/23 OK** — os 19 antigos inalterados + 4 novos (sem evento → None + par do teto, A_teto 0.14435 × 0.14444
analítico; evento SÓ acima do teto → sem evento na faixa; supralinear suave → o MESMO limiar com e sem o teto, 0.336513; frações do teto com passo para baixo →
[0.25, 0.5, 0.8]). O processo travado (PID 172068, gravado pelo supervisor) encerrado por SIGTERM às 09:06 (o SIGKILL de reserva chegou a um processo já zumbi);
a fila relança o condicionamento de g_apic[70]_48 com o código novo. Diagnóstico (PID 196628, meu) encerrado depois de cumprir o papel.

---

*Última atualização: 2026-09-30 — 132 decisões registradas (D132 itens 51–52: a MESMA CADEIA DE MEDIDA nos dois lados (emulação da aquisição: taxa, anti-alias, local, bloqueio nas janelas de estímulo) para o desmame inteiro → P28/P54/P24; integrador é CONDIÇÃO (6 de 56 PAs a dt 0.1) → D116/P54, pico baixo → requisito D123; λ dos axônios declarado antes do resultado (Allen ~40–45 µm, razão ~1 → pode refutar, com ressalva de passivo axonal sem dado; Hay4 913 µm, razão 0.05 → não bimodal = INCONCLUSIVO); injeção comum `stim_common` com autoteste (T1 restore(1), T3 cvode_active NOVA, T2 NÃO reproduz, T6 custo da grade fina NOVA), leitura de junção e portão do detector como autotestes)*
*Registro anterior: 2026-09-29 — 132 decisões registradas (D132: C2 mal declarado (local errado; vale p/ trás — "1 868×" do D130 riscado) e NÃO VERIFICÁVEL (distância de Williams & Stuart 2002 não obtível); seguir com C1+C3 e viés de sinal misto; Beaulieu-Laroche 2018 conferido no PDF — eixo = SEPARAÇÃO ENTRE ELETRODOS → extremo de 408 µm mal posto/INDISPONÍVEL; F1 (c_m) não alcança (368 µm máx.); ruído vira SAÍDA (especificação do sensor); regra 4/5 trocada por p_req 0.90 com 95% (n final 60, ≤1 falha, futilidade 5/15/30); pergunta realista: Hay completo → árvore reduzida; CONVERGÊNCIA NO TEMPO: C1 trivial, C3 só converge com CVode (35.1/25.4 mV; Euler não converge nem a 0.003 ms; Crank–Nicolson dá PA espúrios em dt grosso) e no dt convergido o C3 NÃO CAI pelo sub-critério "decremental" estrito (+1.2 mV 200→300 µm) — veredito virou, banda não alargada; CUSTO: exaustivo ~2×10¹⁰ simulações (10⁴–10⁵ anos-CPU, inviável); escolha = duas etapas (A Fisher/Cramér–Rao ~0.6–1.7 anos-CPU; B pontual a 0.7x̂/1.4x̂, inviável como declarada) — nada lançado, alavancas de custo para decisão; reduzido com LinearMechanism é MAIS LENTO que o completo no NEURON; verificação da redução no Hay em andamento; ITENS 14–20: C3 avaliado nos sítios do dado → CAI (4ª aparição da tolerância zero sobre grandeza contínua), Hay = verdade de base sob C1+C3; CVode obrigatório; NEURON nativo nseg=N ≡ D126 a 10⁻¹³ (divergência inicial = defeito de LEITURA do reduzido no ponto de injeção, corrigido) → adotado, ~15× mais rápido; Etapa A ≈ 26 dias-CPU (viável); B só sanidade (0.7x̂, σ_V, s*, n=10, ≥3 falhas) e mesmo assim ~0.9 ano-CPU por ajuste → fica p/ L2; C++ HHNeuronModel = 1ª ORDEM medida (+1.06 ms no 1º PA a dt 0.1) → P24 possivelmente subestimado 1–1.5 ordens; L2: junções explícitas, não Kron; bAP absolutos do D130 não citáveis até CVode)*
*Registro anterior: 2026-09-29 — 131 decisões registradas (D131: teste de identificabilidade PREPARADO — verdade de base não precisa ser a célula-alvo (identificabilidade é do par estrutura+protocolo; mesma preparação vale para a fidelidade); Hay 2011 (ModelDB 139653, biophys3/cell1, rato P36) verificado: restringido por bAP a 620/800 µm e Ca-spike, NÃO por atenuação; critérios declarados antes; C1 estacionária CAI (50% a 351 µm vs ~332 medido), C3 bAP CAI na borda (27.9/18.7 mV), C2 EPSP do tufo NÃO CAI (1 226× na ponta vs [20, 400]) → Hay reprovado, registrado e parado, nada ajustado; diagnóstico: métrica de PONTA dominada pela impedância local (tronco/nexo 15–204×), critério possivelmente mal posto — decisão pendente, vale retroativamente para a leitura "na ponta" do D130; convergência Δ1/Δ0.5 0.27%; apical 1 300 µm = 1.73 λ passivos, "caso mais difícil" segue hipótese; lacuna: Beaulieu-Laroche 2018 aberto (rato/humano), 2021 tem camundongo TEA sem razões de atenuação, Marti Mengual 2020 camundongo S1/ACC duplo — camundongo V1 segue sem dado; desenho do teste DECLARADO (30 parâmetros, M1–M5, sensibilidade+multipartida+perfil, suficiência FUNCIONAL por conjunto de teste fora do ajuste, perfeito→ruído, espaçamentos incl. D51-oráculo e adaptativo); Rin local + diâmetro dão √(R_m·R_i), não λ)*
*Registro anterior: 2026-09-29 — 130 decisões registradas (D130: alvo dendrítico — o PERISOMÁTICO não desconecta o tufo como o all active (soma→tufo 0.024 vs 3×10⁻⁷; EPSP do tufo 1 868× vs 8.5×10⁷×) mas NENHUM dos dois cai na faixa fisiológica: estacionária ~8× (peri) e 10³–10⁵× (all active) mais atenuada que o rato S1 medido (50% a 332 µm), EPSP do tufo ~10× acima dos >40× medidos, bAP ausente além de 200–300 µm; dados de camundongo V1 (Shai 2015) dão Rin local/repouso/sag mas não atenuação — lacuna; alvo terá de ser construído/ajustado com restrição dendrítica (fatia própria); regra: métricas contínuas > contagens com corte fixo; λ é configuração, não catálogo (obs. sobre D51); teste de identificabilidade registrado no P54)*
*Registro anterior: 2026-09-29 — 129 decisões registradas (D129: TRILHA DO MÉTODO ENCERRADA — o degrau ativo contra o L0 CONVERGIDO (omissão do protocolo corrigida; regra do D127) PASSA nas duas células: contagens idênticas 16/16 no piramidal, ≤2 PA no interneurônio, inclinação/adaptação/latência <1%, ruído 0–0.8%; L0 convergido por amplitude (Δ5/Δ2, refino a Δ1/Δ0.5; 550 pA do interneurônio oscila por borda da janela); a árvore reduzida com nós de bifurcação reproduz o modelo que recebe, passiva e ativamente, erro ~10⁻⁵. PIVÔ: o gargalo passou do MÉTODO para o ALVO (três distâncias: adaptação, dendritos não restringidos, ajuste sobre modelo não convergido); N=16 é fidelidade a artefato, N=1 é cegueira dendrítica; piso ~110/34 compartimentos; pendências: dados dendríticos fisiológicos (registro duplo soma–dendrito L5), tufo no perisomático, que dados o elemento precisa captar (liga ao D96 e à penetração dendrítica), número de energia do substrato)*
*Registro anterior: 2026-09-29 — 128 decisões registradas (D128: critério de RESOLUÇÃO redeclarado = portão passivo em N e em todos os N aninhados mais finos (razão só diagnóstico; proxies mal postos registrados); menor N: interneurônio 8 (K=265, 4 421 estados), piramidal 16 (K=1 745, 28 277 estados — ditado pelo TUFO, livre no ajuste; só com Rin/τ seria N=1); PASSIVO FECHADO para o método (erro da redução ~10⁻⁵; o maior erro está no ALVO); degrau ATIVO: FALHA contra o L0-Allen perto do limiar nas duas células (contagem; latência no interneurônio), passam reobase/inclinação/adaptação/ruído; diagnóstico: o L0-Allen não está convergido no ativo — refinado, converge EXATAMENTE para o reduzido (6 contagens + latência); pendente: comparação contra o L0 ativo convergido, declarada antes)*
*Registro anterior: 2026-09-28 — 127 decisões registradas (D127 adendos 2–4: erro de ESPECIFICAÇÃO do critério de 2ª ordem para auto-voltagem em ponto não-nó (não do método); ALERTA tufo desconectado → registros somáticos não restringem dendritos; métricas separadas em RESTRINGIDAS POR DADOS (Rin, τ) e LIVRES NO AJUSTE (dendríticas); pontos de meio movidos para o ponto de ramificação mais próximo (pós-dados, justificado; faixa inalterada); N=128 declarado antes; referência refinada Δ 0.05 µm; RESULTADO: interneurônio (ii) PASSA → N=8, K=265, 4 421 estados (fidelidade ao L0, não fisiológica); piramidal (ii) FALHA só por 2 métricas basais convergindo RÁPIDO DEMAIS (r 8.8 e 7.2) após cruzamento de zero do erro; todas as métricas de ramificação e do tufo passam; menor N do piramidal NÃO reportado)*
*Registro anterior: 2026-09-28 — 127 decisões registradas (D127: métricas em PONTOS FÍSICOS FIXOS (caminho mais longo por tipo de ramo: meio e ponta; EPSP funcional no tufo e controle basal) + referência L0 fina extrapolada + sequência ANINHADA 1..64 + critério (ii) de 2ª ordem (r em [2.5, 6.5]) — DECLARADO antes; RESULTADO: (ii) FALHA nas duas células — apicais/tufo, Rin e τ do piramidal passam em 2ª ordem limpa; basais do piramidal e Rin/τ/ponto→soma do interneurônio falham; auto-voltagem em ponto não-nó é 1ª ordem inerente (métrica); encaixe interno descartado; curva e menor N NÃO construídos; L0 do Allen erra 14–19% no tufo; tufo do ajuste all active eletricamente desconectado (3×10⁻⁷). Diagnóstico registrado; referências do tufo do D124/D125 RISCADAS)*
*Registro anterior: 2026-09-28 — 126 decisões registradas (D126: método de redução v2 — por ramo, nós de bifurcação explícitos eliminados por Kron (preserva irmãos); (i) EXATO no limite nas duas células (0.0000%, tufo incluído) → o "piso" do D125 era defeito da ferramenta; (ii) monotonicidade FALHA como declarado (interneurônio 4→5, piramidal 5→6) — só nas atenuações da região distal, por serrilhado da fronteira de 150 µm numa sequência NÃO aninhada; Rin/τ/s→p monotônicos; subsequência aninhada 1,2,4,8,16 monotônica (post-hoc, não aprovação); curva e menor N NÃO construídos; métrica do tufo depende 10× da regra de região. + ADENDO ao D125: três correções de raciocínio — menor N exige convergência; piso era da ferramenta; fidelidade×orçamento indecidível (orçamento ~1 fJ/atualização, digital ~pJ — Horowitz 2014 conferido; Landauer ~3e−6 fJ; decide o SUBSTRATO; pendência no P24); critério do tufo mantido com direção funcional; formalismo do Na para depois)*
*Registro anterior: 2026-09-28 — 125 decisões registradas (D125: TOPOLOGIA × N de compartimentos no NEURON — NENHUMA configuração passa o portão passivo nas duas células: piramidal nada passa (cadeia e estrela, N 1..12; estrela acerta Rin/τ/soma→prox mas não a atenuação do tufo); interneurônio passa só em ILHAS (cadeia K=10–14, estrela N=10) que PIORAM ao refinar; o agrupamento por distância NÃO converge (junta ramos paralelos) — no limite 1 nó/segmento o interneurônio passa (K=106) e o piramidal falha d→s +12% por piso do método; ilhas NÃO adotadas como "menor N"; estrela: média por tipo exata (confirmado); generalidade: nenhuma regra serve às duas — evidência aponta topologia = árvore da própria célula (configuração); ativo NÃO rodado; custo: estados 27/21/16 por AIS/soma/dendrito, NaV Markov ~5× o custo de um Na HH por segmento; interneurônio árvore 1 723 estados (36×), piramidal 4 219 (88×); P24 = 23/50 fJ por passo por neurônio. + D114 REABERTO: a cadeia de 4 falha no passivo)*
*Registro anterior: 2026-09-25 — 124 decisões registradas (D123: ESTRUTURA GERAL proposta — catálogo por pessoa (entradas imutáveis com procedência; formalismos HH/Markov/Ca) + configuração por neurônio (geometria, passivo, temperatura, reversais, referencial −14 mV, Ca, lista explícita de canais × densidade em 4 compartimentos); HANU_P estima densidades/seleção/passivo, nunca cinética; REGRA da mesma preparação relaxada SÓ para a cinética do catálogo substituto (validação da biblioteca inteira + procedência), estrita para a configuração; achados: premissa do catálogo compatível com o Allen POR CONSTRUÇÃO (328 ajustes, zero parâmetro de cinética; teto visível), NENHUMA variante do Allen tem NaP dendrítico, perisomático do piramidal tem início contínuo, Rin não é critério duro; escada L0→L0.x→L1→L2 (estrutura/mapeamento/implementação). D124: bug de área (6ª aparição; 7 407 µm², não 11 740; conversor pelo soma não afetado; sumidouro do D114 ~2.2× o da célula), apical INTACTO (cortes no basal), axônio truncated = default do AllenSDK; L1 no NEURON: PORTÃO PASSIVO FALHA nas duas células — piramidal por MÉDIA entre tipos (basal+tronco apical), e por tipo quebra a CADEIA; interneurônio por AGRUPAMENTO (1 nó); ativo não rodado; a pergunta vira topologia/número de compartimentos. Vendorizados .mod, 4 genomas, resumo dos 328, scripts NEURON)*
*Registro anterior: 2026-09-24 — 122 decisões registradas (D122: DETECTOR de PA trocado para o critério IPFX do Allen no soma (dV/dt>20, pico>−30, proeminência≥20) — o antigo AIS>0 perdia PAs atenuados (21 de 602 no ruído do Allen; ISIs fundidos = P26 pelo HH); ENGATE A e ELO 1 mudam juntos; nenhum teste mudou de contagem (a suíte não cobria o regime) → teste novo CountsAttenuatedSpikes (falha com o detector antigo). CONTROLE NEGATIVO APÓS ATIVIDADE: o modelo é silencioso a frio mas dispara para sempre após atividade → DISABLED_ModelIsSilentAfterActivity (falha: 63 PA/2 s), critério de aceitação da fatia estrutural do P54. LIÇÃO: controle negativo cobre o estado APÓS atividade. + ADENDO 2 ao D121: diagnóstico de classe — trem do D120 é oscilação soma–dendrito do NaP DENDRÍTICO (gerador sozinho = classe 3; knock-out causal); D120/D121 em parte artefato; tensão do D114 em aberto; corrente A REFUTADA (K rápida L5 é de limiar alto); nenhum início contínuo; correção do anel (15.4 Hz, não 31). 204/204 + 1 desabilitado)*
*Registro anterior: 2026-09-23 — 121 decisões registradas (ADENDO ao D121, nenhum parâmetro alterado: (1) âncora do Kir é de OUTRO tipo celular — Leão et al. 2012 (não 2011) é DCN, modelo pontual, valor escolhido por comportamento; 4ª aparição do padrão "fonte que soa certa, preparação errada"; a curva de retificação (V½ −70) é de estriado (Steephen&Manchanda) e não acompanha o g_max; cortical Day 2005 usa 0.06 mS/cm² V½ −90 (g efetivo em repouso ~48× menor); densidade medida em L5 não encontrada → g_Kir=1.0 PROVISÓRIO; REGRA: toda âncora confere MESMA PREPARAÇÃO (espécie/região/tipo/temperatura; g_max+cinética da mesma fonte). (2) f-I completa medida: reobase 14.5 pA vs 290 (~20×), início DESCONTÍNUO 0→30 Hz vs contínuo desde 1 Hz, ganho ~0.03 vs 0.080 Hz/pA, faixa 30→42 vs 1→11 Hz; ~~repouso = foco perto de Hopf (anel ~31 Hz = frequência de início)~~ [CORRIGIDO 2026-09-24: anel 15.4 Hz]; Rin 33–40 vs 94 MΩ; "bloqueio >30" é em parte artefato do detector (bloqueio real ≥47 µA/cm²). Distal: sustentado por NaP, não HCN/CaT; repouso BIESTÁVEL (estado B: distal −73.5, soma −76.5; reobase 35 pA, f-I ainda plana); axial líquida no soma +54 pA. Ganho da f-I = alvo explícito da pergunta 2)*
*Registro anterior: 2026-09-17 — 121 decisões registradas (D121: REPOUSO SILENCIOSO — o modelo do D120 oscilava ~48 Hz sem entrada (comparação Allen invalidada). Hipótese do Kdr CONFIRMADA: o Kdr de lula g=36 dava K de repouso acidental (I_Kdr a −70: 0.38 vs 0.05 com g=5, 7.2×); silencia a g_Kdr≥20. Conserto: ACRESCENTAR Kir (retificador — fecha ao despolarizar, segura o repouso sem matar o PA; K2P linear mata), g_Kir=1.0 mS/cm² ANCORADO em Leão et al. 2011 (piramidal silenciosa). Reversais Pospischil commitados JUNTO (E_Na +50, E_L −70; isolados quebravam, com Kir funcionam). NaP=0.5 confirmado fisiológico. Verificadas 2 propriedades: (a) repouso −73.3 mV silencioso, 0 espontâneos, Ca 0.10; (b) dispara trem, PA nasce no AIS. Teste novo ModelIsSilentWithoutInput (controle negativo) + EngateA/OneSpikeOneEvent reescritos com condição de controle. Allen re-rodada LIMPA: 40/44/40 vs 0/1/11, noise 516 vs 45 — super-excitável = pergunta 2, não mais oscilador. 203/203)*
*Registro anterior: 2026-09-17 — 120 decisões registradas (D120: modelo COMPLETO dispara repetitivamente com D114 intacto — 3 trocas ancoradas: densidades corticais Pospischil 2008 (gNa 120→50, gKdr 36→5, gKM 0.5→0.07, gleak 0.03→0.1; eram de lula), Na do AIS ancorado em Kole 2008 (250 mS/cm² → scale 3→5, critério=densidade absoluta não "faz disparar"), e correção do BK (V½ era −20 mV/meio-aberto em repouso → +150 mV/fechado, Latorre&Cui; 3ª aparição do padrão do 0.01; BK mantido não zerado). Resultado: 49–58 PA regulares, PA NASCE NO AIS e invade o soma. Limitações p/ pergunta 2: janela estreita (bloqueia >~25 µA/cm²), repouso deslocou p/ −82 mV, Allen super-excitável (150/310/430→110/49/49 vs 0/1/11). 1 teste (EPSP) reescrito relativo ao repouso medido; 202/202)*
*Registro anterior: 2026-09-17 — 119 decisões registradas (D119: modelo de identidade da fase seguinte — identidade é a CADEIA de mudanças graduais, não o estado (backup antigo = outra pessoa; = D01 no eixo temporal do sujeito); aposta: pequenas mudanças mantêm o eu, aprimoramento muda o ser e ele ainda se sente ele; assimetria do amadurecimento (lento/não-escolhido/sem-alvo vs rápido/deliberado/direcionado) + recursão (melhorar cognição muda quem escolhe a próxima) remove os 2 freios → ritmo MEDIDO, não só pequeno; a conversão mede TOLERÂNCIA A MUDANÇA se registrar os valores dos 3 fatores (extensão D118) = 1ª medida empírica de margem; backup compra reversão mas a versão melhorada pode não querer voltar e é ela quem avalia — quem reverte fica em aberto; referência próxima vs distante, backup antigo não é "o verdadeiro eu"; nada implementado)*
*Registro anterior: 2026-09-17 — 118 decisões registradas (D118: requisitos de preparação para a fase seguinte — fidelidade agora/capacidade depois (desmame é portão de entrada; melhoria posterior por RITMO, mesmo princípio noutro eixo; sem alvo na melhoria, verificação não transfere); 3ª categoria de dados REGISTRAR, critério "o que não pode ser remedido depois" (biológico irrepetível sai, sintético re-obtenível fica) — catálogo, assinatura/veredito/params por neurônio, conexões, FALHAS, correlação; via cateter/D63-D76; 3 requisitos: observabilidade permanente, modificabilidade, agrupamento como benefício acidental; ressalva substrato≠sistema, acesso≠capacidade; registro de critério, nada implementado)*
*Registro anterior: 2026-09-17 — 117 decisões registradas (D117: inativação do Na corrigida — h_inf era α/(α+β), crescia com V (h_inf(+41)≈0.996), Na nunca inativava → bloqueio de despolarização do P54; vira Boltzmann M&S 1/(1+exp((V+65)/6.2)), τ_h segue de α/β; 2ª aparição do padrão "cita a fonte e implementa outra coisa" (1ª: 0.01/D112); m e n conferidos corretos (ativação usa α/(α+β)), f e q já eram Boltzmann; bloqueio some (PA+AHP real) mas disparo repetitivo sob DC não volta — reobase de onset ~100, 1 PA/pulso, o resto é pergunta 2; 6 testes: drive 50→200/300 e os 3 nomeados reescritos p/ borda/trem pulsado; 202/202)*
*Registro anterior: 2026-09-14 — 116 decisões registradas (D115: guard de estabilidade — detecta V não-físico (faixa dos reversais, não só NaN), congela o HH e bloqueia o collector mas deixa a FSM seguir, marca/conta à parte, não exceção; expôs que o modelo explodia em TODO disparo a dt=0.1 e a suíte estava verde sobre lixo. D116: integrador EXPONENCIAL no V — fecha P52 #3, estável a dt=0.1; 6 testes de disparo voltam com PAs reais; OneSpikeOneEvent reescrito p/ bloqueio de despolarização real; guard vira rede de segurança)*
*Registro anterior: 2026-09-10 — 114 decisões registradas (D114: geometria dos compartimentos corrigida — área ~26k µm² ancorada em piramidal L5, cilindro equivalente de Rall; EPSP unitário volta a ~1 mV (era ~9–13); N vai de 1 para 5, limiar real; densidades de canal inalteradas eram fisiológicas; N-de-dezenas p/ entrada distribuída fica como limitação assumida do modelo de 4 compartimentos; 8 testes reajustados no drive/fixture, modelo intocado)*
*Registro anterior: 2026-09-10 — 113 decisões registradas (D113: unidades do acoplamento axial fechadas — erro dimensional nA-como-densidade, mesmo padrão do 0.01; I_axial derivado da geometria par a par, fonte única; construtor confirmou por convergência, Rall aposentado; clamp migrado p/ condutância; N≈1 persiste e o residual é a GEOMETRIA pequena, P52 #4)*
*Registro anterior: 2026-09-04 — 112 decisões registradas (D112: escala sináptica calibrada — conversão derivada da geometria corrige o erro de 4 ordens do 0.01; erro de SINAL achado e corrigido (excitação hiperpolarizava); condutância ancorada na conexão neocortical; entrega no dendrito; 1º teste de EFEITO entre modelos; regime de excitabilidade — acoplamento colapsado + Euler instável a dt=0.1 — fica em P52)*
*Registro anterior: 2026-09-04 — 111 decisões registradas (D111: discriminação do teste ativo fechada de verdade — pré pulsa por canal walled, host correlaciona o parceiro pela rede, sem nada injetado; latência é config declarada, não medição; parede STDP/collector intacta; assinatura de advance_connection_test perdeu response_ms; variabilidade emergente pendente em P51)*
*Registro anterior: 2026-09-04 — 110 decisões registradas (D110: ligar o caminho do cabo — emissão no ENGATE A, host possui os cabos e roteia com atraso sináptico; primeira rede real; cluster/inject_network_psc marcados redundantes; circuito da correlação se fecharia mas não foi mexido)*
*Registro anterior: 2026-08-19 — 109 decisões registradas (D109: a admissão em desmame consome as autorizações do nível 1 — bloqueia sem reprovar, libera na conclusão, sem fome; liga a informação que ninguém lia)*
*Registro anterior: 2026-08-19 — 108 decisões registradas (D108: temperatura emergente da computação — fecha a malha rápida do P24; a fuga do calor isento vira teste reprodutível)*
*Registro anterior: 2026-08-19 — 107 decisões registradas (D107: docking — central injeta com info atrasada, aceitação é local com info de agora; reusa slot LIVRE da retração, fechando o ciclo; contrato não cresceu)*
*Registro anterior: 2026-08-19 — 106 decisões registradas (D106: ciclo de vida do slot — host é o motor da retração, limite de tração vem do tecido, slot PERDIDO contabilizado; fecha o laço aberto pelo D104)*
*Registro anterior: 2026-08-19 — 105 decisões registradas (D105: política de escalonamento — três níveis, térmica é o único absoluto, ordem por distância-do-fim; D95 CORRIGIDO — isenção é prioridade máxima, não intocabilidade)*
*Registro histórico anterior: 2026-08-19 — 104 decisões registradas (D99: relógio salta para parede na retomada, pausa como buraco declarado; D100: argumento do agrupamento corrigido — modelo errado, não RAM; habilita as três malhas do P24; D101: HANU_R = host de ~100 modelos, coluna = federação de ~100 HANU_R, classe nova = HanuR; D102: carretel/ioiô — elemento carrega o próprio cabo, defeituoso retrai por tração; D103: recuperação de célula órfã por eliminação numa casca, não por busca; D104: julgamento do silêncio — saturação antes de defeito, régua dos sucessos, viés para esperar). Contrato ElementReport/ElementCommand v0 em CONTRATO_ELEMENTO_V0.md (ElementCommand cresceu order_retraction)*
*Última atualização anterior: 2026-08-16 — 98 decisões registradas (D96–D98: scan estrutural / fork D75 resolvido / variância-idiossincrasia / divisão de trabalho entre rotas)*
*PASSE 2A concluído 2026-08-12. PASSE 2B pendente*
*Fonte: extração sistemática de MIGRACAO_REVESTIMENTO.md + PROBLEMAS_NAO_RESOLVIDOS.md + PESQUISAS_FUTURAS.md + CADEIA_COMPLETA.md* (D61–D62: granularidade/FSM; D63–D67: sistema maduro; D68–D69: topologia em estrela, ligação flexível; D70–D72: duas ondas, feixe/multiplex em aberto, redundância capilar; D73–D75: limpador/assunção/fork FSM; D76: backup via cateter; D77–D81: corpo sintético; D82–D84: fronteira de conversão; D85–D86: substrato computacional e restrição vascular; D87–D90: remoção do material biológico; D91: P46 dissolvido / dianteira mínima; D92–D93: design do P24; D94: estrangulamento por escalonamento/pausa não lentidão; D95: isenção obrigatória do desmame)*  
*PASSE 2A concluído 2026-08-12. PASSE 2B pendente*  
*Fonte: extração sistemática de MIGRACAO_REVESTIMENTO.md + PROBLEMAS_NAO_RESOLVIDOS.md + PESQUISAS_FUTURAS.md + CADEIA_COMPLETA.md* (D61–D62: granularidade/FSM; D63–D67: sistema maduro; D68–D69: topologia em estrela, ligação flexível; D70–D72: duas ondas, feixe/multiplex em aberto, redundância capilar; D73–D75: limpador/assunção/fork FSM; D76: backup via cateter; D77–D81: corpo sintético; D82–D84: fronteira de conversão; D85–D86: substrato computacional e restrição vascular; D87–D90: remoção do material biológico; D91: P46 dissolvido / dianteira mínima ≥ R; D92–D93: design do P24 — controlador/cascata de três malhas)*  
*PASSE 2A concluído 2026-08-12. PASSE 2B pendente*  
*Fonte: extração sistemática de MIGRACAO_REVESTIMENTO.md + PROBLEMAS_NAO_RESOLVIDOS.md + PESQUISAS_FUTURAS.md + CADEIA_COMPLETA.md* (D61–D62: granularidade/FSM; D63–D67: sistema maduro; D68–D69: topologia em estrela, ligação flexível; D70–D72: duas ondas, feixe/multiplex em aberto, redundância capilar; D73–D75: limpador/assunção/fork FSM; D76: backup via cateter; D77–D81: corpo sintético; D82–D84: fronteira de conversão; D85–D86: substrato computacional e restrição vascular; D87–D90: remoção do material biológico; D91: P46 dissolvido / distância mínima de dianteira ≥ R)*  
*PASSE 2A concluído 2026-08-12. PASSE 2B pendente (inclui D87: robôs livres/rastejando descartados)*  
*Fonte: extração sistemática de MIGRACAO_REVESTIMENTO.md + PROBLEMAS_NAO_RESOLVIDOS.md + PESQUISAS_FUTURAS.md + CADEIA_COMPLETA.md* (D61–D62: granularidade/FSM; D63–D67: sistema maduro; D68–D69: topologia em estrela, ligação flexível; D70–D72: duas ondas, feixe/multiplex em aberto, redundância capilar; D73–D75: limpador/assunção/fork FSM; D76: backup via cateter; D77–D81: corpo sintético — cobertura aferente, amortecedor, controladores órfãos, reaproveitamento, sinal anestésico; D82–D84: fronteira de conversão, critério funcional na retina, código de saída; D85: computação no HANU_R / elemento como interface burra; D86: malha em arteríolas e acima, nunca capilares; D87: digestão no local / transporte descartado; D88: escopo campanha = só o neurônio / glia/matriz preservados; D89: varredura final antes da anestesia; D90: gel como substrato estrutural único / acoplamento com frente de remoção)*  
*PASSE 2A concluído 2026-08-12: notas de supersedência em D46 (neuromodulação), D48, D59, D68, D76, D82; D85–D86 adicionados*  
*Fonte: extração sistemática de MIGRACAO_REVESTIMENTO.md + PROBLEMAS_NAO_RESOLVIDOS.md + PESQUISAS_FUTURAS.md + CADEIA_COMPLETA.md* (D61–D62: granularidade/FSM; D63–D67: sistema maduro; D68–D69: topologia em estrela, ligação flexível; D70–D72: duas ondas, feixe/multiplex em aberto, redundância capilar; D73–D75: limpador/assunção/fork FSM; D76: backup via cateter; D77–D81: corpo sintético — cobertura aferente, amortecedor, controladores órfãos, reaproveitamento, sinal anestésico; D82–D84: fronteira de conversão, critério funcional na retina, código de saída; D85: computação no HANU_R / elemento como interface burra; D86: malha em arteríolas e acima, nunca capilares)*  
*PASSE 2A concluído: notas de supersedência em D46 (rádio→D68), D48 (correlação→D68), D59 (papéis HANU_R→D68), D68 (cabo por parceiro→estrela), D76 (backup em elementos→cateter), D82 (converter todos→fronteira bulbo-medular); D85–D86 adicionados*  
*Fonte: extração sistemática de MIGRACAO_REVESTIMENTO.md + PROBLEMAS_NAO_RESOLVIDOS.md + PESQUISAS_FUTURAS.md + CADEIA_COMPLETA.md*

**157. (D132) DOIS GUARDAS GERAIS EM TODA SIMULAÇÃO (decisão do Martel, 2026-10-24 ~09:10) — PROPOSTOS, IMPLEMENTADOS E TESTADOS ANTES DE ATIVAR.**
Pedido: (1) GUARDA FÍSICO — abortar no instante em que uma voltagem passa de um limite de plausibilidade; (2) GUARDA DE TEMPO — abortar a simulação que passa de
um múltiplo do tempo mediano do seu tipo; falha registrada com motivo; a avaliação vira NÃO AVALIADO; a fila segue; o vigia continua, mas a ação não depende de
alguém ler o alerta. **Valores (propostos e adotados):** |V| > **200 mV** (V_PLAUS); **5 ×** a mediana do tipo (K_TEMPO), com piso de **60 s** e só depois de
**5** medidas do tipo (antes disso só o guarda físico); **tempo de CPU do processo**, não de relógio (suspensão da máquina e disputa por núcleo não disparam o
guarda). **Onde:** `stim_common.CommonSim.run` — o caminho ÚNICO de todas as simulações em uso (unidades θ e de direções, condicionamento, funcional G,
referência do Hay). **Como, sem mudar a integração:** advance() do stdrun redefinido como fadvance() + checagem que só LÊ a voltagem dos sítios vigiados
(os estimulados + o soma) e o relógio de CPU depois de cada passo aceito; disparo → stoprun no próprio passo; pós-checagem de TODAS as leituras gravadas
(|V| > 200 mV ou não finito); tipo = (estímulos, tstop, nº de leituras, nº de segmentos do modelo, atol); tempos de CPU acumulados em
`results/guardas/tempos_cpu.log` (uma linha por simulação, gravação atômica por anexação). **Falha → SimulacaoAbortada(motivo):** unidade → subpasso
`nao_avaliado` com o motivo e sem traços parciais; funcional G → `nao_avaliado`; condicionamento → simulação abortada conta como fora do físico (a grade do limiar
para, a amplitude reprova; M1 ou bordas abortados → o ponto não passa). **Testes com resposta conhecida (`etapaA_guardas_teste.py`, compartimento passivo real
pelo CommonSim): 6/6 OK** — G1 fuga +100 nA abortada 0.036 ms depois do início do estímulo (+214 mV); G2 fuga −100 nA abortada (−202 mV); G3 sem o guarda de
passo a PÓS-CHECAGEM pega a fuga (sem guarda nenhum o soma iria a **78 971 mV**); G4 simulação artificialmente lenta (evento que queima CPU a cada 1 ms) abortada
com 0.21 s de CPU contra o limite de teste de 0.2 s (sem guarda: ~2 s); G5 guarda ligado sem disparo × advance() ORIGINAL → **traços IDÊNTICOS bit a bit**;
G6 rodada normal não dispara e registra o tempo. (Três tropeços do PRÓPRIO teste, corrigidos: v_init antes do stdrun; pulso de autoteste do CommonSim forte demais
para o soma pequeno; o gerador de eventos criado depois do repouso salvo e depois com eventos no passado — o NEURON abortou numa asserção do CVode.) **Pendente
de decisão:** o que a ANÁLISE faz com uma avaliação NÃO AVALIADA (θ de uma unidade ou rodada de direções) — hoje a acumulação daquela unidade falharia com o
motivo (sem apagar nada) e o lote ficaria esperando; proposta abaixo no relatório ao Martel. **REGRESSÃO NO MODELO REAL (com os guardas ligados):** subpasso base de g_apic[36]_16 com as amplitudes do piloto condicionado → **M1m, M1p, M4
IDÊNTICOS bit a bit** aos gravados; sem custo visível (protocolos 145 s de relógio; CPU por simulação: M1 40 s, M4 14–34 s). **Análise:** a acumulação de
uma unidade com subpasso NÃO AVALIADO PÁRA com o motivo, sem apagar nada e sem ok.json (`etapaA_apagar_teste.py` caso C; os casos A e B continuam OK). **ATIVADO
(2026-10-24 10:25):** a fila foi PAUSADA (~/.hanu_pausa) durante a implementação para nenhum trabalho novo carregar código pela metade; o condicionamento de
g_apic[70]_48 em curso seguiu com o código anterior (só a opção A); pausa retirada — todo trabalho lançado daqui em diante roda com os dois guardas.


**158. (D132) DECISÃO DO MARTEL SOBRE NÃO AVALIADA NA ANÁLISE DO LOTE (2026-10-24 ~10:40) — a recomendação aprovada, COM AJUSTE; implementado e testado ANTES
de ativar.** (1) Unidade com QUALQUER avaliação NÃO AVALIADA (θ ou rodada de direções): **SAI do conjunto do lote**, registrada com o motivo; a análise usa o
conjunto sem ela. (2) **Mais de uma unidade fora no mesmo lote → a cadeia PARA e reporta** (problema sistemático). (3) **AJUSTE — assimetria da regra de
parada:** um lote desfalcado mostra melhora MENOR que mostraria completo, o que empurraria a regra para parar cedo demais → **lote COMPLETO: a regra age
sozinha, nos dois sentidos; uma unidade fora e a regra diz SEGUIR: segue sozinha; uma unidade fora e a regra diz PARAR: NÃO para — reporta e espera a decisão
do Martel.** **Implementação:** `etapaA_piloto.py` — `--acumular`: NÃO AVALIADO → ok.json com "excluida" e o motivo, nada apagado, nenhum acumulado; `--direcoes`:
unidade com θ NÃO AVALIADO fica fora do Gram (registrada no arquivo de direções); `--acumulados`: pula as unidades fora e registra em "excluidas"; os
conjuntos sem elas. `etapaA_lote_aval.py` — `decisao()`: >1 fora → PARADA_SISTEMATICA; 0 → PARAR/SEGUIR pela regra; 1 → SEGUIR ou ESPERA_DECISAO; grava
`<DECISÃO>.json` (só SEGUIR.json libera o lote seguinte) e o relatório lista as unidades fora. **Testes com resposta conhecida: 12/12** no avaliador (os 6 da
regra + os 6 da decisão: completo PARAR → PARAR; completo SEGUIR → SEGUIR; 1 fora SEGUIR → SEGUIR; 1 fora PARAR → ESPERA_DECISAO; 2 fora → PARADA_SISTEMATICA nos
dois sentidos); **3/3** no apagamento (C: subpasso NÃO AVALIADO → unidade fora, nada apagado); **análise com uma unidade fora = as outras 4 analisadas
diretamente — números IGUAIS** nos 4 modelos de ruído (acumulados do piloto condicionado; ex. OU 50 ms σ* 1.418, σ_lin 0.7719 nos dois), a excluída registrada
com o motivo. Ativo para os trabalhos lançados daqui em diante (o próximo a usar estes scripts é o Gram do lote 1, depois das unidades).


**159. (D132) GUARDA DE TEMPO: FALSO POSITIVO NUM AUTOTESTE — CORRIGIDO; E 4ª SUSPENSÃO → BOOT FRIO (2026-10-24).** **(a) O que houve:** a unidade θ de
g_apic[17]_16 caiu 3 vezes com "GUARDA DE TEMPO: CPU 1223.7 s > limite 1223.7 s" — DENTRO do construtor do CommonSim, na checagem α por epsp × play (um
AUTOTESTE de código, não um protocolo), fora do ponto que converte o aborto em NÃO AVALIADA → o processo caiu e a fila relançou (numa das tentativas passou;
a unidade seguiu). **Causa (erro MEU):** a chave do tipo juntava duas simulações muito diferentes — o α pelo PLAY (CVode parando a cada 5 µs: centenas a ~1 500 s
de CPU) e o α pelo epsp (2–6 s) — a mediana desse "tipo" não significa nada. **Correção:** (1) a chave distingue α por play ('aP') de α por epsp ('a'; as
chaves dos PROTOCOLOS não mudam, o histórico vale); (2) os autotestes do construtor (α epsp × play, início tardio) e o teste de deriva do resettle rodam SEM o
guarda de TEMPO (o FÍSICO continua). **Teste novo (resposta conhecida) G7:** com limite minúsculo semeado, o autoteste NÃO aborta e uma rodada de protocolo do
MESMO tipo aborta → **7/7 OK** (G1–G6 inalterados, inclusive o bit a bit). Fila pausada durante a edição. **Margem medida (protocolos, com disputa e swap):**
M1 (1150 ms, 504 leituras) CPU mín 39 / mediana 108 / máx 228 s (2.1×); M4 (300 ms) 12 / 37 / 99 s (2.7×) → 5× adequado para eles.
**(b) 4ª SUSPENSÃO → BOOT FRIO:** 24/10 18:48:54 "The system will suspend now!" e boot frio 27 s depois (como em 14/10, 16/10 e 22/10). O inibidor estava ativo e
BLOQUEOU as suspensões por inatividade do dia (gsd-power 11:57, 13:36, 13:56, 16:03: "BlockedByInhibitorLock"); a das 18:48 passou por cima dele, sem registro de
tampa ou botão — compatível com suspensão pedida pelo menu ("suspender assim mesmo"). O supervisor retomou sozinho depois do boot (subpassos gravados; perda ≤ 1
subpasso por processo). Nesta máquina, SUSPENDER = REINICIAR (o retorno da suspensão falha).


**161. (D132) RESULTADO DO LOTE 1 (concluído 2026-10-25 20:52; relatório `results/etapaA_lotes/lote1/relatorio.txt`) — LOTE COMPLETO; REGRA DE PARADA: SEGUIR.**
10 distais (5 do piloto + g_apic[70]_48, [77]_48, [37]_32, [19]_16, [17]_16) + somática; Gram acumulado → **25 direções relevantes**; funcional nas 5 além da faixa:
v_1, v_2, v_4, v_5 DENTRO (determinadas pela faixa), **v_3 FORA** (a única que fica na conta). **Nenhuma unidade NÃO AVALIADA**; 50 repousos das direções
calculados antes (0 falhas); as 10 rodadas de direções apagadas unidade a unidade depois dos acumulados conferidos (10 manifestos).
| ruído | σ* lote 1 | σ* ref (6 inj.) | ganho | σ_lin lote 1 | σ_lin ref | ganho | nível |
|---|---|---|---|---|---|---|---|
| iid | 28.27 | 4.628 | +510.8% | 8.555 | 4.717 | +81.4% | [8.55; 28.3] |
| OU 1 ms | 11.60 | 1.663 | +597.8% | 1.929 | 1.366 | +41.3% | [1.93; 11.6] |
| OU 10 ms | 5.731 | 1.179 | +386.2% | 0.590 | 0.717 | **−17.7%** | [0.59; 5.73] |
| OU 50 ms | 6.315 | 1.418 | +345.5% | 0.558 | 0.759 | **−26.5%** | [0.56; 6.32] |
(mV; σ* limitado pelo CaBurst_PA1, pelo BAC_PA2 no iid; σ_lin limitado por v_3.) **Regra declarada (item 151): ganhos < 10% em σ* E σ_lin nos dois ruídos
lentos → PARAR; aqui σ* subiu ~4.5× → SEGUIR (decisão do item 158: lote completo, age sozinha).** **Registrado ao lado (não muda o veredito):** com ruído LENTO
o σ_lin CAIU (0.717 → 0.590; 0.759 → 0.558) — a informação cresceu muito, mas a curvatura ao longo de v_3 piorou; nenhum modelo de ruído fica certificado
(todos são intervalo); o EXTREMO INFERIOR com ruído lento ficou pior que no piloto. **Soma sozinho** (direções do lote 1): σ* 0.346 / 0.344 / 0.344 / 0.345
mV. **Tolerância (item 149):** troca da somática pior 0.44%; distal estimada 0.005% → 10⁻⁸ basta. **Disco:** 65.4 GiB livres. **Arquivo frio dos traços de
direções do piloto condicionado (22.76 GB, 735 arquivos):** o HD não foi conectado nas 12 h de espera (avisos de hora em hora, 25/10 20:58 → 26/10 08:58) →
**APAGADOS SEM ARQUIVO FRIO**, como decidido (manifesto com sha256: `frio_pcond_dirs.txt`). **Porém existe cópia:** a fotografia restic "brutos" 27312e7a do HD
(23/10 21:18) contém esses traços — e a retenção dos "brutos" (as 2 mais recentes) a descartaria depois de DOIS novos backups no HD. **Lote 2** começou
26/10 09:04 (guarda de disco OK; condicionamento dos 5 pontos aprovado 10:30; unidades lançando).


**162. (D132) LOTE 1 — TRÊS ANÁLISES SEM SIMULAR + DECISÕES DO MARTEL (2026-10-26). O lote 2 não foi interrompido.**
**REGISTRADO (Martel):** reportar SEMPRE o **NÍVEL CERTIFICADO = min(σ_lin, σ*)** por modelo de ruído. A queda com ruído lento NÃO pode ser física — medidas a mais
não pioram a estimabilidade (o analista pode ignorá-las); é DEFEITO DO MÉTODO, que obriga a usar todas as linhas. **O nível certificado do EXPERIMENTO é o MÁXIMO
entre os desenhos avaliados**; o do piloto-6 continua valendo. A regra de parada NÃO muda (mandou seguir, o lado seguro), mas a comparação de σ_lin entre lotes
pode ser enganada por essa não-monotonicidade.
**(1) Nível certificado (mV), piloto-6 → lote 1:** iid 4.63 → **8.55**; OU 1 ms 1.37 → **1.93**; OU 10 ms **0.717** → 0.59; OU 50 ms **0.759** → 0.558 → do
EXPERIMENTO: 8.55 / 1.93 (lote 1) e **0.717 / 0.759 (piloto-6)**. (`etapaA_lote1_diag.py`, `lote1/diag_lote1.json`; conferência ANTES: as fórmulas reproduzem
EXATAMENTE piloto_fis.json do lote 1 e do piloto, a partir dos acumulados por unidade.)
**(2a) Decomposição do salto (escala log; "contabilidade" = as MESMAS 6 injeções nas direções e com a faixa do lote 1; "dados novos" = 6 → 11 na mesma
contabilidade):** σ* iid ×6.11 = contab. ×1.38 · dados ×4.41 (18% pela contabilidade); 1 ms ×6.98 = ×2.09 · ×3.33 (38%); **10 ms ×4.86 = ×2.61 · ×1.87 (61%); 50 ms
×4.45 = ×2.34 · ×1.91 (57%)** → com ruído LENTO, **mais da metade do salto do σ* é CONTABILIDADE** (direções diferentes; 4 resolvidas pela faixa contra 1 no
piloto); os dados novos dão ×1.9 (próximo do ~1.4× esperado de 6 → 11 com contribuições parecidas, um pouco acima). σ_lin: a contabilidade REDUZ (×0.49–0.57: no
conjunto de direções do lote 1 as 6 do piloto são mais curvas) e os dados novos AUMENTAM (×1.49–3.21) → **a queda do σ_lin lento (0.717 → 0.59; 0.759 → 0.558) vem
INTEIRA da mudança das direções; os dados novos MELHORARAM o σ_lin** (×1.62 / ×1.49 na mesma contabilidade).
**(2b) A direção que limitava o σ* no piloto** (variância do CaBurst_PA1): 66–91% numa direção ≈ v_4 do piloto (|cos| 1.00 iid; 0.63–0.74 nos outros); no lote 1,
só **18–29% dela** está no subespaço resolvido pela faixa; mais parecida com **v_6 do lote 1** (|cos| 0.50–0.58), **NÃO resolvida**.
**(2c) Autoconsistência — NÃO é ponto fixo:** o raio usa o σ* iid ANTES da regra; depois da regra o σ* sobe e outras direções passam do fator 2 sem terem sido
testadas no funcional. Piloto-6: σ* iid 3.57 → (faixa) 4.63 → novas candidatas **v_5, v_2**; lote 1: 12.3 → 28.3 → nova candidata **v_6**. A remoção das resolvidas
(projetor) não depende da ordem; o que depende do passo é QUAIS são testadas. **Em jogo (otimista, se as novas fossem resolvidas):** lote 1, v_6 → σ* 1 ms 11.6 →
16.9; **10 ms 5.73 → 9.41; 50 ms 6.32 → 9.31** (iid igual); piloto-6, v_5 e v_2 → 10 ms 1.18 → 1.62; 50 ms 1.42 → 1.75. (Muda o σ* — e com ele os ganhos que a regra de
parada compara —, não o nível certificado com ruído lento, que é o σ_lin.)
**(3) Curvatura ao longo de v_3 (a direção que limita o σ_lin no lote 1):** as 5 unidades DO PILOTO carregam **99–100% de Σ‖a‖²** ao longo de v_3; as 5 novas,
~0%. Tirando cada nova: σ_lin INALTERADO para g_apic[70]_48, [77]_48, [19]_16, [17]_16 (**g_apic[70]_48, a do M4 por frações do teto, não traz a curvatura** —
nem informação: σ* igual sem ela); **sem g_apic[37]_32 o σ_lin CAI** (iid 8.55 → 2.80; 1 ms 1.93 → 0.705; 10 ms 0.59 → 0.386; 50 ms 0.558 → 0.422) **e o σ* também**
(28.3 → 6.41; 11.6 → 3.49; 5.73 → 3.08; 6.32 → 3.32) — ela não traz aceleração, traz VELOCIDADE (‖J v_3‖), que reduz a curvatura RELATIVA. **Por protocolo: NÃO
AVALIÁVEL sem simular** — os traços das rodadas de direções foram apagados depois de acumulados (o acumulado soma M1m, M1p e M4); reabrir exige rodar de novo
v_3 ± nas 5 unidades do piloto (10 subpassos, ~1.3 h de CPU) — proposto, não rodado.
**DECISÕES DO MARTEL, EXECUTADAS:** (1) **foto "brutos" de 23/10 marcada FRIA** — e ACHADO: o HD estava conectado (10:37) e o backup automático já estava no passo
dos brutos; a linha seguinte (retenção "as 2 mais recentes") DESCARTARIA a foto de 23/10 (já havia 2) — **o serviço foi PARADO a tempo** (o restic soltou a
trava; nenhuma limpeza rodou); foto marcada "frio" (novo id **b135a90e**; conteúdo igual — contém os 735 traços de direções do piloto condicionado, apagados
sem arquivo frio em 26/10, e os de dirsrel64/dirs64/migr64); **script corrigido**: a limpeza dos brutos mantém SEMPRE as fotos "frio" (`--keep-tag frio`) —
testado ANTES num repositório descartável (a "frio" sobrevive com o conteúdo + as 2 mais recentes: OK); backup do HD refeito: brutos **e404dbb9** (+26.4 GiB, 13.6
GiB gravados), retenção manteve b135a90e + as 2 mais recentes, check sem erros. (2) **Arquivo frio do migr64_1e-6/1e-10** feito NESTA conexão: 366 arquivos, 11.33
GB, CADA cópia conferida por sha256 lida de volta do HD, depois apagados (o trabalho lt_frio_migr64 da fila ficou FEITO). (3) **dirsrel64_1e-8 e dirs64_1e-8
APAGADOS** (só .npy; 216 arquivos, 6.69 GB; manifesto `limpeza/apagados_2026-10-26.txt`) DEPOIS da foto marcada (cópias em b135a90e e e404dbb9). Disco: ~98 GiB
livres → o lote 3 deixa de esbarrar na guarda de disco. **Leitura SMART (o Martel, 26/10, depois das gravações):** atributos **5 / 197 / 198 = 0 / 0 / 0**;
último teste longo "Completed without error" → **pela regra declarada, o HD continua APROVADO.** **A acompanhar:** Multi_Zone_Error_Rate (atributo 200, erros
de ESCRITA) **40 → 68** durante as gravações de hoje (~38 GB; VALUE 100, sem limite); os dados gravados estão conferidos (arquivo frio: sha256 relido do HD, cada
arquivo; restic check sem erros). Proposta: ler os atributos a CADA conexão; se o 200 continuar subindo em duas conexões seguidas, ou 5/197/198 > 0 →
recomendar troca. Temperatura 43 °C (máx. 46); 37 h de uso.


**163. (D132) DECISÃO DO MARTEL (2026-10-26 ~12:30) — FECHAR O PONTO FIXO EM TODOS OS DESENHOS + CURVATURA POR PROTOCOLO. O lote 2 não é interrompido.**
**REGISTRADO:** (i) **quase-perda da foto de 23/10:** o backup automático ao conectar roda ANTES de qualquer marcação manual — a instrução "marcar na próxima
conexão" tinha essa brecha; corrigido no CÓDIGO (a limpeza nunca descarta foto "frio"). (ii) A queda do σ_lin com ruído lento veio TODA da mudança de direções;
com a mesma contabilidade, os dados novos aumentam o σ_lin de 1.5× a 3.2×. (iii) **PRINCÍPIO (sem mudar a ordem dos lotes agora):** g_apic[37]_32 reduz a
curvatura RELATIVA de v_3 trazendo VELOCIDADE (informação) ao longo dela — **a curvatura relativa cai com informação ao longo da direção curva → candidato a
critério de escolha de pontos de injeção (informação nas direções curvas, além da distância).**
**(2) PONTO FIXO EM TODOS OS DESENHOS:** o conjunto de direções resolvidas pela faixa não é ponto fixo nem no lote 1 nem no piloto → os dois resultados estão
INCOMPLETOS, e a comparação entre eles também. Rodar o funcional ao longo de v_6 do lote 1 E de v_5, v_2 do piloto; ITERAR até nenhuma direção não testada passar
do fator 2 no σ* resultante (monótono: remover direções só aumenta o σ*; termina); recalcular σ*, σ_lin e o nível certificado do piloto-6 e do lote 1 no PONTO
FIXO. **DECLARADO AGORA, antes de o lote 2 terminar: a avaliação da regra de parada depois do lote 2 usa σ* e σ_lin NO PONTO FIXO, para TODOS os desenhos
comparados** — não é mudança da regra, é calcular corretamente as grandezas que ela usa. **O passo de iteração entra na cadeia dos lotes seguintes.** Custo
estimado (abaixo do limite de ~12 h que exigiria consulta): piloto v_5, v_2 → 4 avaliações do funcional (~6.7 h de CPU); lote 1 v_6 → 2 (~3.4 h); rodadas extras
não previstas pela cadeia otimista do item 162 (se surgirem, reportadas). A avaliação do funcional em θ_verd (base) é REAPROVEITADA da rodada de cada desenho.
**(3) CURVATURA EM v_3 POR PROTOCOLO: APROVADA** — v_3 ± nas 5 unidades do piloto (~1.3 h), separando M1m, M1p e M4 (repousos em cache da rodada do lote 1).
**Implementação declarada:** a curvatura INTRÍNSECA ‖a_N‖², com a_N = a − J c e c = G⁻¹ Jᵀa do Gram COMBINADO do lote 1, é SOMA por linhas → decomposição EXATA
por unidade e por protocolo: E = Σaᵀa − 2 cᵀ Σ Jᵀa + cᵀ (Σ JᵀJ) c em cada parte. Por unidade (as 10) sai dos acumulados (sem simular); por protocolo, dos
acumulados POR PROTOCOLO das 5 refeitas. Conferência: a soma por protocolo reproduz o acumulado da unidade (tolerância de arredondamento).
**Implementado e testado ANTES do uso (26/10 ~13:00):** `etapaA_ponto_fixo.py` (passo r: candidatas = NÃO testadas com raio·max|v| > ln 2 no σ* iid RESULTANTE
da análise anterior; sem candidatas → `PONTO_FIXO.json` = a análise + registro + certificado; guardas: teto de avaliações → ESPERA_DECISAO_CUSTO; r > r_max = 3
→ NAO_ALCANCADO); `etapaA_piloto.py` ganhou `--fdir a,b,…` (junção; direção em dois Fdir → recusa) e `--acumular … --por-protocolo`; `etapaA_curv_protocolo.py`.
**Testes (`etapaA_ponto_fixo_teste.py`, 13/13 OK):** P1–P7 passo sintético (candidatas, δ, base copiada, teto, rodada 2, NÃO ALCANÇADO, PONTO FIXO com
certificado, duas recusas); P8 monotonia (500 casos: tirar direções nunca aumenta a variância; maior "aumento" −6.4e−6); **A1** análise do lote 1 com o código
modificado → `piloto_fis.json` IDÊNTICO; **A2** `--fdir Fdir.json,<v_6 DENTRO>` → o σ* otimista do item 162 (código independente), diferença 0.0; **C1** unidade
sintética com aceleração só no M4 → Jᵀa, aᵀa do M1 = 0 exatos, M4 = total, Σ protocolos = total. `etapaA_curv_protocolo.py`: (0) identidade da decomposição
(200 casos, pior 6.7e−16, E_p ≥ 0) e (1) σ_lin(v_3) das 10 = item 162 EXATO (lição: o `sum()` do Python ≥ 3.12 COMPENSA somas de float → ~1e−11 de diferença;
somar como no código oficial). **Ensaio a seco do passo 1 nos dados reais:** piloto → [v_5, v_2] (δ 1.026, 1.392; σ* iid 4.628), lote 1 → [v_6] (δ 1.047;
σ* iid 28.27) — as MESMAS do item 162; a base do funcional do piloto e a do lote 1 são idênticas bit a bit (reaproveitamento seguro).
**Fila (`results/etapaA_lotes/cadeia_pf.py`, 101 trabalhos):** piloto-6 (teto 4 avaliações) e lote 1 (teto 2) — juntos ~10 h de CPU; QUALQUER rodada extra
passaria de ~12 h → para e espera a decisão; curvatura (`c3_*`: repousos da cache → vrest → v_3 ± nas 5 → acumulados por protocolo → análise; traços MANTIDOS
até o relatório, ~1.3 GB). Esses entram ANTES de `lt2_dirs` (prioridade sobre as PRÓXIMAS etapas do lote 2, atraso estimado ~3–4 h; nada interrompido).
**Lotes 2 e 3:** iteração do ponto fixo depois da análise (teto 7 avaliações ≈ 11.7 h cada) e `lt2_aval`/`lt3_aval` comparam `lote<b>/pf/PONTO_FIXO.json` com
`lote<b−1>/pf/PONTO_FIXO.json` (conjunto "acum"). Rodadas não usadas ficam em ESPERA (não seguram a fila nem o inibidor).


**164. (D132) RESULTADO DO ITEM 163 (2026-10-26, cadeia concluída 23:56) — PONTO FIXO NOS DOIS DESENHOS SEM NENHUMA DIREÇÃO NOVA RESOLVIDA; A CURVATURA
EM v_3 NASCE NO M4 DE g_apic[36]_16 E g_apic[60]_32.** O lote 2 não foi interrompido.
**(2) Ponto fixo.** Funcional ao longo das candidatas (δ = ln 2/max|v|; base reaproveitada): **piloto v_5 FORA** (CaBurst_PA1 ΔF/tol = 1.25 no extremo +; o −
dentro, pior 0.40), **v_2 FORA** (CaBurst_PA1 8.03 no +; − dentro, pior 0.43); **lote 1 v_6 FORA** (contagem do CaBurst 1 → 0 no +, 1 → 2 no −). Nenhuma
resolvida → o σ* resultante não muda → passo 2 sem candidatas → **PONTO FIXO na rodada 2 nos dois desenhos** (`etapaA_pcond/pf/PONTO_FIXO.json`,
`lote1/pf/PONTO_FIXO.json`). Os valores são os dos itens 161/162, agora no ponto fixo (mV; σ* / σ_lin / certificado):

| ruído | piloto-6 | lote 1 |
|---|---|---|
| iid | 4.628 / 4.717 / **4.628** | 28.27 / 8.555 / **8.555** |
| OU 1 ms | 1.663 / 1.366 / **1.366** | 11.60 / 1.929 / **1.929** |
| OU 10 ms | 1.179 / 0.717 / **0.717** | 5.731 / 0.590 / **0.590** |
| OU 50 ms | 1.418 / 0.759 / **0.759** | 6.315 / 0.558 / **0.558** |

Limitante do σ*: CaBurst_PA1 (iid do lote 1: BAC_PA2); σ_lin limitado por v_3 (iid do piloto: v_2). **Nível certificado do EXPERIMENTO (máximo entre os
desenhos): iid 8.555 e 1 ms 1.929 (lote 1); 10 ms 0.717 e 50 ms 0.759 (piloto-6)** — inalterado. O ganho otimista do item 162 (2c') NÃO se realiza: o
CaBurst_PA1 impede resolver mais direções pela faixa. A referência da parada do lote 2 no ponto fixo = os valores do lote 1 já reportados.
**Custo real:** 6 avaliações do funcional, 4652–7688 s cada (piloto 8.25 h, lote 1 3.04 h; 11.3 h de relógio somado, com 5+ processos em 4 núcleos) — acima da
estimativa de ~10 h, abaixo de 12 h. Curvatura: 3.8 h somadas (as 5 bases 1425–2353 s; as direções 189–516 s).
**(3) Curvatura em v_3 por protocolo** (`lote1/curv_v3/curv_protocolo.json`). **Conferências:** (0) identidade sintética 6.7e−16; (1) σ_lin(v_3) das 10 = item
162 EXATO; (2) Σ protocolos = total (≤ 1.1e−15); (3) a rodada refeita REPRODUZ os acumulados do lote 1 ao longo de v_3 (≤ 1e−15) — com e sem a faixa os
resultados coincidem (nenhuma linha dessas unidades fora da faixa): a ressalva da máscara não se materializou. Σ E_p/‖a_N‖² = 1 ± 1.2e−4 (cancelamento:
‖a‖² ≫ ‖a_N‖²) → partes com resolução de ~0.1%.
- **Aceleração BRUTA (Σ‖a‖²): o M4 do g_apic[36]_16 tem 98.5% (iid) a 100% (lentos)**; M1m e M1p ≈ 0 em todas.
- **Mas ela é quase toda TANGENTE** (absorvida por uma mudança de parâmetros). A parte INTRÍNSECA ‖a_N‖² mora no g_apic[37]_32 (56–69%; sem aceleração própria
  — é onde a explicação tangente não fecha) e no **M4 do g_apic[60]_32 (20–36%)**; M4 do g36 0.5–3.6%. Por protocolo (as 5 do piloto): **M4 27–38%**, M1p
  1.0–2.7%, M1m 0.8–2.1%. Por unidade do piloto: g60 21–38%, g36 2.2–4.4%, g44 0.8–2.2%, g64 1.2–1.6%, g9 0.1%.
- **Teste direto — σ_lin(v_3) TIRANDO a parte** (iid / 1 / 10 / 50 ms; todas: 8.555 / 1.929 / 0.590 / 0.558): sem o M4 do g60 → 10.34 / 2.324 / 0.636 / 0.576
  (SOBE: traz curvatura); sem o M4 do g36 → 10.85 / 2.345 / 0.576 / 0.621 (sobe, exceto em 10 ms, onde ele traz 16% da velocidade); **sem o g37 → 2.80 / 0.705 /
  0.386 / 0.422 (CAI: traz 66–81% da VELOCIDADE ao longo de v_3)**; sem qualquer M1 (m ou p) de qualquer unidade: ≤ 1.5%; sem o g77: até −5% (50 ms).
**Conclusão:** a curvatura ao longo de v_3 nasce no protocolo M4 (perto do limiar, supralinear) do g_apic[36]_16 e do g_apic[60]_32; os M1 não contam; a
velocidade do g_apic[37]_32 é o que a reduz — confirma o princípio do item 163 (iii) (curvatura relativa cai com informação ao longo da direção curva).
Traços da rodada refeita (`curv_v3/dirs_*`, 1.3 GB) MANTIDOS — remoção aguarda o aval do Martel. **Lote 2:** as unidades θ terminaram 19:12–19:42; os
trabalhos do item 163 tiveram prioridade e `lt2_dirs` entra ~00:00 (atraso ~4.3 h; nada interrompido). Rodadas não usadas do ponto fixo (piloto/lote 1)
ficam em ESPERA na fila. Relatório: `docs/canal/relatorios/R0002-ponto-fixo-curvatura.md`.


**165. (D132) PROMPT 0001 DO CANAL — O QUE TORNA v_3 RELEVANTE + A ESPECIFICAÇÃO SEM O CaBurst_PA1 (executado 2026-10-27 por ordem do Martel, D135). Sem
simular; o lote 2 não foi interrompido.** **Decisão listada no prompt** (remover os traços da rodada refeita em v_3): **APROVADA pelo Martel e feita** — 45
arquivos .npy, 1.393 GB (`results/limpeza/apagados_2026-10-27.txt`); os acumulados por protocolo ficam.
**(1) REGISTRADO:** (i) ponto fixo fechado nos dois desenhos sem direção nova resolvida; v_2, v_5 (piloto) e v_6 (lote 1) saem da tolerância SÓ pelo
CaBurst_PA1; os números dos itens 161/162/164 ficam valendo. Conferido agora: TODAS as direções FORA dos dois desenhos (também v_3, v_4 do piloto e v_3 do lote
1) caem SÓ pelo CaBurst_PA1. (ii) **ACHADO (sem mudar critério):** a CONTAGEM de PA do CaBurst muda DENTRO da faixa fisiológica (fator 2) — v_6 do lote 1
(1 → 0 no +, 1 → 2 no −), v_3 do piloto (1 → 0 no −), v_4 do piloto (1 → 0 no +): o protocolo CaBurst está perto de uma fronteira de regime também no ESPAÇO DE
PARÂMETROS, não só na amplitude (o item 143 testou a contagem em ±2% de amplitude em θ_verd — estável — e, ao longo de v_4 do piloto ANTIGO, só os limiares:
1º PA +2.5% / −0.5%, contagem 1 mantida em 1.5 nA). **A propriedade que limita a especificação muda de regime dentro da variabilidade natural entre células.**
(iii) Curvatura em v_3 (item 164): parte intrínseca do g_apic[37]_32 (que traz 66–81% da velocidade) e do M4 do g_apic[60]_32; M1 irrelevantes — confirma o
princípio do item 163.
**(2) O QUE TORNA v_3 RELEVANTE** (`etapaA_relevancia_caburst.py`, `results/etapaA_lotes/prompt0001/`). **Conferências:** R0 a seleção refeita dos acumulados
(iid, sem faixa) reproduz o conjunto gravado — mesmos índices na mesma ordem, |Δs/s| = 0, 1 − |cos| ≤ 2e−15; R1 σ*, σ_lin = PONTO_FIXO.json EXATOS.
- **lote 1, v_3** (2ª na ordem gulosa; maior f = 0.550, no BAC_PA2): 38 componentes PRECISAM dela (sem ela, < 99%), entre elas o BAC_PA2 (sem ela 0.45) — o
  CaBurst_PA1 NÃO (f 0.002). Maior 1.645·σ_g/tol em σ_lin entre as que precisam: iid BAC_PA2 0.303; 1 ms BAC_PA2 0.120; **10 ms EPSP_apical_ponta 0.058 (BAC_PA2
  0.043); 50 ms EPSP_apical_ponta 0.060 (BAC_PA2 0.039)**. Contribuição absoluta de v_3 no BAC_PA2 (σ²c/(tol/1.645)²; iid/1/10/50 ms): em σ* 0.90 / 0.43 / 0.135 /
  0.152; em σ_lin 0.083 / 0.012 / 1.4e−3 / 1.2e−3. σ_lin sem v_3: 15.21 / 6.83 / 6.99 / 4.49 (passa a v_6).
- **piloto-6, v_3** (limita o σ_lin com 1/10/50 ms; 9ª na ordem): o **CaBurst_PA1 PRECISA dela** (f 0.085; sem ela 0.912), com razão em σ_lin 0.82 / 0.61 / 0.54;
  **v_2** (limita no iid): o CaBurst também precisa (f 0.008; sem ela 0.989, na beira dos 99%). σ_lin sem v_3: 4.72 / 2.21 / 2.93 / 2.19.
- **LEITURA DECLARADA, aplicada:** piloto-6 → **REFUTADA** (v_3 e v_2 entram pelo CaBurst_PA1, em todos os ruídos); lote 1 iid e 1 ms → **REFUTADA** (BAC_PA2 a
  30% / 12% da tolerância em σ_lin); **lote 1 10 e 50 ms → v_3 entra SÓ por componentes FOLGADAS (≤ 6% em σ_lin): o nível certificado do lote 1 com ruído
  lento está fixado por uma direção que não ameaça a especificação → PROPOSTA abaixo.**
- **PROPOSTA P-abs (NÃO ADOTADA — para o Martel decidir antes da análise do lote 2;** `etapaA_relev_abs.py`): dentro do conjunto relevante de hoje (cobertura
  relativa), menos as resolvidas, a direção v_i só CONTA no ruído σ se mover alguma componente em ≥ ε = 10% da tolerância: 1.645·σ·|g·v_i|·√(v_iᵀB(BᵀG_τB)⁻¹Bᵀv_i)
  ≥ ε·tol_g → entrada σ_i; nível AUTOCONSISTENTE σ_c = max{σ ≤ σ* : σ ≤ σ_lin,i para toda v_i que conta em σ} = min(σ*, min_i max(σ_lin,i, σ_i)). **Controles
  (7/7 OK):** K1 forma fechada = definição por varredura (300 casos, ≤ resolução); K2 direção curva que só move componente folgada → não limita; K3 curva na
  limitante → limita; K4 ε = 0 → a regra de hoje, EXATA nos dois desenhos; K5 σ_c não decresce com ε (sintético e real); K6 invariância de unidades.
  **Diagnóstico (ε = 0.10):** só muda o lote 1 com ruído lento — **10 ms 0.590 → 1.559 (×2.64), 50 ms 0.558 → 1.621 (×2.91)** (v_3 passa a contar em 1.56 /
  1.62 mV); o piloto-6 e os ruídos rápidos não mudam; o nível do EXPERIMENTO com ruído lento passaria de 0.717 / 0.759 (piloto-6) a 1.56 / 1.62 (lote 1).
  **PREMISSA NÃO TESTADA:** que a curvatura intrínseca ao longo de uma direção só prejudica o funcional pelo movimento ao longo dela (o critério de Bates &
  Watts protege a região de confiança INTEIRA). **Controle K7 proposto antes de adotar:** modelo sintético NÃO LINEAR de resposta conhecida (uma direção muito
  curva que não move o funcional + uma reta que move), Monte Carlo do ajuste por mínimos quadrados com σ entre o nível de hoje e o do P-abs: a componente fica
  dentro da tolerância em ≥ 95% dos ajustes? Sem NEURON, minutos.
**(3) SENSIBILIDADE SEM O CaBurst_PA1** (rótulo; o critério D131 7.4 NÃO muda): sem ele (e sem a contagem dele no Fdir), TODAS as direções testadas ficam
DENTRO (piloto v_1–v_5; lote 1 v_1–v_6) — v_3 passa a resolvida pela faixa. O conjunto relevante recalculado é subconjunto do gravado (piloto 24 de 24; lote 1
24 de 25, sai v_20) e dá os mesmos números. **NÃO é ponto fixo:** com o σ* maior, 6 direções NOVAS passam do fator 2 em cada desenho (piloto v_6–v_10, v_13;
lote 1 v_7–v_11, v_13) → 12 avaliações do funcional por desenho (~23 h de CPU cada, ~46 h no total) — **PARADO, custo reportado, aguarda decisão.** Valores
com as resolvidas de agora = LIMITES INFERIORES dos do ponto fixo (resolver mais só sobe σ* e σ_lin), mV, σ* (limitante) / σ_lin / certificado (× o de hoje):

| ruído | piloto-6 | lote 1 |
|---|---|---|
| iid | 62.73 (EPSP_apical_ponta) / 73.17 / **≥ 62.73 (×13.6)** | 71.99 (EPSP_apical_ponta) / 46.4 / **≥ 46.4 (×5.4)** |
| OU 1 ms | 19.38 / 61.66 / **≥ 19.38 (×14.2)** | 22.66 / 15.5 / **≥ 15.5 (×8.0)** |
| OU 10 ms | 9.678 / 15.34 / **≥ 9.68 (×13.5)** | 10.68 / 12.88 / **≥ 10.68 (×18.1)** |
| OU 50 ms | 9.251 / 6.654 / **≥ 6.65 (×8.8)** | 9.907 / 8.324 / **≥ 8.32 (×14.9)** |

O σ* passa a ser limitado pelo **EPSP_apical_ponta** em todos os ruídos. **Para o preprint:** a especificação certificada depende de UMA propriedade (a latência
do 1º PA do CaBurst, 1 ms de tolerância) por um fator ≥ 5–18 — e é ela que muda de regime dentro da faixa fisiológica. Relatório:
`docs/canal/relatorios/0001-relevancia-v3-e-caburst.md`.


**166. (D132) PROMPT 0002 DO CANAL — TESTAR O P-abs ANTES DE ADOTAR; SENSIBILIDADE SEM O CaBurst FICA COMO LIMITE INFERIOR (2026-10-27, por ordem do Martel).**
**Decisões listadas no prompt, APROVADAS pelo Martel:** (1) a sensibilidade sem o CaBurst_PA1 NÃO tem o ponto fixo fechado (~46 h) — os valores ficam como
LIMITES INFERIORES (≥ 5–18×); (2) o P-abs NÃO é adotado por enquanto: testes abaixo; a análise do lote 2 usa a regra ATUAL, com o P-abs ao lado como
"candidato, termos cruzados não medidos".
**(1) REGISTRADO:** a especificação certificada depende de UMA propriedade — a latência do 1º PA do CaBurst (tolerância 1 ms, D131 7.4) — por um fator ≥ 5–18;
é a mesma propriedade cuja contagem muda de regime dentro da faixa fisiológica (v_6 do lote 1; v_3 e v_4 do piloto). **Para o preprint:** apresentar a
especificação como FUNÇÃO da tolerância do CaBurst_PA1 (pontos 0.2 / 0.5 / 1.0 ms do item 139 e o limite inferior "sem CaBurst"), não como um número só.
Correção aceita: o item 143 já tinha medido os limiares ao longo de v_4; a novidade é a mudança de CONTAGEM.
**(2) LITERATURA** (conferida antes de comparar): **Cook & Goldberg (1986, Ann. Statist. 14:1399–1418)** — lido na fonte PRIMÁRIA disponível, o relatório
técnico nº 448 (Univ. Minnesota, março 1985) que o precede (o texto publicado pode diferir no detalhe): as curvaturas para um SUBCONJUNTO θ₂ de parâmetros
(Γ_s^T, Γ_s^n, Γ_s) estendem Bates & Watts; **a forma final SUPÕE a curvatura intrínseca do modelo inteiro DESPREZÍVEL** ("The final form of (14) is based on
the assumption that the intrinsic curvature of F at θ̂ is negligible"); a "intrínseca do subconjunto" vem SÓ dos termos MISTOS entre parâmetros de interesse e
de incômodo (fanning e torção do arranjo A₁₂ — "depends only on fanning and torsion components of A") — ou seja, para um subconjunto o que importa são
justamente as derivadas segundas MISTAS (a preocupação do prompt); só subconjuntos de coordenadas (função dos parâmetros exige reparametrizar); guia
c = F_α(p₂, n−p)^{−1/2}, "curvatures must be substantially less than c". **Não resolve o nosso caso** (a curvatura intrínseca ao longo de v_3 é GRANDE — é
ela que limita o σ_lin). **Clarke (1987, JASA 82:844–850)** — fonte primária INACESSÍVEL daqui (Taylor & Francis, 403); só o RESUMO: estimação por
intervalo de parâmetros INDIVIDUAIS em relação à curvatura do lugar das soluções; critérios para curvatura "severa"; fórmula de correção para curvatura
moderada. **NÃO conferido** como a intrínseca entra nas curvaturas marginais — não usado.
**(3) DESENHO DOS TESTES, DECLARADO ANTES DE RODAR** (`etapaA_k7k8.py`; Monte Carlo de mínimos quadrados NÃO LINEAR, 2000 ajustes por nível, sementes fixas;
ajuste local a partir da verdade — mede o efeito estatístico da curvatura, não o otimizador; ajuste que não converge conta como FORA). **Critério do prompt,
SEM alteração:** no nível que o P-abs certifica, CADA componente dentro da tolerância em ≥ 95% dos ajustes e |viés médio| ≤ 10% da tolerância. **Decisão do
Martel (pergunta feita antes de rodar):** como 1.645 = 90% bilateral (item 26), no nível σ* até o modelo LINEAR dá 90% → o K7 é desenhado com u movendo uma
componente FOLGADA (como v_3 no lote 1), e o P-abs certifica ~0.5σ*, onde 95% é alcançável; o caso literal (u não move nada → nível = σ*) sai só como
informação, ao lado do modelo linear.
- **K7 (sintético, iid):** n = 200, θ = (θ_u, θ_w), verdade 0; f(θ) = s_u θ_u b_u + s_w θ_w b_w + ½κ_u θ_u² e_N + κ_x θ_u θ_w e_X (b_u, b_w, e_N ortonormais;
  e_N e e_X NORMAIS ao plano tangente → curvatura INTRÍNSECA). s_u = 0.2, s_w = 1; componentes g_w = θ_w (tol 1.645 → σ*_w = 1 = σ*, LIMITANTE) e g_u = θ_u
  (tol 41.1 → σ*_u = 5, FOLGADA). κ_u tal que σ_lin,u = 0.1 (Bates & Watts com p = 2, F₀.₉₅(2, 198) = 3.04) → a regra de hoje certifica 0.1; o P-abs (as MESMAS
  funções de `etapaA_relev_abs`) certifica σ_c = max(σ_lin,u, entrada_u = 0.1·σ*_u) = 0.5. **K7a:** κ_x = 0, em σ = 0.5 (decide; informativos 0.1 e 1.0).
  **K7b:** X = K^N_uw/K^N_uu (curvaturas normalizadas: K_uw = κ_x/(s_u s_w), K_uu = κ_u/s_u²), grade 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10 e bisseção
  entre o último que passa e o primeiro que falha; e_X = e_N (principal) e e_X ⟂ e_N (informativo); controle: X = 0 reproduz o K7a (mesmas sementes, idêntico).
  Controle LINEAR (κ = 0): cobertura = a gaussiana analítica (|Δ| ≤ 4 erros-padrão).
- **K8 (dados reais do lote 1):** superfície quadrática y(θ) = y0 + Jδθ + ½Σ_i a_i(v_iᵀδθ)² nas coordenadas branqueadas do Gram que dá o σ* (iid e OU 10 ms);
  parte tangente de a_i pelo Jᵀa medido (R⁻ᵀJA_i, R = Cholesky do Gram), parte normal pela norma ‖a_N,i‖² = aᵀa − ‖R⁻ᵀJA_i‖²; as resolvidas pela faixa
  (v_1, v_2, v_4, v_5) fixas na verdade; 26 parâmetros livres; funcional linear (G a 10⁻⁸, as 53 componentes). Variantes: **K8-v3** (só a aceleração de v_3 —
  EXATA, sem premissa) e **K8-todas** (as 21 direções livres; PREMISSA: as partes normais de direções diferentes ORTOGONAIS entre si — os produtos a_iᵀa_j não
  foram gravados); controle **K8-lin** (sem aceleração: cobertura = gaussiana analítica por componente). Premissas comuns: sem termos cruzados (não medidos);
  aceleração da somática não medida (0). Níveis: iid 8.555 (hoje = P-abs); OU 10 ms 0.590 (hoje) e 1.559 (P-abs, decide).
- **Regra de adoção (do prompt):** K7a ou K8 falha → NÃO adotar; os dois passam → reportar o X do K7b e o CUSTO de medir as derivadas mistas reais (v_3 ×
  as direções que mais movem BAC_PA2, CaBurst_PA1, EPSP_apical_ponta, nas unidades g_apic[37]_32 e g_apic[60]_32), SEM lançar. Até lá o P-abs fica fora da
  regra de parada do lote 2.
**RESULTADO (166, `results/etapaA_lotes/prompt0002/k7k8.json`, 2000 ajustes por nível):** **controles OK** (K7 e K8 lineares = gaussiana analítica; K7b com
X = 0 idêntico ao K7a). **K7a PASSA** — no nível do P-abs (0.5σ*), cobertura 0.999 / 1.000 (limitante / folgada), viés 0.08% / 0.17% da tolerância; em σ* (info)
0.9075 = a do modelo LINEAR (os 90% da definição). **K7b: NENHUMA falha na grade declarada até X = 10** (K^N_uw/K^N_uu), com e_X = e_N (cobertura ≥ 0.9975, viés
≤ 0.35%) e com e_X ⟂ e_N (cobertura 1.000, viés ≤ 1.5%) → X > 10 (fim da grade; o termo cruzado INTRÍNSECO acrescenta uma dimensão que também informa sobre w).
**K8 FALHA:** no **iid, σ = 8.555 (aqui hoje = P-abs)**, a cobertura passa (pior: CaBurst_PA1 0.997 só com v_3; 0.9935 com todas), mas o **VIÉS do CaBurst_PA1 é
−12.7% (K8-v3, EXATO) e −14.7% (K8-todas) da tolerância > 10%**; no **OU 10 ms, σ = 1.559 (P-abs) PASSA** (cobertura 1.000, viés ≤ 2.4%; no nível de hoje, 0.590,
≤ 0.4%). **PELA REGRA DECLARADA: K8 falha → o P-abs NÃO é adotado.** Os termos cruzados reais não precisam ser medidos agora (a regra só pede o custo se K7a E K8
passarem); direções candidatas, só para registro: v_3 × {v_6, v_20 (CaBurst_PA1); v_18, v_23 (EPSP_apical_ponta); v_8, v_12 (BAC_PA2)}.
**ACHADO (não muda critério; para o Martel):** a falha do K8 está num nível em que o P-abs e a REGRA ATUAL COINCIDEM (iid 8.555 — o σ_lin de v_3) → a regra
atual também não passaria neste critério. A causa é a curvatura de PARÂMETRO (parte TANGENTE da aceleração ao longo de v_3 — 98–100% dela, item 164): o ajuste
de mínimos quadrados fica enviesado ~ −½σ²(g·c)(vᵀG⁻¹v) (viés de Box), que cresce com σ² e passa de 10% da tolerância do CaBurst_PA1 acima de σ ≈ 7.6 mV (iid, escala σ² a partir de 12.7% em 8.555);
o critério de Bates & Watts (curvatura INTRÍNSECA, o σ_lin) não vê esse viés, e o critério da especificação (item 26: |viés da redução| + 1.645σ_F ≤ tol) não
inclui o viés do ESTIMADOR. Com ruído lento (os níveis que decidem a parada) o viés é pequeno (≤ 2.4% em 1.559 mV, OU 10 ms). Pendente para o relatório do lote
2: o P-abs sai AO LADO como "candidato — NÃO adotado (K8 falhou); termos cruzados não medidos". Relatório: `docs/canal/relatorios/0002-teste-p-abs-e-sensibilidade.md`.


**167. (D132) PROMPT 0003 DO CANAL — O VIÉS DE SEGUNDA ORDEM, CALCULADO COMPLETO ANTES DE DECIDIR (2026-10-27, por ordem do Martel; prioridade baixa; sem
simular; o lote 2 não foi interrompido).**
**Decisão listada no prompt — APROVADA pelo Martel: NÍVEL DE CONFIANÇA DO σ*.** O critério |viés| + 1.645·σ_F ≤ tol (item 26) garante que a estimativa fica
dentro de ±tol em ~**90%** das vezes (bilateral), não 95% — o K7 confirmou (0.9075 em σ*). **Mantém-se o 1.645 e escreve-se "90%" em todo lugar (preprint
incluso)**, em vez de trocar por 1.96 (que reduziria todos os σ* por ×0.84).
**(1) REGISTRADO:** P-abs NÃO adotado pela regra declarada (K8 falhou); K7a passou; K7b sem falha até X = 10 no modelo sintético. **Achado do K8:** o viés de
segunda ordem do estimador (Box), vindo da curvatura de PARÂMETRO ao longo de v_3, não é visto pelo critério de Bates & Watts nem pela especificação atual;
no iid passa de 10% da tolerância do CaBurst_PA1 acima de σ ≈ 7.6 mV; com ruído lento é ≤ 2.4% — a regra de parada não é afetada.
**(2) IMPLEMENTAÇÃO, DECLARADA ANTES DE RODAR** (`etapaA_vies2.py`): viés de F̂ = F(θ̂) em segunda ordem, viés(F̂_g) ≈ gᵀ·b_Box + ½·tr(H_F,g·Σ), SÓ ao longo de
v_3 (como o K8-v3, exato no modelo de dados): b_β = −(σ²/2)·M⁻¹·BᵀJA_3·q, q = v_3ᵀB·M⁻¹·Bᵀv_3, M = BᵀG_τB (as resolvidas fixas); termo do funcional
½·h_g·σ²·q, com h_g = (F₊ + F₋ − 2F₀)/δ² das avaliações JÁ GRAVADAS do funcional em θ·exp(±δ·v_3) (Gdir de cada desenho). **Ressalva:** δ grande (lote 1
1.215, piloto 1.035 — até o fator 2) → estimativa GROSSEIRA da curvatura em θ verdadeiro. **Lote 1:** CaBurst_PA1 h = +2.96 ms (os DOIS extremos atrasam o PA:
+1.10 e +3.28 ms), BAC_PA2 +0.25 ms, EPSP_apical_ponta ≈ 0. **Piloto:** BAC_PA2 +0.14; **CaBurst_PA1 NÃO ESTIMÁVEL** (contagem 1 → 0 no extremo −) → termo do
funcional omitido nele (só Box; assinalado). Componentes: CaBurst_PA1, BAC_PA2, EPSP_apical_ponta (as demais lineares); 4 modelos de ruído; cada desenho no
SEU nível certificado de hoje (PONTO_FIXO.json). **Monte Carlo** (2000 ajustes; o modelo do K8-v3 + o funcional quadrático): viés e cobertura de F(θ̂) e do
estimador CORRIGIDO F̂_c = F(θ̂) − [∇F(θ̂)ᵀ·b_β(θ̂) + ½·h·σ²·q(θ̂)] (correção avaliada em θ̂, σ conhecido — o padrão). **Conferência da fórmula:**
|MC − fórmula| ≤ 3 erros-padrão do MC OU ≤ 20% da fórmula (segunda ordem). **Leitura (do prompt, declarada):** sobre o viés COMPLETO do MC no nível certificado:
≤ 10% da tolerância → registrar, nada muda; > 10% e residual corrigido ≤ 10% → propor que a especificação suponha um estimador com correção de viés (e o
preprint diga isso); residual > 10% → propor incluir o viés na especificação e reportar quanto cada nível certificado cai. Nada é adotado sem o Martel.
**RESULTADO (167, `results/etapaA_lotes/prompt0003/vies2.json`, 2000 ajustes por caso): CONFERÊNCIA fórmula × MC OK em TODOS os casos.** Viés/tol no nível
certificado de cada desenho (Box + funcional = fórmula | MC | corrigido):
- **lote 1, CaBurst_PA1:** iid (8.555) **−0.160 + 0.196 = +0.036 | MC +0.033 | +0.010**; 1 ms +0.006 | +0.004; 10 ms +0.0005 | +0.001; 50 ms +0.0003 | +0.0001.
  BAC_PA2 iid −0.016 + 0.017 = +0.0005 | MC +0.003; EPSP_apical_ponta iid +0.010 | +0.008. **O viés de Box do K8 é CANCELADO pela curvatura do próprio funcional
  ao longo de v_3** (a latência do CaBurst é convexa ao longo de v_3 nos dados E no funcional — a mesma física): o viés completo fica ≤ 3.3% em todos os ruídos.
  (Nota: o termo de Box SOZINHO pela fórmula, −0.160, é ~25% maior que o MC do K8-v3, −0.127 — a 2ª ordem superestima nesse σ; o completo confere.)
- **piloto-6:** **CaBurst_PA1 SEM o termo do funcional** (h não estimável: contagem 1 → 0 no extremo − de v_3) → só Box: iid (4.628 = σ*) −0.100 | **MC −0.106** |
  corrigido −0.016; 1 ms −0.033 | −0.049 | −0.016; 10 ms −0.012 | −0.006; 50 ms −0.011 | −0.016. BAC_PA2 e EPSP_apical_ponta ≤ 0.2%.
**LEITURA (declarada no prompt):** lote 1, todos os ruídos → viés completo ≤ 10% → **nada muda**; piloto-6 1/10/50 ms → ≤ 10% → nada muda; **piloto-6 iid →
"viés" 0.106 > 10% e residual corrigido 0.016 ≤ 10% → pela leitura, PROPOR estimador com correção de viés** — COM A RESSALVA de que ali o viés NÃO é completo (falta
o termo do funcional, que no lote 1 cancelou o de Box). **Os níveis certificados do EXPERIMENTO** (iid 8.555 e 1 ms 1.929 do lote 1; 10 ms 0.717 e 50 ms 0.759
do piloto-6) **têm viés completo ≤ 3.3%** — nenhum é afetado. Critério do prompt 0002 (≥ 95%): lote 1 PASSA nos 4; piloto-6 PASSA em 10/50 ms e "falha" em iid
(cobertura 0.8845) e 1 ms (0.944) por COBERTURA, não por viés — o nível certificado ali é σ* (iid) ou 0.82σ* (1 ms), onde os 90% da definição (decisão 1)
dominam; a correção quase não muda a cobertura (0.892 / 0.945). Relatório: `docs/canal/relatorios/0003-vies-de-segunda-ordem.md`.
**DECISÃO DO MARTEL SOBRE O 167 (2026-10-27): NÃO ADOTAR o estimador com correção de viés.** A especificação continua sem correção de viés do estimador.
**Registrado:** o viés de segunda ordem do estimador (Box + curvatura do próprio funcional, ao longo de v_3) FOI CALCULADO e é DESPREZÍVEL nos níveis
certificados do experimento — ≤ 3.3% da tolerância (iid 8.555 e OU 1 ms 1.929, lote 1; OU 10 ms 0.717 e OU 50 ms 0.759, piloto-6); fórmula e Monte Carlo
concordam. É assim que o preprint deve dizer.


**168. (D132) RESULTADO DO LOTE 2 (concluído 2026-10-28 07:46; relatório `results/etapaA_lotes/lote2/relatorio.txt`) — LOTE COMPLETO; REGRA DE PARADA NO
PONTO FIXO (item 163): PARAR.** 15 injeções distais + somática (piloto 5 + lote 1 5 + lote 2 5); nenhuma unidade NÃO AVALIADA. Ponto fixo na rodada 2
(candidata v_6 → funcional FORA: contagem do CaBurst 1 → 0 no +, 1 → 2 no − — de novo a fronteira de regime do item 165); resolvidas v_1, v_2, v_4, v_5.
Lote 2 × lote 1, no ponto fixo (σ* / σ_lin, mV; ganho): iid 28.82 / 7.175 (+2.0% / −16.1%); 1 ms 11.76 / 1.619 (+1.3% / −16.1%); **10 ms 5.733 / 0.538
(+0.0% / −8.9%); 50 ms 6.327 / 0.541 (+0.2% / −3.1%)** → todos os ganhos com ruído lento < 10% (queda conta como < 10%) → **PARAR (lote completo: a curva
saturou)**. O lote 3 NÃO roda (exige SEGUIR; os trabalhos lt3_* e as rodadas não usadas do ponto fixo ficam em ESPERA, sem segurar a fila). σ* limitado pelo
CaBurst_PA1 (iid: BAC_PA2); σ_lin limitado por v_3 nos 4 ruídos. **De novo a NÃO MONOTONIA** (item 162): 15 injeções dão σ_lin MENOR que 10 (−16% / −9% / −3%)
— defeito do método (obriga a usar todas as linhas), registrado; a regra declarada mandou parar. **Nível certificado do EXPERIMENTO (máximo entre os desenhos)
INALTERADO:** iid 8.555 e 1 ms 1.929 (lote 1); 10 ms 0.717 e 50 ms 0.759 (piloto-6). Lote 2 sozinho: 7.175 / 1.619 / 0.538 / 0.541. Disco: 76 GiB livres
(lote 2 ocupa 27 GB; traços das direções já apagados por unidade, item 154). **P-abs AO LADO (candidato — NÃO adotado, K8 falhou; `etapaA_pabs_ao_lado.py`,
K4 exato):** iid 7.175, 1 ms 1.782, 10 ms 1.568, 50 ms 1.636 (lote 1: 8.555 / 1.929 / 1.559 / 1.621) → pelo P-abs também saturou com ruído lento (+0.6% / +0.9%),
SEM a queda não monótona — só informação.
Relatório: `docs/canal/relatorios/R0003-lote2.md`.


**169. (D132) PROMPT 0006 DO CANAL — FIM DA ETAPA A EM LOTES; DECISÕES 1–4 DO MARTEL (2026-10-28).**
**Registrado:** a Etapa A em lotes TERMINOU (R0003): a regra de parada agiu sozinha (PARAR, lote completo); nível certificado do experimento INALTERADO — iid 8.555
e OU 1 ms 1.929 (lote 1); OU 10 ms 0.717 e OU 50 ms 0.759 (piloto-6). A queda do σ_lin com mais dados repetiu-se no lote 2 (defeito do método, item 162); pelo
P-abs (candidato, não adotado) ela não aparece e o lote 2 também satura (1.568 / 1.636). **Correções aceitas do relatório 0005:** (a) não há rádio (D68): o campo
de moduladores é um perfil calculado no HANU_R e entregue pela estrela e pela cadeia; (b) "acoplar primeiro, converter por último" já estava registrado (P24/P34)
— o novo é o mecanismo explícito e o bônus de observação durante a campanha; (c) o D82 já convertia o tronco inteiro.
**Decisões do Martel (APROVADAS):** (1) **estudo das sinapses** (D133, 1º da fila): começar pelo PLANO, sem simular até ele ser aprovado → `docs/PLANO_SINAPSES.md`
(estudo mínimo: kernels sinápticos do reduzido + Fisher analítica + teste sintético, ~1–2 h de CPU; aguarda aprovação das premissas, do conjunto funcional
sináptico e dos limiares). (2) **Limpeza da fila:** retirados do TRABALHOS.json os 127 trabalhos em ESPERA — lote 3 (63) e rodadas não usadas do ponto fixo (64)
(`neuron/results/limpeza/fila_retirados_2026-10-28.txt`; os concluídos ficam como registro). (3) **Os 27 GB do lote 2** (traços das unidades θ): MANTIDOS até a
próxima conexão do HD; aí copiar para o arquivo frio, conferir por sha256 e só então apagar (o backup do HD de 26/10 é anterior ao lote 2 — hoje esses traços
não têm cópia). (4) **D82 CONFIRMADO** (nota no D137).


**170. (D132) PROMPT 0007 DO CANAL — DECISÕES 1–4 DO MARTEL, TODAS APROVADAS (2026-10-28).** (1) **Estudo mínimo das sinapses APROVADO com as emendas** do
prompt; procedimento: premissas (com fonte primária conferida), conjunto funcional, tolerâncias, limiares de leitura e a conta de guardanapo escritos no
`docs/PLANO_SINAPSES.md` → commit e push → só então calcular; trocar uma premissa depois do resultado exige justificativa independente (fonte errada conta).
(2) **Consulta-piloto dos atlas LIBERADA** (CELLxGENE Census, ~10 mil neurônios corticais humanos, ambiente separado, sem tocar no `.nrnvenv`; parar e reportar se
a transferência passar de 5 GB). (3) **D138: operacionalização aceita com DUAS condições** (envelope objetivo E reconhecimento pela pessoa e por quem convive;
vale a mais conservadora) — registrado no D138. (4) **Material do preprint APROVADO:** figuras com scripts a partir de resultados GRAVADOS; densidade de leitura
nos desenhos condicionados (≤ 6 h de CPU; NADA do lote 2 sai do disco antes); remedida do artefato do repouso em dupla precisão (≤ 24 h de CPU e ≤ 10 GB, fila
vazia); pasta do repositório público pronta FORA do HANU e NÃO publicada; conferência independente dos números; sensibilidade ao CaBurst e soma sozinho nos
desenhos condicionados.


**171. (D132) PROMPT 0007 DO CANAL — RESULTADOS (2026-10-29; relatório `docs/canal/relatorios/0007-revisao-sinapses-atlas-preprint.md`).**
**(1) SINAPSES — estudo mínimo** (premissas, tolerâncias, limiares e conta de guardanapo no `docs/PLANO_SINAPSES.md` §9, commit `c084c2f` ANTES do cálculo).
**Teste sintético** (GLS × 1/F; 20 observadas, 30 não observadas, 400 repetições; critério [0.75, 1.25], mediana [0.9, 1.1]): 1ª rodada **FALHOU** (mediana
1.245, máx 4.4 — a variabilidade quântica e o jitter da própria conexão são travados no evento, tratados como estacionários); fórmula corrigida com o **piso
por evento** (critério inalterado) → **PASSA** (mediana 1.025 [0.886, 1.152] e 1.026 [0.868, 1.206]). **Kernels** do reduzido a 10⁻⁸ (64 sítios; R_in 41.55
MΩ; ΔV ao limiar 32.67 mV; pontos de operação obtidos 2.21× e 5.54× para alvos 2× e 5×). **Resultado (v2):** **C: T* = 0.26 h → NÃO LIMITA em W1/W2/W3**;
**P: T* = 19 252 h → CANDIDATO A LIMITE FUNDAMENTAL nas três**. Em C, robusto a f, R_in, jitter, taxa, σ_e, CV e EPSP 0.15 mV (todos ≤ 1.3 h); só o soma lido
→ 4.0 h (APERTADO em W1); **1 contato por conexão → 189 h (CANDIDATO em W1 e W2, APERTADO em W3)**. Decide quase sempre o critério (b), no menor k (k_lim/2).
Modo ativo: 50 pulsos discriminam mas NÃO medem o peso (C: ~138 por parceiro; serial 5.7 h; o passivo é mais rápido; simultâneo só aproximado). **Conta de
guardanapo:** C concorda (minutos–1 h × 0.26 h); P NÃO (49 h × 19 252 h) — a conta errou o EPSP no ponto de operação (0.028 mV, não 0.15: ×29) e o ε exigido
pelo critério (a) (~3%, não 20%: ×43), e não contou o ganho do estimador eficiente (~×13); o pior padrão soma ×3.1. **Correção de código antes do relatório:** a
busca gulosa do pior padrão olhava só 2 000 conexões por índice (fora do método declarado) → v2 com todas; casos com ≤ 2 000 observadas IDÊNTICOS (conferência);
mudaram f = 0.9 (0.286 → 0.294 h) e f = 1.0 (0.242 → 0.261 h); nenhuma leitura de janela mudou; a v1 fica gravada. **Correção de FONTE (valor inalterado):** os
2 mV de σ_e em P vêm do rascunho do preprint, não do DECISOES → ESTIMATIVA (nota no plano §9.2). **Consistência entre premissas (informação, nada mudado):** em
P, 72% das conexões têm EPSP somático a 1× abaixo do mínimo medido por Markram 1997 (0.15 mV) — a calibração a 147 µm + distribuição pela área põe a maioria
fora do suporte da fonte (que mediu pares L5–L5 com contatos a 80–585 µm); em C, 0% (percentis 5/50/95: 0.56 / 0.93 / 1.31 mV). Registrado no P24 (resultado)
e no P55 (Q1: em P, T* ≫ escala das regras lentas → observação passiva mal posta).
**(2) ATLAS:** lista de 101 genes DECLARADA antes (HGNC; pseudogenes HTR3C2P e HTR5BP retirados antes de consultar). Piloto do Census **BLOQUEADO**: o
`tiledbsoma` 2.3.0 só tem wheel para Python 3.9–3.13; a máquina tem 3.14; a compilação falhou (memória; build) — ~325 MB de pacotes transferidos, nenhuma
consulta. Caminho = decisão do Martel. Patch-seq listados (DANDI 000020, 141.9 GB; 000636, 24.5 GB), nada baixado.
**(3) PREPRINT:** (a) seis figuras com script (`neuron/preprint_figuras.py`; dados 450 KB). (b) **Densidade nos desenhos condicionados** (~22 min de CPU;
conferências EXATAS): 504 → 21 leituras custa ÷1.07–1.38 no σ* dos lotes e ÷1.20–1.74 no piloto-6; σ_lin por grade NÃO AVALIÁVEL (traços de direções
apagados; ~96 h para refazer no lote 2) → condição para os 27 GB do lote 2 cumprida (seguem até o HD). (c) **Repouso em double** (1 648 s): o artefato
(3.3×10⁻⁴ mV em M1, 4.3×10⁻³ mV em M4) independe da tolerância e fica 760–850× acima do piso a 10⁻⁸ (o "11–22×" do item 88 era limitado pelo float32).
(d) Pasta pública pronta FORA do repositório, NÃO publicada (50 arquivos, 388 KB; varredura 0/0/0; ModelDB 139653). (e) Números do rascunho conferidos; dois
NÃO conferem como escritos: a "grade de leitura de 400 µm" (as leituras são 504; a de 400 µm é a dos 20 candidatos de injeção) e "39× / ≥ 3.8×" do soma
sozinho (do conjunto de 2 injeções do piloto CONDICIONADO, item 150 — não dos desenhos do preprint; rótulo corrigido em 29/10, item 172). (f) **Sensibilidade ao CaBurst_PA1 nos desenhos condicionados** (`etapaA_sens_caburst_cond.py`; conferência 1.0 ms = PONTO_FIXO
EXATA nos três; ponto fixo FECHA em todas as tolerâncias): nível do experimento iid / 1 / 10 / 50 ms = 4.305 / 1.699 / 0.590 / 0.558 (0.2 ms), 8.555 / 1.929 /
0.590 / 0.709 (0.5 ms), 8.555 / 1.929 / 0.717 / 0.759 (1.0 ms) — com ruído lento cai só ×1.22–1.36 (nos lotes limita o σ_lin); substitui o item 139 no
preprint. (g) Soma sozinho, mesmas direções: desvantagem ≥ 55.7 / 17.3 / 9.0 / 9.2 (piloto-6), ≥ 24.7 / 5.6 / 1.71 / 1.62 (lote 1), ≥ 21.2 / 4.81 / 1.60 /
1.60 (lote 2). Código: `etapaA_piloto.py` ganhou `--tol-CaBurst` (padrão inalterado) e ficou importável (`elif '--analise'`); regressão do ponto fixo 13/13 depois do
`elif` (o `--tol-CaBurst` veio depois: sem a opção o código não muda; com 1.0 ms a análise reproduz os três PONTO_FIXO exatamente).
**Adendo ao item 171 (2026-10-29 08:55; job `sin_pior_padrao`, conferência T* = v2 EXATA):** em P o pior padrão é ESTRUTURAL (membro dominante = 3% do
numerador; sem ele, 19 100 h); com 1 contato por conexão, os 189 h vêm de UMA conexão lenta (0.059 Hz, percentil 0.3; EPSP 0.50 mV; 100% do numerador) unida a
26 parceiros desprezíveis — sem ela, 0.04 h: o critério (b) vira "peso da conexão mais lenta a ~3%". Critério e resultado ficam como declarados; a observação
vai ao Martel como opção (b′) (critério novo, declarado antes e testado em dado sintético) — relatório 0007, adendo.
**Ressalva (prompt 0009, item 174):** a busca do (b) pode subestimar o pior padrão em até ~10% em casos pequenos (teste do 0008: 0.90 do exato no pior caso);
nenhuma leitura de janela muda.


**172. (D132) PROMPT 0008 DO CANAL — DECISÕES 1–4 DO MARTEL, TODAS ACEITAS (2026-10-29).** (1) **Atlas:** Python 3.13 pelo `uv` no nível do usuário (sem
sudo; reversível apagando as pastas do `uv` e o ambiente novo) e o piloto como declarado no 0007 (para em 5 GB). (2) **Sinapses, próximo passo:** (a) literatura
primeiro, sem cálculo — tabela por via e proposta de cenário C revisto, NENHUM cálculo com premissas revistas antes da revisão; (b) critério **(b′)** declarado no
plano, commit e push, teste sintético de resposta conhecida, só então calcular — reportado AO LADO do (b), que segue sendo o resultado registrado do estudo;
(c) combinações dois a dois de "1 contato" e "só o soma" com as outras variações, com (b) e (b′); a plasticidade de curto prazo fica para depois de (a).
(3) **Pasta pública:** licença MIT no código e CC BY 4.0 em dados e figuras; ficam o nome do Martel e os nomes de infraestrutura; comentários em português com
nota no README; fila reduzida (só Etapa A, varrida); extrato do registro D131–D132 com os itens pessoais/operacionais marcados para o Martel decidir um a um.
(4) **Pré-registro verificável:** quando o repositório público existir, os critérios de cada estudo novo são publicados nele ANTES de rodar (a data passa a
ser verificável por terceiros; hoje só o histórico privado a comprova). **Correção de rótulo (item 171 e relatório 0007):** o conjunto "2 inj." do item 150
(soma + g_apic[60]_32; 3.22 / 0.863 / [0.322; 0.412] / [0.310; 0.455]) é do piloto CONDICIONADO, não "desenho antigo, não condicionado" como escrevi; a
conclusão prática não muda (os desenhos do preprint são soma + 5/10/15 → vale a tabela (g) do 0007).


**173. (D132) PROMPT 0008 DO CANAL — RESULTADOS (2026-10-29; relatório `docs/canal/relatorios/0008-sinapses-literatura-atlas-pasta.md`).** **(1) Literatura
(sem cálculo; fontes conferidas, MEDIDO):** contatos por conexão — 5.5 ± 1.1 PUTATIVOS em rato P14–16 (Markram 1997), 4.0 / 3.2 putativos em humano / camundongo
adultos L2/3 (Hunt 2023), mas **1.1 ± 0.4 sinapse por conexão na EM** (L5-ET → excitatórias, camundongo P87; "a sinapse única é a típica"; Bodor 2025);
EPSP unitário adulto: camundongo L5-ET 0.52 / L5-IT 0.24 mV (médias), humano L5 0.80 (Seeman 2018), humano L2/3 1.36 (Hunt 2023); conexões locais
proximais (~80–150 µm); tufo distal atenuado > 40× (Williams & Stuart 2002). Lefort 2009 não conferido (texto inacessível). **Proposta C′ PARA REVISÃO,
não calculada:** 1 contato, 0.5 mV, conexões locais proximais, tufo como classe separada (EPSP local ESTIMATIVA), CV 0.4. **(2) Critério (b′)** (plano §10,
commit `b5ae1ff` ANTES): teste sintético PASSA de primeira (T1 erro 2×10⁻¹⁶; T2 ≥ 0.99 do exato em 100% de 300; info: a busca do (b) registrado chega a só 0.90
do exato no pior caso pequeno). Estudo v3 (conferência (a), (b) = v2 EXATA em 18 casos): com (b′), C 0.186 h; **1 contato 189 → 7.25 h** (APERTADO em W1); só o
soma 4.02 → 1.33 h; **P 6 202 h — segue CANDIDATO nas três janelas, agora pelo critério (a)**. **(3) Combinações (15 pares):** com (b), todo par com 1 contato é
CANDIDATO em W1; com (b′), só **"1 contato + só o soma" = 69.8 h** é CANDIDATO (W1) — leituras dendríticas deixam de ser opcionais se o contato único é o típico.
**(4) Atlas:** `uv` + Python 3.13 (ambiente novo `~/.venvs/hanu_census313`; nada apagado); Census 2025-11-08 sem conta; Siletti (Human Brain Cell Atlas v1.0)
PRESENTE, 138 conjuntos, 10.1 milhões de células; 5 138 342 neurônios corticais candidatos; a amostra 10 mil × 101 genes NÃO rodou — o vigia de memória (novo:
para abaixo de 600 MB disponíveis ou acima de 5 GB) parou duas tentativas (navegador ~6 GB); uma tentativa travou por erro meu (contexto sem o S3 anônimo do
Census), parada pelo PID; ~0.6 GB transferidos ao todo. **(5) Preprint:** figuras com os termos do artigo; valores singulares do repouso em double PRECISAM
simular (~8 h de CPU; ~16 GB com traços ou ~0.1 GB acumulando) — não rodado. **(6) Pasta pública** (não publicada): MIT + CC BY 4.0, nota de idioma, dados e
figuras, fila reduzida (238 trabalhos), caminhos absolutos dos PONTO_FIXO relativizados; varredura 0/0/0; extrato D131–D132 com 71 de 175 blocos marcados, FORA
da pasta pública.


**174. (D132) PROMPT 0009 DO CANAL — DECISÕES 1–6 DO MARTEL, TODAS APROVADAS (2026-10-29).** (1) **C′ é o novo cenário CENTRAL das sinapses** (1 contato,
variante 2; EPSP 0.5 mV, variantes 0.25 e 0.8; conexões locais em basal + oblíquo proximal até ~200 µm, calibradas no sítio; tufo como classe separada, ≤ 30%
das sinapses, EPSP no soma = local ÷ 40; CV 0.4), com uma **variante HUMANA adulta (H: EPSP 0.8 mV, CV 0.2)** e variantes do EPSP local do tufo (igual ao das
locais e metade); P fica como está, para comparação; tempo também por CLASSE (locais × tufo). (2) **(b) e (b′) lado a lado** nos estudos. (3) **Leitura
dendrítica como requisito do elemento** (D133 e P24). (4) **Janela de computação:** trabalhos pesados (NEURON, atlas) só lançam em dias úteis 23:00–07:30 e
sábado/domingo o dia inteiro; a porta de memória continua valendo dentro da janela; trabalhos leves (numpy, minutos) podem rodar fora se a porta deixar; as
configurações de energia do GNOME NÃO são tocadas. (5) **Valores singulares do repouso em dupla precisão:** rodar numa noite, dentro da janela. (6) **Extrato
do registro:** ficam os itens científicos, saem os puramente operacionais (backup, HD, GitHub, energia/GNOME, chaves/nuvem, caminhos pessoais,
navegador/máquina); o Claude Code lista só os DUVIDOSOS; licença MIT com o nome completo "Martel Alexandre Del Colle". **Ressalva do (b) registrado (anotada
junto do resultado, item 171):** a busca do (b) pode SUBESTIMAR o pior padrão em até ~10% em casos pequenos (teste do 0008: mínimo 0.90 do exato); nenhuma
leitura de janela muda.


