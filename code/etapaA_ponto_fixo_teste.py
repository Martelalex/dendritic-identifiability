# etapaA_ponto_fixo_teste.py — D132 item 163: TESTES COM RESPOSTA CONHECIDA, antes do uso, do PASSO DO PONTO FIXO (etapaA_ponto_fixo), da junção de
# VÁRIOS Fdir na análise e dos acumulados POR PROTOCOLO (etapaA_piloto --por-protocolo).
#   P1–P7 passo (sintético: 6 direções com raio·max|v| conhecido): candidatas certas e arquivo do funcional (δ = ln 2/max|v|, base copiada); teto de
#          custo → ESPERA, nada gravado; rodada 2 com σ* maior → só a nova; r > r_max → NÃO ALCANÇADO; sem candidatas → PONTO_FIXO com certificado = min;
#          análise que não usou os Fdir dados → recusa; direção em dois Fdir → recusa.
#   P8     premissa da MONOTONIA: condicionar (tirar direções) nunca aumenta a variância de um funcional linear (500 casos aleatórios).
#   A1     análise do lote 1 com o código modificado e "--fdir Fdir.json" → piloto_fis.json do lote 1 IDÊNTICO (caminho padrão intocado).
#   A2     "--fdir Fdir.json,<v_6 DENTRO>" → o σ* otimista do item 162 (2c'), calculado por código INDEPENDENTE (etapaA_lote1_diag).
#   C1     unidade SINTÉTICA com aceleração SÓ no M4 (traços das direções = base no M1): Jᵀa, aᵀa do M1m e M1p = 0 exatos; M4 = total; soma = total.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_ponto_fixo_teste.py
import sys, os, json, math, shutil, subprocess, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_ponto_fixo as PF
import etapaA_model as EM

AQ = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQ, 'results'); T = tempfile.mkdtemp(prefix='pf_teste_', dir=RES); FAL = []
def confere(n, ok, msg=''):
    print('%-92s %s %s' % (n, 'OK' if ok else 'FALHOU', msg), flush=True)
    if not ok: FAL.append(n)


# ---------------- P1–P7: o passo, sintético
rng = np.random.default_rng(163); NP = 30; s0 = 2.0
Q, _ = np.linalg.qr(rng.normal(size=(NP, NP))); V = Q[:, :6].T; mx = np.abs(V).max(1)
alvo = np.array([3.0, 1.5, 0.9, 0.5, 0.69, 0.70])                  # raio·max|v| com σ* = s0 (ln 2 = 0.6931: v_5 abaixo, v_6 acima por pouco)
sig = s0 * math.sqrt(NP * PF.F) * mx / alvo
FZ = os.path.join(T, 'direcoes.npz'); np.savez(FZ, V=V, excursoes=np.full(6, 0.5), indices=np.arange(6), sigma=sig)
GD0 = os.path.join(T, 'Gdir0', 'G'); os.makedirs(GD0); np.savez(os.path.join(GD0, 'base.npz'), F=np.arange(3.0)); open(os.path.join(GD0, 'IMPRESSAO'), 'w').write('x')
def an(nome, s, det):
    p = os.path.join(T, nome); json.dump({'determinadas': det, 'conjuntos': {'acum': {t: {'sigma_estrela': s * f, 'sigma_lin': 1.0 + f, 'limitante': 'x', 'v_lin': 4}
                                          for t, f in (('0.0', 1.0), ('1.0', 0.5), ('10.0', 0.3), ('50.0', 0.2))}}}, open(p, 'w')); return p
def fdir(nome, d):
    p = os.path.join(T, nome); json.dump({'direcoes': {'v_%d' % k: {'veredito': 'DENTRO nos dois extremos' if v else 'FORA'} for k, v in d.items()}}, open(p, 'w')); return p
