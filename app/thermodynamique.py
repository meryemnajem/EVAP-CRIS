"""
Module thermodynamique
Propriétés eau / vapeur avec CoolProp
"""

from CoolProp.CoolProp import PropsSI
import numpy as np


class Thermo:

    @staticmethod
    def Tsat(P_bar):
        """Température de saturation (°C)"""
        return PropsSI('T', 'P', P_bar * 1e5, 'Q', 0, 'Water') - 273.15

    @staticmethod
    def chaleur_latente(P_bar):
        """Chaleur latente de vaporisation (J/kg)"""
        h_v = PropsSI('H', 'P', P_bar * 1e5, 'Q', 1, 'Water')
        h_l = PropsSI('H', 'P', P_bar * 1e5, 'Q', 0, 'Water')
        return h_v - h_l

    @staticmethod
    def Cp_solution(x):
        """Cp solution (J/kg.K) – approximation"""
        return 4180 * (1 - 0.3 * x)

    @staticmethod
    def EPE(x):
        """Élévation du point d’ébullition (°C) – approximation"""
        return 0.5 * x


    @staticmethod
    def densite(x, T):
        """
        Densité de la solution (kg/m3)
        x : fraction massique
        T : température (°C)
        """
        return 1000 + 400*x - 0.3*(T - 20)