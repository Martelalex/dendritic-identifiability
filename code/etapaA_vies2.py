# etapaA_vies2.py — D132 item 167 (prompt 0003): VIÉS DE SEGUNDA ORDEM COMPLETO de F̂ = F(θ̂) (implementação DECLARADA no item 167 antes de rodar), sem simular.
# Ao longo de v_3 (como o K8-v3: modelo de dados quadrático EXATO a partir de J, Jᵀa_3, aᵀa_3 medidos):
#   viés(F̂_g) ≈ g_Bᵀ b_β + ½ h_g σ² q,  b_β = −(σ²/2) M⁻¹ BᵀJA_3 q,  q = v_3ᵀB M⁻¹ Bᵀv_3,  M = BᵀG_τB   (Box 1971 + termo do funcional)
#   h_g = (F₊ + F₋ − 2F₀)/δ² das avaliações GRAVADAS do funcional em θ·exp(±δ v_3) (Gdir do desenho; δ grande → estimativa grosseira); contagem que muda → NaN.
# Monte Carlo (2000 ajustes; mesmo modelo do K8-v3 + funcional quadrático nas 3 componentes): viés e cobertura de F(θ̂) e do estimador CORRIGIDO
#   F̂_c = F(θ̂) − [∇F(θ̂)ᵀ b_β(θ̂) + ½ h σ² q(θ̂)] (correção em θ̂, σ conhecido). Cada desenho no SEU nível certificado (PONTO_FIXO.json), 4 modelos de ruído.
# Conferência: |MC − fórmula| ≤ 3 EP do MC ou ≤ 20% da fórmula. Leitura (do prompt): sobre o viés COMPLETO do MC.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_vies2.py <saida.json>
import sys, os, json, math
import numpy as np
from scipy.optimize import least_squares
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_relevancia_caburst as RC

NFIT = 2000; COMP = ['CaBurst_PA1', 'BAC_PA2', 'EPSP_apical_ponta']; IC = [RC.NOM.index(c) for c in COMP]; res = {'nfit': NFIT, 'desenhos': {}}
FALHA_CONF = []


def curvatura_funcional(d):
    z = np.load(os.path.join(d, 'dirF.npz')); q = [int(i) + 1 for i in z['indices']].index(3); dl = float(z['excursoes'][q])
    G = os.path.join(d, 'Gdir', 'G'); b, m, n = (np.load(os.path.join(G, f), allow_pickle=True) for f in ('base.npz', 'dir%02d_mais.npz' % q, 'dir%02d_menos.npz' % q))
    nomes = [str(x) for x in b['nomes']]; h = {}
    for c in COMP:
        i = nomes.index(c); cont = i < len(b['contagens']) and not (int(b['contagens'][i]) == int(m['contagens'][i]) == int(n['contagens'][i]))
        v = (float(m['F'][i]) + float(n['F'][i]) - 2 * float(b['F'][i])) / dl ** 2
        h[c] = float('nan') if (cont or not math.isfinite(v)) else v
    return h, dl, z['V'][q]


