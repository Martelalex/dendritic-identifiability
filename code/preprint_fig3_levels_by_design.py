# preprint_fig3_levels_by_design.py — Figura 3: σ_lin e σ* por modelo de ruído e desenho; o nível certificado do experimento (o máximo entre os desenhos).
# Dados: PONTO_FIXO.json de cada desenho. Sem título. (prompt 0020: o rótulo do nível certificado não encosta mais no traço na legenda.)
# Uso: python3 neuron/preprint_fig3_levels_by_design.py <dir de saída>
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprint_comum import TAUS, TL, LAB, DES, plt, salva
from matplotlib.lines import Line2D
def pf():
    return {n: json.load(open(os.path.join(d, 'pf', 'PONTO_FIXO.json')))['conjuntos'][c] for n, (d, c) in DES.items()}
def main(out):
    PF = pf(); fig, ax = plt.subplots(figsize=(6.4, 3.8)); x = np.arange(4); w = 0.26; hs = []
    for i, (n, P) in enumerate(PF.items()):
        ss = [P[t]['sigma_estrela'] for t in TAUS]; sl = [P[t]['sigma_lin'] for t in TAUS]
        for j in range(4): ax.plot([x[j] + (i - 1) * w] * 2, [min(ss[j], sl[j]), max(ss[j], sl[j])], color='C%d' % i, lw=3, alpha=0.6)
        hs += ax.plot(x + (i - 1) * w, ss, 'v', color='C%d' % i, label='%s: σ*' % LAB[n]); hs += ax.plot(x + (i - 1) * w, sl, '^', color='C%d' % i, mfc='none', label='%s: σ_lin' % LAB[n])
    cert = [max(min(P[t]['sigma_estrela'], P[t]['sigma_lin']) for P in PF.values()) for t in TAUS]
    ax.plot(x, cert, 'k_', ms=26, mew=2)
    hs.append(Line2D([], [], color='k', marker='_', ls='none', ms=12, mew=2, label='certified level of the experiment (max over designs)'))
    ax.set_yscale('log'); ax.set_xticks(x); ax.set_xticklabels(TL); ax.set_ylabel('noise level (mV)')
    ax.legend(handles=hs, fontsize=6, ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.1), handlelength=2.2, handletextpad=0.8)
    return salva(fig, out, 'fig3_levels_by_design')
if __name__ == '__main__': print(main(os.path.abspath(sys.argv[1])))
