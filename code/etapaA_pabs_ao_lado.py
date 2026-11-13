# etapaA_pabs_ao_lado.py — D132 itens 166/168: o P-abs AO LADO da regra atual num desenho (candidato — NÃO adotado: o K8 falhou), sem simular. Usa as MESMAS
# funções da proposta (etapaA_relev_abs.no_desenho); conferência K4: com ε = 0 reproduz EXATAMENTE o certificado do PONTO_FIXO.json do desenho.
# Uso: python3 neuron/lancar.py toy --esperar -- .nrnvenv/bin/python neuron/etapaA_pabs_ao_lado.py <rótulo> <dir do desenho> <conjunto> <membros a,b,…> <saida.json>
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etapaA_relevancia_caburst as RC
import etapaA_relev_abs as PA

ROT, DD, CJ, MEM, OUT = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3], sys.argv[4].split(','), sys.argv[5]
D = RC.desenho(ROT, DD, DD, MEM); out = {'rotulo': ROT, 'eps': PA.EPS, 'nota': 'candidato — NÃO adotado (K8 falhou, item 166); termos cruzados não medidos', 'ruidos': {}}
for t in RC.TAUS:
    s0 = PA.no_desenho(D, t, 0.0)[0]; sc, quem, det, e = PA.no_desenho(D, t, PA.EPS); hoje = D['PF']['conjuntos'][CJ][t]
    assert s0 == hoje['certificado'], ('K4 falhou: ε = 0 não reproduz o certificado', t, s0, hoje['certificado'])
    out['ruidos'][t] = {'hoje': hoje['certificado'], 'p_abs': sc, 'p_abs_limita': quem}
    print('%-9s hoje %.4g (σ* %.4g, σ_lin %.4g v_%s) | P-abs (candidato, NÃO adotado) %.4g (%s)' % (RC.nm(t), hoje['certificado'], hoje['sigma_estrela'], hoje['sigma_lin'], hoje['v_lin'], sc, quem), flush=True)
json.dump(out, open(OUT, 'w'), indent=1)
