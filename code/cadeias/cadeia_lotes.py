# D132 itens 151/154: a cadeia dos 3 LOTES da Etapa A em s = 400 pela fila do supervisor (gera os TRABALHOS). Lote 1 REQUER a regressão do item 154
# (regr154_ok.json); lote b ≥ 2 REQUER lote(b−1)/SEGUIR.json (regra de parada) + o arquivo frio/apagamento aprovado antes dele; todo lote começa pela
# GUARDA DE DISCO. Por unidade: rodada de direções → acumulados (com e sem a faixa) gravados e conferidos → apagamento dos traços daquela rodada.
import json, os
f='neuron/results/supervisor/TRABALHOS.json'; J=json.load(open(f)); L='neuron/results/etapaA_lotes'; P='neuron/results/etapaA_pcond'; C='neuron/results/etapaA_conf'
py='.nrnvenv/bin/python'; HAY='.cache/hay/139653-master'; GF='neuron/results/etapaA_G8/G.npz'; CA=C+'/cache_1e-8'; SOMA=C+'/soma64_1e-8/p_soma'
assert not any(j['nome'].startswith('lt') for j in J)
LT=json.load(open(L+'/lotes.json'))['lotes']; RED=['g_apic[35]_16','g_apic[41]_48']                  # item 154 (5): redundantes FORA
LOTES=[LT[0], LT[1], [p for p in LT[2] if p not in RED]]; assert len(LOTES[2]) == 3
PC=['g_apic[60]_32','g_apic[36]_16','g_apic[9]_16','g_apic[44]_48','g_apic[64]_48']
dono={p: 0 for p in PC}; dono.update({p: b + 1 for b, l in enumerate(LOTES) for p in l})
theta=lambda p: P+'/unid_%s/p_%s' % (p,p) if dono[p] == 0 else L+'/lote%d/unid_%s/p_%s' % (dono[p],p,p)
NEC={1: 63.5, 2: 63.5, 3: 53.0}                                       # GiB: θ novos (5.3 cada) + 5 rodadas em voo (5.4) + margem 10
def add(**k): J.append(k)
for b in (1, 2, 3):
    R=L+'/lote%d' % b; os.makedirs(R, exist_ok=True); NEW=LOTES[b-1]; ACC=PC+[p for l in LOTES[:b] for p in l]; tag='l%d' % b
    prev=[L+'/regr154/regr154_ok.json'] if b == 1 else [L+'/lote%d/SEGUIR.json' % (b-1), L+('/frio_pcond_dirs.txt.ok.json' if b == 2 else '/frio_migr64.txt.ok.json')]
    amp_ant=P+'/amplitudes.json' if b == 1 else L+'/lote%d/amplitudes.json' % (b-1)
    ref=(P+'/piloto_fis.json','6inj') if b == 1 else (L+'/lote%d/piloto_fis.json' % (b-1),'acum')
    OK=R+'/condicionamento_ok.json'; REP=[R+'/repousos_s%d.json' % k for k in range(5)]
    add(nome='lt%d_disco' % b, tipo='toy', argv=[py,'neuron/etapaA_disco_guarda.py',R+'/disco_ok.json','%g' % NEC[b],'lote %d' % b], saida=R+'/disco.log', requer=prev, feito=[R+'/disco_ok.json'])
    for p in NEW:
        add(nome='lt%d_cond_%s' % (b,p), tipo='distal', argv=[py,'neuron/etapaA_condiciona.py',HAY,CA,p,R+'/cond_%s.json' % p], saida=R+'/cond_%s.log' % p,
            requer=[R+'/disco_ok.json'], feito=[R+'/cond_%s.json' % p])
    add(nome='lt%d_condaval' % b, tipo='toy', argv=[py,'neuron/etapaA_condiciona_lote.py',R,','.join(NEW),amp_ant], saida=R+'/condicionamento.log',
        requer=[R+'/cond_%s.json' % p for p in NEW]+([amp_ant] if b > 1 else []), feito=[R+'/condicionamento.json'])
    for p in NEW:
        D=R+'/unid_'+p
        add(nome='lt%d_u_%s' % (b,p), tipo='distal', argv=[py,'neuron/etapaA_runner.py','unit',D,'--hay',HAY,'--only',p,'--so-theta','--atol','1e-8','--cache',CA,'--amplitudes',R+'/amplitudes.json'],
            saida=D+'.log', dir=D, requer=[OK], feito=[D+'/p_%s.npz' % p])
    add(nome='lt%d_dirs' % b, tipo='distal', argv=[py,'neuron/etapaA_piloto.py',GF,'--distal',','.join('%s=%s' % (p,theta(p)) for p in ACC),'--soma',SOMA,'--direcoes',R+'/direcoes.npz',R+'/dirF.npz'],
        saida=R+'/dirs.log', requer=[OK]+[theta(p)+'.npz' for p in ACC], feito=[R+'/direcoes.npz'])
    for k in range(5):
        add(nome='lt%d_rep_s%d' % (b,k), tipo='distal', argv=[py,'neuron/etapaA_repousos.py',HAY,CA,R+'/direcoes.npz','%d/5' % k,REP[k]], saida=R+'/repousos_s%d.log' % k,
            requer=[R+'/direcoes.npz'], feito=[REP[k]])
    add(nome='lt%d_vrest' % b, tipo='distal', argv=[py,'neuron/etapaA_vrest.py',HAY,CA,R+'/vrest.npz','%s=%s' % (tag,R+'/direcoes.npz')], saida=R+'/vrest.log', requer=REP, feito=[R+'/vrest.npz'])
    base=[py,'neuron/etapaA_piloto.py',GF,'--soma',SOMA]
    add(nome='lt%d_acc_soma' % b, tipo='distal', argv=base+['--vrest',R+'/vrest.npz','--dirtag',tag,'--acumular','soma',R+'/direcoes.npz',R+'/acc_soma'],
        saida=R+'/acc_soma.log', requer=[R+'/vrest.npz'], feito=[R+'/acc_soma.ok.json'])
    for p in ACC:
        D=R+'/dirs_'+p
        add(nome='lt%d_dir_%s' % (b,p), tipo='distal', argv=[py,'neuron/etapaA_runner.py','unit',D,'--hay',HAY,'--only',p,'--atol','1e-8','--cache',CA,'--direcoes',R+'/direcoes.npz',
            '--amplitudes',R+'/amplitudes.json'], saida=D+'.log', dir=D, requer=[R+'/direcoes.npz']+REP, feito=[D+'/p_%s.npz' % p])
        add(nome='lt%d_acc_%s' % (b,p), tipo='distal', argv=base+['--distal','%s=%s=%s/p_%s' % (p,theta(p),D,p),'--vrest',R+'/vrest.npz','--dirtag',tag,
            '--acumular',p,R+'/direcoes.npz',R+'/acc_'+p,'--apagar-direcoes'], saida=R+'/acc_%s.log' % p,
            requer=[D+'/p_%s.npz' % p, R+'/vrest.npz', L+'/regr154/regr154_ok.json'], feito=[R+'/acc_%s.ok.json' % p])
    for k in range(5):
        add(nome='lt%d_Gdir_s%d' % (b,k), tipo='distal', argv=[py,'neuron/etapaA_runner.py','G',R+'/Gdir','--hay',HAY,'--atol','1e-8','--cache','neuron/results/etapaA_G8/cache',
            '--direcoes',R+'/dirF.npz','--sub-worker','%d/5' % k], saida=R+'/Gdir_s%d.log' % k, dir=R+'/Gdir', requer=[R+'/dirF.npz'], feito=[R+'/Gdir/G.npz'])
    add(nome='lt%d_Fdir' % b, tipo='toy', argv=[py,'neuron/etapaA_Fdir.py',R+'/Gdir',R+'/dirF.npz',R+'/Fdir.json'], saida=R+'/Fdir.log', requer=[R+'/Gdir/G.npz'], feito=[R+'/Fdir.json'])
    lst=','.join('%s=%s/acc_%s' % (p,R,p) for p in ACC)+',soma=%s/acc_soma' % R; accok=[R+'/acc_%s.ok.json' % p for p in ACC]+[R+'/acc_soma.ok.json']
    for v in ('fis','inf'):
        add(nome='lt%d_an_%s' % (b,v), tipo='distal', argv=base+['--analise',R+'/direcoes.npz',R+'/piloto_%s.json' % v,'--fdir',R+'/Fdir.json','--conjuntos','acum='+','.join(ACC),
            '--acumulados',lst,'--variante',v]+(['--grams',R+'/grams_inf.npz'] if v == 'inf' else []), saida=R+'/piloto_%s.log' % v,
            requer=[R+'/Fdir.json']+accok, feito=[R+'/piloto_%s.json' % v]+([R+'/grams_inf.npz'] if v == 'inf' else []))
    add(nome='lt%d_soma' % b, tipo='distal', argv=base+['--so-soma','--analise',R+'/direcoes.npz',R+'/soma_fis.json','--fdir',R+'/Fdir.json','--conjuntos','soma=',
        '--vrest',R+'/vrest.npz','--faixa','-110,60','--dirtag',tag], saida=R+'/soma_fis.log', requer=[R+'/Fdir.json',R+'/vrest.npz'], feito=[R+'/soma_fis.json'])
    add(nome='lt%d_piso' % b, tipo='toy', argv=[py,'neuron/etapaA_piso_cond.py',R+'/grams_inf.npz',R+'/direcoes.npz',C+'/comb64_v123_grams.npz',R+'/amplitudes.json',R+'/piso.json'],
        saida=R+'/piso.log', requer=[R+'/grams_inf.npz'], feito=[R+'/piso.json'])
    add(nome='lt%d_aval' % b, tipo='toy', argv=[py,'neuron/etapaA_lote_aval.py',R+'/piloto_fis.json','acum',ref[0],ref[1],R,'lote %d' % b], saida=R+'/aval.log',
        requer=[R+'/piloto_fis.json',R+'/piloto_inf.json',R+'/soma_fis.json',R+'/piso.json'], feito=[R+'/relatorio.txt'])
    if b == 1:
        add(nome='lt_frio_pcond', tipo='toy', argv=[py,'neuron/etapaA_arquivo_frio.py','--esperar-hd','12','etapaA_pcond_dirs',L+'/frio_pcond_dirs.txt']+[P+'/dirs_'+p for p in PC],
            saida=L+'/frio_pcond_dirs.log', requer=[L+'/lote1/SEGUIR.json', L+'/hd_pronto.json'], feito=[L+'/frio_pcond_dirs.txt.ok.json'])
    if b == 2:
        add(nome='lt_frio_migr64', tipo='toy', argv=[py,'neuron/etapaA_arquivo_frio.py','--esperar-hd','12','etapaA_conf_migr64',L+'/frio_migr64.txt',C+'/migr64_1e-6',C+'/migr64_1e-10'],
            saida=L+'/frio_migr64.log', requer=[L+'/lote2/SEGUIR.json', L+'/hd_pronto.json'], feito=[L+'/frio_migr64.txt.ok.json'])
json.dump(J, open(f+'.tmp','w'), indent=1, ensure_ascii=False); os.replace(f+'.tmp', f)
print('cadeia dos lotes: %d trabalhos (lotes %s)' % (sum(1 for j in J if j['nome'].startswith('lt')), [len(l) for l in LOTES]))
