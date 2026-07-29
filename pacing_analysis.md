# TPRn6 — Analyse de pacing (parcours v1)

> ⚠️ **Calculé sur un brouillon — chiffres à recalculer (2026-07-29).**
> `TPRn6 Full v1.gpx` n'est pas le parcours de course mais un premier jet. La distance, la
> distribution de pentes et donc le **~100 h de roulage** ci-dessous en héritent.
> Le parcours de course est **`TPRn6 Full v2.gpx`** : **1 849,3 km / +34 345 m**, chaîne
> quasi continue, les 3 CP dessus (voir `chain_status.md`). Le modèle de pente donne
> **89,0 h** de roulage **hors pénalité de surface** ; avec les ~58 km de vrai tout-terrain
> recensés dans `surface_and_tyres_v2.md`, compter **~92 à 94 h**. Recalcul :
> `python3 scripts/race/audit_tpr_chain.py --markdown races/2026-tpr-n6/chain_status.md`.
> Le « choix de pneus pour les ~23 km de gravier » plus bas est caduc : voir
> `surface_and_tyres_v2.md`.
> La méthode et les vitesses de référence par tranche de pente restent valables : c'est
> l'entrée GPX qu'il faut changer. À régénérer une fois les liaisons figées.
> Attention aussi à l'usage du **18,8 km/h** : c'est une moyenne de course entière (fatigue
> et gravier compris), pas un plafond applicable à une étape isolée.
> Voir `roadbook-review-2026-07-29.md`.

Combien de km et de dénivelé par jour pour finir en 5, 6 ou 7 jours, avec un
rythme de **18 h de roulage + 6 h de pause** par jour.

## Données de référence

- Parcours : `races/2026-tpr-n6/TPRn6 Full v1.gpx` — **1 902,5 km**, **+32 839 m** D+
  (analysé via `scripts/race/analyze_gpx_osm_surface.py`, seuil 200 m, chunks 15 km).
- Fenêtre course : départ Ven 25 sept (07:00 CEST d'après le race manual,
  à confirmer vs 06:00), cut-off GC Sam 3 oct 23:59 CEST ≈ **8 j 17 h**.
- Surface du tracé : ~62,6 % bitume + ~28 % probablement bitumé (~90 % roulant),
  ~8,3 % non-bitumé/suspect (~158 km), dont le seul vrai point dur gravier au
  **km 514–538** (montée +686 m puis descente -905 m sur gravier).

## Vitesses mesurées sur portions bitumées

Calculées avec `scripts/race/analyze_ride_speed.py` (vitesse **en mouvement**,
stops exclus), par tranche de pente.

- **Course route Corsica (8e solo, 2024, setup ≈ TPR)** — 996 km, 44 h roulage,
  moyenne **22,7 km/h**. Référence principale (TPR ~90 % roulant).
- **555 Gravel Corsica (bitume uniquement)** — 489 km, 26 h roulage,
  moyenne **18,7 km/h**. Référence conservatrice.

| Pente | Route (km/h) | Gravel bitume (km/h) |
|---|---:|---:|
| ≤ -6 % | 45 | 39 |
| -6 à -3 % | 42 | 38 |
| -3 à -1 % | 35 | 31 |
| -1 à +1 % | 29 | 26 |
| +1 à +3 % | 22 | 19 |
| +3 à +6 % | 14,5 | 13 |
| ≥ +6 % | 9,7 | 9,7 |

Détails bruts : `races/2026-tpr-n6/ref_speed_corsica_road.json`,
`races/2026-tpr-n6/ref_speed_corsica_gravel_paved.json`.

## Temps de roulage prévu sur la TPR

Vitesses appliquées à la distribution de pentes du tracé v1 :

| Modèle | Temps roulage | Vit. moy. |
|---|---:|---:|
| Route pur (optimiste, non tenable 5–7 j) | 84 h | 22,6 km/h |
| Route + 12 % fatigue multi-jours + pénalité gravel | ~101 h | ~18,8 km/h |
| Gravel + pénalité gravel | ~99 h | ~19,2 km/h |

**Estimation réaliste retenue : ~100 h de roulage effectif.**

## Objectifs par jour (18 h roulage / 6 h pause)

| Scénario | km/jour | D+/jour | Vit. moy. requise | Roulage réel/jour | Verdict |
|---|---:|---:|---:|---:|---|
| **5 jours** | 380 km | +6 570 m | 21,1 km/h | ~20 h/j | Irréaliste — exige ~20 h/j en mouvement (casse la règle 18 h) à vitesse route fraîche tenue 5 j |
| **6 jours** | 317 km | +5 470 m | 17,6 km/h | ~16,7 h/j | **Cible réaliste** — tient dans la fenêtre 18 h avec ~1,3 h de marge |
| **7 jours** | 272 km | +4 690 m | 15,1 km/h | ~14,3 h/j | Confortable — ~3,7 h de marge/jour (sommeil, météo, mécanique) |

## Conclusion

- ~100 h de roulage placent naturellement la course à **6 jours** avec le rythme
  18 h/6 h (≈ 5,6 j de roulage pur + stops). **Objectif principal : 6 jours.**
- **5 jours** non compatible avec « 18 h de roulage » : il faudrait ~20 h/j en
  mouvement à vitesse de course route fraîche — pas tenable en autosuffisance
  avec 6 h de pause.
- **7 jours** = plan sécurité, vraie marge.
- Les 3 scénarios passent largement le cut-off GC (~8 j 17 h).

### À vérifier / décider

- Heure de départ réelle (07:00 vs 06:00).
- Choix de pneus pour les ~23 km de gravier (km 514–538) avec le setup route.
