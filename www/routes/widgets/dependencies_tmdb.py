#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
disk2iso - Dependencies Widget (4x1) - TMDB
============================================================================
Filepath: www/routes/widgets/dependencies_tmdb.py

Beschreibung:
    Flask Blueprint für TMDB-Dependencies-Widget
    - Zeigt TMDB spezifische Software-Abhängigkeiten
    - Nutzt systeminfo_get_software_info() aus libsysteminfo.sh
    - Filtert auf TMDB-spezifische Tools: python-tmdbv3api, requests
============================================================================
"""

from flask import Blueprint, jsonify
import subprocess
import json
import os
from datetime import datetime

# Blueprint erstellen
dependencies_tmdb_bp = Blueprint(
    'dependencies_tmdb',
    __name__,
    url_prefix='/api/widgets/tmdb'
)

# Pfade
INSTALL_DIR = os.environ.get('DISK2ISO_INSTALL_DIR', '/opt/disk2iso')


def get_software_info():
    """
    Ruft Software-Informationen via Bash-Funktion ab
    Nutzt systeminfo_get_software_info() aus libsysteminfo.sh
    """
    try:
        result = subprocess.run(
            ['bash', '-c', f'source {INSTALL_DIR}/lib/libsysteminfo.sh && systeminfo_get_software_info'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        return {}
    except Exception as e:
        print(f"Fehler beim Abrufen von Software-Informationen: {e}")
        return {}


@dependencies_tmdb_bp.route('/dependencies')
def api_dependencies():
    """
    GET /api/widgets/tmdb/dependencies
    Liefert TMDB-spezifische Software-Dependencies
    """
    software_info = get_software_info()
    
    # TMDB-spezifische Tools
    tmdb_tools = ['tmdbv3api', 'python-tmdbv3api', 'requests', 'python-requests']
    
    # Konvertiere Dictionary in flache Liste und filtere TMDB-Tools
    software_list = []
    for category, tools in software_info.items():
        if isinstance(tools, list):
            for tool in tools:
                if tool.get('name') in tmdb_tools:
                    software_list.append(tool)
    
    return jsonify({
        'success': True,
        'software': software_list,
        'timestamp': datetime.now().isoformat()
    })


def register_blueprint(app):
    """Registriert Blueprint in Flask-App"""
    app.register_blueprint(dependencies_tmdb_bp)
