import numpy as np
from thermodynamique import Thermo


def evaporation_triple_effet(F, xF, x_final, P, T_feed):
    n = 3

    # Bilans matière
    Lf = F * xF / x_final
    Vtot = F - Lf
    V = [Vtot / n] * n

    L = [F]
    x = [xF]

    for i in range(n):
        L.append(L[i] - V[i])
        x.append(L[i] * x[i] / L[i + 1])

    # Températures
    T = []
    for i in range(n):
        Ts = Thermo.Tsat(P[i])
        T.append(Ts + Thermo.EPE(x[i + 1] * 100))

    # Propriétés thermiques
    lambda_i = [Thermo.chaleur_latente(P[i]) for i in range(n)]
    Cp = [Thermo.Cp_solution(x[i + 1]) for i in range(n)]

    # Bilans énergétiques
    Q = []
    for i in range(n):
        if i == 0:
            Qi = (
                L[1] * Cp[0] * T[0]
                + V[0] * lambda_i[0]
                - F * Thermo.Cp_solution(xF) * T_feed
            ) / 0.97
        else:
            Qi = (V[i - 1] * lambda_i[i - 1]) / 1.03
        Q.append(Qi)

    return L[1:], V, x[1:], T, Q