# etapaA_F.py — D132 item 66: CONJUNTO FUNCIONAL F da Etapa A (D131 7.4 / D132 item 13) e o TERMO DE VIÉS (item 26),
# UM caminho de código para o Hay de referência (L0 Δ0.5) e para o modelo direto (RegionModel em θ).
#   (a) EPSC 10 pA (mecanismo `epsp` do Hay, τ 0.5/3 ms, início 1 ms) em cada sítio: 30 sorteados (semente 131) + pontos
#       do V2 → pico do EPSP SOMÁTICO (traço − linha de base sem estímulo) e tempo do pico;
#   (b) BAC (1.9 nA × 5 ms no soma a 100 ms + EPSP 0.5 nA τ 0.5/5 no hay_620 a 105 ms) e CaBurst (EPSP 1.5 nA) → tempos
#       dos PA somáticos (detector de PICO) e pico do Ca-spike no hay_620;
#   (c) f-I nos degraus do Hay (0.78 / 1.0 / 1.9 nA × 2 s, início 150 ms) → taxa por ISI (Hz).
# Integração (D132 item 73): CÓDIGO ÚNICO stim_common.CommonSim — repouso assentado ATÉ CONVERGIR, CVode atol 1e-6,
# injeção por play (degrau; α = forma do epsp do Hay) com autoteste; leitura ponderada.
# viés(F_red, F_ref) = F_red − F_ref por componente — a MESMA função na validação e na Etapa A.
# Uso: python .../etapaA_F.py <hay|region> <dir do Hay> <N|Δ> <saida.json>
import sys, os, math, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neuron import h
import etapaA_model as EM
import detect_peak as DP
import points_lib as PL

FI_AMPS = (0.78, 1.0, 1.9)


def sites(cell):
    return {**EM.points_v2(cell), **EM.random_sites(cell, 30, 131)}


class HayRef:
    """Hay completo (biophys3), nseg = max(regra, ⌈L/Δ⌉), pontos SEM divisão (leitura por interpolação entre nós)."""

    def __init__(self, hay, delta):
        EM.load(hay); cell = h.L5PCtemplate(os.path.join(hay, 'morphologies', 'cell1.asc'))
        for s in cell.all: s.nseg = max(s.nseg, int(math.ceil(s.L / delta)))
        h.L5PCbiophys().biophys(cell)
        self.cell = cell; self.PTS = sites(cell); self.SOMA = cell.soma[0](0.5); self.BY = {s.name(): s for s in cell.all}

    def at(self, pt):
        s = self.BY[pt['sec']]; pos, xs = PL.node_positions(s)
        return [(s(xs[i]), w) for i, w in PL.bracket(pos, pt['arc'])]


class Sim:
    """D132 item 73 (1): CÓDIGO ÚNICO — assentamento por critério, injeção e leitura pelo stim_common.CommonSim."""

    def __init__(self, M, settle=None, atol=1e-6, cache_dir=None):   # `settle` (duração) sem efeito: assentamento por critério
        import stim_common as SC
        kw = {} if cache_dir is None else {'cache_dir': cache_dir}
        self.M = M; h.v_init = -80.0; self.C = SC.CommonSim(M.SOMA, verbose=False, atol=atol, **kw)

    def run(self, tstop, stims, rec):
        st2 = [('s', q[3], q[2], q[4], q[0]) if q[1] == 'i' else ('a', q[3], q[2], q[4], q[0]) for q in stims]
        t, o = self.C.run(st2, tstop, rec); o['t'] = t
        return o


