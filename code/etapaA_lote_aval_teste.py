# etapaA_lote_aval_teste.py — D132 item 154: TESTE COM RESPOSTA CONHECIDA (sintético) da regra de parada (etapaA_lote_aval.veredito), antes do uso.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_lote_aval_teste.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_lote_aval as LA

ref = {t: {'sigma_estrela': 1.0, 'sigma_lin': 2.0} for t in LA.TODOS}


def cur(gs, gl, outros=(0.5, 0.5)):
    """gs/gl: {τ: ganho} nos lentos; nos rápidos, ganhos `outros` (não devem decidir)."""
    c = {t: {'sigma_estrela': 1.0 * (1 + outros[0]), 'sigma_lin': 2.0 * (1 + outros[1])} for t in LA.TODOS}
    for t in LA.LENTOS: c[t] = {'sigma_estrela': 1.0 * (1 + gs[t]), 'sigma_lin': 2.0 * (1 + gl[t])}
    return c


casos = [  # (descrição, ganho σ* {10, 50}, ganho σ_lin {10, 50}, PARAR esperado)
    ('todos os ganhos lentos 5% (rápidos +50% não decidem)', {'10.0': .05, '50.0': .05}, {'10.0': .05, '50.0': .05}, True),
    ('σ* +12% só em τ = 10', {'10.0': .12, '50.0': .05}, {'10.0': .05, '50.0': .05}, False),
    ('σ_lin +15% só em τ = 50', {'10.0': .05, '50.0': .05}, {'10.0': .05, '50.0': .15}, False),
    ('σ_lin CAI 20%, σ* +5% (queda conta como < 10%)', {'10.0': .05, '50.0': .05}, {'10.0': -.20, '50.0': -.20}, True),
    ('exatamente 10% em σ* τ = 50 (não é "menos de 10%")', {'10.0': .05, '50.0': .10}, {'10.0': .05, '50.0': .05}, False),
    ('9.99% em tudo', {'10.0': .0999, '50.0': .0999}, {'10.0': .0999, '50.0': .0999}, True),
]
F = []
for d, gs, gl, esp in casos:
    p, g = LA.veredito(cur(gs, gl), ref); ok = p == esp
    print('%-58s PARAR=%-5s esperado %-5s %s' % (d, p, esp, 'OK' if ok else 'FALHOU'))
    if not ok: F.append(d)
# ITEM 158 — a decisão com unidades FORA (a regra assimétrica)
PAR = ({'10.0': .05, '50.0': .05}, {'10.0': .05, '50.0': .05}); SEG = ({'10.0': .20, '50.0': .05}, {'10.0': .05, '50.0': .05})
casos2 = [('lote COMPLETO, regra diz PARAR → PARAR', PAR, 0, 'PARAR'), ('lote COMPLETO, regra diz SEGUIR → SEGUIR', SEG, 0, 'SEGUIR'),
          ('1 unidade FORA, regra diz SEGUIR → SEGUIR', SEG, 1, 'SEGUIR'), ('1 unidade FORA, regra diz PARAR → ESPERA_DECISAO (não para sozinho)', PAR, 1, 'ESPERA_DECISAO'),
          ('2 unidades FORA (regra diz SEGUIR) → PARADA_SISTEMATICA', SEG, 2, 'PARADA_SISTEMATICA'), ('2 unidades FORA (regra diz PARAR) → PARADA_SISTEMATICA', PAR, 2, 'PARADA_SISTEMATICA')]
for d, (gs, gl), nf, esp in casos2:
    dec, p, g = LA.decisao(cur(gs, gl), ref, nf); ok = dec == esp
    print('%-66s %-19s esperado %-19s %s' % (d, dec, esp, 'OK' if ok else 'FALHOU'))
    if not ok: F.append(d)
print('TESTES: %d falha(s)' % len(F)); sys.exit(1 if F else 0)
