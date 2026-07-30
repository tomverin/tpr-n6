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

# Only documents that describe the current route belong here. terrain_analysis.md
# and the 29/07 review carry their own obsolescence banners and pointed at
# replacements that were not published, so the site argued with itself.
DOCS = [
    ("roadbook.md", "Roadbook & plan d'étapes", "Plan en 7 jours, hébergements vérifiés, marges aux cut-off et checklist d'appels."),
    ("chain_status.md", "État de la chaîne auditée", "Audit des 15 fichiers GPX assemblés et position des 3 control points."),
    ("surface_by_segment.md", "Surfaces segment par segment", "Part de non bitumé et descentes raides, mesurées sur OSM segment par segment."),
    ("surface_and_tyres_v2.md", "Surfaces & choix de pneus", "Ce que les 178 km de non bitumé impliquent pour le choix de gomme en 32 mm."),
    ("variantes_liaisons_4_et_6.md", "Variantes liaisons 4 et 6", "Arbitrage gravier contre route, et points de bascule si le temps est sec."),
    ("pacing_analysis.md", "Analyse pacing & stratégie", "Vitesses de référence par tranche de pente et méthode de calcul du temps de roulage."),
    ("climb_gear_analysis.md", "Braquets & matériel", "Transmission mono-plateau 40T x 10-44 et braquets en montagne."),
    ("logistique.md", "Logistique & transports", "Billets de train, réservations, matériel et échéances d'annulation."),
]