for D in RC.desenhos():
    cj = '6inj' if D['rot'] == 'piloto-6' else 'acum'; h, dl, vF = curvatura_funcional(D['d']); q3 = D['IDX'].index(3); v3 = D['V'][q3]
    assert np.allclose(vF, v3), 'v_3 do Gdir ≠ v_3 do conjunto relevante'
    e = RC.estado(D, False); qdet = [q for q in D['qs'] if D['IDX'][q] in e['DET']]; B = RC.base(D['V'], qdet); GB = RC.Gf @ B; vB = B.T @ v3; nb = B.shape[1]
    hv = np.zeros(len(RC.NOM)); flag = {}
    for c, i in zip(COMP, IC):
        if math.isfinite(h[c]): hv[i] = h[c]
        else: flag[c] = 'h NÃO estimável (contagem muda ao longo de v_3) → só o termo de Box'
    R_ = res['desenhos'][D['rot']] = {'h_funcional': h, 'delta': dl, 'omitidos': flag, 'ruidos': {}}
    print('\n%s: h ao longo de v_3 (δ = %.3f): %s %s' % (D['rot'], dl, {c: round(x, 4) for c, x in h.items()}, flag or ''), flush=True)
    for t in RC.TAUS:
        A = D['A']; m = D['membros']; Gc = sum(A[u][t][0] for u in m) + D['S'][t][0]; JA3 = sum(A[u][t][1] for u in m)[q3]; AA3 = sum(A[u][t][2] for u in m)[q3]
        M = B.T @ Gc @ B; Mi = np.linalg.inv(M); qq = float(vB @ Mi @ vB); sig = D['PF']['conjuntos'][cj][t]['certificado']
        box_u = GB @ (-0.5 * Mi @ (B.T @ JA3) * qq); fun_u = 0.5 * hv * qq                                   # por σ²
        form = sig ** 2 * (box_u + fun_u) / RC.tol
        # modelo reduzido (exato para a superfície quadrática): coordenadas tangentes R·Bβ (+ ½ t (vB·β)²) e a normal ½ n (vB·β)²
        R = np.linalg.cholesky(Gc).T; RB = R @ B; tq = np.linalg.solve(R.T, JA3); nq = math.sqrt(max(float(AA3 - tq @ tq), 0.0)); coef = np.r_[tq, nq]
        f = lambda b_: np.r_[RB @ b_ + 0.5 * tq * float(vB @ b_) ** 2, 0.5 * nq * float(vB @ b_) ** 2]
        jac = lambda b_: np.vstack([RB + np.outer(tq, vB) * float(vB @ b_), nq * float(vB @ b_) * vB[None]])
        Ffun = lambda b_: GB @ b_ + 0.5 * hv * float(vB @ b_) ** 2
        rng = np.random.default_rng(1670 + int(float(t)) + (0 if cj == 'acum' else 100)); E = np.empty((NFIT, len(RC.NOM))); Ec = np.empty_like(E); falhas = 0
        for k in range(NFIT):
            y = sig * rng.standard_normal(RB.shape[0] + 1)
            r = least_squares(lambda b_: f(b_) - y, np.zeros(nb), jac=jac, method='lm', xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=2000)
            if r.status <= 0 or not np.all(np.isfinite(r.x)): falhas += 1; E[k] = Ec[k] = np.inf; continue
            bh = r.x; Jh = jac(bh); Mhi = np.linalg.inv(Jh.T @ Jh); qh = float(vB @ Mhi @ vB)
            bbeta = -0.5 * sig ** 2 * Mhi @ (Jh.T @ coef) * qh; grad = GB + np.outer(hv, vB) * float(vB @ bh)
            E[k] = Ffun(bh); Ec[k] = E[k] - (grad @ bbeta + 0.5 * hv * sig ** 2 * qh)
        fin = np.isfinite(E).all(1); er = E[fin] / RC.tol; erc = Ec[fin] / RC.tol
        vies, ep = er.mean(0), er.std(0, ddof=1) / math.sqrt(fin.sum()); viesc = erc.mean(0)
        cob = np.mean(np.abs(E) <= RC.tol[None], 0); cobc = np.mean(np.abs(Ec) <= RC.tol[None], 0)
        conf = {c: bool(abs(vies[i] - form[i]) <= 3 * ep[i] or abs(vies[i] - form[i]) <= 0.2 * abs(form[i])) for c, i in zip(COMP, IC)}
        FALHA_CONF += ['%s %s %s' % (D['rot'], t, c) for c, ok in conf.items() if not ok]
        crit = bool(np.all(cob >= 0.95) and np.all(np.abs(vies) <= 0.10))
        R_['ruidos'][t] = {'sigma_certificado': sig, 'q_por_sigma2': qq, 'falhas': falhas, 'criterio_prompt0002_passa': crit,
                           'pior_cobertura': (RC.NOM[int(np.argmin(cob))], float(cob.min())), 'maior_vies_rel_MC': (RC.NOM[int(np.argmax(np.abs(vies)))], float(vies[np.argmax(np.abs(vies))])),
                           'componentes': {c: {'box_formula': float(sig ** 2 * box_u[i] / RC.tol[i]), 'funcional_formula': float(sig ** 2 * fun_u[i] / RC.tol[i]), 'completo_formula': float(form[i]),
                                               'completo_MC': float(vies[i]), 'ep_MC': float(ep[i]), 'residual_corrigido_MC': float(viesc[i]),
                                               'cobertura': float(cob[i]), 'cobertura_corrigido': float(cobc[i]), 'conferencia_formula_MC': conf[c]} for c, i in zip(COMP, IC)}}
        print('  %-9s σ = %-7.4g (certificado) | critério do 0002: %s (pior cobertura %s %.4f; maior |viés| %s %.3f)' % (RC.nm(t), sig, 'PASSA' if crit else 'FALHA',
              R_['ruidos'][t]['pior_cobertura'][0], cob.min(), R_['ruidos'][t]['maior_vies_rel_MC'][0], R_['ruidos'][t]['maior_vies_rel_MC'][1]), flush=True)
        for c, i in zip(COMP, IC):
            x = R_['ruidos'][t]['componentes'][c]
            print('     %-18s viés/tol: Box %+.4f + funcional %+.4f = fórmula %+.4f | MC %+.4f ± %.4f (%s) | corrigido %+.4f | cobertura %.4f → %.4f' % (
                  c, x['box_formula'], x['funcional_formula'], x['completo_formula'], x['completo_MC'], x['ep_MC'], 'confere' if x['conferencia_formula_MC'] else 'NÃO CONFERE',
                  x['residual_corrigido_MC'], x['cobertura'], x['cobertura_corrigido']), flush=True)

# leitura (do prompt): sobre o viés COMPLETO do MC das 3 componentes, no nível certificado de cada desenho e ruído
L = {}
for dr, x in res['desenhos'].items():
    for t, y in x['ruidos'].items():
        mx = max(abs(c['completo_MC']) for c in y['componentes'].values()); mr = max(abs(c['residual_corrigido_MC']) for c in y['componentes'].values())
        L['%s|%s' % (dr, t)] = 'viés completo ≤ 10%% (máx %.3f) → nada muda' % mx if mx <= 0.10 else (
            'viés completo %.3f > 10%%, residual corrigido %.3f ≤ 10%% → PROPOR estimador com correção de viés' % (mx, mr) if mr <= 0.10 else
            'residual corrigido %.3f > 10%% → PROPOR incluir o viés na especificação' % mr)
res['leitura'] = L; res['conferencia_formula_falhas'] = FALHA_CONF
print('\nLEITURA (declarada no prompt):'); [print('  %-22s %s' % (k, v)) for k, v in L.items()]
print('CONFERÊNCIA fórmula × MC: %s' % ('OK em todas' if not FALHA_CONF else 'NÃO confere em %s' % FALHA_CONF))
json.dump(res, open(sys.argv[1], 'w'), indent=1, default=float)
