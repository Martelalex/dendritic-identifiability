# etapaA_k7k8.py — D132 item 166 (prompt 0002): TESTES DO P-abs ANTES DE ADOTAR — Monte Carlo de mínimos quadrados NÃO LINEAR (desenho DECLARADO no item 166
# antes de rodar). Critério (do prompt, sem alteração): no nível que o P-abs certifica, CADA componente dentro da tolerância em ≥ 95% dos ajustes e
# |viés médio| ≤ 10% da tolerância. 2000 ajustes por nível, sementes fixas; ajuste local (scipy least_squares, 'lm') a partir da verdade; não convergido = FORA.
#   K7a  sintético 2 parâmetros: u muito curva (intrínseca), move só uma componente FOLGADA; w linear move a LIMITANTE; sem termo cruzado.
#   K7b  o mesmo com derivada segunda MISTA entre u e w (normal), X = K^N_uw/K^N_uu varrido; menor X em que o P-abs falha; e_X = e_N (principal) e ⟂ (info).
#   K8   superfície quadrática com o J, Jᵀa e aᵀa MEDIDOS no lote 1 (iid e OU 10 ms): K8-v3 (exato), K8-todas (partes normais ortogonais — premissa), K8-lin.
#   Controles: linear (κ = 0 / sem aceleração) → cobertura = gaussiana analítica (|Δ| ≤ 4 EP); K7b com X = 0 = K7a (idêntico).
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_k7k8.py <saida.json>
import sys, os, json, math
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import f as Fdist, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU
import etapaA_relev_abs as PA
import etapaA_relevancia_caburst as RC

NFIT = 2000; Z = 1.645; PASSA_COB = 0.95; PASSA_VIES = 0.10
res = {'nfit': NFIT}


def monte_carlo(f, jac, npar, ndim, sigma, G_, tol_, semente):
    """Ajustes de mínimos quadrados de y = f(0) + ε (f(0) = 0), ε ~ N(0, σ² I_ndim); erros das componentes G_ @ θ̂."""
    rng = np.random.default_rng(semente); E = np.empty((NFIT, len(tol_))); falhas = 0
    for k in range(NFIT):
        y = sigma * rng.standard_normal(ndim)
        r = least_squares(lambda th: f(th) - y, np.zeros(npar), jac=jac, method='lm', xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=2000)
        if r.status <= 0 or not np.all(np.isfinite(r.x)): falhas += 1; E[k] = np.inf; continue
        E[k] = G_ @ r.x
    cob = np.mean(np.abs(E) <= tol_[None], 0); fin = np.isfinite(E).all(1)
    vies = E[fin].mean(0) / tol_ if fin.any() else np.full(len(tol_), np.inf)
    return {'cobertura': cob, 'vies_rel': vies, 'falhas': falhas, 'passa': bool(np.all(cob >= PASSA_COB) and np.all(np.abs(vies) <= PASSA_VIES))}


def resumo(r, nomes):
    i = int(np.argmin(r['cobertura'])); j = int(np.argmax(np.abs(r['vies_rel'])))
    return {'passa': r['passa'], 'falhas': r['falhas'], 'pior_cobertura': (nomes[i], float(r['cobertura'][i])), 'maior_vies_rel': (nomes[j], float(r['vies_rel'][j]))}


