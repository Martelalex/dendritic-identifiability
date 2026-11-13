# etapaA_sstar.py — D132 item 83 (2): AVALIAÇÃO DO ESPAÇAMENTO ao fim de cada estágio da Etapa A (ordem grosso → fino,
# item 73 (3)). Critério JÁ DECLARADO (item 13 + item 26), nada novo:
#   (i)  F IDENTIFICÁVEL no espaçamento s: com V₀ = direções de JᵀJ_s com σ < 10⁻⁶·σ_max, ‖G·V₀‖₂ ≤ 10⁻³·‖G‖₂;
#   (ii) o VIÉS de especificação sozinho cabe: |δF_viés,i| < tolerância_i para toda grandeza com tolerância declarada,
#        δF_viés = G·(JᵀJ_s)⁺·(JᵀΔy)_s + (F_Hay − F_red) (se o viés sozinho estoura, nenhum ruído basta — item 26).
#   BASTA(s) ⇔ (i) e (ii). Tolerâncias (D131 7.4): EPSP somático 5% (relativo a F0), 1º PA 1 ms, taxa f-I 2%; picos de
#   Ca SEM tolerância declarada → reportados, NÃO decidem. Falta de qualquer entrada (bloco de unidade, G, viés, uma
#   grandeza com tolerância ausente do G — ex.: a taxa f-I) → NÃO AVALIADO (nunca aprovação).
#   Saída também (não decide): σ_F por grandeza com σ_V unitário e x̂_V = min_i (tol_i − |δF_i|) / (1.645·σ_F,i).
# JᵀJ_s = soma dos blocos (p, r) com p e r no subconjunto de s (+ M4@p, M4@soma de cada p; + a unidade somática nas
# leituras de s) — reaproveitamento EXATO verificado no item 74 (B).
# Uso: python3 etapaA_sstar.py <s> <dir unidades> <G.npz> <vies.npz> <pontos.json> <saida.json>
#      python3 etapaA_sstar.py --autoteste
import sys, os, json
import numpy as np

TOL = {'EPSP': ('rel', 0.05), 'PA': ('abs', 1.0), 'taxa': ('rel', 0.02)}   # D131 7.4
NEEDED = ('EPSP', 'PA', 'taxa')


def tol_of(name):
    if name.startswith('EPSP_'): return TOL['EPSP']
    if name.endswith(('_PA1', '_PA2')): return TOL['PA']
    if name.startswith('taxa_'): return TOL['taxa']
    return None                                                          # picos de Ca: sem tolerância declarada


def evaluate(JtJ, JtDy, G, F0, names, dF_direct, cond=None):
    """Núcleo do critério. Entradas None → NÃO AVALIADO com o motivo. cond: por grandeza, a derivada é condicionada
    (etapaA_G: mesma contagem de PA em θ ± h para todos os parâmetros; G e F0 finitos) — uma grandeza COM tolerância e
    sem condicionamento → NÃO AVALIADO."""
    miss = [k for k, v in (('JtJ', JtJ), ('JtDy', JtDy), ('G', G), ('F_Hay − F_red', dF_direct)) if v is None]
    kinds = {k for k in NEEDED if any((tol_of(n) is TOL[k]) for n in names)} if names is not None else set()
    miss += ['grandeza "%s" ausente do G' % k for k in NEEDED if k not in kinds]
    if not miss:
        bad = [n for i, n in enumerate(names) if tol_of(n) is not None and ((cond is not None and not cond[i])
               or not (np.all(np.isfinite(G[i])) and np.isfinite(F0[i]) and np.isfinite(dF_direct[i])))]
        miss += ['grandeza não condicionada ou não finita: %s' % n for n in bad]
    if miss: return {'veredito': 'NÃO AVALIADO', 'faltam': miss}
    w, V = np.linalg.eigh(JtJ); sig = np.sqrt(np.clip(w, 0, None)); smax = sig.max()
    V0 = V[:, sig < 1e-6 * smax]; nG = np.linalg.norm(G, 2)
    leak = float(np.linalg.norm(G @ V0, 2) / nG) if V0.shape[1] else 0.0
    ident = leak <= 1e-3
    P = np.linalg.pinv(JtJ, rcond=1e-6, hermitian=True)                 # (JᵀJ)⁺ na mesma escala do corte de (i)
    dF = G @ (P @ JtDy) + dF_direct; sF = np.sqrt(np.clip(np.einsum('ij,jk,ik->i', G, P, G), 0, None))
    rows, ok_bias, xs = [], True, []
    for i, n in enumerate(names):
        t = tol_of(n)
        if t is None:
            rows.append({'grandeza': n, 'vies': float(dF[i]), 'sigmaF_unit': float(sF[i]), 'tolerancia': None, 'decide': False}); continue
        tol = t[1] * abs(F0[i]) if t[0] == 'rel' else t[1]; fits = abs(dF[i]) < tol; ok_bias &= bool(fits)
        if fits and sF[i] > 0: xs.append((tol - abs(dF[i])) / (1.645 * sF[i]))
        rows.append({'grandeza': n, 'vies': float(dF[i]), 'sigmaF_unit': float(sF[i]), 'tolerancia': float(tol), 'cabe': bool(fits), 'decide': True})
    return {'veredito': 'BASTA' if ident and ok_bias else 'NÃO BASTA', 'identificavel': bool(ident), 'vazamento_G_V0': leak,
            'n_direcoes_nulas': int(V0.shape[1]), 'sigma_min': float(sig.min()), 'sigma_max': float(smax), 'vies_cabe': bool(ok_bias),
            'x_hat_sigmaV_mV': float(min(xs)) if xs and ident and ok_bias else None, 'por_grandeza': rows}


