# ================== IMPORTS ==================
from evaporateurs import evaporation_triple_effet
from optimisation import *
from cristallisation import *
from thermodynamique import Thermo

import numpy as np
import matplotlib.pyplot as plt


# ================== DONNÉES ==================
F = 20000
xF = 0.15
x_out = 0.65
x_final = 0.65
T_feed = 85
P_base = [1.5, 0.6, 0.15]
U = [2500, 2200, 1800]


# ================== CALCULS ÉVAPORATION ==================
L, V, x, T, Q = evaporation_triple_effet(F, xF, x_final, P_base, T_feed)

DT = [120 - T[0], T[0] - T[1], T[1] - T[2]]
A = surface_echange(Q, U, DT)

S = abs(Q[0]) / 2.15e6
E = economie_vapeur(V, S)


# ================== AFFICHAGE RÉSULTATS ==================
print("\n===== RÉSULTATS ÉVAPORATION =====\n")
for i in range(3):
    print(f"Effet {i+1}")
    print(f"  Débit liquide L{i+1} = {L[i]:.1f} kg/h")
    print(f"  Vapeur produite V{i+1} = {V[i]:.1f} kg/h")
    print(f"  Concentration x{i+1} = {x[i]*100:.2f} %")
    print(f"  Température T{i+1} = {T[i]:.2f} °C")
    print(f"  Flux thermique Q{i+1} = {Q[i]/1e6:.2f} MW")
    print(f"  Surface A{i+1} = {A[i]:.1f} m²\n")

print("===== PERFORMANCE =====")
print(f"Débit vapeur de chauffe S = {S:.1f} kg/h")
print(f"Économie de vapeur = {E:.2f}")


# ================== OPTIMISATION ==================
print("\n===== OPTIMISATION NOMBRE D’EFFETS =====")
for n in [2, 3, 4, 5]:
    e, s, v = etude_nombre_effets(F, xF, x_out, n)
    print(f"{n} effets : économie={e:.2f}, surface={s:.1f} m², vapeur={v:.1f} kg/h")


# ================== CRISTALLISATION ==================
print("\n===== CRISTALLISATION =====")

t = np.linspace(0, 4*3600, 100)
Tlin = profil_lineaire(t, 70, 35, 4*3600)
C = 75

Slin = sursaturation(C, Tlin)
Glin = croissance(Slin, Tlin)
Blin = nucleation(Slin, 50)

print(f"Sursaturation finale = {Slin[-1]:.3f}")
print(f"Croissance G finale = {Glin[-1]:.2e} m/s")
print(f"Nucléation B finale = {Blin[-1]:.2e}")
print(f"L50 finale = {L50(Glin[-1], t[-1])*1e6:.1f} µm")
print(f"CV = {CV()} %")


# ================== DIMENSIONNEMENT ==================
rho = Thermo.densite(0.65, 60)
Vcr = volume_cristalliseur(5000, rho)
Pagit = puissance_agitation(Vcr)

print("\n===== DIMENSIONNEMENT CRISTALLISEUR =====")
print(f"Volume = {Vcr:.2f} m³")
print(f"Puissance agitation = {Pagit:.1f} W")


# ================== ANALYSE ÉCONOMIQUE ==================
Cev = sum(cout_evaporateur(a) for a in A)
Ccr = cout_cristalliseur(Vcr)

TCI_total = TCI(Cev + Ccr)
opex = OPEX(S, 150)
roi = ROI(TCI_total, 300000)

print("\n===== ANALYSE ÉCONOMIQUE =====")
print(f"TCI = {TCI_total/1e6:.2f} M€")
print(f"OPEX = {opex/1e6:.2f} M€/an")
print(f"ROI = {roi:.2f} ans")


# ================== AFFICHAGE GRAPHIQUE (COMME LA PHOTO) ==================
effets = np.array([1, 2, 3])

plt.figure(figsize=(10, 8))

# Profil de température
plt.subplot(2, 2, 1)
plt.plot(effets, T, 'o-', linewidth=2)
plt.title("Profil de température")
plt.xlabel("Nombre d’effets")
plt.ylabel("Température (°C)")
plt.grid(True)

# Profil de concentration
plt.subplot(2, 2, 2)
plt.plot(effets, np.array(x)*100, 'o-', color='red', linewidth=2)
plt.title("Profil de concentration")
plt.xlabel("Nombre d’effets")
plt.ylabel("Concentration (%)")
plt.grid(True)

# Production de vapeur
plt.subplot(2, 2, 3)
plt.bar(effets, V)
plt.title("Production de vapeur")
plt.xlabel("Nombre d’effets")
plt.ylabel("Vapeur produite (kg/h)")
plt.grid(axis='y')

# Surface d’échange
plt.subplot(2, 2, 4)
plt.bar(effets, A, color='green')
plt.title("Surface d’échange")
plt.xlabel("Nombre d’effets")
plt.ylabel("Surface (m²)")
plt.grid(axis='y')

plt.tight_layout()
plt.show()