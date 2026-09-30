def rule_risk(t):
 s=0; r=[]
 def add(condition,points,text):
  nonlocal s
  if condition: s+=points; r.append(text)
 add(t["amount"]>50000,30,"Transaction amount is unusually high")
 add(20000<t["amount"]<=50000,15,"Transaction amount is higher than usual")
 add(t["hour"]<6 or t["hour"]>23,20,"Transaction occurred at an unusual hour")
 add(t["new_beneficiary"],20,"Beneficiary is new")
 add(t["transaction_count"]>10,15,"Transaction frequency is unusually high")
 add(t["device_changed"],15,"A newly observed device was used")
 add(t["failed_attempts"]>=2,15,"Recent failed payment attempts were detected")
 add(t["amount_ratio"]>4,20,"Amount is much higher than the user's normal amount")
 return min(s,100),r
