# lancar.py — D132 item 123 (4): PONTO ÚNICO DE LANÇAMENTO de qualquer processo do harness (simulação, análise, diagnóstico "leve").
# Confere a porta de memória (mem_gate.check(<tipo>), a mesma regra dos itens 81/83) e:
#   FECHADA → NÃO lança: sai com código 75 (ou, com --esperar, reconfere a cada mem_gate.CADA_S até abrir);
#   ABERTA  → grava HANU_PORTA = o próprio PID e faz exec do comando (o PID não muda: é o PID do processo lançado).
# Todo lançamento fica em results/porta/lancamentos.log. Os módulos do harness (porta.py) recusam processos que não descendem de um
# lançamento por aqui — um `check; comando` deixa de ser possível.
# Uso: python3 neuron/lancar.py <tipo> [--esperar] -- <comando> [args...]
import sys, os, time
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import mem_gate as MG

LOG = os.path.join(AQUI, 'results', 'porta', 'lancamentos.log')


RECUSA = 75                     # porta fechada (a guarda porta.py usa 77: lançado por fora)


def via_porta(tipo, cmd, **popen_kw):
    """Para FILAS (supervisor, mem_gate fila, etapaA_fila, preempcao): abre `lancar.py <tipo> -- cmd` e só volta quando o lançador
    fez o exec (→ Popen do processo lançado: o PID é o mesmo) ou recusou (→ None). Assim uma fila nunca deixa vários lançamentos esperando
    a porta ao mesmo tempo."""
    import subprocess
    p = subprocess.Popen(['/usr/bin/python3', os.path.join(AQUI, 'lancar.py'), tipo, '--'] + list(cmd), **popen_kw)
    while True:
        rc = p.poll()
        if rc is not None: return None if rc == RECUSA else p
        try: cl = open('/proc/%d/cmdline' % p.pid, 'rb').read()
        except OSError: cl = b''
        if cl and b'lancar.py' not in cl: return p            # cmdline VAZIO = processo saindo (zumbi): volta ao poll (19/10: lido como exec)
        time.sleep(0.5)


def registra(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'a') as f: f.write('%s pid %d %s\n' % (time.strftime('%F %T'), os.getpid(), msg))


if __name__ == '__main__':
    if '--' not in sys.argv or sys.argv.index('--') < 2: sys.exit('uso: lancar.py <tipo> [--esperar] -- <comando> [args...]')
    i = sys.argv.index('--'); tipo = sys.argv[1]; esperar = '--esperar' in sys.argv[2:i]; cmd = sys.argv[i + 1:]
    if tipo not in MG.ORCAMENTO_MB: sys.exit('tipo desconhecido: %s (tipos: %s)' % (tipo, sorted(MG.ORCAMENTO_MB)))
    while True:
        ok, msg = MG.check(tipo)
        if ok: break
        registra('PORTA FECHADA [%s] %s | %s' % (tipo, msg, ' '.join(cmd)))
        if not esperar:
            sys.stderr.write('PORTA FECHADA — NÃO LANÇADO: %s\n' % msg); sys.exit(RECUSA)
        time.sleep(MG.CADA_S)
    registra('LANÇADO [%s] %s | %s' % (tipo, msg, ' '.join(cmd)))
    os.environ['HANU_PORTA'] = str(os.getpid()); sys.stdout.flush(); sys.stderr.flush()
    os.execvp(cmd[0], cmd)
