from src.rules import rule_risk
from src.privacy import protect_id
def base(): return {"amount":1000,"hour":14,"new_beneficiary":0,"transaction_count":1,"device_changed":0,"failed_attempts":0,"amount_ratio":1,"account_age_days":365}
def test_safe_transaction(): assert rule_risk(base())[0]==0
def test_high_risk_transaction():
 t=base(); t.update(amount=60000,hour=2,new_beneficiary=1,device_changed=1,transaction_count=15,amount_ratio=7); assert rule_risk(t)[0]>=70
def test_id_is_protected(monkeypatch):
 monkeypatch.setenv("ID_HASH_SECRET","test-secret"); assert protect_id("alice@upi") != "alice@upi"
