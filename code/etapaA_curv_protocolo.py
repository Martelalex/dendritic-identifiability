# etapaA_curv_protocolo.py — D132 item 163 (3): QUEM TRAZ A CURVATURA AO LONGO DE v_3 DO LOTE 1 — por UNIDADE e por PROTOCOLO (M1m, M1p, M4).
# As 5 unidades do piloto refeitas só em v_3 ± (acumulados POR PROTOCOLO, curv_v3/acc_<u>.<var>.<lab>.npz); as 5 novas pelos acumulados do lote 1.
# Decomposição EXATA da curvatura intrínseca (soma por linhas): c = G⁺ Jᵀa do conjunto (as 10 distais, como o σ_lin); por parte p (linhas de um protocolo
# de uma unidade):  E_p = aᵀa_p − 2 cᵀ (Jᵀa)_p + cᵀ G_p c = ‖a_p − J_p c‖² ≥ 0,  Σ_p E_p = ‖a_N‖² (a do etapaA_unit.curvaturas). Por parte também: aᵀa
# (aceleração bruta), vᵀG_p v (VELOCIDADE ao longo de v_3) e σ_lin(v_3) SEM a parte.
# CONFERÊNCIAS antes (resposta conhecida): (0) sintético: Σ E_p = aᵀa − (Jᵀa)ᵀG⁺(Jᵀa) e E_p ≥ 0; (1) σ_lin(v_3) das 10 pelos acumulados do lote 1 = o do
# item 162 (diag_lote1.json, código independente); (2) soma dos protocolos = total de cada unidade refeita; (3) variante SEM faixa ("inf": sem máscara) — a
# rodada refeita REPRODUZ os acumulados do lote 1 ao longo de v_3 (mesmo θ, mesmas amplitudes, mesma cache). Na variante COM faixa ("fis"), a máscara de
# uma linha usa TODAS as avaliações da rodada (25 direções no lote 1, só v_3 aqui) → diferença REPORTADA (não é erro).
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_curv_protocolo.py <saida.json>
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU

AQ = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQ, 'results'); OUT = sys.argv[1]
NP = 30; F = 1.4591; TAUS = ('0', '1', '10', '50'); LABS = ('M1m', 'M1p', 'M4')
L1 = os.path.join(RES, 'etapaA_lotes', 'lote1'); CV = os.path.join(L1, 'curv_v3')
PC = ['g_apic[60]_32', 'g_apic[36]_16', 'g_apic[9]_16', 'g_apic[44]_48', 'g_apic[64]_48']; NOV = ['g_apic[70]_48', 'g_apic[77]_48', 'g_apic[37]_32', 'g_apic[19]_16', 'g_apic[17]_16']
nm = lambda t: 'iid' if t == '0' else 'OU %s ms' % t


def coef(G, JA):
    w, U = np.linalg.eigh(G); k = w > 0; return U[:, k] @ ((U[:, k].T @ JA) / w[k])


def energia(c, Gp, JAp, AAp): return float(AAp - 2 * c @ JAp + c @ Gp @ c)


def slin(G, JA, AA, v): return EU.sigma_lin(EU.curvaturas(G, JA, AA, float(v @ G @ v))[0], NP, F)


res = {'conferencias': {}}
# (0) sintético: identidade da decomposição
rng = np.random.default_rng(1630); pior = 0.0; neg = 0.0
for _ in range(200):
    parts = [(rng.normal(size=(int(rng.integers(5, 40)), NP)), None) for _ in range(5)]; parts = [(J, rng.normal(size=len(J))) for J, _ in parts]
    G = sum(J.T @ J for J, _ in parts); JA = sum(J.T @ a for J, a in parts); AA = sum(float(a @ a) for _, a in parts); c = coef(G, JA)
    E = [energia(c, J.T @ J, J.T @ a, float(a @ a)) for J, a in parts]; n2 = AA - float(JA @ np.linalg.solve(G, JA))
    pior = max(pior, abs(sum(E) / n2 - 1)); neg = min(neg, min(E) / AA)
