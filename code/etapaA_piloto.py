# etapaA_piloto.py — D132 item 137: PILOTO — a diversidade de INJEÇÃO move o σ_lin? Dados gravados (sem simular aqui).
# Unidades: --distal "nome=dir θ[=dir das direções],…" (unidades distais do runner, --so-theta, 10⁻⁸) e --soma <dir θ da somática>.
#   --direcoes <saida_dir.npz> <saida_dirF.npz>: Gram COMBINADO (iid, representação com as 61 avaliações) de TODAS as unidades → direções relevantes
#       (etapaA_unit.direcoes_relevantes com o G a 10⁻⁸, 52 componentes) e excursões (δ = tol/|g·v|, piso h, teto fator 2); σ* (iid, sem viés) e o
#       raio em σ* ao longo de cada uma; as de raio ALÉM da faixa fisiológica (fator 2 no parâmetro mais carregado) → arquivo para o funcional ao
#       longo delas (δ = ln 2/max|v|, regra do item 132).
#   --analise <dir.npz> <saida.json> [--fdir F.json | --determinadas 1,2] --conjuntos "2=a,b;4=a,b,c,d;…": por unidade e modelo de ruído (iid, OU
#       1/10/50 ms) a Fisher (voltagem branqueada, tempos independentes) e, nas distais, a aceleração ao longo das direções; direções DETERMINADAS
#       pela faixa fisiológica (as DENTRO da tolerância nos dois extremos, do Fdir) conhecidas; σ* (combinado do conjunto) e σ_lin (parte DISTAL do
#       conjunto); a REGRA declarada no item 137. Item 163: --fdir aceita VÁRIOS arquivos "a.json,b.json" (rodadas do ponto fixo; uma direção
#       testada uma vez só).
#   --acumular … --por-protocolo (item 163 (3)): além do total, os acumulados de CADA protocolo (<pref>.<variante>.<M1m|M1p|M4>.npz), mesmas linhas,
#       máscaras e branqueamento do total (a máscara de uma linha usa TODAS as avaliações) → a soma dos protocolos confere com o total.
# Uso: python3 neuron/lancar.py distal -- .nrnvenv/bin/python neuron/etapaA_piloto.py <G.npz> --distal … --soma … (--direcoes … | --analise …)
import sys, os, math, json, glob, hashlib, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_model as EM
import etapaA_unit as EU
import etapaA_sstar as S

P = EM.THETA_NAMES; H = math.log(1.01); NP = 30; F = 1.4591; Z = 1.645; DT = EU.DT
TAUS = (0.0, 1.0, 10.0, 50.0); PHI = {t: (math.exp(-DT / t) if t > 0 else 0.0) for t in TAUS}
SUBS = ['base'] + ['%s_%s' % (n, g) for n in P for g in ('mais', 'menos')]
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
GF = os.path.abspath(sys.argv[1])
DIST = []
for it in (arg('--distal').split(',') if arg('--distal') else []):
    p = it.split('='); DIST.append((p[0], os.path.abspath(p[1]), os.path.abspath(p[2]) if len(p) > 2 and p[2] else None))
SOMA = os.path.abspath(arg('--soma'))
zg = np.load(GF, allow_pickle=True); nomes = [str(x) for x in zg['nomes']]; tl = [S.tol_of(x) for x in nomes]
use = [i for i, t in enumerate(tl) if t is not None and zg['condicionado'][i] and np.all(np.isfinite(zg['G'][i]))]
Gf = zg['G'][use]; tol = np.array([tl[i][1] * abs(zg['F0'][i]) if tl[i][0] == 'rel' else tl[i][1] for i in use])
if '--tol-CaBurst' in sys.argv:                                       # prompt 0007 (f): SENSIBILIDADE — só a tolerância do CaBurst_PA1 (ms), rotulada (como no etapaA_Fdir)
    tol[[nomes[i] for i in use].index('CaBurst_PA1')] = float(arg('--tol-CaBurst')); print('SENSIBILIDADE: tolerância do CaBurst_PA1 = %g ms' % float(arg('--tol-CaBurst')))


