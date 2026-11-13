# l1_lib.py — degraus L0 e L1 da escada de atribuição de falhas (D123/D124), em NEURON.
#   L0 = modelo "all active" do Allen na morfologia completa, montado como o AllenSDK monta
#        (AllActiveUtils, axon_type='truncated' = default do runner.load_description).
#   L1 = MESMA biblioteca (.mod) e MESMAS densidades, reduzidas a 4 compartimentos (AIS, soma,
#        dendrito proximal, dendrito distal) — a geometria do HANU, em NEURON.
# Mapeamento (declarado ANTES de rodar):
#   regiões: AIS ← axon; soma ← soma; prox ← dend/apic a distância de CAMINHO < CUT_UM do soma;
#            distal ← dend/apic a ≥ CUT_UM (150 µm = definição de CompartmentType do HANU).
#   densidades gbar, cm, g_pas, gamma/decay do Ca: média ponderada pela ÁREA (preserva o total);
#   e_pas: média ponderada pela CONDUTÂNCIA g_pas·área (preserva a corrente de repouso).
#   acoplamento: da IMPEDÂNCIA PASSIVA DC da morfologia completa (determinístico): Z_ij = V̄_i/I_j
#   com corrente injetada UNIFORME (∝ área) na região j e V̄_i a média ponderada por área da
#   região i; G = Z⁻¹; cadeia AIS–soma–prox–distal com G_c = −G_ij. Membrana de cada nó = a das
#   densidades mapeadas (NÃO as somas de linha de G) → o portão passivo não é tautológico.
#   Cruzamento: acoplamento de Rall (cilindros equivalentes).
import json, math
import numpy as np
from neuron import h

h.load_file('stdrun.hoc'); h.load_file('import3d.hoc')
import os
CUT_UM = 150.0
# REGION_MODE: 'distance' = mapeamento DECLARADO (prox/distal pelo corte de 150 µm);
#              'type'     = DIAGNÓSTICO L0.x (prox = basal 'dend', distal = apical 'apic') — só para
#                           localizar perda; NÃO é o mapeamento adotado.
REGION_MODE = os.environ.get('REGION_MODE', 'distance')
REG = ['AIS', 'soma', 'prox', 'distal']


def load_mechs(moddir):
    h.nrn_load_dll(moddir + '/x86_64/libnrnmech.so')


def clear():
    for s in list(h.allsec()):
        h.delete_section(sec=s)


def build_L0(swc, fit, passive_only=False):
    """AllActiveUtils.generate_morphology (legacy 'truncated') + load_cell_parameters."""
    clear()
    D = json.load(open(fit))
    r = h.Import3d_SWC_read(); r.input(swc); imp = h.Import3d_GUI(r, 0)
    h('objref this'); imp.instantiate(h.this)
    for s in h.allsec():
        s.nseg = 1 + 2 * int(s.L / 40.0)
    h('soma[0] area(0.5)')
    d = [h.axon[0].diam, h.axon[0].diam]
    h.distance(sec=h.soma[0])
    for s in h.allsec():
        if s.name()[:4] == 'axon' and h.distance(0.5, sec=s) > 60:
            d[1] = s.diam; break
    for s in list(h.allsec()):
        if s.name()[:4] == 'axon':
            h.delete_section(sec=s)
    h('create axon[2]')
    for i, s in enumerate(h.axon):
        s.L = 30; s.diam = d[i]
    for s in h.allsec():
        s.nseg = 1 + 2 * int(s.L / 40.0)
    h.axon[0].connect(h.soma[0], 1.0, 0.0); h.axon[1].connect(h.axon[0], 1.0, 0.0)
    h.area(0.5, sec=h.soma[0])
    P = D['passive'][0]; C = D['conditions'][0]
    for s in h.allsec():
        s.Ra = P['ra']; s.insert('pas')
    for p in D['genome']:
        if not hasattr(h, p['section']):
            continue
        if passive_only and p['mechanism']:
            continue
        for s in getattr(h, p['section']):
            if p['mechanism'] and h.ismembrane(p['mechanism'], sec=s) != 1:
                s.insert(p['mechanism'])
            setattr(s, p['name'], float(p['value']))
    for e in C['erev']:
        if hasattr(h, e['section']):
            for s in getattr(h, e['section']):
                if h.ismembrane('k_ion', sec=s) == 1: s.ek = float(e['ek'])
                if h.ismembrane('na_ion', sec=s) == 1: s.ena = float(e['ena'])
    h.v_init = C['v_init']; h.celsius = C['celsius']
    return D


