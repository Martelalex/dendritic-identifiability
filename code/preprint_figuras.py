# preprint_figuras.py — prompt 0020: roda as SEIS figuras do preprint, uma por script (preprint_fig1_… a preprint_fig6_…), a partir de resultados GRAVADOS
# (sem NEURON), PDF + PNG, rótulos em inglês, numeração pela ordem em que o texto as cita; grava figuras.json (feitas / faltam, com o erro).
# Uso: python3 neuron/preprint_figuras.py <dir de saída>
import sys, os, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1]); feitas, faltam = [], {}
for m in ('preprint_fig1_morphology_designs', 'preprint_fig2_attenuation', 'preprint_fig3_levels_by_design', 'preprint_fig4_soma_alone',
          'preprint_fig5_caburst_tolerance', 'preprint_fig6_artifacts'):
    try: feitas.append(importlib.import_module(m).main(OUT))
    except Exception as e: faltam[m] = repr(e)
json.dump({'feitas': feitas, 'faltam': faltam}, open(os.path.join(OUT, 'figuras.json'), 'w'), indent=1)
print('feitas:', feitas); print('faltam:', faltam)
