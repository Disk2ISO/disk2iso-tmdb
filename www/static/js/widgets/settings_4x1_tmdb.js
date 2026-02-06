/**
 * disk2iso - Settings Widget (4x1) - TMDB
 * Lädt TMDB Einstellungen dynamisch
 */

let tmdbSaveTimeout = null;

document.addEventListener('DOMContentLoaded', function() {
    // Lade Widget-Content via AJAX
    fetch('/api/widgets/tmdb/settings')
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById('tmdb-settings-container');
            if (container) {
                container.innerHTML = html;
                initTmdbSettingsWidget();
            }
        })
        .catch(error => console.error('Fehler beim Laden der TMDB Settings:', error));
});

function initTmdbSettingsWidget() {
    const activeCheckbox = document.getElementById('tmdb_active');
    const cacheCheckbox = document.getElementById('tmdb_cache_enabled');
    const settingsDiv = document.getElementById('tmdb-settings');
    const cacheSettingsDiv = document.getElementById('tmdb-cache-settings');
    
    if (activeCheckbox) {
        activeCheckbox.addEventListener('change', function() {
            if (settingsDiv) {
                settingsDiv.style.display = this.checked ? 'block' : 'none';
            }
            saveTmdbSettings();
        });
    }
    
    if (cacheCheckbox) {
        cacheCheckbox.addEventListener('change', function() {
            if (cacheSettingsDiv) {
                cacheSettingsDiv.style.display = this.checked ? 'block' : 'none';
            }
            saveTmdbSettings();
        });
    }
    
    // Auto-save bei Änderungen (blur = beim Verlassen des Feldes)
    const apiKeyInput = document.getElementById('tmdb_api_key');
    const cacheDurationInput = document.getElementById('tmdb_cache_duration');
    
    if (apiKeyInput) {
        apiKeyInput.addEventListener('blur', saveTmdbSettings);
    }
    
    if (cacheDurationInput) {
        cacheDurationInput.addEventListener('blur', saveTmdbSettings);
        // Bei Number-Inputs auch bei Enter/Change
        cacheDurationInput.addEventListener('change', saveTmdbSettings);
    }
}

function saveTmdbSettings() {
    // Debounce: Warte 500ms nach letzter Änderung
    if (tmdbSaveTimeout) {
        clearTimeout(tmdbSaveTimeout);
    }
    
    tmdbSaveTimeout = setTimeout(() => {
        saveTmdbSettingsNow();
    }, 500);
}

function saveTmdbSettingsNow() {
    const active = document.getElementById('tmdb_active')?.checked || false;
    const cacheEnabled = document.getElementById('tmdb_cache_enabled')?.checked || false;
    const cacheDuration = parseInt(document.getElementById('tmdb_cache_duration')?.value) || 30;
    const apiKey = document.getElementById('tmdb_api_key')?.value || '';
    
    const data = {
        active: active,
        cache_enabled: cacheEnabled,
        cache_duration_days: cacheDuration,
        api_key: apiKey
    };
    
    fetch('/api/widgets/tmdb/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification('TMDB Einstellungen gespeichert', 'success');
        } else {
            showNotification('Fehler beim Speichern: ' + result.error, 'error');
        }
    })
    .catch(error => {
        console.error('Fehler:', error);
        showNotification('Fehler beim Speichern der Einstellungen', 'error');
    });
}
