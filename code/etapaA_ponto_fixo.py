# etapaA_ponto_fixo.py — D132 item 163 (2): PASSO r DA ITERAÇÃO DO PONTO FIXO do conjunto de direções resolvidas pela faixa (regra do item 132) num
# desenho. O raio de cada direção relevante usa o σ* (iid) RESULTANTE — o da análise da rodada anterior, com as resolvidas de TODAS as rodadas fora:
#   raio_i = σ*·√(NP·F)/s_i; CANDIDATA = NÃO testada no funcional (em nenhum Fdir) com raio_i·max|v_i| > ln 2.
# Sem candidatas → PONTO FIXO: <pf>/PONTO_FIXO.json = a análise da rodada anterior (os campos que o etapaA_lote_aval lê) + o registro da iteração e o
# nível certificado min(σ*, σ_lin). Com candidatas → <pf>/dirF_<r>.npz (δ = ln 2/max|v|, como no --direcoes) e a avaliação do funcional em θ_verd (base)
# da rodada ORIGINAL do desenho copiada para <pf>/Gdir_<r>/G/ (reaproveitada; a impressão digital do runner decide se vale).
# Guardas: custo acumulado acima do teto (avaliações do funcional) → ESPERA_DECISAO_CUSTO.json, nada lançado; r > r_max com candidatas →
# PONTO_FIXO_NAO_ALCANCADO.json. Os dois notificam e PARAM a cadeia do desenho (a avaliação da parada espera o PONTO_FIXO.json).
# Monótono: tirar uma direção do Gram (resolvida) é condicionar → a variância de todo funcional linear só cai → σ* só sobe → candidatas só aparecem;
# cada direção é testada uma vez → termina em no máximo (nº de direções relevantes) rodadas.
# Uso: python3 neuron/lancar.py toy -- .nrnvenv/bin/python neuron/etapaA_ponto_fixo.py <direcoes.npz> <análise anterior.json> <conjunto> <fdirs a,b,…>
#      <r> <r_max> <teto de avaliações> <Gdir original (contém G/base.npz)> <pf>
import sys, os, json, math, shutil, subprocess
import numpy as np

NP = 30; F = 1.4591; TETO_LOG = math.log(2.0); H_AVAL = 1.67                   # h de CPU por avaliação do funcional (MEDIDO: Gdir dos lotes, item 163)


def candidatas(z, sigma_iid, testadas):
    """Direções NÃO testadas com raio em σ* além do fator 2 (índices 1-based) e os raios·max|v| de todas."""
    mx = np.abs(z['V']).max(1); r = sigma_iid * math.sqrt(NP * F) / z['sigma'] * mx; idx = [int(i) + 1 for i in z['indices']]
    return [d for d, x in zip(idx, r) if x > TETO_LOG and d not in testadas], {'v_%d' % d: float(x) for d, x in zip(idx, r)}


def fdirs(lista):
    fd = {}
    for f in [x for x in lista.split(',') if x]:
        d = json.load(open(f))['direcoes']; assert not set(d) & set(fd), ('direção testada em dois Fdir', f); fd.update(d)
    return fd


def avalia_custo(lista):
    """Avaliações do funcional já feitas nas rodadas do ponto fixo (não conta a rodada original do desenho, a 1ª da lista)."""
    return sum(2 * len(json.load(open(f))['direcoes']) for f in [x for x in lista.split(',') if x][1:])


def notifica(t, m, critico=True):
    try: subprocess.run(['notify-send'] + (['-u', 'critical'] if critico else []) + [t, m], timeout=10)
    except Exception: pass


