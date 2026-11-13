# porta.py — D132 item 123 (4): A PORTA DE MEMÓRIA EM CÓDIGO. Importado (na 1ª linha útil) por etapaA_model, stim_common e etapaA_runner —
# portanto por todo processo pesado do harness e por todo diagnóstico que lê/simula com eles. Na importação, RECUSA o processo (SystemExit)
# se ele não descende de um lançamento feito pelo PONTO ÚNICO `neuron/lancar.py` (que conferiu a porta e gravou HANU_PORTA = o próprio PID
# antes do exec): HANU_PORTA tem de ser o PID deste processo ou de um ANCESTRAL (o runner re-executado sob o inibidor e os passos de um
# script lançado pela porta descendem do lançado; um valor herdado de um shell, de outro lançamento, ou forjado não é ancestral).
import os, sys


def _ancestrais(pid):
    out = []
    while pid > 1 and len(out) < 64:
        out.append(pid)
        try: pid = int(open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()[1])
        except Exception: break
    return out


def conferir():
    v = os.environ.get('HANU_PORTA', '')
    if v.isdigit() and int(v) in _ancestrais(os.getpid()): return int(v)
    sys.stderr.write('RECUSADO pela porta (D132 item 123): processo do harness lançado POR FORA do ponto único — use\n'
                     '  python3 neuron/lancar.py <tipo> [--esperar] -- <comando>   (HANU_PORTA=%r não é ancestral deste processo)\n' % v)
    raise SystemExit(77)


LANCADOR = conferir()
