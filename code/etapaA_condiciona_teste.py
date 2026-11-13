# etapaA_condiciona_teste.py — D132 item 146: TESTES COM RESPOSTA CONHECIDA dos critérios novos do condicionamento (etapaA_condiciona), ANTES do uso.
#   T1 R_in e ρ_I num compartimento PASSIVO real (NEURON): R_in = 1/(g_pas·área); ρ_I ≈ 0.
#   T2 ρ_I com termo quadrático conhecido: y± = ±a·s + b·s² → ρ_I = (b/a)·máx s.
#   T3 regra da METADE do alvo (simulador modelo com ρ_I = c·ΔV): c = 0.03/mV → 5 ✘, 2.5 ✔; c = 0.1/mV → nenhum passa.
#   T4 limiar local por bisseção: degrau de ganho em 0.7 nA; supralinear suave A·(1 + (A/0.4)⁴) (limiar analítico); sublinear → nenhum.
#   T5 teto por bisseção: V máx = −70 + 100·A → 1.3 nA.
#   T6 latência/identidade com disparos SINTÉTICOS em t(A) = 20 + 2/(A − 0.5) ms: A = 1.0 passa (−0.080 ms por 1%); 0.55 falha pela latência
#      (−4.45 ms por 1%); 0.505 falha pela identidade (o disparo aparece dentro de ±2%).
#   T7 escolha/passo/omissão com mocks: [0.5, 0.7] (0.9 → 0.8 → 0.7; 1.2 omitida no teto); teto abaixo de 1.2× → amplitude no teto; teto abaixo
#      do limiar → omitida; sem limiar → as antigas.
#   T8 bordas: salto rápido de 25 mV no degrau → detectado (M1p no liga; M1m no desliga); de 5 mV → nada.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_condiciona_teste.py
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_condiciona as C
import etapaA_unit as EU
from neuron import h

FALHAS = []


def confere(nome, cond, msg=''):
    print('%-62s %s %s' % (nome, 'OK' if cond else 'FALHOU', msg), flush=True)
    if not cond: FALHAS.append(nome)


T1150 = np.arange(0.0, EU.M1['tstop'] + 1e-9, EU.DT); T300 = np.arange(0.0, EU.M4['tstop'] + 1e-9, EU.DT)


def s_degrau(t, tau=20.0):
    on, off = EU.M1['delay'], EU.M1['delay'] + EU.M1['dur']
    s = np.where(t >= on, 1 - np.exp(-np.clip(t - on, 0, None) / tau), 0.0)
    return np.where(t >= off, s * np.exp(-np.clip(t - off, 0, None) / tau), s)


# T1 ---------------------------------------------------------------------------------------------------------------
h.load_file('stdrun.hoc')
cmp_ = h.Section(name='c'); cmp_.L = cmp_.diam = 20.0; cmp_.nseg = 1; cmp_.insert('pas'); cmp_.g_pas = 1e-4; cmp_.e_pas = -70.0; cmp_.cm = 1.0


def sim_passivo(kind, amp, reads):
    c = h.IClamp(cmp_(0.5)); c.delay = EU.M1['delay']; c.dur = EU.M1['dur']; c.amp = amp
    tv = h.Vector(T1150); v = h.Vector().record(cmp_(0.5)._ref_v, tv)
    h.cvode_active(1); h.cvode.atol(1e-10); h.finitialize(-70.0); h.continuerun(EU.M1['tstop'])
    return np.array(tv), np.array(v)[None]


R_esp = 1.0 / (cmp_.g_pas * h.area(0.5, sec=cmp_) * 1e-8) / 1e6
R, _ = C.rin(sim_passivo, 'c')
confere('T1 R_in passivo = 1/(g·área)', abs(R / R_esp - 1) < 1e-6, '(%.6f × %.6f MΩ)' % (R, R_esp))
m = C.m1_condiciona(sim_passivo, 'c')
confere('T1 ρ_I passivo ≈ 0 e passa a 5 mV', m['passa'] and m['alvo_mV'] == 5.0 and m['historico'][0]['rho_I'] < 1e-6,
        '(ρ_I %.2e; deflexão %.4f mV)' % (m['historico'][0]['rho_I'], m['historico'][0]['deflexao_estacionaria_mV']))

