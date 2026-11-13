# etapaA_relevancia_caburst.py — D132 item 165 (prompt 0001 do canal), SEM SIMULAR, a partir dos acumulados por unidade e dos Fdir gravados.
# (2) O QUE TORNA v_3 RELEVANTE (diagnóstico; a regra NÃO muda): o conjunto relevante sai UMA vez do Gram de seleção (iid, sem faixa, θ das unidades + somática)
#     por cobertura RELATIVA (etapaA_unit.direcoes_relevantes: ≥ 99% de Σ_i f_gi para TODA componente g). Para v_3 (e a direção que limita o σ_lin de cada τ):
#     (a) as componentes que PRECISAM dela (sem ela, Σ f_gi < 99%); (b) 1.645·σ_g(σ)/tol_g em σ = σ* e σ = σ_lin; (c) contribuição ABSOLUTA
#     σ²·c_gq/(tol_g/1.645)², c_gq = (g·v_q)²·v_qᵀ B(BᵀG_τB)⁻¹Bᵀ v_q (o Gram que dá o σ*; no iid também o c do código, (g·v_q)²/s_q²); (d) σ_lin sem v_q.
#     LEITURA (declarada no prompt): v_3 entra SÓ por componentes com 1.645·σ_g(σ_lin)/tol_g < 10% → PROPOR critério absoluto; entra pelo CaBurst_PA1 ou por
#     componente perto da tolerância → hipótese REFUTADA.
# (3) SENSIBILIDADE (rótulo; o critério D131 7.4 NÃO muda): conjunto funcional SEM o CaBurst_PA1 (e sem a contagem dele no Fdir: um Fdir FORA só pelo
#     CaBurst_PA1 vira DENTRO); conjunto relevante (A) o gravado e (B) recalculado sem o CaBurst_PA1; ponto fixo com os Fdir gravados — candidata NOVA não
#     testada → PARA e reporta o custo (os valores com as resolvidas de agora são LIMITES INFERIORES dos do ponto fixo: resolver mais só sobe σ* e σ_lin).
# CONFERÊNCIAS antes (resposta conhecida): R0 o Gram de seleção refeito dos acumulados (variante sem faixa, iid) reproduz o conjunto relevante gravado
# (mesmos índices na mesma ordem, s e v); R1 σ*, σ_lin dos dois desenhos = PONTO_FIXO.json (exato).
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_relevancia_caburst.py <saida.json>
import sys, os, json, math, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU
import etapaA_sstar as S

AQ = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQ, 'results')
NP = 30; F = 1.4591; Z = 1.645; TAUS = ('0.0', '1.0', '10.0', '50.0'); TT = (0.0, 1.0, 10.0, 50.0); H_AVAL = 1.9   # h por avaliação (MEDIDO, item 164)
zg = np.load(os.path.join(RES, 'etapaA_G8', 'G.npz'), allow_pickle=True); nomes = [str(x) for x in zg['nomes']]; tl = [S.tol_of(x) for x in nomes]
use = [i for i, t in enumerate(tl) if t is not None and zg['condicionado'][i] and np.all(np.isfinite(zg['G'][i]))]
Gf = zg['G'][use]; tol = np.array([tl[i][1] * abs(zg['F0'][i]) if tl[i][0] == 'rel' else tl[i][1] for i in use]); NOM = [nomes[i] for i in use]
iCB = NOM.index('CaBurst_PA1'); SEM = [g for g in range(len(NOM)) if g != iCB]
PC = ['g_apic[60]_32', 'g_apic[36]_16', 'g_apic[9]_16', 'g_apic[44]_48', 'g_apic[64]_48']; NOV = ['g_apic[70]_48', 'g_apic[77]_48', 'g_apic[37]_32', 'g_apic[19]_16', 'g_apic[17]_16']
nm = lambda t: 'iid' if t == '0.0' else 'OU %g ms' % float(t)


def fdirs(d):
    fd = {}
    for f in [os.path.join(d, 'Fdir.json')] + sorted(glob.glob(os.path.join(d, 'pf', 'Fdir_*.json'))):
        x = json.load(open(f))['direcoes']; assert not set(x) & set(fd); fd.update(x)
    return fd


def dentro(r, sem_cb):
    return all(not [c for c in r[g]['fora'] if not (sem_cb and c[0] == 'CaBurst_PA1')] for g in ('mais', 'menos'))


def base(V, qdet):
    Pc = np.eye(NP) - sum((np.outer(V[q], V[q]) for q in qdet), np.zeros((NP, NP))); w, U = np.linalg.eigh(Pc); return U[:, w > 0.5]


def acc(pref, var='fis'):
    z = np.load('%s.%s.npz' % (pref, var)); return {t: (z['G_%g' % tt], z['JA_%g' % tt], z['AA_%g' % tt]) for t, tt in zip(TAUS, TT)}


