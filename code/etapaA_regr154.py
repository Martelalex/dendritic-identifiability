# etapaA_regr154.py — D132 item 154 (1a): REGRESSÃO do caminho "acumulados por unidade → análise" contra o piloto condicionado: os JSONs refeitos SÓ a
# partir dos acumulados gravados têm de ser IGUAIS aos de referência (piloto_fis.json / piloto_inf.json) — números (objeto JSON) e texto. Grava
# <R>/regr154_ok.json só se as duas variantes forem idênticas.
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_regr154.py <dir dos refeitos> <dir de referência>
import sys, os, json
N, REF = sys.argv[1:3]; ok = True; rel = {}
for v in ('fis', 'inf'):
    a, b = os.path.join(N, 'piloto_%s.json' % v), os.path.join(REF, 'piloto_%s.json' % v)
    oa, ob = json.load(open(a)), json.load(open(b)); ta, tb = open(a).read(), open(b).read()
    rel[v] = {'objeto_igual': oa == ob, 'texto_igual': ta == tb}; ok &= oa == ob and ta == tb
    print('%s: números %s; texto %s' % (v, 'IGUAIS' if oa == ob else 'DIFERENTES', 'IGUAL' if ta == tb else 'DIFERENTE'))
    if oa != ob:
        for cn in ob.get('conjuntos', {}):
            for t in ob['conjuntos'][cn]:
                x, y = oa['conjuntos'][cn][t], ob['conjuntos'][cn][t]
                if x != y: print('   %s τ=%s: refeito %s × referência %s' % (cn, t, x, y))
if ok: json.dump({'item': 154, 'regressao': rel}, open(os.path.join(N, 'regr154_ok.json'), 'w'), indent=1)
print('REGRESSÃO dos acumulados por unidade: %s' % ('IDÊNTICA bit a bit → o caminho novo está liberado' if ok else 'FALHOU — nada é apagado, o lote 1 NÃO é lançado'))
sys.exit(0 if ok else 1)
