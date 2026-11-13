# stim_common.py — D132 item 51(3)/52: INJEÇÃO DE ESTÍMULO COM RESTAURAÇÃO DE ESTADO, compartilhada (NEURON, qualquer
# modelo), com AUTOTESTE OBRIGATÓRIO: o Injector roda sozinho, no construtor, o teste de UM PULSO contra PASSO FIXO no
# próprio modelo e no próprio ponto de injeção; falhou → AutotestFailed e a rodada NÃO começa. run() recusa rodar sem
# autoteste aprovado. O que vive só em texto se repete; o que vive aqui, com autoteste, não.
# Armadilhas cobertas (todas já encontradas no D131/D132):
#   T1 Vector.play NÃO atua depois de SaveState.restore(): o restore() LIMPA a fila de eventos — inclusive os eventos de
#      descontinuidade que o play montou no finitialize (D131: EPSP zero; ref_ii: estímulo sumia). → restore(1), que
#      mantém a fila do finitialize (verificado num compartimento: restore() 0.000 mV; restore(1) 15.652 vs IClamp 15.656).
#   T2 CVode passa por cima de pulso curto quando o play é contínuo sem índices de descontinuidade → índices nas bordas.
#   T6 (custo) o play contínuo numa grade fina em TODO o intervalo faz o CVode parar em CADA ponto da grade (≈2 passos por
#      ponto: 17 699 passos em 40 ms a 5 µs) — correto, mas o CVode vira passo fixo de ~2.5 µs. → só pontos de quebra +
#      grade apenas onde há α ativo.
#   T3 h.cvode.active(1) chamado do Python NÃO liga o `using_cvode_` do stdrun: o continuerun não posta o evento de
#      tstop e o CVode passa do fim (num passivo puro: pedido 500 ms, parou em 4 400 ms). → h.cvode_active(1) (proc do
#      stdrun) e conferência do t final em toda rodada.
#   (T4, convergência da referência: convergence_check(); T5, detector validado: require_validated_detector().)
# Estímulos: ('s', t0, amp nA, dur ms) retangular | ('a', t0, amp nA, tau_d ms) α de dupla exponencial (τr 0.5 ms), pico
# = amp. Tempos relativos ao fim do repouso.
import os, json, hashlib, time
import sys as _sys; _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import porta  # noqa: F401 — D132 item 123 (4): recusa (SystemExit 77) processo lançado por fora do ponto único neuron/lancar.py
import numpy as np
from neuron import h

HERE = os.path.dirname(os.path.abspath(__file__))
GRID = 0.005                                   # ms — grade da forma de onda tocada


class AutotestFailed(RuntimeError):
    pass


def alpha(x, td, tr=0.5):
    tp = tr * td * np.log(td / tr) / (td - tr); nrm = np.exp(-tp / td) - np.exp(-tp / tr)
    return np.where(x >= 0, (np.exp(-np.clip(x, 0, None) / td) - np.exp(-np.clip(x, 0, None) / tr)) / nrm, 0.0)


def _I(stims, t):
    I = np.zeros_like(t)
    for s in stims:
        if s[0] == 's': I += np.where((t >= s[1]) & (t < s[1] + s[3]), s[2], 0.0)
        elif s[0] == 'a': I += s[2] * alpha(t - s[1], s[3])
        else: raise ValueError(s)
    return I


def waveform(stims, tstop, grid=GRID, gridded=False):
    """Forma de onda para Vector.play contínuo: (t, I, índices de descontinuidade).
    Só os PONTOS DE QUEBRA (degraus: tempo duplicado — valor à esquerda e à direita —, índice no 2º) e a grade fina apenas
    onde um α está ativo (do início a 20·τd). gridded=True: grade fina em todo o intervalo (o desenho antigo do ref_ii —
    correto, mas o CVode para em CADA ponto da grade: 17 699 passos em 40 ms num compartimento)."""
    if gridded:
        tg = np.arange(0.0, tstop + 1.0, grid); I = _I(stims, tg); disc = set()
        for s in stims:
            disc |= {int(round(s[1] / grid))} | ({int(round((s[1] + s[3]) / grid))} if s[0] == 's' else set())
        return tg, I, sorted(i for i in disc if 0 <= i < len(tg))
    jumps = sorted({x for s in stims if s[0] == 's' for x in (s[1], s[1] + s[3])})
    pts = {0.0, tstop + 1.0}
    for s in stims:
        if s[0] == 'a': pts |= set(np.round(np.arange(s[1], min(s[1] + 20 * s[3], tstop + 1.0), grid), 9))
    pts = np.array(sorted(pts - set(jumps)))
    t = list(pts); I = list(_I(stims, pts)); tag = [0] * len(t)
    for j in jumps:                                   # degrau: dois pontos no mesmo instante (esquerda, direita)
        if not (0.0 < j <= tstop + 1.0): continue
        t += [j, j]; I += [float(_I(stims, np.array([j - 1e-9]))[0]), float(_I(stims, np.array([j]))[0])]; tag += [1, 2]
    o = np.lexsort((tag, t)); t = np.array(t)[o]; I = np.array(I)[o]; tag = np.array(tag)[o]
    return t, I, list(np.flatnonzero(tag == 2))


