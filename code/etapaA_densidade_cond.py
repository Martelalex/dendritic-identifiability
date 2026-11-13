# etapaA_densidade_cond.py — prompt 0007 (3b): DENSIDADE DE LEITURA nos desenhos CONDICIONADOS (piloto-6, lote 1, lote 2) — a análise do item 136 (3),
# sem simular, a partir dos traços θ gravados (504 leituras: grade de 25 µm + soma). Grades: 400 / 200 / 100 / 50 µm e todas (leituras da grade de 25 µm a
# distância múltipla de s, + o soma; o M4 no ponto de injeção conta — os pontos de injeção estão na grade de 400 µm). Gram de cada grade na MESMA passada
# (etapaA_piloto.acumula com `grades`). σ* por grade e modelo de ruído, com as direções resolvidas do PONTO FIXO de cada desenho. σ_lin por grade: NÃO
# AVALIÁVEL (os traços das rodadas de direções foram apagados por unidade, item 154) — reportado com o custo de refazer.
# CONFERÊNCIAS (resposta conhecida): (1) cobertura por região reproduz as contagens do item 136 (400: 1/7/12/0; 200: 3/18/21/9; 100: 6/33/37/43;
# todas: 25/132/143/203 — tronco/oblíquo/tufo/basal); (2) o Gram de 'todas' reproduz o acumulado OFICIAL (fis) de cada unidade; (3) o σ* de 'todas'
# reproduz o PONTO_FIXO.json de cada desenho.
# Uso: python3 neuron/lancar.py distal -- .nrnvenv/bin/python neuron/etapaA_densidade_cond.py <saida.json>
import sys, os, json, math, time
import numpy as np
AQ = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQ, 'results'); L = os.path.join(RES, 'etapaA_lotes'); OUT = os.path.abspath(sys.argv[1])
CACHE = os.path.join(L, 'prompt0007', 'densidade'); os.makedirs(CACHE, exist_ok=True)
SOMA = os.path.join(RES, 'etapaA_conf', 'soma64_1e-8', 'p_soma')
sys.argv = [sys.argv[0], os.path.join(RES, 'etapaA_G8', 'G.npz'), '--soma', SOMA, '--vrest', os.path.join(L, 'lote2', 'vrest.npz')]
sys.path.insert(0, AQ)
import etapaA_piloto as EP
import etapaA_model as EM
from neuron import h

HAY = os.path.join(os.path.dirname(AQ), '.cache', 'hay', '139653-master')
EM.load(HAY); cell = h.L5PCtemplate(os.path.join(HAY, 'morphologies', 'cell1.asc'))
G25 = EM.grid_points(cell, 25.0)


def regioes():
    """Região de cada seção pela definição declarada no item 135 (cópia literal de etapaA_leituras.regioes — conferida pelas contagens do item 136)."""
    secs = {s.name(): s for s in cell.all}; filhos = {n: [c.name() for c in h.SectionRef(sec=s).child] for n, s in secs.items()}
    sub = {}
    def Lr(n):
        if n not in sub: sub[n] = secs[n].L + sum(Lr(c) for c in filhos[n])
        return sub[n]
    reg = {n: ('basal' if '.dend' in n or n.startswith('dend') else None) for n in secs}
    apic0 = next(n for n in secs if n.endswith('apic[0]')); n = apic0; tronco = []
    while True:
        tronco.append(n); fs = sorted([c for c in filhos[n] if 'apic' in c], key=Lr, reverse=True)
        if not fs: break
        if len(fs) > 1 and Lr(fs[1]) >= 0.3 * Lr(fs[0]): break
        n = fs[0]
    def marca(n, r):
        reg[n] = r
        for c in filhos[n]: marca(c, r)
    for n in tronco: reg[n] = 'tronco'
    for n in tronco:
        for c in filhos[n]:
            if c in tronco or 'apic' not in c: continue
            marca(c, 'tufo' if n == tronco[-1] else 'obliquo')
    return reg


REG = regioes(); RD = EP.RD
regiao = lambda r: 'soma' if r == 'soma' else REG[G25[r]['sec']]
GR = {}
for s in (400, 200, 100, 50):
    GR['%d' % s] = set(r for r in RD if r == 'soma' or G25[r]['dist'] % s == 0.0)
GR['todas'] = set(RD)
cob = {g: {} for g in GR}
for g, st in GR.items():
    for r in st: cob[g][regiao(r)] = cob[g].get(regiao(r), 0) + 1
esperado = {'400': (1, 7, 12, 0), '200': (3, 18, 21, 9), '100': (6, 33, 37, 43), 'todas': (25, 132, 143, 203)}
ok1 = all(tuple(cob[g].get(r, 0) for r in ('tronco', 'obliquo', 'tufo', 'basal')) == e for g, e in esperado.items())
print('CONFERÊNCIA (1) cobertura = item 136: %s | %s' % ('EXATA' if ok1 else 'DIFERENTE', {g: (len(GR[g]), cob[g]) for g in GR}), flush=True)
assert ok1