def passo(FZ, AN, CJ, FD, r, rmax, teto, GD0, PF):
    os.makedirs(PF, exist_ok=True); z = np.load(FZ); A = json.load(open(AN)); fd = fdirs(FD)
    TEST = sorted(int(n[2:]) for n in fd); DET = sorted(int(n[2:]) for n, x in fd.items() if x['veredito'].startswith('DENTRO'))
    assert sorted(A['determinadas']) == DET, ('a análise anterior não usou os Fdir dados', A['determinadas'], DET)
    s_iid = A['conjuntos'][CJ]['0.0']['sigma_estrela']; cand, raios = candidatas(z, s_iid, TEST)
    reg = {'rodada': r, 'analise_anterior': os.path.abspath(AN), 'conjunto': CJ, 'fdirs': FD.split(','), 'testadas': TEST, 'resolvidas': DET,
           'sigma_estrela_iid': s_iid, 'raio_vezes_max_v': raios, 'candidatas': cand, 'aval_feitas': avalia_custo(FD)}
    nome = lambda d: 'v_%d' % d
    print('rodada %d (%s): σ* iid resultante %.4g mV; testadas %s; resolvidas %s → candidatas NÃO testadas além do fator 2: %s' % (
          r, CJ, s_iid, [nome(d) for d in TEST], [nome(d) for d in DET], [nome(d) for d in cand] or 'nenhuma'), flush=True)
    if not cand:
        cert = {c: {t: dict(v, certificado=min(v['sigma_estrela'], v['sigma_lin']) if v['sigma_lin'] is not None else None) for t, v in cs.items()} for c, cs in A['conjuntos'].items()}
        out = dict(A, conjuntos=cert, ponto_fixo=dict(reg, alcancado_na_rodada=r))
        for t, v in cert[CJ].items():
            print('   PONTO FIXO %-9s σ* %-8.4g σ_lin %-8.4g certificado %.4g' % ('iid' if t == '0.0' else 'OU %g ms' % float(t), v['sigma_estrela'], v['sigma_lin'], v['certificado']))
        json.dump(out, open(os.path.join(PF, 'PONTO_FIXO.json'), 'w'), indent=1); json.dump(reg, open(os.path.join(PF, 'passo_%d.json' % r), 'w'), indent=1)
        print('PONTO FIXO alcançado (nenhuma direção não testada passa do fator 2 no σ* resultante)'); return 'PONTO_FIXO'
    if r > rmax:
        json.dump(reg, open(os.path.join(PF, 'PONTO_FIXO_NAO_ALCANCADO.json'), 'w'), indent=1); json.dump(reg, open(os.path.join(PF, 'passo_%d.json' % r), 'w'), indent=1)
        notifica('HANU — ponto fixo NÃO alcançado', '%s: %d rodadas e ainda há candidatas %s' % (PF, rmax, cand)); print('NÃO ALCANÇADO em %d rodadas — a cadeia PARA e reporta' % rmax)
        return 'NAO_ALCANCADO'
    novo = 2 * len(cand)
    if reg['aval_feitas'] + novo > teto:
        reg['custo_h'] = (reg['aval_feitas'] + novo) * H_AVAL
        json.dump(reg, open(os.path.join(PF, 'ESPERA_DECISAO_CUSTO.json'), 'w'), indent=1); json.dump(reg, open(os.path.join(PF, 'passo_%d.json' % r), 'w'), indent=1)
        notifica('HANU — ponto fixo: custo acima do teto', '%s: %d avaliações (~%.0f h de CPU) > teto %d — esperar a decisão' % (PF, reg['aval_feitas'] + novo, reg['custo_h'], teto))
        print('CUSTO acima do teto (%d + %d > %d avaliações) — NADA lançado; ESPERA a decisão' % (reg['aval_feitas'], novo, teto)); return 'ESPERA_DECISAO_CUSTO'
    idx = [int(i) + 1 for i in z['indices']]; q = [idx.index(d) for d in cand]; V = z['V'][q]; mx = np.abs(V).max(1)
    fz = os.path.join(PF, 'dirF_%d.npz' % r); tmp = fz[:-4] + '.tmp.npz'
    G = os.path.join(PF, 'Gdir_%d' % r, 'G'); os.makedirs(G, exist_ok=True)
    b = np.load(os.path.join(GD0, 'base.npz'), allow_pickle=True); assert 'nao_avaliado' not in b.files, 'base original NÃO AVALIADA'
    for f in ('base.npz', 'IMPRESSAO'): shutil.copy2(os.path.join(GD0, f), os.path.join(G, f))
    np.savez(tmp, V=V, excursoes=TETO_LOG / mx, indices=np.array([d - 1 for d in cand]),
             rotulo=np.array('item 163: ponto fixo, rodada %d — direções NÃO testadas de raio além do fator 2 no σ* resultante; δ = ln 2/max|v|' % r)); os.replace(tmp, fz)
    reg['dirF'] = fz; reg['excursoes'] = [float(x) for x in TETO_LOG / mx]; reg['custo_rodada_h'] = novo * H_AVAL
    json.dump(reg, open(os.path.join(PF, 'passo_%d.json' % r), 'w'), indent=1)
    print('→ funcional ao longo de %s (δ = %s; %d avaliações, ~%.1f h de CPU; base reaproveitada de %s)' % ([nome(d) for d in cand], ['%.3f' % x for x in TETO_LOG / mx], novo, novo * H_AVAL, GD0))
    return 'CANDIDATAS'


if __name__ == '__main__':
    a = sys.argv[1:]
    passo(os.path.abspath(a[0]), a[1], a[2], a[3], int(a[4]), int(a[5]), int(a[6]), os.path.abspath(a[7]), os.path.abspath(a[8]))
