def to_str(val):
    if isinstance(val, float):
        return str(round(val, 5))
    
    return val.encode('utf-8')