def gather(s, udir, pontos):
    """Soma dos blocos (p, r) no subconjunto de s. Devolve (JtJ, JtDy) ou (None, motivo)."""
    S = set(pontos[str(s)]); JtJ = np.zeros((30, 30)); JtDy = np.zeros(30); has_dy = True
    for u in ['p_' + p for p in sorted(S)] + ['p_soma']:
        f = os.path.join(udir, '%s.npz' % u)
        if not os.path.exists(f): return None, None, 'unidade %s ausente' % u
        z = np.load(f); lr = [str(x) for x in z['leituras']]
        sel = [i for i, r in enumerate(lr) if r.split('@')[-1] in S or r.split('@')[-1] == 'soma' or r in S or r == 'soma'
               or r == 'M4@p']
        JtJ += z['JtJ'][sel].sum(0)
        if 'JtDy' in z.files: JtDy += z['JtDy'][sel].sum(0)
        else: has_dy = False
    return JtJ, (JtDy if has_dy else None), None


def selftest():
    """O critério tem de poder FALHAR: 4 casos sintéticos com veredito conhecido."""
    rng = np.random.default_rng(7); A = rng.normal(size=(400, 30)); JtJ = A.T @ A
    names = ['EPSP_a', 'EPSP_b', 'BAC_PA2', 'taxa_1', 'BAC_Ca']; F0 = np.array([1.0, 2.0, 50.0, 10.0, 20.0])
    G = rng.normal(size=(5, 30)) * 1e-3; JtDy = np.zeros(30); d0 = np.zeros(5)
    out = {}
    out['posto cheio, sem viés'] = (evaluate(JtJ, JtDy, G, F0, names, d0)['veredito'], 'BASTA')
    w, V = np.linalg.eigh(JtJ); Js = JtJ - w[0] * np.outer(V[:, 0], V[:, 0]) * (1 - 1e-16)   # direção nula
    G2 = G.copy(); G2[0] += V[:, 0] * np.linalg.norm(G, 2)                                 # F enxerga a direção nula
    out['direção nula vista por F'] = (evaluate(Js, JtDy, G2, F0, names, d0)['veredito'], 'NÃO BASTA')
    out['viés estoura o EPSP'] = (evaluate(JtJ, JtDy, G, F0, names, np.array([0.06, 0, 0, 0, 0]))['veredito'], 'NÃO BASTA')
    out['G sem taxa f-I'] = (evaluate(JtJ, JtDy, G[[0, 1, 2, 4]], F0[[0, 1, 2, 4]], [names[i] for i in (0, 1, 2, 4)], d0[[0, 1, 2, 4]])['veredito'], 'NÃO AVALIADO')
    out['viés ausente'] = (evaluate(JtJ, None, G, F0, names, d0)['veredito'], 'NÃO AVALIADO')
    out['taxa não condicionada'] = (evaluate(JtJ, JtDy, G, F0, names, d0, cond=np.array([1, 1, 1, 0, 1], bool))['veredito'], 'NÃO AVALIADO')
    out['Ca não condicionado (sem tol.)'] = (evaluate(JtJ, JtDy, G, F0, names, d0, cond=np.array([1, 1, 1, 1, 0], bool))['veredito'], 'BASTA')
    ok = all(a == b for a, b in out.values())
    for k, (a, b) in out.items(): print('%-28s → %-13s (esperado %s) %s' % (k, a, b, 'ok' if a == b else 'ERRADO'))
    print('AUTOTESTE:', 'PASSA' if ok else 'FALHA'); return ok


if __name__ == '__main__':
    if sys.argv[1] == '--autoteste': sys.exit(0 if selftest() else 1)
    s, udir, gf, vf, pf, out = int(sys.argv[1]), *sys.argv[2:7]
    if not selftest(): sys.exit('autoteste do critério FALHOU — avaliação recusada')
    pontos = json.load(open(pf)); JtJ, JtDy, why = gather(s, udir, pontos)
    G = F0 = names = dF = cond = None
    if os.path.exists(gf):
        z = np.load(gf); G, F0, names = z['G'], z['F0'], [str(x) for x in z['nomes']]
        cond = z['condicionado'] if 'condicionado' in z.files else None
    if os.path.exists(vf):
        zv = np.load(vf); dF = zv['dF_direto']
        if names is not None and ('nomes' not in zv.files or [str(x) for x in zv['nomes']] != names):
            why = why or 'nomes do termo direto do viés ≠ nomes do G'
    res = {'veredito': 'NÃO AVALIADO', 'faltam': [why]} if why else evaluate(JtJ, JtDy, G, F0, names, dF, cond)
    res.update({'s_um': s, 'n_pontos': len(pontos[str(s)])})
    tmp = out + '.tmp%d' % os.getpid(); json.dump(res, open(tmp, 'w'), indent=1); os.replace(tmp, out)
    print('s = %d µm → %s' % (s, res['veredito']), res.get('faltam', ''))
