from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score,precision_score,recall_score,f1_score
from src.data import FEATURES,ensure_data
def train_and_save(path="models/fraud_model.joblib"):
 df=ensure_data(); Xtr,Xte,ytr,yte=train_test_split(df[FEATURES],df.is_fraud,test_size=.2,stratify=df.is_fraud,random_state=42)
 m=RandomForestClassifier(n_estimators=200,max_depth=12,min_samples_leaf=3,class_weight="balanced",random_state=42,n_jobs=-1).fit(Xtr,ytr)
 p=m.predict_proba(Xte)[:,1]; pred=(p>=.5).astype(int); metrics={"PR-AUC":round(average_precision_score(yte,p),3),"Precision":round(precision_score(yte,pred,zero_division=0),3),"Recall":round(recall_score(yte,pred,zero_division=0),3),"F1":round(f1_score(yte,pred,zero_division=0),3)}
 Path(path).parent.mkdir(exist_ok=True); joblib.dump({"model":m,"metrics":metrics},path); return metrics
def load_model(path="models/fraud_model.joblib"):
 if not Path(path).exists(): train_and_save(path)
 return joblib.load(path)