# T2 ---------------------------------------------------------------------------------------------------------------
s = s_degrau(T1150); a, b = 2.0, 0.3
r = C.rho_I(a * s + b * s * s, -a * s + b * s * s)[0]
confere('T2 ρ_I com termo quadrático = (b/a)·máx s', abs(r - (b / a) * s.max()) < 1e-12, '(%.6f × %.6f)' % (r, (b / a) * s.max()))


# T3 ---------------------------------------------------------------------------------------------------------------
def sim_quad(c, Rm=100.0):
    def f(kind, amp, reads):
        dv = Rm * amp; sd = s_degrau(T1150)
        return T1150, (-70.0 + dv * sd + c * dv * dv * sd * sd)[None]
    return f


m = C.m1_condiciona(sim_quad(0.03), 'x')
confere('T3 metade: c = 0.03/mV → 5 ✘, 2.5 ✔ (R_in exata)', m['passa'] and m['alvo_mV'] == 2.5 and abs(m['R_in_MOhm'] - 100.0) < 1e-9
        and [x['passa'] for x in m['historico']] == [False, True], '(ρ_I %s)' % ['%.4f' % x['rho_I'] for x in m['historico']])
m = C.m1_condiciona(sim_quad(0.1), 'x')
confere('T3 metade: c = 0.1/mV → nenhum alvo passa', (not m['passa']) and len(m['historico']) == 3, '(ρ_I %s)' % ['%.4f' % x['rho_I'] for x in m['historico']])

# T4 ---------------------------------------------------------------------------------------------------------------
lim, _ = C.limiar_local(lambda A: A if A < 0.7 else 3.0 * A)
confere('T4 limiar: degrau de ganho em 0.7 nA', lim is not None and 0.7 <= lim <= 0.7 * (1 + C.REL), '(%s)' % lim)
A1 = 0.4; eps = (C.A_LIN / A1) ** 4; Aesp = A1 * (C.SUPRA * (1 + eps) - 1) ** 0.25
lim, _ = C.limiar_local(lambda A: A * (1 + (A / A1) ** 4))
confere('T4 limiar: supralinear suave (analítico)', lim is not None and Aesp <= lim <= Aesp * (1 + C.REL), '(%.6f × %.6f)' % (lim, Aesp))
lim, _ = C.limiar_local(lambda A: A / (1 + A))
confere('T4 limiar: sublinear → nenhum', lim is None)

# T5 ---------------------------------------------------------------------------------------------------------------
A = C.teto(lambda A: -70.0 + 100.0 * A, 1.0, 1.5)
confere('T5 teto: V máx = −70 + 100·A → 1.3 nA', 1.3 * (1 - C.REL) <= A <= 1.3, '(%.6f)' % A)


# T6 ---------------------------------------------------------------------------------------------------------------
def tracos_sint(A):
    y = np.full((2, len(T300)), -70.0); y[1] = -75.0
    if A > 0.5:
        ts = 20.0 + 2.0 / (A - 0.5)
        if ts < 290.0: y[0] += 80.0 * np.exp(-0.5 * ((T300 - ts) / 0.5) ** 2)
    return y


ok, det = C.testa_amp(tracos_sint, 1.0); esp = ((20 + 2 / 0.51) - (20 + 2 / 0.49)) / 2
confere('T6 A = 1.0 passa; dlat = −0.080 ms por 1%', ok and det[0]['K'] == 1 and abs(det[0]['dlat_ms_por_1pct'][0] - esp) < 0.005,
        '(%.4f × %.4f)' % (det[0]['dlat_ms_por_1pct'][0], esp))
ok, det = C.testa_amp(tracos_sint, 0.55)
confere('T6 A = 0.55 falha pela LATÊNCIA (identidade ok)', (not ok) and det[0]['identidade'] and not det[0]['latencia_ok'],
        '(%s ms por 1%%)' % ['%.3f' % x for x in det[0]['dlat_ms_por_1pct']])
ok, det = C.testa_amp(tracos_sint, 0.505)
confere('T6 A = 0.505 falha pela IDENTIDADE (contagem muda em ±2%)', (not ok) and not det[0]['identidade'], '(%s)' % det[0]['contagens'])