ok0 = pior < 1e-9 and neg > -1e-12; res['conferencias']['sintetico'] = {'pior_rel': pior, 'menor_E_rel': neg, 'ok': ok0}
print('(0) SINTÉTICO: Σ E_p = ‖a_N‖² (pior %.1e) e E_p ≥ 0 (menor %.1e) → %s' % (pior, neg, 'OK' if ok0 else 'FALHOU'), flush=True); assert ok0

z1 = np.load(os.path.join(L1, 'direcoes.npz')); IDX = [int(i) + 1 for i in z1['indices']]; q3 = IDX.index(3); v3 = z1['V'][q3]
zc = np.load(os.path.join(CV, 'direcoes_v3.npz')); assert np.array_equal(zc['V'][0], v3) and zc['excursoes'][0] == z1['excursoes'][q3] and int(zc['indices'][0]) == 2


def lote1(u, var):
    z = np.load(os.path.join(L1, 'acc_%s.%s.npz' % (u, var))); return {t: (z['G_' + t], z['JA_' + t][q3], z['AA_' + t][q3]) for t in TAUS}   # np.float64: soma IEEE simples


def refeito(u, var, lab=None):
    z = np.load(os.path.join(CV, 'acc_%s.%s%s.npz' % (u, var, '' if lab is None else '.' + lab)))
    assert json.loads(str(z['meta']))['sha256_direcoes'] == json.load(open(os.path.join(CV, 'acc_%s.ok.json' % u)))['sha256_direcoes']
    return {t: (z['G_' + t], z['JA_' + t][0], z['AA_' + t][0]) for t in TAUS}


# (1) σ_lin(v_3) das 10 pelos acumulados do lote 1 = item 162 (somas dos VETORES inteiros, como no etapaA_piloto; o sum() do Python ≥ 3.12 COMPENSA somas de
#     float — diferença ~1e-11 relativa — por isso os aᵀa ficam np.float64)
D = json.load(open(os.path.join(L1, 'diag_lote1.json')))['sem_cada']; ok1 = True
for t in TAUS:
    Z = [np.load(os.path.join(L1, 'acc_%s.fis.npz' % u)) for u in PC + NOV]
    s = slin(sum(z['G_' + t] for z in Z), sum(z['JA_' + t] for z in Z)[q3], sum(z['AA_' + t] for z in Z)[q3], v3); r = D['%s.0' % t]['_todas']['sigma_lin_v3']
    ok1 &= s == r
res['conferencias']['sigma_lin_v3_item162'] = bool(ok1); print('(1) σ_lin(v_3) das 10 (acumulados do lote 1) = item 162: %s' % ('EXATO' if ok1 else 'DIFERENTE'), flush=True); assert ok1