def sF(Gc, B, G_):
    gb = G_ @ B; return np.sqrt(np.einsum('gi,ij,gj->g', gb, np.linalg.inv(B.T @ Gc @ B), gb))


def sestrela(Gc, B, gs):
    x = tol[gs] / (Z * sF(Gc, B, Gf[gs])); i = int(np.argmin(x)); return float(x[i]), NOM[gs[i]]


def slin(D, t, qdet, excl=()):
    A = D['A']; m = D['membros']; Gd = sum(A[u][t][0] for u in m); JA = sum(A[u][t][1] for u in m); AA = sum(A[u][t][2] for u in m); V = D['V']
    out = [(EU.sigma_lin(EU.curvaturas(Gd, JA[q], AA[q], float(V[q] @ Gd @ V[q]))[0], NP, F), D['IDX'][q]) for q in D['qs'] if q not in qdet and D['IDX'][q] not in excl]
    return min(out) if out else (float('inf'), None)


def desenho(rot, d, accdir, membros):
    z = np.load(os.path.join(d, 'direcoes.npz')); fd = fdirs(d)
    D = {'rot': rot, 'd': d, 'V': z['V'], 'IDX': [int(i) + 1 for i in z['indices']], 'sigma': z['sigma'], 'fd': fd, 'membros': membros,
         'A': {u: acc(os.path.join(accdir, 'acc_' + u)) for u in membros}, 'S': acc(os.path.join(accdir, 'acc_soma')),
         'Ainf': {u: np.load(os.path.join(accdir, 'acc_%s.inf.npz' % u))['G_0'] for u in membros}, 'Sinf': np.load(os.path.join(accdir, 'acc_soma.inf.npz'))['G_0'],
         'PF': json.load(open(os.path.join(d, 'pf', 'PONTO_FIXO.json')))}
    D['qs'] = list(range(len(D['IDX']))); return D


def estado(D, sem_cb, qs=None):
    """DET pelos Fdir (sem o CaBurst_PA1 se sem_cb), σ*, σ_lin por τ; ponto fixo: candidatas NÃO testadas além do fator 2 no σ* iid resultante."""
    qs = D['qs'] if qs is None else qs; gs = SEM if sem_cb else list(range(len(NOM)))
    TEST = [int(n[2:]) for n in D['fd']]; DET = [int(n[2:]) for n, r in D['fd'].items() if dentro(r, sem_cb)]
    qdet = [q for q in qs if D['IDX'][q] in DET]; B = base(D['V'], qdet); r = {}
    for t in TAUS:
        Gc = sum(D['A'][u][t][0] for u in D['membros']) + D['S'][t][0]; ss, lim = sestrela(Gc, B, gs)
        DD = dict(D, qs=qs); sl, vl = slin(DD, t, qdet)
        r[t] = {'sigma_estrela': ss, 'limitante': lim, 'sigma_lin': sl, 'v_lin': vl, 'certificado': min(ss, sl)}
    mx = np.abs(D['V']).max(1); s_iid = r['0.0']['sigma_estrela']
    cand = [D['IDX'][q] for q in qs if s_iid * math.sqrt(NP * F) / D['sigma'][q] * mx[q] > EU.TETO_LOG and D['IDX'][q] not in TEST]
    return {'DET': sorted(DET), 'testadas': sorted(TEST), 'conjuntos': r, 'candidatas_novas': cand, 'ponto_fixo': not cand}


def desenhos():
    return [desenho('piloto-6', os.path.join(RES, 'etapaA_pcond'), os.path.join(RES, 'etapaA_lotes', 'regr154'), PC),
            desenho('lote 1', os.path.join(RES, 'etapaA_lotes', 'lote1'), os.path.join(RES, 'etapaA_lotes', 'lote1'), PC + NOV)]


