# etapaA_unit.py — D132 item 66 (1b) / item 85: a UNIDADE da Etapa A = um ponto de injeção p, com TODAS as perturbações
# (θ ±1% em log nos 30 parâmetros, ganho, posição, geometria) e a redução por ponto de leitura r (JᵀJ, JᵀX, XᵀX, JᵀΔy).
# Interface do etapaA_runner (units / substeps / evaluate / reduce).
# ITEM 85 — PORTE PARA O CÓDIGO ÚNICO: repouso e protocolos pelo `stim_common.CommonSim` (repouso CONVERGIDO por critério,
# guardado pela chave automática do modelo → reaproveitado entre unidades e processos; parada forçada em todo estímulo;
# autotestes no construtor; a cada subpasso, `resettle` confere o repouso). O laço e o repouso próprios (3 s a passo fixo,
# usados na checagem de tolerância do item 78) SAÍRAM daqui — a cópia antiga fica só como registro.
# DOIS MODELOS, O MESMO CÓDIGO: 'region' (modelo direto, 30 parâmetros por região, nós nos 503 pontos da grade) e 'hay'
# (Hay L0 Δ 0.5 µm em θ verdadeiro, leitura/injeção por interpolação entre nós — a MESMA referência do termo de viés do
# conjunto funcional, etapaA_F.HayRef): os traços do 'hay' no ponto p dão o VIÉS DE ESPECIFICAÇÃO POR PONTO (item 26),
# JᵀΔy por leitura com Δy = y_Hay − y_red(θ_verd), calculado na redução da unidade 'region' (que ESPERA os traços do 'hay').
# UNIDADE SOMÁTICA ('p_soma', item 78): M3 (1.9 nA × 5 ms, lê os 503 pontos + soma) e M5 (degraus do Hay, lê o soma);
# sem o subpasso 'posicao' (o eletrodo no soma não tem "ao longo do ramo").
import os, math, time, json
import numpy as np
from neuron import h
import etapaA_model as EM
import stim_common as SC

STEP = math.log(1.01)
M1 = dict(amp=0.05, delay=100.0, dur=1000.0, tstop=1150.0)
M4 = dict(amps=(0.2, 0.5, 1.5), onset=5.0, taud=5.0, tstop=300.0)
M3 = dict(amp=1.9, delay=50.0, dur=5.0, tstop=150.0)                   # item 78: unidade SOMÁTICA (bAP, lê todos os pontos)
M5 = dict(amps=(0.78, 1.0, 1.9), delay=150.0, dur=2000.0, tstop=2300.0)  # degraus do Hay no soma (lê o soma)
DT = 0.1
GEO_SEED = 131
HAY_DELTA = 0.5


# ITEM 91 — CADEIA DE MEDIDA (regra de bloqueio do D132 itens 51–52 / P24–P28, parte mínima): linha de base na ÚLTIMA
# amostra ANTES do estímulo, e EXCLUÍDAS as amostras nos instantes de DESCONTINUIDADE do estímulo (salto no VALOR da
# corrente: ligar/desligar de cada degrau; o α do M4 é contínuo em valor). A MESMA função em todo lado: na redução (J, X,
# Δy do viés), na análise de tolerância e nas verificações (os dois lados de toda comparação).
PROT = {'M1m': (M1['delay'], (M1['delay'], M1['delay'] + M1['dur'])), 'M1p': (M1['delay'], (M1['delay'], M1['delay'] + M1['dur'])),
        'M4': (M4['onset'], ()), 'M3': (M3['delay'], (M3['delay'], M3['delay'] + M3['dur'])),
        'M5': (M5['delay'], (M5['delay'], M5['delay'] + M5['dur']))}
_ix = lambda t: int(round(t / DT))


def pre_index(lab):
    return _ix(PROT[lab][0]) - 1


def cadeia(a, lab):
    """Traço(s) de um rótulo (tempo no ÚLTIMO eixo, grade DT a partir do fim do repouso) → linha de base pré-estímulo e
    sem as amostras nos instantes de descontinuidade. Idempotente na linha de base."""
    a = np.asarray(a, np.float64); a = a - a[..., [pre_index(lab)]]
    disc = [_ix(t) for t in PROT[lab][1]]
    return np.delete(a, disc, axis=-1) if disc else a


# ITEM 101/103 — PROTOCOLOS COM DISPARO (base aprovada no item 103): voltagem só ANTES do 1º disparo (o mais cedo entre
# TODAS as avaliações → as mesmas amostras em todas); disparos pelos TEMPOS (cruzamento ascendente do nível fixado na BASE —
# início + ½·amplitude —, interpolado; × |dV/dt| da base no cruzamento: com o mesmo σ_V, σ_t = σ_V/|dV/dt|); e, por disparo
# identificado (item 95, com a contagem do item 102), ATRIBUTOS em mV (ruído σ_V): voltagem no LIMIAR (instante interpolado
# em que dV/dt cruza DV_MIN), no PICO e o VALOR mínimo da pós-hiperpolarização (interpolação parabólica nos extremos; só o
# valor). Nenhuma amostra de voltagem depois do 1º disparo. UM caminho: redução, análises e comparações usam `representar`.
DV_MIN = 20.0             # mV/ms — critério de derivada do detector (D122)
PROM_MIN = 20.0           # mV — proeminência mínima
ATRIBUTOS = ('tempo', 'limiar', 'pico', 'ahp')       # todos os implementados (verificação)
ATRIBUTOS_USADOS = ('tempo',)                            # item 104: limiar, pico e AHP FORA (linearidade real)


