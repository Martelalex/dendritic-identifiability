# ref_ii_C.py — D132 item 83 (1): a tarefa C do ref_ii (AIS × axônio distal, Allen/Hay4; desenho do item 49) pelo RUNNER
# da Etapa A — gravação por subpasso, retomada, portão de memória. Antes era um laço de várias horas que recomeçava do
# zero a cada queda (pv_C e hay4_C perdidos no reinício de 07/10).
# Unidade = a célula ('<modelo>_C'); subpassos EM ORDEM (dependem dos anteriores; rodar SÓ em série, sem --sub-worker):
#   Ap, Aa  — limiares de 1 PA (pulso 1 ms; PSC α τd 3) por bissecção; cada sonda guardada (sondas.json, escrita atômica)
#             → a retomada repete a MESMA trajetória sem resimular;
#   tpk     — pico do PA do pulso 1.5 Ap;
#   cen_000…cen_073 — os 74 cenários (S1 par pulso+α; S2 bloqueio; S3 bombardeio, rng 12345), um por subpasso;
#   neg_0…neg_3 — controle negativo: a MESMA célula passiva, estímulo sozinho nas amplitudes usadas.
# Simulação pelo código ÚNICO (stim_common.CommonSim: repouso convergido, parada forçada, autoteste de início tardio);
# traços numa grade de 5 µs (200 kHz). Redução = o JSON de antes (Ap, Aa, eventos, bimodalidade, controle negativo).
import os, json
import numpy as np
from scipy.signal import find_peaks
from neuron import h
import detect_peak as DP
import stim_common as SC
import ref_ii_cells as RC

NEG = (('pulso 1 ms × Ap', 's', 'Ap', 1.0, 1.0), ('pulso 1 ms × 1.5 Ap', 's', 'Ap', 1.5, 1.0),
       ('α τd 3 × Aa', 'a', 'Aa', 1.0, 3.0), ('α τd 3 × 2 Aa', 'a', 'Aa', 2.0, 3.0))


def scenarios(model, Ap, Aa, tpk):
    scen = []
    for d in range(2, 16):
        for f in (0.5, 1.0, 1.5, 2.0): scen.append(('S1', [('s', 50.0, 1.5 * Ap, 1.0), ('a', tpk + d, f * Aa, 3.0)], 120.0))
    for B in (1.5, 3.0):
        for f in (0.5, 1.0, 2.0):
            scen.append(('S2', [('s', 50.0, B * RC.RHEO[model], 300.0)] + [('a', tt, f * Aa, 3.0) for tt in np.arange(70.0, 350.0, 20.0)], 400.0))
    rng = np.random.default_rng(12345)
    for f in (0.1, 0.2, 0.4):
        for rate in (200.0, 500.0, 1000.0, 2000.0):
            ts = 50.0 + np.cumsum(rng.exponential(1000.0 / rate, size=int(rate * 1.2)))
            scen.append(('S3', [('a', float(x), f * Aa, 3.0) for x in ts[ts < 1050.0]], 1100.0))
    return scen


N_SCEN = 14 * 4 + 2 * 3 + 3 * 4


def bimodal(x):
    xs = np.sort(x); best = None
    for a in np.arange(xs.min(), xs.max() - 20.0, 0.25):
        if np.mean((xs >= a) & (xs < a + 20.0)) < 0.01 and np.mean(xs < a) >= 0.05 and np.mean(xs >= a + 20.0) >= 0.05:
            b = a + 20.0
            while b + 0.25 <= xs.max() and np.mean((xs >= a) & (xs < b + 0.25)) < 0.01: b += 0.25
            if best is None or b - a > best[1] - best[0]: best = (a, b)
    return best


