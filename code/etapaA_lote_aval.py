# etapaA_lote_aval.py — D132 itens 151/154: AVALIAÇÃO DA PARADA ao fim de um lote da Etapa A em s = 400 (regra declarada no item 151): PARAR se, para τ = 10
# E τ = 50 ms, σ*_b < 1.10·σ*_ref E σ_lin_b < 1.10·σ_lin_ref (os quatro ganhos < 10%; uma queda conta como ganho < 10%); senão SEGUIR. Cada lote nas SUAS
# direções (Gram acumulado); referência do lote 1 = piloto condicionado de 6 injeções (com a faixa). Grava <saida>/SEGUIR.json ou <saida>/PARAR.json e o
# RELATÓRIO (σ*, σ_lin nos 4 modelos, ganhos, veredito, disco) em <saida>/relatorio.txt; aviso na área de trabalho.
# ITEM 158: unidades FORA do lote (avaliação NÃO AVALIADA) → decisao(): >1 fora → PARADA_SISTEMATICA; 1 fora e a regra diz PARAR → ESPERA_DECISAO (não
# para sozinho); grava <saida>/<DECISÃO>.json — só SEGUIR.json libera o lote seguinte.
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_lote_aval.py <json do lote> <conjunto> <json de referência> <conjunto ref> <saida> [<rótulo>]
import sys, os, json, shutil, subprocess

LIM = 0.10; LENTOS = ('10.0', '50.0'); TODOS = ('0.0', '1.0', '10.0', '50.0')


def veredito(cur, ref):
    """cur/ref: {τ: {'sigma_estrela', 'sigma_lin'}} → (PARAR?, ganhos {τ: (g*, g_lin)})."""
    g = {t: (cur[t]['sigma_estrela'] / ref[t]['sigma_estrela'] - 1, cur[t]['sigma_lin'] / ref[t]['sigma_lin'] - 1) for t in TODOS}
    parar = all(cur[t]['sigma_estrela'] < (1 + LIM) * ref[t]['sigma_estrela'] and cur[t]['sigma_lin'] < (1 + LIM) * ref[t]['sigma_lin'] for t in LENTOS)   # a forma DECLARADA
    return parar, g


def decisao(cur, ref, n_fora):
    """ITEM 158 — a regra de parada com unidades FORA do lote: n_fora > 1 → PARADA_SISTEMATICA (a cadeia para e reporta); n_fora == 0 → a regra age
    sozinha (PARAR ou SEGUIR); n_fora == 1 → SEGUIR se a regra diz seguir; se a regra diz PARAR → ESPERA_DECISAO (um lote desfalcado mostra melhora MENOR —
    a assimetria empurraria a parada cedo demais). Devolve (decisão, parar_pela_regra, ganhos)."""
    parar, g = veredito(cur, ref)
    if n_fora > 1: return 'PARADA_SISTEMATICA', parar, g
    if n_fora == 0: return ('PARAR' if parar else 'SEGUIR'), parar, g
    return ('ESPERA_DECISAO' if parar else 'SEGUIR'), parar, g


if __name__ == '__main__':
    FJ, CJ, FR, CR, OUT = sys.argv[1:6]; ROT = sys.argv[6] if len(sys.argv) > 6 else os.path.basename(os.path.abspath(OUT))
    J = json.load(open(FJ)); cur = J['conjuntos'][CJ]; ref = json.load(open(FR))['conjuntos'][CR]; fora = J.get('excluidas', [])
    dec, parar, g = decisao(cur, ref, len(fora))
    du = shutil.disk_usage(OUT); nome = lambda t: 'iid' if t == '0.0' else 'OU %g ms' % float(t)
    L = ['RELATÓRIO DO %s (Etapa A em s = 400, item 151)' % ROT.upper(), '%-9s %10s %10s %10s %10s %9s %9s' % ('ruído', 'σ*', 'σ* ref', 'σ_lin', 'σ_lin ref', 'ganho σ*', 'ganho σ_lin')]
    for t in TODOS:
        L.append('%-9s %10.4g %10.4g %10.4g %10.4g %+8.1f%% %+8.1f%%%s' % (nome(t), cur[t]['sigma_estrela'], ref[t]['sigma_estrela'], cur[t]['sigma_lin'], ref[t]['sigma_lin'],
                 100 * g[t][0], 100 * g[t][1], '   ← decide' if t in LENTOS else ''))
    L.append('unidades FORA do lote: %s' % ('nenhuma (lote COMPLETO)' if not fora else '; '.join('%s — %s' % (x['unidade'], x['motivo']) for x in fora)))
    L.append('REGRA DE PARADA (ganhos < 10%% em σ* E σ_lin com τ = 10 E 50 ms): %s' % ('PARAR' if parar else 'SEGUIR'))
    L.append('DECISÃO (item 158): %s' % {'PARAR': 'PARAR — a curva saturou (lote completo)', 'SEGUIR': 'SEGUIR para o próximo lote',
             'ESPERA_DECISAO': 'NÃO PARAR SOZINHO — lote DESFALCADO e a regra diz PARAR: reportar e ESPERAR a decisão do Martel',
             'PARADA_SISTEMATICA': 'PARAR E REPORTAR — mais de uma unidade fora (problema sistemático)'}[dec])
    L.append('disco: %.1f GiB livres de %.1f GiB' % (du.free / 2**30, du.total / 2**30))
    txt = '\n'.join(L); print(txt); open(os.path.join(OUT, 'relatorio.txt'), 'w').write(txt + '\n')
    marca = os.path.join(OUT, dec + '.json')                              # só SEGUIR.json libera o próximo lote
    json.dump({'lote': ROT, 'decisao': dec, 'unidades_fora': fora, 'parar': parar, 'ganhos': {t: {'sigma_estrela': g[t][0], 'sigma_lin': g[t][1]} for t in TODOS},
               'atual': cur, 'referencia': {'arquivo': FR, 'conjunto': CR, 'valores': ref}, 'disco_livre_GiB': du.free / 2**30}, open(marca, 'w'), indent=1)
    try: subprocess.run(['notify-send'] + ([] if dec == 'SEGUIR' else ['-u', 'critical']) + ['HANU Etapa A — %s' % ROT, '%s (relatório: %s)' % (dec, os.path.join(OUT, 'relatorio.txt'))], timeout=10)
    except Exception: pass