def disparos(y):
    """Disparos de um traço (grade DT): cada subida contígua com dV/dt ≥ DV_MIN abre um disparo; pico = 1º máximo local
    depois; proeminência (pico − mínimo desde o pico anterior) ≥ PROM_MIN. Lista de dicts (i_on, i_pk)."""
    y = np.asarray(y, float); n = len(y)
    if n < 3: return []
    dv = np.diff(y) / DT
    if dv.max() < DV_MIN: return []
    out = []; prev_pk = 0; k = 0
    for a in np.flatnonzero(dv >= DV_MIN):
        if a < k: continue
        b = a
        while b + 1 < n and y[b + 1] >= y[b]: b += 1
        k = b + 1                                                  # a próxima subida começa depois deste pico
        if y[b] - y[prev_pk:a + 1].min() < PROM_MIN: continue
        out.append({'i_on': int(a), 'i_pk': int(b)}); prev_pk = b
    return out


def _parab(y, i):
    """Valor do extremo pela parábola nos 3 pontos em torno de i."""
    if i <= 0 or i >= len(y) - 1: return float(y[i])
    y0, y1, y2 = y[i - 1], y[i], y[i + 1]; den = y0 - 2 * y1 + y2
    return float(y1) if den == 0 else float(y1 - 0.125 * (y0 - y2) ** 2 / den)


def _limiar(y, q):
    """V no instante (interpolado) em que dV/dt cruza DV_MIN na subida do disparo q."""
    dv = np.diff(y) / DT; i = q['i_on']
    if i == 0 or dv[i - 1] >= DV_MIN: return float(y[i])
    f = (DV_MIN - dv[i - 1]) / (dv[i] - dv[i - 1]); t = (i - 0.5 + f)          # dv[j] vive no ponto médio j + ½
    j = int(np.floor(t)); w = t - j
    return float(y[j] * (1 - w) + y[j + 1] * w)


def _cruza(y, sp, L):
    """Tempo (ms) do cruzamento ascendente do nível L na subida do disparo sp; None se não chega a L."""
    for k in range(max(sp['i_on'], 1), sp['i_pk'] + 1):
        if y[k] >= L > y[k - 1]:
            return (k - 1 + (L - y[k - 1]) / (y[k] - y[k - 1])) * DT
    return None


def _identidade(tb, tx, T_end):
    """Identidade dos K disparos da base, SÓ NO TRECHO DAS GRANDEZAS USADAS (item 123 (1)): as grandezas são os tempos dos K disparos da
    base (e a voltagem antes do 1º) — um disparo POSTERIOR ao K-ésimo não as altera. (a) deslocamentos: K = 1 → |d_1| < ½·min(tb_1,
    T − tb_1); K ≥ 2 → consecutivos (item 95); (b) NENHUMA INSERÇÃO até o K-ésimo: para i = 1…K, o disparo da avaliação mais próximo da
    posição prevista p_i = tb_i + d_{i−1} (d_0 = 0; acompanha a deriva) é o i-ésimo — um disparo inserido antes de um usado fica mais perto
    dele que o casado; (c) NADA depois do K-ésimo (a contagem até o horizonte do item 102 saiu: recusava leituras por um 2º disparo
    posterior ao único usado — os 195 bAPs do item 122)."""
    tb, tx = np.asarray(tb, float), np.asarray(tx, float); K = len(tb)
    if len(tx) < K: return False
    d = tx[:K] - tb[:K]
    if K == 1:
        ok = abs(d[0]) < 0.5 * min(tb[0], T_end - tb[0])
    else:
        isi = np.diff(tb)
        r = np.concatenate(([abs(d[0]) / (0.5 * isi[0])], np.abs(np.diff(d)) / (0.5 * isi)))
        ok = bool(np.all(r < 1.0))
    for i in range(K):
        p = tb[i] + (d[i - 1] if i else 0.0)
        if int(np.argmin(np.abs(tx - p))) != i: return False
    return bool(ok)


def _atributos(y, sp, L, dvdt, ahp_last):
    """Para os disparos sp (já casados com os da base): tempo×|dV/dt|, limiar, pico, mínimo da AHP (por disparo)."""
    T = len(y); out = {k: [] for k in ATRIBUTOS}
    for i, q in enumerate(sp):
        t = _cruza(y, q, L[i])
        if t is None: return None
        out['tempo'].append(t * dvdt[i]); out['limiar'].append(_limiar(y, q)); out['pico'].append(_parab(y, q['i_pk']))
        end = sp[i + 1]['i_on'] if i + 1 < len(sp) else min(T, q['i_pk'] + ahp_last)
        seg = y[q['i_pk']:max(end, q['i_pk'] + 2)]; j = q['i_pk'] + int(np.argmin(seg))
        out['ahp'].append(_parab(y, j))
    return out


