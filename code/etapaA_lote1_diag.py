# etapaA_lote1_diag.py — D132 item 162: TRÊS ANÁLISES DO LOTE 1 SEM SIMULAR, a partir dos ACUMULADOS por unidade (σ*, σ_lin pelas MESMAS fórmulas do
# etapaA_piloto). Conferência ANTES (resposta conhecida): reproduzir EXATAMENTE piloto_fis.json do lote 1 ("acum", 10 distais + somática) e do piloto
# condicionado ("6inj", acumulados do regr154 nas direções do piloto).
#   (1) nível certificado min(σ_lin, σ*) por modelo de ruído: piloto-6 → lote 1-11;
#   (2) decomposição do salto do σ*: (a) o subconjunto das 6 injeções NAS DIREÇÕES e na CONTABILIDADE do lote 1 → parte "contabilidade" × parte "dados novos"
#       (em escala log); (b) a direção que dominava a variância da componente limitante no piloto e quanto dela está no subespaço resolvido pela faixa no
#       lote 1; (c) autoconsistência do conjunto resolvido pela faixa (o raio usa σ*; σ* depende de quais saem): novas candidatas com o σ* depois da regra;
#   (3) σ_lin tirando CADA unidade nova por vez; parte de cada unidade na energia da aceleração ao longo de v_3 (Σ‖a‖², AA) e σ_lin de v_3 da unidade sozinha.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_lote1_diag.py <saida.json>
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU
import etapaA_sstar as S

AQ = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQ, 'results'); OUT = sys.argv[1]
NP = 30; F = 1.4591; Z = 1.645; TAUS = ('0.0', '1.0', '10.0', '50.0'); TT = (0.0, 1.0, 10.0, 50.0)
zg = np.load(os.path.join(RES, 'etapaA_G8', 'G.npz'), allow_pickle=True); nomes = [str(x) for x in zg['nomes']]; tl = [S.tol_of(x) for x in nomes]
use = [i for i, t in enumerate(tl) if t is not None and zg['condicionado'][i] and np.all(np.isfinite(zg['G'][i]))]
Gf = zg['G'][use]; tol = np.array([tl[i][1] * abs(zg['F0'][i]) if tl[i][0] == 'rel' else tl[i][1] for i in use]); NOM = [nomes[i] for i in use]
PC = ['g_apic[60]_32', 'g_apic[36]_16', 'g_apic[9]_16', 'g_apic[44]_48', 'g_apic[64]_48']; NOV = ['g_apic[70]_48', 'g_apic[77]_48', 'g_apic[37]_32', 'g_apic[19]_16', 'g_apic[17]_16']


def contab(d):
    """Direções, excursões e o conjunto DETERMINADO pela faixa (Fdir) de um arquivo de direções."""
    z = np.load(os.path.join(d, 'direcoes.npz')); V = z['V']; IDX = [int(i) + 1 for i in z['indices']]
    fd = json.load(open(os.path.join(d, 'Fdir.json')))['direcoes']; DET = [int(n[2:]) for n, r in fd.items() if r['veredito'].startswith('DENTRO')]
    TEST = [int(n[2:]) for n in fd]; qdet = [q for q in range(len(IDX)) if IDX[q] in DET]
    return {'V': V, 'IDX': IDX, 'DET': DET, 'TEST': TEST, 'qdet': qdet, 'sigma': z['sigma'], 'B': base(V, qdet)}


def base(V, qdet):
    Pc = np.eye(NP) - sum((np.outer(V[q], V[q]) for q in qdet), np.zeros((NP, NP))); w, U = np.linalg.eigh(Pc); return U[:, w > 0.5]


def acc(pref):
    z = np.load(pref + '.fis.npz'); return {t: (z['G_%g' % tt], z['JA_%g' % tt], z['AA_%g' % tt]) for t, tt in zip(TAUS, TT)}


def sigma_estrela(Gc, B):
    Gq = B.T @ Gc @ B; gb = Gf @ B; sF = np.sqrt(np.einsum('gi,ij,gj->g', gb, np.linalg.inv(Gq), gb)); xs = tol / (Z * sF); i = int(np.argmin(xs))
    return float(xs[i]), NOM[i], i


