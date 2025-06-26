permission_risks = {
    "tabs": "High",
    "webRequest": "High",
    "webRequestBlocking": "High",
    "cookies": "Medium",
    "history": "High",
    "clipboardWrite": "Medium",
    "storage": "Low",
    "notifications": "Low",
    "<all_urls>": "High"
}

def rate_permissions(perms):
    results = {"High": [], "Medium": [], "Low": [], "Unknown": []}
    for p in perms:
        risk = permission_risks.get(p, "Unknown")
        results[risk].append(p)
    return results
 