def labs(ud):
    return ('M3', 'M5') if os.path.basename(ud) == 'p_soma' else ('M1m', 'M1p', 'M4')


# item 144 (2): máscara FISIOLÓGICA (--vrest <npz do etapaA_vrest> --faixa lo,hi --dirtag <rótulo das direções>) e soma sozinho (--so-soma)
VR = None; FAIXA = None; DIRTAG = arg('--dirtag', ''); EXC = {}; GAPS = [0]
if '--vrest' in sys.argv:
    _z = np.load(arg('--vrest')); VR = {str(t): v for t, v in zip(_z['tags'], _z['V'])}; RD = [str(x) for x in _z['leituras']]; RIX = {n: i for i, n in enumerate(RD)}
    FAIXA = tuple(float(x) for x in arg('--faixa', '-1e9,1e9').split(','))   # item 154: sem --faixa = faixa infinita (o --acumular define as suas)


def segmentos(m):
    """Trechos contíguos [a, b) onde a máscara é verdadeira."""
    out = []; a = None
    for i, x in enumerate(m):
        if x and a is None: a = i
        if not x and a is not None: out.append((a, i)); a = None
    if a is not None: out.append((a, len(m)))
    return out


def branqueia_seg(X, m, phi):
    """Branqueamento AR(1) de cada trecho contíguo mantido como série própria (exato quando o mantido é um prefixo)."""
    sg = segmentos(m)
    if len(sg) > 1: GAPS[0] += 1
    return np.concatenate([EU.branqueia_ar1(X[a:b], phi) for a, b in sg]) if sg else X[:0]


