# etapaA_model.py — D132 item 66: MODELO DIRETO DA ETAPA A — Hay (L5PCbiophys3 + cell1) em NEURON nativo, N por ramo,
# NÓS NOS PONTOS DE MEDIDA (regra de desenho, item 58), parametrizado pelos 30 parâmetros POR REGIÃO do D131 7.1 com as
# FORMAS espaciais do Hay fixas (nível 1): exponencial do Ih apical, zonas de Ca 685–885 µm, uniformes por região.
# Convenção de distância das formas = a do código do Hay: `distribute_channels` chama `getLongestBranch("apic")`, que
# põe a ORIGEM em apic[0](0) (não no soma); a distância normalizada do Ih divide pelo maior distance(1) das pontas
# apicais a partir dessa origem. Compartilhado com `hay_native.py` (split_section, points — um caminho de código só).
import os, math
import sys as _sys; _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import porta  # noqa: F401 — D132 item 123 (4): recusa (SystemExit 77) processo lançado por fora do ponto único neuron/lancar.py
import numpy as np
from neuron import h
import points_lib as PL

MECHS = ['Ca_LVAst', 'Ca_HVA', 'SKv3_1', 'SK_E2', 'K_Tst', 'K_Pst', 'Nap_Et2', 'NaTa_t', 'CaDynamics_E2', 'Ih', 'Im']
_loaded = set()


def load(hay):
    if hay in _loaded: return
    h.nrn_load_dll(os.path.join(hay, 'mod', 'x86_64', 'libnrnmech.so')); h.load_file('stdrun.hoc'); h.load_file('import3d.hoc')
    h.load_file(os.path.join(hay, 'models', 'L5PCbiophys3.hoc')); h.load_file(os.path.join(hay, 'models', 'L5PCtemplate.hoc'))
    _loaded.add(hay)


# ------------------------------------------------------------------ θ: os 30 parâmetros (D131 7.1)
THETA_TRUE = {
    # passivo por região (8)
    'g_pas_soma': 3.38e-5, 'g_pas_axon': 3.25e-5, 'g_pas_basal': 4.67e-5, 'g_pas_apical': 5.89e-5,
    'cm_somaaxon': 1.0, 'cm_dend': 2.0, 'Ra': 100.0, 'e_pas': -90.0,
    # soma (11)
    'soma_NaTa_t': 2.04, 'soma_Nap_Et2': 0.00172, 'soma_K_Pst': 0.00223, 'soma_K_Tst': 0.0812, 'soma_SKv3_1': 0.693,
    'soma_SK_E2': 0.0441, 'soma_Ca_HVA': 0.000992, 'soma_Ca_LVAst': 0.00343, 'soma_Ih': 0.0002,
    'soma_gamma': 0.000501, 'soma_decay': 460.0,
    # apical (10)
    'apic_NaTa_t': 0.0213, 'apic_SKv3_1': 0.000261, 'apic_SK_E2': 0.0012, 'apic_Im': 0.0000675,
    'apic_Ca_LVAst_zona': 0.0187, 'apic_Ca_HVA_zona': 0.000555, 'apic_gamma': 0.000509, 'apic_decay': 122.0,
    'apic_Ih_amp': 0.0002, 'apic_Ih_escala': 1.0,     # escala de comprimento RELATIVA (1 = a do Hay: expoente 3.6161/θ)
    # basal (1)
    'basal_Ih': 0.0002,
}
THETA_NAMES = list(THETA_TRUE)
assert len(THETA_NAMES) == 30


def typ(s):
    return s.name().split('.')[-1].split('[')[0].split('_x')[0]


# ------------------------------------------------------------------ geometria: divisão nos pontos (item 59)
def split_section(sec, arcs, key, mechs=MECHS):
    """Divide `sec` nos arcos dados (µm). Geometria 3D partida EXATAMENTE (pontos interpolados nos cortes), peças
    encadeadas (peça j+1 no extremo 1 da peça j), filhos religados no MESMO arco. Retorna [(seção, a0, a1)]."""
    n3 = int(h.n3d(sec=sec))
    P = [(h.x3d(i, sec=sec), h.y3d(i, sec=sec), h.z3d(i, sec=sec), h.diam3d(i, sec=sec), h.arc3d(i, sec=sec)) for i in range(n3)]
    L = P[-1][4]; b = [0.0] + list(arcs) + [L]

    def interp(a):
        for i in range(n3 - 1):
            if P[i][4] <= a <= P[i + 1][4]:
                w = 0.0 if P[i + 1][4] == P[i][4] else (a - P[i][4]) / (P[i + 1][4] - P[i][4])
                return tuple(P[i][j] + w * (P[i + 1][j] - P[i][j]) for j in range(4))
        raise ValueError(a)
    kids = [(c, c.parentseg().x * L, h.section_orientation(sec=c)) for c in sec.children()]
    for c, _, _ in kids: h.disconnect(sec=c)
    ms = [m for m in list(mechs) + ['pas'] if h.ismembrane(m, sec=sec)]
    pieces = [sec] + [h.Section(name='%s_x%d' % (key, j)) for j in range(1, len(b) - 1)]
    for j, ps in enumerate(pieces):
        a0, a1 = b[j], b[j + 1]
        q3 = [interp(a0)] + [q[:4] for q in P if a0 < q[4] < a1] + [interp(a1)]
        h.pt3dclear(sec=ps)
        for q in q3: h.pt3dadd(*q, sec=ps)
        if j:
            ps.Ra = sec.Ra
            for m in ms: ps.insert(m)
            ps.connect(pieces[j - 1](1), 0)
    for c, ac, ori in kids:
        j = 0 if ac <= 0 else next(j for j in range(len(pieces)) if b[j] < ac <= b[j + 1] + 1e-9)
        c.connect(pieces[j]((ac - b[j]) / (b[j + 1] - b[j])), ori)
    return [(pieces[j], b[j], b[j + 1]) for j in range(len(pieces))]


