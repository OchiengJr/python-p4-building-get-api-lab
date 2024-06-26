def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par and par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node and node.__doc__ else node.__name__
    
    # Provide default values if pref or suf are None
    pref = pref or "NoTestClass"
    suf = suf or "NoTestMethod"
    
    # Set the node ID with a clear format
    item._nodeid = f"{pref}::{suf}"