def main(OUT):
    DS = desenhos()
    res = {'conferencias': {}}
    # ---- R0: o Gram de seleção refeito reproduz o conjunto relevante gravado; R1: PONTO_FIXO.json
    for D in DS:
        Gs = sum(D['Ainf'][u] for u in D['membros']) + D['Sinf']; w, V = np.linalg.eigh(Gs); s = np.sqrt(np.clip(w, 0, None))
        esc, f = EU.direcoes_relevantes(s, V, Gf); D['sel'] = (s, V, esc, f)
        ok_i = [int(i) + 1 for i in esc] == D['IDX']; ds = float(np.max(np.abs(s[esc] / D['sigma'] - 1))); dv = float(np.max(1 - np.abs(np.sum(V[:, esc].T * D['V'], 1))))
        e = estado(D, False); ok1 = all(e['conjuntos'][t]['sigma_estrela'] == D['PF']['conjuntos'][c][t]['sigma_estrela'] and e['conjuntos'][t]['sigma_lin'] == D['PF']['conjuntos'][c][t]['sigma_lin']
                                        for t in TAUS for c in [('6inj' if D['rot'] == 'piloto-6' else 'acum')])
        res['conferencias'][D['rot']] = {'R0_indices_iguais': ok_i, 'R0_dif_rel_s': ds, 'R0_1_menos_cos_v': dv, 'R1_ponto_fixo_exato': ok1, 'R1_ponto_fixo_alcancado': e['ponto_fixo']}
        print('CONFERÊNCIA %-8s R0 seleção refeita: índices %s, |Δs/s| máx %.1e, 1−|cos| máx %.1e | R1 σ*, σ_lin = PONTO_FIXO.json: %s' % (
              D['rot'], 'IGUAIS' if ok_i else 'DIFERENTES', ds, dv, 'EXATO' if ok1 else 'DIFERENTE'), flush=True)
        assert ok_i and ds < 1e-6 and dv < 1e-6 and ok1 and e['ponto_fixo'], 'conferência falhou — nada adiante vale'
        D['e0'] = e

    # ---- (2) o que torna v_3 relevante
    print('\n(2) O QUE TORNA v_3 RELEVANTE (seleção: Gram iid sem faixa; f_gq = c_gq/Σ_j c_gj; cobertura 99%)'); res['relevancia'] = {}
    for D in DS:
        s, V, esc, f = D['sel']; e = D['e0']; R = res['relevancia'].setdefault(D['rot'], {})
        alvo = sorted({3} | {e['conjuntos'][t]['v_lin'] for t in TAUS})
        for vq in alvo:
            q = D['IDX'].index(vq); iq = int(esc[q]); resto = [int(i) for i in esc if int(i) != iq]
            cob = f[:, resto].sum(1); need = [g for g in range(len(NOM)) if cob[g] < EU.COBERTURA]
            ordem = int(q); amax = int(np.argmax(f[:, iq]))
            acum_antes = f[:, [int(i) for i in esc[:q]]].sum(1)
            abaixo = [g for g in range(len(NOM)) if acum_antes[g] < EU.COBERTURA and f[g, iq] > 0.01]
            ref = sorted(set(need) | {iCB, NOM.index(e['conjuntos']['0.0']['limitante'])} | {NOM.index(e['conjuntos'][t]['limitante']) for t in TAUS})
            qdet = [qq for qq in D['qs'] if D['IDX'][qq] in e['DET']]; B = base(D['V'], qdet); v = D['V'][q]
            lin = {}
            for t in TAUS:
                Gc = sum(D['A'][u][t][0] for u in D['membros']) + D['S'][t][0]; sf = sF(Gc, B, Gf); ss, sl = e['conjuntos'][t]['sigma_estrela'], e['conjuntos'][t]['sigma_lin']
                Bv = B.T @ v; marg = float(Bv @ np.linalg.inv(B.T @ Gc @ B) @ Bv); sl_sem, vl_sem = slin(D, t, qdet, excl=(vq,))
                lin[t] = {'sigma_estrela': ss, 'sigma_lin': sl, 'sigma_lin_sem_v': sl_sem, 'v_lin_sem_v': vl_sem, 'componentes': {}}
                for g in ref:
                    cg = float((Gf[g] @ v) ** 2) * marg; csel = float((Gf[g] @ V[:, iq]) ** 2 / s[iq] ** 2)
                    lin[t]['componentes'][NOM[g]] = {'f_gq': float(f[g, iq]), 'cobertura_sem_v': float(cob[g]), 'precisa': g in need,
                                                     'razao_em_sigma_estrela': Z * ss * sf[g] / tol[g], 'razao_em_sigma_lin': Z * sl * sf[g] / tol[g],
                                                     'contrib_abs_sigma_estrela': ss ** 2 * cg / (tol[g] / Z) ** 2, 'contrib_abs_sigma_lin': sl ** 2 * cg / (tol[g] / Z) ** 2,
                                                     'contrib_abs_iid_codigo_sigma_estrela': (ss ** 2 * csel / (tol[g] / Z) ** 2) if t == '0.0' else None,
                                                     'contrib_abs_iid_codigo_sigma_lin': (sl ** 2 * csel / (tol[g] / Z) ** 2) if t == '0.0' else None}
            if not need: leit = {t: 'NENHUMA componente precisa de v_%d (entra só pela ordem gulosa)' % vq for t in TAUS}
            else:
                leit = {}
                for t in TAUS:
                    rl = {NOM[g]: lin[t]['componentes'][NOM[g]]['razao_em_sigma_lin'] for g in need}
                    if iCB in need: leit[t] = 'REFUTADA (entra pelo CaBurst_PA1)'
                    elif max(rl.values()) < 0.10: leit[t] = 'SÓ por componentes FOLGADAS em σ_lin (< 10%) → PROPOR critério absoluto'
                    else: leit[t] = 'REFUTADA (componente perto da tolerância: %s %.0f%% em σ_lin)' % (max(rl, key=rl.get), 100 * max(rl.values()))
            R['v_%d' % vq] = {'posicao_na_ordem': ordem + 1, 'componente_do_max_f': NOM[amax], 'max_f': float(f[amax, iq]), 'precisam': [NOM[g] for g in need],
                              'abaixo_de_99_quando_entrou_com_f>1%': [NOM[g] for g in abaixo], 'por_ruido': lin, 'leitura': leit}
            print('\n  %s — v_%d: %dª na ordem gulosa (max f = %.3f em %s); PRECISAM dela (sem ela < 99%%): %s' % (D['rot'], vq, ordem + 1, f[amax, iq], NOM[amax],
                  ['%s (f %.3f; sem ela %.3f)' % (NOM[g], f[g, iq], cob[g]) for g in need] or 'NENHUMA'))
            for t in TAUS:
                L = lin[t]; print('    %-9s σ* %.4g σ_lin %.4g (sem v_%d: %.4g, v_%s) | %s' % (nm(t), L['sigma_estrela'], L['sigma_lin'], vq, L['sigma_lin_sem_v'], L['v_lin_sem_v'], leit[t]))
                for n, c in L['componentes'].items():
                    print('       %-16s %-7s f %.3f | 1.645σ_g/tol: em σ* %.3f, em σ_lin %.3f | contrib. abs. de v_%d: em σ* %.2e, em σ_lin %.2e%s' % (
                          n, 'PRECISA' if c['precisa'] else '', c['f_gq'], c['razao_em_sigma_estrela'], c['razao_em_sigma_lin'], vq, c['contrib_abs_sigma_estrela'], c['contrib_abs_sigma_lin'],
                          '' if c['contrib_abs_iid_codigo_sigma_lin'] is None else ' (c do código: %.2e / %.2e)' % (c['contrib_abs_iid_codigo_sigma_estrela'], c['contrib_abs_iid_codigo_sigma_lin'])))

    # ---- (3) sensibilidade sem o CaBurst_PA1
    print('\n(3) SENSIBILIDADE — SEM o CaBurst_PA1 (e sem a contagem dele no Fdir); critério declarado NÃO muda'); res['sem_caburst'] = {}
    for D in DS:
        s, V, esc, f = D['sel']; esc2, f2 = EU.direcoes_relevantes(s, V, Gf[SEM]); sub = set(int(i) for i in esc2) <= set(int(i) for i in esc)
        novas = [int(i) + 1 for i in esc2 if int(i) not in set(int(x) for x in esc)]; R = res['sem_caburst'].setdefault(D['rot'], {'relevantes_sem_cb': [int(i) + 1 for i in esc2], 'subconjunto': sub, 'fora_do_gravado': novas})
        print('\n  %s: conjunto relevante recalculado sem o CaBurst_PA1: %d direções (gravado %d); %s' % (D['rot'], len(esc2), len(esc),
              'SUBCONJUNTO do gravado' if sub else 'tem direções FORA do gravado %s (exigiriam simular a aceleração)' % novas))
        for var, qs in (('A (conjunto gravado)', D['qs']), ('B (conjunto recalculado)', [q for q in D['qs'] if D['IDX'][q] - 1 in set(int(i) for i in esc2)] if sub else None)):
            if qs is None: R[var] = 'NÃO CALCULADO (exige simulação)'; continue
            e = estado(D, True, qs); c0 = D['e0']['conjuntos']; R[var] = e
            print('    variante %s: resolvidas pela faixa %s; candidatas NOVAS não testadas além do fator 2: %s%s' % (var, ['v_%d' % x for x in e['DET']], ['v_%d' % x for x in e['candidatas_novas']] or 'nenhuma (PONTO FIXO)',
                  '' if e['ponto_fixo'] else ' → NÃO é ponto fixo: %d avaliações do funcional (~%.0f h de CPU) — PARADO; os números abaixo são LIMITES INFERIORES' % (2 * len(e['candidatas_novas']), 2 * len(e['candidatas_novas']) * H_AVAL)))
            for t in TAUS:
                x = e['conjuntos'][t]; print('      %-9s σ* %-8.4g (%-14s) σ_lin %-8.4g (v_%s) certificado %-8.4g | com o CaBurst: %.4g (×%.2f)' % (
                      nm(t), x['sigma_estrela'], x['limitante'], x['sigma_lin'], x['v_lin'], x['certificado'], c0[t]['certificado'], x['certificado'] / c0[t]['certificado']))
    json.dump(res, open(OUT, 'w'), indent=1, default=float)


if __name__ == '__main__':
    main(sys.argv[1])
