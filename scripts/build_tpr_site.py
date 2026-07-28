#!/usr/bin/env python3
"""Build a self-contained interactive public web application for TransPyrenees Race No.6.

Outputs: races/2026-tpr-n6/site/index.html
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TPR_DIR = ROOT / "races" / "2026-tpr-n6"
TRACK_GPX = TPR_DIR / "TPRn6 Full v1.gpx"
OUT_HTML = TPR_DIR / "site" / "index.html"

DOCS = [
    ("roadbook.md", "Roadbook & Plan d'Étapes", "Découpage officiel par segment GPX, ravitos, hôtels et numéros de téléphone."),
    ("pacing_analysis.md", "Analyse Pacing & Stratégie", "Modèles de vitesse, rythme 18h/6h, temps de roulage et stratégie de sommeil."),
    ("logistique.md", "Logistique & Transports", "Billets de train réservés (Aller Lyon→Girona, 3 options Retour), matériel et hôtels."),
    ("terrain_analysis.md", "Analyse du Relief", "Profil d'altitude, cols majeurs, types de surface et secteurs à risque."),
    ("climb_gear_analysis.md", "Braquets & Matériel", "Analyse de la transmission mono-plateau 40T x 10-44 et braquets en montagne.")
]

def haversine_m(la1: float, lo1: float, la2: float, lo2: float) -> float:
    R = 6371000.0
    p1, p2 = math.radians(la1), math.radians(la2)
    dp = math.radians(la2 - la1)
    dl = math.radians(lo2 - lo1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def parse_and_downsample_gpx(gpx_path: Path, max_pts: int = 1500) -> list[dict]:
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    ns = {"gpx": "http://www.topografix.com/GPX/1/1"}
    trkpts = root.findall(".//gpx:trkpt", ns) or root.findall(".//trkpt")

    pts = []
    cum_m = 0.0
    prev = None

    for tp in trkpts:
        lat = float(tp.attrib["lat"])
        lon = float(tp.attrib["lon"])
        ele_el = tp.find("gpx:ele", ns) or tp.find("ele")
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0.0
        if prev is not None:
            cum_m += haversine_m(prev[0], prev[1], lat, lon)
        prev = (lat, lon)
        pts.append({"lat": round(lat, 5), "lon": round(lon, 5), "ele": round(ele, 1), "km": round(cum_m / 1000.0, 1)})

    if len(pts) <= max_pts:
        return pts

    step = len(pts) / max_pts
    downsampled = []
    for i in range(max_pts):
        idx = int(i * step)
        downsampled.append(pts[idx])
    if pts and downsampled[-1] != pts[-1]:
        downsampled.append(pts[-1])
    return downsampled

def build():
    print(f"Parsing GPX track: {TRACK_GPX.name}...")
    track_pts = parse_and_downsample_gpx(TRACK_GPX, max_pts=2000)
    print(f"Downsampled track to {len(track_pts)} points.")

    docs_json = {}
    for filename, title, desc in DOCS:
        p = TPR_DIR / filename
        if p.exists():
            docs_json[filename] = {
                "title": title,
                "desc": desc,
                "content": p.read_text(encoding="utf-8")
            }
        else:
            print(f"Warning: missing doc {filename}")

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)

    track_pts_str = json.dumps(track_pts)
    docs_json_str = json.dumps(docs_json)

    html_content = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TransPyrenees Race No. 6 (2026) — Roadbook & Stratégie d'Étapes</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#eff6ff',
                            100: '#dbeafe',
                            500: '#3b82f6',
                            600: '#2563eb',
                            700: '#1d4ed8',
                            900: '#1e3a8a',
                        }},
                        dark: {{
                            bg: '#0b0f19',
                            card: '#151c2c',
                            border: '#232d42'
                        }}
                    }},
                    fontFamily: {{
                        sans: ['Inter', 'sans-serif'],
                        display: ['Outfit', 'sans-serif']
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <!-- Marked Markdown Parser CDN -->
    <script src="https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.parse.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked@12.0.0/lib/marked.umd.js"></script>

    <style>
        body {{
            background-color: #0b0f19;
            color: #f3f4f6;
        }}
        .glass-panel {{
            background: rgba(21, 28, 44, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        #map {{
            height: 520px;
            width: 100%;
            border-radius: 1rem;
            z-index: 10;
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #151c2c;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #3b82f6;
            border-radius: 3px;
        }}
        .prose pre {{
            background-color: #1e293b;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
        }}
        .prose table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }}
        .prose th, .prose td {{
            border: 1px solid #334155;
            padding: 0.5rem 0.75rem;
            text-align: left;
        }}
        .prose th {{
            background-color: #1e293b;
        }}
    </style>
</head>
<body class="font-sans antialiased min-h-screen flex flex-col">

    <!-- Header -->
    <header class="border-b border-gray-800 bg-dark-card/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 font-bold text-xl">
                    🚵‍♂️
                </div>
                <div>
                    <h1 class="text-xl font-display font-bold text-white tracking-wide">TransPyrenees Race No. 6</h1>
                    <p class="text-xs text-blue-400 font-medium">Girona → Pyrenées → Girona · 1 893 km · +32 840 m D+</p>
                </div>
            </div>
            
            <!-- Target Badges -->
            <div class="hidden md:flex items-center gap-3">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    ⏱️ Objectif 6,5 Jours
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                    🛌 6h Sommeil / Nuit
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/30">
                    🚆 All/Ret Trains Réser.
                </span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="border-b border-gray-800 bg-dark-bg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="flex space-x-2 sm:space-x-8 overflow-x-auto py-3" id="tab-nav">
                <button onclick="switchTab('summary')" id="tab-btn-summary" class="tab-btn text-blue-400 border-b-2 border-blue-500 px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📋 Synthèse 7 Jours
                </button>
                <button onclick="switchTab('roadbook')" id="tab-btn-roadbook" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    🛒 Roadbook par GPX
                </button>
                <button onclick="switchTab('map')" id="tab-btn-map" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📍 Carte & Parcours
                </button>
                <button onclick="switchTab('logistics')" id="tab-btn-logistics" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    🚆 Logistique & Trains
                </button>
                <button onclick="switchTab('docs')" id="tab-btn-docs" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📖 Documents & Analyses
                </button>
            </nav>
        </div>
    </div>

    <!-- Main Content Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- TAB 1: SUMMARY TABLE -->
        <section id="tab-summary" class="tab-content block space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <div class="flex items-center justify-between mb-6">
                    <div>
                        <h2 class="text-2xl font-display font-bold text-white">Tableau Synthétique des 7 Étapes</h2>
                        <p class="text-sm text-gray-400">Pacing ultra équilibré (6h de vrai sommeil en hôtel chaque nuit + 2h à 2h45 de pauses ravitos)</p>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm text-gray-300">
                        <thead class="bg-gray-800/60 text-xs uppercase text-gray-400 border-b border-gray-700">
                            <tr>
                                <th class="px-4 py-3 font-semibold">Étape</th>
                                <th class="px-4 py-3 font-semibold">Jour & Date</th>
                                <th class="px-4 py-3 font-semibold">Parcours (Départ → Ville Étape)</th>
                                <th class="px-4 py-3 font-semibold">Distance</th>
                                <th class="px-4 py-3 font-semibold">D+</th>
                                <th class="px-4 py-3 font-semibold">Dépar.</th>
                                <th class="px-4 py-3 font-semibold">Arriv.</th>
                                <th class="px-4 py-3 font-semibold">Pauses</th>
                                <th class="px-4 py-3 font-semibold">Roulage Eff.</th>
                                <th class="px-4 py-3 font-semibold">Nuit Hôtel</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-800">
                            <tr class="hover:bg-gray-800/40 transition">
                                <td class="px-4 py-3 font-bold text-blue-400">E1</td>
                                <td class="px-4 py-3 text-gray-300">Ven 25 sep</td>
                                <td class="px-4 py-3 font-medium text-white">Girona → <span class="text-emerald-400 font-semibold">Sant Llorenç de Morunys</span></td>
                                <td class="px-4 py-3 font-bold text-white">303 km</td>
                                <td class="px-4 py-3 text-blue-400">+5 380 m</td>
                                <td class="px-4 py-3 text-gray-400">07h00</td>
                                <td class="px-4 py-3 font-semibold text-emerald-400">22h45</td>
                                <td class="px-4 py-3 text-gray-400">2h30</td>
                                <td class="px-4 py-3 text-gray-300">~13h15</td>
                                <td class="px-4 py-3 font-medium text-purple-300">6h00</td>
                            </tr>
                            <tr class="hover:bg-gray-800/40 transition">
                                <td class="px-4 py-3 font-bold text-blue-400">E2</td>
                                <td class="px-4 py-3 text-gray-300">Sam 26 sep</td>
                                <td class="px-4 py-3 font-medium text-white">Sant Llorenç → <span class="text-emerald-400 font-semibold">Sarvisé / Broto</span> (CP2)</td>
                                <td class="px-4 py-3 font-bold text-white">271 km</td>
                                <td class="px-4 py-3 text-blue-400">+5 300 m</td>
                                <td class="px-4 py-3 text-gray-400">05h30</td>
                                <td class="px-4 py-3 font-semibold text-emerald-400">22h30</td>
                                <td class="px-4 py-3 text-gray-400">2h30</td>
                                <td class="px-4 py-3 text-gray-300">~14h30</td>
                                <td class="px-4 py-3 font-medium text-purple-300">6h00</td>
                            </tr>
                            <tr class="hover:bg-gray-800/40 transition">
                                <td class="px-4 py-3 font-bold text-blue-400">E3</td>
                                <td class="px-4 py-3 text-gray-300">Dim 27 sep</td>
                                <td class="px-4 py-3 font-medium text-white">Sarvisé → <span class="text-emerald-400 font-semibold">St-Jean-Pied-de-Port</span></td>
                                <td class="px-4 py-3 font-bold text-white">280 km</td>
                                <td class="px-4 py-3 text-blue-400">+4 800 m</td>
                                <td class="px-4 py-3 text-gray-400">05h30</td>
                                <td class="px-4 py-3 font-semibold text-emerald-400">22h45</td>
                                <td class="px-4 py-3 text-gray-400">2h30</td>
                                <td class="px-4 py-3 text-gray-300">~14h45</td>
                                <td class="px-4 py-3 font-medium text-purple-300">6h00</td>
                            </tr>
                            <tr class="hover:bg-gray-800/40 transition">
                                <td class="px-4 py-3 font-bold text-blue-400">E4</td>
                                <td class="px-4 py-3 text-gray-300">Lun 28 sep</td>
                                <td class="px-4 py-3 font-medium text-white">St-Jean-Pied-de-Port → <span class="text-emerald-400 font-semibold">Alsasua</span> (CP3)</td>
                                <td class="px-4 py-3 font-bold text-white">265 km</td>
                                <td class="px-4 py-3 text-blue-400">+4 100 m</td>
                                <td class="px-4 py-3 text-gray-400">05h30</td>
                                <td class="px-4 py-3 font-semibold text-emerald-400">22h15</td>
                                <td class="px-4 py-3 text-gray-400">2h15</td>
                                <td class="px-4 py-3 text-gray-300">~14h30</td>
                                <td class="px-4 py-3 font-medium text-purple-300">6h00</td>
                            </tr>
                            <tr class="hover:bg-gray-800/40 transition">
                                <td class="px-4 py-3 font-bold text-blue-400">E5</td>
                                <td class="px-4 py-3 text-gray-300">Mar 29 sep</td>
                                <td class="px-4 py-3 font-medium text-white">Alsasua → <span class="text-emerald-400 font-semibold">Bagnères-de-Luchon</span></td>
                                <td class="px-4 py-3 font-bold text-white">250 km</td>
                                <td class="px-4 py-3 text-blue-400">+5 800 m</td>
                                <td class="px-4 py-3 text-gray-400">05h30</td>
                                <td class="px-4 py-3 font-semibold text-emerald-400">23h00</td>
                                <td class="px-4 py-3 text-gray-400">2h45</td>
                                <td class="px-4 py-3 text-gray-300">~14h45</td>
                                <td class="px-4 py-3 font-medium text-purple-300">6h00</td>
                            </tr>
                            <tr class="hover:bg-gray-800/40 transition">
                                <td class="px-4 py-3 font-bold text-blue-400">E6</td>
                                <td class="px-4 py-3 text-gray-300">Mer 30 sep</td>
                                <td class="px-4 py-3 font-medium text-white">Luchon → <span class="text-emerald-400 font-semibold">Ripoll / Olot</span></td>
                                <td class="px-4 py-3 font-bold text-white">270 km</td>
                                <td class="px-4 py-3 text-blue-400">+5 200 m</td>
                                <td class="px-4 py-3 text-gray-400">05h30</td>
                                <td class="px-4 py-3 font-semibold text-emerald-400">22h45</td>
                                <td class="px-4 py-3 text-gray-400">2h45</td>
                                <td class="px-4 py-3 text-gray-300">~14h30</td>
                                <td class="px-4 py-3 font-medium text-purple-300">6h00</td>
                            </tr>
                            <tr class="hover:bg-gray-800/40 transition bg-emerald-500/10 border-t-2 border-emerald-500/40">
                                <td class="px-4 py-3 font-bold text-emerald-400">E7</td>
                                <td class="px-4 py-3 text-gray-300 font-semibold">Jeu 01 oct</td>
                                <td class="px-4 py-3 font-bold text-emerald-300">Ripoll → <span class="text-emerald-400 underline">GIRONA FINISH LINE 🏆</span></td>
                                <td class="px-4 py-3 font-bold text-emerald-300">215 km</td>
                                <td class="px-4 py-3 text-blue-400">+2 200 m</td>
                                <td class="px-4 py-3 text-gray-400">05h30</td>
                                <td class="px-4 py-3 font-bold text-emerald-400 text-base">20h00</td>
                                <td class="px-4 py-3 text-gray-400">2h00</td>
                                <td class="px-4 py-3 text-gray-300">~12h30</td>
                                <td class="px-4 py-3 font-bold text-emerald-400">Nuit Girona</td>
                            </tr>
                        </tbody>
                        <tfoot class="bg-gray-800/80 font-bold text-white">
                            <tr>
                                <td class="px-4 py-3 text-blue-400" colspan="3">CUMUL TOTAL (6,5 JOURS)</td>
                                <td class="px-4 py-3 text-emerald-400 text-base">1 854 km</td>
                                <td class="px-4 py-3 text-blue-400 text-base">+32 780 m</td>
                                <td class="px-4 py-3" colspan="2">—</td>
                                <td class="px-4 py-3 text-yellow-400">17h15</td>
                                <td class="px-4 py-3 text-white">~104h</td>
                                <td class="px-4 py-3 text-purple-300">36h Hôtel</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 2: ROADBOOK & HOTELS -->
        <section id="tab-roadbook" class="tab-content hidden space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <h2 class="text-2xl font-display font-bold text-white mb-4">🛒 Roadbook Étape par Étape & Annuaire Téléphonique</h2>
                <div id="roadbook-rendered" class="prose prose-invert max-w-none"></div>
            </div>
        </section>

        <!-- TAB 3: MAP & PROFILE -->
        <section id="tab-map" class="tab-content hidden space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <h2 class="text-2xl font-display font-bold text-white mb-4">📍 Carte Officielle & Parcours</h2>
                <div id="map"></div>
            </div>
        </section>

        <!-- TAB 4: LOGISTICS -->
        <section id="tab-logistics" class="tab-content hidden space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <h2 class="text-2xl font-display font-bold text-white mb-4">🚆 Logistique & Transports Réservez</h2>
                <div id="logistics-rendered" class="prose prose-invert max-w-none"></div>
            </div>
        </section>

        <!-- TAB 5: DOCS VIEWER -->
        <section id="tab-docs" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <div class="glass-panel p-4 rounded-xl space-y-2">
                    <h3 class="text-xs uppercase font-bold text-gray-400 tracking-wider mb-2">Documents Officiels</h3>
                    <div class="space-y-1" id="docs-list"></div>
                </div>
                <div class="lg:col-span-3 glass-panel p-6 rounded-xl">
                    <div id="doc-viewer-rendered" class="prose prose-invert max-w-none"></div>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-800 bg-dark-card mt-auto py-6">
        <div class="max-w-7xl mx-auto px-4 text-center text-xs text-gray-500">
            TransPyrenees Race No.6 (2026) Roadbook & Pacing Dashboard · Généré pour Thomas Vérin
        </div>
    </footer>

    <!-- Script Data & Logic -->
    <script>
        const TRACK_POINTS = {track_pts_str};
        const DOCS_DATA = {docs_json_str};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.classList.remove('text-blue-400', 'border-blue-500');
                el.classList.add('text-gray-400', 'border-transparent');
            }});

            const targetSection = document.getElementById('tab-' + tabId);
            const targetBtn = document.getElementById('tab-btn-' + tabId);
            if (targetSection) targetSection.classList.remove('hidden');
            if (targetBtn) {{
                targetBtn.classList.remove('text-gray-400', 'border-transparent');
                targetBtn.classList.add('text-blue-400', 'border-blue-500');
            }}

            if (tabId === 'map') {{
                setTimeout(initMap, 100);
            }}
        }}

        let mapInitialized = false;
        function initMap() {{
            if (mapInitialized) return;
            mapInitialized = true;

            const map = L.map('map').setView([42.2, 1.8], 8);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 18,
                attribution: '© OpenStreetMap'
            }}).addTo(map);

            const latlngs = TRACK_POINTS.map(p => [p.lat, p.lon]);
            const polyline = L.polyline(latlngs, {{color: '#3b82f6', weight: 4, opacity: 0.85}}).addTo(map);
            map.fitBounds(polyline.getBounds());

            const waypoints = [
                {{name: 'Girona (Start/Finish)', lat: 41.979, lon: 2.821, color: '#10b981'}},
                {{name: 'Sant Llorenç de Morunys (Nuit 1)', lat: 42.137, lon: 1.591, color: '#3b82f6'}},
                {{name: 'CP1 Pessonada (Tremp)', lat: 42.167, lon: 0.895, color: '#f59e0b'}},
                {{name: 'CP2 Cañón de Añisclo / Sarvisé (Nuit 2)', lat: 42.610, lon: 0.050, color: '#f59e0b'}},
                {{name: 'St-Jean-Pied-de-Port (Nuit 3)', lat: 43.163, lon: -1.237, color: '#3b82f6'}},
                {{name: 'CP3 Zarautz / Alsasua (Nuit 4)', lat: 43.285, lon: -2.170, color: '#f59e0b'}},
                {{name: 'Bagnères-de-Luchon / Vielha (Nuit 5)', lat: 42.790, lon: 0.593, color: '#3b82f6'}},
                {{name: 'Ripoll / Olot (Nuit 6)', lat: 42.200, lon: 2.285, color: '#3b82f6'}}
            ];

            waypoints.forEach(wp => {{
                L.circleMarker([wp.lat, wp.lon], {{
                    radius: 7,
                    color: wp.color,
                    fillColor: wp.color,
                    fillOpacity: 0.9
                }}).addTo(map).bindPopup(`<b>${{wp.name}}</b>`);
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            if (window.marked) {{
                if (DOCS_DATA['roadbook.md']) {{
                    document.getElementById('roadbook-rendered').innerHTML = marked.parse(DOCS_DATA['roadbook.md'].content);
                }}
                if (DOCS_DATA['logistique.md']) {{
                    document.getElementById('logistics-rendered').innerHTML = marked.parse(DOCS_DATA['logistique.md'].content);
                }}

                const docsListEl = document.getElementById('docs-list');
                const docKeys = Object.keys(DOCS_DATA);
                
                docKeys.forEach((key, idx) => {{
                    const doc = DOCS_DATA[key];
                    const btn = document.createElement('button');
                    btn.className = idx === 0 
                        ? 'w-full text-left p-3 rounded-lg text-sm transition flex flex-col gap-1 bg-blue-600/20 border border-blue-500/40 text-blue-300'
                        : 'w-full text-left p-3 rounded-lg text-sm transition flex flex-col gap-1 hover:bg-gray-800 text-gray-400';
                    btn.innerHTML = `<span class="font-semibold text-white">${{doc.title}}</span><span class="text-xs text-gray-500">${{doc.desc}}</span>`;
                    btn.onclick = () => {{
                        document.querySelectorAll('#docs-list button').forEach(b => b.className = 'w-full text-left p-3 rounded-lg text-sm transition flex flex-col gap-1 hover:bg-gray-800 text-gray-400');
                        btn.className = 'w-full text-left p-3 rounded-lg text-sm transition flex flex-col gap-1 bg-blue-600/20 border border-blue-500/40 text-blue-300';
                        document.getElementById('doc-viewer-rendered').innerHTML = marked.parse(doc.content);
                    }};
                    docsListEl.appendChild(btn);
                }});

                if (docKeys.length > 0) {{
                    document.getElementById('doc-viewer-rendered').innerHTML = marked.parse(DOCS_DATA[docKeys[0]].content);
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✓ Built self-contained interactive public site at: {OUT_HTML}")

if __name__ == "__main__":
    build()