F0 = fdir('Fdir0.json', {1: True, 2: False}); A0 = an('an0.json', s0, [1]); P_ = os.path.join(T, 'pf')
r = PF.passo(FZ, A0, 'acum', F0, 1, 2, 7, GD0, P_); z = np.load(os.path.join(P_, 'dirF_1.npz'))
confere('P1 candidatas = v_3, v_6 (v_5 0.69 < ln 2; testadas fora); δ = ln 2/max|v|; base copiada',
        r == 'CANDIDATAS' and list(z['indices']) == [2, 5] and np.array_equal(z['V'], V[[2, 5]]) and np.allclose(z['excursoes'], math.log(2) / mx[[2, 5]])
        and open(os.path.join(P_, 'Gdir_1', 'G', 'IMPRESSAO')).read() == 'x' and np.array_equal(np.load(os.path.join(P_, 'Gdir_1', 'G', 'base.npz'))['F'], np.arange(3.0)))
P2 = os.path.join(T, 'pf2'); r = PF.passo(FZ, A0, 'acum', F0, 1, 2, 3, GD0, P2)
confere('P2 custo 4 avaliações > teto 3 → ESPERA_DECISAO_CUSTO, nenhum arquivo do funcional', r == 'ESPERA_DECISAO_CUSTO' and os.path.exists(os.path.join(P2, 'ESPERA_DECISAO_CUSTO.json'))
        and not os.path.exists(os.path.join(P2, 'dirF_1.npz')))
F1 = fdir('Fdir1.json', {3: True, 6: False}); A1 = an('an1.json', 1.2 * s0, [1, 3])
r = PF.passo(FZ, A1, 'acum', F0 + ',' + F1, 2, 2, 7, GD0, P_); z = np.load(os.path.join(P_, 'dirF_2.npz')); pj = json.load(open(os.path.join(P_, 'passo_2.json')))
confere('P3 rodada 2 (σ* ×1.2): só v_5 (0.83) nova; v_4 (0.60) não; 4 avaliações já contadas', r == 'CANDIDATAS' and list(z['indices']) == [4] and pj['aval_feitas'] == 4)
F2 = fdir('Fdir2.json', {5: True}); A2 = an('an2.json', 1.5 * s0, [1, 3, 5]); P4 = os.path.join(T, 'pf4'); os.makedirs(P4)
r = PF.passo(FZ, an('an2b.json', 1.5 * s0 * 1.25, [1, 3, 5]), 'acum', ','.join([F0, F1, F2]), 3, 2, 7, GD0, P4)   # v_4: 0.5·1.875 = 0.94 → candidata
confere('P4 rodada 3 > r_max 2 com candidata (v_4) → PONTO_FIXO_NAO_ALCANCADO', r == 'NAO_ALCANCADO' and os.path.exists(os.path.join(P4, 'PONTO_FIXO_NAO_ALCANCADO.json')))
r = PF.passo(FZ, A2, 'acum', ','.join([F0, F1, F2]), 3, 5, 9, GD0, P_)
ok5 = r == 'CANDIDATAS' and list(np.load(os.path.join(P_, 'dirF_3.npz'))['indices']) == [3]   # σ* ×1.5: v_4 0.75 > ln 2 → candidata (NÃO é ponto fixo)
F3 = fdir('Fdir3.json', {4: False}); r = PF.passo(FZ, A2, 'acum', ','.join([F0, F1, F2, F3]), 4, 5, 9, GD0, P_)
J = json.load(open(os.path.join(P_, 'PONTO_FIXO.json'))) if r == 'PONTO_FIXO' else {}
confere('P5 σ* ×1.5: v_4 (0.75) ainda candidata; testada (FORA) → PONTO FIXO; certificado = min(σ*, σ_lin); campos da análise mantidos',
        ok5 and r == 'PONTO_FIXO' and J['conjuntos']['acum']['0.0']['certificado'] == min(1.5 * s0, 2.0) and math.isclose(J['conjuntos']['acum']['50.0']['certificado'], 0.2 * 1.5 * s0, rel_tol=1e-12)
        and J['ponto_fixo']['alcancado_na_rodada'] == 4 and J['determinadas'] == [1, 3, 5])