# ======================= K7: sintético
n = 200; F2 = float(Fdist.ppf(0.95, 2, n - 2)); su, sw = 0.2, 1.0
tol7 = np.array([Z * 1.0 / sw, Z * 5.0 / su]); G7 = np.array([[0.0, 1.0], [1.0, 0.0]]); N7 = ['g_w (limitante)', 'g_u (folgada)']   # g_w = θ_w, g_u = θ_u
KNuu = 0.3 / (math.sqrt(F2) * math.sqrt(2) * 0.1); ku = KNuu * su ** 2                     # σ_lin,u = 0.1
sl_u = EU.sigma_lin(KNuu, 2, F2); Gc7 = np.diag([su ** 2, sw ** 2]); V7 = np.eye(2); B7 = np.eye(2)
sstar7 = float(np.min(tol7 / (Z * np.sqrt(np.einsum('gi,ij,gj->g', G7, np.linalg.inv(Gc7), G7)))))
ent = PA.entradas(V7, [0, 1], Gc7, B7, G7, tol7, PA.EPS); sc7, quem7 = PA.nivel(sstar7, {0: (sl_u, ent[0]), 1: (float('inf'), ent[1])})
hoje7 = min(sstar7, sl_u)
res['K7_parametros'] = {'n': n, 'F': F2, 's_u': su, 's_w': sw, 'tol': list(tol7), 'kappa_u': ku, 'K_N_uu': KNuu, 'sigma_lin_u': sl_u, 'sigma_estrela': sstar7,
                        'entradas': {'u': ent[0], 'w': ent[1]}, 'p_abs': sc7, 'hoje': hoje7}
print('K7: σ* = %.4g; σ_lin,u = %.4g (hoje certifica %.4g); entradas u %.4g, w %.4g → P-abs certifica %.4g' % (sstar7, sl_u, hoje7, ent[0], ent[1], sc7), flush=True)
assert math.isclose(sstar7, 1.0) and math.isclose(sl_u, 0.1) and math.isclose(sc7, 0.5)


def modelo7(kx, ortog):
    """Coordenadas reduzidas (exatas): (b_u, b_w, e_N[, e_X]); só elas importam para o ajuste."""
    nd = 4 if ortog else 3
    def f(th):
        u, w = th; out = np.zeros(nd); out[0] = su * u; out[1] = sw * w; out[2] = 0.5 * ku * u * u
        if ortog: out[3] = kx * u * w
        else: out[2] += kx * u * w
        return out
    def jac(th):
        u, w = th; J = np.zeros((nd, 2)); J[0, 0] = su; J[1, 1] = sw; J[2, 0] = ku * u
        if ortog: J[3, 0] = kx * w; J[3, 1] = kx * u
        else: J[2, 0] += kx * w; J[2, 1] = kx * u
        return J
    return f, jac, nd


def k7(X, sigma, ortog=False, linear=False, sem=1):
    kx = X * KNuu * su * sw                                             # K^N_uw = κ_x/(s_u s_w) = X·K^N_uu
    if linear:
        f = lambda th: np.array([su * th[0], sw * th[1], 0.0]); jac = lambda th: np.array([[su, 0], [0, sw], [0, 0.0]]); nd = 3
    else: f, jac, nd = modelo7(kx, ortog)
    return monte_carlo(f, jac, 2, nd, sigma, G7, tol7, sem)


FAL = []
# controle linear K7: cobertura analítica
ctl = True
for s in (0.5, 1.0):
    r = k7(0, s, linear=True); an = 2 * norm.cdf(tol7 / (s * np.array([1 / sw, 1 / su]))) - 1; ep = np.sqrt(an * (1 - an) / NFIT) + 1e-12
    ctl &= bool(np.all(np.abs(r['cobertura'] - an) <= 4 * ep + 1.0 / NFIT))   # 4 EP + correção de continuidade
    res.setdefault('K7_controle_linear', {})[str(s)] = {'mc': list(r['cobertura']), 'analitica': list(an)}
print('controle LINEAR K7: cobertura MC = gaussiana analítica (≤ 4 EP) → %s' % ('OK' if ctl else 'FALHOU'), flush=True); FAL += [] if ctl else ['K7_controle_linear']
# K7a
k7a = {str(s): k7(0, s) for s in (hoje7, sc7, sstar7)}
res['K7a'] = {s: resumo(r, N7) for s, r in k7a.items()}; pass7a = k7a[str(sc7)]['passa']
for s, r in k7a.items():
    print('K7a σ = %-5s %s cobertura %s viés/tol %s falhas %d %s' % (s, '(P-abs, DECIDE)' if s == str(sc7) else '(info)         ', np.round(r['cobertura'], 4), np.round(r['vies_rel'], 4), r['falhas'],
          ('PASSA' if r['passa'] else 'FALHA') if s == str(sc7) else ''), flush=True)
