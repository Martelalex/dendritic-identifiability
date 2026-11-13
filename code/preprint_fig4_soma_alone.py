# preprint_fig4_soma_alone.py — Figura 4: o soma sozinho × o combinado (as mesmas direções conhecidas dos dois lados): nível certificado combinado ÷ σ*
# do soma sozinho. Como σ* limita por cima o nível certificado do soma sozinho, a razão é um LIMITE INFERIOR (≥) da desvantagem — dito na legenda do
# artigo (prompt 0020: sem título na figura). Dados: PONTO_FIXO.json e soma_fis.json de cada desenho.
# Uso: python3 neuron/preprint_fig4_soma_alone.py <dir de saída>
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprint_comum import RES, TAUS, TL, LAB, DES, plt, salva
from preprint_fig3_levels_by_design import pf
def razoes():
    PF = pf(); S = {n: json.load(open(os.path.join(d if 'pilot' not in n else os.path.join(RES, 'etapaA_pcond'), 'soma_fis.json')))['conjuntos']['soma'] for n, (d, c) in DES.items()}
    return {n: [min(PF[n][t]['sigma_estrela'], PF[n][t]['sigma_lin']) / S[n][t]['sigma_estrela'] for t in TAUS] for n in PF}
def main(out):
    R = razoes(); fig, ax = plt.subplots(figsize=(6.0, 3.6)); x = np.arange(4)
    for i, (n, r) in enumerate(R.items()): ax.plot(x, r, 'o-', color='C%d' % i, label=LAB[n])
    ax.axhline(1, color='k', lw=0.8); ax.set_yscale('log'); ax.set_xticks(x); ax.set_xticklabels(TL)
    ax.set_ylabel('combined certified level / soma-alone σ*'); ax.legend(fontsize=7)
    return salva(fig, out, 'fig4_soma_alone')
if __name__ == '__main__': print(main(os.path.abspath(sys.argv[1])))
