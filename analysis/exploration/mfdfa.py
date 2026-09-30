import numpy as np
def mfdfa(x,qs=np.arange(-4,4.1,1.0),scales=None,order=1):
    x=np.asarray(x,float); y=np.cumsum(x-x.mean()); N=len(y)
    if scales is None: scales=np.unique(np.logspace(np.log10(10),np.log10(N//5),12).astype(int))
    F=np.zeros((len(qs),len(scales)))
    for j,s in enumerate(scales):
        ns=N//s; v=[]
        for seg in (y[:ns*s].reshape(ns,s), y[N-ns*s:].reshape(ns,s)):
            t=np.arange(s)
            for r in seg:
                c=np.polyfit(t,r,order); v.append(np.mean((r-np.polyval(c,t))**2))
        v=np.array(v)+1e-300
        for i,q in enumerate(qs):
            F[i,j]=np.exp(0.5*np.mean(np.log(v))) if q==0 else np.mean(v**(q/2))**(1/q)
    h=np.array([np.polyfit(np.log(scales),np.log(F[i]),1)[0] for i in range(len(qs))])
    return qs,h,scales
