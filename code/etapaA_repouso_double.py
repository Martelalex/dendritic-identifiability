# etapaA_repouso_double.py — prompt 0007 (3c): REMEDIDA DO ARTEFATO DO REPOUSO EM DUPLA PRECISÃO (o "[To re-measure]" da seção 3.5 do preprint).
# A MESMA comparação do diagnóstico do item 88/91 (etapaA_porte_check.py): repouso de 3 s a passo fixo (o antigo) × repouso CONVERGIDO, no MESMO caminho de
# código (CommonSim; EtapaAUnit.protocols, que desde o item 101 grava em float64), unidade p_g_apic[60]_32, subpasso 'base', M1 (M1m + M1p) e M4, regra da
# cadeia de medida (etapaA_unit.cadeia). Piso em DUPLA precisão (antes era o passo do float32): piso(X) = máx |y_conv(X) − y_conv(X/100)|.
# Reporta, para X = 10⁻⁶ e 10⁻⁸: máx |y_conv(X) − y_3s(X)| (com e sem a leitura do ponto de injeção), o piso e a razão.
# Uso: python3 neuron/lancar.py distal -- .nrnvenv/bin/python neuron/etapaA_repouso_double.py <dir do Hay> <saída> --cache <dir>
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neuron import h
import etapaA_unit as EU

hay, out = [os.path.abspath(a) for a in sys.argv[1:3]]
cache = os.path.abspath(sys.argv[sys.argv.index('--cache') + 1]) if '--cache' in sys.argv else None
P, U = 'g_apic[60]_32', 'p_g_apic[60]_32'; os.makedirs(out, exist_ok=True); t0 = time.time()
unit = EU.EtapaAUnit(hay, only=[P], atol=1e-8, cache_dir=cache); unit._apply(U, 'base')
info = unit._sim(U); C = unit.C; I = C.inj
print('CommonSim (repouso convergido): %s (%.0f s)' % (info, time.time() - t0), flush=True)
f_conv, f_old = os.path.join(out, 'repouso_convergido.dat'), os.path.join(out, 'repouso_3s.dat')
I.save_state(f_conv)
h.cvode_active(0); h.dt = 0.1; h.finitialize(-80.0); h.continuerun(3000.0)            # o repouso ANTIGO (3 s a passo fixo 0.1 ms)
I.ss = h.SaveState(); I.ss.save(); I.TS = h.t; I.v_rest = I.rec_seg.v; I.rest_ms = 3000.0; I.save_state(f_old)
print('repouso de 3 s: V soma %.9f mV (%.0f s)' % (I.v_rest, time.time() - t0), flush=True)
i_inj = unit.read.index(P); res = {'repouso_construcao': info, 'leitura_injecao': i_inj}
for X in (1e-6, 1e-8, 1e-10):
    C.atol = X
    for tag, f in (('convergido', f_conv), ('repouso_3s', f_old)):
        if tag == 'repouso_3s' and X == 1e-10: continue                 # o piso só precisa do convergido a X/100
        d = os.path.join(out, '%s_%g' % (tag, X)); os.makedirs(d, exist_ok=True)
        t1 = time.time(); I.load_state(f); I.ok = True; unit.protocols(U, 'base', d, 1.0)
        print('X = %g, %s: protocolos em %.0f s' % (X, tag, time.time() - t1), flush=True)
ld = lambda tag, X, l: EU.cadeia(np.load(os.path.join(out, '%s_%g' % (tag, X), 'base.%s.npy' % l)), l)
for X in (1e-6, 1e-8):
    r = {}
    for fam, labs in (('M1', ('M1m', 'M1p')), ('M4', ('M4',))):
        piso = max(float(np.abs(ld('convergido', X, l) - ld('convergido', X / 100, l)).max()) for l in labs)
        dif = max(float(np.abs(ld('convergido', X, l) - ld('repouso_3s', X, l)).max()) for l in labs)
        dif_sem = max(float(np.abs(np.delete(ld('convergido', X, l), i_inj, axis=0) - np.delete(ld('repouso_3s', X, l), i_inj, axis=0)).max()) if l != 'M4' else
                      float(np.abs(ld('convergido', X, l) - ld('repouso_3s', X, l)).max()) for l in labs)
        r[fam] = {'piso_double_mV': piso, 'dif_repouso_mV': dif, 'dif_repouso_sem_injecao_mV': dif_sem, 'razao_piso': dif / piso if piso else None}
        print('X = %g %s: piso (double) %.3g mV | repouso convergido × 3 s: %.3g mV (sem a leitura da injeção %.3g) → %.1f× o piso' % (
              X, fam, piso, dif, dif_sem, dif / piso if piso else float('nan')), flush=True)
    res['%g' % X] = r
import resource
res['pico_memoria_MB'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0; res['tempo_s'] = time.time() - t0
json.dump(res, open(os.path.join(out, 'repouso_double.json'), 'w'), indent=1, default=float)
print('FIM (%.0f s, pico %.0f MB)' % (res['tempo_s'], res['pico_memoria_MB']), flush=True)