try: PF.passo(FZ, an('an_x.json', s0, [1, 3]), 'acum', F0, 1, 2, 7, GD0, os.path.join(T, 'pfx')); ok = False
except AssertionError: ok = True
confere('P6 análise com resolvidas ≠ as dos Fdir dados → RECUSA', ok)
try: PF.passo(FZ, A0, 'acum', F0 + ',' + fdir('Fdir_dup.json', {2: True}), 2, 2, 7, GD0, os.path.join(T, 'pfy')); ok = False
except AssertionError: ok = True
confere('P7 direção testada em dois Fdir → RECUSA', ok)
# ---------------- P8: monotonia (condicionar não aumenta a variância)
pior = -np.inf
for _ in range(500):
    X = rng.normal(size=(60, NP)); G = X.T @ X + 1e-3 * np.eye(NP); g = rng.normal(size=NP); Qb, _ = np.linalg.qr(rng.normal(size=(NP, NP)))
    k = int(rng.integers(1, 10)); B, Bp = Qb, Qb[:, k:]
    v = lambda B: float(g @ B @ np.linalg.inv(B.T @ G @ B) @ B.T @ g); pior = max(pior, v(Bp) / v(B) - 1)
confere('P8 tirar k direções nunca aumenta a variância de g·θ (500 casos)', pior <= 1e-9, '(maior aumento relativo %.1e)' % pior)

# ---------------- A1/A2: junção de Fdir na análise (dados reais do lote 1)
L1 = os.path.join(RES, 'etapaA_lotes', 'lote1'); PC = ['g_apic[60]_32', 'g_apic[36]_16', 'g_apic[9]_16', 'g_apic[44]_48', 'g_apic[64]_48']
NOV = ['g_apic[70]_48', 'g_apic[77]_48', 'g_apic[37]_32', 'g_apic[19]_16', 'g_apic[17]_16']; ACC = PC + NOV
def analise(fd, out):
    cmd = [sys.executable, os.path.join(AQ, 'etapaA_piloto.py'), os.path.join(RES, 'etapaA_G8', 'G.npz'), '--soma', os.path.join(RES, 'etapaA_conf', 'soma64_1e-8', 'p_soma'),
           '--analise', os.path.join(L1, 'direcoes.npz'), out, '--fdir', fd, '--conjuntos', 'acum=' + ','.join(ACC),
           '--acumulados', ','.join('%s=%s/acc_%s' % (p, L1, p) for p in ACC) + ',soma=%s/acc_soma' % L1, '--variante', 'fis']
    r = subprocess.run(cmd, capture_output=True, text=True); return r, (json.load(open(out)) if os.path.exists(out) else None)
r, J = analise(os.path.join(L1, 'Fdir.json'), os.path.join(T, 'a1.json')); R1 = json.load(open(os.path.join(L1, 'piloto_fis.json')))
confere('A1 "--fdir Fdir.json" (código modificado) → piloto_fis.json do lote 1 IDÊNTICO', J is not None and J['conjuntos'] == R1['conjuntos'] and J['determinadas'] == R1['determinadas'],
        '' if J is not None else r.stderr[-600:])
f6 = fdir('Fdir_v6.json', {6: True}); r, J = analise(os.path.join(L1, 'Fdir.json') + ',' + f6, os.path.join(T, 'a2.json'))
D = json.load(open(os.path.join(L1, 'diag_lote1.json')))['em_jogo']['lote 1']
dif = max(abs(J['conjuntos']['acum'][t]['sigma_estrela'] / D[t]['otimista'] - 1) for t in D) if J else np.inf
confere("A2 \"--fdir Fdir.json,<v_6 DENTRO>\" → σ* otimista do item 162 (2c', código independente)", J is not None and dif < 1e-12 and sorted(J['determinadas']) == [1, 2, 4, 5, 6],
        '(maior diferença relativa %.1e)' % dif)

