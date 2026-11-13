# D132 item 163: PONTO FIXO EM TODOS OS DESENHOS + CURVATURA EM v_3 POR PROTOCOLO pela fila do supervisor (gera os TRABALHOS; o que roda NÃO é tocado).
# (a) Iteração do ponto fixo — UMA função para todos os desenhos (piloto-6, lotes 1, 2, 3): passo r (etapaA_ponto_fixo) → funcional ao longo das candidatas
#     (G em K sub-trabalhadores; base reaproveitada) → Fdir → a MESMA análise do desenho com os Fdir de todas as rodadas → passo r+1 … até PONTO_FIXO.json.
#     r_max = 3 rodadas de simulação. Teto de avaliações do funcional: piloto 4 + lote 1 2 = 6 (~10 h; o limite de ~12 h do item 163 não comporta mais
#     nenhuma direção → uma rodada extra PARA e espera a decisão); lotes 2 e 3: 7 cada (~11.7 h).
# (b) Lotes 2 e 3: a avaliação da parada passa a comparar os PONTO_FIXO.json (declarado no item 163, antes de o lote 2 terminar).
# (c) Curvatura em v_3 por protocolo: repousos (cache) → vrest → v_3 ± nas 5 unidades do piloto → acumulados POR PROTOCOLO → etapaA_curv_protocolo.
# Os trabalhos de (a) para piloto/lote 1 e (c) entram ANTES de lt2_dirs (prioridade sobre as próximas etapas do lote 2; nada do lote 2 é interrompido).
import json, os
f='neuron/results/supervisor/TRABALHOS.json'; J=json.load(open(f)); L='neuron/results/etapaA_lotes'; P='neuron/results/etapaA_pcond'; C='neuron/results/etapaA_conf'
py='.nrnvenv/bin/python'; HAY='.cache/hay/139653-master'; GF='neuron/results/etapaA_G8/G.npz'; CA=C+'/cache_1e-8'; SOMA=C+'/soma64_1e-8/p_soma'
assert not any(j['nome'].startswith(('pf_', 'c3_')) for j in J)
PC=['g_apic[60]_32','g_apic[36]_16','g_apic[9]_16','g_apic[44]_48','g_apic[64]_48']
job=lambda n: next(j for j in J if j['nome'] == n)


def troca(argv, fdirs, saida):
    """A MESMA linha de análise do desenho, só com os Fdir (todas as rodadas) e a saída trocados."""
    a=list(argv); a[a.index('--fdir')+1]=','.join(fdirs); a[a.index('--analise')+2]=saida; return a


def pf(rot, R, AN0, CJ, an_argv, teto, rmax=3, K=4):
    FZ, FD0, GD0, PF = R+'/direcoes.npz', R+'/Fdir.json', R+'/Gdir/G', R+'/pf'; os.makedirs(PF, exist_ok=True); out=[]
    for r in range(1, rmax+2):
        AN = AN0 if r == 1 else PF+'/analise_%d.json' % (r-1); FDs=[FD0]+[PF+'/Fdir_%d.json' % i for i in range(1, r)]
        out.append(dict(nome='pf_%s_passo%d' % (rot,r), tipo='toy', argv=[py,'neuron/etapaA_ponto_fixo.py',FZ,AN,CJ,','.join(FDs),str(r),str(rmax),str(teto),GD0,PF],
                        saida=PF+'/passo_%d.log' % r, requer=[AN]+FDs, feito=[PF+'/passo_%d.json' % r]))
        if r > rmax: break
        GD, FZr = PF+'/Gdir_%d' % r, PF+'/dirF_%d.npz' % r
        for k in range(K):
            out.append(dict(nome='pf_%s_G%d_s%d' % (rot,r,k), tipo='distal', argv=[py,'neuron/etapaA_runner.py','G',GD,'--hay',HAY,'--atol','1e-8','--cache','neuron/results/etapaA_G8/cache',
                            '--direcoes',FZr,'--sub-worker','%d/%d' % (k,K)], saida=PF+'/Gdir_%d_s%d.log' % (r,k), dir=GD, requer=[FZr], feito=[GD+'/G.npz']))
        out.append(dict(nome='pf_%s_Fdir%d' % (rot,r), tipo='toy', argv=[py,'neuron/etapaA_Fdir.py',GD,FZr,PF+'/Fdir_%d.json' % r], saida=PF+'/Fdir_%d.log' % r,
                        requer=[GD+'/G.npz'], feito=[PF+'/Fdir_%d.json' % r]))
        out.append(dict(nome='pf_%s_an%d' % (rot,r), tipo='distal', argv=troca(an_argv, FDs+[PF+'/Fdir_%d.json' % r], PF+'/analise_%d.json' % r), saida=PF+'/analise_%d.log' % r,
                        requer=[PF+'/Fdir_%d.json' % r], feito=[PF+'/analise_%d.json' % r]))
    return out