def _feat_disparos(y, spk, K, L, tb, dvdt, ahp_last, T, tipos):
    """Atributos de UMA avaliação para os K disparos da base (contagem, nível, identidade do item 95/102, atributos); None se
    qualquer passo falhar. UM caminho: usado por `representar` e por `representar_extra`."""
    if len(spk) < K: return None
    tk = [_cruza(y, spk[i], L[i]) for i in range(K)]
    if any(t is None for t in tk): return None
    if not _identidade(tb, tk + [q['i_pk'] * DT for q in spk[K:]], T * DT): return None
    a = _atributos(y, spk[:K], L, dvdt, ahp_last)
    if a is None: return None
    return np.concatenate([a[t] for t in tipos]) if tipos else np.zeros(0)


def representar(evals, base='base', tipos=ATRIBUTOS_USADOS):
    """evals: {chave: array (R, T)} — as MESMAS R leituras em todas as avaliações (inclusive a referência do viés).
    feats[chave][r] = [voltagem antes do 1º disparo (o mais cedo entre as avaliações)] ++ [atributos dos disparos da base, na
    ordem de `tipos`] — o MESMO conjunto em todas as avaliações; os atributos só entram se a identidade valer em TODAS.
    info por leitura: nº de disparos, se os atributos entraram, nº de amostras de voltagem, |dV/dt| nos cruzamentos."""
    keys = list(evals); R, T = evals[base].shape
    feats = {k: [] for k in keys}; info = {'n_disparos': [], 'tempos_ok': [], 'n_voltagem': [], 'dvdt': []}
    for r in range(R):
        sp = {k: disparos(evals[k][r]) for k in keys}
        # item 105: corte = a última amostra ANTES do início detectado (o detector atrasa até uma amostra — o "pé" carrega o
        # instante de início, que já está no tempo do disparo)
        first = [sp[k][0]['i_on'] for k in keys if sp[k]]
        cut = max(0, min(first) - 1) if first else T
        sb = sp[base]; yb = evals[base][r]; K = len(sb)
        L = [yb[q['i_on']] + 0.5 * (yb[q['i_pk']] - yb[q['i_on']]) for q in sb]
        tb = [_cruza(yb, q, l) for q, l in zip(sb, L)]
        dvdt = [abs(yb[int(np.floor(t / DT)) + 1] - yb[int(np.floor(t / DT))]) / DT for t in tb] if K and None not in tb else []
        ahp_last = int(round((tb[-1] - tb[-2]) / DT)) if K >= 2 else T
        ok = K > 0 and None not in tb; at = {}
        for k in keys:
            if not ok: break
            a = _feat_disparos(evals[k][r], sp[k], K, L, tb, dvdt, ahp_last, T, tipos)
            if a is None: ok = False; break
            at[k] = a
        for k in keys:
            v = evals[k][r][:cut]
            feats[k].append(np.concatenate([v, at[k]]) if ok else v)
        info['n_disparos'].append(K); info['tempos_ok'].append(bool(ok)); info['n_voltagem'].append(int(cut)); info['dvdt'].append(dvdt)
    return feats, info


def representar_extra(evals, extra, base='base', tipos=ATRIBUTOS_USADOS):
    """ITEM 121: features das avaliações `extra` (θ·exp(±δ_i v_i)) com o corte, os disparos da base e a identidade DEFINIDOS só por
    `evals` (o conjunto do Gram: base + eixos) — as extras NÃO mudam as features do Gram. Uma extra cujos disparos falham a
    identidade → atributos NaN (a linha conta como NÃO linear ao longo daquela direção); amostras de voltagem de uma extra que dispara
    antes do corte entram como estão (a 2ª diferença as marca). Devolve (feats de evals, feats de extra, info de evals)."""
    f, info = representar(evals, base, tipos)
    R, T = evals[base].shape; fx = {k: [] for k in extra}
    for r in range(R):
        cut, ok = info['n_voltagem'][r], info['tempos_ok'][r]
        if ok:
            yb = evals[base][r]; sb = disparos(yb); K = len(sb)
            L = [yb[q['i_on']] + 0.5 * (yb[q['i_pk']] - yb[q['i_on']]) for q in sb]
            tb = [_cruza(yb, q, l) for q, l in zip(sb, L)]; dvdt = info['dvdt'][r]
            ahp_last = int(round((tb[-1] - tb[-2]) / DT)) if K >= 2 else T
        for k in extra:
            y = extra[k][r]; v = y[:cut]
            if ok:
                a = _feat_disparos(y, disparos(y), K, L, tb, dvdt, ahp_last, T, tipos)
                fx[k].append(np.concatenate([v, a if a is not None else np.full(K * len(tipos), np.nan)]))
            else:
                fx[k].append(v)
    return f, fx, info


RHO_MAX = 0.1             # item 111: limiar do índice de linha
D_MIN = 1e-6              # linha sem sinal (‖d‖ ≤ D_MIN) fica — não pesa


def linhas_lineares(y0, yp, ym):
    """ITEM 113 — MÁSCARA DE LINHAS (redefinida após o resultado; a MESMA classificação do critério de peso): y0 (n,), yp/ym (n, P)
    → máscara (n,) True = linha MANTIDA. Para cada parâmetro p com |y₊ − y₋| > D_MIN, índice_p = |y₊ + y₋ − 2y₀| / |y₊ − y₋|; a linha
    é EXCLUÍDA se máx_p índice_p > RHO_MAX. Limite conhecido (K5): perturba UM eixo por vez — não vê não linearidade só ao longo
    de combinações (derivada cruzada); a verificação direta ao longo das direções fracas cobre isso (item 113 (2))."""
    dd = np.abs(yp - ym)
    idx = np.where(dd > D_MIN, np.abs(yp + ym - 2 * y0[:, None]) / np.maximum(dd, 1e-300), 0.0)
    return idx.max(axis=1) <= RHO_MAX


