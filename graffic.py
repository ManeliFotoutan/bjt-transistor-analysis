import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk

from DC_BJT import *

# Color and font constants
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

# Button hover effect functions
def on_enter(e): # mouse enters
    e.widget.config(bg=BUTTON_HOVER_COLOR)

def on_leave(e):
    e.widget.config(bg=BUTTON_COLOR)

def clear_inputs_and_results():
    for entry in [beta_entry, vcc_entry, rc_entry, rb_entry, rb1_entry, rb2_entry, re_entry]:
        entry.delete(0, tk.END)
    result_text.set("")

def select_mode():
    def handle_selection(mode):
        selected_mode.set(mode)
        clear_inputs_and_results()
        animate_mode_label(f"\u25CF {mode.upper()} selected")
        update_entry_visibility()
        mode_window.destroy()

    mode_window = tk.Toplevel()
    mode_window.title("Select Mode")
    mode_window.geometry("900x1100") 
    mode_window.configure(bg=BG_COLOR)

    tk.Label(mode_window, text="Choose BJT Mode:", bg=BG_COLOR, fg=DARK_BROWN, font=FONT_TITLE).pack(pady=10)

    frame = tk.Frame(mode_window, bg=BG_COLOR)
    frame.pack()

    # Create mode selection interface with images
    for i, img_path in enumerate(image_paths):
        try:
            img = Image.open(img_path).resize((290, 290))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(frame, image=img_tk, bg=BG_COLOR)
            lbl.image = img_tk
            row = i // 2
            col = i % 2
            lbl.grid(row=row * 2, column=col, padx=20, pady=10)

            rb = tk.Radiobutton(
                frame,
                text=f"Mode {i + 1}",
                variable=selected_mode,
                value=f"mode{i + 1}",
                bg=BG_COLOR,
                fg=BLACK,
                command=lambda m=f"mode{i + 1}": handle_selection(m)
            )
            rb.grid(row=row * 2 + 1, column=col, pady=(0, 15))
        except FileNotFoundError:
            continue

# Animate mode selection label with blinking effect
def animate_mode_label(text):
    def animate():
        for i in range(3):
            mode_label.config(fg="green")
            time.sleep(0.3)
            mode_label.config(fg=BG_COLOR)
            time.sleep(0.3)
        mode_label.config(text=text, fg="green")

    threading.Thread(target=animate).start()

# Show/hide input fields based on selected mode
def update_entry_visibility():
    mode = selected_mode.get()
    param_title_label.pack(pady=10)
    for frame in input_frames.values():
        frame.pack_forget()

    # Always show these basic parameters
    input_frames["beta"].pack(pady=5)
    input_frames["vcc"].pack(pady=5)
    input_frames["rc"].pack(pady=5)

    # Show additional parameters based on mode
    if mode in ["mode1", "mode2", "mode3", "mode5"]:
        input_frames["rb"].pack(pady=5)
    if mode in ["mode3", "mode4", "mode5"]:
        input_frames["re"].pack(pady=5)
    if mode == "mode4":
        input_frames["rb1"].pack(pady=5)
        input_frames["rb2"].pack(pady=5)

    calc_btn.pack(pady=10)