ORDERED_STAGES = [
    ("1.TPRn6 Start parcours.gpx", True, "Start Parcours (Costa Brava)"),
    ("2.TPRn6 start to parcours A road.gpx", False, "Liaison Start → A"),
    ("3.TPRn6 A.gpx", True, "Parcours A (Coll d'Arques)"),
    ("4.TPRn6 A to B Road.gpx", False, "Liaison A → B (Solsona)"),
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

import sys  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tpr_chain_guard import check as _check_chain  # noqa: E402
from audit_tpr_chain import (  # noqa: E402
    CONTROL_POINTS,
    build_chain,
    locate_on_chain,
    smooth,
)

_check_chain(ORDERED_STAGES, "build_tpr_site.py")

STAGES_CFG = TPR_DIR / "config" / "stages.json"


def map_markers(total_km: float) -> list[dict]:
    """Start, control points and night stops, placed from the current plan.

    These used to be a hand-written list that still named the night stops of a
    superseded plan and quoted checkpoint kilometres from an older trace, so the
    map contradicted the roadbook it sits next to.
    """
    segments = build_chain()
    start_lat, start_lon, _ = segments[0].points[0]
    markers = [
        {"name": "Girona — Départ / Arrivée", "lat": start_lat, "lon": start_lon,
         "color": "#10b981", "detail": f"km 0 et km {total_km:.0f}"},
    ]
    for name, lat, lon in CONTROL_POINTS:
        hit = locate_on_chain(segments, lat, lon)
        markers.append({
            "name": name, "lat": lat, "lon": lon, "color": "#f59e0b",
            "detail": f"km {hit['cum_km']:.0f}",
        })
    if STAGES_CFG.exists():
        cfg = json.loads(STAGES_CFG.read_text(encoding="utf-8"))
        for night in cfg["nights"]:
            markers.append({
                "name": f"Nuit {night['night']} — {night['name']}",
                "lat": night["lat"], "lon": night["lon"], "color": "#3b82f6",
                "detail": f"km {night['planned_km']:.0f}",
            })
    return markers


def fr_num(value: float, decimals: int = 0) -> str:
    return f"{value:,.{decimals}f}".replace(",", "\u202f").replace(".", ",")


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

    for fname, is_official, title in ORDERED_STAGES:
        fpath = STAGES_DIR / fname
        if not fpath.exists():
            continue
        tree = ET.parse(fpath)
        root = tree.getroot()
        trkpts = root.findall(".//gpx:trkpt", ns) or root.findall(".//trkpt")

        pts_raw = []
        for tp in trkpts:
            lat = float(tp.attrib["lat"])
            lon = float(tp.attrib["lon"])
            # An <ele> element has no children, so it is falsy: `a or b` would
            # always fall through to the un-namespaced lookup and lose elevation.
            ele_el = tp.find("gpx:ele", ns)
            if ele_el is None:
                ele_el = tp.find("ele")
            ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0.0
            pts_raw.append((lat, lon, ele))

        # D+ is summed on the smoothed series, like audit_tpr_chain. The raw GPX
        # series counts sensor noise as climbing and inflates the total by ~20 %:
        # that is how the site advertised +42 063 m and the roadbook +34 641 m
        # for the same route. Points keep their raw altitude for the profile.
        eles_sm = smooth([p[2] for p in pts_raw])

        seg_pts = []
        seg_start_cum = cum_m / 1000.0
        seg_dplus = 0.0

        for i, (lat, lon, ele) in enumerate(pts_raw):
            if i > 0:
                plat, plon, _ = pts_raw[i - 1]
                cum_m += haversine_m(plat, plon, lat, lon)
                dele = eles_sm[i] - eles_sm[i - 1]
                if dele > 0:
                    total_dplus += dele
                    seg_dplus += dele

            rel_k = (cum_m / 1000.0) - seg_start_cum
            pt_dict = {
                "lat": round(lat, 5),
                "lon": round(lon, 5),
                "ele": round(ele, 1),
                "cum_km": round(cum_m / 1000.0, 1),
                "rel_km": round(rel_k, 1)
            }
            seg_pts.append(pt_dict)
            all_pts_flat.append(pt_dict)

        # Downsample points per segment for fast web rendering
        max_seg_pts = 300
        if len(seg_pts) > max_seg_pts:
            step = len(seg_pts) / max_seg_pts
            ds_pts = [seg_pts[int(i * step)] for i in range(max_seg_pts)]
        else:
            ds_pts = seg_pts

        raw_segments.append({
            "name": title,
            "filename": fname,
            "is_official": is_official,
            "dist_km": round((cum_m / 1000.0) - seg_start_cum, 1),
            "dplus_m": round(seg_dplus, 0),
            "start_cum_km": round(seg_start_cum, 1),
            "end_cum_km": round(cum_m / 1000.0, 1),
            "pts": ds_pts
        })

    # Ultra-fast overlap detection on downsampled points
    processed_segments = []
    for i, s1 in enumerate(raw_segments):
        pts1 = s1["pts"]
        overlaps = [False] * len(pts1)

        for j, s2 in enumerate(raw_segments):
            if i == j:
                continue
            if s1["is_official"] != s2["is_official"] or (not s1["is_official"] and not s2["is_official"]):
                pts2 = s2["pts"]
                for p1_idx, p1 in enumerate(pts1):
                    if overlaps[p1_idx]:
                        continue
                    lat1, lon1 = p1["lat"], p1["lon"]
                    for p2 in pts2[::2]:
                        if abs(lat1 - p2["lat"]) < 0.001 and abs(lon1 - p2["lon"]) < 0.001:
                            if haversine_m(lat1, lon1, p2["lat"], p2["lon"]) < 60.0:
                                overlaps[p1_idx] = True
                                break

        final_pts = []
        for idx, p in enumerate(pts1):
            p_copy = dict(p)
            p_copy["overlap"] = overlaps[idx]
            final_pts.append(p_copy)

        processed_segments.append({
            "name": s1["name"],
            "filename": s1["filename"],
            "is_official": s1["is_official"],
            "dist_km": s1["dist_km"],
            "dplus_m": s1["dplus_m"],
            "start_cum_km": s1["start_cum_km"],
            "end_cum_km": s1["end_cum_km"],
            "points": final_pts
        })

    # Downsample flat points for profile
    max_pts = 1500
    if len(all_pts_flat) > max_pts:
        step = len(all_pts_flat) / max_pts
        full_pts = [all_pts_flat[int(i * step)] for i in range(max_pts)]
    else:
        full_pts = all_pts_flat

    return processed_segments, full_pts, cum_m / 1000.0, total_dplus

def build():
    print("Parsing segmented GPX files with mileage markers...")
    segments_data, full_pts, total_km, total_dplus = parse_segmented_gpx()
    print(f"Processed {len(segments_data)} segments. Total: {total_km:.1f} km, +{total_dplus:.0f} m D+.")

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
    markers_json_str = json.dumps(map_markers(total_km), ensure_ascii=False)

    n_official = sum(1 for _, is_official, _ in ORDERED_STAGES if is_official)
    n_liaison = len(ORDERED_STAGES) - n_official
    total_km_str = fr_num(total_km, 1)
    total_dplus_str = fr_num(total_dplus)

    html_content = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TransPyrenees Race No. 6 (2026) — Roadbook Autoritaire & Stratégie d'Étapes</title>
    
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
            height: 580px;
            width: 100%;
            border-radius: 1rem;
            z-index: 10;
        }}
        .km-label-badge {{
            background: rgba(15, 23, 42, 0.92);
            color: #f3f4f6;
            border: 1px solid rgba(59, 130, 246, 0.6);
            padding: 2px 6px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        }}
        .km-label-badge.official {{
            border-color: rgba(239, 68, 68, 0.8);
            color: #fca5a5;
        }}
        .km-label-badge.seg-summary {{
            background: rgba(30, 41, 59, 0.95);
            border: 1.5px solid #3b82f6;
            font-size: 12px;
            color: #ffffff;
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
                    <p class="text-xs text-blue-400 font-medium">Girona → Pyrénées → Girona · <span class="text-white font-bold">{total_km_str} km</span> · <span class="text-white font-bold">+{total_dplus_str} m D+</span> · <span class="text-emerald-400 font-bold">Kilométrage dynamique par zoom</span></p>
                </div>
            </div>
            
            <!-- Target Badges -->
            <div class="hidden md:flex items-center gap-3">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/30">
                    🔴 {n_official} parcours orga
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                    🔵 {n_liaison} liaisons tracées
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    🔍 Bornes KM Dynamiques
                </span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="border-b border-gray-800 bg-dark-bg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="flex space-x-2 sm:space-x-8 overflow-x-auto py-3" id="tab-nav">
                <button onclick="switchTab('roadbook')" id="tab-btn-roadbook" class="tab-btn text-blue-400 border-b-2 border-blue-500 px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📕 Roadbook
                </button>
                <button onclick="switchTab('map')" id="tab-btn-map" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📍 Carte Interactive avec Kilométrage par Zoom
                </button>
                <button onclick="switchTab('docs')" id="tab-btn-docs" class="tab-btn text-gray-400 hover:text-gray-200 border-b-2 border-transparent px-3 py-2 text-sm font-semibold flex items-center gap-2 whitespace-nowrap">
                    📖 Documents & Analyses
                </button>
            </nav>
        </div>
    </div>

    <!-- Main Content Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- TAB 1: ROADBOOK AUTORITAIRE -->
        <section id="tab-roadbook" class="tab-content block space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <div id="roadbook-rendered" class="prose prose-invert max-w-none"></div>
            </div>
        </section>

        <!-- TAB 2: LEAFLET MAP -->
        <section id="tab-map" class="tab-content hidden space-y-6">
            <div class="glass-panel p-6 rounded-2xl">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                    <div>
                        <h2 class="text-2xl font-display font-bold text-white">Carte Interactive avec Kilométrage Dynamique</h2>
                        <p class="text-sm text-gray-400">Le niveau de détail du kilométrage s'adapte automatiquement au zoom (Zoom global : résumés tronçons · Zoom moyen : bornes tous les 20 km · Zoom gros plan : bornes tous les 5 km + altitude).</p>
                    </div>
                    
                    <!-- Map Legend -->
                    <div class="flex flex-wrap items-center gap-4 text-xs font-semibold bg-gray-900/80 px-4 py-2 rounded-xl border border-gray-800">
                        <div class="flex items-center gap-2">
                            <span class="w-4 h-1.5 rounded-full bg-red-500 inline-block"></span>
                            <span class="text-red-400">Parcours Officiel</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="w-4 h-1.5 rounded-full bg-blue-500 inline-block"></span>
                            <span class="text-blue-400">Liaison Tracée</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="w-4 h-1.5 rounded-full bg-yellow-400 border border-dashed border-yellow-500 inline-block"></span>
                            <span class="text-yellow-400">Chevauchement</span>
                        </div>
                    </div>
                </div>

                <div id="map"></div>
            </div>
        </section>

        <!-- TAB 3: DOCS VIEWER -->
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
        const MAP_MARKERS = {markers_json_str};

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
        let kmMarkersLayerGroup = null;

        function initMap() {{
            if (mapInitialized) return;
            mapInitialized = true;

            const map = L.map('map').setView([42.2, 1.8], 8);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 18,
                attribution: '© OpenStreetMap'
            }}).addTo(map);

            kmMarkersLayerGroup = L.layerGroup().addTo(map);

            const allLatLngs = [];

            SEGMENTS_DATA.forEach(seg => {{
                const isOfficial = seg.is_official;
                const baseColor = isOfficial ? '#ef4444' : '#3b82f6';
                const baseWeight = isOfficial ? 6 : 5;

                const segLatLngs = seg.points.map(p => [p.lat, p.lon]);
                allLatLngs.push(...segLatLngs);

                const polyline = L.polyline(segLatLngs, {{
                    color: baseColor,
                    weight: baseWeight,
                    opacity: 0.85
                }}).addTo(map);

                polyline.bindPopup(`<b>${{seg.name}}</b><br><span style="color:${{baseColor}}; font-weight:bold">${{isOfficial ? '🔴 Parcours Officiel Orga' : '🔵 Liaison Tracée'}}</span><br><b>Distance tronçon :</b> ${{seg.dist_km}} km (+${{seg.dplus_m}}m D+)<br><b>Cumul course :</b> km ${{seg.start_cum_km}} → km ${{seg.end_cum_km}}<br><small>${{seg.filename}}</small>`);

                let overlapChunk = [];
                seg.points.forEach(p => {{
                    if (p.overlap) {{
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

            MAP_MARKERS.forEach(wp => {{
                L.circleMarker([wp.lat, wp.lon], {{
                    radius: 7,
                    color: wp.color,
                    fillColor: wp.color,
                    fillOpacity: 0.9
                }}).addTo(map).bindPopup(`<b>${{wp.name}}</b><br>${{wp.detail}}`);
            }});

            // Dynamic Zoom-dependent Mileage Markers logic
            function updateKmMarkers() {{
                kmMarkersLayerGroup.clearLayers();
                const zoom = map.getZoom();

                SEGMENTS_DATA.forEach(seg => {{
                    const pts = seg.points;
                    if (!pts || pts.length === 0) return;

                    // LEVEL 1: Zoom < 9 -> Display segment summary badge at mid-segment
                    if (zoom < 9) {{
                        const midIdx = Math.floor(pts.length / 2);
                        const midPt = pts[midIdx];
                        const icon = L.divIcon({{
                            className: 'km-label-badge seg-summary',
                            html: `${{seg.is_official ? '🔴' : '🔵'}} ${{seg.name.split('(')[0]}}: <b>${{Math.round(seg.dist_km)}} km</b> (+${{Math.round(seg.dplus_m)}}m)`,
                            iconSize: null
                        }});
                        L.marker([midPt.lat, midPt.lon], {{icon: icon}}).addTo(kmMarkersLayerGroup);
                    }}
                    // LEVEL 2: Zoom 9 to 11 -> Display mileage markers every ~20 km
                    else if (zoom >= 9 && zoom < 12) {{
                        let lastKm = -20;
                        pts.forEach(p => {{
                            if (p.rel_km - lastKm >= 20.0 || p.rel_km === 0) {{
                                lastKm = p.rel_km;
                                const icon = L.divIcon({{
                                    className: `km-label-badge ${{seg.is_official ? 'official' : ''}}`,
                                    html: `km ${{Math.round(p.cum_km)}} <small>(+${{Math.round(p.rel_km)}}km)</small>`,
                                    iconSize: null
                                }});
                                L.marker([p.lat, p.lon], {{icon: icon}}).addTo(kmMarkersLayerGroup);
                            }}
                        }});
                    }}
                    // LEVEL 3: Zoom >= 12 -> Display fine-grained mileage markers every 5 km + altitude
                    else if (zoom >= 12) {{
                        let lastKm = -5;
                        pts.forEach(p => {{
                            if (p.rel_km - lastKm >= 5.0 || p.rel_km === 0) {{
                                lastKm = p.rel_km;
                                const icon = L.divIcon({{
                                    className: `km-label-badge ${{seg.is_official ? 'official' : ''}}`,
                                    html: `km ${{Math.round(p.cum_km)}} · ${{Math.round(p.ele)}}m`,
                                    iconSize: null
                                }});
                                L.marker([p.lat, p.lon], {{icon: icon}}).addTo(kmMarkersLayerGroup);
                            }}
                        }});
                    }}
                }});
            }}

            map.on('zoomend', updateKmMarkers);
            updateKmMarkers(); // Initial trigger
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            if (window.marked) {{
                if (DOCS_DATA['roadbook.md']) {{
                    document.getElementById('roadbook-rendered').innerHTML = marked.parse(DOCS_DATA['roadbook.md'].content);
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

    print(f"✓ Built self-contained interactive public site with dynamic zoom mileage markers at: {OUT_HTML}")

if __name__ == "__main__":
    build()
