import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from evaporateurs import evaporation_triple_effet

Rf = 0.0002

Rf = 0.0002  # résistance thermique due à l’encrassement

def surface_echange(Q, U, DT):
    """Calcule la surface d’échange thermique pour chaque effet"""
    A = []
    for i in range(len(Q)):
        Ueff = 1 / (1/U[i] + Rf)  # corrige U pour encrassement
        surface = Q[i] / (Ueff * DT[i])
        surface = max(surface, 0)  # empêche surface négative
        A.append(surface)
    return A

# ---------- ÉCONOMIE DE VAPEUR ----------
def economie_vapeur(V, S):
    return sum(V) / S

# ---------- ÉTUDE NOMBRE D’EFFETS ----------
def etude_nombre_effets(F, xF, x_out, n_effets):
    economie = 0.9 * n_effets
    surface = 100 * n_effets**0.8
    vapeur = F / economie
    return economie, surface, vapeur

# ---------- ANALYSE DE SENSIBILITÉ ----------
def analyse_sensibilite(param, valeurs, fonction):
    resultats = []
    for v in valeurs:
        resultats.append(fonction(v))
    return resultats

# ---------- COÛTS ----------
def cout_evaporateur(A):
    return 15000 * A**0.65

def cout_echangeur(A):
    return 8000 * A**0.7

def cout_cristalliseur(V):
    return 25000 * V**0.6

def TCI(Cequip):
    return 1.55 * Cequip

def OPEX(S, Pelec):
    vapeur = S * 8000 * 25 / 1000
    elec = Pelec * 8000 * 0.12
    return vapeur + elec

def ROI(TCI, profit):
    return TCI / profit


U = [2500, 2200, 1800]

# ================================
# ANALYSE DE SENSIBILITÉ GÉNÉRALE
# ================================
def sensibilite(param_values, param_name, F, xF, x_out, T_feed, P_base):
    vapeur = []
    surface = []
    temperatures = []

    for v in param_values:
        if param_name == "pression":
            P = [v, 0.6, 0.15]
            F0, x0, T0 = F, xF, T_feed
        elif param_name == "concentration":
            P = P_base
            F0, x0, T0 = F, xF, T_feed
            x_out = v
        elif param_name == "debit":
            P = P_base
            F0, x0, T0 = v, xF, T_feed
        elif param_name == "temperature":
            P = P_base
            F0, x0, T0 = F, xF, v

        L, V, x, T, Q = evaporation_triple_effet(F0, x0, x_out, P, T0)

        S = Q[0] / 2.15e6
        DT = [120-T[0], T[0]-T[1], T[1]-T[2]]
        A = surface_echange(Q, U, DT)

        vapeur.append(S)
        surface.append(sum(A))
        temperatures.append(T)

    return vapeur, surface, temperatures


# ================================
# TRACE DES GRAPHES
# ================================
# ... tes autres fonctions ici ...

# ================================
#import matplotlib.pyplot as plt

def tracer_graphes(param_values, vapeur, surface, temperatures, param_label):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 1 ligne, 3 colonnes

    # Graphe 1 : consommation de vapeur
    axs[0].plot(param_values, vapeur, marker='o', color='blue')
    axs[0].set_xlabel(param_label)
    axs[0].set_ylabel("Consommation de vapeur (kg/h)")
    axs[0].grid(True)
    axs[0].set_title("Vapeur consommée")

    # Graphe 2 : surface totale d'échange
    axs[1].plot(param_values, surface, marker='s', color='orange')
    axs[1].set_xlabel(param_label)
    axs[1].set_ylabel("Surface totale d'échange (m²)")
    axs[1].grid(True)
    axs[1].set_title("Surface totale")

    # Graphe 3 : températures dans chaque effet
    T1 = [T[0] for T in temperatures]
    T2 = [T[1] for T in temperatures]
    T3 = [T[2] for T in temperatures]

    axs[2].plot(param_values, T1, label="Effet 1", marker='o')
    axs[2].plot(param_values, T2, label="Effet 2", marker='s')
    axs[2].plot(param_values, T3, label="Effet 3", marker='^')
    axs[2].set_xlabel(param_label)
    axs[2].set_ylabel("Température (°C)")
    axs[2].legend()
    axs[2].grid(True)
    axs[2].set_title("Températures")

    plt.tight_layout()  # ajuste automatiquement
    plt.show()