def functional_set(M, log=print, fI=True, settle=3000.0, so_epsp=False, sim=None):
    """sim: um Sim já construído NESTE modelo (item 85: o G reaproveita o CommonSim do processo — o chamador fez o
    resettle depois de mudar θ). Sem sim, constrói um (repouso + autotestes)."""
    S = sim if sim is not None else Sim(M, settle); SOMA = [(M.SOMA, 1.0)]; F = {'EPSP_pico': {}, 'EPSP_tpico': {}}
    base = S.run(100.0, [], {'soma': SOMA}); t0 = time.time()
    for k, p in M.PTS.items():
        r = S.run(100.0, [(M.at(p), 'epsp', 0.010, 1.0, 3.0)], {'soma': SOMA})
        d = r['soma'] - np.interp(r['t'], base['t'], base['soma']); i = int(np.argmax(d))
        F['EPSP_pico'][k] = float(d[i]); F['EPSP_tpico'][k] = float(r['t'][i])
    log('EPSP em %d sítios (%.0f s)' % (len(M.PTS), time.time() - t0)); t0 = time.time()
    if so_epsp: return F
    site = M.at(M.PTS['hay_620'])
    for name, stims, stt in (('BAC', [(SOMA, 'i', 1.9, 100.0, 5.0), (site, 'epsp', 0.5, 105.0, 5.0)], [100.0, 105.0]),
                             ('CaBurst', [(site, 'epsp', 1.5, 105.0, 5.0)], [105.0])):
        r = S.run(400.0, stims, {'soma': SOMA, 'hay_620': M.at(M.PTS['hay_620'])})
        dd = DP.detect(r['t'], r['soma'], 90.0, 400.0, stt)
        F[name] = {'picos': [x['peak'] for x in dd], 'n': len(dd), 'Ca_pico': float(r['hay_620'][r['t'] >= 99.0].max())}
    log('BAC/CaBurst (%.0f s): %s' % (time.time() - t0, {n: F[n]['picos'] for n in ('BAC', 'CaBurst')})); t0 = time.time()
    F['fI'] = {}
    for a in (FI_AMPS if fI else ()):
        r = S.run(2300.0, [(SOMA, 'i', a, 150.0, 2000.0)], {'soma': SOMA})
        pk = [x['peak'] for x in DP.detect(r['t'], r['soma'], 150.0, 2150.0, [150.0, 2150.0])]
        F['fI'][str(a)] = {'n': len(pk), 'taxa': float(1000.0 / np.mean(np.diff(pk))) if len(pk) >= 2 else None, 'picos': pk}
        log('f-I %.2f nA: %d PA (%.0f s)' % (a, len(pk), time.time() - t0)); t0 = time.time()
    return F


IDX = {'BAC': 1, 'CaBurst': 0}      # item 39: BAC pelo 2º PA (o 1º é o pulso somático), CaBurst pelo 1º


def fvec(F, K=None):
    """item 85/95: F como VETOR com nomes — a MESMA função para o G (reduzido) e para o termo direto do viés (Hay × reduzido).
    EPSP somático por sítio; 1º PA (BAC 2º, CaBurst 1º); pico do Ca; e, se K ({amp: K} — item 95) for dado, a TAXA CONTÍNUA
    da f-I por amplitude: taxa_K = K / (t_{K+1} − t_1) (NaN se houver menos de K+1 disparos). Devolve (valores, nomes,
    contagens) — as contagens de BAC/CaBurst decidem o condicionamento do 1º PA."""
    keys = sorted(F['EPSP_pico'])
    v = [F['EPSP_pico'][k] for k in keys] + [F['BAC']['picos'][1] if F['BAC']['n'] > 1 else np.nan,
                                            F['CaBurst']['picos'][0] if F['CaBurst']['n'] > 0 else np.nan, F['BAC']['Ca_pico'], F['CaBurst']['Ca_pico']]
    n = ['EPSP_' + k for k in keys] + ['BAC_PA2', 'CaBurst_PA1', 'BAC_Ca', 'CaBurst_Ca']
    c = [0] * len(keys) + [F['BAC']['n'], F['CaBurst']['n'], 0, 0]
    for a in sorted(K or {}, key=float):
        v.append(taxa_K(F['fI'][a]['picos'], K[a])); n.append('taxa_%s' % a); c.append(F['fI'][a]['n'])
    return np.array(v, float), np.array(n), np.array(c)


def taxa_K(picos, K):
    """item 95: 1 / média dos primeiros K ISIs = K / (t_{K+1} − t_1)."""
    t = np.asarray(picos, float)
    return float(K / (t[K] - t[0])) if K >= 1 and len(t) >= K + 1 else np.nan


def K_regra(n_base):
    """item 95: K = contagem na base − 2 (regra declarada antes de olhar contagens)."""
    return int(n_base) - 2


