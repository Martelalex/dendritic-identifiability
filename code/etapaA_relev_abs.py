# etapaA_relev_abs.py — D132 item 165 (prompt 0001, parte 2): PROPOSTA (NÃO ADOTADA) de critério de RELEVÂNCIA ABSOLUTO no nível de operação + controles
# sintéticos de resposta conhecida + o que ela daria nos dados (DIAGNÓSTICO, sem efeito em nenhuma regra).
# CRITÉRIO P-abs (proposto): dentro do conjunto relevante pela cobertura relativa (o de hoje), menos as resolvidas pela faixa, a direção v_i só CONTA no
# ruído σ se mover alguma componente funcional g em pelo menos ε da tolerância:  1.645·σ·|g·v_i|·√(v_iᵀB(BᵀG_τB)⁻¹Bᵀv_i) / tol_g ≥ ε  (o Gram que dá o σ*;
# contribuição ABSOLUTA da parte (c)). Isso define o ENTRADA de v_i: σ_i = ε·min_g tol_g / (1.645·|g·v_i|·√marg_i). Nível certificado AUTOCONSISTENTE:
#   σ_c = max{σ ≤ σ* : σ ≤ σ_lin,i para toda v_i que conta em σ}  =  min(σ*, min_i max(σ_lin,i, σ_i))
# (fechado: a v_i curva só limita até o ruído em que ela passa a importar). ε = 0.10 (o mesmo 10% da leitura declarada). Propriedades: ε → 0 devolve a regra
# de hoje (min(σ*, min σ_lin)); σ_c não decresce com ε; invariante a unidades (g e tol escalam juntos).
# CONTROLES (resposta conhecida): K1 forma fechada = definição por varredura (300 instâncias aleatórias); K2 direção curva que só move componente FOLGADA
# (entrada acima de σ*) → não limita, σ_c = o próximo limite conhecido; K3 direção curva que move a componente LIMITANTE → limita (σ_c = σ_lin dela);
# K4 ε = 0 → a regra de hoje, EXATA nos dois desenhos reais (= PONTO_FIXO.json); K5 σ_c não decresce com ε (real e sintético); K6 invariância de unidades.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_relev_abs.py <saida.json>
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU
import etapaA_relevancia_caburst as RC

EPS = 0.10; Z = RC.Z; NP = RC.NP; F = RC.F


def entradas(V, qs, Gc, B, G_, tol_, eps):
    """σ_i em que cada direção v_i passa a mover alguma componente em ε da tolerância (1.645σ·|g·v|·√marg ≥ ε·tol)."""
    Gi = np.linalg.inv(B.T @ Gc @ B); out = {}
    for q in qs:
        bv = B.T @ V[q]; m = float(bv @ Gi @ bv); gv = np.abs(G_ @ V[q])
        with np.errstate(divide='ignore'): out[q] = eps * float(np.min(np.where(gv > 0, tol_ / (Z * gv * math.sqrt(m)), np.inf)))
    return out


def nivel(sstar, lims):
    """lims: {q: (σ_lin,q, σ_entrada,q)} → (σ_c, quem limita) = min(σ*, min_q max(σ_lin,q, σ_q))."""
    best = (sstar, 'σ*')
    for q, (sl, se) in lims.items():
        x = max(sl, se)
        if x < best[0]: best = (x, q)
    return best


def nivel_varredura(sstar, lims, n=20001):
    """A DEFINIÇÃO, por varredura: o maior σ ≤ σ* com σ ≤ σ_lin,q para toda q com σ_q ≤ σ."""
    ok = [s for s in np.linspace(0, sstar, n)[1:] if all(s <= sl for sl, se in lims.values() if se <= s)]
    return max(ok) if ok else 0.0


