import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Arc
import numpy as np

class PowerTriangleSimulation:
    def __init__(self, master):
        self.master = master
        self.master.title("POWER TRIANGLE SIMULATION - GSM")
        self.master.geometry("1000x600")
        
        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left frame for inputs and references
        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Input frame
        input_frame = ttk.LabelFrame(left_frame, text="Inputs", padding="10")
        input_frame.pack(fill=tk.X)

        # Active Power input with validation
        ttk.Label(input_frame, text="Active Power (kW):").grid(row=0, column=0, sticky="w")
        self.active_power = tk.DoubleVar(value=100)
        vcmd_active = (self.master.register(self.validate_active_power), '%P')
        ttk.Entry(input_frame, textvariable=self.active_power, width=10, validate='key', validatecommand=vcmd_active).grid(row=0, column=1)

        # Power Factor input with validation
        ttk.Label(input_frame, text="Power Factor:").grid(row=1, column=0, sticky="w")
        self.power_factor = tk.DoubleVar(value=0.8)
        vcmd_pf = (self.master.register(self.validate_power_factor), '%P')
        ttk.Entry(input_frame, textvariable=self.power_factor, width=10, validate='key', validatecommand=vcmd_pf).grid(row=1, column=1)

        # Update button
        ttk.Button(input_frame, text="Update", command=self.update_plot).grid(row=2, column=0, columnspan=2, pady=10)

        # Reference frame
        self.ref_frame = ttk.LabelFrame(left_frame, text="References", padding="10")
        self.ref_frame.pack(fill=tk.BOTH, expand=True)

        # Create plot
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def validate_active_power(self, new_value):
        if new_value == "":
            return True
        try:
            value = float(new_value)
            return value >= 0
        except ValueError:
            return False

    def validate_power_factor(self, new_value):
        if new_value == "":
            return True
        try:
            value = float(new_value)
            return 0 <= value <= 1
        except ValueError:
            return False

    def update_plot(self):
        P_input = self.active_power.get()
        pf = self.power_factor.get()
        
        if pf == 0:
            P = 0
            Q = S = P_input  # When pf = 0, S = Q and P = 0
            angle = np.pi / 2  # 90 degrees
        else:
            P = P_input
            angle = np.arccos(pf)
            Q = P * np.tan(angle)
            S = P / pf

        self.ax.clear()
        max_value = max(P, Q, S)
        self.ax.set_xlim(0, max_value * 1.2)
        self.ax.set_ylim(0, max_value * 1.2)

        # Draw power triangle
        self.ax.arrow(0, 0, P, 0, head_width=max_value*0.02, head_length=max_value*0.02, fc='r', ec='r', linewidth=2)
        self.ax.arrow(0, 0, P, Q, head_width=max_value*0.02, head_length=max_value*0.02, fc='b', ec='b', linewidth=2)
        self.ax.arrow(P, 0, 0, Q, head_width=max_value*0.02, head_length=max_value*0.02, fc='g', ec='g', linewidth=2)

        # Add angle arc 
        angle_radius = max_value * 0.2
        arc = Arc((0, 0), angle_radius * 2, angle_radius * 2, 
                  theta1=0, theta2=np.degrees(angle), color='k')
        self.ax.add_patch(arc)

        # Add axes labels
        self.ax.set_xlabel('Active Power (kW)')
        self.ax.set_ylabel('Reactive Power (kVAr)')

        self.ax.set_title('Power Triangle')
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.canvas.draw()

        # Update reference frame
        for widget in self.ref_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.ref_frame, text="🔴 Active Power (P):", anchor="w").grid(row=0, column=0, sticky="w")
        ttk.Label(self.ref_frame, text=f"{P:.2f} kW", anchor="e").grid(row=0, column=1, sticky="e")

        ttk.Label(self.ref_frame, text="🔵 Apparent Power (S):", anchor="w").grid(row=1, column=0, sticky="w")
        ttk.Label(self.ref_frame, text=f"{S:.2f} kVA", anchor="e").grid(row=1, column=1, sticky="e")

        ttk.Label(self.ref_frame, text="🟢 Reactive Power (Q):", anchor="w").grid(row=2, column=0, sticky="w")
        ttk.Label(self.ref_frame, text=f"{Q:.2f} kVAr", anchor="e").grid(row=2, column=1, sticky="e")

        ttk.Label(self.ref_frame, text="Power Factor:", anchor="w").grid(row=3, column=0, sticky="w")
        ttk.Label(self.ref_frame, text=f"{pf:.2f}", anchor="e").grid(row=3, column=1, sticky="e")

        ttk.Label(self.ref_frame, text="Angle φ:", anchor="w").grid(row=4, column=0, sticky="w")
        ttk.Label(self.ref_frame, text=f"{np.degrees(angle):.2f}°", anchor="e").grid(row=4, column=1, sticky="e")

        info_text = "\nThe power factor (PF) evaluates the efficiency of electrical energy use in a system. It is the ratio between active power, which performs useful work, and apparent power, which includes both active and reactive power. Expressed as the cosine of the phase angle between current and voltage, a PF close to 1 indicates high efficiency in energy utilization.. "
    
        
        ttk.Label(self.ref_frame, text=info_text, wraplength=200, justify="left").grid(row=5, column=0, columnspan=2, sticky="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerTriangleSimulation(root)
    root.mainloop()