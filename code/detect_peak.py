# detect_peak.py — D132 item 43: DETECTOR DE ANÁLISE "PICO-PRIMEIRO" (substitui active_l1_detect.spikes nas análises novas;
# o antigo fica intacto — a fila do V2 ainda o importa).
# Regras (declaradas antes de validar):
#   1. CANDIDATO = pico local do V do soma com altura > −30 mV e proeminência ≥ 20 mV (scipy.signal.find_peaks), no traço
#      interpolado a 0.025 ms. Um degrau de corrente não gera pico com essa proeminência DURANTE o degrau.
#   2. SUBIDA = o cruzamento de dV/dt > 20 mV/ms MAIS PRÓXIMO do pico: c = último índice antes do pico com dV/dt > 20;
#      exige-se pico − c ≤ 5 ms (max_interval do IPFX). Isso rejeita o máximo de fim de degrau num modelo passivo (o
#      último dV/dt > 20 foi no início do degrau, ~1 s antes).
#   3. INÍCIO (data do limiar) = começo do trecho contínuo com dV/dt > 20 que termina em c, interpolado no cruzamento.
#      AMBÍGUO se esse trecho começa num instante de ESTÍMULO (descontinuidade dada pelo chamador, tolerância de 1
#      amostra): o disparo CONTA, mas NÃO recebe data de início (onset = None).
#   4. MARCAS: 'peak' (tempo do pico) para comparações de MÉTODO e para ISIs; 'onset' (limiar) só para comparação com
#      DADOS que usam a convenção do IPFX.
import numpy as np
from scipy.signal import find_peaks

DT = 0.025


def detect(t, v, lo, hi, stim_times=(), dt=DT):
    """t, v: traço (qualquer amostragem); [lo, hi): janela; stim_times: instantes de descontinuidade do estímulo.
    Retorna lista de dicts {'peak': t_pico, 'onset': t_limiar ou None, 'ambiguous': bool, 'v_peak': mV}."""
    tt = np.arange(0.0, float(t[-1]), dt); vv = np.interp(tt, np.asarray(t), np.asarray(v))
    dv = np.diff(vv) / dt                                    # dv[i] = inclinação entre tt[i] e tt[i+1]
    pk, _ = find_peaks(vv, height=-30.0, prominence=20.0)
    out = []
    for p in pk:
        if not (lo <= tt[p] < hi): continue
        above = np.flatnonzero(dv[:p] > 20.0)
        if above.size == 0: continue
        c = above[-1]
        if tt[p] - tt[c] > 5.0: continue                     # regra 2
        r = c
        while r > 0 and dv[r - 1] > 20.0: r -= 1             # regra 3: começo do trecho contínuo
        # cruzamento interpolado entre tt[r-1] (≤ 20) e tt[r] (> 20), em termos da inclinação
        if r > 0 and dv[r] != dv[r - 1]:
            onset = tt[r] + (20.0 - dv[r - 1]) / (dv[r] - dv[r - 1]) * dt - dt / 2
        else:
            onset = tt[r]
        amb = any(abs(tt[r] - s) <= dt + 1e-9 or (s <= tt[r] <= s + dt + 1e-9) for s in stim_times)
        out.append({'peak': float(tt[p]), 'onset': None if amb else float(onset), 'ambiguous': bool(amb),
                    'v_peak': float(vv[p])})
    return out


def raw_peaks(t, v, lo, hi, dt=DT):
    """Referência independente para o controle positivo: todo máximo local > −30 mV (sem critério de subida)."""
    tt = np.arange(0.0, float(t[-1]), dt); vv = np.interp(tt, np.asarray(t), np.asarray(v))
    pk, _ = find_peaks(vv, height=-30.0)
    return [float(tt[p]) for p in pk if lo <= tt[p] < hi]
