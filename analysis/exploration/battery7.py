import numpy as np
from lib import *
E=events()
def aicc(rss,n,k=2): 
    aic=n*np.log(rss/n)+2*k; return aic+2*k*(k+1)/(n-k-1)
print("non-overlapping windows = 4% of t_f on tau in [0.3,1); models for log(rate): A) a-p*log(TTF)  B) b0+b1*t  C) c+k*log(cumE before window)")
for en in ["Ewf","Eprox"]:
    print("energy:",en)
    for a in ANG:
        d=E[a]; T=TF[a]; w=0.04*T; edges=np.arange(0.3*T,T+1e-9,w)
        rate=[];tm=[];cum=[]
        for lo,hi in zip(edges[:-1],edges[1:]):
            e=d[en][(d.t>lo)&(d.t<=hi)].sum(); rate.append(e/w); tm.append((lo+hi)/2); cum.append(d[en][d.t<=lo].sum())
        rate,tm,cum=map(np.array,(rate,tm,cum)); m=(rate>0)&(cum>0)&(tm<T)
        y=np.log(rate[m]); n=m.sum()
        def rss(X): 
            b=np.linalg.lstsq(X,y,rcond=None)[0]; r=y-X@b; return float(r@r),b
        XA=np.c_[np.ones(n),np.log(T-tm[m])]; XB=np.c_[np.ones(n),tm[m]]; XC=np.c_[np.ones(n),np.log(cum[m])]
        rA,bA=rss(XA); rB,bB=rss(XB); rC,bC=rss(XC)
        aa,ab,ac=aicc(rA,n),aicc(rB,n),aicc(rC,n)
        print(f"  {a}: n={n} p={-bA[1]:.2f} k_cum={bC[1]:.2f} | AICc A={aa:.1f} B={ab:.1f} C={ac:.1f} | best={'ABC'[int(np.argmin([aa,ab,ac]))]}  dA-B={aa-ab:.1f} dC-B={ac-ab:.1f} dC-A={ac-aa:.1f}")
