from pathlib import Path
import numpy as np
import pandas as pd
FEATURES=["amount","hour","new_beneficiary","transaction_count","device_changed","failed_attempts","amount_ratio","account_age_days"]
def make_dataset(n=10000,seed=42):
 r=np.random.default_rng(seed); amount=np.round(r.lognormal(7.6,1,n),2); hour=r.integers(0,24,n); new=r.binomial(1,.16,n); count=r.poisson(3,n); device=r.binomial(1,.1,n); failed=r.poisson(.35,n); ratio=np.round(r.lognormal(.15,.65,n),2); age=r.integers(1,2500,n)
 logit=-6+.000035*amount+.8*new+.18*count+device+.75*failed+.75*ratio+.8*((hour<6)|(hour>23))-.00035*age
 fraud=r.binomial(1,np.clip(1/(1+np.exp(-logit)),.002,.96))
 return pd.DataFrame(dict(amount=amount,hour=hour,new_beneficiary=new,transaction_count=count,device_changed=device,failed_attempts=failed,amount_ratio=ratio,account_age_days=age,is_fraud=fraud))
def ensure_data(path="data/synthetic_upi_transactions.csv"):
 p=Path(path); p.parent.mkdir(exist_ok=True)
 if not p.exists(): make_dataset().to_csv(p,index=False)
 return pd.read_csv(p)
