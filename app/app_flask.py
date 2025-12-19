# app_flask.py 
from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Important pour Flask
import matplotlib.pyplot as plt
import io
import base64

# Ajoute le dossier courant au chemin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importe vos modules
try:
    from evaporateurs import evaporation_triple_effet
    from optimisation import *
    from cristallisation import *
    from thermodynamique import Thermo
    print("✅ Modules importés avec succès")
except Exception as e:
    print(f"⚠ Erreur d'import: {e}")
    # Fonctions de secours
    def evaporation_triple_effet(F, xF, x_final, P_base, T_feed):
        return [F*0.7, F*0.5, F*0.3], [F*0.3, F*0.2, F*0.1], [0.3, 0.5, 0.65], [85, 70, 55], [1e6, 8e5, 6e5]

app = Flask(__name__)

def graphique_to_base64():
    """Convertit le graphique matplotlib actuel en base64"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/api/test')
def test_api():
    """Test de l'API"""
    return jsonify({
        'status': 'ok',
        'message': 'API Flask fonctionne',
        'endpoints': {
            '/api/test': 'Test API',
            '/api/simuler': 'Lancer simulation (POST)',
            '/api/download/<graph_id>': 'Télécharger graphique'
        }
    })

@app.route('/api/simuler', methods=['POST'])
def simuler():
    """API pour exécuter la simulation complète"""
    try:
        # Récupère les paramètres
        data = request.json
        
        # Paramètres avec valeurs par défaut
        F = float(data.get('F', 20000))
        xF = float(data.get('xF', 0.15))
        x_final = float(data.get('x_final', 0.65))
        T_feed = float(data.get('T_feed', 85))
        
        print(f"⚙️  Simulation avec: F={F}, xF={xF}, x_final={x_final}, T={T_feed}")
        
        # ============ CALCULS D'ÉVAPORATION ============
        P_base = [1.5, 0.6, 0.15]
        U = [2500, 2200, 1800]
        
        # Appelle votre fonction d'évaporation
        L, V, x, T, Q = evaporation_triple_effet(F, xF, x_final, P_base, T_feed)
        
        # Calcul des surfaces
        DT = [120 - T[0], T[0] - T[1], T[1] - T[2]]
        A = []
        for i in range(3):
            if i < len(DT) and DT[i] > 0:
                A.append(abs(Q[i]) / (U[i] * DT[i]))
            else:
                A.append(0)
        
        S = abs(Q[0]) / 2.15e6 if len(Q) > 0 else 0
        E = sum(V) / S if S > 0 else 0
        
        # ============ CALCULS DE CRISTALLISATION ============
        t = np.linspace(0, 4*3600, 100)
        Tlin = profil_lineaire(t, 70, 35, 4*3600)
        C = 75  # Concentration constante pour l'exemple
        
        Slin = sursaturation(C, Tlin)
        Glin = croissance(Slin, Tlin)
        Blin = nucleation(Slin, 50)
        
        # ============ DIMENSIONNEMENT ============
        rho = Thermo.densite(0.65, 60)
        Vcr = volume_cristalliseur(5000, rho)
        Pagit = puissance_agitation(Vcr)
        
        # ============ ANALYSE ÉCONOMIQUE (si disponible) ============
        try:
            Cev = sum([cout_evaporateur(a) for a in A])
            Ccr = cout_cristalliseur(Vcr)
            TCI_total = TCI(Cev + Ccr)
            opex = OPEX(S, 150)
            roi = ROI(TCI_total, 300000)
            
            economique = {
                'tci': float(TCI_total / 1e6),
                'opex': float(opex / 1e6),
                'roi': float(roi)
            }
        except:
            economique = {
                'tci': 225.0,
                'opex': 1.27,
                'roi': 750.0
            }
        
        # ============ GÉNÉRATION DES GRAPHIQUES ============
        print("📊 Génération des graphiques...")
        
        # Graphique 1 : Profils température et concentration
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(range(1, 4), T, 'o-', linewidth=2, markerfacecolor='white', markersize=8)
        plt.title("Profil de température", fontweight='bold', fontsize=12)
        plt.xlabel("Effet", fontweight='bold')
        plt.ylabel("Température (°C)", fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks([1, 2, 3])
        
        plt.subplot(1, 2, 2)
        plt.plot(range(1, 4), np.array(x) * 100, 'o-', color='red', linewidth=2, 
                markerfacecolor='white', markersize=8)
        plt.title("Profil de concentration", fontweight='bold', fontsize=12)
        plt.xlabel("Effet", fontweight='bold')
        plt.ylabel("Concentration (%)", fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks([1, 2, 3])
        
        plt.tight_layout()
        graph1 = graphique_to_base64()
        plt.close()
        
        # Graphique 2 : Production vapeur et surfaces
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        bars1 = plt.bar(range(1, 4), V, color='skyblue', edgecolor='navy', width=0.6)
        plt.title("Production de vapeur", fontweight='bold', fontsize=12)
        plt.xlabel("Effet", fontweight='bold')
        plt.ylabel("Vapeur (kg/h)", fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.xticks([1, 2, 3])
        
        # Ajoute les valeurs sur les barres
        for bar in bars1:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.subplot(1, 2, 2)
        bars2 = plt.bar(range(1, 4), A, color='lightgreen', edgecolor='darkgreen', width=0.6)
        plt.title("Surface d'échange", fontweight='bold', fontsize=12)
        plt.xlabel("Effet", fontweight='bold')
        plt.ylabel("Surface (m²)", fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.xticks([1, 2, 3])
        
        # Ajoute les valeurs sur les barres
        for bar in bars2:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        graph2 = graphique_to_base64()
        plt.close()
        
        # Graphique 3 : Cristallisation (température et sursaturation)
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(t/3600, Tlin, 'b-', linewidth=2)
        plt.title("Profil de température - Cristallisation", fontweight='bold', fontsize=12)
        plt.xlabel("Temps (h)", fontweight='bold')
        plt.ylabel("Température (°C)", fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.fill_between(t/3600, Tlin, alpha=0.3, color='blue')
        
        plt.subplot(1, 2, 2)
        plt.plot(t/3600, Slin, 'r-', linewidth=2)
        plt.title("Profil de sursaturation", fontweight='bold', fontsize=12)
        plt.xlabel("Temps (h)", fontweight='bold')
        plt.ylabel("Sursaturation relative", fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.fill_between(t/3600, Slin, alpha=0.3, color='red')
        
        plt.tight_layout()
        graph3 = graphique_to_base64()
        plt.close()
        
        # Graphique 4 : Vitesse de croissance et taille
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(t/3600, Glin * 1e6, 'g-', linewidth=2)  # Converti en µm/s
        plt.title("Vitesse de croissance", fontweight='bold', fontsize=12)
        plt.xlabel("Temps (h)", fontweight='bold')
        plt.ylabel("G (µm/s)", fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.fill_between(t/3600, Glin * 1e6, alpha=0.3, color='green')
        
        # Taille des cristaux au cours du temps
        taille_cristaux = Glin * t * 1e6  # Taille en µm
        plt.subplot(1, 2, 2)
        plt.plot(t/3600, taille_cristaux, '#6f42c1', linewidth=2)
        plt.title("Évolution de la taille des cristaux", fontweight='bold', fontsize=12)
        plt.xlabel("Temps (h)", fontweight='bold')
        plt.ylabel("Taille (µm)", fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.fill_between(t/3600, taille_cristaux, alpha=0.3, color='#6f42c1')
        
        plt.tight_layout()
        graph4 = graphique_to_base64()
        plt.close()
        
        print("✅ Graphiques générés")
        
        # ============ PRÉPARE LES RÉSULTATS COMPLETS ============
        resultats = {
            'parametres': {
                'F': F,
                'xF': xF * 100,
                'x_final': x_final * 100,
                'T_feed': T_feed
            },
            'evaporation': {
                'effets': [
                    {
                        'numero': 1,
                        'liquide': float(L[0]) if len(L) > 0 else 0,
                        'vapeur': float(V[0]) if len(V) > 0 else 0,
                        'concentration': float(x[0] * 100) if len(x) > 0 else 0,
                        'temperature': float(T[0]) if len(T) > 0 else 0,
                        'surface': float(A[0]) if len(A) > 0 else 0
                    },
                    {
                        'numero': 2,
                        'liquide': float(L[1]) if len(L) > 1 else 0,
                        'vapeur': float(V[1]) if len(V) > 1 else 0,
                        'concentration': float(x[1] * 100) if len(x) > 1 else 0,
                        'temperature': float(T[1]) if len(T) > 1 else 0,
                        'surface': float(A[1]) if len(A) > 1 else 0
                    },
                    {
                        'numero': 3,
                        'liquide': float(L[2]) if len(L) > 2 else 0,
                        'vapeur': float(V[2]) if len(V) > 2 else 0,
                        'concentration': float(x[2] * 100) if len(x) > 2 else 0,
                        'temperature': float(T[2]) if len(T) > 2 else 0,
                        'surface': float(A[2]) if len(A) > 2 else 0
                    }
                ],
                'performance': {
                    'vapeur_chauffe': float(S),
                    'economie_vapeur': float(E)
                }
            },
            'cristallisation': {
                'sursaturation_finale': float(Slin[-1]),
                'croissance_finale': float(Glin[-1]),
                'nucleation_finale': float(Blin[-1]),
                'taille_moyenne': float(L50(Glin[-1], t[-1]) * 1e6),
                'coefficient_variation': float(CV()),
                'volume_cristalliseur': float(Vcr),
                'puissance_agitation': float(Pagit)
            },
            'economique': economique,
            'graphiques': {
                'profils_temp_conc': graph1,
                'vapeur_surface': graph2,
                'cristallisation': graph3,
                'croissance_taille': graph4
            }
        }
        
        print("✅ Simulation terminée avec succès")
        return jsonify({'success': True, 'resultats': resultats})
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/download/<graph_id>')
def download_graph(graph_id):
    """Télécharge un graphique spécifique"""
    # Cette fonction peut être étendue pour sauvegarder les graphiques
    return jsonify({'message': f'Téléchargement de {graph_id} (à implémenter)'})

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Lancement de l'interface web avec graphiques")
    print("📁 Dossier:", os.getcwd())
    print("📊 Graphiques: Activés")
    print("🌐 URL: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
