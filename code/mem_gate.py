# mem_gate.py — D132 item 81 (1): REGRA DE LANÇAMENTO. Um processo novo só é lançado se
#   (a) MemAvailable − orçamento do processo ≥ PISO_MB, e
#   (b) a taxa de swap-in (pswpin, medida por JANELA_S) ≤ SWAPIN_MAX páginas/s (sem troca ativa: mais processos pioram), e
#   (c) item 83: simulações PESADAS rodando (não suspensas) < MAX_SIM — a máquina tem 4 núcleos FÍSICOS (i5-8250U, 8 com
#       hyperthreading); medido: 3 processos → velocidade 1.0 cada, 5 → ~0.8, 7 → ~0.44 (vazão 3.0 / ~4.0 / ~3.1).
#       O tipo 'toy' (segundos, ~40 MB) não conta nem é barrado por (c).
# Orçamento por tipo de processo = pico MEDIDO × folga (ORCAMENTO_MB). Abaixo do piso durante a execução: novos
# lançamentos PAUSAM (a fila espera; nada já rodando é parado). Os valores são DECLARADOS antes de lançar (item 81).
# Uso: python3 mem_gate.py check <tipo>            → imprime o veredito, código de saída 0 = pode lançar
#      python3 mem_gate.py fila <tipo> <arq_cmds> <log>  → lança as linhas de <arq_cmds> uma a uma, cada uma só com o portão
#      aberto (reconfere a cada CADA_S), grava PID REAL de cada lançamento (Popen, sem invólucro) no log
import sys, os, time, subprocess, shlex
PISO_MB = 600.0              # reserva para a oscilação do resto da máquina (navegador variou ~550 MB em 2 min, item 81)
ORCAMENTO_MB = {'soma': 250.0, 'distal': 500.0, 'toy': 100.0,  # pico medido 82–95 MB (somática antiga); 236 MB unidade MIGRADA (item 88) → ~2×
                'ref': 1500.0,                                  # PROVISÓRIO até a medida (células L0 do ref_ii; item 83)
                'hay': 600.0,                                   # Hay L0 Δ0.5 na unidade: pico MEDIDO 305 MB (item 93) × ~2
                'teste_fechada': 1e9}                           # item 123: SÓ para testar a recusa (porta sempre fechada)
MAX_SIM = 5
NAO_SIM = (b'tol_vigia', b'etapaA_fila', b'mem_gate', b'mem_sample', b'lancar', b'hanu_supervisor')   # supervisores: não simulam
SWAPIN_MAX = 50.0            # páginas/s
JANELA_S = 60.0
CADA_S = 300.0


def avail():
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1024.0


def swapin_rate():
    v = lambda: next(int(l.split()[1]) for l in open('/proc/vmstat') if l.startswith('pswpin'))
    a = v(); time.sleep(JANELA_S); return (v() - a) / JANELA_S


def running_sims():
    """Simulações pesadas RODANDO (estado ≠ T): processos do .nrnvenv com um script de simulação do neuron/ (só CONTA —
    parar/retomar é sempre pelo PID gravado)."""
    info = {}
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        try:
            c = open('/proc/%s/cmdline' % p, 'rb').read().split(b'\0'); f = open('/proc/%s/stat' % p).read().rsplit(')', 1)[1].split()
        except Exception: continue
        info[p] = (c, f[0], f[1])
    parents = {v[2] for v in info.values()}                  # invólucros (re-execução sob systemd-inhibit) têm filho: não contam
    return sum(1 for p, (c, st, pp) in info.items() if p not in parents and c and c[0].endswith(b'.nrnvenv/bin/python')
               and len(c) > 1 and c[1].startswith(b'neuron/') and b'toy' not in c and st != 'T'
               and not any(x in c[1] for x in NAO_SIM))


def check(tipo):
    r = swapin_rate(); a = avail(); b = ORCAMENTO_MB[tipo]; n = running_sims()
    ok = a - b >= PISO_MB and r <= SWAPIN_MAX and (tipo == 'toy' or n < MAX_SIM)
    return ok, 'disponível %.0f MB − orçamento %.0f = %.0f (piso %.0f) | swap-in %.1f pg/s (máx %.0f) | simulações rodando %d (máx %d) → %s' % (
        a, b, a - b, PISO_MB, r, SWAPIN_MAX, n, MAX_SIM, 'PODE LANÇAR' if ok else 'NÃO LANÇAR')


if __name__ == '__main__':
    if sys.argv[1] == 'check':
        ok, msg = check(sys.argv[2]); print(msg); sys.exit(0 if ok else 1)
    tipo, cmds, log = sys.argv[2:5]
    import lancar as LA                                    # item 123 (4): cada linha pelo PONTO ÚNICO (confere a porta; recusa se fechada)
    L = open(log, 'a')
    for line in [l.strip() for l in open(cmds) if l.strip() and not l.startswith('#')]:
        out = shlex.split(line)
        while True:
            p = LA.via_porta(tipo, out[:-2] if out[-2] == '>' else out, stdout=open(out[-1], 'a') if out[-2] == '>' else None,
                             stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
            if p is not None: break
            L.write('%s porta FECHADA (results/porta/lancamentos.log) — reconfere em %.0f s\n' % (time.strftime('%F %T'), CADA_S)); L.flush()
            time.sleep(CADA_S)
        L.write('%s LANÇADO pid %d: %s\n' % (time.strftime('%F %T'), p.pid, line)); L.flush()
        time.sleep(CADA_S)    # deixa o processo novo chegar ao regime antes de reconferir o portão
