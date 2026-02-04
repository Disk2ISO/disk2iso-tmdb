"""
disk2iso - TMDB Widget Settings Routes
Stellt die TMDB-Einstellungen bereit (Settings Widget)
"""

import os
import sys
from flask import Blueprint, render_template, jsonify
from i18n import t

# Blueprint für TMDB Settings Widget
tmdb_settings_bp = Blueprint('tmdb_settings', __name__)

def get_tmdb_settings():
    """
    Liest die TMDB-Einstellungen aus der Konfigurationsdatei
    Analog zu get_mqtt_settings() in mqtt_widget_settings.py
    """
    try:
        # Lese Einstellungen aus config.sh
        config_sh = '/opt/disk2iso/conf/config.sh'
        
        config = {
            "tmdb_api_key": "",  # Default: leer
        }
        
        if os.path.exists(config_sh):
            with open(config_sh, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # TMDB_API_KEY
                    if line.startswith('TMDB_API_KEY='):
                        value = line.split('=', 1)[1].strip('"').strip("'")
                        # Entferne Kommentare
                        if '#' in value:
                            value = value.split('#')[0].strip()
                        config['tmdb_api_key'] = value
        
        return config
        
    except Exception as e:
        print(f"Fehler beim Lesen der TMDB-Einstellungen: {e}", file=sys.stderr)
        return {
            "tmdb_api_key": "",
        }


@tmdb_settings_bp.route('/api/widgets/tmdb/settings')
def api_tmdb_settings_widget():
    """
    Rendert das TMDB Settings Widget
    Zeigt TMDB-Einstellungen
    """
    config = get_tmdb_settings()
    
    # Rendere Widget-Template
    return render_template('widgets/tmdb_widget_settings.html',
                         config=config,
                         t=t)
