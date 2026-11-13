# etapaA_disco_guarda.py — D132 item 154: GUARDA DE DISCO antes de cada lote: grava <saida> (o portão do lote) só se o espaço livre ≥ o necessário
# declarado no plano (θ das unidades novas + rodadas de direções em voo + margem); senão grava <saida>.INSUFICIENTE.json e avisa — o lote NÃO começa.
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_disco_guarda.py <saida.json> <GiB necessários> <rótulo>
import sys, os, json, shutil, subprocess

OUT, NEC, ROT = sys.argv[1], float(sys.argv[2]), sys.argv[3]
livre = shutil.disk_usage(os.path.dirname(os.path.abspath(OUT))).free / 2**30; ok = livre >= NEC
print('%s: %.1f GiB livres; necessários %.1f GiB → %s' % (ROT, livre, NEC, 'OK' if ok else 'INSUFICIENTE — o lote NÃO começa'))
json.dump({'rotulo': ROT, 'livre_GiB': livre, 'necessario_GiB': NEC}, open(OUT if ok else OUT[:-5] + '.INSUFICIENTE.json', 'w'), indent=1)
if not ok:
    try: subprocess.run(['notify-send', '-u', 'critical', 'HANU Etapa A — %s' % ROT, 'Disco insuficiente: %.1f de %.1f GiB' % (livre, NEC)], timeout=10)
    except Exception: pass