def sigma_lin(C, A, membros, t, so_q=None):
    Gd = sum(A[m][t][0] for m in membros); JA = sum(A[m][t][1] for m in membros); AA = sum(A[m][t][2] for m in membros); V = C['V']; out = []
    for q in range(len(C['IDX'])):
        if q in C['qdet'] or (so_q is not None and q != so_q): continue
        out.append((EU.sigma_lin(EU.curvaturas(Gd, JA[q], AA[q], float(V[q] @ Gd @ V[q]))[0], NP, F), C['IDX'][q]))
    return min(out)


def conjunto(C, A, AS, membros):
    r = {}
    for t in TAUS:
        Gc = sum(A[m][t][0] for m in membros) + AS[t][0]; ss, lim, _ = sigma_estrela(Gc, C['B']); sl = sigma_lin(C, A, membros, t)
        r[t] = {'sigma_estrela': ss, 'limitante': lim, 'sigma_lin': sl[0], 'v_lin': sl[1], 'certificado': min(ss, sl[0])}
    return r


L1 = os.path.join(RES, 'etapaA_lotes', 'lote1'); PCd = os.path.join(RES, 'etapaA_pcond'); RG = os.path.join(RES, 'etapaA_lotes', 'regr154')
C1, Cp = contab(L1), contab(PCd)
A1 = {u: acc(os.path.join(L1, 'acc_' + u)) for u in PC + NOV}; S1 = acc(os.path.join(L1, 'acc_soma'))
Ap = {u: acc(os.path.join(RG, 'acc_' + u)) for u in PC}; Sp = acc(os.path.join(RG, 'acc_soma'))
res = {}
# ---- conferências (resposta conhecida)
l1 = conjunto(C1, A1, S1, PC + NOV); p6 = conjunto(Cp, Ap, Sp, PC)
J1 = json.load(open(os.path.join(L1, 'piloto_fis.json')))['conjuntos']['acum']; Jp = json.load(open(os.path.join(PCd, 'piloto_fis.json')))['conjuntos']['6inj']
ok1 = all(l1[t]['sigma_estrela'] == J1[t]['sigma_estrela'] and l1[t]['sigma_lin'] == J1[t]['sigma_lin'] for t in TAUS)
okp = all(p6[t]['sigma_estrela'] == Jp[t]['sigma_estrela'] and p6[t]['sigma_lin'] == Jp[t]['sigma_lin'] for t in TAUS)
print('CONFERÊNCIA: lote 1 (11) reproduz piloto_fis.json do lote 1: %s | piloto-6 reproduz piloto_fis.json do piloto: %s' % ('EXATO' if ok1 else 'DIFERENTE', 'EXATO' if okp else 'DIFERENTE'))
res['conferencias'] = {'lote1': ok1, 'piloto6': okp}
assert ok1 and okp, 'as fórmulas não reproduzem os resultados gravados — nada adiante vale'
nm = lambda t: 'iid' if t == '0.0' else 'OU %g ms' % float(t)
# ---- (1) nível certificado
print('\n(1) NÍVEL CERTIFICADO = min(σ_lin, σ*) [mV]:'); res['certificado'] = {}
for t in TAUS:
    a, b = p6[t]['certificado'], l1[t]['certificado']; res['certificado'][t] = {'piloto6': a, 'lote1': b, 'experimento_max': max(a, b)}
    print('   %-9s piloto-6 %.3g → lote 1 %.3g | do EXPERIMENTO (máximo entre os desenhos) %.3g (%s)' % (nm(t), a, b, max(a, b), 'lote 1' if b >= a else 'piloto-6'))
# ---- (2a) decomposição
s6 = conjunto(C1, A1, S1, PC); res['seis_na_contabilidade_do_lote1'] = s6
print('\n(2a) DECOMPOSIÇÃO DO SALTO (escala log; contabilidade = mesmos 6, direções/faixa do lote 1; dados novos = 6 → 11 na mesma contabilidade):'); res['decomposicao'] = {}
for t in TAUS:
    for k in ('sigma_estrela', 'sigma_lin'):
        a, m, b = p6[t][k], s6[t][k], l1[t][k]; J = math.log(b / a); Ac = math.log(m / a); D = math.log(b / m)
        res['decomposicao'].setdefault(t, {})[k] = {'piloto6': a, 'seis_L1': m, 'onze_L1': b, 'fator_total': b / a, 'fator_contab': m / a, 'fator_dados': b / m,
                                                    'frac_contab': Ac / J if J else None}
        print('   %-9s %-13s piloto-6 %-8.3g → 6 na contab. do lote 1 %-8.3g → 11 %-8.3g | ×%.2f = contabilidade ×%.2f · dados novos ×%.2f%s' % (nm(t), k.replace('sigma_estrela', 'σ*').replace('sigma_lin', 'σ_lin'),
              a, m, b, b / a, m / a, b / m, '' if not J else ' (%.0f%% do log pela contabilidade)' % (100 * Ac / J)))