# ------------------------------------------------------------------ pontos
def points_v2(cell):
    """Os pontos do D131/V2 (hay_native.points), por nome de seção e arco — independentes da discretização."""
    soma = cell.soma[0]; dist = lambda seg: h.distance(soma(0.5), seg)
    nk = lambda s: int(h.SectionRef(sec=s).nchild())
    pts = {}; paths = {}
    for lst, label in ((cell.basal, 'basal'), (cell.apical, 'apical')):
        tip = max([s for s in lst if nk(s) == 0], key=lambda s: dist(s(1))); dtip = dist(tip(1))
        path = []; s = tip
        while s is not None and s != soma:
            path.append(s); ps = s.parentseg(); s = ps.sec if ps is not None else None
        paths[label] = path
        pts[label + '_ponta'] = {'sec': tip.name(), 'arc': tip.L, 'dist': dtip}
        c = [(abs(dist(s(1)) - dtip / 2), s) for s in path[1:] if nk(s) >= 2]
        if c:
            b = min(c, key=lambda q: q[0])[1]; pts[label + '_ramif'] = {'sec': b.name(), 'arc': b.L, 'dist': dist(b(1))}
    for d in range(100, int(pts['apical_ponta']['dist']), 100):
        for s in paths['apical']:
            d0 = dist(s(0))
            if d0 <= d <= d0 + s.L:
                pts['apical_%d' % d] = {'sec': s.name(), 'arc': d - d0, 'dist': float(d)}; break
    for d in (620, 800):
        sl = cell.locateSites('apic', d); best = None
        for i in range(int(sl.count())):
            si, x = int(sl.o(i).x[0]), sl.o(i).x[1]; dd = cell.apic[si](x).diam
            if best is None or dd > best[0]: best = (dd, si, x)
        s = cell.apic[best[1]]; pts['hay_%d' % d] = {'sec': s.name(), 'arc': best[2] * s.L, 'dist': dist(s(best[2]))}
    return pts


def random_sites(cell, n=30, seed=131):
    """D131 7.4(a): n pontos sorteados UNIFORMEMENTE POR COMPRIMENTO nos dendritos (basal + apical), semente fixa."""
    secs = [s for s in list(cell.basal) + list(cell.apical)]
    Ls = np.array([s.L for s in secs]); cum = np.concatenate(([0.0], np.cumsum(Ls)))
    u = np.random.default_rng(seed).uniform(0.0, cum[-1], n); out = {}
    for i, x in enumerate(np.sort(u)):
        j = int(np.searchsorted(cum, x, side='right') - 1); s = secs[j]
        out['sorteio_%02d' % i] = {'sec': s.name(), 'arc': float(x - cum[j]), 'dist': h.distance(cell.soma[0](0.5), s((x - cum[j]) / s.L))}
    return out


def grid_points(cell, spacing=25.0):
    """Grade ancorada no soma: em cada seção dendrítica, os arcos cuja distância ao soma(0.5) é múltiplo de `spacing`."""
    soma = cell.soma[0]; out = {}
    for s in list(cell.basal) + list(cell.apical):
        d0 = h.distance(soma(0.5), s(0)); k = math.ceil(d0 / spacing - 1e-9)
        while k * spacing <= d0 + s.L + 1e-9:
            arc = k * spacing - d0
            if arc > 1e-9: out['g_%s_%d' % (s.name().split('.')[-1], k)] = {'sec': s.name(), 'arc': min(arc, s.L), 'dist': k * spacing}
            k += 1
    return out


