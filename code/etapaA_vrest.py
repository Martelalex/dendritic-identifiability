# etapaA_vrest.py — D132 item 144 (2): o REPOUSO ABSOLUTO em cada ponto de leitura, para cada θ usado (os traços gravados são DEFLEXÕES — a cadeia de
# medida subtrai o valor pré-estímulo). Sem simular: monta o modelo da unidade (nós nos 503 pontos da grade; o repouso NÃO depende do ponto de injeção — a
# cache é compartilhada), aplica cada θ (base, ±1% por eixo, e as excursões θ·exp(±δ·v) dos arquivos de direções dados), calcula a CHAVE do repouso como o
# CommonSim (model_hash + critério + atol), CARREGA o estado salvo (SaveState) e CONFERE t e V no soma contra os gravados (a mesma checagem do load_state);
# lê V em cada ponto de leitura (o NÓ) e no soma. Saída: npz {tags, V (n_tags × 504, na ordem de EtapaAUnit.read), leituras}; tag = nome do subpasso
# (eixos) ou '<rótulo>:<subpasso>' (direções). Repouso ausente na cache → reportado.
# Uso: python3 neuron/lancar.py distal -- .nrnvenv/bin/python neuron/etapaA_vrest.py <dir do Hay> <cache> <saida.npz> [<rótulo>=<direcoes.npz> …]
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neuron import h
import etapaA_model as EM
import etapaA_unit as EU
import stim_common as SC

HAY, CACHE, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
DIRS = [(a.split('=')[0], os.path.abspath(a.split('=')[1])) for a in sys.argv[4:]]
h.load_file('stdrun.hoc'); h.v_init = -80.0
u = EU.EtapaAUnit(HAY, only=['g_apic[60]_32'], atol=1e-8, cache_dir=CACHE); U = 'p_g_apic[60]_32'
segs = [u.site[k][0][0] for k in u.grid] + [u.M.SOMA]
P = EM.THETA_NAMES; tags, V, falta = [], [], []


def le(tag):
    path = os.path.join(CACHE, SC.state_key(modelo=SC.model_hash(), assentamento=dict(SC.SETTLE), atol=1e-8, partida='v_init') + '.dat')
    if not os.path.exists(path): falta.append(tag); return
    meta = json.load(open(path + '.json')); ss = h.SaveState(); f = h.File(); f.ropen(path); ss.fread(f); f.close()
    h.finitialize(h.v_init); ss.restore(1)
    assert abs(h.t - meta['TS']) < 1e-9 and abs(u.M.SOMA.v - meta['v_rest']) < 1e-9, ('repouso não confere', tag, h.t, meta)
    tags.append(tag); V.append([s.v for s in segs])


for sn in ['base'] + ['%s_%s' % (n, g) for n in P for g in ('mais', 'menos')]:
    u._apply(U, sn); le(sn)
for rot, fz in DIRS:
    z = np.load(fz); u.direcoes = z['V']; u.excursoes = z['excursoes']
    for q in range(len(z['excursoes'])):
        for g in ('mais', 'menos'):
            sn = 'dir%02d_%s' % (q, g); u._apply(U, sn); le('%s:%s' % (rot, sn))
u._restore_geometry()
V = np.array(V); np.savez(OUT, tags=np.array(tags), V=V, leituras=np.array(u.read))
print('repousos lidos e CONFERIDOS (t e V_soma = os gravados): %d; ausentes na cache: %d %s' % (len(tags), len(falta), falta[:6]))
print('V de repouso (base): soma %.2f mV; leituras min %.2f / mediana %.2f / máx %.2f mV; em todos os θ: %.2f a %.2f mV' % (
    V[0, -1], V[0].min(), np.median(V[0]), V[0].max(), V.min(), V.max()))
