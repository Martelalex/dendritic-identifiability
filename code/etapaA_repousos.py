# etapaA_repousos.py — D132 item 146 (lição do item 140: a cache de repousos não tem trava): calcula ANTES, UMA vez, os repousos dos subpassos de
# direção θ·exp(±δ_i v_i) de um arquivo de direções, na cache compartilhada — pelo MESMO caminho das unidades (EtapaAUnit._apply + _sim: chave
# automática do modelo; o repouso não depende do ponto de injeção). PARTIÇÃO DISJUNTA entre processos: o processo k/K faz os subpassos de índice
# ≡ k (mod K) → nenhum repouso é calculado duas vezes. Repouso que falha (AutotestFailed) → registrado (a rodada de direções o marcará NÃO AVALIADO).
# Uso: python3 neuron/lancar.py distal -- .nrnvenv/bin/python neuron/etapaA_repousos.py <dir do Hay> <cache> <direcoes.npz> <k/K> <saida.json>
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_unit as EU
import stim_common as SC

HAY, CACHE, FZ, KK, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3]), sys.argv[4], sys.argv[5]
k, K = (int(x) for x in KK.split('/'))
u = EU.EtapaAUnit(HAY, only=['g_apic[60]_32'], atol=1e-8, cache_dir=CACHE, direcoes=FZ); U = 'p_g_apic[60]_32'
subs = [s for s in u.substeps(U) if s != 'base']; meus = [s for i, s in enumerate(subs) if i % K == k]; res = {}
for sn in meus:
    t0 = time.time(); u._apply(U, sn)
    try: info = u._sim(U)
    except SC.AutotestFailed as e: info = 'FALHOU: %s' % e
    u._restore_geometry(); res[sn] = {'repouso': info, 's': round(time.time() - t0, 1)}
    print('%s: %s (%.0f s)' % (sn, info, time.time() - t0), flush=True)
json.dump({'parte': KK, 'subpassos': res}, open(OUT, 'w'), indent=1)
print('FIM %s: %d repousos (%d falharam)' % (KK, len(res), sum(1 for r in res.values() if str(r['repouso']).startswith('FALHOU'))), flush=True)