def acumula(ud, dd=None, V=None, dl=None, taus=TAUS, nome=None, so_soma=False, so_lab=None, grades=None):
    """Fisher por τ (e, com direções, Jᵀa e aᵀa por direção) de UMA unidade. Com --vrest: linhas NÃO FISIOLÓGICAS fora (item 144).
    so_lab (item 163 (3)): só as linhas de UM protocolo. grades (prompt 0007 (b), densidade de leitura): {nome: conjunto de leituras} → também o Gram
    de cada grade na MESMA passada (linha incluída se a leitura dela está na grade; exige --vrest); devolve então (G, JA, AA, Gg)."""
    k = 0 if V is None else len(V); G = {t: np.zeros((NP, NP)) for t in taus}; JA = {t: np.zeros((k, NP)) for t in taus}; AA = {t: np.zeros(k) for t in taus}
    Gg = None if grades is None else {gn: {t: np.zeros((NP, NP)) for t in taus} for gn in grades}
    for d_, subs_ in ((ud, SUBS), (dd, ['dir%02d_%s' % (q, g) for q in range(k) for g in ('mais', 'menos')] if dd else [])):   # item 157: NÃO AVALIADO → pára COM o motivo
        for sn in subs_:
            f_ = os.path.join(d_, '%s.npz' % sn)
            if os.path.exists(f_) and 'nao_avaliado' in np.load(f_).files:
                raise RuntimeError('NÃO AVALIADO (item 157): %s/%s — %s; a unidade não é acumulada (nada apagado)' % (d_, sn, str(np.load(f_)['nao_avaliado'])))
    nome = nome or os.path.basename(ud)[2:]
    for lab in (labs(ud) if so_lab is None else (so_lab,)):
        shp = np.load(os.path.join(ud, 'base.%s.npy' % lab), mmap_mode='r').shape; R = int(np.prod(shp[:-1]))
        for c0 in range(0, R, 4):
            rr = list(range(c0, min(R, c0 + 4)))
            ld = lambda d, sn: EU.cadeia(np.load(os.path.join(d, '%s.%s.npy' % (sn, lab)), mmap_mode='r').reshape(R, -1)[rr], lab)
            ev = {sn: ld(ud, sn) for sn in SUBS}
            ex = {'dir%02d_%s' % (q, g): ld(dd, 'dir%02d_%s' % (q, g)) for q in range(k) for g in ('mais', 'menos')} if dd else {}
            f, fx, inf = EU.representar_extra(ev, ex)
            for j in range(len(rr)):
                r = rr[j]; leit = (nome if r % 2 == 0 else 'soma') if lab == 'M4' else ('soma' if lab == 'M5' else (RD[r] if VR is not None else None))
                if so_soma and lab == 'M3' and leit != 'soma': continue
                cut = inf['n_voltagem'][j]; y0 = f['base'][j]
                J = np.stack([(f[p + '_mais'][j] - f[p + '_menos'][j]) / (2 * H) for p in P], 1); Jt = J[cut:]
                A = np.stack([(fx['dir%02d_mais' % q][j] + fx['dir%02d_menos' % q][j] - 2 * y0) / dl[q] ** 2 for q in range(k)], 1) if dd else None
                mv = np.ones(cut, bool); mt = np.ones(len(Jt), bool)
                if VR is not None:                                  # item 144: voltagem ABSOLUTA = deflexão + repouso (leitura, θ) em TODAS as avaliações usadas
                    ix = RIX[leit]; ks = list(ev) + list(ex)
                    vr = {kk: VR[kk if kk in ev else '%s:%s' % (DIRTAG, kk)][ix] for kk in ks}
                    absv = np.stack([(f[kk][j] if kk in ev else fx[kk][j])[:cut] + vr[kk] for kk in ks])
                    mv = (absv.min(0) >= FAIXA[0]) & (absv.max(0) <= FAIXA[1])
                    if len(Jt):
                        for i in range(len(Jt)):                    # tempo do i-ésimo disparo: o PICO absoluto em todas as avaliações
                            pk = [(ev[kk][j] if kk in ev else ex[kk][j]) for kk in ks]
                            vals = [y[EU.disparos(y)[i]['i_pk']] + vr[kk] for y, kk in zip(pk, ks) if len(EU.disparos(y)) > i]
                            mt[i] = bool(vals) and min(vals) >= FAIXA[0] and max(vals) <= FAIXA[1]
                    e = EXC.setdefault((nome, lab), [0, 0, 0.0, 0.0]); m = np.concatenate([mv, mt]); jj = (J ** 2).sum(1)
                    e[0] += len(m); e[1] += int((~m).sum()); e[2] += float(jj.sum()); e[3] += float(jj[~m].sum())
                for t in taus:
                    W = branqueia_seg(J[:cut], mv, PHI[t]); Jm = Jt[mt]; G[t] += W.T @ W + Jm.T @ Jm
                    if Gg is not None:
                        for gn, gs in grades.items():
                            if leit in gs: Gg[gn][t] += W.T @ W + Jm.T @ Jm
                    if dd:
                        Wa = branqueia_seg(A[:cut], mv, PHI[t]); At = np.where(np.isfinite(A[cut:]), A[cut:], 0.0)[mt]
                        JA[t] += (W.T @ Wa + Jm.T @ At).T; AA[t] += (Wa ** 2).sum(0) + (At ** 2).sum(0)
    print('  %s: acumulado' % ud, flush=True)
    return (G, JA, AA) if Gg is None else (G, JA, AA, Gg)


def sigma_estrela(Gc, B=None, tl_=None):
    if B is None: B = np.eye(NP)
    Gq = B.T @ Gc @ B; gb = Gf @ B; sF = np.sqrt(np.einsum('gi,ij,gj->g', gb, np.linalg.inv(Gq), gb)); xs = (tol if tl_ is None else tl_) / (Z * sF)
    return float(xs.min()), nomes[use[int(np.argmin(xs))]]


# item 154 (1): ACUMULADOS POR UNIDADE — o MESMO `acumula`, gravado por unidade e variante de faixa; a análise pode partir SÓ deles (--acumulados).
sha = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()


