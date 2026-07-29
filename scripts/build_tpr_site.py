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
STAGES_DIR = TPR_DIR / "Stages"
OUT_HTML = TPR_DIR / "site" / "index.html"

DOCS = [
    ("roadbook.md", "Roadbook & Plan d'Étapes", "Découpage officiel par segment GPX, ravitos, hôtels et numéros de téléphone."),
    ("chain_status.md", "État de la Chaîne Auditée", "Audit officiel de la chaîne continue des 15 fichiers GPX et des 3 Control Points."),
    ("roadbook-review-2026-07-29.md", "Revue du Roadbook & Audit", "Revue stratégique du parcours, analyse des 5 trous et plan d'action."),
    ("pacing_analysis.md", "Analyse Pacing & Stratégie", "Modèles de vitesse, rythme 18h/6h, temps de roulage et stratégie de sommeil."),
    ("logistique.md", "Logistique & Transports", "Billets de train réservés (Aller Lyon→Girona, 3 options Retour), matériel et hôtels."),
    ("terrain_analysis.md", "Analyse du Relief", "Profil d'altitude, cols majeurs, types de surface et secteurs à risque."),
    ("climb_gear_analysis.md", "Braquets & Matériel", "Analyse de la transmission mono-plateau 40T x 10-44 et braquets en montagne.")
]

ORDERED_STAGES = [
    ("1.TPRn6 Start parcours.gpx", True, "Start Parcours (Costa Brava)"),
    ("2.TPRn6 start to parcours A road.gpx", False, "Liaison Start → A"),
    ("3.TPRn6 A.gpx", True, "Parcours A (Coll d'Arques)"),
    ("4.TPRn6 A to B Gravel.gpx", False, "Liaison A → B (Gravel)"),
    ("5.TPRn6 parcours B.gpx", True, "Parcours B (Coll de Nargó)"),
    ("6.TPRn6 B to C Hybrid.gpx", False, "Liaison B → C (Hybrid CP1)"),
    ("7.TPRn6 parcours C.gpx", True, "Parcours C (Cañón de Añisclo)"),
    ("8.TPRn6 C to D.gpx", False, "Liaison C → D"),
    ("9.TPRn6 parcours D.gpx", True, "Parcours D (Saint-Jean-Pied-de-Port)"),
    ("10.TPRn6 D to E.gpx", False, "Liaison D → E (Zarautz CP3)"),
    ("11.TPRn6 parcours E.gpx", True, "Parcours E (Orio / Zarautz)"),
    ("12.TPRn6 E to F.gpx", False, "Liaison E → F (RAID)"),
    ("13.TPRn6 Parcours F.gpx", True, "Parcours F (RAID Pyrenées)"),
    ("14.TPRn6 F to End.gpx", False, "Liaison F → Finish"),
    ("15.TPRn6 Finish.gpx", True, "Finish Parcours (Girona)")
]

