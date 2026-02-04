"""
disk2iso - TMDB Widget Settings Routes
Stellt die TMDB-Einstellungen bereit (Settings Widget)
"""

import os
import sys
import configparser
from flask import Blueprint, render_template, jsonify, request
from i18n import t

# Blueprint für TMDB Settings Widget
tmdb_settings_bp = Blueprint('tmdb_settings', __name__)

def get_tmdb_ini_path():
    """Ermittelt den Pfad zur libtmdb.ini"""
    return '/opt/disk2iso-tmdb/conf/libtmdb.ini'

def get_tmdb_settings():
    """
    Liest die TMDB-Einstellungen aus libtmdb.ini [settings]
    """
    try:
        ini_path = get_tmdb_ini_path()
        
        config = {
            "enabled": True,
            "active": True,
            "cache_enabled": True,
            "cache_duration_days": 30,
            "api_key": ""
        }
        
        if os.path.exists(ini_path):
            parser = configparser.ConfigParser()
            parser.read(ini_path)
            
            if parser.has_section('settings'):
                config['enabled'] = parser.getboolean('settings', 'enabled', fallback=True)
                config['active'] = parser.getboolean('settings', 'active', fallback=True)
                config['cache_enabled'] = parser.getboolean('settings', 'cache_enabled', fallback=True)
                config['cache_duration_days'] = parser.getint('settings', 'cache_duration_days', fallback=30)
                config['api_key'] = parser.get('settings', 'api_key', fallback='')
        
        return config
        
    except Exception as e:
        print(f"Fehler beim Lesen der TMDB-Einstellungen: {e}", file=sys.stderr)
        return {
            "enabled": True,
            "active": True,
            "cache_enabled": True,
            "cache_duration_days": 30,
            "api_key": ""
        }

def save_tmdb_settings(data):
    """
    Speichert TMDB-Einstellungen in libtmdb.ini [settings]
    """
    try:
        ini_path = get_tmdb_ini_path()
        
        if not os.path.exists(ini_path):
            return False, "INI-Datei nicht gefunden"
        
        parser = configparser.ConfigParser()
        parser.read(ini_path)
        
        if not parser.has_section('settings'):
            parser.add_section('settings')
        
        # Aktualisiere Werte
        if 'active' in data:
            parser.set('settings', 'active', 'true' if data['active'] else 'false')
        if 'cache_enabled' in data:
            parser.set('settings', 'cache_enabled', 'true' if data['cache_enabled'] else 'false')
        if 'cache_duration_days' in data:
            parser.set('settings', 'cache_duration_days', str(data['cache_duration_days']))
        if 'api_key' in data:
            parser.set('settings', 'api_key', data['api_key'])
        
        # Schreibe zurück
        with open(ini_path, 'w') as f:
            parser.write(f)
        
        return True, "Einstellungen gespeichert"
        
    except Exception as e:
        return False, str(e)

@tmdb_settings_bp.route('/api/widgets/tmdb/settings', methods=['GET'])
def api_tmdb_settings_widget():
    """
    Rendert das TMDB Settings Widget
    """
    config = get_tmdb_settings()
    
    return render_template('widgets/tmdb_widget_settings.html',
                         config=config,
                         t=t)

@tmdb_settings_bp.route('/api/widgets/tmdb/settings', methods=['POST'])
def api_save_tmdb_settings():
    """
    Speichert TMDB-Einstellungen
    """
    try:
        data = request.get_json()
        success, message = save_tmdb_settings(data)
        
        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