# caso literal (info): u não move nada → nível = σ*; cobertura do não linear ao lado da do linear
lit = k7(0, sstar7); litl = k7(0, sstar7, linear=True)
res['K7_literal_info'] = {'nivel': sstar7, 'cobertura_nao_linear': list(lit['cobertura']), 'cobertura_linear': list(litl['cobertura'])}
print('K7 literal (info; nível = σ*): cobertura g_w não linear %.4f × linear %.4f (90%% esperado pela definição do σ*)' % (lit['cobertura'][0], litl['cobertura'][0]), flush=True)
# K7b
for ortog in (False, True):
    nome = 'K7b_' + ('eX_ortogonal_info' if ortog else 'eX_igual_eN'); grade = [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]; tab = {}
    for X in grade:
        r = k7(X, sc7, ortog=ortog); tab[X] = r
    ctl0 = all(np.array_equal(tab[0][k], k7a[str(sc7)][k]) for k in ('cobertura', 'vies_rel')) if not ortog else True
    fal = [X for X in grade if not tab[X]['passa']]; Xf = None
    if fal:
        hi = fal[0]; lo = max([X for X in grade if X < hi and tab[X]['passa']], default=0.0)
        for _ in range(8):
            mid = 0.5 * (lo + hi); (lo, hi) = (mid, hi) if k7(mid, sc7, ortog=ortog)['passa'] else (lo, mid)
        Xf = (lo, hi)
    res[nome] = {'grade': {str(X): resumo(r, N7) for X, r in tab.items()}, 'X_falha_intervalo': Xf, 'controle_X0_igual_K7a': ctl0}
    print('%s: %s | menor X que FALHA: %s | controle X = 0 ≡ K7a: %s' % (nome, ' '.join('%g:%s' % (X, 'ok' if tab[X]['passa'] else 'FALHA') for X in grade),
          'nenhum na grade' if Xf is None else 'entre %.4g e %.4g' % Xf, 'OK' if ctl0 else 'DIFERENTE'), flush=True)
    for X in grade: print('     X = %-5g cobertura %s viés/tol %s falhas %d' % (X, np.round(tab[X]['cobertura'], 4), np.round(tab[X]['vies_rel'], 4), tab[X]['falhas']))
    if not ortog and not ctl0: FAL.append('K7b_controle_X0')

# ======================= K8: superfície quadrática com o lote 1
D = [d for d in RC.desenhos() if d['rot'] == 'lote 1'][0]; e0 = RC.estado(D, False); qdet = [q for q in D['qs'] if D['IDX'][q] in e0['DET']]; B = RC.base(D['V'], qdet)
livres = [q for q in D['qs'] if q not in qdet]; q3 = D['IDX'].index(3); NOMG = RC.NOM


def modelo8(t, curvas):
    A = D['A']; m = D['membros']; Gc = sum(A[u][t][0] for u in m) + D['S'][t][0]; JA = sum(A[u][t][1] for u in m); AA = sum(A[u][t][2] for u in m)
    R = np.linalg.cholesky(Gc).T; RB = R @ B; VB = D['V'] @ B                            # Gc = RᵀR
    T = {q: np.linalg.solve(R.T, JA[q]) for q in curvas}; Nn = {q: math.sqrt(max(float(AA[q] - T[q] @ T[q]), 0.0)) for q in curvas}
    k = len(curvas); nd = NP_ + k
    def f(b):
        out = np.zeros(nd); out[:NP_] = RB @ b
        for j, q in enumerate(curvas):
            c = float(VB[q] @ b); out[:NP_] += 0.5 * T[q] * c * c; out[NP_ + j] = 0.5 * Nn[q] * c * c
        return out
    def jac(b):
        J = np.zeros((nd, B.shape[1])); J[:NP_] = RB
        for j, q in enumerate(curvas):
            c = float(VB[q] @ b); J[:NP_] += np.outer(T[q], VB[q]) * c; J[NP_ + j] = Nn[q] * c * VB[q]
        return J
    Gq = B.T @ Gc @ B; sF = np.sqrt(np.einsum('gi,ij,gj->g', RC.Gf @ B, np.linalg.inv(Gq), RC.Gf @ B))
    return f, jac, nd, sF, {('v_%d' % D['IDX'][q]): {'tangente': float(np.linalg.norm(T[q])), 'normal': Nn[q]} for q in curvas}


