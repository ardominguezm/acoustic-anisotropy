import pickle, numpy as np, pandas as pd
idx=pd.read_pickle("wf_index.pkl"); W=pickle.load(open("wf.pkl","rb"))
from load import load, TF
D=load()
out=[]
for r in idx.itertuples():
    v=W[(r.angle,r.ch,r.hit)]; dt=r.dt
    pk=np.abs(v).max(); ip=int(np.argmax(np.abs(v)))
    thr=10**(35/20)*1e-6   # 35 dB re 1 uV
    above=np.where(np.abs(v)>=thr)[0]
    first=above[0] if len(above) else ip
    last=above[-1] if len(above) else ip
    cnt=int(np.sum((np.abs(v[1:])>=thr)&(np.abs(v[:-1])<thr)))
    out.append((r.angle,r.ch,r.hit,r.t,pk,20*np.log10(max(pk,1e-12)/1e-6),np.sum(v**2)*dt,(ip-first)*dt*1e6,(last-first)*dt*1e6,cnt))
F=pd.DataFrame(out,columns=["angle","ch","hit","t","pk","Adb_wf","E","rise_us","dur_us","counts"])
F.to_pickle("wf_feat.pkl")
print(F.groupby("angle")[["Adb_wf","E","rise_us","dur_us","counts"]].median().round(3))
# match with xlsx amplitude
for a in [0,60]:
    d=D[a]; f=F[F.angle==a].sort_values("t")
    m=pd.merge_asof(f,d[["t","A","f","fc","stage"]].rename(columns={"t":"tx"}),left_on="t",right_on="tx",direction="nearest",tolerance=1e-4)
    print(a,"matched",m.tx.notna().mean().round(3),"corr Adb_wf vs A",np.corrcoef(m.dropna().Adb_wf,m.dropna().A)[0,1].round(3),"mean diff",(m.Adb_wf-m.A).mean().round(2))