class RefC:
    def __init__(self, model, fout, log=print):
        self.model, self.fout, self.log = model, fout, log
        c = RC.build(model, passive=False); self.cell = c
        self.recs = {k: [(c[k], 1.0)] for k in ('soma', 'ais', 'dist')}
        # pulso do autoteste SUBLIMIAR por modelo (o toyC dispara com 0.2 nA — o autoteste recusou, corretamente)
        self.sim = SC.CommonSim(c['soma'], atol=1e-6, test_amp=0.005 if model == 'toyC' else 0.2)   # construído SEMPRE
        self.passive = False; self.settle_active = self.sim.settle_info

    def units(self): return ['%s_C' % self.model]

    def substeps(self, u):
        return ['Ap', 'Aa', 'tpk'] + ['cen_%03d' % i for i in range(N_SCEN)] + ['neg_%d' % i for i in range(len(NEG))]

    def run(self, stims, tstop):
        return self.sim.run(stims, tstop, self.recs, rec_grid=0.005)

    def _get(self, ud, name):
        f = os.path.join(ud, '%s.npz' % name)
        if not os.path.exists(f): raise RuntimeError('subpasso %s ausente — a tarefa C roda só em série' % name)
        return float(np.load(f)['v'])

    def _bisect(self, ud, kind, par):
        memo_f = os.path.join(ud, 'sondas.json'); memo = json.load(open(memo_f)) if os.path.exists(memo_f) else {}

        def spikes(A):
            k = '%s|%r|%r' % (kind, par, A)
            if k not in memo:
                t, V = self.run([(kind, 50.0, A, par)], 150.0); memo[k] = len(DP.detect(t, V['soma'], 0.0, float(t[-1]), []))
                tmp = memo_f + '.tmp%d' % os.getpid(); json.dump(memo, open(tmp, 'w')); os.replace(tmp, memo_f)
            return memo[k]
        lo, hi = 0.0, 0.5
        while spikes(hi) == 0: hi *= 2
        for _ in range(12):
            mid = 0.5 * (lo + hi)
            if spikes(mid) > 0: hi = mid
            else: lo = mid
        return hi

    def evaluate(self, u, s, ud):
        if s.startswith('neg_'):
            if not self.passive:
                RC.passivate(); self.sim = SC.CommonSim(self.cell['soma'], atol=1e-6); self.passive = True
            lab, kind, which, f, par = NEG[int(s[4:])]; A = f * self._get(ud, which)
            t, V = self.run([(kind, 50.0, A, par)], 150.0)
            return {'n': np.array(len(DP.detect(t, V['soma'], 0.0, float(t[-1]), [50.0, 51.0] if kind == 's' else [])))}
        if self.passive: raise RuntimeError('célula já passiva neste processo — ordem dos subpassos violada')
        if s == 'Ap': return {'v': np.array(self._bisect(ud, 's', 1.0))}
        if s == 'Aa': return {'v': np.array(self._bisect(ud, 'a', 3.0))}
        if s == 'tpk':
            Ap = self._get(ud, 'Ap'); t, V = self.run([('s', 50.0, 1.5 * Ap, 1.0)], 100.0)
            return {'v': np.array(DP.detect(t, V['soma'], 0, 100, [50.0, 51.0])[0]['peak'])}
        i = int(s[4:]); sc, stims, tstop = scenarios(self.model, self._get(ud, 'Ap'), self._get(ud, 'Aa'), self._get(ud, 'tpk'))[i]
        t, V = self.run(stims, tstop); tt = np.arange(0.0, t[-1], 0.025)
        va = np.interp(tt, t, V['ais']); vd = np.interp(tt, t, V['dist'])
        pk, _ = find_peaks(va, prominence=2.0); w5 = int(5.0 / 0.025); a_ais, a_d = [], []
        for k in pk:
            a_ais.append(va[k] - va[max(0, k - w5):k + 1].min())
            j0 = max(0, k - w5); j1 = min(len(vd), k + int(2.0 / 0.025))
            a_d.append(vd[max(0, k - int(0.5 / 0.025)):j1].max() - vd[j0:k + 1].min())
        return {'tipo': np.array(sc), 'a_ais': np.array(a_ais, float), 'a_d': np.array(a_d, float)}

    def reduce(self, u, subs, ud):
        ev = {'S1': [], 'S2': [], 'S3': []}
        for i in range(N_SCEN):
            z = subs['cen_%03d' % i]; ev[str(z['tipo'])] += [(float(a), float(b)) for a, b in zip(z['a_ais'], z['a_d'])]
        Ap, Aa = float(subs['Ap']['v']), float(subs['Aa']['v'])
        out = {'model': self.model, 'task': 'C', 'repouso': self.settle_active,
               'C': {'Ap_nA': Ap, 'Aa_nA': Aa, 'tpk_ms': float(subs['tpk']['v']), 'eventos': ev}}
        allv = np.array([x for L_ in ev.values() for x in L_]).reshape(-1, 2)
        for lab, col in (('AIS', 0), ('distal', 1)):
            x = allv[:, col]; b = bimodal(x) if len(x) else None
            hh, _ = np.histogram(x, bins=np.arange(0, max(130, (x.max() if len(x) else 0) + 5), 5))
            self.log('%s %s: %d eventos | histograma (5 mV): %s' % (self.model, lab, len(x), ' '.join(str(int(c)) for c in hh)))
            self.log('   → %s' % ('BIMODAL: lacuna %.1f–%.1f mV → limiar %.1f mV' % (b[0], b[1], (b[0] + b[1]) / 2) if b else 'NÃO bimodal pelo critério declarado'))
            out['C']['bimodal_' + lab] = None if b is None else {'lacuna': b, 'limiar_mV': (b[0] + b[1]) / 2}
        neg = {NEG[k][0]: int(subs['neg_%d' % k]['n']) for k in range(len(NEG))}
        out['C']['controle_negativo'] = {'deteccoes_no_passivo': neg, 'limiares_suspeitos': any(neg.values())}
        self.log('%s controle negativo (passivo, estímulo sozinho): %s → %s' % (self.model, neg, 'LIMIARES SUSPEITOS' if any(neg.values()) else 'zero detecções'))
        tmp = self.fout + '.tmp%d' % os.getpid(); json.dump(out, open(tmp, 'w'), indent=1, default=float); os.replace(tmp, self.fout)
        return {'Ap': np.array(Ap), 'Aa': np.array(Aa), 'eventos': allv}
