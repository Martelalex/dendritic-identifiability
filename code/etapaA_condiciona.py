# etapaA_condiciona.py — D132 item 146: CONDICIONAMENTO DOS PROTOCOLOS POR PONTO (regras do item 144; condições (a)–(c) do item 146), no θ base,
# pelo MESMO código das unidades (EtapaAUnit._run: o mesmo repouso da cache, CVode, os mesmos estímulos e tempos do M1 e do M4).
#   (b) M1: R_in por ±10 pA (média 1050–1100 ms) → I = ΔV_alvo/R_in (5 mV); simetria ρ_I = máx|y₊ + y₋| / máx|y₊ − y₋| no ponto ≤ RHO_MAX (0.1);
#       falhou → alvo à METADE (no máximo 2 vezes); falhou a 1.25 mV → o ponto NÃO passa.
#   (a) M4: limiar local (deflexão de pico no ponto ≥ 1.5 × a predição linear de 0.02 nA; grade 0.02·1.25^k até 3 nA + bisseção 0.25%); 0.5×, 0.9×,
#       1.2× o limiar; teto +60 mV (ponto e soma); teste de cada amplitude em A × (0.98 … 1.02): contagem e identidade estáveis, cada tempo usado
#       < 1 ms por 1%; falhou → passo de 0.1× o limiar PARA LONGE do limiar (≤ 3); sem amplitude que passe → omitida.
#   (c) bordas: nas amplitudes finais do M1 (±I), as 504 leituras pela cadeia + detector → nenhum disparo; amostras retiradas = liga/desliga.
#   Reportado ao lado (--antigo <dir da unidade gravada>): no protocolo ANTIGO (50 pA), a leitura do ponto foi cortada pelo detector?
# As funções de critério recebem um simulador `sim(tipo, amp, leituras) → (t, Y absoluto)` — testadas com respostas sintéticas de resposta
# conhecida em etapaA_condiciona_teste.py ANTES do uso.
# Uso: python3 neuron/lancar.py distal -- .nrnvenv/bin/python neuron/etapaA_condiciona.py <dir do Hay> <cache> <ponto> <saida.json> [--antigo <dir>]
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU

M1, M4, DT = EU.M1, EU.M4, EU.DT
I_RIN = 0.01; JAN = (1050.0, 1100.0); ALVO = 5.0; RHO = EU.RHO_MAX; METADES = 2           # (b)
A_LIN = 0.02; SUPRA = 1.5; GRADE = 1.25; A_MAX = 3.0; REL = 0.0025; TETO = 60.0               # limiar local e teto (item 144)
FATORES = (0.5, 0.9, 1.2); PASSO = 0.1; NPASSOS = 3; PERT = (0.98, 0.99, 1.0, 1.01, 1.02); LAT_MAX = 1.0   # (a)
ANTIGAS = (0.2, 0.5, 1.5)
_k = lambda f: '%.2f' % f


# ------------------------------------------------------------------------------------------------ (b) M1
def rin(sim, p):
    """R_in (MΩ = mV/nA) no ponto: (V̄₊ − V̄₋)/(2·I_RIN), V̄ = média da deflexão (linha de base pré-estímulo) na janela JAN."""
    i0, i1 = EU._ix(JAN[0]), EU._ix(JAN[1]); v = {}
    for sg in (1, -1):
        _, Y = sim('M1', sg * I_RIN, [p]); y = Y[0] - Y[0, EU.pre_index('M1p')]; v[sg] = float(y[i0:i1].mean())
    return (v[1] - v[-1]) / (2 * I_RIN), v


def rho_I(yp, ym):
    """Índice de 2ª diferença no eixo da AMPLITUDE (a resposta sem estímulo é 0): máx_t|y₊ + y₋| / máx_t|y₊ − y₋| (por linha)."""
    yp, ym = np.atleast_2d(yp), np.atleast_2d(ym)
    return np.abs(yp + ym).max(-1) / np.maximum(np.abs(yp - ym).max(-1), 1e-300)


