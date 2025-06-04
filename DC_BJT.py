# --- Active Mode Calculations ---
def bjt_mode1(beta, vcc, rc, rb):
    ib = (vcc - 0.7) / (((beta + 1) * rc) + rb)
    ic = beta * ib
    ie = ib + ic
    vce = vcc - (((beta + 1) / beta) * rc * ic)
    return ib, ic, ie, vce

def bjt_mode2(beta, vcc, rc, rb):
    ib = (vcc - 0.7) / rb
    ic = beta * ib
    ie = ib + ic
    vce = vcc - rc * ic
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
    ib = (vcc - 0.8) / (rb + rc)
    ic = (vcc - 0.2) / rc
    ie = ib + ic
    return ib, ic, ie

def saturation_mode2(vcc, rc, rb):
    ib = (vcc - 0.8) / rb
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

# --- Display Functions ---
def display_results(ib, ic, ie, vce, rth=None, vth=None):
    print("\n🔎 Active Mode Results:")
    print(f"IB  = {ib:.6f} A")
    print(f"IC  = {ic:.6f} A")
    print(f"IE  = {ie:.6f} A")
    print(f"VCE = {vce:.6f} V")
    if rth is not None and vth is not None:
        print(f"Rth = {rth:.2f} KOhm")
        print(f"Vth = {vth:.2f} V")

def display_saturation(ib, ic, ie):
    print("\n💡 Saturation Mode Values:")
    print(f"IB  = {ib:.6f} A")
    print(f"IC  = {ic:.6f} A")
    print(f"IE  = {ie:.6f} A")

# --- Main Program ---
def main():
    print("📘 Select BJT Circuit Configuration:")
    print("1. Mode 1: IB = (VCC - 0.7) / [(β + 1) * RC + RB]")
    print("2. Mode 2: IB = (VCC - 0.7) / RB")
    print("3. Mode 3: With emitter resistor RE")
    print("4. Mode 4: Voltage divider bias with RE")
    print("5. Mode 5: Denominator includes RC and RE")

    mode = input("🔢 Enter mode number (1 to 5): ")

    try:
        beta = float(input("🧮 Enter β (current gain of transistor): "))
        vcc = float(input("🔋 Enter VCC (volts): "))
        rc = float(input("🟫 Enter RC (kohms): "))

        vce, ib, ic, ie = None, None, None, None
        region = ""

        if mode == "1":
            rb = float(input("🟫 Enter RB (kohms): "))
            ib_a, ic_a, ie_a, vce_a = bjt_mode1(beta, vcc, rc, rb)
            if vce_a > 0.2:
                region = "Active"
                vce, ib, ic, ie = vce_a, ib_a, ic_a, ie_a
            else:
                region = "Saturation"
                ib, ic, ie = saturation_mode1(vcc, rc, rb)
                vce = 0.2

        elif mode == "2":
            rb = float(input("🟫 Enter RB (kohms): "))
            ib_a, ic_a, ie_a, vce_a = bjt_mode2(beta, vcc, rc, rb)
            if vce_a > 0.2:
                region = "Active"
                vce, ib, ic, ie = vce_a, ib_a, ic_a, ie_a
            else:
                region = "Saturation"
                ib, ic, ie = saturation_mode2(vcc, rc, rb)
                vce = 0.2

        elif mode == "3":
            rb = float(input("🟫 Enter RB (kohms): "))
            re = float(input("🟫 Enter RE (kohms): "))
            ib_a, ic_a, ie_a, vce_a = bjt_mode3(beta, vcc, rc, rb, re)
            if vce_a > 0.2:
                region = "Active"
                vce, ib, ic, ie = vce_a, ib_a, ic_a, ie_a
            else:
                region = "Saturation"
                ib, ic, ie = saturation_mode3(vcc, rc, rb, re)
                vce = 0.2

        elif mode == "4":
            rb1 = float(input("🟫 Enter RB1 (kohms): "))
            rb2 = float(input("🟫 Enter RB2 (kohms): "))
            re = float(input("🟫 Enter RE (kohms): "))
            ib_a, ic_a, ie_a, vce_a, rth, vth = bjt_mode4(beta, vcc, rc, rb1, rb2, re)
            if vce_a > 0.2:
                region = "Active"
                vce, ib, ic, ie = vce_a, ib_a, ic_a, ie_a
            else:
                region = "Saturation"
                ib, ic, ie = saturation_mode4(vcc, rc, rth, vth, re)
                vce = 0.2

        elif mode == "5":
            rb = float(input("🟫 Enter RB (kohms): "))
            re = float(input("🟫 Enter RE (kohms): "))
            ib_a, ic_a, ie_a, vce_a = bjt_mode5(beta, vcc, rc, rb, re)
            if vce_a > 0.2:
                region = "Active"
                vce, ib, ic, ie = vce_a, ib_a, ic_a, ie_a
            else:
                region = "Saturation"
                ib, ic, ie = saturation_mode5(vcc, rc, rb, re)
                vce = 0.2
        else:
            print("❌ Invalid mode. Please enter a number between 1 and 5.")
            return

        print(f"\n📊 Region: {region}")
        print(f"IB  = {ib:.6f} A")
        print(f"IC  = {ic:.6f} A")
        print(f"IE  = {ie:.6f} A")
        print(f"VCE = {vce:.6f} V")

        if mode == "4" and region == "Active":
            print(f"Rth = {rth:.2f} KOhm")
            print(f"Vth = {vth:.2f} V")

    except ValueError:
        print("⚠ Error: Please enter numeric values only.")
    except ZeroDivisionError:
        print("⚠ Error: Division by zero detected. Check resistor values.")

if __name__ == "__main__":
    main()