# T7 ---------------------------------------------------------------------------------------------------------------
acc, reg = C.escolhe_m4(1.0, lambda A: -65.0 + 100.0 * A, lambda A: (abs(A - 1.0) >= 0.26, 'mock'))
confere('T7 passo e omissão: [0.5, 0.7]; 1.2 omitida no teto', np.allclose(acc, [0.5, 0.7]) and reg[2]['final'] is None
        and reg[1]['tentativas'][-1]['fator'] == 0.7, '(%s)' % acc)
acc, _ = C.escolhe_m4(1.0, lambda A: -70.0 + 120.0 * A, lambda A: (True, 'mock'))
confere('T7 teto abaixo de 1.2× → amplitude no teto (1.0833)', len(acc) == 3 and np.allclose(acc[:2], [0.5, 0.9]) and 1.0833 * (1 - C.REL) <= acc[2] <= 130 / 120,
        '(%s)' % acc)
acc, reg = C.escolhe_m4(1.0, lambda A: -70.0 + 140.0 * A, lambda A: (True, 'mock'))
confere('T7 teto abaixo do limiar → 1.2× omitida', np.allclose(acc, [0.5, 0.9]) and reg[2]['final'] is None, '(%s)' % acc)
acc, _ = C.escolhe_m4(None, lambda A: -70.0 + 10.0 * A, lambda A: (True, 'mock'))
confere('T7 sem limiar → as antigas', np.allclose(acc, C.ANTIGAS), '(%s)' % acc)


# T8 ---------------------------------------------------------------------------------------------------------------
def degrau_rapido(dv):
    return (-70.0 + dv * s_degrau(T1150, tau=0.5))[None]


d25p = C.detecta(EU.cadeia(degrau_rapido(25.0), 'M1p'), ['p']); d25m = C.detecta(EU.cadeia(degrau_rapido(-25.0), 'M1m'), ['p'])
d5p = C.detecta(EU.cadeia(degrau_rapido(5.0), 'M1p'), ['p']); d5m = C.detecta(EU.cadeia(degrau_rapido(-5.0), 'M1m'), ['p'])
confere('T8 salto de 25 mV detectado (M1p no liga, M1m no desliga)', bool(d25p) and bool(d25m) and abs(d25p[0][1][0][0] - 100.0) < 0.5
        and abs(d25m[0][1][0][0] - 1100.0) < 0.5, '(%s | %s)' % (d25p, d25m))
confere('T8 salto de 5 mV: nada detectado', not d5p and not d5m)

# T9 (item 156, opção A) ------------------------------------------------------------------------------------------
r = C.limiar_local(lambda A: A, lambda A: -70.0 + 900.0 * A)                  # sem supralinearidade; teto em 130/900 nA
esp = 130.0 / 900.0; at = C.teto(lambda A: -70.0 + 900.0 * A, *r[2]) if len(r) > 2 else None
confere('T9 sem evento na faixa → None + par do teto; A_teto por bisseção', r[0] is None and len(r) == 3 and r[2][0] <= esp < r[2][1] and esp * (1 - C.REL) <= at <= esp,
        '(%s; A_teto %.5f × %.5f)' % (r[2], at, esp))
r = C.limiar_local(lambda A: A if A < 0.2 else 3.0 * A, lambda A: -70.0 + 900.0 * A)
confere('T9 evento SÓ acima do teto (0.2 nA; teto 0.144) → sem evento na faixa', r[0] is None)
l0, _ = C.limiar_local(lambda A: A * (1 + (A / A1) ** 4)); l1 = C.limiar_local(lambda A: A * (1 + (A / A1) ** 4), lambda A: -70.0 + 100.0 * A)[0]
confere('T9 compatível: supralinear suave dá o MESMO limiar com e sem o teto', l0 == l1, '(%.6f × %.6f)' % (l0, l1))
acc, reg = C.escolhe_m4(None, lambda A: -70.0 + 100.0 * A, lambda A: (A < 0.85, 'mock'), a_teto=1.0)
confere('T9 frações do teto 0.25/0.5/0.9 com passo para baixo → [0.25, 0.5, 0.8]', np.allclose(acc, [0.25, 0.5, 0.8]), '(%s)' % acc)

print('TESTES: %d falha(s) %s' % (len(FALHAS), FALHAS), flush=True)
sys.exit(1 if FALHAS else 0)
