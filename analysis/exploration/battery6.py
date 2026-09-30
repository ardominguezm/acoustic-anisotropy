import numpy as np
from lib import *
from mfdfa import mfdfa
rng=np.random.default_rng(3)
E=events(); M={a:merge_hits(E[a]) for a in ANG}
def dh(x):
    q,h,_=mfdfa(x); return h[0]-h[-1], h[q==2][0]
print("== MF-DFA on merged-event series: Delta h = h(q=-4)-h(q=4), and H=h(2); shuffle surrogates (30)")
for name,fn in [("amplitude dB",lambda m:m.A.values.astype(float)),("log10 inter-event time",lambda m:np.log10(np.diff(m.t.values)+1e-5))]:
    print(name)
    for a in ANG:
        x=fn(M[a]); d0,H0=dh(x)
        sd=[dh(rng.permutation(x)) for _ in range(30)]; sdh=np.array([s[0] for s in sd]); sH=np.array([s[1] for s in sd])
        print(f"  {a}: N={len(x)} dh={d0:.2f} H={H0:.2f} | shuffled dh={sdh.mean():.2f}±{sdh.std():.2f} H={sH.mean():.2f}±{sH.std():.2f} | z_dh={(d0-sdh.mean())/sdh.std():.1f} z_H={(H0-sH.mean())/sH.std():.1f}")
print("\n== Fano factor of event counts vs timescale; ratio to within-bin-shuffled surrogate (should be 1 if no fast clustering)")
for a in ANG:
    t=M[a].t.values; T=TF[a]; t0=t.min(); out=[]
    # detrend slow rate: use local rate from 48 bins; compute dispersion of counts in bins of width w in the central 0.3-0.9 tau
    lo,hi=0.3*T,0.9*T
    for w in [0.1,0.5,2.0]:
        e=np.arange(lo,hi,w); c=np.histogram(t,e)[0]
        # normalise by local mean (rolling over 20 bins)
        k=max(3,int(20)); loc=np.convolve(c,np.ones(k)/k,mode="same")
        m=loc>0; F=np.var(c[m]-loc[m])/np.mean(loc[m])
        sur=[]
        for _ in range(30):
            s=np.sort(rng.uniform(lo,hi,((t>=lo)&(t<hi)).sum()))   # crude homogeneous
            cs=np.histogram(s,e)[0]; ls=np.convolve(cs,np.ones(k)/k,mode="same"); ms=ls>0
            sur.append(np.var(cs[ms]-ls[ms])/np.mean(ls[ms]))
        out.append(f"w={w}s Fano={F:.2f} (Poisson {np.mean(sur):.2f})")
    print(a," | ".join(out))
