# etapaA_runner.py — D132 itens 63(3)/64: EXECUÇÃO LONGA DA ETAPA A — gravação a cada unidade, retomada, distribuição.
# Desenho (item 64): a unidade independente é o PONTO DE INJEÇÃO p (não a avaliação θ): dentro dela rodam TODAS as
# perturbações (θ do Jacobiano, ganho/posição, geometria) e o que se grava é a REDUÇÃO por ponto de leitura r —
# blocos Gram JᵀJ (e JᵀD) por (p, r) — porque os traços completos (M2: todos os pontos durante cada M1) não cabem em
# disco a s = 25 µm (~6×10⁹ amostras por avaliação). Espaçamentos = subconjuntos de blocos; ruído = analítico.
# GRAVAÇÃO: cada SUBPASSO (uma avaliação θ dentro da unidade) vai para <dir>/<unidade>/<subpasso>.npz por escrita
# ATÔMICA (arquivo temporário + rename); a unidade, quando completa, para <dir>/<unidade>.npz (atômica). Na retomada:
# unidade pronta → pulada; subpassos prontos → lidos, não recalculados. Uma interrupção custa no máximo UM subpasso.
# DISTRIBUIÇÃO: --worker k/K pega as unidades de índice ≡ k (mod K) — 2 processos locais ou K núcleos fora.
# D132 item 81: --sub-worker k/K reparte os SUBPASSOS de cada unidade (índice ≡ k mod K): cada subpasso parte do mesmo
# repouso (calculado dentro da avaliação, sem estado herdado do subpasso anterior) e grava seu próprio arquivo — o objeto
# medido não muda. A redução da unidade é gravada por quem encontrar TODOS os subpassos prontos. --subpassos a,b restringe
# a lista (verificação paralelo × serial). --de-tras: ajudante de um processo serial JÁ EM CURSO (sem interrompê-lo) —
# percorre os subpassos do FIM para o começo, reivindica cada um por arquivo-trava exclusivo (<subpasso>.trava com o PID;
# trava de PID morto é retomada) e pula os prontos, os travados por outro ajudante vivo e o que o serial está fazendo
# (.M3.npy sem .npz, escrito há < 3 h). O serial vem do começo; no encontro, no máximo um subpasso é feito em dobro
# (resultado idêntico — ver verificação paralelo × serial).
# SONO: o próprio processo se re-executa sob `systemd-inhibit --what=sleep:idle` (escopo = este processo; a
# configuração global de energia não é tocada). O modelo direto é PLUGÁVEL (`model`): aqui só o toy do teste de retomada;
# o modelo da Etapa A (30 parâmetros por região, D131 7.1, sobre o NATIVEX) entra pela mesma interface.
# Uso: python .../etapaA_runner.py <toy> <dir> [--worker k/K] [--no-inhibit]
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import porta  # noqa: F401 — D132 item 123 (4): recusa (SystemExit 77) processo lançado por fora do ponto único neuron/lancar.py
import numpy as np


def atomic_save(path, **arrays):
    tmp = path + '.tmp%d' % os.getpid()
    with open(tmp, 'wb') as f: np.savez(f, **arrays)
    os.replace(tmp, path)


