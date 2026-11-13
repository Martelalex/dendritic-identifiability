# hay_common.py — montagem do Hay 2011 (L5PCbiophys3 + cell1) e pontos do D131, para os scripts do D132 itens 6 e 8
# (hay_dt.py, hay_variant.py). Mesmas regras do hay_profile/hay_reduce: nseg = max(regra do Hay, ⌈L/Δ⌉) em TODAS as
# seções, biophys REAPLICADO depois; pontos por nome de seção + arco.
import os, math
import numpy as np
from neuron import h

_loaded = set()


def load(hay):
    if hay in _loaded: return
    h.nrn_load_dll(os.path.join(hay, 'mod', 'x86_64', 'libnrnmech.so'))
    h.load_file('stdrun.hoc'); h.load_file('import3d.hoc')
    h.load_file(os.path.join(hay, 'models', 'L5PCbiophys3.hoc')); h.load_file(os.path.join(hay, 'models', 'L5PCtemplate.hoc'))
    _loaded.add(hay)


def build(hay, delta):
    load(hay)
    cell = h.L5PCtemplate(os.path.join(hay, 'morphologies', 'cell1.asc'))
    for s in cell.all: s.nseg = max(s.nseg, int(math.ceil(s.L / delta)))
    h.L5PCbiophys().biophys(cell)
    h.v_init = -80.0
    return cell


def apical_path(cell):
    soma = cell.soma[0]; dist = lambda seg: h.distance(soma(0.5), seg)
    nk = lambda s: int(h.SectionRef(sec=s).nchild())
    tip = max([s for s in cell.apical if nk(s) == 0], key=lambda s: dist(s(1)))
    path = []; s = tip
    while s is not None and s != soma:
        path.append(s); ps = s.parentseg(); s = ps.sec if ps is not None else None
    return path, dist


def path_points(cell, dists):
    path, dist = apical_path(cell); pts = {}
    for d in dists:
        for s in path:
            d0 = dist(s(0))
            if d0 <= d <= d0 + s.L:
                pts['apical_%d' % d] = {'sec': s.name(), 'arc': d - d0, 'dist': float(d)}; break
    return pts


def hay_sites(cell):
    soma = cell.soma[0]; pts = {}
    for d in (620, 800):
        sl = cell.locateSites('apic', d); best = None
        for i in range(int(sl.count())):
            si, x = int(sl.o(i).x[0]), sl.o(i).x[1]; dd = cell.apic[si](x).diam
            if best is None or dd > best[0]: best = (dd, si, x)
        s = cell.apic[best[1]]
        pts['hay_%d' % d] = {'sec': s.name(), 'arc': best[2] * s.L, 'dist': h.distance(soma(0.5), s(best[2]))}
    return pts


def nodes(cell, pt):
    s = [x for x in cell.all if x.name() == pt['sec']][0]; n = s.nseg; L = s.L
    xs = [0.0] + [(k + 0.5) / n for k in range(n)] + [1.0]; pos = [x * L for x in xs]
    for i in range(len(pos) - 1):
        if pos[i] <= pt['arc'] <= pos[i + 1]:
            if pos[i + 1] == pos[i]: return [(s(xs[i]), 1.0)]
            w = (pt['arc'] - pos[i]) / (pos[i + 1] - pos[i]); return [(s(xs[i]), 1 - w), (s(xs[i + 1]), w)]
    raise ValueError(pt)


class Rest:
    """Repouso (CVode, 3 s, como no D131) salvo; run() recomeça dele com o integrador pedido."""

    def __init__(self, soma_seg):
        self.soma = soma_seg
        h.cvode.active(1); h.finitialize(h.v_init); h.continuerun(3000.0)
        self.ss = h.SaveState(); self.ss.save(); self.TS = h.t; h.cvode.active(0)

    def run(self, tstop, stims, recs, dt=0.025, cvode_atol=None):
        """stims: (lista (seg, w), 'i', amp, atraso rel, dur) | (lista, 'epsp', imax, onset rel, tau1); recs: {nome: lista (seg, w)}."""
        keep = []
        for st in stims:
            for seg, w in st[0]:
                if st[1] == 'i':
                    c = h.IClamp(seg); c.amp = st[2] * w; c.delay = self.TS + st[3]; c.dur = st[4]
                else:
                    c = h.epsp(seg); c.tau0 = 0.5; c.tau1 = st[4]; c.imax = st[2] * w; c.onset = self.TS + st[3]
                keep.append(c)
        vecs = {k: [(h.Vector().record(seg._ref_v), w) for seg, w in rl] for k, rl in recs.items()}
        vs = h.Vector().record(self.soma._ref_v); tv = h.Vector().record(h._ref_t)
        if cvode_atol is not None:
            h.cvode.active(1); h.cvode.atol(cvode_atol)
        else:
            h.cvode.active(0); h.dt = dt
        h.finitialize(h.v_init); self.ss.restore(); h.t = self.TS
        if cvode_atol is not None: h.cvode.re_init()
        h.fcurrent(); h.frecord_init(); h.continuerun(self.TS + tstop)
        o = {'soma': np.array(vs), 't': np.array(tv) - self.TS}
        for k, vl in vecs.items(): o[k] = sum(w * np.array(v) for v, w in vl)
        h.cvode.active(0)
        return o


def at_t(r, k, t):
    return float(np.interp(t, r['t'], r[k]))


def d50(dists, ratios):
    """Distância em que a razão cai a 0.5 (interpolação linear entre pontos consecutivos); None se não cruza."""
    for i in range(len(dists) - 1):
        a, b = ratios[i], ratios[i + 1]
        if a >= 0.5 > b: return dists[i] + (a - 0.5) / (a - b) * (dists[i + 1] - dists[i])
    return None
