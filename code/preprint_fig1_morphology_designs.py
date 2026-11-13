# preprint_fig1_morphology_designs.py — Figura 1 (prompt 0020; antes fig2): a morfologia do Hay com a grade de 400 µm e os pontos de injeção de cada
# desenho (soma + 5 / + 10 / + 15). Dados: results/preprint/morfologia.npz (preprint_morfologia.py). Sem título de figura (vira legenda no artigo).
# Uso: python3 neuron/preprint_fig1_morphology_designs.py <dir de saída>
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprint_comum import RES, plt, salva
def main(out):
    z = np.load(os.path.join(RES, 'preprint', 'morfologia.npz'), allow_pickle=True); inj = json.loads(str(z['inj_json']))
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 6.2), sharey=True)
    for ax, (nome, lista) in zip(axs, inj['desenhos'].items()):
        for P in z['xyz']:
            if getattr(P, 'ndim', 0) == 2 and len(P): ax.plot(P[:, 0], P[:, 1], color='0.55', lw=0.5)
        gr = z['grade']; ax.plot(gr[:, 0], gr[:, 1], 'o', mfc='none', mec='tab:blue', ms=6, label='400-µm grid (20 candidate points)')
        q = np.array([inj['pos'][p] for p in lista]); ax.plot(q[:, 0], q[:, 1], '*', color='tab:red', ms=10, label='injection points')
        ax.plot(*z['soma'][:2], 'ks', ms=6, label='soma (injection + readout)')
        ax.set_title({'piloto-6': 'soma + 5 sites', 'lote 1': 'soma + 10 sites', 'lote 2': 'soma + 15 sites'}[nome], fontsize=9); ax.set_aspect('equal'); ax.set_xlabel('x (µm)')
    axs[0].set_ylabel('y (µm)'); axs[0].legend(fontsize=6, loc='lower left')
    return salva(fig, out, 'fig1_morphology_designs')
if __name__ == '__main__': print(main(os.path.abspath(sys.argv[1])))
