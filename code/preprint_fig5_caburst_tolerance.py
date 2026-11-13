# preprint_fig5_caburst_tolerance.py — Figura 5: a especificação × a tolerância do CaBurst_PA1 (0.2 / 0.5 / 1.0 ms) e o limite inferior sem essa saída.
# Círculos: nível certificado (vazado = ponto fixo não fecha com as direções gravadas, ≥; nenhum aqui); triângulos: limite inferior sem esta saída;
# 1.0 ms = tolerância declarada — tudo isso vai na LEGENDA do artigo (prompt 0020: a linha de texto no topo saiu). Dados: sens_caburst.json, relevancia_caburst.json.
# Uso: python3 neuron/preprint_fig5_caburst_tolerance.py <dir de saída>
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprint_comum import L, TAUS, TL, LAB, plt, salva
import matplotlib.ticker
def main(out):
    SE = json.load(open(os.path.join(L, 'prompt0007', 'sens_caburst', 'sens_caburst.json')))
    RC = json.load(open(os.path.join(L, 'prompt0001', 'relevancia_caburst.json')))['sem_caburst']
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    for ax, (n, k_rc) in zip(axs, (('pilot-6 (soma + 5)', 'piloto-6'), ('batch 1 (soma + 10)', 'lote 1'), ('batch 2 (soma + 15)', None))):
        d = SE[n]
        for j, t in enumerate(TAUS):
            tv = sorted(float(v) for v in d); y = [d[str(v)][t]['certificado'] for v in tv]; ax.plot(tv, y, '-', color='C%d' % j, label=TL[j])
            for v, yy in zip(tv, y): ax.plot([v], [yy], 'o', color='C%d' % j, mfc='C%d' % j if d[str(v)]['_ponto_fixo']['fecha'] else 'none')
            if k_rc: ax.plot([2.2], [RC[k_rc]['A (conjunto gravado)']['conjuntos'][t]['certificado']], '^', color='C%d' % j)
        ax.set_xscale('log'); ax.set_yscale('log'); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.set_xticks([0.2, 0.5, 1.0, 2.2]); ax.set_xticklabels(['0.2', '0.5', '1.0', 'without\nthis output\n(≥)'], fontsize=7); ax.set_xlim(0.17, 2.8)
        if not k_rc: ax.text(2.2, 1.0, 'not\ncomputed', fontsize=6, ha='center', va='center', color='0.4')
        ax.set_title(LAB[n], fontsize=9); ax.set_xlabel('tolerance on the latency of the\nfirst spike of the Ca²⁺ burst (ms)', fontsize=8)
    axs[0].set_ylabel('certified level (mV)'); axs[0].legend(fontsize=7)
    return salva(fig, out, 'fig5_caburst_tolerance')
if __name__ == '__main__': print(main(os.path.abspath(sys.argv[1])))