# ---------------- C1: acumulados por protocolo, unidade sintética com aceleração só no M4
P = os.path.join(RES, 'etapaA_pcond'); NOME = 'g_apic[60]_32'; SUBS = ['base'] + ['%s_%s' % (n, g) for n in EM.THETA_NAMES for g in ('mais', 'menos')]
k = len(np.load(os.path.join(P, 'direcoes.npz'))['excursoes']); DSUB = ['dir%02d_%s' % (q, g) for q in range(k) for g in ('mais', 'menos')]
t1 = np.arange(11501) * 0.1; t4 = np.arange(3001) * 0.1; on = lambda t, a, b: np.clip((t - a) / 20.0, 0, 1) * (t < b)
def traços(e):
    return {'M1m': np.stack([-5 * e * on(t1, 100, 1100), -2 * e * on(t1, 100, 1100)]), 'M1p': np.stack([5 * e * on(t1, 100, 1100), 2 * e * on(t1, 100, 1100)]),
            'M4': np.stack([np.stack([3 * a * e * np.exp(-((t4 - 15) / 8) ** 2)] * 2) for a in (1, 2, 3)])}
TH = os.path.join(T, 'unid', 'p_' + NOME); DD = os.path.join(T, 'dirs_' + NOME, 'p_' + NOME); os.makedirs(TH); os.makedirs(DD)
for sn in SUBS:
    for lab, x in traços(1 + 0.01 * rng.normal()).items(): np.save(os.path.join(TH, '%s.%s.npy' % (sn, lab)), x)
    np.savez(os.path.join(TH, '%s.npz' % sn), t_repouso_s=np.array(0.0))
for sn in ['base'] + DSUB:
    for lab in ('M1m', 'M1p'): shutil.copy2(os.path.join(TH, 'base.%s.npy' % lab), os.path.join(DD, '%s.%s.npy' % (sn, lab)))   # M1: traço = base → a = 0
    np.save(os.path.join(DD, '%s.M4.npy' % sn), np.load(os.path.join(TH, 'base.M4.npy')) * (1.0 if sn == 'base' else 1.03 if sn.endswith('mais') else 1.01))
    np.savez(os.path.join(DD, '%s.npz' % sn), t_repouso_s=np.array(0.0))
PREF = os.path.join(T, 'acc_c1')
cmd = [sys.executable, os.path.join(AQ, 'etapaA_piloto.py'), os.path.join(RES, 'etapaA_G8', 'G.npz'), '--soma', os.path.join(RES, 'etapaA_conf', 'soma64_1e-8', 'p_soma'),
       '--distal', '%s=%s=%s' % (NOME, TH, DD), '--vrest', os.path.join(P, 'vrest.npz'), '--dirtag', 'cnd', '--acumular', NOME, os.path.join(P, 'direcoes.npz'), PREF, '--por-protocolo']
r = subprocess.run(cmd, capture_output=True, text=True); ok = r.returncode == 0
if ok:
    oj = json.load(open(PREF + '.ok.json')); zt = {v: np.load('%s.%s.npz' % (PREF, v)) for v in ('fis', 'inf')}
    zl = {(v, l): np.load('%s.%s.%s.npz' % (PREF, v, l)) for v in ('fis', 'inf') for l in ('M1m', 'M1p', 'M4')}
    for v in ('fis', 'inf'):
        for t in ('0', '1', '10', '50'):
            ok &= all(np.all(zl[(v, l)]['%s_%s' % (n, t)] == 0) for l in ('M1m', 'M1p') for n in ('JA', 'AA'))       # a = 0 no M1: EXATO
            ok &= float(np.abs(zt[v]['AA_' + t]).max()) > 0 and np.allclose(zl[(v, 'M4')]['AA_' + t], zt[v]['AA_' + t], rtol=1e-12, atol=0)
            ok &= np.allclose(sum(zl[(v, l)]['G_' + t] for l in ('M1m', 'M1p', 'M4')), zt[v]['G_' + t], rtol=1e-12, atol=1e-300)
            ok &= all(float(np.abs(zl[(v, l)]['G_' + t]).max()) > 0 for l in ('M1m', 'M1p', 'M4'))
        ok &= oj['variantes'][v]['por_protocolo']['soma_confere_com_total']
confere('C1 aceleração só no M4: Jᵀa, aᵀa do M1m/M1p = 0 exatos; aᵀa do M4 = total; Σ Gram dos protocolos = total; ok.json confere', bool(ok),
        '' if r.returncode == 0 else r.stderr[-800:])
if not FAL: shutil.rmtree(T)
print('TESTES: %d falha(s) %s' % (len(FAL), FAL)); sys.exit(1 if FAL else 0)
