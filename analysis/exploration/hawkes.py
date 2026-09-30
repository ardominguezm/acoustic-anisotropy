import numpy as np
from scipy.optimize import minimize
def nll(theta,t,T,edges):
    K=len(edges)-1
    mu=np.exp(theta[:K]); a=1/(1+np.exp(-theta[K])); b=np.exp(theta[K+1])
    k=np.clip(np.searchsorted(edges,t,side="right")-1,0,K-1)
    R=np.zeros(len(t)); 
    for i in range(1,len(t)):
        R[i]=np.exp(-b*(t[i]-t[i-1]))*(R[i-1]+1.0)
    lam=mu[k]+a*b*R
    ll=np.sum(np.log(lam))-np.sum(mu*np.diff(edges))-a*np.sum(1-np.exp(-b*(T-t)))
    return -ll
def fit(t,T0,T1,K=12,beta0=(0.3,3,30),bmin=0.02):
    t=t-T0; T=T1-T0; edges=np.linspace(0,T,K+1)
    best=None
    for b0 in beta0:
        mu0=np.full(K,len(t)/T*0.7)
        x0=np.r_[np.log(mu0),0.0,np.log(b0)]
        bnds=[(-12,8)]*K+[(-8,6),(np.log(bmin),np.log(200))]
        r=minimize(nll,x0,args=(t,T,edges),method="L-BFGS-B",bounds=bnds)
        if best is None or r.fun<best.fun: best=r
    K_=K; a=1/(1+np.exp(-best.x[K_])); b=np.exp(best.x[K_+1])
    # Poisson null (alpha~0) with same piecewise mu
    k=np.clip(np.searchsorted(edges,t,side="right")-1,0,K-1)
    cnt=np.bincount(k,minlength=K); mu=cnt/np.diff(edges)
    ll0=np.sum(np.log(mu[k]))-np.sum(mu*np.diff(edges))
    lr=2*(-best.fun-ll0)
    return a,b,lr
