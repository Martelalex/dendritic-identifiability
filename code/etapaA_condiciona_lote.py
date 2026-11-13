# etapaA_condiciona_lote.py — D132 itens 151/154: PORTÃO do condicionamento de um LOTE (os mesmos critérios do item 146/147, sem a regressão — o código das
# unidades é o já regredido no item 147): todo ponto do lote passa (b) e (c) e tem ≥ 1 amplitude do M4. Grava <R>/condicionamento.json (sempre),
# <R>/amplitudes.json = as amplitudes ANTERIORES (todas as unidades já feitas) + as do lote, e o portão <R>/condicionamento_ok.json SÓ se tudo passar.
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_condiciona_lote.py <R do lote> <p1,p2,…> <amplitudes anteriores.json>
import sys, os, json

R, PONTOS, ANT = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
amps = json.load(open(ANT)); res = {'pontos': {}}; ok = True
print('%-15s %9s %8s %9s %8s %7s | %-9s %s' % ('ponto', 'R_in MΩ', 'alvo mV', 'I M1 pA', 'ρ_I', '(c)', 'limiar nA', 'M4 nA (fator do limiar)'))
for p in PONTOS:
    assert p not in amps, ('ponto já tem amplitudes', p)
    c = json.load(open(os.path.join(R, 'cond_%s.json' % p))); m = c['M1']; b = c.get('bordas', {}); lim = c['M4_limiar']
    pok = m['passa'] and b.get('passa', False) and len(c['M4']) >= 1; ok &= pok
    omit = [x['pedida'] for x in c['M4_registro'] if x['final'] is None]
    res['pontos'][p] = {'passa': pok, 'M1': m, 'bordas': b, 'M4': c['M4'], 'M4_limiar': lim, 'M4_registro': c['M4_registro'], 'omitidas': omit}
    if pok: amps[p] = {'M1': m['I_nA'], 'M4': c['M4']}
    print('%-15s %9.1f %8s %9s %8s %7s | %-9s %s%s' % (p, m['R_in_MOhm'], '—' if m['alvo_mV'] is None else '%.2f' % m['alvo_mV'],
          '—' if m['I_nA'] is None else '%.2f' % (1e3 * m['I_nA']), '%.4f' % m['historico'][-1]['rho_I'], 'passa' if b.get('passa') else 'FALHA',
          '—' if lim is None else '%.4f' % lim, ', '.join('%.4f%s' % (a, '' if lim is None else ' (%.2f×)' % (a / lim)) for a in c['M4']),
          '' if not omit else ' | OMITIDAS: %s' % omit))
res['portao'] = bool(ok); json.dump(res, open(os.path.join(R, 'condicionamento.json'), 'w'), indent=1, default=float)
if ok:
    json.dump(amps, open(os.path.join(R, 'amplitudes.json'), 'w'), indent=1)
    json.dump({'item': 154, 'pontos': PONTOS}, open(os.path.join(R, 'condicionamento_ok.json'), 'w'))
print('PORTÃO: %s' % ('ABERTO → amplitudes.json (%d pontos no total)' % len(amps) if ok else 'FECHADO — o lote PARA (reportar)'))
