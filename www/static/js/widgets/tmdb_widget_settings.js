/**
 * disk2iso - TMDB Widget Settings
 * Dynamisches Laden und Verwalten der TMDB-Einstellungen
 * Auto-Save bei Fokus-Verlust (moderne UX)
 */

(function() {
    'use strict';

    /**
     * Lädt das TMDB Settings Widget vom Backend
     */
    async function loadTmdbSettingsWidget() {
        try {
            const response = await fetch('/api/widgets/tmdb/settings');
            if (!response.ok) throw new Error('Failed to load TMDB settings widget');
            return await response.text();
        } catch (error) {
            console.error('Error loading TMDB settings widget:', error);
            return `<div class="error">Fehler beim Laden der TMDB-Einstellungen: ${error.message}</div>`;
        }
    }

    /**
     * Injiziert das TMDB Settings Widget in die Settings-Seite
     */
    async function injectTmdbSettingsWidget() {
        const targetContainer = document.querySelector('#tmdb-settings-container');
        if (!targetContainer) {
            console.warn('TMDB settings container not found');
            return;
        }

        const widgetHtml = await loadTmdbSettingsWidget();
        targetContainer.innerHTML = widgetHtml;
        
        // Event Listener registrieren
        setupEventListeners();
    }

    /**
     * Registriert alle Event Listener für das TMDB Settings Widget
     */
    function setupEventListeners() {
        // TMDB API Key - Auto-Save bei Blur
        const tmdbApiKeyField = document.getElementById('tmdb_api_key');
        if (tmdbApiKeyField) {
            tmdbApiKeyField.addEventListener('blur', function() {
                // Nutzt die zentrale handleFieldChange Funktion aus settings.js
                if (window.handleFieldChange) {
                    window.handleFieldChange({ target: tmdbApiKeyField });
                }
            });
        }
    }

    // Auto-Injection beim Laden der Settings-Seite
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectTmdbSettingsWidget);
    } else {
        injectTmdbSettingsWidget();
    }

})();