# D132 item 157 — DOIS GUARDAS GERAIS em TODA simulação do CommonSim.run (o caminho único das unidades, do condicionamento, do G e do Hay):
#  (1) FÍSICO: |V| > V_PLAUS em um sítio VIGIADO (os estimulados + o soma), a cada passo ACEITO da integração → aborta no ato; e uma pós-checagem nas
#      gravações (todas as leituras pedidas) → a mesma falha. Voltagem assim é fuga numérica ou protocolo fora do físico, nunca resultado útil.
#  (2) TEMPO: tempo de CPU da simulação > K_TEMPO × a mediana MEDIDA do mesmo TIPO (estímulos, tstop, nº de leituras, tamanho do modelo, atol), com piso
#      PISO_S, e só depois de N_MIN medidas desse tipo → aborta. CPU (não relógio): suspensão da máquina e disputa por núcleo não contam.
#  Os guardas só LEEM (v dos sítios vigiados e o relógio de CPU) depois de cada fadvance(), pela redefinição de advance() do stdrun — a integração é a
#  MESMA (regressão bit a bit). Falha → SimulacaoAbortada(motivo): o chamador marca a avaliação como NÃO AVALIADA; a fila segue.
V_PLAUS = 200.0; K_TEMPO = 5.0; PISO_S = 60.0; N_MIN = 5
TEMPOS = os.path.join(HERE if 'HERE' in globals() else os.path.dirname(os.path.abspath(__file__)), 'results', 'guardas', 'tempos_cpu.log')


class SimulacaoAbortada(RuntimeError):
    pass


class _Guarda:
    def __init__(self):
        self.ativo = False; self.segs = (); self.lim = None; self.t0 = 0.0; self.motivo = None; self.ts = 0.0

    def tick(self):
        if not self.ativo: return 0
        for s in self.segs:
            v = s.v
            if v > V_PLAUS or v < -V_PLAUS:
                self.motivo = 'GUARDA FÍSICO: V = %.1f mV em %s (t = %.3f ms; limite ±%g mV)' % (v, s, h.t - self.ts, V_PLAUS); self.ativo = False; h.stoprun = 1; return 0
        if self.lim is not None and time.process_time() - self.t0 > self.lim:
            self.motivo = 'GUARDA DE TEMPO: CPU %.1f s > limite %.1f s (t = %.3f ms)' % (time.process_time() - self.t0, self.lim, h.t - self.ts); self.ativo = False; h.stoprun = 1
        return 0


GUARDA = _Guarda(); _MEDIDAS = None


def _medianas():
    global _MEDIDAS
    if _MEDIDAS is None:
        _MEDIDAS = {}
        try:
            for l in open(TEMPOS):
                k, v = l.rstrip('\n').split('\t'); _MEDIDAS.setdefault(k, []).append(float(v))
        except (OSError, ValueError): pass
    return _MEDIDAS


def limite_tempo(chave):
    xs = _medianas().get(chave, [])
    return None if len(xs) < N_MIN else max(K_TEMPO * float(np.median(xs)), PISO_S)


def registra_tempo(chave, cpu):
    _medianas().setdefault(chave, []).append(cpu)
    try:
        os.makedirs(os.path.dirname(TEMPOS), exist_ok=True)
        fd = os.open(TEMPOS, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644); os.write(fd, ('%s\t%.3f\n' % (chave, cpu)).encode()); os.close(fd)
    except OSError: pass


def _stdrun():
    h.load_file('stdrun.hoc')
    if not getattr(h, '_hanu_guarda_ok', 0):                              # item 157: advance() = fadvance() + checagem (só leitura)
        h('objref _hanu_guarda\n_hanu_guarda_ok = 1')
        h._hanu_guarda = GUARDA
        h('proc advance() { fadvance()  _hanu_guarda.tick() }')


def state_key(**desc):
    """D132 item 69 (2b): CHAVE do repouso guardado = hash de TUDO que o define (θ, geometria, discretização, assentamento);
    nunca só θ."""
    return hashlib.sha256(json.dumps(desc, sort_keys=True, default=str).encode()).hexdigest()[:24]