NP_ = RC.NP; GB = RC.Gf @ B
niveis = {}; ab = json.load(open(os.path.join(RC.RES, 'etapaA_lotes', 'prompt0001', 'relev_abs.json')))['diagnostico_NAO_ADOTADO']['lote 1']
niveis['0.0'] = {'hoje = P-abs': ab['0.0']['p_abs']}; niveis['10.0'] = {'hoje': ab['10.0']['hoje'], 'P-abs': ab['10.0']['p_abs']}
assert math.isclose(ab['0.0']['p_abs'], ab['0.0']['hoje'])
pass8 = True; res['K8'] = {}
for t, nv in niveis.items():
    for var, curvas in (('K8-lin', []), ('K8-v3', [q3]), ('K8-todas', livres)):
        f, jac, nd, sF, cur = modelo8(t, curvas); res['K8'].setdefault(t, {})[var] = {'curvaturas': cur}
        for rot, s in nv.items():
            r = monte_carlo(f, jac, B.shape[1], nd, s, GB, RC.tol, 7 + int(float(t)))
            an = 2 * norm.cdf(RC.tol / (s * sF)) - 1; ep = np.sqrt(an * (1 - an) / NFIT) + 1e-12
            x = resumo(r, NOMG); x['dif_max_da_gaussiana_em_EP'] = float(np.max(np.abs(r['cobertura'] - an) / (ep + 1e-300)))
            decide = (rot != 'hoje') and var != 'K8-lin'
            if var == 'K8-lin':
                okl = bool(np.all(np.abs(r['cobertura'] - an) <= 4 * ep + 1.0 / NFIT)); x['controle_ok'] = okl
                if not okl: FAL.append('K8_controle_linear_%s_%s' % (t, rot))
            elif decide: pass8 &= r['passa']
            res['K8'][t][var][rot] = x
            print('K8 %-5s %-9s σ = %-8.4g (%-13s) %s pior cobertura %s %.4f | maior |viés|/tol %s %.4f | falhas %d | Δ da gaussiana máx %.1f EP' % (
                  RC.nm(t), var, s, rot, ('PASSA' if r['passa'] else 'FALHA') if decide else ('controle ' + ('OK' if x.get('controle_ok') else 'FALHOU') if var == 'K8-lin' else 'info '),
                  x['pior_cobertura'][0], x['pior_cobertura'][1], x['maior_vies_rel'][0], x['maior_vies_rel'][1], r['falhas'], x['dif_max_da_gaussiana_em_EP']), flush=True)
res['veredito'] = {'controles_ok': not FAL, 'falhas_de_controle': FAL, 'K7a_passa': bool(pass7a), 'K8_passa': bool(pass8),
                   'regra': ('NÃO ADOTAR (K7a ou K8 falha)' if not (pass7a and pass8) else 'K7a e K8 PASSAM → adoção depende dos termos cruzados REAIS (medir; custo a reportar, sem lançar)')}
print('\nCONTROLES: %s | K7a: %s | K8: %s → %s' % ('OK' if not FAL else 'FALHARAM %s' % FAL, 'PASSA' if pass7a else 'FALHA', 'PASSA' if pass8 else 'FALHA', res['veredito']['regra']))
json.dump(res, open(sys.argv[1], 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))
