# etapaA_excluida_teste.py — D132 item 158: TESTE COM RESPOSTA CONHECIDA da análise com uma unidade FORA do lote: com os acumulados do piloto condicionado
# (regr154), a análise de "acum = as 5 distais" com UMA marcada como excluída (ok.json "excluida") tem de dar EXATAMENTE os mesmos números que a análise de
# "acum = as outras 4" sem exclusão — e registrar a excluída com o motivo.
# Uso: python3 neuron/lancar.py distal --esperar -- .nrnvenv/bin/python neuron/etapaA_excluida_teste.py
import sys, os, json, shutil, subprocess, glob
AQUI = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(AQUI, 'results', 'etapaA_lotes', 'regr154'); T = os.path.join(AQUI, 'results', 'teste_excluida')
P = os.path.join(AQUI, 'results', 'etapaA_pcond'); shutil.rmtree(T, ignore_errors=True); os.makedirs(T)
U = ['g_apic[60]_32', 'g_apic[36]_16', 'g_apic[9]_16', 'g_apic[44]_48', 'g_apic[64]_48']; X = 'g_apic[9]_16'
for f in glob.glob(os.path.join(glob.escape(R), 'acc_*')): shutil.copy(f, T)
json.dump({'unidade': X, 'ok': True, 'excluida': True, 'motivo': 'NÃO AVALIADO (teste): subpasso sintético'}, open(os.path.join(T, 'acc_%s.ok.json' % X), 'w'))
for f in glob.glob(os.path.join(glob.escape(T), 'acc_%s.*.npz' % glob.escape(X))): os.remove(f)
base = [sys.executable, os.path.join(AQUI, 'etapaA_piloto.py'), os.path.join(AQUI, 'results', 'etapaA_G8', 'G.npz'), '--soma', os.path.join(AQUI, 'results', 'etapaA_conf', 'soma64_1e-8', 'p_soma'),
        '--analise', os.path.join(P, 'direcoes.npz')]
lst = lambda us: ','.join('%s=%s' % (u, os.path.join(T, 'acc_' + u)) for u in us) + ',soma=' + os.path.join(T, 'acc_soma')
rA = subprocess.run(base + [os.path.join(T, 'A.json'), '--fdir', os.path.join(P, 'Fdir.json'), '--conjuntos', 'acum=' + ','.join(U), '--acumulados', lst(U), '--variante', 'fis'], capture_output=True, text=True)
U4 = [u for u in U if u != X]
rB = subprocess.run(base + [os.path.join(T, 'B.json'), '--fdir', os.path.join(P, 'Fdir.json'), '--conjuntos', 'acum=' + ','.join(U4), '--acumulados', lst(U4), '--variante', 'fis'], capture_output=True, text=True)
A, B = json.load(open(os.path.join(T, 'A.json'))), json.load(open(os.path.join(T, 'B.json')))
ok1 = A['conjuntos'] == B['conjuntos']; ok2 = [x['unidade'] for x in A.get('excluidas', [])] == [X] and B.get('excluidas') == []
print('%-92s %s' % ('(1) 5 unidades com UMA excluída = as outras 4 sem exclusão (σ*, σ_lin, 4 modelos de ruído)', 'OK' if ok1 else 'FALHOU'))
print('%-92s %s' % ('(2) a excluída registrada com o motivo; nenhuma na outra', 'OK' if ok2 else 'FALHOU %s %s' % (A.get('excluidas'), B.get('excluidas'))))
print('   ex.: OU 50 ms σ* %.4g × %.4g; σ_lin %.4g × %.4g' % (A['conjuntos']['acum']['50.0']['sigma_estrela'], B['conjuntos']['acum']['50.0']['sigma_estrela'],
      A['conjuntos']['acum']['50.0']['sigma_lin'], B['conjuntos']['acum']['50.0']['sigma_lin']))
if ok1 and ok2: shutil.rmtree(T)
else: print(rA.stderr[-1500:], rB.stderr[-1500:])
print('TESTES: %d falha(s)' % (int(not ok1) + int(not ok2))); sys.exit(0 if ok1 and ok2 else 1)
