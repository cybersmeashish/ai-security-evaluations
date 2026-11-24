"""Compare explicitly declared fixture metadata; no real identity or entity extraction."""
FIELDS=("bank","subject_group","case","purpose","epoch","corpus","release","language")
def declared_reuse_eligible(a,b):
    for x in (a,b):
        if x.get("declared_eligible") is not True or not isinstance(x.get("scope"),dict):return False
        s=x["scope"]
        if type(s.get("epoch")) is not int or s["epoch"]<0:return False
        if any(not isinstance(s.get(k),str) or not s[k] for k in FIELDS if k!="epoch"):return False
        if not isinstance(x.get("critical"),list) or any(not isinstance(v,str) for v in x["critical"]):return False
    return all(a["scope"][k]==b["scope"][k] for k in FIELDS) and a["critical"]==b["critical"]
