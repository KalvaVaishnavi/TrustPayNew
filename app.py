import os
import streamlit as st
from src.model import load_model
from src.data import FEATURES
from src.rules import rule_risk
from src.privacy import protect_id
st.set_page_config(page_title="TrustPay",page_icon="🛡️",layout="wide")
st.title("🛡️ TrustPay")
st.caption("Privacy-preserving, explainable fraud-risk screening for simulated UPI-style payments")
if not os.getenv("ID_HASH_SECRET"): st.warning("Demo secret in use. Set ID_HASH_SECRET before deployment.")
@st.cache_resource
def bundle(): return load_model()
b=bundle()
with st.sidebar:
 st.header("Model metrics"); st.json(b["metrics"]); st.caption("Metrics use held-out synthetic data.")
with st.form("payment"):
 c1,c2=st.columns(2)
 with c1:
  uid=st.text_input("User reference","demo-user-001"); amount=st.number_input("Amount (₹)",min_value=1.0,value=2500.0); hour=st.slider("Hour",0,23,14); count=st.number_input("Transactions today",min_value=0,value=2)
 with c2:
  new=st.checkbox("New beneficiary"); device=st.checkbox("New device"); failed=st.number_input("Failed attempts in last hour",min_value=0,value=0); ratio=st.number_input("Amount ÷ usual amount",min_value=.1,value=1.0); age=st.number_input("Account age (days)",min_value=1,value=365)
 submit=st.form_submit_button("Assess transaction")
if submit:
 t={"amount":amount,"hour":hour,"new_beneficiary":int(new),"transaction_count":int(count),"device_changed":int(device),"failed_attempts":int(failed),"amount_ratio":ratio,"account_age_days":int(age)}
 p=float(b["model"].predict_proba([[t[x] for x in FEATURES]])[0][1]); rs,reasons=rule_risk(t); score=round(min(100,70*p+0.30*rs),1)
 level="HIGH RISK" if score>=70 else "MEDIUM RISK" if score>=40 else "LOW RISK"
 a,c,d=st.columns(3); a.metric("Protected user reference",protect_id(uid)); c.metric("Risk score",f"{score}/100"); d.metric("Decision",level)
 st.write("**Recommended action:** " + ("Require verification and analyst review." if score>=70 else "Request additional verification." if score>=40 else "Allow with routine monitoring."))
 st.write("**Why it was flagged:**")
 for r in reasons or ["No major rule-based indicators were detected."]: st.write("• "+r)
 st.caption(f"ML fraud probability: {p:.1%}. Raw user reference is not stored by this app.")