def m1_condiciona(sim, p):
    R, vb = rin(sim, p); alvo = ALVO; hist = []
    for _ in range(METADES + 1):
        I = alvo / R
        _, Yp = sim('M1', I, [p]); _, Ym = sim('M1', -I, [p])
        yp, ym = EU.cadeia(Yp[0], 'M1p'), EU.cadeia(Ym[0], 'M1m'); r = float(rho_I(yp, ym)[0])
        ye = Yp[0] - Yp[0, EU.pre_index('M1p')]
        hist.append({'alvo_mV': alvo, 'I_nA': I, 'rho_I': r, 'deflexao_estacionaria_mV': float(ye[EU._ix(JAN[0]):EU._ix(JAN[1])].mean()),
                     'passa': bool(r <= RHO)})
        if r <= RHO: return {'R_in_MOhm': R, 'V_10pA': {str(k): x for k, x in vb.items()}, 'I_nA': I, 'alvo_mV': alvo, 'passa': True, 'historico': hist}
        alvo /= 2.0
    return {'R_in_MOhm': R, 'V_10pA': {str(k): x for k, x in vb.items()}, 'I_nA': None, 'alvo_mV': None, 'passa': False, 'historico': hist}


# ------------------------------------------------------------------------------------------------ (a) M4
def limiar_local(defl, vmax=None):
    """defl(A) → deflexão de pico NO PONTO. Menor A com defl(A) ≥ SUPRA × (defl(A_LIN)·A/A_LIN): grade A_LIN·GRADE^k até A_MAX, bisseção até REL.
    ITEM 156 (opção A do Martel): com vmax(A) dado, o limiar só é procurado DENTRO da faixa fisiológica — em cada A da grade a razão é testada PRIMEIRO (o
    mesmo de antes) e, se não houver evento, a grade PARA quando vmax(A) > TETO: devolve (None, motivo, (lo, A)) com o par que cerca o teto."""
    d0 = defl(A_LIN); razao = lambda A: defl(A) / (d0 * A / A_LIN)
    lo = A_LIN; k = 1
    while True:
        A = A_LIN * GRADE ** k; k += 1
        if A > A_MAX * (1 + 1e-12): return None, 'sem supralinearidade de %.0f%% até %.2f nA' % (100 * (SUPRA - 1), A_MAX)
        if razao(A) >= SUPRA: hi = A; break
        if vmax is not None and vmax(A) > TETO:
            return None, 'SEM evento local na faixa fisiológica (V passa de +%g mV a %.4f nA antes de supralinearidade de %.0f%%)' % (TETO, A, 100 * (SUPRA - 1)), (lo, A)
        lo = A
    while (hi - lo) / lo > REL:
        mid = 0.5 * (lo + hi)
        if razao(mid) >= SUPRA: hi = mid
        else: lo = mid
    return hi, 'bisseção [%.5f; %.5f] nA' % (lo, hi)


def teto(vmax, lo, hi):
    """Maior A em [lo, hi] com vmax(A) ≤ TETO (vmax(lo) ≤ TETO < vmax(hi)), bisseção até REL."""
    while (hi - lo) / lo > REL:
        mid = 0.5 * (lo + hi)
        if vmax(mid) <= TETO: lo = mid
        else: hi = mid
    return lo


def tempos(ev, r, base='1.00'):
    """Tempos (ms) dos K disparos da base em cada avaliação, pelo MESMO caminho da representação (nível fixado na base, cruzamento interpolado)."""
    yb = ev[base][r]; sb = EU.disparos(yb); L = [yb[q['i_on']] + 0.5 * (yb[q['i_pk']] - yb[q['i_on']]) for q in sb]
    out = {}
    for k, Y in ev.items():
        sp = EU.disparos(Y[r]); out[k] = [EU._cruza(Y[r], sp[i], L[i]) if i < len(sp) else None for i in range(len(sb))]
    return out


def testa_amp(tracos, A):
    """(a) do item 146. tracos(A) → Y (2, T) ABSOLUTOS (ponto, soma) do M4. Passa se, em cada leitura, a contagem do detector é a mesma nas 5
    amplitudes A × PERT, a identidade da representação vale (havendo disparos) e cada tempo usado muda < LAT_MAX ms por 1%."""
    ev = {_k(f): EU.cadeia(tracos(A * f), 'M4') for f in PERT}
    _, inf = EU.representar(ev, base='1.00'); res = []; ok = True
    for r in range(2):
        cont = {k: len(EU.disparos(ev[k][r])) for k in ev}; K = inf['n_disparos'][r]
        ident = len(set(cont.values())) == 1 and (K == 0 or bool(inf['tempos_ok'][r]))
        dlat = []
        if ident and K:
            tm = tempos(ev, r); dlat = [(tm['1.01'][i] - tm['0.99'][i]) / 2.0 for i in range(K)]
        lat = all(abs(x) < LAT_MAX for x in dlat); res.append({'contagens': cont, 'K': K, 'identidade': ident, 'dlat_ms_por_1pct': dlat, 'latencia_ok': lat})
        ok &= ident and lat
    return bool(ok), res


