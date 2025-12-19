import tkinter as tk
from evaporateurs import TripleEffectEvaporator
from cristallisation import BatchCrystallizer

def run_simulation():
    F = float(entry_F.get())
    xF = float(entry_xF.get())
    TF = float(entry_TF.get())
    xL = float(entry_xL.get())

    evap = TripleEffectEvaporator(F, xF, TF, xL)
    res = evap.energy_balance()

    crist = BatchCrystallizer(5000, xL, 70)
    cr = crist.simulate()

    output.delete(1.0, tk.END)
    output.insert(tk.END, "==== ÉVAPORATION ====\n")
    output.insert(tk.END, f"Vapeur : {res['steam']:.2f} kg/h\n")
    output.insert(tk.END, f"Économie vapeur : {res['economy']:.2f}\n")
    output.insert(tk.END, f"Surfaces : {res['areas']}\n")
    output.insert(tk.END, f"Températures : {res['temperatures']}\n")

    output.insert(tk.END, "\n==== CRISTALLISATION ====\n")
    output.insert(tk.END, f"Cristaux : {cr['crystals']:.2f} kg\n")
    output.insert(tk.END, f"Rendement : {cr['yield']:.2f} %\n")

# FENÊTRE
root = tk.Tk()
root.title("Simulation Évaporation - Cristallisation")

tk.Label(root, text="Débit F (kg/h)").grid(row=0, column=0)
tk.Label(root, text="Concentration entrée (%)").grid(row=1, column=0)
tk.Label(root, text="Température entrée (°C)").grid(row=2, column=0)
tk.Label(root, text="Concentration sortie (%)").grid(row=3, column=0)

entry_F = tk.Entry(root)
entry_xF = tk.Entry(root)
entry_TF = tk.Entry(root)
entry_xL = tk.Entry(root)

entry_F.grid(row=0, column=1)
entry_xF.grid(row=1, column=1)
entry_TF.grid(row=2, column=1)
entry_xL.grid(row=3, column=1)

entry_F.insert(0,"20000")
entry_xF.insert(0,"15")
entry_TF.insert(0,"85")
entry_xL.insert(0,"65")

tk.Button(root, text="Lancer Simulation", command=run_simulation).grid(row=4, column=0, columnspan=2)

output = tk.Text(root, height=15, width=60)
output.grid(row=5, column=0, columnspan=2)

root.mainloop()