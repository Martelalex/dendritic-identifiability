# points_lib.py — PONTOS FÍSICOS FIXOS (D127), definidos na MORFOLOGIA antes de discretizar.
# CRITÉRIO ANATÔMICO (declarado antes de rodar): para cada TIPO de ramo dendrítico (basal 'dend', apical 'apic'),
# o CAMINHO MAIS LONGO do soma até uma ponta (a ponta de maior distância de caminho). Em cada caminho, dois pontos:
#   MEIO  = o ponto a 50% da distância de caminho da ponta;
#   PONTA = a ponta (a extremidade anatômica; no apical é o ponto do TUFO mais distante do soma).
# Um ponto é (nome da seção, posição de arco em µm), independente de nseg/N.
from neuron import h


def fixed_points():
    h.distance(0, 0.5, sec=h.soma[0])
    kids = {s.name(): 0 for s in h.allsec()}
    for s in h.allsec():
        p = s.parentseg()
        if p is not None: kids[p.sec.name()] += 1
    pts = {}
    for t, label in (('dend', 'basal'), ('apic', 'apical')):
        tips = [s for s in h.allsec() if s.name().startswith(t + '[') and kids[s.name()] == 0]
        if not tips: continue                        # ramo ausente (interneurônio sem apical)
        tip = max(tips, key=lambda s: h.distance(1, sec=s))
        dtip = h.distance(1, sec=tip)
        pts[label + '_ponta'] = {'sec': tip.name(), 'arc': tip.L, 'dist': dtip}
        dmid = 0.5 * dtip
        s = tip
        while h.distance(0, sec=s) > dmid:           # sobe pelo caminho até a seção que contém o meio
            s = s.parentseg().sec
        pts[label + '_meio'] = {'sec': s.name(), 'arc': dmid - h.distance(0, sec=s), 'dist': dmid}
    return pts


def node_positions(sec):
    """Nós do NEURON ao longo da seção: ponta 0, centros, ponta 1 — como posições de arco (µm) e x."""
    n = sec.nseg; L = sec.L
    xs = [0.0] + [(k + 0.5) / n for k in range(n)] + [1.0]
    return [x * L for x in xs], xs


def bracket(positions, arc):
    """Pesos lineares dos dois nós que envolvem 'arc' (interpolação linear ao longo da seção)."""
    for i in range(len(positions) - 1):
        a, b = positions[i], positions[i + 1]
        if a <= arc <= b:
            if b == a: return [(i, 1.0)]
            w = (arc - a) / (b - a)
            return [(i, 1.0 - w), (i + 1, w)]
    raise ValueError('posição fora da seção')


def fixed_points_nodes():
    """D127 adendo 3 (decisão pós-dados, justificada: pontos de medida ficam em NÓS): as PONTAS ficam; o MEIO de cada
    caminho é trocado pelo PONTO DE RAMIFICAÇÃO (ponta x=1 de uma seção do caminho com ≥2 filhos — bifurcação; soma e
    a própria ponta excluídos) MAIS PRÓXIMO do meio, no MESMO caminho. Sem bifurcação no caminho → sem ponto de meio."""
    base = fixed_points()
    h.distance(0, 0.5, sec=h.soma[0])
    kids = {s.name(): 0 for s in h.allsec()}
    for s in h.allsec():
        p = s.parentseg()
        if p is not None: kids[p.sec.name()] += 1
    out = {}; info = {}
    for label in ('basal', 'apical'):
        if label + '_ponta' not in base: continue
        tip = [s for s in h.allsec() if s.name() == base[label + '_ponta']['sec']][0]
        out[label + '_ponta'] = base[label + '_ponta']
        dmid = base[label + '_meio']['dist']
        cands = []; s = tip.parentseg().sec if tip.parentseg() is not None else None
        while s is not None and not s.name().startswith('soma'):
            if kids[s.name()] >= 2: cands.append((abs(h.distance(1, sec=s) - dmid), s))
            s = s.parentseg().sec if s.parentseg() is not None else None
        info[label] = [(c[1].name(), round(h.distance(1, sec=c[1]), 1), kids[c[1].name()]) for c in cands]
        if cands:
            _, b = min(cands, key=lambda c: c[0])
            out[label + '_ramif'] = {'sec': b.name(), 'arc': b.L, 'dist': h.distance(1, sec=b), 'meio_original': dmid}
    return out, info
