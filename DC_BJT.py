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

def display_results(ib, ic, ie, vce, rth=None, vth=None):
    print("\nResults:")
    print(f"IB  = {ib:.6f} A")
    print(f"IC  = {ic:.6f} A")
    print(f"IE  = {ie:.6f} A")
    print(f"VCE = {vce:.6f} V")
    if rth is not None and vth is not None:
        print(f"Rth = {rth:.2f} KOhm")
        print(f"Vth = {vth:.2f} V")
    if ib<=0 :
        print("Transistor is CUT OFF.")
    elif vce > 0.2:
        print("Transistor is in ACTIVE region.")
    else:
        print("Transistor is in SATURATION region.")

def main():
    print("Select BJT analysis mode:")
    print("1. Mode 1")
    print("2. Mode 2")
    print("3. Mode 3")
    print("4. Mode 4")
    print("5. Mode 5")

    mode = input("Enter mode number (1 to 5): ")

    try:
        beta = float(input("Enter β (current gain): "))
        vcc = float(input("Enter VCC (volts): "))
        rc = float(input("Enter RC (Kohms): "))

        if mode == "1":
            rb = float(input("Enter RB (Kohms): "))
            ib, ic, ie, vce = bjt_mode1(beta, vcc, rc, rb)
            display_results(ib, ic, ie, vce)

        elif mode == "2":
            rb = float(input("Enter RB (Kohms): "))
            ib, ic, ie, vce = bjt_mode2(beta, vcc, rc, rb)
            display_results(ib, ic, ie, vce)

        elif mode == "3":
            rb = float(input("Enter RB (Kohms): "))
            re = float(input("Enter RE (Kohms): "))
            ib, ic, ie, vce = bjt_mode3(beta, vcc, rc, rb, re)
            display_results(ib, ic, ie, vce)

        elif mode == "4":
            rb1 = float(input("Enter RB1 (Kohms): "))
            rb2 = float(input("Enter RB2 (Kohms): "))
            re = float(input("Enter RE (Kohms): "))
            ib, ic, ie, vce, rth, vth = bjt_mode4(beta, vcc, rc, rb1, rb2, re)
            display_results(ib, ic, ie, vce, rth, vth)

        elif mode == "5":
            rb = float(input("Enter RB (Kohms): "))
            re = float(input("Enter RE (Kohms): "))
            ib, ic, ie, vce = bjt_mode5(beta, vcc, rc, rb, re)
            display_results(ib, ic, ie, vce)

        else:
            print("Invalid mode selected. Please choose between 1 and 5.")

    except ValueError:
        print("⚠ Error: Please enter valid numerical values.")
    except ZeroDivisionError:
        print("⚠ Error: Division by zero encountered. Check your resistor values.")

if __name__ == "__main__":
    main()