def controles():
    rng = np.random.default_rng(1650); R = {}
    # K1: forma fechada = definição
    pior = 0.0
    for _ in range(300):
        ss = float(rng.uniform(1, 10)); lims = {q: (float(rng.uniform(0.1, 12)), float(rng.uniform(0, 12))) for q in range(int(rng.integers(1, 8)))}
        a, _ = nivel(ss, lims); b = nivel_varredura(ss, lims); pior = max(pior, abs(a - b) / ss)
    R['K1'] = (pior < 2 * 1 / 20000, 'forma fechada × varredura: pior |Δ|/σ* = %.1e (resolução 5e-5)' % pior)
    # K2/K3: 2 componentes (g0 LIMITANTE, tol 1; g1 FOLGADA, tol 1000), 3 direções ortonormais, Gram diagonal conhecido
    V = np.eye(NP)[:3]; Gc = np.diag(np.r_[1.0, 1.0, 1.0, np.ones(NP - 3)]); B = np.eye(NP)
    g0 = np.zeros(NP); g0[0] = 1.0; g1 = np.zeros(NP); g1[1] = 1.0; G_ = np.stack([g0, g1]); tol_ = np.array([1.0, 1000.0])
    sstar = float(np.min(tol_ / (Z * np.sqrt(np.einsum('gi,ij,gj->g', G_, np.linalg.inv(Gc), G_)))))     # = 1/1.645 (g0)
    ent = entradas(V, [0, 1, 2], Gc, B, G_, tol_, EPS)                 # v_0: ε/1.645 (move g0); v_1: ε·1000/1.645 (só g1); v_2: ∞ (não move nada)
    ok_ent = math.isclose(ent[0], EPS / Z) and math.isclose(ent[1], EPS * 1000 / Z) and ent[2] == np.inf
    # K2: v_1 MUITO curva (σ_lin 0.01) mas só move a folgada → entrada 60.8 > σ* = 0.608 → não limita; v_0 reta (σ_lin 100) → σ_c = σ*
    s2, q2 = nivel(sstar, {0: (100.0, ent[0]), 1: (0.01, ent[1]), 2: (0.001, ent[2])})
    R['K2'] = (ok_ent and math.isclose(s2, sstar) and q2 == 'σ*', 'curva só na folgada: σ_c = %.4g (esperado σ* = %.4g; limitou %s); entradas %s' % (s2, sstar, q2, {k: round(v, 4) for k, v in ent.items()}))
    # K3: v_0 curva (σ_lin 0.2) move a LIMITANTE → entrada 0.061 < 0.2 → σ_c = 0.2 (a regra de hoje também)
    s3, q3 = nivel(sstar, {0: (0.2, ent[0]), 1: (100.0, ent[1])})
    R['K3'] = (math.isclose(s3, 0.2) and q3 == 0, 'curva na limitante: σ_c = %.4g (esperado 0.2, v_0)' % s3)
    # K6: unidades — g1 e tol1 ×1e3 → mesmas entradas
    G2 = G_.copy(); G2[1] *= 1e3; t2 = tol_.copy(); t2[1] *= 1e3; e2 = entradas(V, [0, 1, 2], Gc, B, G2, t2, EPS)
    R['K6'] = (all(math.isclose(e2[q], ent[q]) or (e2[q] == ent[q] == np.inf) for q in ent), 'invariância de unidades: entradas iguais com g_1, tol_1 ×1000')
    # K5 sintético: σ_c não decresce com ε
    mono = True
    for _ in range(200):
        ss = float(rng.uniform(1, 10)); base = {q: (float(rng.uniform(0.1, 12)), float(rng.uniform(0, 5))) for q in range(5)}
        vals = [nivel(ss, {q: (sl, e * k) for q, (sl, e) in base.items()})[0] for k in np.linspace(0, 3, 31)]
        mono &= all(b >= a - 1e-12 for a, b in zip(vals, vals[1:]))
    R['K5_sintetico'] = (mono, 'σ_c não decresce com ε (200 instâncias)')
    return R