class Injector:
    """Corrente no segmento `seg` a partir do repouso salvo (CVode atol, assentado `rest_ms`).
    autotest_rec: segmento lido no autoteste (padrão = o próprio seg). test_amp/test_dur: pulso do autoteste (nA, ms) —
    tem de ficar SUBLIMIAR e dar deflexão ≥ 0.1 mV no ponto lido (senão o autoteste falha e diz por quê)."""

    def __init__(self, seg, rest_ms=3000.0, atol=1e-6, test_amp=0.2, test_dur=1.0, autotest_rec=None, verbose=True, gridded=False,
                 state_file=None):
        _stdrun()
        self.seg = seg; self.atol = atol; self.verbose = verbose; self.ok = False; self.gridded = gridded; self.rest_ms = rest_ms
        self.stim = h.IClamp(seg); self.stim.delay = 0.0; self.stim.dur = 1e9; self.stim.amp = 0.0
        self.rec_seg = seg if autotest_rec is None else autotest_rec
        if state_file and os.path.exists(state_file):            # item 69 (2b): repouso GUARDADO (mesma chave)
            self.load_state(state_file)
        else:
            self.settle()
            if state_file: self.save_state(state_file)
        self.autotest(test_amp, test_dur)

    # ------------------------------------------------------------------ repouso: assentar / guardar / carregar (item 69 2b)
    def settle(self):
        h.cvode_active(1); h.cvode.atol(self.atol)
        h.finitialize(h.v_init); h.continuerun(self.rest_ms)
        if abs(h.t - self.rest_ms) > 1e-6:
            raise AutotestFailed('T3: repouso parou em t = %.6f ms, pedido %.6f (continuerun sem evento de tstop)' % (h.t, self.rest_ms))
        self.ss = h.SaveState(); self.ss.save(); self.TS = h.t; self.v_rest = self.rec_seg.v

    def save_state(self, path):
        tmp = path + '.tmp%d' % os.getpid(); f = h.File(); f.wopen(tmp); self.ss.fwrite(f); f.close(); os.replace(tmp, path)
        meta = {'TS': self.TS, 'v_rest': self.v_rest, 'rest_ms': self.rest_ms}
        tmp = path + '.json.tmp%d' % os.getpid(); json.dump(meta, open(tmp, 'w')); os.replace(tmp, path + '.json')

    def load_state(self, path):
        """Carrega o repouso guardado e CONFERE: t e V no ponto lido têm de ser os gravados (senão AutotestFailed). A
        rodada seguinte usa restore(1) como sempre (T1)."""
        meta = json.load(open(path + '.json'))
        ss = h.SaveState(); f = h.File(); f.ropen(path); ss.fread(f); f.close()
        h.finitialize(h.v_init); ss.restore(1)
        if abs(h.t - meta['TS']) > 1e-9 or abs(self.rec_seg.v - meta['v_rest']) > 1e-9:
            raise AutotestFailed('repouso guardado não confere: t %.9f × %.9f, V %.9f × %.9f' % (h.t, meta['TS'], self.rec_seg.v, meta['v_rest']))
        self.ss = ss; self.TS = h.t; self.v_rest = self.rec_seg.v; self.ok = getattr(self, 'ok', False)

    def move(self, seg, rec=None):
        """Muda o ponto de injeção (o mesmo IClamp; nada de assentar de novo)."""
        self.stim.loc(seg); self.seg = seg
        if rec is not None: self.rec_seg = rec

    # ------------------------------------------------------------------ rodada
    def _run(self, stims, tstop, recs, atol=None, rec_grid=None):
        tg, I, disc = waveform(stims, tstop, gridded=self.gridded)
        tv = h.Vector(tg + self.TS); iv = h.Vector(I); idx = h.Vector(disc)
        iv.play(self.stim._ref_amp, tv, 1, idx)
        if rec_grid:                                  # gravação numa grade FIXA pela interpolação do próprio CVode (não
            TV = h.Vector(np.arange(0.0, tstop + 1e-9, rec_grid) + self.TS)      # acrescenta passos; = amostragem)
            vecs = {k: h.Vector().record(s._ref_v, TV) for k, s in recs.items()}
        else:
            vecs = {k: h.Vector().record(s._ref_v) for k, s in recs.items()}; TV = h.Vector().record(h._ref_t)
        h.cvode_active(1); h.cvode.atol(self.atol if atol is None else atol)
        h.finitialize(h.v_init); self.ss.restore(1); h.cvode.re_init(); h.fcurrent(); h.frecord_init()
        h.continuerun(self.TS + tstop)
        tend = h.t; iv.play_remove(); self.stim.amp = 0.0
        if abs(tend - (self.TS + tstop)) > 1e-6:
            raise AutotestFailed('T3: rodada parou em t = %.6f, pedido %.6f' % (tend - self.TS, tstop))
        t = np.array(TV) - self.TS
        return t, {k: np.array(v) for k, v in vecs.items()}

    def run(self, stims, tstop, recs, atol=None, rec_grid=None):
        """recs: {nome: segmento}. rec_grid (ms): grava numa grade fixa. Retorna (t relativo ao fim do repouso, {nome: V})."""
        if not self.ok:
            raise AutotestFailed('autoteste não aprovado — rodada recusada')
        return self._run(stims, tstop, recs, atol, rec_grid)

    def _fixed(self, amp, t0, dur, tstop, dt):
        """Referência independente do play: IClamp clássico, passo FIXO (Euler implícito), mesmo repouso."""
        c = h.IClamp(self.seg); c.delay = self.TS + t0; c.dur = dur; c.amp = amp
        v = h.Vector().record(self.rec_seg._ref_v); TV = h.Vector().record(h._ref_t)
        h.cvode_active(0); h.dt = dt
        h.finitialize(h.v_init); self.ss.restore(); h.t = self.TS; h.fcurrent(); h.frecord_init()
        h.continuerun(self.TS + tstop)
        h.cvode_active(1); del c
        return np.array(TV) - self.TS, np.array(v)

    # ------------------------------------------------------------------ autoteste (critérios declarados no D132 item 52)
    def autotest(self, amp, dur):
        t0, tstop = 10.0, 40.0
        ta, r = self._run([('s', t0, amp, dur)], tstop, {'v': self.rec_seg}); va = r['v']
        tb, vb = self._fixed(amp, t0, dur, tstop, 0.0025)
        pre = ta < t0 - 1e-9
        da, db = va - self.v_rest, vb - self.v_rest
        ia, ib = int(np.argmax(np.abs(da))), int(np.argmax(np.abs(db)))
        res = {'v_rest': self.v_rest, 'v0_play': float(va[0]), 'v0_fixo': float(vb[0]),
               'deriva_pre_pulso_mV': float(np.abs(da[pre]).max()), 'deflexao_play_mV': float(da[ia]),
               'deflexao_fixo_mV': float(db[ib]), 't_pico_play': float(ta[ia]), 't_pico_fixo': float(tb[ib])}
        fails = []
        if abs(va[0] - self.v_rest) > 1e-3 or abs(vb[0] - self.v_rest) > 1e-3: fails.append('restauração: V inicial ≠ repouso salvo')
        if res['deriva_pre_pulso_mV'] > 0.01: fails.append('V mexe antes do pulso (> 0.01 mV)')
        if abs(res['deflexao_fixo_mV']) < 0.1: fails.append('pulso de teste fraco demais (< 0.1 mV no passo fixo) — aumentar test_amp')
        if abs(res['deflexao_fixo_mV']) > 15.0: fails.append('pulso de teste forte demais (> 15 mV) — reduzir test_amp')
        if abs(res['deflexao_play_mV'] - res['deflexao_fixo_mV']) > 0.02 * abs(res['deflexao_fixo_mV']):
            fails.append('T1/T2: deflexão do play %.4f × passo fixo %.4f mV (> 2%%)' % (res['deflexao_play_mV'], res['deflexao_fixo_mV']))
        if abs(res['t_pico_play'] - res['t_pico_fixo']) > 0.1: fails.append('tempo do pico difere > 0.1 ms')
        self.autotest_result = res
        if fails:
            raise AutotestFailed('AUTOTESTE FALHOU (%s): ' % self.seg + '; '.join(fails) + ' | ' + json.dumps(res))
        self.ok = True
        if self.verbose:
            print('autoteste do estímulo OK (%s): deflexão play %.4f / passo fixo %.4f mV, pico %.3f / %.3f ms, deriva %.1e mV'
                  % (self.seg, res['deflexao_play_mV'], res['deflexao_fixo_mV'], res['t_pico_play'], res['t_pico_fixo'],
                     res['deriva_pre_pulso_mV']), flush=True)

    # ------------------------------------------------------------------ T4: convergência da referência (sentinela)
    def convergence_check(self, stims, tstop, rec_seg, detect, tol_ms=0.05):
        """Roda o protocolo sentinela em atol e atol/10; os eventos (detect(t, v) → lista de tempos de pico) têm de ter a
        mesma contagem e diferir ≤ tol_ms. Falhou → AutotestFailed."""
        ta, ra = self.run(stims, tstop, {'v': rec_seg}); tb, rb = self.run(stims, tstop, {'v': rec_seg}, atol=self.atol / 10)
        ea, eb = detect(ta, ra['v']), detect(tb, rb['v'])
        if len(ea) != len(eb) or (ea and max(abs(a - b) for a, b in zip(ea, eb)) > tol_ms):
            raise AutotestFailed('T4: referência NÃO convergida em atol %g: %d × %d eventos, Δ máx %s ms'
                                 % (self.atol, len(ea), len(eb), max((abs(a - b) for a, b in zip(ea, eb)), default=None)))
        if self.verbose:
            print('T4 convergência OK: %d eventos, Δ máx %.4f ms (atol %g × %g)' % (len(ea), max((abs(a - b) for a, b in zip(ea, eb)), default=0.0),
                                                                              self.atol, self.atol / 10), flush=True)
        return len(ea)