for var in ('fis', 'inf'):
    R = res.setdefault(var, {}); NOVA = {u: lote1(u, var) for u in NOV}; PCL = {u: lote1(u, var) for u in PC}
    TOT = {u: refeito(u, var) for u in PC}; LAB = {(u, l): refeito(u, var, l) for u in PC for l in LABS}
    # (2) soma dos protocolos = total
    d2 = max(float(np.max(np.abs(sum(np.atleast_1d(LAB[(u, l)][t][i]) for l in LABS) - np.atleast_1d(TOT[u][t][i]))) / max(np.max(np.abs(np.atleast_1d(TOT[u][t][i]))), 1e-300))
             for u in PC for t in TAUS for i in range(3))
    # (3) refeita × lote 1 ao longo de v_3 (por unidade do piloto)
    rep = {u: {t: {'G': float(np.abs(TOT[u][t][0] - PCL[u][t][0]).max() / np.abs(PCL[u][t][0]).max()), 'JA': float(np.abs(TOT[u][t][1] - PCL[u][t][1]).max() / max(np.abs(PCL[u][t][1]).max(), 1e-300)),
                   'AA': abs(TOT[u][t][2] / PCL[u][t][2] - 1) if PCL[u][t][2] else None} for t in TAUS} for u in PC}
    pior3 = max(max(x['G'], x['JA'], x['AA'] or 0) for u in PC for x in rep[u].values())
    R['conferencias'] = {'soma_protocolos_dif_rel': d2, 'refeita_vs_lote1_pior_rel': pior3, 'refeita_vs_lote1': rep}
    print('\n[%s] (2) Σ protocolos × total: dif. relativa máx %.1e → %s | (3) refeita × lote 1 ao longo de v_3: pior dif. relativa %.2e%s' % (
          var, d2, 'CONFERE' if d2 < 1e-9 else 'NÃO CONFERE', pior3, ' → REPRODUZ' if pior3 < 1e-6 else (' → a máscara usa todas as avaliações (esperado na variante com faixa)' if var == 'fis' else ' → NÃO REPRODUZ')), flush=True)
    assert d2 < 1e-9
    # decomposição no conjunto HÍBRIDO (5 novas do lote 1 + 5 do piloto refeitas, por protocolo)
    for t in TAUS:
        parts = {('%s' % u, 'toda'): NOVA[u][t] for u in NOV}; parts.update({(u, l): LAB[(u, l)][t] for u in PC for l in LABS})
        G = sum(p[0] for p in parts.values()); JA = sum(p[1] for p in parts.values()); AA = sum(p[2] for p in parts.values()); c = coef(G, JA)
        n2 = AA - float(JA @ coef(G, JA)); vel = float(v3 @ G @ v3); s_all = slin(G, JA, AA, v3)
        s_l1 = slin(sum(A[t][0] for A in list(NOVA.values()) + list(PCL.values())), sum(A[t][1] for A in list(NOVA.values()) + list(PCL.values())),
                    sum(A[t][2] for A in list(NOVA.values()) + list(PCL.values())), v3)
        E = {k: energia(c, *p) for k, p in parts.items()}; sE = sum(E.values())
        linhas = {}
        for k, p in parts.items():
            linhas['%s|%s' % k] = {'frac_aceleracao_aa': p[2] / AA, 'frac_curv_normal': E[k] / sE, 'frac_velocidade': float(v3 @ p[0] @ v3) / vel,
                                   'sigma_lin_v3_sem': slin(G - p[0], JA - p[1], AA - p[2], v3)}
        R[t] = {'sigma_lin_v3_hibrido': s_all, 'sigma_lin_v3_lote1': s_l1, 'K_N': math.sqrt(max(n2, 0)) / vel, 'soma_E_sobre_aN2': sE / n2, 'partes': linhas}
        print('  %-9s σ_lin(v_3): híbrido %.4g (lote 1: %.4g) | Σ E_p/‖a_N‖² = %.12f' % (nm(t), s_all, s_l1, sE / n2), flush=True)
        print('     %-22s %9s %9s %9s %12s' % ('parte', 'aᵀa', 'curv. N', 'veloc.', 'σ_lin sem'))
        for k in sorted(linhas, key=lambda k: -linhas[k]['frac_curv_normal'])[:8]:
            x = linhas[k]; print('     %-22s %8.1f%% %8.1f%% %8.1f%% %12.4g' % (k, 100 * x['frac_aceleracao_aa'], 100 * x['frac_curv_normal'], 100 * x['frac_velocidade'], x['sigma_lin_v3_sem']))
        porlab = {l: sum(linhas['%s|%s' % (u, l)]['frac_curv_normal'] for u in PC) for l in LABS}; poru = {u: sum(linhas['%s|%s' % (u, l)]['frac_curv_normal'] for l in LABS) for u in PC}
        R[t]['por_protocolo_curv_normal'] = porlab; R[t]['por_unidade_piloto_curv_normal'] = poru
        print('     por protocolo (5 do piloto): %s | por unidade: %s' % (' '.join('%s %.1f%%' % (l, 100 * v) for l, v in porlab.items()), ' '.join('%s %.1f%%' % (u, 100 * v) for u, v in poru.items())))
json.dump(res, open(OUT, 'w'), indent=1, default=float)