COBERTURA = 0.99          # item 118 (2): fração da incerteza de CADA componente funcional coberta pelas direções testadas
TETO_LOG = math.log(2.0)  # item 118 (2c): nenhum parâmetro sai do fator 2 na excursão


def direcoes_relevantes(s, V, Gf, cobertura=COBERTURA):
    """ITEM 118 (2): direções do Gram combinado (ii) por RELEVÂNCIA para o conjunto funcional. s (k,) valores singulares, V (30, k)
    vetores; Gf (m, 30) = componentes funcionais COM tolerância. c_gi = (g·v_i)² / s_i² (contribuição de v_i à variância de g; independe
    do ruído); f_gi = c_gi / Σ_j c_gj (adimensional — as componentes têm unidades diferentes); ordem decrescente de max_g f_gi; devolve o
    MENOR prefixo dessa ordem com Σ f_gi ≥ cobertura para TODO g, e as frações. s_i = 0 com g·v_i ≠ 0 → f = 1 (escolhida primeiro)."""
    proj = (Gf @ V) ** 2
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.where(s[None] > 0, proj / np.maximum(s[None], 1e-300) ** 2, np.where(proj > 0, np.inf, 0.0))
    tot = c.sum(1, keepdims=True)
    f = np.where(np.isinf(tot), np.where(np.isinf(c), 1.0, 0.0), c / np.where(tot > 0, tot, 1.0))
    ordem = np.argsort(-f.max(0), kind='stable'); acum = np.zeros(len(Gf)); esc = []
    for i in ordem:
        if np.all(acum >= cobertura): break
        esc.append(int(i)); acum = acum + f[:, i]
    return np.array(esc, int), f


def excursoes(V, esc, Gf, tol, h=STEP, teto=TETO_LOG):
    """ITEM 118 (2): δ_i = tolerância_g / |g·v_i| (o g que dá o MENOR δ_i; tol em unidades de g), limitado a [h, teto/max_p |v_ip|]:
    piso h = passo por eixo já validado (abaixo dele a 2ª diferença fica no piso numérico); teto = nenhum parâmetro sai do fator 2."""
    out = []
    for i in esc:
        gv = np.abs(Gf @ V[:, i])
        d = np.min(np.where(gv > 0, tol / np.maximum(gv, 1e-300), np.inf))
        out.append(float(max(h, min(d, teto / np.abs(V[:, i]).max()))))
    return np.array(out)


def linhas_lineares_direcoes(y0, ypv, ymv):
    """ITEM 118 (2): máscara AO LONGO das direções testadas — ypv/ymv (n, k) = y(θ·exp(±δ_i v_i)). A MESMA regra do índice por eixo
    (índice de 2ª diferença > RHO_MAX em QUALQUER coluna, colunas com |y₊ − y₋| ≤ D_MIN não contam), aplicada às direções.
    Item 121: valor NaN (atributo de disparo cuja identidade falhou na excursão — `representar_extra`) → linha EXCLUÍDA (sem o
    teste, NaN passaria por "sem sinal" e a linha ficaria)."""
    nan = np.any(np.isnan(ypv) | np.isnan(ymv), axis=1)
    return linhas_lineares(y0, np.nan_to_num(ypv), np.nan_to_num(ymv)) & ~nan


CURV_LIM = 0.3            # item 126: γ^N·√F ≤ 0.3 (doc. de MASS::rms.curv, Venables & Ripley, impl. Bates & Watts 1988 §7.3 — secundária)


def curvaturas(G, JtA, AtA, vel2):
    """ITEM 126: curvaturas de UMA direção v a partir de acumulados POR LINHA: G = JᵀJ, JtA = Σ_r J_rᵀ a_r, AtA = Σ_r a_r² (a = aceleração
    ao longo de v), vel2 = ‖J v‖². Parte tangente ‖a_T‖² = (Jᵀa)ᵀ G⁻¹ (Jᵀa) = Σ_k (u_kᵀ a)² (u_k vetores singulares à esquerda — o projetor
    no espaço das colunas de J não depende da escala dos valores singulares); intrínseca ‖a_N‖² = ‖a‖² − ‖a_T‖². Devolve (K^N, K^T) =
    (‖a_N‖, ‖a_T‖) / ‖J v‖² (Bates & Watts: intrínseca e de parâmetro)."""
    w, U = np.linalg.eigh(G); c = U.T @ JtA; k = w > 0
    t2 = float(np.sum(c[k] ** 2 / w[k])); n2 = max(float(AtA) - t2, 0.0)
    return math.sqrt(n2) / vel2, math.sqrt(t2) / vel2


def sigma_lin(KN, p, F, lim=CURV_LIM):
    """ITEM 126: o MAIOR ruído σ (por linha) com γ^N·√F = K^N·σ·√p·√F ≤ lim."""
    return lim / (math.sqrt(F) * math.sqrt(p) * KN) if KN > 0 else float('inf')