# ---------------------------------------------------------------------- T5: detector validado
REGISTRY = os.path.join(HERE, 'results', 'detector', 'VALIDADO.json')


def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def require_validated_detector(model, protocols, detector=os.path.join(HERE, 'detect_peak.py')):
    """O detector só é usado em (modelo, protocolo) que passaram no controle negativo COM ESTE CÓDIGO (hash). Falta → a
    rodada não começa (rodar o controle negativo primeiro e registrar no VALIDADO.json)."""
    reg = json.load(open(REGISTRY)); hsh = sha256(detector)
    ent = [e for e in reg['validacoes'] if e['sha256'] == hsh and e['modelo'] == model]
    if not ent:
        raise AutotestFailed('T5: detector %s (sha256 %s…) sem validação registrada para %s' % (os.path.basename(detector), hsh[:12], model))
    ok = set().union(*(set(e['protocolos_negativos']) for e in ent))
    miss = [p for p in protocols if p not in ok]
    if miss:
        raise AutotestFailed('T5: protocolos sem controle negativo com este detector em %s: %s' % (model, miss))
    return True


# ====================================================================== CÓDIGO ÚNICO (D132 item 73 (1))
# Assentamento POR CRITÉRIO, injeção em VÁRIOS sítios com pesos (degraus e α = forma do `epsp` do Hay, pico = amplitude),
# leitura ponderada e chave do resultado com a discretização e o CRITÉRIO de assentamento. TODO cálculo em CVode do
# desmame (Etapa A, viés, validação do V2) passa por aqui. O autoteste do Injector (pulso × passo fixo) roda uma vez.
SETTLE = {'metodo': 'euler_implicito', 'dt': 0.1, 'bloco_ms': 100.0, 'tol': 1e-8, 'teto_ms': 60000.0}   # item 73 (correção)


