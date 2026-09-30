import numpy as np, time
from lib import *
from hawkes import fit
rng=np.random.default_rng(7)
E=events(); M={a:merge_hits(E[a]) for a in ANG}
def surrogate(t,t0,T,Kb=48):
    edges=np.linspace(t0,T,Kb+1); k=np.clip(np.searchsorted(edges,t,side="right")-1,0,Kb-1)
    s=np.empty_like(t)
    for j in range(Kb):
        m=k==j; s[m]=rng.uniform(edges[j],edges[j+1],m.sum())
    return np.sort(s)
print("Surrogate test: events re-drawn uniformly within 48 equal bins of lifetime (keeps slow rate, removes sub-bin clustering)")
print("fit: K=12 background, kernel timescale 1/beta <= 1 s (bmin=1)")
for a in ANG:
    t=M[a].t.values; T=TF[a]; t0=t.min()-1e-3
    n0,b0,lr=fit(t,t0,T,K=12,bmin=1.0)
    sur=[]; nrep=15 if a==0 else 40
    for r in range(nrep):
        s=surrogate(t,t0,T); sur.append(fit(s,t0,T,K=12,bmin=1.0)[0])
    sur=np.array(sur); p=(1+np.sum(sur>=n0))/(1+len(sur))
    print(a,f"N={len(t)} n_obs={n0:.2f} 1/beta={1/b0*1000:.0f} ms | surrogate n mean={sur.mean():.2f} 95th={np.percentile(sur,95):.2f} max={sur.max():.2f} | excess={n0-sur.mean():.2f} p={p:.3f}")
