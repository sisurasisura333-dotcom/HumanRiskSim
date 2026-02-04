import json
import tkinter as tk
from tkinter import ttk, messagebox
from risk_engine import calculate_risk


#  LOAD SCENARIOS
def load_scenarios():
    with open("data/scenarios.json", "r") as file:
        return json.load(file)


scenarios = load_scenarios()


#  RUN SIMULATION
def run_simulation():
    selected = scenario_var.get()

    if not selected:
        messagebox.showerror("Error", "Please select a scenario")
        return

    scenario = scenarios[selected]
    risk_score = scenario["base_risk"]
    risk_level = calculate_risk(risk_score)

    # Color-code risk
    if risk_level == "LOW":
        risk_color = "#28a745"
    elif risk_level == "MEDIUM":
        risk_color = "#ffc107"
    else:
        risk_color = "#dc3545"

    # Clear previous output
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    #  Scenario Box
    scenario_box = tk.Frame(scrollable_frame, bg="#e3f2fd", bd=2, relief="groove", padx=10, pady=10)
    scenario_box.pack(fill="x", pady=5)
    tk.Label(scenario_box, text="Scenario", font=("Arial", 12, "bold"), bg="#e3f2fd").pack(anchor="w")
    tk.Label(scenario_box, text=scenario['name'], font=("Arial", 11), bg="#e3f2fd").pack(anchor="w")

    #  Risk Box with Progress Bar
    risk_box = tk.Frame(scrollable_frame, bg="#fff3cd", bd=2, relief="groove", padx=10, pady=10)
    risk_box.pack(fill="x", pady=5)
    tk.Label(risk_box, text="Risk Score & Level", font=("Arial", 12, "bold"), bg="#fff3cd").pack(anchor="w")

    # Risk Level Text
    tk.Label(risk_box, text=f"{risk_score} | {risk_level}", font=("Arial", 11, "bold"), fg=risk_color,
             bg="#fff3cd").pack(anchor="w", pady=5)

    # Progress bar
    progress = ttk.Progressbar(risk_box, orient="horizontal", length=500, mode="determinate")
    progress.pack(anchor="w", pady=5)
    progress["maximum"] = 100
    progress["value"] = risk_score
    style = ttk.Style()
    style.theme_use('default')
    style.configure("green.Horizontal.TProgressbar", foreground=risk_color, background=risk_color)
    progress.configure(style="green.Horizontal.TProgressbar")

    #  Impact Box with Icon
    impact_box = tk.Frame(scrollable_frame, bg="#f8d7da", bd=2, relief="groove", padx=10, pady=10)
    impact_box.pack(fill="x", pady=5)
    tk.Label(impact_box, text="Impact", font=("Arial", 12, "bold"), bg="#f8d7da").pack(anchor="w")

    # Icon (example emoji or PNG)
    tk.Label(impact_box, text="⚠️", font=("Arial", 18), bg="#f8d7da").pack(anchor="w", side="left")
    tk.Label(impact_box, text=scenario['impact'], font=("Arial", 11), wraplength=520, justify="left",
             bg="#f8d7da").pack(anchor="w", pady=5)

    #  Prevention Box with Icon
    prevention_box = tk.Frame(scrollable_frame, bg="#d4edda", bd=2, relief="groove", padx=10, pady=10)
    prevention_box.pack(fill="x", pady=5)
    tk.Label(prevention_box, text="Prevention", font=("Arial", 12, "bold"), bg="#d4edda").pack(anchor="w")

    # Icon
    tk.Label(prevention_box, text="🛡️", font=("Arial", 18), bg="#d4edda").pack(anchor="w", side="left")
    tk.Label(prevention_box, text=scenario['prevention'], font=("Arial", 11), wraplength=520, justify="left",
             bg="#d4edda").pack(anchor="w", pady=5)

    #  Real-World Insight Box
    insight_box = tk.Frame(scrollable_frame, bg="#fff0f6", bd=2, relief="groove", padx=10, pady=10)
    insight_box.pack(fill="x", pady=5)
    tk.Label(insight_box, text="Real-World Insight", font=("Arial", 12, "bold"), bg="#fff0f6").pack(anchor="w")
    tk.Label(
        insight_box,
        text=f"Based on {scenario['real_world_data']['source']}, this issue appears in approximately {scenario['real_world_data']['breach_percentage']}% of reported breaches.",
        font=("Arial", 11),
        wraplength=520,
        justify="left",
        bg="#fff0f6"
    ).pack(anchor="w")


#  UI SETUP
root = tk.Tk()
root.title("HumanRiskSim – Enterprise Dashboard")
root.geometry("700x650")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="HumanRiskSim", font=("Arial", 22, "bold"))
title_label.pack(pady=10)

subtitle = tk.Label(root, text="Human Error Cyber Attack Simulator (Enterprise Dashboard)", font=("Arial", 11))
subtitle.pack()

# Scenario selection
frame = tk.Frame(root)
frame.pack(pady=15)

tk.Label(frame, text="Select Scenario:", font=("Arial", 11)).grid(row=0, column=0, padx=10)

scenario_var = tk.StringVar()
scenario_dropdown = ttk.Combobox(frame, textvariable=scenario_var, values=list(scenarios.keys()), state="readonly",
                                 width=5)
scenario_dropdown.grid(row=0, column=1)

# Scenario names
scenario_info = tk.Label(root, text="\n".join([f"{k}. {v['name']}" for k, v in scenarios.items()]), justify="left")
scenario_info.pack()

# Run button
run_button = tk.Button(root, text="Run Simulation", command=run_simulation, bg="#2c7be5", fg="white", width=25)
run_button.pack(pady=10)

# Scrollable output frame
output_container = tk.Frame(root, bd=2, relief="sunken")
output_container.pack(fill="both", expand=True, padx=15, pady=10)

canvas = tk.Canvas(output_container, bg="#f4f4f4")
scrollbar = tk.Scrollbar(output_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
