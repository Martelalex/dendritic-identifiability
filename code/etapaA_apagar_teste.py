# etapaA_apagar_teste.py — D132 item 154 (1b): TESTE PONTA A PONTA (resposta conhecida) do caminho "--acumular … --apagar-direcoes" do etapaA_piloto,
# numa unidade SINTÉTICA pequena (2 leituras; mesmas formas de arquivo, grade e protocolos das reais; direções e repousos do piloto condicionado):
# (A) dirs_<ponto>: acumulados gravados e relidos IDÊNTICOS → os .npy da rodada de direções APAGADOS, manifesto com os mesmos arquivos e bytes, .npz
#     ficam, os θ ficam INTOCADOS; (B) mesma rodada num diretório que NÃO é dirs_* → RECUSADO, nada apagado.
# (C) itens 157/158: um subpasso da rodada marcado NÃO AVALIADO → a unidade SAI do lote: ok.json com "excluida" e o motivo; nada apagado, sem acumulados.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_apagar_teste.py
import sys, os, json, glob, shutil, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_model as EM

AQUI = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(AQUI, 'results', 'teste_apagar'); P = os.path.join(AQUI, 'results', 'etapaA_pcond')
shutil.rmtree(T, ignore_errors=True); NOME = 'g_apic[60]_32'; rng = np.random.default_rng(154)
SUBS = ['base'] + ['%s_%s' % (n, g) for n in EM.THETA_NAMES for g in ('mais', 'menos')]
k = len(np.load(os.path.join(P, 'direcoes.npz'))['excursoes']); DSUB = ['dir%02d_%s' % (q, g) for q in range(k) for g in ('mais', 'menos')]
t1 = np.arange(11501) * 0.1; t4 = np.arange(3001) * 0.1
on = lambda t, a, b: np.clip((t - a) / 20.0, 0, 1) * (t < b)


def grava(d, subs):
    os.makedirs(d, exist_ok=True)
    for sn in subs:
        e = 1 + 0.01 * rng.normal(); np.save(os.path.join(d, '%s.M1m.npy' % sn), np.stack([-5 * e * on(t1, 100, 1100), -2 * e * on(t1, 100, 1100)]))
        np.save(os.path.join(d, '%s.M1p.npy' % sn), np.stack([5 * e * on(t1, 100, 1100), 2 * e * on(t1, 100, 1100)]))
        np.save(os.path.join(d, '%s.M4.npy' % sn), np.stack([np.stack([3 * a * e * np.exp(-((t4 - 15) / 8) ** 2)] * 2) for a in (1, 2, 3)]))
        np.savez(os.path.join(d, '%s.npz' % sn), t_repouso_s=np.array(0.0))


TH = os.path.join(T, 'unid', 'p_' + NOME); grava(TH, SUBS)
F = []
for rot, nome_dir in (('A', 'dirs_' + NOME), ('B', 'outro_' + NOME), ('C', 'dirs2_' + NOME)):
    DD = os.path.join(T, nome_dir, 'p_' + NOME); grava(DD, ['base'] + DSUB)
    if rot == 'C': np.savez(os.path.join(DD, '%s.npz' % DSUB[3]), nao_avaliado=np.array('guarda: teste'))   # item 157: um subpasso NÃO AVALIADO
    antes_th = sorted(os.listdir(TH)); antes = sorted(glob.glob(os.path.join(glob.escape(DD), '*.npy'))); tam = {f: os.path.getsize(f) for f in antes}
    PREF = os.path.join(T, 'acc_' + rot)
    cmd = [sys.executable, os.path.join(AQUI, 'etapaA_piloto.py'), os.path.join(AQUI, 'results', 'etapaA_G8', 'G.npz'), '--soma', os.path.join(AQUI, 'results', 'etapaA_conf', 'soma64_1e-8', 'p_soma'),
           '--distal', '%s=%s=%s' % (NOME, TH, DD), '--vrest', os.path.join(P, 'vrest.npz'), '--dirtag', 'cnd', '--acumular', NOME, os.path.join(P, 'direcoes.npz'), PREF, '--apagar-direcoes']
    r = subprocess.run(cmd, capture_output=True, text=True); depois = sorted(glob.glob(os.path.join(glob.escape(DD), '*.npy')))
    th_ok = sorted(os.listdir(TH)) == antes_th; npz_ficam = len(glob.glob(os.path.join(glob.escape(DD), '*.npz'))) == len(DSUB) + 1
    if rot == 'A':
        man = [l.split('\t') for l in open(PREF + '.apagados.txt').read().splitlines() if not l.startswith('#')] if os.path.exists(PREF + '.apagados.txt') else []
        ok = (r.returncode == 0 and not depois and th_ok and npz_ficam and sorted(m[0] for m in man) == antes and all(int(m[1]) == tam[m[0]] for m in man)
              and json.load(open(PREF + '.ok.json'))['ok'] and all(v['relido_identico'] for v in json.load(open(PREF + '.ok.json'))['variantes'].values()))
        d = '(A) dirs_*: acumulados relidos idênticos → %d .npy apagados, manifesto confere, θ intactos, .npz ficam' % len(antes)
    elif rot == 'B':
        ok = r.returncode != 0 and 'recusado' in r.stderr and depois == antes and th_ok and not os.path.exists(PREF + '.apagados.txt')
        d = '(B) diretório que NÃO é dirs_*: RECUSADO, nada apagado'
    else:
        okj = json.load(open(PREF + '.ok.json')) if os.path.exists(PREF + '.ok.json') else {}
        ok = (r.returncode == 0 and okj.get('excluida') is True and 'NÃO AVALIADO' in okj.get('motivo', '') and depois == antes and th_ok
              and not os.path.exists(PREF + '.apagados.txt') and not glob.glob(PREF + '.*.npz'))
        d = '(C) subpasso NÃO AVALIADO (itens 157/158): unidade FORA do lote (ok.json "excluida"), nada apagado'
    print('%-90s %s' % (d, 'OK' if ok else 'FALHOU\n' + r.stdout[-800:] + r.stderr[-1500:]), flush=True)
    if not ok: F.append(rot)
if not F: shutil.rmtree(T)
print('TESTES: %d falha(s)' % len(F)); sys.exit(1 if F else 0)
