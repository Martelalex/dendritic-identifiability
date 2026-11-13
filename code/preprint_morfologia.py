# preprint_morfologia.py — prompt 0007 (3a), figura 2: exporta a morfologia do Hay (cell1.asc; pontos 3D de cada seção), a grade de 400 µm (20 pontos
# candidatos de injeção, âncora no soma) e os pontos de injeção de cada desenho (piloto-6, lote 1, lote 2), para o script das figuras (sem NEURON).
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/preprint_morfologia.py <saida.npz>
import sys, os, json
import numpy as np
AQ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQ)
from neuron import h
import etapaA_model as EM

HAY = os.path.join(os.path.dirname(AQ), '.cache', 'hay', '139653-master'); EM.load(HAY)
cell = h.L5PCtemplate(os.path.join(HAY, 'morphologies', 'cell1.asc'))
secs, xyz = [], []
for s in cell.all:
    n = int(h.n3d(sec=s)); P = np.array([[h.x3d(i, sec=s), h.y3d(i, sec=s), h.z3d(i, sec=s), h.diam3d(i, sec=s), h.arc3d(i, sec=s)] for i in range(n)])
    secs.append(s.name()); xyz.append(P)
def ponto(sec_nome, arc):
    P = xyz[secs.index(sec_nome)]; return [float(np.interp(arc, P[:, 4], P[:, j])) for j in range(3)]
G = EM.grid_points(cell, 400.0); G25 = EM.grid_points(cell, 25.0)
grade = {k: ponto(v['sec'], v['arc']) + [v['dist']] for k, v in G.items()}
L = os.path.join(AQ, 'results', 'etapaA_lotes'); J = json.load(open(os.path.join(AQ, 'results', 'supervisor', 'TRABALHOS.json')))
a = next(j for j in J if j['nome'] == 'lt2_an_fis')['argv']; M2 = a[a.index('--conjuntos') + 1].split('=')[1].split(',')
inj = {'piloto-6': M2[:5], 'lote 1': M2[:10], 'lote 2': M2}
pos = {p: ponto(G25[p]['sec'], G25[p]['arc']) for p in M2}
np.savez(sys.argv[1], secs=np.array(secs), xyz=np.array(xyz, dtype=object), grade_nomes=np.array(list(grade)), grade=np.array(list(grade.values())),
         inj_json=np.array(json.dumps({'desenhos': inj, 'pos': pos})), soma=np.array(ponto(cell.soma[0].name(), cell.soma[0].L / 2)))
print('morfologia: %d seções; grade 400 µm: %d pontos; injeções: %s' % (len(secs), len(grade), {k: len(v) for k, v in inj.items()}))
