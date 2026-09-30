import pandas as pd, numpy as np
P="/root/.claude/uploads/417d4468-4706-525d-b959-3af4d8ae4da2/250f49d8-Frequency_series_of_AE_signals_through_Fast_Fourier_Transform.xlsx"
ANG=[0,30,45,60,90]
TF={0:551.77,30:360.33,45:324.36,60:280.88,90:240.97}  # from manuscript Sec 2.1
def load():
    D={}
    for a in ANG:
        d=pd.read_excel(P,sheet_name=str(a),header=None).iloc[2:,2:7]
        d.columns=["t","f","A","fc","stage"]
        d=d.apply(pd.to_numeric,errors="coerce").dropna().sort_values("t",kind="stable").reset_index(drop=True)
        d["tau"]=d.t/TF[a]; D[a]=d
    return D