# ---- (2b) direção que dominava a variância da componente limitante no piloto
print('\n(2b) DIREÇÃO QUE DOMINAVA A VARIÂNCIA DA COMPONENTE LIMITANTE (piloto-6, contabilidade do piloto):'); res['dominante_piloto'] = {}
Pdet1 = sum((np.outer(C1['V'][q], C1['V'][q]) for q in C1['qdet']), np.zeros((NP, NP)))
for t in TAUS:
    Gc = sum(Ap[m][t][0] for m in PC) + Sp[t][0]; ss, lim, i = sigma_estrela(Gc, Cp['B']); B = Cp['B']; gb = Gf[i] @ B
    lam, U = np.linalg.eigh(B.T @ Gc @ B); c = (gb @ U) ** 2 / lam; k = int(np.argmax(c)); w = B @ U[:, k]; w /= np.linalg.norm(w)
    ov_p = np.abs(Cp['V'] @ w); qp = int(np.argmax(ov_p)); fr_det1 = float(w @ Pdet1 @ w); ov_1 = np.abs(C1['V'] @ w); q1 = int(np.argmax(ov_1))
    res['dominante_piloto'][t] = {'limitante': lim, 'fracao_variancia': float(c[k] / c.sum()), 'parecida_com_piloto': 'v_%d' % Cp['IDX'][qp], 'sobreposicao_piloto': float(ov_p[qp]),
                                  'fracao_no_resolvido_pela_faixa_lote1': fr_det1, 'parecida_com_lote1': 'v_%d' % C1['IDX'][q1], 'sobreposicao_lote1': float(ov_1[q1]),
                                  'resolvida_no_lote1': C1['IDX'][q1] in C1['DET']}
    print('   %-9s %s: %.0f%% da variância numa direção ≈ v_%d do piloto (|cos| %.2f); no lote 1: %.0f%% dela no subespaço RESOLVIDO pela faixa; mais parecida com v_%d do lote 1 (|cos| %.2f, %s)' % (
          nm(t), lim, 100 * c[k] / c.sum(), Cp['IDX'][qp], ov_p[qp], 100 * fr_det1, C1['IDX'][q1], ov_1[q1], 'RESOLVIDA pela faixa' if C1['IDX'][q1] in C1['DET'] else 'NÃO resolvida'))
# ---- (2c) autoconsistência do conjunto resolvido pela faixa
print('\n(2c) AUTOCONSISTÊNCIA (raio em σ* iid; regra do item 132: além do fator 2 E funcional DENTRO → resolvida):'); res['ponto_fixo'] = {}
for rot, C, A, AS, mem in (('piloto-6', Cp, Ap, Sp, PC), ('lote 1', C1, A1, S1, PC + NOV)):
    Gc = sum(A[m]['0.0'][0] for m in mem) + AS['0.0'][0]; s_pre, _, _ = sigma_estrela(Gc, np.eye(NP)); s_pos, _, _ = sigma_estrela(Gc, C['B'])
    mx = np.abs(C['V']).max(1); alem = lambda s: [C['IDX'][q] for q in range(len(C['IDX'])) if s * math.sqrt(NP * F) / C['sigma'][q] * mx[q] > EU.TETO_LOG]
    a_pre, a_pos = alem(s_pre), alem(s_pos); novas = [d for d in a_pos if d not in C['TEST']]
    # cadeia OTIMISTA: se TODAS as novas candidatas fossem resolvidas (funcional DENTRO), até parar
    det = list(C['DET']); s_o = s_pos; cadeia = []
    while True:
        cand = [d for d in alem(s_o) if d not in C['TEST'] and d not in det]
        if not cand: break
        det += cand; qd = [q for q in range(len(C['IDX'])) if C['IDX'][q] in det]; s_o, _, _ = sigma_estrela(Gc, base(C['V'], qd)); cadeia.append((cand, s_o))
    res['ponto_fixo'][rot] = {'sigma_iid_sem_regra': s_pre, 'sigma_iid_com_regra': s_pos, 'alem_pre': a_pre, 'testadas': C['TEST'], 'resolvidas': C['DET'],
                              'alem_com_sigma_pos': a_pos, 'novas_candidatas': novas, 'cadeia_otimista': [{'novas': c, 'sigma_iid': s} for c, s in cadeia]}
    print('   %-9s σ* iid sem regra %.3g → além do fator 2: %s (testadas no funcional; resolvidas %s) → σ* iid com regra %.3g → além com ESSE σ*: %s → NOVAS candidatas não testadas: %s%s' % (
          rot, s_pre, a_pre, C['DET'], s_pos, a_pos, novas or 'nenhuma (PONTO FIXO)',
          '' if not cadeia else ' | cadeia OTIMISTA (se todas resolvidas): ' + ' → '.join('%s → σ* iid %.3g' % (c, s) for c, s in cadeia)))