def branqueia_ar1(X, phi):
    """ITEM 128: branqueamento EXATO do ruído AR(1)/OU de variância marginal 1 ao longo das LINHAS de X (amostras consecutivas de UM traço):
    w_0 = x_0, w_t = (x_t − φ x_{t−1})/√(1 − φ²) → Wᵀ W = Σ⁻¹ (Σ_ij = φ^|i−j|). φ = 0 → identidade (o modelo iid)."""
    X = np.asarray(X, float)
    if phi == 0.0 or len(X) == 0: return X
    W = np.empty_like(X); W[0] = X[0]; W[1:] = (X[1:] - phi * X[:-1]) / math.sqrt(1.0 - phi * phi)
    return W


def linhas_lineares_norma(y0, yp, ym):
    """A regra DECLARADA no item 111 (ρ por norma sobre os parâmetros) — SUBSTITUÍDA (item 113); fica só para o controle K4."""
    d = np.linalg.norm(yp - ym, axis=1); sc = np.linalg.norm(yp + ym - 2 * y0[:, None], axis=1)
    return (d <= D_MIN) | (sc <= RHO_MAX * d)


def representar_all(evals, base='base'):
    """Todos os atributos implementados — SÓ para a verificação (etapaA_rep_check)."""
    return representar(evals, base, tipos=ATRIBUTOS)


def atomic_npy(path, arr):
    tmp = path + '.tmp%d.npy' % os.getpid(); np.save(tmp, arr); os.replace(tmp, path)


