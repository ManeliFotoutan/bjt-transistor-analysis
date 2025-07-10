# --- Active Mode Calculations ---
def bjt_mode1(beta, vcc, rc, rb):
    ib = (vcc - 0.7) / rb
    ic = beta * ib
    ie = ib + ic
    vce = vcc - rc * ic
    return ib, ic, ie, vce

def bjt_mode2(beta, vcc, rc, rb):
    ib = (vcc - 0.7) / (((beta + 1) * rc) + rb)
    ic = beta * ib
    ie = ib + ic
    vce = vcc - (((beta + 1) / beta) * rc * ic)
    return ib, ic, ie, vce

def bjt_mode3(beta, vcc, rc, rb, re):
    ib = (vcc - 0.7) / (((beta + 1) * re) + rb)
    ic = beta * ib
    ie = ib + ic
    vce = vcc - (rc + ((beta + 1) / beta) * re) * ic
    return ib, ic, ie, vce

def bjt_mode4(beta, vcc, rc, rb1, rb2, re):
    rth = (rb1 * rb2) / (rb1 + rb2)
    vth = (rb2 / (rb1 + rb2)) * vcc
    ib = (vth - 0.7) / (rth + (beta + 1) * re)
    ic = beta * ib
    ie = ib + ic
    vce = vcc - (rc + ((beta + 1) / beta) * re) * ic
    return ib, ic, ie, vce, rth, vth

def bjt_mode5(beta, vcc, rc, rb, re):
    ib = (vcc - 0.7) / (((beta + 1) * (re + rc)) + rb)
    ic = beta * ib
    ie = ib + ic
    vce = vcc - (((beta + 1) / beta) * (re + re)) * ic
    return ib, ic, ie, vce

# --- Saturation Mode Calculations ---
def saturation_mode1(vcc, rc, rb):
    ib = (vcc - 0.8) / rb
    ic = (vcc - 0.2) / rc
    ie = ib + ic
    return ib, ic, ie

def saturation_mode2(vcc, rc, rb):
    ib = (vcc - 0.8) / (rb + rc)
    ic = (vcc - 0.2) / rc
    ie = ib + ic
    return ib, ic, ie

def saturation_mode3(vcc, rc, rb, re):
    total_ibic = (vcc - 0.8) / (rb + re)
    ic = (vcc - 0.2 - total_ibic * re) / rc
    ib = total_ibic - ic
    ie = ib + ic
    return ib, ic, ie

def saturation_mode4(vcc, rc, rth, vth, re):
    total_ibic = (vth - 0.8) / (rth + re)
    ic = (vcc - 0.2 - total_ibic * re) / rc
    ib = total_ibic - ic
    ie = ib + ic
    return ib, ic, ie

def saturation_mode5(vcc, rc, rb, re):
    total_ibic = (vcc - 0.8) / (rb + rc + re)
    ic = (vcc - 0.2 - total_ibic * re) / rc
    ib = total_ibic - ic
    ie = ib + ic
    return ib, ic, ie