# Plot IC vs VCE characteristics with Q-point 
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

        vce_range = [vce - 1 + i * 0.2 for i in range(11)]  # 11 dots in [VCE-1, VCE+1]
        ic_values = [ic + 0.01 * (v - vce) for v in vce_range]  # line

        plt.figure(figsize=(6, 4))
        plt.plot(vce_range, ic_values, label="IC vs VCE", color="blue")
        plt.scatter([vce], [ic], color="red", label="Q-point")
        plt.title("Linear Output Characteristics (IC vs VCE)")
        plt.xlabel("VCE (V)")
        plt.ylabel("IC (A)")
        plt.grid(True)
        plt.legend()
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
                result_text.set(f"Active Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode1(vcc, rc, rb)
                result_text.set(f"Saturation Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = 0.2 V")
        elif mode == "mode2":
            ib, ic, ie, vce = bjt_mode2(beta, vcc, rc, rb)
            if vce > 0.2:
                result_text.set(f"Active Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode2(vcc, rc, rb)
                result_text.set(f"Saturation Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = 0.2 V")
        elif mode == "mode3":
            re = float(re_entry.get())
            ib, ic, ie, vce = bjt_mode3(beta, vcc, rc, rb, re)
            if vce > 0.2:
                result_text.set(f"Active Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode3(vcc, rc, rb, re)
                result_text.set(f"Saturation Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = 0.2 V")
        elif mode == "mode4":
            rb1 = float(rb1_entry.get())
            rb2 = float(rb2_entry.get())
            re = float(re_entry.get())
            ib, ic, ie, vce, rth, vth = bjt_mode4(beta, vcc, rc, rb1, rb2, re)
            if vce > 0.2:
                result_text.set(f"Active Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V\nRth = {rth:.6f} KΩ\nVth = {vth:.6f} V")
            else:
                ib, ic, ie = saturation_mode4(vcc, rc, rth, vth, re)
                result_text.set(f"Saturation Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = 0.2 V")
        elif mode == "mode5":
            re = float(re_entry.get())
            ib, ic, ie, vce = bjt_mode5(beta, vcc, rc, rb, re)
            if vce > 0.2:
                result_text.set(f"Active Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = {vce:.6f} V")
            else:
                ib, ic, ie = saturation_mode5(vcc, rc, rb, re)
                result_text.set(f"Saturation Region:\nIB = {ib:.6f} A\nIC = {ic:.6f} A\nIE = {ie:.6f} A\nVCE = 0.2 V")

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
        "Note: Values must be in consistent units and valid numbers."
    )
    messagebox.showinfo("User Guide", guide_text)

def main_gui():
    global beta_entry, vcc_entry, rc_entry, rb_entry, rb1_entry, rb2_entry, re_entry
    global result_text, selected_mode, mode_label, calc_btn, input_frames , param_title_label

    root = tk.Tk()
    root.title("BJT Circuit Simulator")
    root.geometry("600x800")
    root.configure(bg=BG_COLOR)

    selected_mode = tk.StringVar()
    input_frames = {}

    tk.Label(root, text="BJT DC Analysis Tool", bg=BG_COLOR, fg=DARK_BROWN, font=("Arial", 20, "bold")).pack(pady=15)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    for text, cmd in [("Select Mode", select_mode), ("Guide", show_guide), ("Plot", plot_waveform)]:
        btn = tk.Button(button_frame, text=text, command=cmd, bg=BUTTON_COLOR, fg=FG_COLOR, font=FONT_BUTTON, relief="flat", width=12)
        btn.pack(side="left", padx=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    mode_label = tk.Label(root, text="", bg=BG_COLOR, fg=BG_COLOR, font=("Arial", 12, "bold"))
    mode_label.pack(pady=5)

    param_title_label =  tk.Label(root, text="Enter Parameters:", bg=BG_COLOR, fg=DARK_BROWN, font=FONT_TITLE)

    def create_labeled_entry(label_text, key):
        frame = tk.Frame(root, bg=BG_COLOR)
        tk.Label(frame, text=label_text, bg=BG_COLOR, fg=BLACK, font=FONT_LABEL, width=12, anchor="w").pack(side="left")
        entry = tk.Entry(frame, font=FONT_LABEL, width=15)
        entry.pack(side="left")
        input_frames[key] = frame
        return entry

    beta_entry = create_labeled_entry("β (Beta):", "beta")
    vcc_entry = create_labeled_entry("VCC (V):", "vcc")
    rc_entry = create_labeled_entry("RC (KΩ):", "rc")
    rb_entry = create_labeled_entry("RB (KΩ):", "rb")
    re_entry = create_labeled_entry("RE (KΩ):", "re")
    rb1_entry = create_labeled_entry("RB1 (KΩ):", "rb1")
    rb2_entry = create_labeled_entry("RB2 (KΩ):", "rb2")

    # It is shown , when a mode is selected
    calc_btn = tk.Button(root, text="Calculate", command=handle_calculation,
                        bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold"),
                        relief="flat", width=20)
    calc_btn.bind("<Enter>", on_enter)
    calc_btn.bind("<Leave>", on_leave)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, bg=BG_COLOR, fg=BLACK, font=FONT_LABEL, justify="left")
    result_label.pack(pady=20)

    root.mainloop()
    
if __name__ == "__main__":
    main_gui()