// static/js/main.js
// Vous pouvez y mettre des fonctions JavaScript réutilisables

console.log('JavaScript principal chargé');

// Fonctions utilitaires
function formatNumber(num, decimals = 2) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(decimals) + ' M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(decimals) + ' k';
    }
    return num.toFixed(decimals);
}

function formatTemperature(temp) {
    return temp.toFixed(1) + ' °C';
}

function formatPercentage(value) {
    return value.toFixed(2) + ' %';
}

// Fonction pour vérifier si l'API est disponible
async function checkAPIHealth() {
    try {
        const response = await fetch('/api/test');
        const data = await response.json();
        return data.status === 'ok';
    } catch (error) {
        console.error('API non disponible:', error);
        return false;
    }
}

// Exporter les fonctions pour une utilisation globale
window.formatNumber = formatNumber;
window.formatTemperature = formatTemperature;
window.formatPercentage = formatPercentage;
window.checkAPIHealth = checkAPIHealth;