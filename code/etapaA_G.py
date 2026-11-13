# etapaA_G.py — D132 item 69 (2a) / 85 / 95: G = ∂F/∂log θ (diferença central, passo 1%) no modelo direto.
# F COMPLETO: EPSP somático nos 48 sítios + 1º PA (BAC 2º, CaBurst 1º) + pico do Ca + TAXA CONTÍNUA DA f-I (item 95):
# taxa_K = K / (t_{K+1} − t_1), K = contagem na BASE − 2 por amplitude (0.78 / 1.0 / 1.9 nA) — gravado no G (K_amps,
# K_vals) e usado igual no termo direto do viés. Vetor pela MESMA função do termo de viés (etapaA_F.fvec).
# CONDICIONAMENTO (declarado): 1º PA — a contagem de PA (BAC/CaBurst) é a MESMA em todos os subpassos; taxa — os K+1
# primeiros disparos existem e mantêm a IDENTIDADE (etapaA_F.identidade) em todos os subpassos (θ ± h, 30 parâmetros);
# senão a grandeza sai `condicionado = False` → a avaliação do espaçamento dá NÃO AVALIADO nela.
# Código único: um CommonSim por processo, resettle a cada θ. Interface do etapaA_runner: uma unidade 'G'.
import math
import numpy as np
import etapaA_model as EM
import etapaA_F as EF
import stim_common as SC                                             # item 157: SimulacaoAbortada


class GModel:
    def __init__(self, hay, atol=1e-6, cache_dir=None, subpassos=None, direcoes=None):
        self.M = EM.RegionModel(hay, 32, EF.sites); self.atol = atol; self.cache_dir = cache_dir; self.S = None
        self.only_subs = subpassos
        # item 128 (3): F ao longo de direções — npz com V (k × 30) e excursoes (k): subpassos 'dirNN_mais/menos' = θ·exp(±δ_k v_k)
        self.dirs = None if direcoes is None else np.load(direcoes)

    def units(self): return ['G']

    def substeps(self, u):
        if self.dirs is not None: return ['base'] + ['dir%02d_%s' % (k, g) for k in range(len(self.dirs['excursoes'])) for g in ('mais', 'menos')]
        s = ['base'] + ['%s_%s' % (n, sg) for n in EM.THETA_NAMES for sg in ('mais', 'menos')]
        return s if self.only_subs is None else [x for x in s if x in self.only_subs]

    def evaluate(self, u, sname, ud=None):
        th = dict(EM.THETA_TRUE)
        if sname.startswith('dir') and self.dirs is not None:
            k, sg = int(sname[3:5]), sname.rsplit('_', 1)[1]; v = self.dirs['V'][k]; d = float(self.dirs['excursoes'][k])
            for i, n in enumerate(EM.THETA_NAMES): th[n] = th[n] * math.exp((d if sg == 'mais' else -d) * v[i])
        elif sname != 'base':
            n, sg = sname.rsplit('_', 1); th[n] *= 1.01 if sg == 'mais' else 1 / 1.01
        self.M.set_theta(th)
        if self.S is None: self.S = EF.Sim(self.M, atol=self.atol, cache_dir=self.cache_dir)
        else: self.S.C.resettle()
        try: F = EF.functional_set(self.M, log=lambda m: None, fI=True, sim=self.S)
        except SC.SimulacaoAbortada as e:                             # item 157: guarda disparou → NÃO AVALIADO (não trava)
            return {'nao_avaliado': np.array('guarda: %s' % e)}
        v, names, cnt = EF.fvec(F)                                   # sem taxa: a taxa sai na redução (K da base)
        out = {'F': v, 'nomes': names, 'contagens': cnt}
        for a in EF.FI_AMPS: out['picos_%s' % a] = np.array(F['fI'][str(a)]['picos'], float)
        return out

    def reduce(self, u, subs, ud=None):
        if self.only_subs is not None: return {'nota': np.array('subconjunto de verificação — G não montado')}
        if self.dirs is not None: return {'nota': np.array('F ao longo de direções (item 128 (3)) — análise à parte (etapaA_Fdir.py)')}
        return assemble(subs)


def assemble(subs):
    """G a partir dos subpassos (dicionários com F, nomes, contagens, picos_<amp>): K pela regra, taxas contínuas,
    condicionamento. Usado pela redução e pela verificação (etapaA_G_check)."""
    P = EM.THETA_NAMES; b = subs['base']
    K = {str(a): EF.K_regra(len(b['picos_%s' % a])) for a in EF.FI_AMPS}
    def full(sd):
        r = [EF.taxa_K(sd['picos_%s' % a], K[str(a)]) for a in EF.FI_AMPS]
        return np.concatenate([sd['F'], r])
    names = np.concatenate([b['nomes'], ['taxa_%s' % a for a in EF.FI_AMPS]])
    Fs = {s: full(sd) for s, sd in subs.items()}
    P = [n for n in P if '%s_mais' % n in Fs and '%s_menos' % n in Fs]       # só os parâmetros presentes (verificação: o par)
    G = np.stack([(Fs['%s_mais' % n] - Fs['%s_menos' % n]) / (2 * math.log(1.01)) for n in P], axis=1)
    c0 = b['contagens']
    cond_pa = np.array([all(subs[s]['contagens'][i] == c0[i] for s in subs) for i in range(len(c0))])
    ident = {a: [EF.identidade(b['picos_%s' % a], subs[s]['picos_%s' % a], K[str(a)]) for s in subs] for a in EF.FI_AMPS}
    cond_rate = np.array([all(ok for ok, _ in ident[a]) for a in EF.FI_AMPS])
    cond = np.concatenate([cond_pa, cond_rate]) & np.all(np.isfinite(G), axis=1) & np.isfinite(Fs['base'])
    return {'G': G, 'F0': Fs['base'], 'nomes': names, 'condicionado': cond, 'contagens_base': c0,
            'K_amps': np.array([str(a) for a in EF.FI_AMPS]), 'K_vals': np.array([K[str(a)] for a in EF.FI_AMPS]),
            'identidade_pior_razao': np.array([max(r for _, r in ident[a]) for a in EF.FI_AMPS]), 'parametros': np.array(P)}