def versao_codigo():
    r = os.path.dirname(os.path.abspath(__file__))
    try:
        c = subprocess.run(['git', '-C', r, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        d = subprocess.run(['git', '-C', r, 'status', '--porcelain', '--', '.'], capture_output=True, text=True).stdout.strip()
        return {'commit': c, 'modificado_no_harness': bool(d), 'sha256_etapaA_piloto': sha(os.path.abspath(__file__)), 'sha256_etapaA_unit': sha(EU.__file__)}
    except Exception as e: return {'erro': str(e)}


def grava_acumulados(path, res, exc, gaps, meta):
    """Grava (G, Jᵀa, aᵀa) por τ + exclusões da faixa; RELÊ e confere bit a bit com a memória. Devolve True se idêntico."""
    G, JA, AA = res; ks = list(exc)
    d = {'meta': np.array(json.dumps(meta)), 'gaps': np.array(gaps), 'exc_chaves': np.array(['%s|%s' % k for k in ks]),
         'exc_int': np.array([[exc[k][0], exc[k][1]] for k in ks], np.int64).reshape(-1, 2), 'exc_float': np.array([[exc[k][2], exc[k][3]] for k in ks], float).reshape(-1, 2)}
    for t in G: d['G_%g' % t] = G[t]; d['JA_%g' % t] = JA[t]; d['AA_%g' % t] = AA[t]
    tmp = path[:-4] + '.tmp%d.npz' % os.getpid(); np.savez(tmp, **d); os.replace(tmp, path)
    z = np.load(path)
    return all(z['%s_%g' % (n, t)].tobytes() == X[t].tobytes() for t in G for n, X in (('G', G), ('JA', JA), ('AA', AA)))


def carrega_acumulados(path):
    z = np.load(path); ts = sorted(float(k[2:]) for k in z.files if k.startswith('G_'))
    r = tuple({t: z['%s_%g' % (n, t)] for t in ts} for n in ('G', 'JA', 'AA'))
    exc = {tuple(c.split('|')): [int(i[0]), int(i[1]), float(f[0]), float(f[1])] for c, i, f in zip(z['exc_chaves'], z['exc_int'], z['exc_float'])}
    return r, exc, int(z['gaps']), json.loads(str(z['meta']))


if '--acumular' in sys.argv:                                          # item 154 (1): acumulados de UMA unidade (com e sem a faixa) → [apagar os traços das direções]
    i = sys.argv.index('--acumular'); NOME, FZ, PREF = sys.argv[i + 1], os.path.abspath(sys.argv[i + 2]), os.path.abspath(sys.argv[i + 3])
    z = np.load(FZ); V = z['V']; dl = z['excursoes']
    VARS = [(c.split('=')[0], tuple(float(x) for x in c.split('=')[1].split(','))) for c in arg('--faixas', 'fis=-110,60;inf=-1e9,1e9').split(';')]
    assert VR is not None, '--acumular exige --vrest (a faixa é aplicada aqui)'
    if NOME != 'soma': _, UD, DD = next(x for x in DIST if x[0] == NOME); assert DD, 'unidade distal sem rodada de direções'
    resumo = {'unidade': NOME, 'direcoes': FZ, 'sha256_direcoes': sha(FZ), 'vrest': os.path.abspath(arg('--vrest')), 'dirtag': DIRTAG, 'codigo': versao_codigo(), 'variantes': {}}
    ok = True
    for rot, fx in VARS:
        FAIXA = fx; EXC.clear(); GAPS[0] = 0
        try: res = acumula(SOMA, so_soma='--so-soma' in sys.argv) if NOME == 'soma' else acumula(UD, DD, V, dl, nome=NOME)
        except RuntimeError as e:                                         # item 158: avaliação NÃO AVALIADA → a unidade SAI do lote (registrada); nada apagado
            if not str(e).startswith('NÃO AVALIADO'): raise
            resumo.update(ok=True, excluida=True, motivo=str(e)); json.dump(resumo, open(PREF + '.ok.json', 'w'), indent=1)
            print('UNIDADE %s FORA DO LOTE: %s' % (NOME, e), flush=True); sys.exit(0)
        meta = dict(resumo, faixa=list(fx), variante=rot); del meta['variantes']
        o = grava_acumulados('%s.%s.npz' % (PREF, rot), res, dict(EXC), GAPS[0], meta); ok &= o
        resumo['variantes'][rot] = {'arquivo': '%s.%s.npz' % (PREF, rot), 'relido_identico': bool(o), 'sha256': sha('%s.%s.npz' % (PREF, rot)), 'faixa': list(fx)}
        print('acumulados %s (%s, faixa %s): gravados e relidos → %s' % (NOME, rot, fx, 'IDÊNTICOS bit a bit' if o else 'DIFERENTES — NADA será apagado'), flush=True)
        if '--por-protocolo' in sys.argv and NOME != 'soma':         # item 163 (3): por protocolo; a SOMA confere com o total (arredondamento)
            soma_p, pp = None, {}
            for lab in labs(UD):
                EXC.clear(); GAPS[0] = 0; rl = acumula(UD, DD, V, dl, nome=NOME, so_lab=lab); fl = '%s.%s.%s.npz' % (PREF, rot, lab)
                ol = grava_acumulados(fl, rl, dict(EXC), GAPS[0], dict(meta, protocolo=lab)); ok &= ol
                soma_p = rl if soma_p is None else tuple({t: soma_p[n][t] + rl[n][t] for t in rl[n]} for n in range(3))
                pp[lab] = {'arquivo': fl, 'relido_identico': bool(ol), 'sha256': sha(fl)}
            dif = max(float(np.abs(soma_p[n][t] - res[n][t]).max() / max(np.abs(res[n][t]).max(), 1e-300)) for n in range(3) for t in res[n])
            ok &= dif < 1e-9; resumo['variantes'][rot]['por_protocolo'] = dict(pp, soma_confere_com_total=dif < 1e-9, dif_relativa_max=dif)
            print('   por protocolo %s: soma dos protocolos × total: diferença relativa máx %.2e → %s' % (list(pp), dif, 'CONFERE' if dif < 1e-9 else 'NÃO CONFERE'), flush=True)
    if ok and '--apagar-direcoes' in sys.argv and NOME != 'soma':    # item 154 (1): SÓ depois dos acumulados conferidos; SÓ os .npy da rodada de direções
        assert os.path.basename(os.path.dirname(DD)).startswith('dirs_') and os.path.realpath(DD) != os.path.realpath(UD), ('recusado: não é rodada de direções', DD)
        fs = sorted(glob.glob(os.path.join(glob.escape(DD), '*.npy'))); tot = sum(os.path.getsize(f) for f in fs)
        with open(PREF + '.apagados.txt', 'w') as fh:
            fh.write('# D132 item 154 (1): traços da rodada de direções apagados DEPOIS dos acumulados gravados e conferidos bit a bit; %s\n' % DD)
            for f in fs: fh.write('%s\t%d\n' % (f, os.path.getsize(f)))
        for f in fs: os.remove(f)
        resumo['apagados'] = {'arquivos': len(fs), 'bytes': tot, 'manifesto': PREF + '.apagados.txt'}
        print('APAGADOS %d traços da rodada de direções de %s (%.2f GB); manifesto %s' % (len(fs), NOME, tot / 1e9, PREF + '.apagados.txt'), flush=True)
    resumo['ok'] = bool(ok); json.dump(resumo, open(PREF + '.ok.json' if ok else PREF + '.FALHOU.json', 'w'), indent=1)
    sys.exit(0 if ok else 1)
if '--direcoes' in sys.argv:
    out, outF = [os.path.abspath(a) for a in sys.argv[sys.argv.index('--direcoes') + 1:sys.argv.index('--direcoes') + 3]]
    Gc = np.zeros((NP, NP)); EXCL = []
    for nome_, d, _ in DIST:                                              # item 158: unidade com θ NÃO AVALIADO fica FORA do Gram (registrada)
        try: Gc = Gc + acumula(d, taus=(0.0,))[0][0.0]
        except RuntimeError as e:
            if not str(e).startswith('NÃO AVALIADO'): raise
            EXCL.append({'unidade': nome_, 'motivo': str(e)}); print('UNIDADE %s FORA DO GRAM: %s' % (nome_, e), flush=True)
    Gc = Gc + acumula(SOMA, taus=(0.0,))[0][0.0]
    w, V = np.linalg.eigh(Gc); s = np.sqrt(np.clip(w, 0, None))
    esc, fr = EU.direcoes_relevantes(s, V, Gf); dl = EU.excursoes(V, esc, Gf, tol)
    ss, lim = sigma_estrela(Gc); raio = ss * math.sqrt(NP * F) / s[esc]; mx = np.abs(V[:, esc]).max(0); alem = raio * mx > EU.TETO_LOG
    np.savez(out, V=V[:, esc].T, excursoes=dl, indices=esc, sigma=s[esc], raio=raio, rotulo=np.array('item 137: Gram combinado do piloto'), excluidas=np.array(json.dumps(EXCL)))
    q = np.where(alem)[0]
    np.savez(outF, V=V[:, esc[q]].T, excursoes=math.log(2) / mx[q], indices=esc[q], rotulo=np.array('item 137: direções de raio além do fator 2 — δ = ln 2/max|v|'))
    print('Gram combinado de %d unidades: %d direções relevantes; σ* (iid, sem viés) = %.3g mV (%s)%s' % (len(DIST) + 1 - len(EXCL), len(esc), ss, lim,
          '' if not EXCL else ' | FORA: %s' % [x['unidade'] for x in EXCL]))
    for i, e in enumerate(esc): print('  v_%-3d σ = %-9.3g δ = %-7.4f raio em σ* = %-7.3g %s' % (e + 1, s[e], dl[i], raio[i], 'ALÉM do fator 2 → funcional' if alem[i] else ''))
    print('direções além da faixa: %d → %s' % (int(alem.sum()), outF))
elif '--analise' in sys.argv:                                         # (prompt 0007: sem --analise, importável como módulo — ex. etapaA_densidade_cond)
    fz, OUT = [os.path.abspath(a) for a in sys.argv[sys.argv.index('--analise') + 1:sys.argv.index('--analise') + 3]]
    z = np.load(fz); V = z['V']; dl = z['excursoes']; k = len(dl); IDX = [int(i) + 1 for i in z['indices']]
    if '--fdir' in sys.argv:
        fd = {}
        for f_ in arg('--fdir').split(','):                           # item 163: rodadas do ponto fixo — cada direção testada UMA vez
            d_ = json.load(open(f_))['direcoes']; assert not set(d_) & set(fd), ('direção testada em dois Fdir', sorted(set(d_) & set(fd)), f_); fd.update(d_)
        DET = [int(n[2:]) for n, r in fd.items() if r['veredito'].startswith('DENTRO')]
    else:
        DET = [int(x) for x in arg('--determinadas', '').split(',') if x]
    qdet = [q for q in range(k) if IDX[q] in DET]; Pc = np.eye(NP) - sum((np.outer(V[q], V[q]) for q in qdet), np.zeros((NP, NP)))
    wP, UP = np.linalg.eigh(Pc); B = UP[:, wP > 0.5]
    if '--acumulados' in sys.argv:                                     # item 154 (1): a análise SÓ a partir dos acumulados gravados por unidade
        rot = arg('--variante'); AC = {}; EXC.clear(); GAPS[0] = 0; GS = None
        EXCL = []
        for it in arg('--acumulados').split(','):
            nm, pref = it.split('=')
            okj = os.path.abspath(pref) + '.ok.json'
            if os.path.exists(okj) and json.load(open(okj)).get('excluida'):   # item 158: unidade FORA do lote
                EXCL.append({'unidade': nm, 'motivo': json.load(open(okj)).get('motivo')}); print('UNIDADE %s FORA DO LOTE: %s' % (nm, EXCL[-1]['motivo']), flush=True); continue
            r, exc, gp, meta = carrega_acumulados('%s.%s.npz' % (os.path.abspath(pref), rot))
            assert meta['sha256_direcoes'] == sha(fz), ('acumulados de OUTRO arquivo de direções', nm)
            EXC.update(exc); GAPS[0] += gp; FAIXA = tuple(meta['faixa'])
            if nm == 'soma': GS = r[0]
            else: AC[nm] = r
        assert GS is not None, 'faltam os acumulados da somática'
    else:
        AC = {nome: acumula(ud, dd, V, dl, nome=nome) for nome, ud, dd in DIST} if DIST else {}; GS = acumula(SOMA, so_soma='--so-soma' in sys.argv)[0]
    if '--grams' in sys.argv:                                          # item 148 (2): Grams iid por unidade (piso numérico, sem simular)
        np.savez(os.path.abspath(arg('--grams')), nomes=np.array(list(AC)), GS=GS[0.0], **{'G_%d' % i: AC[n][0][0.0] for i, n in enumerate(AC)})
    if VR is not None or '--acumulados' in sys.argv:
        print('LINHAS NÃO FISIOLÓGICAS (faixa %s mV; voltagem absoluta = deflexão + repouso; θ e todas as perturbações usadas):' % (FAIXA,))
        for (nm, lb), e in sorted(EXC.items()): print('  %-16s %-4s linhas %8d, fora %7d (%.3f%%) | traço do Gram (iid) fora %.3f%%' % (nm, lb, e[0], e[1], 100 * e[1] / max(e[0], 1), 100 * e[3] / max(e[2], 1e-300)))
        print('  traços com trechos mantidos NÃO contíguos (branqueamento por trecho): %d' % GAPS[0])
        res_exc = {'%s|%s' % k: v for k, v in EXC.items()}
    CONJ = [(c.split('=')[0], [m for m in c.split('=')[1].split(',') if m]) for c in arg('--conjuntos').split(';')]
    res = {'determinadas': DET, 'conjuntos': {}}
    if '--acumulados' in sys.argv:                                        # item 158: os conjuntos SEM as unidades fora (registradas)
        CONJ = [(cn, [m for m in mb if m in AC]) for cn, mb in CONJ]; res['excluidas'] = EXCL
    print('direções: %d; DETERMINADAS pela faixa fisiológica (conhecidas): %s' % (k, ['v_%d' % d for d in DET]))
    for cn, membros in CONJ:
        res['conjuntos'][cn] = {}
        for t in TAUS:
            Gd = sum((AC[m][0][t] for m in membros), np.zeros((NP, NP))); JA = sum((AC[m][1][t] for m in membros), np.zeros((k, NP))); AA = sum((AC[m][2][t] for m in membros), np.zeros(k))
            ss, lim = sigma_estrela(Gd + GS[t], B)
            sl = min((EU.sigma_lin(EU.curvaturas(Gd, JA[q], AA[q], float(V[q] @ Gd @ V[q]))[0], NP, F), IDX[q]) for q in range(k) if q not in qdet) if membros else (None, None)
            res['conjuntos'][cn][str(t)] = {'sigma_estrela': ss, 'limitante': lim, 'sigma_lin': sl[0], 'v_lin': sl[1]}
            print('%-14s %-9s σ* %-8.3g (%s) | σ_lin (distal) %-8s (v_%s) | %s' % (cn, 'iid' if t == 0 else 'OU %g ms' % t, ss, lim, '—' if sl[0] is None else '%.3g' % sl[0], sl[1],
                  'σ_lin NÃO AVALIADO (sem direções)' if sl[0] is None else ('CERTIFICADA' if ss <= sl[0] else 'intervalo [%.3g; %.3g]' % (sl[0], ss))))
    if VR is not None or '--acumulados' in sys.argv: res['exclusao'] = res_exc
    c0, cN = CONJ[0][0], CONJ[-1][0]
    if res['conjuntos'][c0]['0.0']['sigma_lin'] is None or c0 == cN:
        json.dump(res, open(OUT, 'w'), indent=1); sys.exit(0)
    raz = {t: res['conjuntos'][cN][str(t)]['sigma_lin'] / res['conjuntos'][c0][str(t)]['sigma_lin'] for t in TAUS}
    alav = raz[10.0] >= 1.5 and raz[50.0] >= 1.5
    res['razao_sigma_lin'] = {str(t): r for t, r in raz.items()}; res['regra_item137'] = 'ALAVANCA' if alav else 'GARGALO FÍSICO'
    print('σ_lin(%s) / σ_lin(%s): %s' % (cN, c0, '  '.join('%s %.2f' % ('iid' if t == 0 else '%g ms' % t, r) for t, r in raz.items())))
    print('REGRA (item 137, ruído lento τ = 10 E 50 ms, limiar 1.5×): %s' % ('a diversidade de injeção é uma ALAVANCA → a Etapa A completa em s = 400 se justifica' if alav
          else 'o gargalo é a FÍSICA das direções fracas → Etapa A completa SUSPENSA; próximo passo: repetição / análise não linear'))
    if '--sens' in sys.argv:                                          # item 139: SENSIBILIDADE à tolerância do CaBurst_PA1 (rótulo), no ÚLTIMO conjunto
        iC = [nomes[i] for i in use].index('CaBurst_PA1'); res['sensibilidade_CaBurst'] = {}
        mx = np.abs(V).max(1); membros = CONJ[-1][1]
        G0 = sum((AC[m][0][0.0] for m in membros), np.zeros((NP, NP))) + GS[0.0]
        print('\n=== ANÁLISE DE SENSIBILIDADE (item 139) — tolerância do CaBurst_PA1; %s; 1.0 ms = DECLARADA (D131 7.4), 0.2 ms = nível B do V2 ===' % cN)
        for it in arg('--sens').split(','):
            tv, fj = it.split('='); tv = float(tv); tl_ = tol.copy(); tl_[iC] = tv
            s0, _ = sigma_estrela(G0, None, tl_); raio = s0 * math.sqrt(NP * F) / z['sigma']; alem = [IDX[q] for q in range(k) if raio[q] * mx[q] > EU.TETO_LOG]
            fdj = json.load(open(fj))['direcoes']; dentro = [int(n[2:]) for n, r in fdj.items() if r['veredito'].startswith('DENTRO')]
            det = [d for d in alem if d in dentro]; qd = [q for q in range(k) if IDX[q] in det]
            Pq = np.eye(NP) - sum((np.outer(V[q], V[q]) for q in qd), np.zeros((NP, NP))); wq, Uq = np.linalg.eigh(Pq); Bq = Uq[:, wq > 0.5]
            res['sensibilidade_CaBurst'][str(tv)] = {'alem_da_faixa': alem, 'determinadas': det, 'tau': {}}
            print('tol CaBurst_PA1 = %g ms: σ*(iid, sem regra) %.3g → além da faixa %s; DENTRO no funcional %s → DETERMINADAS %s' % (tv, s0, alem, dentro, det))
            for t in TAUS:
                Gd = sum((AC[m][0][t] for m in membros), np.zeros((NP, NP))); JA = sum((AC[m][1][t] for m in membros), np.zeros((k, NP))); AA = sum((AC[m][2][t] for m in membros), np.zeros(k))
                ss, lim = sigma_estrela(Gd + GS[t], Bq, tl_)
                sl = min((EU.sigma_lin(EU.curvaturas(Gd, JA[q], AA[q], float(V[q] @ Gd @ V[q]))[0], NP, F), IDX[q]) for q in range(k) if q not in qd)
                nivel = 'CERTIFICADA em %.3g' % ss if ss <= sl[0] else 'intervalo [%.3g; %.3g]' % (sl[0], ss)
                res['sensibilidade_CaBurst'][str(tv)]['tau'][str(t)] = {'sigma_estrela': ss, 'limitante': lim, 'sigma_lin': sl[0], 'v_lin': sl[1], 'nivel': nivel}
                print('   %-9s σ* %-8.3g limitante %-16s σ_lin %-8.3g (v_%d) → %s' % ('iid' if t == 0 else 'OU %g ms' % t, ss, lim, sl[0], sl[1], nivel))
    json.dump(res, open(OUT, 'w'), indent=1)
