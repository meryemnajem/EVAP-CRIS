import numpy as np

R = 8.314  # J/(mol·K)

# ---------- SOLUBILITÉ ----------
def solubilite(T):
    """
    Solubilité du saccharose (g/100g solution) en fonction de la température T (°C)
    """
    return 64.18 + 0.1337*T + 5.52e-3*T**2 - 9.73e-6*T**3

def sursaturation(C, T):
    """
    Sursaturation relative S
    C : concentration réelle (g/100g)
    T : température (°C)
    """
    S = (C - solubilite(T)) / solubilite(T)
    # On autorise une faible sursaturation positive pour la zone métastable
    return S

# ---------- CINÉTIQUES ----------
def nucleation(S, mT):
    """
    Taux de nucléation B (noyaux/m³/s)
    S : sursaturation relative
    mT : masse cristallisée (kg/m³)
    """
    S = np.maximum(S, 1e-5)  # sécurité pour éviter 0^b
    return 1.5e10 * S**2.5 * mT**0.5

def croissance(S, T):
    """
    Vitesse de croissance G (m/s)
    S : sursaturation relative
    T : température (°C)
    """
    S = np.maximum(S, 1e-5)  # sécurité pour exponentielle
    return 2.8e-7 * S**1.5 * np.exp(-45000 / (R * (T + 273.15)))

# ---------- PROFILS DE REFROIDISSEMENT ----------
def profil_lineaire(t, T0, Tf, tau):
    """
    Profil linéaire : refroidissement à vitesse constante
    t : temps (s)
    T0 : température initiale
    Tf : température finale
    tau : durée totale (s)
    """
    alpha = (T0 - Tf) / tau
    return T0 - alpha * t

def profil_exponentiel(t, T0, Tf, beta):
    """
    Profil exponentiel : refroidissement rapide initialement
    beta : constante de temps (s^-1)
    """
    return Tf + (T0 - Tf) * np.exp(-beta * t)

# ---------- BILAN DE POPULATION SIMPLIFIÉ ----------
def population_finale(B, G, t):
    """
    Distribution finale de cristaux simplifiée
    """
    # Évite division par zéro
    G_safe = np.maximum(G, 1e-12)
    return B * t / G_safe

def L50(G, t):
    """
    Taille moyenne des cristaux
    """
    return G * t / 2

def CV():
    """
    Coefficient de variation typique
    """
    return 35  # %

# ---------- DIMENSIONNEMENT ----------
def volume_cristalliseur(masse_batch, densite):
    """
    Volume du cristalliseur (m³)
    """
    return masse_batch / densite

def puissance_agitation(V):
    """
    Puissance agitation estimée (W)
    """
    return 5 * V

def surface_serpentin(Q, U, DT):
    """
    Surface nécessaire pour échangeur (m²)
    """
    return Q / (U * DT)

def temps_residence(V, debit):
    """
    Temps de résidence hydraulique (s)
    """
    return V / debit

# ---------- EXEMPLE D'UTILISATION ----------
if __name__ == "__main__":
    # Test des fonctions avec des valeurs d'exemple
    T_test = 50  # °C
    C_test = 80  # g/100g
    
    print("Test des fonctions corrigées:")
    print(f"Solubilité à {T_test}°C: {solubilite(T_test):.2f} g/100g")
    print(f"Sursaturation: {sursaturation(C_test, T_test):.4f}")
    
    S_test = sursaturation(C_test, T_test)
    mT_test = 100  # kg/m³
    
    print(f"Nucléation: {nucleation(S_test, mT_test):.2e} noyaux/m³/s")
    print(f"Croissance: {croissance(S_test, T_test):.2e} m/s")
    
    # Test des profils de température
    t_test = 3600  # 1 heure
    T0_test = 80
    Tf_test = 20
    tau_test = 7200  # 2 heures
    
    print(f"\nProfil linéaire à t={t_test}s: {profil_lineaire(t_test, T0_test, Tf_test, tau_test):.2f}°C")
    print(f"Profil exponentiel (beta=0.001): {profil_exponentiel(t_test, T0_test, Tf_test, 0.001):.2f}°C")