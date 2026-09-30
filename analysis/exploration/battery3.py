import numpy as np, pandas as pd
from lib import *
from hawkes import fit
E=events(); M={a:merge_hits(E[a]) for a in ANG}
print("== events after merging multi-channel hits (gap>0.5 ms):")
for a in ANG:
    m=M[a]; print(a,"hits",len(E[a]),"events",len(m),"nch dist",m.nch.value_counts().sort_index().to_dict())
print("\n== D. Hawkes branching ratio n (exp kernel, piecewise-const background K=12), whole pre-peak, and by lifetime thirds")
for a in ANG:
    m=M[a]; t=m.t.values; T=TF[a]
    a0,b0,lr=fit(t,t.min()-1e-3,T,K=12)
    row=[f"all: n={a0:.2f} 1/beta={1/b0:.3f}s LR={lr:.0f}"]
    for lo,hi in [(0,0.6),(0.6,0.9),(0.9,1.0)]:
        s=t[(t>=lo*T)&(t<hi*T)]
        if len(s)>=25:
            x=fit(s,lo*T,hi*T,K=6); row.append(f"[{lo:.1f},{hi:.1f}) N={len(s)} n={x[0]:.2f} 1/b={1/x[1]:.3f}")
        else: row.append(f"[{lo:.1f},{hi:.1f}) N={len(s)} skip")
    print(a,len(t),"|"," | ".join(row))