def model_hash():
    """D132 item 73: impressão do MODELO como está agora (todas as seções vivas: nome sem o índice do template, nseg, L,
    Ra; por segmento: diam, cm e TODOS os parâmetros RANGE dos mecanismos inseridos; pontos de processo por tipo). Entra na
    chave do repouso guardado — θ, geometria e discretização ficam todos dentro, sem descrição manual."""
    hs = hashlib.sha256(); mt = h.MechanismType(0); names = []
    for i in range(int(mt.count())):
        mt.select(i); nm = h.ref(''); mt.selected(nm); names.append(nm[0])
    for sec in sorted(h.allsec(), key=lambda q: q.name().split('.')[-1]):
        hs.update(('%s|%d|%.12g|%.12g' % (sec.name().split('.')[-1], sec.nseg, sec.L, sec.Ra)).encode())
        mechs = [m for m in names if h.ismembrane(m, sec=sec) and m not in ('morphology', 'capacitance')]
        for seg in sec:
            hs.update(('%.12g|%.12g' % (seg.diam, seg.cm)).encode())
            for m in mechs:
                if m.endswith('_ion'): continue
                ms = h.MechanismStandard(m, 1)
                for j in range(int(ms.count())):
                    q = h.ref(''); ms.name(q, j)
                    try: hs.update(('%s=%.12g' % (q[0], getattr(seg, q[0]))).encode())
                    except Exception: pass
    # pontos de processo que INJETAM no repouso (item 85): IClamp com amp ≠ 0 e epsp com imax ≠ 0. Os grampos de amplitude
    # zero (os do play, entre rodadas) não mudam o repouso — contá-los fazia a chave depender da HISTÓRIA do processo
    # (quantos grampos já foram criados) e impedia o reaproveitamento do repouso entre unidades e processos.
    pp = {}
    if hasattr(h, 'IClamp'): pp['IClamp'] = sum(1 for c in h.List('IClamp') if c.amp != 0.0)
    if hasattr(h, 'epsp'): pp['epsp'] = sum(1 for e in h.List('epsp') if e.imax != 0.0)
    hs.update(json.dumps(pp, sort_keys=True).encode())
    return hs.hexdigest()[:24]


