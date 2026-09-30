import numpy as np, pandas as pd
from load import load, TF, ANG
D=load()
np.set_printoptions(precision=3,suppress=True)
# --- gaps between consecutive hits
print("== inter-hit gap quantiles (s) pre-peak")
for a in ANG:
    d=D[a][D[a].t<=TF[a]]; g=np.diff(d.t.values)
    print(a,len(d),"frac gap<=2e-4:",round((g<=2e-4).mean(),3),"<=1e-3:",round((g<=1e-3).mean(),3),"<=1e-2:",round((g<=1e-2).mean(),3),"median",round(np.median(g),4))
# --- A. stage claim under alternative conventions
print("\n== A. stage of max energy rate under conventions (pre-peak only)")
def Eproxy(A): return 10**(A/10.0)
for a in ANG:
    d=D[a]; d=d[d.t<=TF[a]].copy(); d["E"]=Eproxy(d.A)
    st=d.groupby("stage").agg(t0=("t","min"),t1=("t","max"),n=("t","size"),E=("E","sum"))
    # stage duration: from first event of stage to first event of next / tf
    starts=st.t0.values; ends=np.r_[starts[1:],TF[a]]; st["dur"]=ends-starts
    st["rate"]=st.E/st.dur
    res={"per-stage mean rate":int(st.rate.idxmax()),"per-stage energy share":int(st.E.idxmax())}
    # largest event stage
    res["largest event"]=int(d.loc[d.E.idxmax(),"stage"])
    for w in [2,5,10,15,30]:
        grid=np.arange(w,TF[a]+1e-9,0.5)
        r=[d.E[(d.t>g-w)&(d.t<=g)].sum()/w for g in grid]
        ie=int(np.argmax(r)); ge=grid[ie]
        # stage at window end and window midpoint
        se=d.stage[d.t<=ge].iloc[-1] if (d.t<=ge).any() else np.nan
        sm=d.stage[d.t<=ge-w/2].iloc[-1] if (d.t<=ge-w/2).any() else np.nan
        res[f"w{w} end/mid"]=f"{int(se)}/{int(sm)} (tau_end={ge/TF[a]:.3f})"
    print(a,{k:res[k] for k in res})
    print(st.assign(dur_frac=(st.dur/TF[a]).round(3),E_share=(st.E/st.E.sum()).round(3))[["n","dur","dur_frac","E_share","rate"]].round(3).to_string())
