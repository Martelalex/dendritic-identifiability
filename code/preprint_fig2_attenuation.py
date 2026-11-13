# preprint_fig2_attenuation.py — Figura 2 (prompt 0020; antes fig1): atenuação estacionária ao longo do tronco apical — modelo do Hay × ajustes Allen ×
# as FAIXAS DE ACEITAÇÃO do critério C1 (DECISOES D131, "CRITÉRIOS DE CONFRONTO — DECLARADOS ANTES DE RODAR"; derivadas de Stuart & Spruston 1998,
# Fig. 1F, controle): razão a 100 µm ∈ [0.6, 1.0] (barra vertical em 100 µm), distância de 50% ∈ [250, 450] µm (barra horizontal em 0.5), razão a
# 500 µm ∈ [0.05, 0.52] (barra vertical em 500 µm; o lido 0.1–0.26 alargado por fator 2). Sem título de figura.
# Uso: python3 neuron/preprint_fig2_attenuation.py <dir de saída>
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprint_comum import RES, plt, salva
def perfil(d, pts):
    return np.array(sorted((pts[k]['dist'], d['s2' + k]) for k in pts if k.startswith('apical_') and k[7:].isdigit() and 's2' + k in d))
def main(out):
    H = json.load(open(os.path.join(RES, 'hay', 'hay_d1.json'))); A = {k: json.load(open(os.path.join(RES, 'target', 'pyr_%s.json' % k))) for k in ('aa', 'peri')}
    fig, ax = plt.subplots(figsize=(4.6, 3.4)); B = dict(color='0.6', alpha=0.5)
    ax.add_patch(plt.Rectangle((95, 0.6), 10, 0.4, **B)); ax.add_patch(plt.Rectangle((495, 0.05), 10, 0.47, **B)); ax.plot([250, 450], [0.5, 0.5], lw=6, solid_capstyle='butt', **B)
    h1 = perfil(H['A_step50'], H['points']); ax.plot(h1[:, 0], h1[:, 1], 'o-', color='k', label='Hay et al. 2011 model (active, −50 pA)')
    for k, lab, c in (('aa', 'Allen fit, all-active', 'tab:blue'), ('peri', 'Allen fit, perisomatic', 'tab:orange')):
        p = perfil(A[k]['passive_d01'], A[k]['points']); ax.plot(p[:, 0], p[:, 1], 's--', color=c, ms=3, label=lab)
    ax.annotate('50% reached\nat 250–450 µm', xy=(450, 0.5), xytext=(520, 0.58), fontsize=7, ha='left', va='center', arrowprops=dict(arrowstyle='-', color='0.5', lw=0.6))
    ax.plot([], [], lw=6, label='acceptance bands (criterion C1,\nfrom Stuart & Spruston 1998)', **B)
    ax.set_xlabel('distance from soma along the apical trunk (µm)'); ax.set_ylabel('steady-state attenuation (dendrite / soma)')
    ax.legend(fontsize=6.5, loc='upper right'); ax.set_ylim(0, 1.05)
    return salva(fig, out, 'fig2_attenuation')
if __name__ == '__main__': print(main(os.path.abspath(sys.argv[1])))
