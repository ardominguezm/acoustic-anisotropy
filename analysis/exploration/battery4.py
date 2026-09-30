import numpy as np, pandas as pd, time
from lib import *
from hawkes import fit
rng=np.random.default_rng(1)
E=events(); M={a:merge_hits(E[a]) for a in ANG}
def sim_hawkes(mu_edges_vals,edges,a,b,T):
    # thinning-free cluster simulation: immigrants (piecewise Poisson) + offspring exp kernel
    imm=[]
    for k in range(len(mu_edges_vals)):
        n=rng.poisson(mu_edges_vals[k]*(edges[k+1]-edges[k]))
        imm+=list(rng.uniform(edges[k],edges[k+1],n))
    ev=list(imm); q=list(imm)
    while q:
        t0=q.pop(); n=rng.poisson(a)
        for _ in range(n):
            t1=t0+rng.exponential(1/b)
            if t1<T: ev.append(t1); q.append(t1)
    return np.sort(np.array(ev))
print("== robustness of n to background resolution K (whole pre-peak)")
for a in ANG:
    t=M[a].t.values; T=TF[a]; t0=t.min()-1e-3
    print(a,{K:round(fit(t,t0,T,K=K)[0],2) for K in (6,12,24,48)})
print("\n== null calibration: Poisson with data-driven fine background (K=48 counts), refit with K=12 -> estimated n under truth n=0")
for a in ANG:
    t=M[a].t.values; T=TF[a]; t0=t.min()-1e-3
    edges=np.linspace(0,T-t0,49); cnt=np.histogram(t-t0,edges)[0]; mu=cnt/np.diff(edges)
    est=[]
    for r in range(25):
        s=sim_hawkes(mu,edges,0.0,5.0,T-t0)
        if len(s)>20: est.append(fit(s,0,T-t0,K=12)[0])
    print(a,"null n mean",round(np.mean(est),3),"95th pct",round(np.percentile(est,95),3))
print("\n== parametric bootstrap CI for n (K=12)")
for a in ANG:
    t=M[a].t.values; T=TF[a]; t0=t.min()-1e-3
    a0,b0,lr=fit(t,t0,T,K=12)
    edges=np.linspace(0,T-t0,13)
    # background from fitted Poisson-ish: use counts*(1-a0) per bin
    cnt=np.histogram(t-t0,edges)[0]; mu=cnt/np.diff(edges)*(1-a0)
    est=[]; tic=time.time()
    nrep=30 if a==0 else 80
    for r in range(nrep):
        s=sim_hawkes(mu,edges,a0,b0,T-t0)
        if len(s)>20: est.append(fit(s,0,T-t0,K=12)[0])
    print(a,"n_hat",round(a0,2),"boot 95% CI",np.percentile(est,[2.5,97.5]).round(2),"reps",len(est),f"{time.time()-tic:.0f}s")
