# etapaA_Fdir.py — D132 item 128 (3): o FUNCIONAL ao longo das 5 direções de raio além do fator 2 (v_1…v_5), em θ·exp(±ln 2·v_i) — F
# dentro da tolerância nos DOIS extremos → a direção NÃO precisa ser determinada pelos dados (o limite fisiológico basta); fora → a
# especificação FALHA nela. Premissa declarada: faixa fisiológica = fator 2 (suposição, a confirmar na literatura).
# F completo como no G (etapaA_F.fvec + taxa contínua com o K da BASE); tolerâncias do D131 7.4 (etapaA_sstar.tol_of): EPSP 5% de F0, PA 1 ms,
# taxa 2% de F0; picos de Ca sem tolerância (reportados). Uma componente cuja CONTAGEM muda (PA do BAC/CaBurst) ou cuja taxa perde a
# identidade dos K+1 primeiros disparos conta como FORA (o funcional mudou de natureza). taxa_1.9 já é NÃO condicionada na base (item 124).
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_Fdir.py <dir da rodada (contém G/)> <dirF.npz> <saida.json> [--tol-CaBurst X]
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_F as EF
import etapaA_sstar as S

D, FZ, OUT = sys.argv[1:4]; z = np.load(FZ); k = len(z['excursoes']); ud = os.path.join(D, 'G')
b = np.load(os.path.join(ud, 'base.npz'), allow_pickle=True)
K = {a: EF.K_regra(len(b['picos_%s' % a])) for a in EF.FI_AMPS}
full = lambda sd: np.concatenate([sd['F'], [EF.taxa_K(sd['picos_%s' % a], K[a]) for a in EF.FI_AMPS]])
nomes = [str(x) for x in b['nomes']] + ['taxa_%s' % a for a in EF.FI_AMPS]; F0 = full(b); tl = [S.tol_of(n) for n in nomes]
tol = np.array([np.nan if t is None else (t[1] * abs(F0[i]) if t[0] == 'rel' else t[1]) for i, t in enumerate(tl)])
if '--tol-CaBurst' in sys.argv:                                       # item 139: SENSIBILIDADE — só a tolerância do CaBurst_PA1 (ms), rotulada
    tol[nomes.index('CaBurst_PA1')] = float(sys.argv[sys.argv.index('--tol-CaBurst') + 1]); print('SENSIBILIDADE: tolerância do CaBurst_PA1 = %g ms' % tol[nomes.index('CaBurst_PA1')])
nc = len(b['contagens']); res = {'direcoes': {}}
print('componentes com tolerância: %d; K = %s' % (int(np.isfinite(tol).sum()), K))
for q in range(k):
    vd = {}
    for g in ('mais', 'menos'):
        x = np.load(os.path.join(ud, 'dir%02d_%s.npz' % (q, g)), allow_pickle=True); Fx = full(x)
        fora = []
        for i in range(len(nomes)):
            if not np.isfinite(tol[i]): continue
            if i < nc and int(x['contagens'][i]) != int(b['contagens'][i]): fora.append((nomes[i], 'contagem %d → %d' % (b['contagens'][i], x['contagens'][i]), np.inf)); continue
            if nomes[i].startswith('taxa_'):
                a = float(nomes[i][5:]); ok, r = EF.identidade(b['picos_%s' % a], x['picos_%s' % a], K[a])
                if not ok: fora.append((nomes[i], 'identidade dos K+1 perdida (razão %.2f; disparos %d → %d)' % (r, len(b['picos_%s' % a]), len(x['picos_%s' % a])), np.inf)); continue
            rr = abs(Fx[i] - F0[i]) / tol[i]
            if not np.isfinite(rr) or rr > 1: fora.append((nomes[i], 'ΔF/tol = %.2f' % rr, rr))
        ca = {n: (float(F0[i]), float(Fx[i])) for i, n in enumerate(nomes) if n.endswith('_Ca')}
        vd[g] = {'fora': [(n, m) for n, m, _ in fora], 'n_fora': len(fora), 'Ca (sem tolerância)': ca,
                 'pior_dentro': float(max([abs(Fx[i] - F0[i]) / tol[i] for i in range(len(nomes)) if np.isfinite(tol[i]) and nomes[i] not in [f[0] for f in fora]] or [0]))}
    dentro = vd['mais']['n_fora'] == 0 and vd['menos']['n_fora'] == 0
    res['direcoes']['v_%d' % (int(z['indices'][q]) + 1)] = dict(vd, veredito='DENTRO nos dois extremos' if dentro else 'FORA')
    print('v_%d (θ·exp(±δ·v), δ do arquivo de direções): %s' % (int(z['indices'][q]) + 1, 'DENTRO da tolerância nos dois extremos → não precisa ser determinada pelos dados' if dentro else 'FORA → a especificação FALHA nesta direção'))
    for g in ('mais', 'menos'):
        print('   %-5s componentes fora %2d %s | pior das de dentro ΔF/tol = %.2f' % (g, vd[g]['n_fora'], vd[g]['fora'][:6], vd[g]['pior_dentro']))
json.dump(res, open(OUT, 'w'), indent=1, default=str)
