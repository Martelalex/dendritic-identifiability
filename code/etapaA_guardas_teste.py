# etapaA_guardas_teste.py — D132 item 157: TESTES COM RESPOSTA CONHECIDA dos dois GUARDAS do CommonSim.run, ANTES de ativar (compartimento passivo real):
#   G1 fuga provocada para CIMA (+100 nA no soma): aborta NO ATO (t do aborto < 0.1 ms depois do início do estímulo), GUARDA FÍSICO, SimulacaoAbortada;
#   G2 fuga para BAIXO (−100 nA): idem;
#   G3 PÓS-CHECAGEM: com o guarda de passo desligado, a fuga é pega nas gravações;
#   G4 simulação ARTIFICIALMENTE LENTA (um evento a cada 1 ms queima ~20 ms de CPU) contra um limite de teste (mediana semeada 0.01 s, piso 0.2 s):
#      GUARDA DE TEMPO, abortada perto do limite (não no fim);
#   G5 BIT A BIT: a mesma rodada normal com advance() = fadvance() + guarda (sem disparo) × advance() ORIGINAL (só fadvance) → traços IDÊNTICOS;
#   G6 rodada normal: não dispara; o tempo de CPU é registrado na chave do tipo (arquivo de teste, não o real).
#   G7 (item 159) autoteste do CommonSim (início tardio) NÃO aborta com um limite de tempo minúsculo; uma rodada de protocolo do mesmo tipo aborta.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_guardas_teste.py
import sys, os, time, tempfile, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stim_common as SC
from neuron import h

F = []
def confere(n, ok, msg=''):
    print('%-78s %s %s' % (n, 'OK' if ok else 'FALHOU', msg), flush=True)
    if not ok: F.append(n)


tmp = tempfile.mkdtemp(prefix='guardas_'); SC.TEMPOS = os.path.join(tmp, 'tempos.log'); SC._MEDIDAS = None
soma = h.Section(name='soma'); soma.L = soma.diam = 20.0; soma.insert('pas'); soma.g_pas = 1e-4; soma.e_pas = -70.0
h.load_file("stdrun.hoc"); h.v_init = -70.0
QUEIMA = [False]                                                     # G4: o gerador de eventos existe ANTES do repouso salvo (estrutura fixa), desligado
def queima():
    if not QUEIMA[0]: return
    t0 = time.process_time()
    while time.process_time() - t0 < 0.02: pass
ns = h.NetStim(); ns.start = 1e9; ns.interval = 1.0; ns.number = 1e9; ns.noise = 0; nc = h.NetCon(ns, None); nc.record(queima)
C = SC.CommonSim(soma(0.5), atol=1e-8, verbose=False, test_amp=0.05)   # pulso de autoteste do próprio CommonSim (≤ 15 mV neste soma pequeno)
rec = {'v': [(soma(0.5), 1.0)]}


def aborta(stims, tstop):
    try: C.run(stims, tstop, rec, rec_grid=0.1); return None
    except SC.SimulacaoAbortada as e: return str(e)


m = aborta([('s', 10.0, 100.0, 50.0)], 100.0); t = float(re.search(r't = ([\d.]+) ms', m).group(1)) if m else None
confere('G1 fuga +100 nA → GUARDA FÍSICO no ato', m is not None and m.startswith('GUARDA FÍSICO:') and t is not None and t < 10.1, '(%s)' % m)
m = aborta([('s', 10.0, -100.0, 50.0)], 100.0)
confere('G2 fuga −100 nA → GUARDA FÍSICO no ato', m is not None and m.startswith('GUARDA FÍSICO:') and 'V = -' in m, '(%s)' % m)
orig = SC.GUARDA.tick; SC.GUARDA.tick = lambda: 0
m = aborta([('s', 10.0, 100.0, 50.0)], 100.0); SC.GUARDA.tick = orig
confere('G3 sem o guarda de passo → a PÓS-CHECAGEM pega a fuga', m is not None and 'pós-checagem' in m, '(%s)' % m)

# G4: simulação artificialmente lenta
st = [('s', 10.0, 0.01, 50.0)]; chave = '%s|%g|%d|%d|%g' % ('s', 100.0, 1, C._nseg, 1e-8)
SC._MEDIDAS = {chave: [0.01] * 5}; SC.PISO_S, piso0 = 0.2, SC.PISO_S
QUEIMA[0] = True; ns.start = C.inj.TS + 1.0                          # eventos só DEPOIS do instante de partida da rodada
t0 = time.process_time(); m = aborta(st, 100.0); dt = time.process_time() - t0
QUEIMA[0] = False; ns.start = 1e9; SC.PISO_S = piso0; SC._MEDIDAS = None
confere('G4 simulação lenta → GUARDA DE TEMPO perto do limite (0.2 s), não no fim (~2 s)', m is not None and m.startswith('GUARDA DE TEMPO') and dt < 1.0, '(%.2f s de CPU; %s)' % (dt, m))

# G5: bit a bit — guarda ligado (sem disparo) × advance() original
st = [('s', 10.0, 0.05, 50.0), ('a', 70.0, 0.1, 5.0)]
t1, o1 = C.run(st, 120.0, rec, rec_grid=0.1)
h('proc advance() { fadvance() }'); t2, o2 = C.run(st, 120.0, rec, rec_grid=0.1); h('proc advance() { fadvance()  _hanu_guarda.tick() }')
confere('G5 guarda ligado sem disparo × advance() original → traços IDÊNTICOS bit a bit', o1['v'].tobytes() == o2['v'].tobytes() and t1.tobytes() == t2.tobytes(),
        '(máx |Δ| = %.1e mV)' % float(np.abs(o1['v'] - o2['v']).max()))
# G6: rodada normal registra o tempo e não dispara
SC._MEDIDAS = None; n0 = len(open(SC.TEMPOS).read().splitlines()) if os.path.exists(SC.TEMPOS) else 0
C.run(st, 120.0, rec, rec_grid=0.1); n1 = len(open(SC.TEMPOS).read().splitlines())
confere('G6 rodada normal: não dispara; tempo de CPU registrado no tipo', n1 == n0 + 1 and SC.GUARDA.motivo is None, '(%d → %d linhas)' % (n0, n1))
# G7 (item 159): os AUTOTESTES do CommonSim (aqui: início tardio) não têm guarda de TEMPO; uma rodada de protocolo do MESMO tipo tem
ch = '%s|%g|%d|%d|%g' % ('s', 70.0, 1, C._nseg, 1e-8); SC._MEDIDAS = {ch: [1e-6] * 5}; SC.PISO_S, piso0 = 1e-4, SC.PISO_S
try: C.late_onset_check(); m1 = None
except SC.SimulacaoAbortada as e: m1 = str(e)
QUEIMA[0] = True; ns.start = C.inj.TS + 1.0; m2 = aborta([('s', 10.0, 0.05, 5.0)], 70.0); QUEIMA[0] = False; ns.start = 1e9; SC.PISO_S = piso0; SC._MEDIDAS = None
confere('G7 autoteste do CommonSim SEM guarda de tempo; protocolo do mesmo tipo COM', m1 is None and m2 is not None and m2.startswith('GUARDA DE TEMPO'), '(autoteste: %s; protocolo: %s)' % (m1, m2))
print('TESTES: %d falha(s) %s' % (len(F), F)); sys.exit(1 if F else 0)
