#  BJT DC Analysis & Q-Point Simulator

This project provides a graphical tool to **analyze DC behavior of PNP/NPN BJT transistors** in five common biasing configurations (modes). It helps determine the operating region (**Active** or **Saturation**) and calculates key parameters like **IB**, **IC**, **IE**, **VCE**, and plots the **load line** and **Q-point**.


##  Features

- GUI built using **Tkinter**
- Supports **5 BJT operating modes**
- Calculates:
  - Base Current (**IB**)
  - Collector Current (**IC**)
  - Emitter Current (**IE**)
  - Collector-Emitter Voltage (**VCE**)
- Determines transistor region: **Active** or **Saturation**
- Plots **Load Line** and **Q-point** using Matplotlib
- User-friendly interface with mode-specific inputs and circuit images
- Includes Persian documentation


##  Supported Biasing Modes

1. **Fixed Bias**
2. **Base Bias with Feedback (RC + RB)**
3. **Emitter Bias with RE**
4. **Voltage Divider Bias**
5. **Collector-to-Base Bias with Emitter Resistor**

Each mode corresponds to a different transistor biasing configuration with distinct formulas implemented in `DC_BJT.py`.


##  Project Structure

```
├── DC_BJT.py                  # Logic and calculation functions for all BJT modes
├── graphic.py                 # GUI implementation and plotting
├── images/                    # Circuit diagrams for each mode (mode1.jpg to mode5.jpg)
├── تحلیل و مثال های مدار.pdf  # Persian documentation and worked examples
├── نقطه ی کار.jpeg             # Q-point diagram
├── .gitignore
├── .gitattributes
```


## 🖥️ How to Run

Ensure you have **Python 3.6+** installed.

### ✅ Install Required Libraries:

```bash
pip install matplotlib Pillow
```

###  Run the Application:

```bash
python graphic.py
```


##  Sample Output

- Region: `Active Region` or `Saturation Region`
- Output Parameters:

```
IB = 0.000010 A
IC = 0.001000 A
IE = 0.001010 A
VCE = 5.234 V
```

- **Q-point** is visualized on an **IC vs VCE** plot with the **load line**.


##  Guide

Click the **"Guide"** button inside the GUI to see usage instructions.

For detailed circuit theory and example problems (in Persian), refer to:  
📄 `تحلیل و مثال های مدار.pdf`

##  Notes

- Units must be consistent:
  - Volt for VCC and VCE
  - KΩ for resistors
  - β is dimensionless
- Application determines transistor operating region based on VCE threshold
- Circuit images are displayed for each selected mode