FRAC_TETO = (0.25, 0.5, 0.9)   # item 156 (opção A): sem evento local na faixa → frações da amplitude-teto A_teto (a maior com V ≤ +60 mV)


def escolhe_m4(lim, vmax, testa, a_teto=None):
    """Amplitudes do M4 (item 146 (a)). lim: limiar local (None → as ANTIGAS); vmax(A): V absoluta máx (ponto, soma); testa(A) → (passa, detalhe).
    ITEM 156: lim None COM a_teto (sem evento local na faixa) → FRAC_TETO × a_teto, o MESMO teste (a), passo de 0.1 × a_teto para BAIXO (≤ 3), sem amplitude
    que passe → omitida. Devolve (amplitudes aceitas em ordem, registro por amplitude pedida)."""
    reg = []; acc = []
    if lim is None and a_teto is not None:
        for f0 in FRAC_TETO:
            tent = []; final = None
            for st in range(NPASSOS + 1):
                f = round(f0 - PASSO * st, 10)
                if f <= 0: break
                A = f * a_teto; v = vmax(A)
                if v > TETO: tent.append({'fator_teto': f, 'A': A, 'vmax': v, 'passa': False, 'detalhe': 'teto'}); continue
                ok, det = testa(A); tent.append({'fator_teto': f, 'A': A, 'vmax': v, 'passa': ok, 'detalhe': det})
                if ok: final = A; break
            reg.append({'pedida': 'teto×%g' % f0, 'tentativas': tent, 'final': final})
            if final is not None: acc.append(final)
        return sorted(acc), reg
    if lim is None:
        for A in ANTIGAS:
            v = vmax(A); ok, det = (testa(A) if v <= TETO else (False, 'teto'))
            reg.append({'pedida': A, 'tentativas': [{'A': A, 'vmax': v, 'passa': ok, 'detalhe': det}], 'final': A if ok else None})
            if ok: acc.append(A)
        return acc, reg
    for f0 in FATORES:
        sent = -1 if f0 < 1 else 1; tent = []; final = None; ant = None
        for st in range(NPASSOS + 1):
            f = round(f0 + sent * PASSO * st, 10); A = f * lim; v = vmax(A)
            if v > TETO:
                if sent < 0: tent.append({'fator': f, 'A': A, 'vmax': v, 'passa': False, 'detalhe': 'teto'}); continue
                base = ant if ant is not None else lim
                if vmax(base) > TETO: tent.append({'fator': f, 'A': A, 'vmax': v, 'passa': False, 'detalhe': 'teto já em %.4f nA' % base}); break
                A = teto(vmax, base, A); v = vmax(A)
                if A <= lim * (1 + 1e-12): tent.append({'fator': A / lim, 'A': A, 'vmax': v, 'passa': False, 'detalhe': 'teto ≤ 1.0× o limiar'}); break
                ok, det = testa(A); tent.append({'fator': A / lim, 'A': A, 'vmax': v, 'passa': ok, 'detalhe': det, 'no_teto': True})
                if ok: final = A
                break                                                       # para cima, nada além do teto
            ok, det = testa(A); tent.append({'fator': f, 'A': A, 'vmax': v, 'passa': ok, 'detalhe': det}); ant = A
            if ok: final = A; break
        reg.append({'pedida': f0, 'tentativas': tent, 'final': final})
        if final is not None: acc.append(final)
    return sorted(acc), reg


# ------------------------------------------------------------------------------------------------ (c) bordas
def detecta(Yc, nomes):
    """Leituras (após a cadeia) com algum disparo detectado: [(nome, [(t_início ms, pico ms), …])]."""
    out = []
    for r, n in enumerate(nomes):
        sp = EU.disparos(Yc[r])
        if sp: out.append((n, [(q['i_on'] * DT, q['i_pk'] * DT) for q in sp]))
    return out