class CommonSim:
    def __init__(self, soma_seg, atol=1e-6, settle=SETTLE, state_file=None, test_amp=0.2, verbose=True, cache_dir=os.environ.get('HANU_REST_CACHE'), warm=None,
                 sites=(), rest_key_atol=None):
        """cache_dir: guarda/carrega o repouso pela chave AUTOMÁTICA (model_hash + critério + atol). warm: SaveState de onde o
        assentamento parte (determinístico; padrão = finitialize em v_init). sites: segmentos que vão receber injeção — os
        grampos (amp 0) são criados ANTES do assentamento (item 85)."""
        self.warm = warm; self.cache_dir = cache_dir; self.test_amp = test_amp
        # item 103: o repouso é por Euler implícito (sem CVode) → não depende do atol (conferido: 61 repousos idênticos byte a
        # byte nas caches de 10⁻⁸ e 10⁻¹⁰); rest_key_atol permite reaproveitar a cache de outro atol sem mudar o estado
        self.rest_key_atol = atol if rest_key_atol is None else rest_key_atol
        self.atol = atol; self.crit = dict(settle)
        if cache_dir and state_file is None: state_file = self._state_path()
        self.state_file = state_file
        _stdrun(); self.verbose = verbose; self.clamps = {}; self._nseg = sum(sec.nseg for sec in h.allsec())   # item 157: tamanho do modelo (chave do tipo)
        self.inj = Injector.__new__(Injector)                       # o Injector sem o assentamento por tempo
        I = self.inj; I.seg = soma_seg; I.atol = atol; I.verbose = False; I.ok = False; I.gridded = False; I.rest_ms = None
        I.stim = h.IClamp(soma_seg); I.stim.delay = 0.0; I.stim.dur = 1e9; I.stim.amp = 0.0; I.rec_seg = soma_seg
        self.clamps[soma_seg] = I.stim
        for seg in sites: self._clamp(seg)
        if state_file and os.path.exists(state_file): I.load_state(state_file); self.settle_info = 'carregado'
        else:
            self.settle_info = self._settle()
            if state_file: I.save_state(state_file)
        I.autotest(test_amp, 1.0)
        # α: o mecanismo `epsp` do Hay (forma idêntica: dupla exponencial τ0/τ1, pico = imax, corrente para dentro) é
        # analítico — o play numa grade de 5 µs faz o CVode parar em cada ponto (T6). Usado SÓ se, neste processo, o EPSP
        # pelos dois caminhos concordar no soma (pico ≤ 0.1%); senão fica o play (D132 item 73).
        self.alpha_epsp = False
        if hasattr(h, 'epsp'):
            rec = {'v': [(soma_seg, 1.0)]}; st = [('a', 105.0, 0.05, 3.0)]          # início TARDIO: o caso que falhava (item 76)
            tb, b0 = self.run([], 160.0, rec, guarda_tempo=False); tp, yp = self.run(st, 160.0, rec, guarda_tempo=False)   # item 159: autotestes sem o guarda de TEMPO
            self.alpha_epsp = True; te, ye = self.run(st, 160.0, rec, guarda_tempo=False)
            pp = (yp['v'] - np.interp(tp, tb, b0['v'])).max(); pe = (ye['v'] - np.interp(te, tb, b0['v'])).max()
            self.alpha_epsp = abs(pe / pp - 1) <= 1e-3; self.alpha_check = (pp, pe)
            if verbose: print('CommonSim: α por epsp × play: pico %.6f × %.6f mV (%.1e) → %s' % (pe, pp, pe / pp - 1, 'epsp' if self.alpha_epsp else 'play'), flush=True)
        self.late_onset_check()
        if verbose: print('CommonSim: repouso %s; autoteste ok (inclui início tardio)' % self.settle_info, flush=True)

    def _state_path(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        return os.path.join(self.cache_dir, state_key(modelo=model_hash(), assentamento=dict(self.crit), atol=self.rest_key_atol,
                                                      partida='quente' if self.warm is not None else 'v_init') + '.dat')

    def resettle(self, drift_tol=0.01):
        """item 85: o MODELO mudou (θ, geometria) no mesmo processo — assenta de novo pela MESMA regra (critério de
        convergência; repouso guardado pela chave automática), com os mesmos grampos. Os autotestes de código (pulso × passo
        fixo, α, início tardio) já passaram no construtor; aqui a conferência é a do REPOUSO: carregado confere t e V
        (load_state), e 1 ms sem estímulo pelo CVode não sai de V_repouso por mais de drift_tol mV."""
        I = self.inj; I.ok = False
        for c in self.clamps.values(): c.amp = 0.0
        sf = self._state_path() if self.cache_dir else None
        if sf and os.path.exists(sf): I.load_state(sf); self.settle_info = 'carregado'
        else:
            I.rec_seg = I.seg; self.settle_info = self._settle()
            if sf: I.save_state(sf)
        self.state_file = sf; I.ok = True
        t, o = self.run([], 1.0, {'v': [(I.rec_seg, 1.0)]}, rec_grid=0.1, guarda_tempo=False)
        d = float(np.abs(o['v'] - I.v_rest).max())
        if d > drift_tol:
            I.ok = False; raise AutotestFailed('repouso NÃO parado depois do reassentamento: |ΔV| %.3e mV em 1 ms' % d)
        return self.settle_info

    def late_onset_check(self, tol=0.01):
        """item 78: AUTOTESTE DE INÍCIO TARDIO para todo tipo de estímulo. A partir do repouso (equilíbrio, invariante no
        tempo), o estímulo com início em 10 ms e em 105 ms tem de dar a MESMA forma deslocada: |Δ| máx ≤ tol × deflexão."""
        rec = {'v': [(self.inj.seg, 1.0)]}; res = {}
        for kind, amp, par in (('s', 0.05, 5.0), ('a', 0.05, 3.0)):
            ys = []
            for t0 in (10.0, 105.0):
                t, o = self.run([(kind, t0, amp, par)], t0 + 60.0, rec, rec_grid=0.025, guarda_tempo=False)
                ys.append(o['v'][(t >= t0 - 1e-9) & (t <= t0 + 60.0 + 1e-9)][:2400])
            n = min(len(ys[0]), len(ys[1])); d0 = np.abs(ys[0][:n] - ys[0][0]).max(); dd = np.abs(ys[0][:n] - ys[1][:n]).max()
            res[kind] = (dd, d0)
            if d0 <= 0 or dd > tol * d0:
                raise AutotestFailed('início TARDIO (%s): resposta a 105 ms ≠ a 10 ms (|Δ| %.3e de deflexão %.3e) — estímulo pulado?' % (kind, dd, d0))
        self.late_check = res

    def _states(self):
        a = h.cvode.active(); h.cvode.active(1); h.cvode.re_init(); v = h.Vector(); h.cvode.states(v); h.cvode.active(a)
        return np.array(v)

    def _settle(self):
        """Repouso por EULER IMPLÍCITO (ponto fixo = equilíbrio verdadeiro, sem ruído de tolerância) até |Δx| ≤ tol."""
        c = self.crit; h.cvode_active(0); h.dt = c['dt']; h.finitialize(h.v_init)
        if self.warm is not None: self.warm.restore(); h.t = 0.0; h.fcurrent()
        prev = self._states(); t = 0.0
        while True:
            t += c['bloco_ms']; h.continuerun(t)
            if abs(h.t - t) > 1e-6: raise AutotestFailed('T3 no assentamento: t = %.6f, pedido %.6f' % (h.t, t))
            cur = self._states(); d = float(np.abs(cur - prev).max()); prev = cur
            if d <= c['tol']: break
            if t >= c['teto_ms']: raise AutotestFailed('repouso NÃO convergiu em %.0f ms (|Δx| máx %.2e > %.0e)' % (t, d, c['tol']))
        I = self.inj; I.ss = h.SaveState(); I.ss.save(); I.TS = h.t; I.v_rest = I.rec_seg.v
        return 'convergido em %.0f ms (|Δx| máx no último bloco %.1e)' % (t, d)

    def key(self, **desc):
        return state_key(assentamento=self.crit, atol=self.atol, alfa='epsp' if getattr(self, 'alpha_epsp', False) else 'play', **desc)

    def _clamp(self, seg):
        if seg not in self.clamps:
            c = h.IClamp(seg); c.delay = 0.0; c.dur = 1e9; c.amp = 0.0; self.clamps[seg] = c
        return self.clamps[seg]

    def run(self, stims, tstop, recs, rec_grid=None, atol=None, guarda_tempo=True):
        """stims: ('s', t0, amp, dur, sítios) | ('a', t0, amp, τd, sítios); sítios = [(seg, w)] (padrão: o soma).
        recs: {nome: [(seg, w)]}. Retorna (t, {nome: V ponderado})."""
        I = self.inj
        if not I.ok: raise AutotestFailed('autoteste não aprovado — rodada recusada')
        by = {}; keep = []
        for st in stims:
            sites = st[4] if len(st) > 4 else [(I.seg, 1.0)]
            for seg, w in sites:
                if w == 0.0: continue
                if st[0] == 'a' and self.alpha_epsp:          # α analítico (mecanismo epsp do Hay): sem paradas do CVode
                    e = h.epsp(seg); e.tau0 = 0.5; e.tau1 = st[3]; e.imax = st[2] * w; e.onset = I.TS + st[1]; keep.append(e)

                else:
                    by.setdefault(seg, []).append((st[0], st[1], st[2] * w, st[3]))
        # item 78: PARADA FORÇADA PARA TODO ESTÍMULO — um marcador de amplitude ZERO (descontinuidade do play) no início de
        # cada estímulo e no fim de cada degrau: o CVode, partindo de um equilíbrio perfeito, não pula nenhum (item 76).
        for st in (stims if getattr(self, 'forced_stop', True) else ()):
            by.setdefault(I.seg, []).append(('s', st[1], 0.0, 1e-3))
            if st[0] == 's': by.setdefault(I.seg, []).append(('s', st[1] + st[3], 0.0, 1e-3))
        plays = []
        for seg, sl in by.items():
            tg, Iw, disc = waveform(sl, tstop); tv = h.Vector(tg + I.TS); iv = h.Vector(Iw); idx = h.Vector(disc)
            iv.play(self._clamp(seg)._ref_amp, tv, 1, idx); plays.append((iv, tv, idx, seg))
        segs = {seg for rl in recs.values() for seg, w in rl}
        if rec_grid:
            TV = h.Vector(np.arange(0.0, tstop + 1e-9, rec_grid) + I.TS); vec = {seg: h.Vector().record(seg._ref_v, TV) for seg in segs}
        else:
            vec = {seg: h.Vector().record(seg._ref_v) for seg in segs}; TV = h.Vector().record(h._ref_t)
        h.cvode_active(1); h.cvode.atol(self.atol if atol is None else atol)
        # item 157: os GUARDAS — sítios vigiados = os estimulados + o soma; limite de CPU pela mediana do tipo
        vig = {I.seg}
        for st in stims:
            for seg, w in (st[4] if len(st) > 4 else [(I.seg, 1.0)]): vig.add(seg)
        # item 159: o α pelo PLAY (CVode parando a cada 5 µs) é OUTRO tipo de simulação que o α pelo epsp → 'aP' (as chaves dos protocolos não mudam)
        chave = '%s|%g|%d|%d|%g' % ('+'.join(st[0] + ('P' if st[0] == 'a' and not self.alpha_epsp else '') for st in stims) or '-', tstop, len(segs), self._nseg, self.atol if atol is None else atol)
        GUARDA.segs = tuple(vig); GUARDA.lim = limite_tempo(chave) if guarda_tempo else None; GUARDA.motivo = None; GUARDA.ts = I.TS
        h.finitialize(h.v_init); I.ss.restore(1); h.cvode.re_init(); h.fcurrent(); h.frecord_init()
        GUARDA.t0 = time.process_time(); GUARDA.ativo = True
        try: h.continuerun(I.TS + tstop)
        finally: GUARDA.ativo = False
        tend = h.t; cpu = time.process_time() - GUARDA.t0
        for iv, tv, idx, seg in plays: iv.play_remove(); self.clamps[seg].amp = 0.0
        del keep
        if GUARDA.motivo: raise SimulacaoAbortada(GUARDA.motivo)
        if abs(tend - (I.TS + tstop)) > 1e-6: raise AutotestFailed('T3: rodada parou em t = %.6f, pedido %.6f' % (tend - I.TS, tstop))
        t = np.array(TV) - I.TS
        out = {k: sum(w * np.array(vec[seg]) for seg, w in rl) for k, rl in recs.items()}
        for k, y in out.items():                                          # item 157: pós-checagem nas gravações (todas as leituras)
            m = float(np.abs(y).max()) if np.size(y) else 0.0
            if not np.isfinite(m) or m > V_PLAUS: raise SimulacaoAbortada('GUARDA FÍSICO (pós-checagem): |V| = %.1f mV na leitura %s (limite ±%g mV)' % (m, k, V_PLAUS))
        if guarda_tempo: registra_tempo(chave, cpu)
        return t, out