def region_of(sec, seg):
    t = sec.name().split('[')[0]
    if t == 'axon': return 0
    if t == 'soma': return 1
    if REGION_MODE == 'type':
        return 2 if t == 'dend' else 3
    return 2 if h.distance(seg.x, sec=sec) < CUT_UM else 3


def segments():
    h.distance(0, 0.5, sec=h.soma[0])
    out = []
    for s in h.allsec():
        for seg in s:
            out.append((s, seg, region_of(s, seg), seg.area()))
    return out


def region_params(D):
    """Parâmetros mapeados por região a partir do L0 ATIVO já montado."""
    segs = segments()
    mechs = sorted({p['mechanism'] for p in D['genome'] if p['mechanism']})
    A = np.zeros(4); cm = np.zeros(4); gp = np.zeros(4); gpe = np.zeros(4)
    dens = {}          # (mech, param) -> [4] (Σ valor·área)
    for s, seg, r, a in segs:
        A[r] += a; cm[r] += seg.cm * a; gp[r] += seg.pas.g * a; gpe[r] += seg.pas.g * seg.pas.e * a
        for m in mechs:
            if h.ismembrane(m, sec=s):
                for p in D['genome']:
                    if p['mechanism'] == m:
                        key = (m, p['name'])
                        dens.setdefault(key, np.zeros(4))[r] += getattr(seg, p['name']) * a
    out = {'area_um2': A, 'cm': cm / A, 'g_pas': gp / A, 'e_pas': gpe / gp,
           'dens': {k: v / A for k, v in dens.items()}}
    return out


def mean_v(segs):
    V = np.zeros(4); A = np.zeros(4)
    for s, seg, r, a in segs:
        V[r] += seg.v * a; A[r] += a
    return V / A


def dc_Z(I_nA=0.05, tstop=1500.0):
    """Z (MΩ) entre regiões: injeção uniforme (∝ área) na região j, média ponderada na região i.
    Chamar com o L0 PASSIVO montado. Linear ⇒ Z independe de I."""
    segs = segments()
    Areg = np.zeros(4)
    for _, _, r, a in segs: Areg[r] += a
    h.dt = 0.1
    h.finitialize(h.v_init); h.continuerun(tstop); V0 = mean_v(segs)
    Z = np.zeros((4, 4))
    for j in range(4):
        cl = []
        for s, seg, r, a in segs:
            if r == j:
                c = h.IClamp(seg); c.delay = 0; c.dur = 1e9; c.amp = I_nA * a / Areg[j]; cl.append(c)
        h.finitialize(h.v_init); h.continuerun(tstop)
        Z[:, j] = (mean_v(segs) - V0) / I_nA
        del cl
    return Z


def rall_couplings(D):
    """Cruzamento: acoplamento de cilindros equivalentes (Rall). d_eq = (Σ d_raiz^1.5)^(2/3) sobre os
    ramos que ENTRAM na região; L = A/(π d_eq); meia-resistência r = Ra·(L/2)/(π d²/4)."""
    segs = segments()
    A = np.zeros(4); RaA = np.zeros(4)
    for s, seg, r, a in segs: A[r] += a; RaA[r] += s.Ra * a
    Ra = RaA / A
    roots = {0: [], 2: [], 3: []}
    # fronteiras de região podem cair NO MEIO de uma seção (corte por distância) — percorre
    # segmento a segmento: pai de um segmento = segmento anterior da mesma seção, ou parentseg.
    for s in h.allsec():
        prev = s.parentseg()
        prev_r = None
        if prev is not None:
            pt = prev.sec.name().split('[')[0]
            prev_r = 1 if pt == 'soma' else (0 if pt == 'axon' else region_of(prev.sec, prev))
        for seg in s:
            r_seg = region_of(s, seg)
            if prev_r is not None and r_seg != prev_r and r_seg in roots:
                roots[r_seg].append(seg.diam)
            prev_r = r_seg
    # soma: cilindro próprio; AIS/prox/distal: equivalentes
    d = np.zeros(4); L = np.zeros(4)
    d[1] = h.soma[0].diam; L[1] = h.soma[0].L
    for r in (0, 2, 3):
        d[r] = sum(x ** 1.5 for x in roots[r]) ** (2 / 3); L[r] = A[r] / (math.pi * d[r])
    half = Ra * 1e-4 * (L / 2) / (math.pi * (d * 1e-4) ** 2 / 4) / 1e6   # MΩ
    G = [1.0 / (half[0] + half[1]), 1.0 / (half[1] + half[2]), 1.0 / (half[2] + half[3])]   # µS
    return np.array(G), d, L, roots


