def to_str(val):
    if isinstance(val, float): # If float round it up to 5 decimals
        return str(round(val, 5))
    elif val is None: # If None type do nothing
        return val
    
    return val.encode('utf-8')