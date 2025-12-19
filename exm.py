import matplotlib.pyplot as plt
import numpy as np

# Données
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Créer le graphique
plt.plot(x, y)
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.title('Fonction Sinus')
plt.grid(True)
plt.show()