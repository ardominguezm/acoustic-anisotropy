import numpy as np, pandas as pd
from load import load, TF, ANG
F=pd.read_pickle("wf_feat.pkl")
def events():
    D=load(); out={}
    for a in ANG:
        d=D[a].reset_index(drop=True); f=F[F.angle==a].sort_values("t").reset_index(drop=True)
        assert len(d)==len(f)
        d["ch"]=f.ch.values; d["Ewf"]=f.E.values; d["Eprox"]=10**(d.A/10.0)
        out[a]=d[d.t<=TF[a]].reset_index(drop=True)   # pre-peak only
    return out

def merge_hits(d,gap=5e-4):
    d=d.sort_values("t",kind="stable").reset_index(drop=True)
    g=(d.t.diff().fillna(1)>gap).cumsum()
    e=d.groupby(g).agg(t=("t","min"),A=("A","max"),Ewf=("Ewf","sum"),nch=("ch","nunique"),stage=("stage","first"),f=("f","median"),fc=("fc","first")).reset_index(drop=True)
    return e