def identidade(t_base, t_x, K):
    """item 95 (ajuste ANTES do G2): os K+1 primeiros disparos existem nos dois e mantêm a identidade, pelos DESLOCAMENTOS
    CONSECUTIVOS: com Δt_i = t_i(x) − t_i(base), |Δt_1| < ½·ISI_1 e |Δt_i − Δt_{i−1}| < ½·ISI_i (base), i = 2…K+1
    (ISI_i = t_i − t_{i−1}; ISI_1 = t_2 − t_1). Uma deriva SUAVE de taxa faz uma RAMPA em Δt (diferenças pequenas); uma
    inserção/remoção faz um SALTO de ~1 ISI (somadas, as duas diferenças em torno do disparo inserido dão 1 ISI → uma delas
    ≥ ½ ISI). O critério anterior (tempos absolutos) recusava escalas de 1.02–1.03 sem inserção. Devolve (ok, pior razão)."""
    tb, tx = np.asarray(t_base, float), np.asarray(t_x, float)
    if K < 1 or len(tb) < K + 1 or len(tx) < K + 1: return False, np.inf
    d = tx[:K + 1] - tb[:K + 1]; isi = np.diff(tb[:K + 1])
    r = np.concatenate(([abs(d[0]) / (0.5 * isi[0])], np.abs(np.diff(d)) / (0.5 * isi)))
    # item 101 (correção): CONTAGEM até o horizonte t_{K+1} + Δt_K + ½·ISI_K da base — uma inserção/remoção no ÚLTIMO intervalo
    # comparado escapava das diferenças consecutivas (o par seguinte não era comparado)
    hor = tb[K] + d[K - 1] + 0.5 * isi[-1]          # horizonte acompanha a deriva medida no disparo anterior
    cnt = int(np.sum(tx < hor)) == K + 1
    return bool(np.all(r < 1.0) and cnt), float(r.max())


def vies(Fr, F0):
    """TERMO DE VIÉS DIRETO da Etapa A (item 26: F_Hay − F_red(θ_verd) entra com sinal oposto): r = F_red − F_ref, por
    componente, nas unidades do critério. Usado IGUAL na validação do modelo direto e na Etapa A."""
    r = {'EPSP_pico_rel': {k: Fr['EPSP_pico'][k] / F0['EPSP_pico'][k] - 1 for k in F0['EPSP_pico'] if k in Fr['EPSP_pico']},
         'EPSP_tpico_ms': {k: Fr['EPSP_tpico'][k] - F0['EPSP_tpico'][k] for k in F0['EPSP_tpico'] if k in Fr['EPSP_tpico']}}
    for n in ('BAC', 'CaBurst'):
        i = IDX[n]; ok = Fr[n]['n'] == F0[n]['n'] and F0[n]['n'] > i
        r[n] = {'contagem': (Fr[n]['n'], F0[n]['n']), 'PA_ms': (Fr[n]['picos'][i] - F0[n]['picos'][i]) if ok else None,
                'Ca_pico_mV': Fr[n]['Ca_pico'] - F0[n]['Ca_pico']}
    r['fI_taxa_rel'] = {a: (Fr['fI'][a]['taxa'] / F0['fI'][a]['taxa'] - 1) if (Fr['fI'][a]['taxa'] and F0['fI'][a]['taxa']) else None for a in F0['fI']}
    return r


if __name__ == '__main__':
    which, hay, par, out = sys.argv[1:5]; hay = os.path.abspath(hay); t0 = time.time()
    M = HayRef(hay, float(par)) if which == 'hay' else EM.RegionModel(hay, int(par), sites)
    print('%s %s: %d sítios, %d segmentos (%.0f s)' % (which, par, len(M.PTS), (M.nseg if which != 'hay' else sum(s.nseg for s in M.cell.all)), time.time() - t0), flush=True)
    F = functional_set(M, log=lambda m: print(m, flush=True))
    F['_meta'] = {'modelo': which, 'par': par, 'theta': getattr(M, 'theta', None)}
    json.dump(F, open(out, 'w'), indent=1, default=float); print('total %.0f s' % (time.time() - t0))