J = json.load(open(os.path.join(RES, 'supervisor', 'TRABALHOS.json')))
a = next(j for j in J if j['nome'] == 'lt2_an_fis')['argv']; M2 = a[a.index('--conjuntos') + 1].split('=')[1].split(',')
PC = M2[:5]; NOV = M2[5:10]; L2 = M2[10:]
UD = {p: os.path.join(RES, 'etapaA_pcond', 'unid_%s' % p, 'p_%s' % p) for p in PC}
UD.update({p: os.path.join(L, 'lote1', 'unid_%s' % p, 'p_%s' % p) for p in NOV}); UD.update({p: os.path.join(L, 'lote2', 'unid_%s' % p, 'p_%s' % p) for p in L2})
UD['soma'] = SOMA
DES = {'piloto-6': (os.path.join(RES, 'etapaA_pcond'), os.path.join(L, 'regr154'), PC, '6inj'),
       'lote 1': (os.path.join(L, 'lote1'), os.path.join(L, 'lote1'), PC + NOV, 'acum'),
       'lote 2': (os.path.join(L, 'lote2'), os.path.join(L, 'lote2'), M2, 'acum')}

Gg = {}
for u, ud in UD.items():
    cf = os.path.join(CACHE, 'G_%s.npz' % u)
    if os.path.exists(cf):
        zc = np.load(cf); Gg[u] = {g: {t: zc['%s_%g' % (g, t)] for t in EP.TAUS} for g in GR}; continue
    t0 = time.time(); r = EP.acumula(ud, taus=EP.TAUS, so_soma=False, grades=GR) if u == 'soma' else EP.acumula(ud, taus=EP.TAUS, nome=u, grades=GR)
    Gg[u] = r[3]; np.savez(cf, **{'%s_%g' % (g, t): Gg[u][g][t] for g in GR for t in EP.TAUS})
    print('unidade %-16s acumulada por grade (%.0f s)' % (u, time.time() - t0), flush=True)

res = {'cobertura': cob, 'conferencias': {}, 'desenhos': {}}
for nome, (d, accdir, mem, cj) in DES.items():
    # (2) Gram 'todas' × acumulado oficial (fis), por unidade
    dif = max(float(np.abs(Gg[u]['todas'][t] - np.load(os.path.join(accdir, 'acc_%s.fis.npz' % u))['G_%g' % t]).max() /
                    np.abs(np.load(os.path.join(accdir, 'acc_%s.fis.npz' % u))['G_%g' % t]).max()) for u in mem + ['soma'] for t in EP.TAUS)
    z = np.load(os.path.join(d, 'direcoes.npz')); V = z['V']; IDX = [int(i) + 1 for i in z['indices']]
    PF = json.load(open(os.path.join(d, 'pf', 'PONTO_FIXO.json'))); DET = PF['determinadas']; qdet = [q for q in range(len(IDX)) if IDX[q] in DET]
    Pc = np.eye(EP.NP) - sum((np.outer(V[q], V[q]) for q in qdet), np.zeros((EP.NP, EP.NP))); wP, UP = np.linalg.eigh(Pc); B = UP[:, wP > 0.5]
    R = res['desenhos'][nome] = {'membros': len(mem), 'DET': DET, 'dif_rel_Gram_todas_vs_oficial': dif, 'grades': {}}
    ok3 = True
    for g in ('400', '200', '100', '50', 'todas'):
        R['grades'][g] = {}
        for t in EP.TAUS:
            Gd = sum((Gg[u][g][t] for u in mem), np.zeros((EP.NP, EP.NP))); ss, lim = EP.sigma_estrela(Gd + Gg['soma'][g][t], B)
            R['grades'][g][str(t)] = {'sigma_estrela': ss, 'limitante': lim}
            if g == 'todas': ok3 &= abs(ss / PF['conjuntos'][cj][str(t)]['sigma_estrela'] - 1) < 1e-9
    R['conferencia_todas_igual_PONTO_FIXO'] = bool(ok3)
    print('\n%s (%d distais + soma; resolvidas %s) | conferência (2) Gram todas × oficial: dif. rel. máx %.1e | (3) σ* todas = PONTO_FIXO: %s' % (
          nome, len(mem), DET, dif, 'EXATO' if ok3 else 'DIFERENTE'), flush=True)
    for g in ('400', '200', '100', '50', 'todas'):
        x = R['grades'][g]; print('   grade %-6s (%3d leituras; tronco/oblíquo/tufo/basal %s) σ* %s' % (g, len(GR[g]), tuple(cob[g].get(r, 0) for r in ('tronco', 'obliquo', 'tufo', 'basal')),
              ' / '.join('%.4g' % x[str(t)]['sigma_estrela'] for t in EP.TAUS)))
res['sigma_lin_por_grade'] = ('NÃO AVALIÁVEL: os traços das rodadas de direções foram apagados por unidade (item 154); refazer = rodadas de direções de 15 unidades '
                              '(lote 2: 25 direções × 2 subpassos + base ≈ 51 subpassos × ~450 s ≈ 6.4 h de CPU por unidade → ~96 h no lote 2)')
json.dump(res, open(OUT, 'w'), indent=1, default=float)
