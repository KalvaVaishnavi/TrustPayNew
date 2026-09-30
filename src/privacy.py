import os, hmac, hashlib
def protect_id(user_id):
 secret=os.getenv("ID_HASH_SECRET","DEMO_ONLY_CHANGE_ME").encode()
 return hmac.new(secret,user_id.encode(),hashlib.sha256).hexdigest()[:16]