# ------------------------------------------------------------------ o modelo
class RegionModel:
    """Hay nativo, N por ramo, nó em cada ponto de medida, densidades = FORMAS do Hay × θ (30 parâmetros por região).
    points_fn(cell) → {nome: {'sec','arc'}}: pontos que viram nós (definidos sobre a célula ANTES da divisão)."""

    def __init__(self, hay, N, points_fn, theta=None):
        load(hay); self.hay = hay; self.N = N
        cell = h.L5PCtemplate(os.path.join(hay, 'morphologies', 'cell1.asc')); self.cell = cell
        for s in cell.all: s.nseg = 1
        h.L5PCbiophys().biophys(cell)                         # insere os mecanismos por região; VALORES vêm de θ
        self.PTS = points_fn(cell)
        self.region = {}
        for lst, r in ((cell.somatic, 'soma'), (cell.axonal, 'axon'), (cell.basal, 'basal'), (cell.apical, 'apical')):
            for s in lst: self.region[s] = r
        BYS = {s.name().split('.')[-1]: s for s in cell.all}; self.BYS = BYS
        cuts = {}
        for p in self.PTS.values():
            key = p['sec'].split('.')[-1]
            if 1e-6 < p['arc'] < BYS[key].L - 1e-6: cuts.setdefault(key, set()).add(p['arc'])
        Lorig = {key: BYS[key].L for key in cuts}
        self.PIECES = {key: split_section(BYS[key], sorted(a), key) for key, a in cuts.items()}
        self.secs = list(cell.all)
        for key, pcs in self.PIECES.items():
            for sec_, a0, a1 in pcs[1:]: self.secs.append(sec_); self.region[sec_] = self.region[BYS[key]]
        for s in self.secs:
            key = s.name().split('.')[-1].split('_x')[0]
            s.nseg = 1 if self.region[s] == 'soma' else (N if key not in self.PIECES else max(1, int(round(N * s.L / Lorig[key]))))
        # distâncias das formas: origem apic[0](0) (convenção do código do Hay — ver cabeçalho)
        o = cell.apic[0](0)
        tips = [s for s in self.secs if self.region[s] == 'apical' and int(h.SectionRef(sec=s).nchild()) == 0]
        self.maxL = max(h.distance(o, s(1)) for s in tips)
        self.segd = {s: [h.distance(o, seg) for seg in s] for s in self.secs if self.region[s] == 'apical'}
        self.SOMA = cell.soma[0](0.5); self.nseg = sum(s.nseg for s in self.secs)
        self.set_theta(THETA_TRUE if theta is None else theta)

    def set_theta(self, th):
        self.theta = dict(th)
        for s in self.secs:
            r = self.region[s]; s.Ra = th['Ra']
            for k, seg in enumerate(s):
                seg.pas.e = th['e_pas']
                if r in ('soma', 'axon'): seg.cm = th['cm_somaaxon']
                else: seg.cm = th['cm_dend']
                seg.pas.g = th['g_pas_' + {'soma': 'soma', 'axon': 'axon', 'basal': 'basal', 'apical': 'apical'}[r]]
                if r == 'soma':
                    for m, q in (('NaTa_t', 'gNaTa_tbar_NaTa_t'), ('Nap_Et2', 'gNap_Et2bar_Nap_Et2'), ('K_Pst', 'gK_Pstbar_K_Pst'),
                                 ('K_Tst', 'gK_Tstbar_K_Tst'), ('SKv3_1', 'gSKv3_1bar_SKv3_1'), ('SK_E2', 'gSK_E2bar_SK_E2'),
                                 ('Ca_HVA', 'gCa_HVAbar_Ca_HVA'), ('Ca_LVAst', 'gCa_LVAstbar_Ca_LVAst'), ('Ih', 'gIhbar_Ih')):
                        setattr(seg, q, th['soma_' + m])
                    seg.gamma_CaDynamics_E2 = th['soma_gamma']; seg.decay_CaDynamics_E2 = th['soma_decay']
                    seg.ek = -85.0; seg.ena = 50.0
                elif r == 'apical':
                    d = self.segd[s][k]; dn = d / self.maxL
                    seg.gNaTa_tbar_NaTa_t = th['apic_NaTa_t']; seg.gSKv3_1bar_SKv3_1 = th['apic_SKv3_1']
                    seg.gSK_E2bar_SK_E2 = th['apic_SK_E2']; seg.gImbar_Im = th['apic_Im']
                    seg.gamma_CaDynamics_E2 = th['apic_gamma']; seg.decay_CaDynamics_E2 = th['apic_decay']
                    seg.gIhbar_Ih = th['apic_Ih_amp'] * (-0.8696 + 2.0870 * math.exp((3.6161 / th['apic_Ih_escala']) * (dn - 0.0)))
                    inz = 685.0 < d < 885.0
                    seg.gCa_LVAstbar_Ca_LVAst = th['apic_Ca_LVAst_zona'] * (1.0 if inz else 0.01)
                    seg.gCa_HVAbar_Ca_HVA = th['apic_Ca_HVA_zona'] * (1.0 if inz else 0.1)
                    seg.ek = -85.0; seg.ena = 50.0
                elif r == 'basal':
                    seg.gIhbar_Ih = th['basal_Ih']

    def at(self, pt):
        """Pesos de leitura/injeção do ponto (nó: peso 1 no extremo da peça)."""
        key = pt['sec'].split('.')[-1]; arc = pt['arc']; s = self.BYS[key]
        if key in self.PIECES:
            s, a0, a1 = next(q for q in self.PIECES[key] if q[1] < arc <= q[2] + 1e-9); arc = arc - a0
        arc = min(max(arc, 0.0), s.L)
        pos, xs = PL.node_positions(s)
        return [(s(xs[i]), w) for i, w in PL.bracket(pos, arc)]
