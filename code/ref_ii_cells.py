# ref_ii_cells.py — D132 item 83 (1): construção das células de referência do ref_ii (Allen PV/piramidal L0 Δ 2 µm; Hay
# biophys3/biophys4 L0 Δ 1 µm), UM caminho só — usado por ref_ii_axon.py (tarefas A/B/T/R) e por ref_ii_C.py (tarefa C
# pelo runner da Etapa A). 'toyC' = célula pequena com HH (soma + 2 axônios) só para o TESTE DE RETOMADA do runner.
import os, math
from neuron import h

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLEN = {'pv': ('.cache/swc_471077857.swc', 'allen_models/genomes/pv_471077857_all_active_497233075.json'),
         'pyr': ('.cache/swc_471129934.swc', 'allen_models/genomes/pyr_471129934_all_active_497233049.json')}
RHEO = {'pv': 0.38, 'pyr': 0.34, 'hay3': 0.4, 'hay4': 0.4, 'toyC': 0.02}   # nA — degraus de 1 s (D129 / P6 do V2); toyC: teste
HAY_ACTIVE = ['Ca_LVAst', 'Ca_HVA', 'SKv3_1', 'SK_E2', 'K_Tst', 'K_Pst', 'Nap_Et2', 'NaTa_t', 'CaDynamics_E2', 'Ih', 'Im']


def build(model, passive=False):
    """Devolve dict(soma, ais, dist, keep) — keep segura as referências Python da célula."""
    if model == 'toyC':
        h.load_file('stdrun.hoc')
        soma = h.Section(name='soma'); soma.L = soma.diam = 20.0
        a0 = h.Section(name='axon0'); a0.L = 30.0; a0.diam = 1.0; a0.nseg = 7; a0.connect(soma(0))
        a1 = h.Section(name='axon1'); a1.L = 300.0; a1.diam = 1.0; a1.nseg = 31; a1.connect(a0(1))
        for s in (soma, a0, a1):
            s.insert('hh') if not passive else s.insert('pas')
            s.Ra = 100.0
        h.v_init = -65.0
        return dict(soma=soma(0.5), ais=a0(0.5), dist=a1(1.0), keep=[soma, a0, a1])
    if model in ALLEN:
        import l1_lib as L
        L.load_mechs(os.path.join(HERE, 'allen_models', 'mod'))
        swc, fit = ALLEN[model]; L.build_L0(os.path.join(HERE, swc), os.path.join(HERE, fit), passive_only=passive)
        for s in h.allsec():
            if not s.name().startswith('soma'): s.nseg = max(s.nseg, int(math.ceil(s.L / 2.0)))
        return dict(soma=h.soma[0](0.5), ais=h.axon[0](0.5), dist=h.axon[1](1.0), keep=[])
    import hay_common as HC
    hay = os.path.join(HERE, '.cache', 'hay', '139653-master')
    if model == 'hay4':                                  # template não se redefine: carrega o biophys4 NO LUGAR do 3
        h.nrn_load_dll(os.path.join(hay, 'mod', 'x86_64', 'libnrnmech.so')); h.load_file('stdrun.hoc'); h.load_file('import3d.hoc')
        h.load_file(os.path.join(hay, 'models', 'L5PCbiophys4.hoc')); h.load_file(os.path.join(hay, 'models', 'L5PCtemplate.hoc'))
        HC._loaded.add(hay)
    else:
        HC.load(hay)
    cell = HC.build(hay, 1.0)
    if passive:
        for s in cell.all:
            for m in HAY_ACTIVE:
                if h.ismembrane(m, sec=s): s.uninsert(m)
    return dict(soma=cell.soma[0](0.5), ais=cell.axon[0](0.5), dist=cell.axon[1](1.0), keep=[cell])


def passivate():
    """Controle negativo (D132 itens 40c/52): remove todos os mecanismos de membrana exceto pas (e íons)."""
    mt = h.MechanismType(0); names = []
    for i in range(int(mt.count())):
        mt.select(i); nm = h.ref(''); mt.selected(nm); names.append(nm[0])
    for sec in h.allsec():
        for nm in names:
            if nm not in ('pas', 'capacitance', 'morphology') and not nm.endswith('_ion') and h.ismembrane(nm, sec=sec): sec.uninsert(nm)