# (c) curvatura em v_3 por protocolo
CV=L+'/lote1/curv_v3'; FZ3=CV+'/direcoes_v3.npz'; c3=[]
c3.append(dict(nome='c3_rep', tipo='distal', argv=[py,'neuron/etapaA_repousos.py',HAY,CA,FZ3,'0/1',CV+'/repousos.json'], saida=CV+'/repousos.log', requer=[FZ3], feito=[CV+'/repousos.json']))
c3.append(dict(nome='c3_vrest', tipo='distal', argv=[py,'neuron/etapaA_vrest.py',HAY,CA,CV+'/vrest.npz','c3='+FZ3], saida=CV+'/vrest.log', requer=[CV+'/repousos.json'], feito=[CV+'/vrest.npz']))
c3d, c3a = [], []
for p in PC:
    D=CV+'/dirs_'+p; TH=P+'/unid_%s/p_%s' % (p,p)
    c3d.append(dict(nome='c3_dir_%s' % p, tipo='distal', argv=[py,'neuron/etapaA_runner.py','unit',D,'--hay',HAY,'--only',p,'--atol','1e-8','--cache',CA,'--direcoes',FZ3,
                    '--amplitudes',L+'/lote1/amplitudes.json'], saida=D+'.log', dir=D, requer=[FZ3, CV+'/repousos.json'], feito=[D+'/p_%s.npz' % p]))
    c3a.append(dict(nome='c3_acc_%s' % p, tipo='distal', argv=[py,'neuron/etapaA_piloto.py',GF,'--soma',SOMA,'--distal','%s=%s=%s/p_%s' % (p,TH,D,p),'--vrest',CV+'/vrest.npz',
                    '--dirtag','c3','--acumular',p,FZ3,CV+'/acc_'+p,'--por-protocolo'], saida=CV+'/acc_%s.log' % p, requer=[D+'/p_%s.npz' % p, CV+'/vrest.npz'], feito=[CV+'/acc_%s.ok.json' % p]))
c3an=dict(nome='c3_an', tipo='toy', argv=[py,'neuron/etapaA_curv_protocolo.py',CV+'/curv_protocolo.json'], saida=CV+'/curv_protocolo.log',
          requer=[CV+'/acc_%s.ok.json' % p for p in PC], feito=[CV+'/curv_protocolo.json'])

# (a) piloto-6 e lote 1
pil=pf('pil', P, L+'/regr154/piloto_fis.json', '6inj', job('rg154_an_fis')['argv'], teto=4)
l1=pf('l1', L+'/lote1', L+'/lote1/piloto_fis.json', 'acum', job('lt1_an_fis')['argv'], teto=2)
passos1=[j for j in pil+l1 if j['nome'].endswith('_passo1')]; Gs1=[j for j in l1+pil if '_G1_' in j['nome']]
resto=[j for j in pil+l1 if j not in passos1 and j not in Gs1]
NOVOS=passos1+c3+c3d+Gs1+c3a+[c3an]+resto
i=[j['nome'] for j in J].index('lt2_dirs'); J[i:i]=NOVOS

# (b) lotes 2 e 3: iteração depois da análise; a parada compara os PONTO_FIXO.json
for b in (2, 3):
    R=L+'/lote%d' % b; ch=pf('l%d' % b, R, R+'/piloto_fis.json', 'acum', job('lt%d_an_fis' % b)['argv'], teto=7)
    REF=L+'/lote%d/pf/PONTO_FIXO.json' % (b-1); av=job('lt%d_aval' % b)
    av['argv']=[py,'neuron/etapaA_lote_aval.py',R+'/pf/PONTO_FIXO.json','acum',REF,'acum',R,'lote %d (ponto fixo)' % b]
    av['requer']=av['requer']+[R+'/pf/PONTO_FIXO.json', REF]
    i=[j['nome'] for j in J].index('lt%d_aval' % b); J[i:i]=ch
json.dump(J, open(f+'.tmp','w'), indent=1, ensure_ascii=False); os.replace(f+'.tmp', f)
print('item 163: %d trabalhos novos (piloto/lote 1 + curvatura: %d; lotes 2 e 3: %d); lt2_aval e lt3_aval comparam no PONTO FIXO' % (
      sum(1 for j in J if j['nome'].startswith(('pf_', 'c3_'))), len(NOVOS), sum(1 for j in J if j['nome'].startswith(('pf_l2', 'pf_l3')))))