def no_desenho(D, t, eps):
    e = RC.estado(D, False); qdet = [q for q in D['qs'] if D['IDX'][q] in e['DET']]; B = RC.base(D['V'], qdet)
    A = D['A']; m = D['membros']; Gd = sum(A[u][t][0] for u in m); JA = sum(A[u][t][1] for u in m); AA = sum(A[u][t][2] for u in m); V = D['V']
    Gc = sum(A[u][t][0] for u in m) + D['S'][t][0]; ss = e['conjuntos'][t]['sigma_estrela']
    livres = [q for q in D['qs'] if q not in qdet]
    sl = {q: EU.sigma_lin(EU.curvaturas(Gd, JA[q], AA[q], float(V[q] @ Gd @ V[q]))[0], NP, F) for q in livres}
    en = entradas(V, livres, Gc, B, RC.Gf, RC.tol, eps) if eps > 0 else {q: 0.0 for q in livres}
    sc, qq = nivel(ss, {q: (sl[q], en[q]) for q in livres})
    return sc, ('σ*' if qq == 'σ*' else 'v_%d' % D['IDX'][qq]), {('v_%d' % D['IDX'][q]): (sl[q], en[q]) for q in livres}, e


if __name__ == '__main__':
    OUT = sys.argv[1]; res = {'eps': EPS, 'controles': {}, 'diagnostico_NAO_ADOTADO': {}}; FAL = []
    for k, (ok, msg) in controles().items():
        print('%-14s %s  %s' % (k, 'OK' if ok else 'FALHOU', msg), flush=True); res['controles'][k] = {'ok': bool(ok), 'msg': msg}
        if not ok: FAL.append(k)
    DS = RC.desenhos(); ok4 = True; ok5 = True
    for D in DS:
        c = '6inj' if D['rot'] == 'piloto-6' else 'acum'
        for t in RC.TAUS:
            s0, _, _, _ = no_desenho(D, t, 0.0); ok4 &= s0 == D['PF']['conjuntos'][c][t]['certificado']
            vals = [no_desenho(D, t, x)[0] for x in (0.0, 0.05, 0.10, 0.20)]; ok5 &= all(b >= a for a, b in zip(vals, vals[1:]))
    for k, ok, msg in (('K4_real', ok4, 'ε = 0 → a regra de hoje, EXATA nos dois desenhos (= certificado do PONTO_FIXO.json)'), ('K5_real', ok5, 'σ_c não decresce com ε (0, 0.05, 0.1, 0.2) nos dados')):
        print('%-14s %s  %s' % (k, 'OK' if ok else 'FALHOU', msg), flush=True); res['controles'][k] = {'ok': bool(ok), 'msg': msg}
        if not ok: FAL.append(k)
    assert not FAL, ('controles falharam — nada adiante vale', FAL)
    print('\nDIAGNÓSTICO (NÃO ADOTADO): nível certificado pela regra de hoje × pelo P-abs (ε = %.2f); entre parênteses quem limita' % EPS)
    for D in DS:
        c = '6inj' if D['rot'] == 'piloto-6' else 'acum'
        for t in RC.TAUS:
            sc, quem, det, e = no_desenho(D, t, EPS); hoje = D['PF']['conjuntos'][c][t]
            top = sorted(det.items(), key=lambda kv: max(kv[1]))[:3]
            res['diagnostico_NAO_ADOTADO'].setdefault(D['rot'], {})[t] = {'hoje': hoje['certificado'], 'hoje_limita': 'σ*' if hoje['sigma_estrela'] <= hoje['sigma_lin'] else 'v_%d' % hoje['v_lin'],
                                                                         'p_abs': sc, 'p_abs_limita': quem, 'sigma_estrela': hoje['sigma_estrela'],
                                                                         'direcoes': {k: {'sigma_lin': a, 'entrada': b} for k, (a, b) in det.items()}}
            print('  %-8s %-9s hoje %.4g (%s) → P-abs %.4g (%s, ×%.2f) | 3 menores max(σ_lin, entrada): %s' % (D['rot'], RC.nm(t), hoje['certificado'],
                  res['diagnostico_NAO_ADOTADO'][D['rot']][t]['hoje_limita'], sc, quem, sc / hoje['certificado'], ', '.join('%s (σ_lin %.3g, entra em %.3g)' % (k, a, b) for k, (a, b) in top)))
    json.dump(res, open(OUT, 'w'), indent=1, default=float)