def bordas(sim, p, leituras, I):
    t, Yp = sim('M1', I, leituras); _, Ym = sim('M1', -I, leituras)
    disc = [EU._ix(x) for x in EU.PROT['M1p'][1]]
    instantes = [float(t[i]) for i in disc]; inst_ok = all(abs(a - b) < 1e-9 for a, b in zip(instantes, (M1['delay'], M1['delay'] + M1['dur'])))
    Cp, Cm = EU.cadeia(Yp, 'M1p'), EU.cadeia(Ym, 'M1m'); dp, dm = detecta(Cp, leituras), detecta(Cm, leituras)
    rr = rho_I(Cp, Cm); ip = leituras.index(p)
    return {'passa': not dp and not dm and inst_ok, 'detectados_M1p': dp[:20], 'detectados_M1m': dm[:20], 'n_leituras_com_disparo': len(dp) + len(dm),
            'instantes_retirados_ms': instantes, 'instantes_ok': inst_ok, 'rho_I_ponto': float(rr[ip]), 'rho_I_max_leituras': float(rr.max()),
            'rho_I_max_em': leituras[int(np.argmax(rr))]}


def antigo(ud, ip, subs):
    """Protocolo ANTIGO (gravado): o corte da voltagem na leitura do ponto (a mesma regra da representação: a última amostra antes do 1º
    disparo detectado em QUALQUER das avaliações) em M1m e M1p."""
    out = {}
    for lab in ('M1m', 'M1p'):
        first = []
        for sn in subs:
            y = EU.cadeia(np.load(os.path.join(ud, '%s.%s.npy' % (sn, lab)), mmap_mode='r')[ip], lab); sp = EU.disparos(y)
            if sp: first.append((sp[0]['i_on'], sn))
        T = EU.cadeia(np.load(os.path.join(ud, 'base.%s.npy' % lab), mmap_mode='r')[ip], lab).shape[-1]
        if first:
            i, sn = min(first); out[lab] = {'cortada': True, 'corte_amostra': max(0, i - 1), 'de': T, 'avaliacoes_com_disparo': len(first), 'primeira': sn}
        else: out[lab] = {'cortada': False, 'de': T}
    return out


