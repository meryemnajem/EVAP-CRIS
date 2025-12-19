from evaporateurs import TripleEffectEvaporator
import numpy as np

def cost_evaporator(A):
    return 15000 * A**0.65

def annual_steam_cost(steam_kg_h):
    return steam_kg_h * 24 * 330 * 25 / 1000

def economic_optimization():

    best_cost = 1e20
    best_flow = 0
    best_result = None

    for F in np.linspace(16000, 24000, 10):
        evap = TripleEffectEvaporator(F, 15, 85, 65)
        res = evap.energy_balance()

        A_total = sum(res["areas"])
        C_inv = cost_evaporator(A_total)
        C_op = annual_steam_cost(res["steam"])
        C_total = C_inv + C_op

        if C_total < best_cost:
            best_cost = C_total
            best_flow = F
            best_result = res

    return best_flow, best_cost, best_result

if __name__ == "__main__":
    Fopt, Copt, res = economic_optimization()

    print("\n====== OPTIMISATION ÉCONOMIQUE ======")
    print("Débit optimal (kg/h):", Fopt)
    print("Coût total minimal (€):", round(Copt,2))
    print("Vapeur consommée (kg/h):", round(res["steam"],2))
    print("Surface totale (m²):", round(sum(res["areas"]),2))