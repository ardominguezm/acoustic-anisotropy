import numpy as np, pandas as pd
from lib import *
E=events()
print("== A2. stage of max rate using WAVEFORM energy (sum v^2 dt, 1 ms record) vs amplitude proxy")
for a in ANG:
    d=E[a]; res={}
    for name in ["Ewf","Eprox"]:
        r={}
        for w in [5,15,30]:
            grid=np.arange(w,TF[a]+1e-9,0.5)
            rt=[d[name][(d.t>g-w)&(d.t<=g)].sum()/w for g in grid]; ge=grid[int(np.argmax(rt))]
            r[w]=(int(d.stage[d.t<=ge].iloc[-1]),round(ge/TF[a],3))
        st=d.groupby("stage")[name].sum(); r["share_max_stage"]=int(st.idxmax())
        res[name]=r
    print(a,res)
# b-value (Aki-Utsu on amplitude), time-resolved, by event-count windows
print("\n== B. b-value trend over tau (Aki MLE, A in dB, bin 1 dB, Amin per specimen = mode-based)")
def bval(A,Amin):
    A=A[A>=Amin]; 
    if len(A)<30: return np.nan
    return np.log10(np.e)/((A.mean()-(Amin-0.5))/20.0), len(A)
from scipy.stats import spearmanr
for a in ANG:
    d=E[a]; Amin=int(d.A.mode().iloc[0])
    k=max(60,len(d)//6)
    rows=[]
    for i in range(0,len(d)-k+1,k//2):
        s=d.iloc[i:i+k]; b=bval(s.A.values,Amin)
        rows.append((s.tau.mean() if 'tau' in s else (s.t.mean()/TF[a]),b[0] if isinstance(b,tuple) else np.nan))
    r=pd.DataFrame(rows,columns=["tau","b"]).dropna()
    rho,p=spearmanr(r.tau,r.b) if len(r)>3 else (np.nan,np.nan)
    print(a,"Amin",Amin,"n",len(d),"win",k,"b range",r.b.min().round(2),r.b.max().round(2),"first/last",r.b.iloc[0].round(2),r.b.iloc[-1].round(2),"spearman tau-b",round(rho,2),"npts",len(r))
