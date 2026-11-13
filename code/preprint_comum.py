# preprint_comum.py — prompt 0020: o que as figuras do preprint compartilham (caminhos dos resultados GRAVADOS, rótulos do artigo, gravação PDF + PNG).
# Sem NEURON. Cada figura tem o seu script (preprint_fig1_… a preprint_fig6_…); preprint_figuras.py roda todas e grava figuras.json.
import os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
AQ = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQ, 'results'); L = os.path.join(RES, 'etapaA_lotes')
TAUS = ['0.0', '1.0', '10.0', '50.0']; TL = ['white', 'OU 1 ms', 'OU 10 ms', 'OU 50 ms']
LAB = {'pilot-6 (soma + 5)': 'soma + 5 sites', 'batch 1 (soma + 10)': 'soma + 10 sites', 'batch 2 (soma + 15)': 'soma + 15 sites'}   # termos do ARTIGO (prompt 0008)
DES = {'pilot-6 (soma + 5)': (os.path.join(RES, 'etapaA_pcond'), '6inj'), 'batch 1 (soma + 10)': (os.path.join(L, 'lote1'), 'acum'), 'batch 2 (soma + 15)': (os.path.join(L, 'lote2'), 'acum')}


def salva(fig, out, nome):
    os.makedirs(out, exist_ok=True)
    for ext in ('pdf', 'png'):                                   # prompt 0021: PDF sem data de criação → a mesma figura sai bit a bit igual em cada rodada
        fig.savefig(os.path.join(out, '%s.%s' % (nome, ext)), dpi=200, bbox_inches='tight', metadata={'CreationDate': None} if ext == 'pdf' else None)
    plt.close(fig); return nome
