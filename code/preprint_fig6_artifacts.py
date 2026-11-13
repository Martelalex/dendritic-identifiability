# preprint_fig6_artifacts.py — Figura 6 (prompt 0020, refeita): os artefatos medidos em dupla precisão, em TRAÇO e em VALORES SINGULARES (o argumento do
# artigo). Sem título. Unidade: p_g_apic[60]_32 nos painéis (b) e (c).
#  (a) diferença de traço × piso do integrador (repouso_double.json), tolerâncias 10⁻⁶ e 10⁻⁸;
#  (b) repouso de 3 s ÷ repouso convergido: σ_3s/σ_conv por índice (valores_singulares.json, adendo 2 do relatório 0009): os 23 avaliáveis (≥ 10× o piso)
#      e os 2 logo abaixo do limite, marcados;
#  (c) tolerância 10⁻⁶ ÷ 10⁻⁸: σ(10⁻⁶)/σ(10⁻⁸) por índice — as 7 direções mais fracas (NÃO avaliadas pelo critério do item 103) com os valores
#      REGISTRADOS no DECISOES item 107 (18, 18, 18, 16, 8.5, 2.7× e 5.2%); as 23 avaliadas só têm o PIOR desvio gravado (1.8%, piso64.json) → faixa ±1.8%.
#      (Os traços a 10⁻⁶ e 10⁻¹⁰ já não existem; refazer o perfil completo exigiria simular de novo.)
# Uso: python3 neuron/preprint_fig6_artifacts.py <dir de saída>
import sys, os, json
import numpy as np
import matplotlib.ticker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprint_comum import RES, L, plt, salva
R107 = [18.0, 18.0, 18.0, 16.0, 8.5, 2.7, 1.052]                         # DECISOES item 107, k = 1 (a mais fraca) … 7: σ(10⁻⁶)/σ(10⁻⁸)
def main(out):
    RD = json.load(open(os.path.join(L, 'prompt0007', 'repouso_double', 'repouso_double.json')))
    VS = json.load(open(os.path.join(L, 'prompt0009', 'repouso_J', 'valores_singulares.json')))
    P64 = json.load(open(os.path.join(RES, 'etapaA_conf', 'piso64.json')))['M1 + M4 COM a representação (decide)']
    fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.8), gridspec_kw={'width_ratios': [1.25, 1, 1]})
    ax = axs[0]; labs, vals = [], []; TOL = {'1e-06': '10⁻⁶', '1e-08': '10⁻⁸'}
    for X in ('1e-06', '1e-08'):
        for fam in ('M1', 'M4'):
            r = RD[X][fam]; nf = {'M1': 'subthreshold step', 'M4': 'synaptic-like current'}[fam]
            labs += ['rest 3 s vs converged\n%s, %s' % (nf, TOL[X]), 'integrator floor\n%s, %s' % (nf, TOL[X])]; vals += [r['dif_repouso_mV'], r['piso_double_mV']]
    ax.barh(range(len(vals)), vals, color=['tab:red', 'tab:gray'] * (len(vals) // 2)); ax.set_yticks(range(len(vals))); ax.set_yticklabels(labs, fontsize=6)
    ax.axvline(7.63e-6, color='tab:blue', ls='--', label='float32 step at −75 mV (single-precision storage)'); ax.set_xscale('log'); ax.set_xlabel('max |Δ| in the trace (mV)')
    ax.legend(fontsize=6.5, loc='upper right'); ax.text(-0.02, 1.02, 'a', transform=ax.transAxes, fontsize=11, fontweight='bold', ha='right')
    ax = axs[1]; c, s3 = np.array(VS['valores_singulares']['conv']), np.array(VS['valores_singulares']['3s']); nav = len(VS['indices_acima_de_10x_piso'])
    k = np.arange(1, nav + 3); r = s3[:nav + 2] / c[:nav + 2]
    ax.axvspan(nav + 0.5, nav + 2.5, color='0.85', zorder=0); ax.text(nav + 1.5, 2.6, 'below\n10×\nfloor', fontsize=6, ha='center', va='center', color='0.35')
    ax.axhline(1, color='k', lw=0.8); ax.axhspan(1 / 1.1, 1.1, color='tab:green', alpha=0.15, label='±10% (acceptance rule)')
    ax.plot(k[:nav], r[:nav], 'o', color='tab:red', ms=4, label='23 evaluated (≥ 10× floor)'); ax.plot(k[nav:], r[nav:], 'o', mfc='none', color='tab:red', ms=4, label='2 just below the limit')
    ax.set_yscale('log'); ax.set_xlabel('singular value index (1 = strongest)'); ax.set_ylabel('σ(rest 3 s) / σ(converged)'); ax.set_xlim(0.3, nav + 2.7); ax.set_ylim(0.8, 7)
    ax.set_yticks([1, 2, 4, 6]); ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter()); ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(fontsize=6.5, loc='upper left'); ax.text(-0.02, 1.02, 'b', transform=ax.transAxes, fontsize=11, fontweight='bold', ha='right')
    ax = axs[2]; nt = 30; ev = P64['sigma_avaliados']; pior = P64['pior_6x8']
    ax.axvspan(ev + 0.5, nt + 0.5, color='0.85', zorder=0); ax.text((ev + nt + 1) / 2, 5.0, 'not\nevaluated\n(< 10×\nfloor)', fontsize=6, ha='center', va='center', color='0.35')
    ax.axhline(1, color='k', lw=0.8); ax.fill_between([0.5, ev + 0.5], 1 - pior, 1 + pior, color='tab:purple', alpha=0.35, label='23 evaluated: within ±%.1f%%\n(worst value recorded)' % (100 * pior))
    kk = np.arange(nt, nt - 7, -1); ax.plot(kk, R107, 'o', color='tab:purple', ms=4, label='7 weakest (values from the run log)')
    ax.set_yscale('log'); ax.set_xlabel('singular value index (1 = strongest)'); ax.set_ylabel('σ(10⁻⁶) / σ(10⁻⁸)'); ax.set_xlim(0.3, nt + 0.7); ax.set_ylim(0.8, 35)
    ax.set_yticks([1, 2, 5, 10, 20]); ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter()); ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(fontsize=6.5, loc='upper left'); ax.text(-0.02, 1.02, 'c', transform=ax.transAxes, fontsize=11, fontweight='bold', ha='right')
    fig.tight_layout(); return salva(fig, out, 'fig6_artifacts')
if __name__ == '__main__': print(main(os.path.abspath(sys.argv[1])))
