# etapaA_sens_caburst_cond.py — prompt 0007 (3f): SENSIBILIDADE à tolerância do CaBurst_PA1 (0.2 / 0.5 / 1.0 ms) nos desenhos CONDICIONADOS (piloto-6,
# lote 1, lote 2), a partir dos dados GRAVADOS (sem simular): o funcional ao longo das direções testadas re-julgado na tolerância (etapaA_Fdir --tol-CaBurst,
# rodada original + rodada 1 do ponto fixo), a análise OFICIAL de cada desenho (o argv da fila: rg154_an_fis / lt1_an_fis / lt2_an_fis) com esses Fdir e
# --tol-CaBurst, e a checagem do ponto fixo (etapaA_ponto_fixo.candidatas): direção NÃO testada com raio além do fator 2 no σ* resultante → o ponto fixo
# NÃO fecha com os dados gravados; como resolver direções só faz σ* e σ_lin subirem (monótono, item 163), o nível é então um LIMITE INFERIOR (≥).
# CONFERÊNCIA (resposta conhecida): 1.0 ms é a tolerância declarada (D131 7.4) → a linha de 1.0 ms reproduz o PONTO_FIXO.json de cada desenho
# (resolvidas, σ*, σ_lin) EXATAMENTE.
# Uso: python3 neuron/etapaA_sens_caburst_cond.py   (cada análise vai pelo neuron/lancar.py distal --esperar, o tipo do job oficial)
import sys, os, json, subprocess
import numpy as np
AQ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQ)
import etapaA_ponto_fixo as PFX

RES = os.path.join(AQ, 'results'); L = os.path.join(RES, 'etapaA_lotes'); O = os.path.join(L, 'prompt0007', 'sens_caburst'); RAIZ = os.path.dirname(AQ)
TAUS = ['0.0', '1.0', '10.0', '50.0']; TVS = ('0.2', '0.5', '1.0')
DES = {'pilot-6 (soma + 5)': ('rg154_an_fis', 'pcond', os.path.join(RES, 'etapaA_pcond'), '6inj'),
       'batch 1 (soma + 10)': ('lt1_an_fis', 'lote1', os.path.join(L, 'lote1'), 'acum'),
       'batch 2 (soma + 15)': ('lt2_an_fis', 'lote2', os.path.join(L, 'lote2'), 'acum')}
J = json.load(open(os.path.join(RES, 'supervisor', 'TRABALHOS.json')))
out = {'_meta': {'regra': 'análise oficial com Fdir re-julgados na tolerância + checagem de candidatas do ponto fixo; fecha=False → nível ≥ (limite inferior)',
                 'tolerancia_declarada_ms': 1.0}, '_conferencia': {}}
for nome, (job, tag, d, cj) in DES.items():
    a = list(next(j for j in J if j['nome'] == job)['argv']); PF = json.load(open(os.path.join(d, 'pf', 'PONTO_FIXO.json')))
    out[nome] = {}
    for tv in TVS:
        fds = '%s/Fdir_%s_orig_%s.json,%s/Fdir_%s_pf_%s.json' % (O, tag, tv, O, tag, tv); an = os.path.join(O, 'analise_%s_%s.json' % (tag, tv))
        b = list(a); b[b.index('--fdir') + 1] = fds; b[b.index('--analise') + 2] = an; b += ['--tol-CaBurst', tv]
        r = subprocess.run(['python3', os.path.join(AQ, 'lancar.py'), 'distal', '--esperar', '--'] + b, cwd=RAIZ, capture_output=True, text=True)
        open(an[:-5] + '.log', 'w').write(r.stdout + r.stderr); assert r.returncode == 0, (nome, tv, r.stderr[-2000:])
        A = json.load(open(an)); fd = PFX.fdirs(fds); TEST = sorted(int(n[2:]) for n in fd)
        s_iid = A['conjuntos'][cj]['0.0']['sigma_estrela']; cand, raios = PFX.candidatas(np.load(os.path.join(d, 'direcoes.npz')), s_iid, TEST)
        out[nome][tv] = {t: dict(v, certificado=min(v['sigma_estrela'], v['sigma_lin']), fecha=not cand) for t, v in A['conjuntos'][cj].items()}
        out[nome][tv]['_ponto_fixo'] = {'testadas': TEST, 'resolvidas': sorted(A['determinadas']), 'candidatas_nao_testadas': cand, 'fecha': not cand}
        print('%-20s tol %s ms: resolvidas %s; candidatas não testadas %s → %s | certificado %s' % (nome, tv, sorted(A['determinadas']), cand or 'nenhuma',
              'FECHA' if not cand else 'NÃO FECHA (nível ≥)', ' / '.join('%.4g' % out[nome][tv][t]['certificado'] for t in TAUS)), flush=True)
    c1 = out[nome]['1.0']; P = PF['conjuntos'][cj]
    ok = sorted(PF['determinadas']) == c1['_ponto_fixo']['resolvidas'] and c1['_ponto_fixo']['fecha'] and all(
         c1[t]['sigma_estrela'] == P[t]['sigma_estrela'] and c1[t]['sigma_lin'] == P[t]['sigma_lin'] for t in TAUS)
    out['_conferencia'][nome] = 'EXATA' if ok else 'DIFERENTE'
    print('CONFERÊNCIA %s: linha de 1.0 ms = PONTO_FIXO.json → %s' % (nome, out['_conferencia'][nome]), flush=True)
json.dump(out, open(os.path.join(O, 'sens_caburst.json'), 'w'), indent=1)
assert all(v == 'EXATA' for v in out['_conferencia'].values()), out['_conferencia']