class L1:
    """4 nós nseg=1 (L = diam = √(A/π) ⇒ área exata), acoplados por LinearMechanism com
    condutância absoluta G_c (µS) por aresta da cadeia (linha i escalada por 1/A_i — validado)."""

    def __init__(self, P, Gc, D=None, active=False):
        clear()
        self.secs = []
        for i in range(4):
            s = h.Section(name='L1_' + REG[i]); dd = math.sqrt(P['area_um2'][i] / math.pi)
            s.L = dd; s.diam = dd; s.nseg = 1; s.Ra = 100
            s.insert('pas'); s.cm = P['cm'][i]; s.g_pas = P['g_pas'][i]; s.e_pas = P['e_pas'][i]
            self.secs.append(s)
        if active:
            for (m, pname), v in P['dens'].items():
                for i in range(4):
                    if v[i] != 0.0:
                        if h.ismembrane(m, sec=self.secs[i]) != 1: self.secs[i].insert(m)
                        setattr(self.secs[i], pname, float(v[i]))
            C = D['conditions'][0]; e = C['erev'][0]
            for s in self.secs:
                if h.ismembrane('k_ion', sec=s) == 1: s.ek = float(e['ek'])
                if h.ismembrane('na_ion', sec=s) == 1: s.ena = float(e['ena'])
            h.v_init = C['v_init']; h.celsius = C['celsius']
        Acm = [self.secs[i](0.5).area() * 1e-8 for i in range(4)]
        n = 4
        self.c = h.Matrix(n, n, 2); self.g = h.Matrix(n, n, 2)
        for (i, j), G in zip(((0, 1), (1, 2), (2, 3)), Gc):
            for a, b in ((i, j), (j, i)):
                self.g.setval(a, a, self.g.getval(a, a) + G * 1e-6 / Acm[a])
                self.g.setval(a, b, self.g.getval(a, b) - G * 1e-6 / Acm[a])
        self.y = h.Vector(n); self.b = h.Vector(n); self.sl = h.SectionList()
        for s in self.secs: self.sl.append(sec=s)
        self.lm = h.LinearMechanism(self.c, self.g, self.y, self.b, self.sl, h.Vector([0.5] * n))

    def seg(self, i):
        return self.secs[i](0.5)


def metrics(soma_seg, reg_segs, I=-0.05, t0=500.0, tstop=2000.0):
    """reg_segs: lista (seg, região, área). Retorna Rin (MΩ), τ63 (ms), atenuações DC."""
    def run(inj):
        cl = []
        for seg, amp in inj:
            c = h.IClamp(seg); c.delay = t0; c.dur = 1e9; c.amp = amp; cl.append(c)
        vs = h.Vector().record(soma_seg._ref_v); tv = h.Vector().record(h._ref_t)
        h.dt = 0.025; h.finitialize(h.v_init); h.continuerun(tstop)
        V = np.zeros(4); A = np.zeros(4); V0 = None
        for seg, r, a in reg_segs: V[r] += seg.v * a; A[r] += a
        return np.array(vs), np.array(tv), V / A
    vb, tb, Vb = run([])
    vs, tv, Vs = run([(soma_seg, I)])
    dv = vs - vb; ss = dv[-1]
    k = np.flatnonzero((tv >= t0) & (np.abs(dv) >= 0.632 * abs(ss)))
    tau = tv[k[0]] - t0 if len(k) else float('nan')
    dVs = Vs - Vb
    Ad = sum(a for _, r, a in reg_segs if r == 3)
    _, _, Vd = run([(seg, I * a / Ad) for seg, r, a in reg_segs if r == 3])
    dVd = Vd - Vb
    return {'Rin': ss / I, 'tau': tau, 'att_s2p': dVs[2] / dVs[1], 'att_s2d': dVs[3] / dVs[1],
            'att_d2s': dVd[1] / dVd[3], 'Vrest_soma': vb[int(t0 / 0.025) - 1]}
