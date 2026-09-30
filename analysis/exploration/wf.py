import os, re, glob, numpy as np, pandas as pd
R="/home/claude/work/data/raw/Raw AE Waveforms"
rows=[]; W={}
for a in [0,30,45,60,90]:
    for f in glob.glob(f"{R}/beta{a}°/*.txt"):
        L=open(f,encoding="latin-1").read().split("\n")
        ch=int(re.search(r"CHANNEL NUMBER:\s*(\d+)",L[8]).group(1)) if "CHANNEL" in L[8] else None
        hit=int([l for l in L[:14] if l.startswith("HIT NUMBER")][0].split(":")[1])
        tt=float([l for l in L[:14] if l.startswith("TIME OF TEST")][0].split(":")[1])
        si=float([l for l in L[:14] if l.startswith("SAMPLE INTERVAL")][0].split(":")[1])
        v=np.array([float(x) for x in L[13:] if x.strip()!=""])
        rows.append((a,os.path.basename(f),ch,hit,tt,si,len(v)))
        W[(a,ch,hit)]=v
df=pd.DataFrame(rows,columns=["angle","file","ch","hit","t","dt","n"])
df.to_pickle("wf_index.pkl")
import pickle; pickle.dump(W,open("wf.pkl","wb"))
print(df.groupby("angle").agg(n=("file","count"),chs=("ch",lambda s:sorted(set(s))),dts=("dt",lambda s:sorted(set(s))),npts=("n",lambda s:sorted(set(s)))))
print(df.groupby(["angle","ch"]).size().unstack(fill_value=0))
print("dup t within angle:",df.groupby("angle").t.apply(lambda s:s.duplicated().sum()).to_dict())
