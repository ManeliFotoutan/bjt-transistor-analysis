import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk

from DC_BJT import *

BG_COLOR = "#FFE4C4" 
FG_COLOR = "#FFE4C4"
BUTTON_COLOR = "#640f09" 
BUTTON_HOVER_COLOR = "#85331f" 
DARK_BROWN = "#500C07"
BROWN = "#640f09"
CREAM = "#FFE4C4"
BLACK = "#000000"
FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 12)
FONT_BUTTON = ("Arial", 12, "bold")

image_paths = [f"./images/mode{i+1}.jpg" for i in range(5)] 

def on_enter(e):
    e.widget.config(bg=BUTTON_HOVER_COLOR)

def on_leave(e):
    e.widget.config(bg=BUTTON_COLOR)

def select_mode():
    def handle_selection(mode):
        selected_mode.set(mode)
        animate_mode_label(f"\u25CF {mode.upper()} selected")
        update_entry_visibility()
        mode_window.destroy()

    mode_window = tk.Toplevel()
    mode_window.title("Select Mode")
    mode_window.geometry("600x400")
    mode_window.configure(bg=BG_COLOR)

    tk.Label(mode_window, text="Choose BJT Mode:", bg=BG_COLOR, fg=DARK_BROWN, font=FONT_TITLE).pack(pady=10)

    frame = tk.Frame(mode_window, bg=BG_COLOR)
    frame.pack()

    for i, img_path in enumerate(image_paths):
        try:
            img = Image.open(img_path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(frame, image=img_tk, bg=BG_COLOR)
            lbl.image = img_tk
            lbl.grid(row=0, column=i, padx=10)

            rb = tk.Radiobutton(
                frame,
                text=f"Mode {i+1}",
                variable=selected_mode,
                value=f"mode{i+1}",
                bg=BG_COLOR,
                fg=BLACK,
                command=lambda m=f"mode{i+1}": handle_selection(m)
            )
            rb.grid(row=1, column=i)
        except FileNotFoundError:
            continue

def animate_mode_label(text):
    def animate():
        for i in range(3):
            mode_label.config(fg="green")
            time.sleep(0.3)
            mode_label.config(fg=BG_COLOR)
            time.sleep(0.3)
        mode_label.config(text=text, fg="green")

    threading.Thread(target=animate).start()

def update_entry_visibility():
    mode = selected_mode.get()
    for entry in [rb_entry, rb1_entry, rb2_entry, re_entry]:
        entry.master.pack_forget()
    if mode in ["mode1", "mode2", "mode3", "mode5"]:
        rb_entry.master.pack(pady=5)
    if mode in ["mode3", "mode4", "mode5"]:
        re_entry.master.pack(pady=5)
    if mode == "mode4":
        rb1_entry.master.pack(pady=5)
        rb2_entry.master.pack(pady=5)

def export_results():
    if not result_text.get():
        messagebox.showinfo("Export", "No results to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(result_text.get())
        messagebox.showinfo("Export", "Results saved successfully.")

def plot_waveform():
    mode = selected_mode.get()
    try:
        beta = float(beta_entry.get())
        vcc = float(vcc_entry.get())
        rc = float(rc_entry.get())

        if mode in ["mode1", "mode2", "mode3", "mode5"]:
            rb = float(rb_entry.get())
        if mode in ["mode3", "mode4", "mode5"]:
            re = float(re_entry.get())
        if mode == "mode4":
            rb1 = float(rb1_entry.get())
            rb2 = float(rb2_entry.get())

        if mode == "mode1":
            ib, ic, ie, vce = bjt_mode1(beta, vcc, rc, rb)
        elif mode == "mode2":
            ib, ic, ie, vce = bjt_mode2(beta, vcc, rc, rb)
        elif mode == "mode3":
            ib, ic, ie, vce = bjt_mode3(beta, vcc, rc, rb, re)
        elif mode == "mode4":
            ib, ic, ie, vce, rth, vth = bjt_mode4(beta, vcc, rc, rb1, rb2, re)
        elif mode == "mode5":
            ib, ic, ie, vce = bjt_mode5(beta, vcc, rc, rb, re)
        else:
            messagebox.showinfo("Plot", "Please select a valid mode.")
            return

        t = [x for x in range(10)]
        ic_wave = [ic * (0.8 + 0.2 * (x % 2)) for x in t]  # small fluctuation
        vce_wave = [vce * (0.8 + 0.2 * ((x+1) % 2)) for x in t]

        plt.figure(figsize=(7, 4))
        plt.plot(t, ic_wave, label="IC (A)", color="blue")
        plt.plot(t, vce_wave, label="VCE (V)", color="red")

        # Q-point
        plt.scatter([5], [ic], label="Q-point IC", color="navy", zorder=5)
        plt.scatter([5], [vce], label="Q-point VCE", color="darkred", zorder=5)

        plt.xlabel("Time (a.u.)")
        plt.ylabel("Amplitude")
        plt.title("IC & VCE Waveforms with Q-point")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Plot Error", f"Check inputs or mode selection.\n\n{str(e)}")

def handle_calculation():
    try:
        beta = float(beta_entry.get())
        vcc = float(vcc_entry.get())
        rc = float(rc_entry.get())
        mode = selected_mode.get()

        if mode in ["mode1", "mode2", "mode3", "mode5"]:
            rb = float(rb_entry.get())

        if mode == "mode1":
            ib, ic, ie, vce = bjt_mode1(beta, vcc, rc, rb)
            if vce > 0.2:
                result_text.set(f"IB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode1(vcc, rc, rb)
                result_text.set(f"Saturation Mode:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A")
        elif mode == "mode2":
            ib, ic, ie, vce = bjt_mode2(beta, vcc, rc, rb)
            if vce > 0.2:
                result_text.set(f"IB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode2(vcc, rc, rb)
                result_text.set(f"Saturation Mode:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A")
        elif mode == "mode3":
            re = float(re_entry.get())
            ib, ic, ie, vce = bjt_mode3(beta, vcc, rc, rb, re)
            if vce > 0.2:
                result_text.set(f"IB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode3(vcc, rc, rb, re)
                result_text.set(f"Saturation Mode:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A")
        elif mode == "mode4":
            rb1 = float(rb1_entry.get())
            rb2 = float(rb2_entry.get())
            re = float(re_entry.get())
            ib, ic, ie, vce, rth, vth = bjt_mode4(beta, vcc, rc, rb1, rb2, re)
            if vce > 0.2:
                result_text.set(f"IB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V\nRth = {rth:.6f} Ω\nVth = {vth:.6f} V")
            else:
                ib, ic, ie = saturation_mode4(vcc, rc, rth, vth, re)
                result_text.set(f"Saturation Mode:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A")
        elif mode == "mode5":
            re = float(re_entry.get())
            ib, ic, ie, vce = bjt_mode5(beta, vcc, rc, rb, re)
            if vce > 0.2:
                result_text.set(f"IB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode5(vcc, rc, rb, re)
                result_text.set(f"Saturation Mode:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numerical values.")

def show_guide():
    guide_text = (
        "Welcome to the BJT Circuit Simulator!\n\n"
        "This tool helps analyze DC behavior of Bipolar Junction Transistors (BJTs).\n\n"
        "Steps to use:\n"
        "1. Click 'Select Mode' to choose from 5 BJT operating modes.\n"
        "2. Enter the appropriate values depending on mode.\n"
        "3. Click 'Calculate' to compute IB, IC, IE, and VCE.\n"
        "4. Use buttons to export results or view waveforms.\n\n"
        "Note: Values must be in consistent units and valid numbers."
    )
    messagebox.showinfo("User Guide", guide_text)

def main_gui():
    global beta_entry, vcc_entry, rc_entry, rb_entry, rb1_entry, rb2_entry, re_entry
    global result_text, selected_mode, mode_label

    root = tk.Tk()
    root.title("BJT Circuit Simulator")
    root.geometry("600x800")
    root.configure(bg=BG_COLOR)

    selected_mode = tk.StringVar()

    tk.Label(root, text="BJT DC Analysis Tool", bg=BG_COLOR, fg=DARK_BROWN, font=("Arial", 20, "bold")).pack(pady=15)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    for text, cmd in [("Select Mode", select_mode), ("Guide", show_guide), ("Export", export_results), ("Plot", plot_waveform)]:
        btn = tk.Button(button_frame, text=text, command=cmd, bg=BUTTON_COLOR, fg=FG_COLOR, font=FONT_BUTTON, relief="flat", width=12)
        btn.pack(side="left", padx=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    mode_label = tk.Label(root, text="", bg=BG_COLOR, fg=BG_COLOR, font=("Arial", 12, "bold"))
    mode_label.pack(pady=5)

    tk.Label(root, text="Enter Parameters:", bg=BG_COLOR, fg=DARK_BROWN, font=FONT_TITLE).pack(pady=10)

    def create_labeled_entry(label_text):
        frame = tk.Frame(root, bg=BG_COLOR)
        frame.pack(pady=10)
        tk.Label(frame, text=label_text, bg=BG_COLOR, fg=BLACK, font=FONT_LABEL, width=12, anchor="w").pack(side="left")
        entry = tk.Entry(frame, font=FONT_LABEL, width=15)
        entry.pack(side="left")
        return entry

    beta_entry = create_labeled_entry("β (Beta):")
    vcc_entry = create_labeled_entry("VCC (V):")
    rc_entry = create_labeled_entry("RC (Ω):")
    rb_entry = create_labeled_entry("RB (Ω):")
    re_entry = create_labeled_entry("RE (Ω):")
    rb1_entry = create_labeled_entry("RB1 (Ω):")
    rb2_entry = create_labeled_entry("RB2 (Ω):")

    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(fill='x', pady=10)

    calc_btn = tk.Button(btn_frame, text="Calculate", command=handle_calculation,
                        bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold"), relief="flat", width=20)
    calc_btn.bind("<Enter>", on_enter)
    calc_btn.bind("<Leave>", on_leave)
    calc_btn.pack(side='right', padx=40)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, bg=BG_COLOR, fg=BLACK, font=FONT_LABEL, justify="left")
    result_label.pack(side='right', padx=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()