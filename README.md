# TrustPay
Privacy-preserving and explainable fraud detection for simulated UPI-style payments.

## Run
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:ID_HASH_SECRET="your-local-secret"
python train.py
pytest -q
streamlit run app.py
```

This is a synthetic-data hackathon prototype. It has no real UPI, bank, or NPCI integration.
