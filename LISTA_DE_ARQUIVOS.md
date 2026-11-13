# Lista de arquivos (tamanho em bytes)

- ./.gitignore — 19
- ./CITATION.cff — 375
- ./LICENSE — 1083
- ./LICENSE-DATA — 18657
- ./README.md — 5428
- ./code/cadeias/cadeia_lotes.py — 7798
- ./code/cadeias/cadeia_pf.py — 6396
- ./code/detect_peak.py — 3101
- ./code/etapaA_F.py — 9362
- ./code/etapaA_Fdir.py — 4148
- ./code/etapaA_G.py — 5105
- ./code/etapaA_apagar_teste.py — 4899
- ./code/etapaA_condiciona.py — 17653
- ./code/etapaA_condiciona_lote.py — 2373
- ./code/etapaA_condiciona_teste.py — 9428
- ./code/etapaA_curv_protocolo.py — 8715
- ./code/etapaA_densidade_cond.py — 7544
- ./code/etapaA_disco_guarda.py — 1111
- ./code/etapaA_excluida_teste.py — 3058
- ./code/etapaA_guardas_teste.py — 5524
- ./code/etapaA_k7k8.py — 11769
- ./code/etapaA_lote1_diag.py — 12666
- ./code/etapaA_lote_aval.py — 4687
- ./code/etapaA_lote_aval_teste.py — 2727
- ./code/etapaA_model.py — 12025
- ./code/etapaA_pabs_ao_lado.py — 1521
- ./code/etapaA_piloto.py — 25611
- ./code/etapaA_ponto_fixo.py — 7198
- ./code/etapaA_ponto_fixo_teste.py — 11695
- ./code/etapaA_regr154.py — 1562
- ./code/etapaA_relev_abs.py — 9068
- ./code/etapaA_relevancia_caburst.py — 14442
- ./code/etapaA_repouso_double.py — 3934
- ./code/etapaA_repousos.py — 1817
- ./code/etapaA_runner.py — 15862
- ./code/etapaA_sens_caburst_cond.py — 4257
- ./code/etapaA_sstar.py — 7984
- ./code/etapaA_unit.py — 35222
- ./code/etapaA_vies2.py — 8256
- ./code/etapaA_vrest.py — 2999
- ./code/hay_common.py — 4609
- ./code/l1_lib.py — 10571
- ./code/lancar.py — 2914
- ./code/mem_gate.py — 4858
- ./code/points_lib.py — 3761
- ./code/porta.py — 1398
- ./code/preprint_comum.py — 1355
- ./code/preprint_fig1_morphology_designs.py — 1651
- ./code/preprint_fig2_attenuation.py — 2364
- ./code/preprint_fig3_levels_by_design.py — 1906
- ./code/preprint_fig4_soma_alone.py — 1510
- ./code/preprint_fig5_caburst_tolerance.py — 2374
- ./code/preprint_fig6_artifacts.py — 5085
- ./code/preprint_figuras.py — 992
- ./code/preprint_morfologia.py — 2028
- ./code/ref_ii_C.py — 7949
- ./code/ref_ii_cells.py — 3342
- ./code/results/etapaA_conf/piso64.json — 2567
- ./code/results/etapaA_lotes/lote1/pf/PONTO_FIXO.json — 4531
- ./code/results/etapaA_lotes/lote1/soma_fis.json — 755
- ./code/results/etapaA_lotes/lote2/pf/PONTO_FIXO.json — 5682
- ./code/results/etapaA_lotes/lote2/soma_fis.json — 756
- ./code/results/etapaA_lotes/prompt0001/relevancia_caburst.json — 196518
- ./code/results/etapaA_lotes/prompt0007/repouso_double/repouso_double.json — 947
- ./code/results/etapaA_lotes/prompt0007/sens_caburst/sens_caburst.json — 9524
- ./code/results/etapaA_lotes/prompt0009/repouso_J/valores_singulares.json — 3822
- ./code/results/etapaA_pcond/pf/PONTO_FIXO.json — 4958
- ./code/results/etapaA_pcond/soma_fis.json — 743
- ./code/results/hay/hay_d1.json — 18908
- ./code/results/preprint/morfologia.npz — 207020
- ./code/results/supervisor/TRABALHOS.json — 201060
- ./code/results/target/pyr_aa.json — 4941
- ./code/results/target/pyr_peri.json — 4869
- ./code/stim_common.py — 31583
- ./figures/fig1_morphology_designs.pdf — 133237
- ./figures/fig1_morphology_designs.png — 130283
- ./figures/fig2_attenuation.pdf — 21015
- ./figures/fig2_attenuation.png — 87382
- ./figures/fig3_levels_by_design.pdf — 16359
- ./figures/fig3_levels_by_design.png — 54780
- ./figures/fig4_soma_alone.pdf — 14038
- ./figures/fig4_soma_alone.png — 73108
- ./figures/fig5_caburst_tolerance.pdf — 22337
- ./figures/fig5_caburst_tolerance.png — 109893
- ./figures/fig6_artifacts.pdf — 28302
- ./figures/fig6_artifacts.png — 174033
- ./record/D131_D132_extract.md — 549438
- ./requirements-figures.txt — 150
- ./requirements-simulation.txt — 313

Total: 89 arquivos (mais esta lista), 2.49 MB.

## Notas (prompt 0021, 12/11)
- **Decisões aplicadas:** os 15 itens que estavam em dúvida FICAM e o extrato entra (`record/D131_D132_extract.md`); as menções ao HANU, o nome pessoal e as
  citações a itens internos ficam; o caminho do venv nas linhas de uso dos scripts de figura virou genérico; a fila (`code/results/supervisor/TRABALHOS.json`)
  é só a da Etapa A (238 trabalhos); o supervisor ficou FORA (o README explica como rodar pelo runner, através da porta `code/lancar.py`); LICENSE MIT e
  `CITATION.cff` (o TÍTULO está marcado para o autor confirmar).
- **Varredura:** nenhum segredo, chave, token ou e-mail; nenhum caminho absoluto com o nome do usuário; nenhum arquivo acima de 5 MB. Restam, como CONTEÚDO (não dado
  sensível): o modelo da CPU (i5-8250U) num comentário do `code/mem_gate.py` e no extrato; "Fedora" no extrato; `~/.hanu_pausa` e `~/.venvs/hanu_census313`
  no texto literal do extrato.
- **Figuras:** as 12 (PDF e PNG) saem bit a bit idênticas às do repositório, rodando só a partir desta pasta.

## Notas (prompt 0023, 12/11)
- `code/__pycache__/` saiu (7 `.pyc`: gravavam o caminho absoluto da pasta, com o nome do usuário; tinham nascido da conferência das figuras rodada dentro da
  pasta). Entrou o `.gitignore` (`__pycache__/`, `*.pyc`).
- `CITATION.cff` com o título do preprint e o nome (given "Martel Alexandre", family "Del Colle").
- Varredura de novo, INCLUINDO os binários (`grep -a`; o `.npz` aberto): nenhum caminho absoluto, nome de usuário, e-mail ou token.

## Notas (prompt 0024, 12/11)
- README: status "Released with the preprint" e a linha de requisitos com o SciPy; dois arquivos de versões EXATAS (`requirements-simulation.txt`,
  `requirements-figures.txt`), só com os pacotes que o código importa (conferido pela AST: numpy, neuron, scipy, matplotlib; nenhum faltando).