# ---- (2c') o que está EM JOGO nas candidatas novas: σ* em TODOS os modelos de ruído se elas fossem resolvidas (otimista)
print("\n(2c') σ* SE AS CANDIDATAS NOVAS FOSSEM RESOLVIDAS (otimista; só o funcional ao longo delas decide):"); res['em_jogo'] = {}
for rot, C, A, AS, mem in (('piloto-6', Cp, Ap, Sp, PC), ('lote 1', C1, A1, S1, PC + NOV)):
    nv = res['ponto_fixo'][rot]['novas_candidatas']
    if not nv: continue
    qd = [q for q in range(len(C['IDX'])) if C['IDX'][q] in C['DET'] + nv]; Bo = base(C['V'], qd); linha = []
    for t in TAUS:
        Gc = sum(A[m][t][0] for m in mem) + AS[t][0]; s0, _, _ = sigma_estrela(Gc, C['B']); s1, l1_, _ = sigma_estrela(Gc, Bo)
        res['em_jogo'].setdefault(rot, {})[t] = {'atual': s0, 'otimista': s1, 'limitante_otimista': l1_}; linha.append('%s %.3g → %.3g' % (nm(t), s0, s1))
    print('   %-9s novas %s: %s' % (rot, nv, ' | '.join(linha)))
# ---- (3) curvatura em v_3: sem cada unidade nova
q3 = C1['IDX'].index(3); print('\n(3) CURVATURA AO LONGO DE v_3 (lote 1): σ_lin tirando cada unidade nova; parte de cada unidade em Σ‖a‖² ao longo de v_3:'); res['sem_cada'] = {}
for t in TAUS:
    base_all = sigma_lin(C1, A1, PC + NOV, t); v3_all = sigma_lin(C1, A1, PC + NOV, t, so_q=q3)[0]; tot = sum(A1[u][t][2][q3] for u in PC + NOV)
    linha = []
    for u in NOV:
        mem = [m for m in PC + NOV if m != u]; sl = sigma_lin(C1, A1, mem, t); v3 = sigma_lin(C1, A1, mem, t, so_q=q3)[0]
        Gc = sum(A1[m][t][0] for m in mem) + S1[t][0]; ss, _, _ = sigma_estrela(Gc, C1['B']); so = sigma_lin(C1, A1, [u], t, so_q=q3)[0]
        res['sem_cada'].setdefault(t, {})[u] = {'sigma_lin': sl[0], 'v_lin': sl[1], 'sigma_lin_v3': v3, 'sigma_estrela': ss, 'parte_AA_v3': float(A1[u][t][2][q3] / tot), 'sigma_lin_v3_sozinha': so}
        linha.append('%s: σ_lin %.3g (v_%d), v_3 %.3g, σ* %.3g, %.0f%% de Σ‖a‖²(v_3), sozinha %.3g' % (u, sl[0], sl[1], v3, ss, 100 * A1[u][t][2][q3] / tot, so))
    pc_part = sum(A1[u][t][2][q3] for u in PC) / tot
    res['sem_cada'][t]['_todas'] = {'sigma_lin': base_all[0], 'v_lin': base_all[1], 'sigma_lin_v3': v3_all, 'parte_AA_v3_das_6_do_piloto': float(pc_part)}
    print('   %-9s TODAS: σ_lin %.3g (v_%d), v_3 %.3g; as 5 do piloto têm %.0f%% de Σ‖a‖²(v_3)' % (nm(t), base_all[0], base_all[1], v3_all, 100 * pc_part))
    for l in linha: print('      sem ' + l)
json.dump(res, open(OUT, 'w'), indent=1, default=float)