def fingerprint():
    """D132 item 73: identidade da máquina/compilação. Retomada BIT A BIT só vale na MESMA impressão digital."""
    import platform
    try: cpu = [l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')][0]
    except Exception: cpu = platform.processor()
    try:
        import neuron; nv = neuron.__version__
    except Exception: nv = '?'
    return json.dumps({'cpu': cpu, 'maquina': platform.machine(), 'python': platform.python_version(), 'numpy': np.__version__, 'neuron': nv}, sort_keys=True)


def _claim(ud, sname):
    """--de-tras: reivindica o subpasso (trava exclusiva com o PID). Falso se pronto, travado por PID vivo, ou em curso no serial."""
    if os.path.exists(os.path.join(ud, '%s.npz' % sname)): return False
    m3 = os.path.join(ud, '%s.M3.npy' % sname)
    if os.path.exists(m3) and time.time() - os.path.getmtime(m3) < 3 * 3600: return False
    tr = os.path.join(ud, '%s.trava' % sname)
    try:
        fd = os.open(tr, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, str(os.getpid()).encode()); os.close(fd); return True
    except FileExistsError:
        try:
            pid = int(open(tr).read() or 0); os.kill(pid, 0); return False      # dono vivo
        except (ValueError, ProcessLookupError):
            os.remove(tr); return _claim(ud, sname)                          # trava órfã: retoma
        except PermissionError: return False


def _claim_unit(outdir, u):
    """item 89 (3): trava EXCLUSIVA da unidade (PID); trava de PID morto é retomada."""
    tr = os.path.join(outdir, '%s.trava' % u)
    try:
        fd = os.open(tr, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, str(os.getpid()).encode()); os.close(fd); return True
    except FileExistsError:
        try:
            pid = int(open(tr).read() or 0); os.kill(pid, 0); return pid == os.getpid()
        except (ValueError, ProcessLookupError):
            os.remove(tr); return _claim_unit(outdir, u)
        except PermissionError: return False


def run_queue(model, outdir, log=print, only_subs=None):
    """item 89 (3): TRABALHADOR DE VIDA LONGA — constrói o modelo UMA vez (o chamador) e PUXA as unidades da lista
    (model.units()), reivindicando cada uma por trava. Uma unidade com os subpassos prontos mas sem o que a redução precisa
    (model.ready_to_reduce falso: a referência do viés ainda não chegou) é LIBERADA e fica para uma próxima passada — o
    trabalhador não bloqueia. Sai quando não há mais o que reivindicar."""
    os.makedirs(outdir, exist_ok=True); stats = {'unidades_feitas': 0, 'unidades_adiadas': 0, 'subpassos_calculados': 0}
    for u in model.units():
        fu = os.path.join(outdir, '%s.npz' % u)
        if os.path.exists(fu) or not _claim_unit(outdir, u): continue
        try:
            st = run_units(model, outdir, only_subs=only_subs, units=[u], defer_reduce=True, log=log)
            stats['subpassos_calculados'] += st['subpassos_calculados']
            if os.path.exists(fu): stats['unidades_feitas'] += 1
            elif st.get('adiadas'): stats['unidades_adiadas'] += 1
        finally:
            tr = os.path.join(outdir, '%s.trava' % u)
            if os.path.exists(tr) and open(tr).read() == str(os.getpid()): os.remove(tr)
    return stats


def run_units(model, outdir, worker=(0, 1), log=print, sub=(0, 1), only_subs=None, backwards=False, units=None, defer_reduce=False):
    os.makedirs(outdir, exist_ok=True)
    units = model.units() if units is None else units; k, K = worker
    stats = {'subpassos_calculados': 0, 'subpassos_lidos': 0, 'unidades_puladas': 0, 'adiadas': 0}
    for i, u in enumerate(units):
        if i % K != k: continue
        fu = os.path.join(outdir, '%s.npz' % u)
        if os.path.exists(fu): stats['unidades_puladas'] += 1; continue
        ud = os.path.join(outdir, u); os.makedirs(ud, exist_ok=True); subs = {}
        fp, ffp = fingerprint(), os.path.join(ud, 'IMPRESSAO')
        if os.path.exists(ffp) and open(ffp).read() != fp:           # outra máquina/compilação: não mistura subpassos
            for f in os.listdir(ud):
                if f != 'IMPRESSAO': os.remove(os.path.join(ud, f))
            log('unidade %s: impressão digital diferente — subpassos parciais descartados (recomeça a unidade)' % u)
        if not os.path.exists(ffp):
            tmp = ffp + '.tmp%d' % os.getpid(); open(tmp, 'w').write(fp); os.replace(tmp, ffp)
        allsubs = model.substeps(u)
        order = list(enumerate(allsubs))[::-1] if backwards else list(enumerate(allsubs))
        for i_s, sname in order:
            if i_s % sub[1] != sub[0] or (only_subs is not None and sname not in only_subs): continue
            fs = os.path.join(ud, '%s.npz' % sname)
            if os.path.exists(fs): stats['subpassos_lidos'] += 1; continue
            if backwards and not _claim(ud, sname): continue
            t0 = time.time(); r = model.evaluate(u, sname, ud); atomic_save(fs, **r)
            if backwards: os.remove(os.path.join(ud, '%s.trava' % sname))
            stats['subpassos_calculados'] += 1; log('%s/%s (%.1f s)' % (u, sname, time.time() - t0))
        if not all(os.path.exists(os.path.join(ud, '%s.npz' % sn)) for sn in allsubs):
            log('unidade %s: subpassos deste processo prontos; faltam os de outros processos' % u); continue
        if defer_reduce and hasattr(model, 'ready_to_reduce') and not model.ready_to_reduce(u):
            log('unidade %s: subpassos prontos; redução ADIADA (referência do viés ainda não chegou)' % u); stats['adiadas'] += 1; continue
        subs = {sn: np.load(os.path.join(ud, '%s.npz' % sn)) for sn in allsubs}            # leitura preguiçosa (memória)
        atomic_save(fu, **model.reduce(u, subs, ud)); log('unidade %s PRONTA' % u)
        if hasattr(model, 'after_reduce'): model.after_reduce(u, ud)
    return stats


class Toy:
    """Modelo REAL do NEURON, pequeno, para testar a retomada: soma + 2 dendritos; Θ = 4 parâmetros (g_pas soma,
    g_pas dendrito, R_i, c_m); unidade = ponto de injeção (3); subpasso = avaliação θ (base + ±1% em cada = 9);
    protocolo M1: ±50 pA × 200 ms no ponto, leitura em todos os pontos, CVode atol 1e-6, amostra 0.1 ms."""
    P = ['g_soma', 'g_dend', 'Ra', 'cm']

    def __init__(self):
        from neuron import h
        self.h = h; h.load_file('stdrun.hoc')
        self.soma = h.Section(name='soma'); self.soma.L = self.soma.diam = 20
        self.d = [h.Section(name='d%d' % i) for i in range(2)]
        for dd in self.d: dd.L = 300; dd.diam = 1.5; dd.nseg = 31; dd.connect(self.soma(1))
        for s in [self.soma] + self.d: s.insert('pas'); s.e_pas = -70
        self.pts = {'soma': self.soma(0.5), 'd0': self.d[0](0.5), 'd1': self.d[1](1.0)}

    def units(self): return ['p_' + k for k in self.pts]

    def substeps(self, u): return ['base'] + ['%s_%s' % (p, sg) for p in self.P for sg in ('mais', 'menos')]

    def set_theta(self, sname):
        th = {'g_soma': 1e-4, 'g_dend': 5e-5, 'Ra': 150.0, 'cm': 1.0}
        if sname != 'base':
            p, sg = sname.rsplit('_', 1); th[p] *= 1.01 if sg == 'mais' else 1 / 1.01
        self.soma.g_pas = th['g_soma']
        for dd in self.d: dd.g_pas = th['g_dend']
        for s in [self.soma] + self.d: s.Ra = th['Ra']; s.cm = th['cm']

    def evaluate(self, u, sname, ud=None):
        h = self.h; self.set_theta(sname); seg = self.pts[u[2:]]; out = {}
        for amp in (-0.05, 0.05):
            c = h.IClamp(seg); c.delay = 10; c.dur = 200; c.amp = amp
            tv = h.Vector(np.arange(0, 250.0 + 1e-9, 0.1)); rec = {k: h.Vector().record(s._ref_v, tv) for k, s in self.pts.items()}
            h.cvode_active(1); h.cvode.atol(1e-6); h.finitialize(-70); h.continuerun(250.0)
            for k, v in rec.items(): out['%s_%+.2f' % (k, amp)] = np.array(v)
            del c
        return out

    def reduce(self, u, subs, ud=None):
        """Blocos Gram por ponto de leitura r: J_r (linhas = amostras dos traços em r; colunas = ∂/∂log θ por diferença
        central) → JᵀJ (4×4) por r. É o que a Etapa A guarda por (p, r)."""
        keys = sorted(subs['base']); out = {}
        for r in self.pts:
            ks = [k for k in keys if k.startswith(r + '_')]
            J = np.stack([np.concatenate([(subs['%s_mais' % p][k] - subs['%s_menos' % p][k]) / (2 * np.log(1.01)) for k in ks])
                          for p in self.P], axis=1)
            out['JtJ_' + r] = J.T @ J
        return out


if __name__ == '__main__':
    which, outdir = sys.argv[1:3]
    wk = next((a.split('/') for a in sys.argv if a.startswith('--worker')), None)
    worker = (0, 1)
    if '--worker' in sys.argv:
        i = sys.argv.index('--worker'); k, K = sys.argv[i + 1].split('/'); worker = (int(k), int(K))
    if '--no-inhibit' not in sys.argv and os.environ.get('HANU_INHIBITED') != '1':
        env = dict(os.environ, HANU_INHIBITED='1')
        sys.exit(subprocess.call(['systemd-inhibit', '--what=sleep:idle', '--who=HANU', '--why=Etapa A (%s, worker %d/%d)' % (which, *worker),
                                  '--mode=block', sys.executable] + sys.argv, env=env))
    if which == 'unit':                                   # D132 item 66: unidade da Etapa A (modelo direto)
        import etapaA_unit as EU
        arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
        only = [l.strip() for l in open(arg('--fila-unidades')) if l.strip()] if '--fila-unidades' in sys.argv else arg('--only').split(',')
        model = EU.EtapaAUnit(os.path.abspath(arg('--hay')), only=only,
                              rec_mode='passos' if '--passos' in sys.argv else 'grade', so_theta='--so-theta' in sys.argv,
                              atol=float(arg('--atol', 1e-6)), modelo=arg('--modelo', 'region'),       # item 85: CommonSim, 'region' | 'hay'
                              cache_dir=arg('--cache') and os.path.abspath(arg('--cache')), vies_dir=arg('--vies') and os.path.abspath(arg('--vies')),
                              apagar_brutos='--apagar-brutos' in sys.argv,
                              referencia='--referencia' in sys.argv,
                              rest_key_atol=float(arg('--repouso-chave-atol')) if '--repouso-chave-atol' in sys.argv else None,
                              direcoes=arg('--direcoes') and os.path.abspath(arg('--direcoes')),
                              amplitudes=arg('--amplitudes') and os.path.abspath(arg('--amplitudes')),      # item 146: por ponto
                              theta_ref=dict((kv.split('=')[0], float(kv.split('=')[1])) for kv in arg('--theta-ref').split(',')) if '--theta-ref' in sys.argv else None)
        if '--so-theta' in sys.argv: model.reduce = lambda u, subs, ud: {'nota': np.array('reducao feita fora (item 69 2a)')}
    elif which == 'G':                                    # D132 item 69 (2a): G = ∂F/∂log θ (F reduzido), modelo direto
        import etapaA_G as EG
        arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
        model = EG.GModel(os.path.abspath(arg('--hay')), atol=float(arg('--atol', 1e-6)), cache_dir=arg('--cache') and os.path.abspath(arg('--cache')),
                          subpassos=arg('--subpassos-G') and arg('--subpassos-G').split(','),       # item 85
                          direcoes=arg('--direcoes') and os.path.abspath(arg('--direcoes')))       # item 128 (3): F ao longo de direções
    elif which == 'ref':                                  # D132 item 83: tarefa C do ref_ii (pv_C, hay4_C) — só em série
        import ref_ii_C as RIC
        model = RIC.RefC(sys.argv[sys.argv.index('--modelo') + 1], os.path.abspath(sys.argv[sys.argv.index('--saida') + 1]))
    else:
        model = {'toy': Toy}[which]()
    sub = (0, 1)
    if '--sub-worker' in sys.argv:
        i = sys.argv.index('--sub-worker'); k, K = sys.argv[i + 1].split('/'); sub = (int(k), int(K))
    only_subs = sys.argv[sys.argv.index('--subpassos') + 1].split(',') if '--subpassos' in sys.argv else None
    os.makedirs(outdir, exist_ok=True)                     # vários workers no mesmo diretório: sem corrida, um PID por worker
    pidf = 'PID' if worker[1] == 1 else 'PID.w%d_%d' % worker
    if sub[1] > 1: pidf += '.s%d_%d' % sub
    if '--de-tras' in sys.argv: pidf += '.tras%d' % os.getpid()
    if '--fila-unidades' in sys.argv: pidf += '.trab%d' % os.getpid()
    with open(os.path.join(outdir, pidf), 'w') as f: f.write(str(os.getpid()))
    if '--fila-unidades' in sys.argv:                     # item 89 (3): trabalhador de vida longa (lista de unidades)
        st = run_queue(model, outdir, only_subs=only_subs)
    else:
        st = run_units(model, outdir, worker, sub=sub, only_subs=only_subs, backwards='--de-tras' in sys.argv)
    import resource
    st['pico_memoria_MB'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0   # item 78: memória por tipo de processo
    print('FIM', json.dumps(st), flush=True)