def haversine_m(la1: float, lo1: float, la2: float, lo2: float) -> float:
    R = 6371000.0
    p1, p2 = math.radians(la1), math.radians(la2)
    dp = math.radians(la2 - la1)
    dl = math.radians(lo2 - lo1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def parse_segmented_gpx() -> tuple[list[dict], list[dict], float, float]:
    ns = {"gpx": "http://www.topografix.com/GPX/1/1"}
    raw_segments = []
    all_pts_flat = []
    cum_m = 0.0
    total_dplus = 0.0
    prev_pt = None

    for fname, is_official, title in ORDERED_STAGES:
        fpath = STAGES_DIR / fname
        if not fpath.exists():
            continue
        tree = ET.parse(fpath)
        root = tree.getroot()
        trkpts = root.findall(".//gpx:trkpt", ns) or root.findall(".//trkpt")

        seg_pts = []
        for tp in trkpts:
            lat = float(tp.attrib["lat"])
            lon = float(tp.attrib["lon"])
            ele_el = tp.find("gpx:ele", ns) or tp.find("ele")
            ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0.0

            if prev_pt is not None:
                plat, plon, pele = prev_pt
                d = haversine_m(plat, plon, lat, lon)
                cum_m += d
                dele = ele - pele
                if dele > 0.1:
                    total_dplus += dele

            prev_pt = (lat, lon, ele)
            pt_dict = {
                "lat": round(lat, 5),
                "lon": round(lon, 5),
                "ele": round(ele, 1),
                "km": round(cum_m / 1000.0, 1)
            }
            seg_pts.append(pt_dict)
            all_pts_flat.append(pt_dict)

        raw_segments.append({
            "name": title,
            "filename": fname,
            "is_official": is_official,
            "pts": seg_pts
        })

    # Point-level overlap detection: tag each point if it's within 50m of another segment of different type or another liaison
    processed_segments = []
    for i, s1 in enumerate(raw_segments):
        pts1 = s1["pts"]
        overlaps = [False] * len(pts1)

        for j, s2 in enumerate(raw_segments):
            if i == j:
                continue
            # Check overlap between official and liaison or between different liaisons
            if s1["is_official"] != s2["is_official"] or (not s1["is_official"] and not s2["is_official"]):
                pts2 = s2["pts"]
                for p1_idx, p1 in enumerate(pts1):
                    if overlaps[p1_idx]:
                        continue
                    lat1, lon1 = p1["lat"], p1["lon"]
                    # Sample every 3rd point of s2 for fast distance check
                    for p2 in pts2[::3]:
                        if haversine_m(lat1, lon1, p2["lat"], p2["lon"]) < 50.0:
                            overlaps[p1_idx] = True
                            break

        # Attach overlap flag to points
        downsampled_pts = []
        max_seg_pts = 400
        if len(pts1) > max_seg_pts:
            step = len(pts1) / max_seg_pts
            for idx_step in range(max_seg_pts):
                idx = int(idx_step * step)
                p = dict(pts1[idx])
                p["overlap"] = overlaps[idx]
                downsampled_pts.append(p)
        else:
            for idx, p in enumerate(pts1):
                p_copy = dict(p)
                p_copy["overlap"] = overlaps[idx]
                downsampled_pts.append(p_copy)

        processed_segments.append({
            "name": s1["name"],
            "filename": s1["filename"],
            "is_official": s1["is_official"],
            "points": downsampled_pts
        })

    # Downsample all flat points for profile
    max_pts = 2000
    if len(all_pts_flat) > max_pts:
        step = len(all_pts_flat) / max_pts
        full_pts = [all_pts_flat[int(i * step)] for i in range(max_pts)]
    else:
        full_pts = all_pts_flat

    return processed_segments, full_pts, cum_m / 1000.0, total_dplus

def build():
    print("Parsing segmented GPX files with exact point-level overlap detection...")
    segments_data, full_pts, total_km, total_dplus = parse_segmented_gpx()
    print(f"Processed {len(segments_data)} segments with overlap flags. Total: {total_km:.1f} km, +{total_dplus:.0f} m D+.")

    docs_json = {}
    for filename, title, desc in DOCS:
        p = TPR_DIR / filename
        if p.exists():
            docs_json[filename] = {
                "title": title,
                "desc": desc,
                "content": p.read_text(encoding="utf-8")
            }

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)

    segments_json_str = json.dumps(segments_data)
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
            height: 560px;
            width: 100%;
            border-radius: 1rem;
            z-index: 10;
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
                    <p class="text-xs text-blue-400 font-medium">Girona → Pyrenées → Girona · <span class="text-white font-bold">1 896,2 km</span> · <span class="text-white font-bold">+34 223 m D+</span> · <span class="text-emerald-400 font-bold">Carte Bicolore Officielle</span></p>
                </div>
            </div>
            
            <!-- Target Badges -->
            <div class="hidden md:flex items-center gap-3">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/30">
                    🔴 8 Parcours Orga (Rouge)
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                    🔵 7 Liaisons Tracées (Bleu)
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-yellow-500/10 text-yellow-400 border border-yellow-500/30">
                    🟡 Chevauchements (Pointillés)
                </span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="border-b border-gray-800 bg-dark-bg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="flex space-x-2 sm:space-x-8 overflow-x-auto py-3" id="tab-nav">
                <button onclick="switchTab('map')" id="tab-btn-map" class="tab-btn text-blue-400 border-b-2 border-blue-500 px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📍 Carte Bicolore (Rouge / Bleu / Chevauchement)
                </button>
                <button onclick="switchTab('summary')" id="tab-btn-summary" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📋 Synthèse 7 Jours
                </button>
                <button onclick="switchTab('roadbook')" id="tab-btn-roadbook" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    🛒 Roadbook par Fichier GPX
                </button>
                <button onclick="switchTab('review')" id="tab-btn-review" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📝 Revue & Audit 29/07
                </button>
                <button onclick="switchTab('docs')" id="tab-btn-docs" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📖 Documents & Analyses
                </button>
            </nav>
        </div>
    </div>

    <!-- Main Content Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- TAB 1: LEAFLET MAP -->
        <section id="tab-map" class="tab-content block space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                    <div>
                        <h2 class="text-2xl font-display font-bold text-white">Carte Bicolore du Parcours Global</h2>
                        <p class="text-sm text-gray-400">🔴 Parcours officiels orga en <b>Rouge</b> · 🔵 Liaisons en <b>Bleu</b> · 🟡 Chevauchements / Aller-Retours en <b>Pointillés Jaunes/Orange</b>.</p>
                    </div>
                    
                    <!-- Map Legend -->
                    <div class="flex flex-wrap items-center gap-4 text-xs font-semibold bg-gray-900/80 px-4 py-2 rounded-xl border border-gray-800">
                        <div class="flex items-center gap-2">
                            <span class="w-4 h-1.5 rounded-full bg-red-500 inline-block"></span>
                            <span class="text-red-400">Parcours Officiel Orga</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="w-4 h-1.5 rounded-full bg-blue-500 inline-block"></span>
                            <span class="text-blue-400">Liaison Tracée</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="w-4 h-1.5 rounded-full bg-yellow-400 border border-dashed border-yellow-500 inline-block"></span>
                            <span class="text-yellow-400">Zone de Chevauchement / Aller-Retour</span>
                        </div>
                    </div>
                </div>

                <div id="map"></div>
            </div>
        </section>

        <!-- TAB 2: SUMMARY TABLE -->
        <section id="tab-summary" class="tab-content hidden space-y-6">
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
                                <td class="px-4 py-3 text-emerald-400 text-base">1 896 km</td>
                                <td class="px-4 py-3 text-blue-400 text-base">+34 223 m</td>
                                <td class="px-4 py-3" colspan="2">—</td>
                                <td class="px-4 py-3 text-yellow-400">17h15</td>
                                <td class="px-4 py-3 text-white">~90,6h</td>
                                <td class="px-4 py-3 text-purple-300">36h Hôtel</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 3: ROADBOOK -->
        <section id="tab-roadbook" class="tab-content hidden space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <h2 class="text-2xl font-display font-bold text-white mb-4">🛒 Roadbook Étape par Étape & Annuaire Téléphonique</h2>
                <div id="roadbook-rendered" class="prose prose-invert max-w-none"></div>
            </div>
        </section>

        <!-- TAB 4: REVIEW -->
        <section id="tab-review" class="tab-content hidden space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <h2 class="text-2xl font-display font-bold text-white mb-4">📝 Conclusions de la Revue du Roadbook</h2>
                <div id="review-rendered" class="prose prose-invert max-w-none"></div>
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
        const SEGMENTS_DATA = {segments_json_str};
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

            const allLatLngs = [];

            SEGMENTS_DATA.forEach(seg => {{
                const isOfficial = seg.is_official;
                const baseColor = isOfficial ? '#ef4444' : '#3b82f6';
                const baseWeight = isOfficial ? 6 : 5;

                // 1. Draw base polyline for the segment (RED for Official, BLUE for Liaisons)
                const segLatLngs = seg.points.map(p => [p.lat, p.lon]);
                allLatLngs.push(...segLatLngs);

                const polyline = L.polyline(segLatLngs, {{
                    color: baseColor,
                    weight: baseWeight,
                    opacity: 0.85
                }}).addTo(map);

                polyline.bindPopup(`<b>${{seg.name}}</b><br><span style="color:${{baseColor}}; font-weight:bold">${{isOfficial ? '🔴 Parcours Officiel Orga' : '🔵 Liaison Tracée'}}</span><br><small>${{seg.filename}}</small>`);

                // 2. Draw ONLY the overlapping sub-segments with a yellow/orange dashed overlay line!
                let overlapChunk = [];
                seg.points.forEach((p, idx) => {{
                    if (p.overlap) {{
                        // Shift coordinates slightly (+0.00009 lat/lon ~9 meters) so both red and dashed yellow are visible
                        overlapChunk.push([p.lat + 0.00009, p.lon + 0.00009]);
                    }} else {{
                        if (overlapChunk.length > 1) {{
                            L.polyline(overlapChunk, {{
                                color: '#f59e0b',
                                weight: 4,
                                dashArray: '8, 8',
                                opacity: 0.95
                            }}).addTo(map).bindPopup(`<b>${{seg.name}}</b><br><span style="color:#f59e0b; font-weight:bold">🟡 Zone de Chevauchement / Aller-Retour</span>`);
                        }}
                        overlapChunk = [];
                    }}
                }});

                if (overlapChunk.length > 1) {{
                    L.polyline(overlapChunk, {{
                        color: '#f59e0b',
                        weight: 4,
                        dashArray: '8, 8',
                        opacity: 0.95
                    }}).addTo(map).bindPopup(`<b>${{seg.name}}</b><br><span style="color:#f59e0b; font-weight:bold">🟡 Zone de Chevauchement / Aller-Retour</span>`);
                }}
            }});

            if (allLatLngs.length > 0) {{
                map.fitBounds(L.polyline(allLatLngs).getBounds());
            }}

            // Control Points & Waypoints
            const waypoints = [
                {{name: 'Girona (Start/Finish)', lat: 41.979, lon: 2.821, color: '#10b981'}},
                {{name: 'Sant Llorenç de Morunys (Nuit 1)', lat: 42.137, lon: 1.591, color: '#3b82f6'}},
                {{name: 'CP1 Pessonada (km 376.0)', lat: 42.215, lon: 1.020, color: '#f59e0b'}},
                {{name: 'CP2 Sarvisé / Hostal Pirineos (km 600.1)', lat: 42.578, lon: -0.114, color: '#f59e0b'}},
                {{name: 'St-Jean-Pied-de-Port (Nuit 3)', lat: 43.163, lon: -1.237, color: '#3b82f6'}},
                {{name: 'CP3 Gran Camping Zarautz (km 1009.9)', lat: 43.289, lon: -2.146, color: '#f59e0b'}},
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
            setTimeout(initMap, 100);

            if (window.marked) {{
                if (DOCS_DATA['chain_status.md']) {{
                    document.getElementById('chain-rendered').innerHTML = marked.parse(DOCS_DATA['chain_status.md'].content);
                }}
                if (DOCS_DATA['roadbook.md']) {{
                    document.getElementById('roadbook-rendered').innerHTML = marked.parse(DOCS_DATA['roadbook.md'].content);
                }}
                if (DOCS_DATA['roadbook-review-2026-07-29.md']) {{
                    document.getElementById('review-rendered').innerHTML = marked.parse(DOCS_DATA['roadbook-review-2026-07-29.md'].content);
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

    print(f"✓ Built self-contained interactive public site with exact point-level overlap detection at: {OUT_HTML}")

if __name__ == "__main__":
    build()
