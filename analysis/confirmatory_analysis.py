from pathlib import Path
import os, zipfile, itertools, json
import numpy as np
import pandas as pd

ANGLES=[0,30,45,60,90]
WINDOWS=[15,30,45]
EVAL_TAUS=[0.6,0.7,0.8]
TRAIN_TAUS=np.arange(0.50,0.91,0.05)

candidates=[
    Path(os.environ["DATA_ZIP"]) if os.environ.get("DATA_ZIP") else None,
    Path("data/raw/18501172.zip"),
    Path("../data/raw/18501172.zip"),
]
DATA_ZIP=next((p for p in candidates if p is not None and p.exists()),None)
if DATA_ZIP is None:
    raise FileNotFoundError("Set DATA_ZIP or place 18501172.zip in data/raw/")

WORK=Path("confirmatory_work")
RESULTS=Path("results")
WORK.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

with zipfile.ZipFile(DATA_ZIP) as z:
    z.extractall(WORK)

f9=WORK/"Supporting data for Figure 9.xlsx"
data={}
for a in ANGLES:
    df=pd.read_excel(f9,sheet_name=str(a),header=None)
    lt=pd.to_numeric(df.iloc[2:,2],errors="coerce").to_numpy(float)
    lv=pd.to_numeric(df.iloc[2:,3],errors="coerce").to_numpy(float)
    m=np.isfinite(lt)&np.isfinite(lv)
    lt,lv=lt[m],lv[m]
    i=int(np.argmax(lv)); tf=float(lt[i])
    et=pd.to_numeric(df.iloc[2:,4],errors="coerce").to_numpy(float)
    ev=pd.to_numeric(df.iloc[2:,5],errors="coerce").to_numpy(float)
    m=np.isfinite(et)&np.isfinite(ev)&(et>=0)&(ev>=0)&(et<=tf)
    data[a]={"tf":tf,"peak":float(lv[i]),"e_t":et[m],"energy":ev[m]}

def energy_rate(angle,t_end,window):
    lo=max(0.0,t_end-window)
    d=data[angle]
    m=(d["e_t"]>lo)&(d["e_t"]<=t_end)
    return max(float(d["energy"][m].sum())/window,1e-12)

def training_frame(trajectories,window,label_map):
    rows=[]
    for trj in trajectories:
        tf=data[trj]["tf"]
        for tau in TRAIN_TAUS:
            rows.append((label_map[trj],energy_rate(trj,tau*tf,window),tf*(1-tau)))
    return pd.DataFrame(rows,columns=["angle","rate","ttf"])

def X_aniso(df):
    b=np.deg2rad(df.angle.to_numpy(float))
    c2=np.cos(2*b); c4=np.cos(4*b); x=np.log(df.ttf.to_numpy(float))
    return np.c_[np.ones(len(df)),c2,c4,x,c2*x,c4*x]

def cv_one(window,label_map=None):
    label_map=label_map or {a:a for a in ANGLES}
    rows=[]
    for test in ANGLES:
        tr=training_frame([a for a in ANGLES if a!=test],window,label_map)
        y=np.log(tr.rate.to_numpy(float))
        Xu=np.c_[np.ones(len(tr)),np.log(tr.ttf.to_numpy(float))]
        bu=np.linalg.lstsq(Xu,y,rcond=None)[0]
        ba=np.linalg.lstsq(X_aniso(tr),y,rcond=None)[0]
        b=np.deg2rad(label_map[test]); c2,c4=np.cos(2*b),np.cos(4*b)
        aeff=ba[0]+ba[1]*c2+ba[2]*c4
        slope=ba[3]+ba[4]*c2+ba[5]*c4
        for tau in EVAL_TAUS:
            tf=data[test]["tf"]; true=tf*(1-tau)
            rate=energy_rate(test,tau*tf,window)
            pu=np.exp(np.clip((np.log(rate)-bu[0])/bu[1],-20,20))
            pa=np.exp(np.clip((np.log(rate)-aeff)/slope,-20,20)) if abs(slope)>1e-10 else np.inf
            rows.append({
                "window":window,"held_out_angle":test,"tau":tau,
                "nmae_universal":abs(pu-true)/tf,
                "nmae_anisotropic":abs(pa-true)/tf
            })
    return pd.DataFrame(rows)

cv=pd.concat([cv_one(w) for w in WINDOWS],ignore_index=True)
cv.to_csv(RESULTS/"leave_one_angle_out.csv",index=False)

wins=cv.assign(win=cv.nmae_anisotropic<cv.nmae_universal).groupby("window").win.sum().to_dict()

obs=cv_one(30)
obs_mean=float(obs.nmae_anisotropic.mean())
perm_stats=[]
for perm in itertools.permutations(ANGLES):
    mapping=dict(zip(ANGLES,perm))
    perm_stats.append(float(cv_one(30,mapping).nmae_anisotropic.mean()))
p_exact=float(np.mean(np.asarray(perm_stats)<=obs_mean))

primary=cv[cv.window==30]
influence=[]
for drop in ANGLES:
    d=primary[primary.held_out_angle!=drop]
    influence.append({
        "removed_angle":drop,
        "mean_improvement":float((d.nmae_universal-d.nmae_anisotropic).mean())
    })
influence=pd.DataFrame(influence)
influence.to_csv(RESULTS/"influence_analysis.csv",index=False)

gate={
    "primary_window_s":30,
    "primary_wins_out_of_15":int(wins[30]),
    "wins_by_window":{str(k):int(v) for k,v in wins.items()},
    "exact_angle_permutation_p":p_exact,
    "removing_60deg_eliminates_mean_advantage":
        bool(influence.loc[influence.removed_angle==60,"mean_improvement"].iloc[0]<=0),
}
gate["confirmatory_gate_pass"]=bool(
    gate["primary_wins_out_of_15"]>=11
    and sum(v>=11 for v in gate["wins_by_window"].values())>=2
    and p_exact<0.05
    and not gate["removing_60deg_eliminates_mean_advantage"]
)
(RESULTS/"confirmatory_gate.json").write_text(json.dumps(gate,indent=2))
print(json.dumps(gate,indent=2))