class EtapaAUnit:
    def __init__(self, hay, only=None, N=32, spacing=25.0, rec_mode='grade', so_theta=False, atol=1e-6, modelo='region',
                 cache_dir=None, vies_dir=None, apagar_brutos=False, theta_ref=None, referencia=False, rest_key_atol=None,
                 direcoes=None, amplitudes=None):
        """modelo: 'region' | 'hay'. cache_dir: repousos guardados (compartilhados). vies_dir: diretório das unidades 'hay'
        (a redução 'region' espera p_<ponto>.npz lá e calcula JᵀΔy). referencia: a rodada é uma REFERÊNCIA do viés (só 'base'; 'hay' sempre é); theta_ref: FATORES sobre
        θ_verd ({nome: fator}) — SÓ para o controle positivo do viés (o 'region' perturbado no papel de referência)."""
        self.hay = hay; self.rec_mode = rec_mode; self.so_theta = so_theta; self.atol = atol; self.modelo = modelo
        self.cache_dir = cache_dir; self.vies_dir = vies_dir; self.apagar = apagar_brutos
        self.only = only; self.C = None; self.is_ref = referencia or modelo == 'hay'; self.rest_key_atol = rest_key_atol
        # item 146: amplitudes POR PONTO ({ponto: {'M1': nA, 'M4': [nA, …]}}, do etapaA_condiciona_aval); sem arquivo → as globais M1/M4.
        # Com arquivo, o ponto TEM de estar nele (um nome errado não volta calado às amplitudes antigas).
        self.amps = json.load(open(amplitudes)) if amplitudes else None
        # item 113 (2): verificação direta — subpassos θ·exp(±h·v) ao longo de direções dadas (k × 30, unitárias, em log θ)
        # item 113 (2): .npy = direções com o passo h; item 121: .npz do etapaA_dir_rel = direções (V) com as excursões δ_i
        if direcoes is None: self.direcoes = self.excursoes = None
        elif str(direcoes).endswith('.npz'): z = np.load(direcoes); self.direcoes = z['V']; self.excursoes = z['excursoes']
        else: self.direcoes = np.load(direcoes); self.excursoes = np.full(len(self.direcoes), STEP)
        if modelo == 'hay':
            import etapaA_F as EF
            self.M = EF.HayRef(hay, HAY_DELTA); self.M.PTS = EM.grid_points(self.M.cell, spacing)
            self.grid = sorted(self.M.PTS, key=lambda k: (self.M.PTS[k]['dist'], k))
            self.site = {k: [(s, w) for s, w in self.M.at(self.M.PTS[k])] for k in self.grid}
        else:
            self.M = EM.RegionModel(hay, N, lambda c: EM.grid_points(c, spacing))
            if theta_ref:
                th = dict(EM.THETA_TRUE)
                for k, f in theta_ref.items(): th[k] *= f
                self.M.set_theta(th)
            self.theta_base = dict(self.M.theta)
            self.grid = sorted(self.M.PTS, key=lambda k: (self.M.PTS[k]['dist'], k))
            # NÓ de cada ponto, fixado UMA vez na geometria de base: injeção e leitura sempre no NÓ (item 69)
            self.site = {}
            for k in self.grid:
                q = max(self.M.at(self.M.PTS[k]), key=lambda x: x[1]); assert q[1] > 0.999, (k, q); self.site[k] = [(q[0], 1.0)]
            self.base_diam = {s: [seg.diam for seg in s] for s in self.M.secs}
            self.base_L = {s: s.L for s in self.M.secs}
            self.orig = {s: s.name().split('.')[-1].split('_x')[0] for s in self.M.secs}
            rng = np.random.default_rng(GEO_SEED); keys = sorted(set(self.orig.values()))
            self.geo = {}
            for i in range(30): self.geo['geo_d%02d' % i] = ('d', dict(zip(keys, rng.normal(0.0, 0.2, len(keys)))))
            for i in range(30): self.geo['geo_L%02d' % i] = ('L', dict(zip(keys, rng.normal(0.0, 0.02, len(keys)))))
            self.geo['geo_esc_mais'] = ('s', 1.01); self.geo['geo_esc_menos'] = ('s', 1 / 1.01)
        self.read = self.grid + ['soma']
        self.SOMA = [(self.M.SOMA, 1.0)]

    # ---------------------------------------------------------------- interface do runner
    def units(self):
        return ['p_' + k for k in (self.only or self.grid)]          # 'soma' = a unidade SOMÁTICA (M3/M5)

    def substeps(self, u):
        if self.is_ref: return ['base']
        if self.direcoes is not None:
            return ['base'] + ['dir%02d_%s' % (k, g) for k in range(len(self.direcoes)) for g in ('mais', 'menos')]
        th = ['base'] + ['%s_%s' % (n, sg) for n in EM.THETA_NAMES for sg in ('mais', 'menos')]
        if self.so_theta: return th
        return th + (['ganho'] if u == 'p_soma' else ['ganho', 'posicao']) + list(self.geo)

    def others(self, u):
        return [] if self.so_theta else (['ganho'] if u == 'p_soma' else ['ganho', 'posicao']) + list(self.geo)

    # ---------------------------------------------------------------- perturbações (só 'region')
    def _refresh(self):
        o = self.M.cell.apic[0](0)
        tips = [s for s in self.M.secs if self.M.region[s] == 'apical' and int(h.SectionRef(sec=s).nchild()) == 0]
        self.M.maxL = max(h.distance(o, s(1)) for s in tips)
        self.M.segd = {s: [h.distance(o, seg) for seg in s] for s in self.M.secs if self.M.region[s] == 'apical'}

    def _restore_geometry(self):
        if self.modelo != 'region': return
        for s in self.M.secs:
            if abs(s.L - self.base_L[s]) > 1e-12: s.L = self.base_L[s]
            for seg, d in zip(s, self.base_diam[s]): seg.diam = d

    def _apply(self, u, sname):
        if self.modelo != 'region': return 1.0
        th = dict(self.theta_base); gain = 1.0
        self._restore_geometry()
        if sname in self.geo:
            kind, v = self.geo[sname]
            for s in self.M.secs:
                if kind == 'd':
                    for seg, d in zip(s, self.base_diam[s]): seg.diam = max(0.1, d + v[self.orig[s]])
                elif kind == 'L':
                    s.L = self.base_L[s] * (1.0 + v[self.orig[s]])
                else:
                    for seg, d in zip(s, self.base_diam[s]): seg.diam = d * v
        elif sname == 'ganho':
            gain = 1.01
        elif sname == 'posicao':                                       # nó p deslocado +2 µm ao longo do ramo
            s_p = self.site[u[2:]][0][0].sec
            nxt = [c for c in s_p.children() if self.orig.get(c) == self.orig[s_p]]
            if nxt:
                s_p.L = self.base_L[s_p] + 2.0; nxt[0].L = max(0.1, self.base_L[nxt[0]] - 2.0)
            else:                                                       # ponto na ponta/fim de seção sem continuação
                s_p.L = self.base_L[s_p] + 2.0
        elif sname.startswith('dir') and self.direcoes is not None:            # item 113 (2) / 121: θ · exp(±δ_k·v)
            k, sg = int(sname[3:5]), sname.rsplit('_', 1)[1]; v = self.direcoes[k]; d = float(self.excursoes[k])
            for i, n in enumerate(EM.THETA_NAMES): th[n] = th[n] * math.exp((d if sg == 'mais' else -d) * v[i])
        elif sname != 'base':
            n, sg = sname.rsplit('_', 1); th[n] = th[n] * (1.01 if sg == 'mais' else 1 / 1.01)
        self._refresh(); self.M.set_theta(th)
        return gain

    # ---------------------------------------------------------------- simulação (CÓDIGO ÚNICO)
    def _sim(self, u):
        """CommonSim na 1ª avaliação (repouso + autotestes de código); nas seguintes, resettle (o modelo mudou)."""
        if self.C is None:
            h.v_init = -80.0
            sites = [seg for seg, w in (self.SOMA if u == 'p_soma' else self.site[u[2:]])]
            self.C = SC.CommonSim(self.M.SOMA, atol=self.atol, cache_dir=self.cache_dir, sites=sites, verbose=False, rest_key_atol=self.rest_key_atol)
            return 'construtor: ' + self.C.settle_info
        return self.C.resettle()

    def _run(self, stims, tstop, reads):
        """reads: lista de nomes (grade, 'soma'). Devolve (t, Y[len(reads), T]) — grade fixa DT, ou passos do CVode."""
        recs = {k: (self.SOMA if k == 'soma' else self.site[k]) for k in reads}
        t, o = self.C.run(stims, tstop, recs, rec_grid=None if self.rec_mode == 'passos' else DT)
        return t, np.array([o[k] for k in reads])

    def evaluate(self, u, sname, ud):
        t0 = time.time(); gain = self._apply(u, sname)
        try: info = self._sim(u)
        except SC.AutotestFailed as e:                                 # item 121: θ·exp(±δv) sem repouso estável → NÃO AVALIADA
            if not sname.startswith('dir'): raise                       # (só nos subpassos de direção; nos outros a regra é parar)
            self._restore_geometry()
            return {'nao_avaliado': np.array('repouso/autoteste: %s' % e), 't_repouso_s': np.array(time.time() - t0)}
        t1 = time.time()
        try: self.protocols(u, sname, ud, gain)
        except SC.SimulacaoAbortada as e:                                # item 157: guarda disparou → NÃO AVALIADO (não trava); traços parciais fora
            for f in os.listdir(ud):
                if f.startswith(sname + '.') and f.endswith('.npy'): os.remove(os.path.join(ud, f))
            self._restore_geometry()
            return {'nao_avaliado': np.array('guarda: %s' % e), 't_repouso_s': np.array(t1 - t0), 't_protocolos_s': np.array(time.time() - t1)}
        t2 = time.time(); self._restore_geometry()
        return {'t_repouso_s': np.array(t1 - t0), 't_protocolos_s': np.array(t2 - t1), 'repouso': np.array(info)}

    def protocols(self, u, sname, ud, gain):
        """Os protocolos da unidade a partir do repouso que o CommonSim tem AGORA (gravação atômica por arquivo). ITEM 101:
        traços em FLOAT64 (antes: float32 convertido ANTES de tirar a linha de base, em ~−75 mV → passo 7.6×10⁻⁶ mV, que
        virou o 'piso' da comparação entre tolerâncias)."""
        if u == 'p_soma':
            _, Y = self._run([('s', M3['delay'], M3['amp'] * gain, M3['dur'])], M3['tstop'], self.read)
            atomic_npy(os.path.join(ud, '%s.M3.npy' % sname), Y - Y[:, [pre_index('M3')]])
            Y5 = []
            for a in M5['amps']:
                _, y = self._run([('s', M5['delay'], a * gain, M5['dur'])], M5['tstop'], ['soma'])
                Y5.append(y[0] - y[0, pre_index('M5')])
            atomic_npy(os.path.join(ud, '%s.M5.npy' % sname), np.array(Y5))
        else:
            p = u[2:]; sp = self.site[p]; m1a, m4a = self._amps(p)
            if self.rec_mode == 'passos':
                for sgn, lab in ((-1, 'M1m'), (1, 'M1p')):
                    t, Y = self._run([('s', M1['delay'], sgn * m1a * gain, M1['dur'], sp)], M1['tstop'], self.read)
                    atomic_npy(os.path.join(ud, '%s.%s_t.npy' % (sname, lab)), t); atomic_npy(os.path.join(ud, '%s.%s_V.npy' % (sname, lab)), Y)
                for i, a in enumerate(m4a):
                    t, y = self._run([('a', M4['onset'], a * gain, M4['taud'], sp)], M4['tstop'], [p, 'soma'])
                    atomic_npy(os.path.join(ud, '%s.M4_%d_t.npy' % (sname, i)), t); atomic_npy(os.path.join(ud, '%s.M4_%d_V.npy' % (sname, i)), y)
            else:
                for sgn, lab in ((-1, 'M1m'), (1, 'M1p')):
                    _, Y = self._run([('s', M1['delay'], sgn * m1a * gain, M1['dur'], sp)], M1['tstop'], self.read)
                    atomic_npy(os.path.join(ud, '%s.%s.npy' % (sname, lab)), Y - Y[:, [pre_index(lab)]])
                Y4 = []
                for a in m4a:
                    _, y = self._run([('a', M4['onset'], a * gain, M4['taud'], sp)], M4['tstop'], [p, 'soma'])
                    Y4.append(y - y[:, [pre_index('M4')]])
                atomic_npy(os.path.join(ud, '%s.M4.npy' % sname), np.array(Y4))

    def _amps(self, p):
        """item 146: (amplitude do M1, amplitudes do M4) do ponto p."""
        if self.amps is None: return M1['amp'], tuple(M4['amps'])
        a = self.amps[p]; return float(a['M1']), tuple(float(x) for x in a['M4'])

    # ---------------------------------------------------------------- redução por ponto de leitura
    def ready_to_reduce(self, u):
        """item 89 (3): o trabalhador de vida longa não espera — sem a referência do viés, a redução fica para depois."""
        return self.is_ref or not self.vies_dir or os.path.exists(os.path.join(self.vies_dir, '%s.npz' % u))

    def _wait_vies(self, u):
        """A redução 'region' com vies_dir ESPERA a unidade 'hay' do mesmo ponto (os brutos só vivem até a redução)."""
        if not self.vies_dir: return None
        f = os.path.join(self.vies_dir, '%s.npz' % u); t0 = time.time()
        while not os.path.exists(f):
            if time.time() - t0 > 48 * 3600: raise RuntimeError('viés de %s não chegou em 48 h' % u)
            time.sleep(300)
        return os.path.join(self.vies_dir, u)

    def reduce(self, u, subs, ud, chunk=2):
        if self.direcoes is not None: return {'nota': np.array('verificação direta ao longo de direções (item 113) — análise à parte')}
        """ITEM 108 (1º): redução pelo CAMINHO ÚNICO de representação (`representar`: voltagem antes do 1º disparo sem o pé +
        tempos × |dV/dt|), com TODAS as avaliações da unidade juntas por leitura (θ ±, extras e a referência do viés) → as
        MESMAS amostras e os MESMOS disparos em todas; J, X e Δy saem das mesmas features. Blocos por leitura r (M1m + M1p, ou M3)
        e as leituras extras (M4: no ponto e no soma, 3 amplitudes cada; M5: soma, 3 amplitudes) somadas no bloco do seu local."""
        if self.is_ref: return {'nota': np.array('referência do viés por ponto (%s): só os traços base' % self.modelo)}
        vd = self._wait_vies(u)
        P = EM.THETA_NAMES; oth = self.others(u); nX = len(oth)
        keys = ['base'] + ['%s_%s' % (n, g) for n in P for g in ('mais', 'menos')] + oth + (['ref'] if vd else [])
        src = lambda k: (vd, 'base') if k == 'ref' else (ud, k)
        ld = lambda k, lab: np.load(os.path.join(src(k)[0], '%s.%s.npy' % (src(k)[1], lab)), mmap_mode='r')
        soma = u == 'p_soma'
        main, extra = (('M3',), 'M5') if soma else (('M1m', 'M1p'), 'M4')
        nR = len(self.read); nE = 1 if soma else 2
        JtJ = np.zeros((nR + nE, 30, 30)); JtX = np.zeros((nR + nE, 30, nX)); XtX = np.zeros((nR + nE, nX)); JtDy = np.zeros((nR + nE, 30))
        # item 111: os MESMOS blocos só com as linhas LINEARES (máscara de linhas) → especificação (i) conservadora; os completos → (ii)
        JtJl = np.zeros_like(JtJ); JtXl = np.zeros_like(JtX); XtXl = np.zeros_like(XtX); JtDyl = np.zeros_like(JtDy)
        n_disp = np.zeros(nR + nE, int); t_ok = np.ones(nR + nE, bool); n_lin = np.zeros(nR + nE, int); n_tot = np.zeros(nR + nE, int)

        def acc(b, F):
            yp = np.stack([F['%s_mais' % n] for n in P], axis=1); ym = np.stack([F['%s_menos' % n] for n in P], axis=1)
            J = (yp - ym) / (2 * STEP); m = linhas_lineares(F['base'], yp, ym); Jl = J[m]
            JtJ[b] += J.T @ J; JtJl[b] += Jl.T @ Jl; n_lin[b] += int(m.sum()); n_tot[b] += len(m)
            if nX:
                X = np.stack([F[o] - F['base'] for o in oth], axis=1); JtX[b] += J.T @ X; XtX[b] += (X * X).sum(0)
                JtXl[b] += Jl.T @ X[m]; XtXl[b] += (X[m] * X[m]).sum(0)
            if vd:
                dy = F['ref'] - F['base']; JtDy[b] += J.T @ dy; JtDyl[b] += Jl.T @ dy[m]

        for c0 in range(0, nR, chunk):
            rr = list(range(c0, min(nR, c0 + chunk))); fl = {}
            for lab in main:
                fl[lab], inf = representar({k: cadeia(ld(k, lab)[rr], lab) for k in keys})
                for j, r in enumerate(rr): n_disp[r] += inf['n_disparos'][j]; t_ok[r] &= inf['tempos_ok'][j] or not inf['n_disparos'][j]
            for j, r in enumerate(rr):
                acc(r, {k: np.concatenate([fl[lab][k][j] for lab in main]) for k in keys})
        shp = ld('base', extra).shape; R = int(np.prod(shp[:-1]))
        ev = {k: cadeia(np.asarray(ld(k, extra)).reshape(R, -1), extra) for k in keys}
        f, inf = representar(ev)
        for j in range(R):
            b = nR + (0 if soma else j % 2)                       # M4: linha = amplitude·2 + local (0 = p, 1 = soma)
            acc(b, {k: f[k][j] for k in keys}); n_disp[b] += inf['n_disparos'][j]; t_ok[b] &= inf['tempos_ok'][j] or not inf['n_disparos'][j]
        out = {'JtJ': JtJ, 'JtX': JtX, 'XtX': XtX, 'colunas_X': np.array(oth), 'disparos_base': n_disp, 'tempos_ok': t_ok,
               'JtJ_lin': JtJl, 'JtX_lin': JtXl, 'XtX_lin': XtXl, 'linhas_lineares': n_lin, 'linhas_total': n_tot,
               'leituras': np.array(self.read + (['M5@soma'] if soma else ['M4@p', 'M4@soma'])), 'representacao': np.array('item 108')}
        if vd: out['JtDy'] = JtDy; out['JtDy_lin'] = JtDyl
        out['t_repouso_s'] = np.array([float(subs[s]['t_repouso_s']) for s in subs]); out['t_protocolos_s'] = np.array([float(subs[s]['t_protocolos_s']) for s in subs])
        return out

    def after_reduce(self, u, ud):
        """--apagar-brutos: os traços (~6 GB por unidade distal) saem DEPOIS da redução gravada; ficam os .npz dos tempos."""
        if not self.apagar: return
        for f in os.listdir(ud):
            if f.endswith('.npy'): os.remove(os.path.join(ud, f))