if __name__ == '__main__':
    from neuron import h
    HAY, CACHE, PONTO, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3], sys.argv[4]
    arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    t0 = time.time(); u = EU.EtapaAUnit(HAY, only=[PONTO], atol=1e-8, cache_dir=CACHE); U = 'p_' + PONTO
    u._apply(U, 'base'); info = u._sim(U); sp = u.site[PONTO]; nsim = [0]
    print('%s: repouso %s' % (PONTO, info), flush=True)

    def sim(kind, amp, reads):                                             # os MESMOS estímulos de EtapaAUnit.protocols
        nsim[0] += 1
        if kind == 'M1': return u._run([('s', M1['delay'], amp, M1['dur'], sp)], M1['tstop'], reads)
        return u._run([('a', M4['onset'], amp, M4['taud'], sp)], M4['tstop'], reads)

    memo = {}

    def m4(A):                                                             # item 157: simulação ABORTADA por um guarda → traço sintético +∞
        A = round(float(A), 9)                                             # (fora do físico: passa do teto, reprova no teste) e registrada
        if A not in memo:
            try: memo[A] = sim('M4', A, [PONTO, 'soma'])[1]
            except EU.SC.SimulacaoAbortada as e:
                memo[A] = np.full((2, EU._ix(M4['tstop']) + 1), np.inf); res.setdefault('abortadas', []).append({'A': A, 'motivo': str(e)})
                print('   simulação ABORTADA em A = %.5f nA: %s' % (A, e), flush=True)
        return memo[A]
    res = {'ponto': PONTO, 'repouso': info}
    try: res['M1'] = m1_condiciona(sim, PONTO)
    except EU.SC.SimulacaoAbortada as e:                                   # item 157: o ponto NÃO passa (b); registrado
        res['M1'] = {'R_in_MOhm': float('nan'), 'V_10pA': {'1': float('nan'), '-1': float('nan')}, 'I_nA': None, 'alvo_mV': None, 'passa': False,
                     'historico': [{'alvo_mV': None, 'I_nA': None, 'rho_I': float('nan'), 'passa': False}], 'abortada': str(e)}
        print('(b) M1: simulação ABORTADA — %s' % e, flush=True)
    m = res['M1']
    if 'abortada' not in m: print('(b) M1: R_in %.1f MΩ (±10 pA: %+.3f / %+.3f mV) | %s' % (m['R_in_MOhm'], m['V_10pA']['1'], m['V_10pA']['-1'], ' → '.join(
        'alvo %.2f mV: I %.4f nA, ρ_I %.4f %s' % (x['alvo_mV'], x['I_nA'], x['rho_I'], '✔' if x['passa'] else '✘') for x in m['historico'])), flush=True)
    i0 = EU.pre_index('M4')
    vmax = lambda A: float(m4(A).max())
    r_lim = limiar_local(lambda A: float((m4(A)[0] - m4(A)[0, i0]).max()), vmax)   # item 156: só na faixa fisiológica
    lim, como = r_lim[0], r_lim[1]; a_teto = None
    if lim is None and len(r_lim) > 2:                                     # sem evento na faixa → amplitude-teto por bisseção (0.25%)
        a_teto = teto(vmax, *r_lim[2]); como += '; A_teto = %.4f nA (V máx %.1f mV)' % (a_teto, vmax(a_teto))
    res['M4_limiar'] = lim; res['M4_limiar_como'] = como; res['M4_A_teto'] = a_teto
    print('(a) M4: limiar local %s (%s)' % ('NENHUM' if lim is None else '%.4f nA' % lim, como), flush=True)
    amps, reg = escolhe_m4(lim, vmax, lambda A: testa_amp(m4, A), a_teto)
    res['M4'] = amps; res['M4_registro'] = reg
    for x in reg:
        print('   pedida %s → %s | %s' % (x['pedida'], 'OMITIDA' if x['final'] is None else '%.4f nA' % x['final'], '; '.join(
            '%.2f×%s %.4f nA Vmáx %.1f mV %s' % (tt.get('fator', tt.get('fator_teto', 0)), '' if 'fator' in tt else ' teto', tt['A'], tt['vmax'], '✔' if tt['passa'] else '✘ (%s)' % (tt['detalhe'] if isinstance(tt['detalhe'], str)
            else ' / '.join('K %d ident %s dlat %s' % (d['K'], d['identidade'], ['%.3f' % z for z in d['dlat_ms_por_1pct']]) for d in tt['detalhe'])))
            for tt in x['tentativas'])), flush=True)
    res['M4_detalhe_final'] = {('%.6f' % A): {'vmax_mV': vmax(A), 'disparos_ponto': len(EU.disparos(EU.cadeia(m4(A), 'M4')[0])),
                                               'disparos_soma': len(EU.disparos(EU.cadeia(m4(A), 'M4')[1]))} for A in amps}
    if m['passa']:
        try: res['bordas'] = bordas(sim, PONTO, u.read, m['I_nA'])
        except EU.SC.SimulacaoAbortada as e: res['bordas'] = {'passa': False, 'abortada': str(e), 'n_leituras_com_disparo': -1, 'instantes_retirados_ms': [], 'instantes_ok': False,
                                                              'rho_I_ponto': float('nan'), 'rho_I_max_leituras': float('nan'), 'rho_I_max_em': '—'}
        b = res['bordas']
        print('(c) bordas (±%.4f nA, %d leituras): disparos detectados em %d leituras; instantes retirados %s ms (%s) → %s | ρ_I no ponto %.4f, máx nas leituras %.4f (%s)' % (
            m['I_nA'], len(u.read), b['n_leituras_com_disparo'], b['instantes_retirados_ms'], 'ok' if b['instantes_ok'] else 'ERRADOS',
            'PASSA' if b['passa'] else 'FALHA', b['rho_I_ponto'], b['rho_I_max_leituras'], b['rho_I_max_em']), flush=True)
    if arg('--antigo'):
        subs = ['base'] + ['%s_%s' % (n, g) for n in EU.EM.THETA_NAMES for g in ('mais', 'menos')]
        res['antigo'] = antigo(os.path.abspath(arg('--antigo')), u.read.index(PONTO), subs)
        print('antigo (50 pA, gravado): %s' % '; '.join('%s %s' % (lab, ('CORTADA na amostra %d de %d (%d avaliações com disparo; 1ª: %s)' % (
            x['corte_amostra'], x['de'], x['avaliacoes_com_disparo'], x['primeira'])) if x['cortada'] else 'inteira') for lab, x in res['antigo'].items()), flush=True)
    u._restore_geometry(); res['simulacoes'] = nsim[0]; res['s'] = round(time.time() - t0, 1)
    json.dump(res, open(OUT, 'w'), indent=1, default=float)
    print('FIM %s: %d simulações, %.0f s' % (PONTO, nsim[0], time.time() - t0), flush=True)
