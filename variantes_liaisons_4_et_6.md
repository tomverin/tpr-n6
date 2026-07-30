# Liaisons 4 et 6 — variantes gravier / route

> **Décision prise le 2026-07-29 : la chaîne utilise `4.TPRn6 A to B Road.gpx` et
> `6.TPRn6 B to C Hybrid.gpx`.** Parcours résultant : **1 920,8 km / +34 641 m, chaîne
> continue, 3 CP sur le tracé** (`chain_status.md`). Les variantes gravier restent dans
> `Stages/` comme plan B par temps sec ; les points de bascule sont décrits plus bas.

Date : 2026-07-29 · Mesures : `scripts/race/audit_tpr_chain.py` (modèle de pente Corse 2024),
routage BRouter pour les compléments. Roulage = jambes fraîches, hors arrêts, **pénalité de
surface incluse** sur les portions non bitumées (descente bridée à 18 km/h, montée à 80 %).

## Liaison 4 — A to B

| Option | Distance | D+ | Roulage | Non bitumé |
|---|---:|---:|---:|---:|
| `4.TPRn6 A to B Gravel.gpx` | 19,5 km | +657 m | 1 h 12 | 7,2 km dont **5,6 km grade4 à −6,3 %** |
| `4.TPRn6 A to B Road.gpx` | 44,2 km | +1 075 m | 2 h 07 | ~0 |
| **Écart** | **+24,6 km** | **+418 m** | **+54 min** | — |

La variante route passe à **317 m de Solsona**. Verdict inchangé : au chrono seul elle ne se
justifie pas, puisque le gravier ne coûte que 11 minutes de pénalité de surface. **Elle se
justifie par le ravitaillement et le couchage** — Solsona est la seule ville entre le km 272
et le km 384, et les deux fins de journée possibles sur l'itinéraire gravier (1 462 m puis
1 317 m) n'ont aucun service. Décision suspendue au découpage en étapes. Détail dans
`surface_and_tyres_v2.md`.

## Liaison 6 — B to C

### Le piège : la variante route ne valide pas CP1

`6.TPRn6 B to C Road.gpx` **passe à 4,80 km de CP1 Pessonada**, en fond de vallée à 520 m,
alors que le CP est à 874 m. La Carretera de Pessonada étant une impasse, il n'existe aucune
boucle : il faut un aller-retour, mesuré au routeur à **24,0 km et +422 m** depuis la
jonction (km 50,0 du fichier route).

**La comparaison n'est donc pas 138 → 205 km, mais 138 → 229 km.**

### Les trois options réelles

| Option | Distance | D+ | Roulage | CP1 | Gravier |
|---|---:|---:|---:|:---:|---:|
| **A.** Gravier intégral (`B to C.gpx`) | 138,8 km | +3 065 m | **7 h 34** | ✅ sur le tracé | 43 km |
| **B.** Route, 1ʳᵉ version | 205,2 km | +2 910 m | 8 h 18 | ❌ **manqué de 4,8 km** | ~0 |
| **B′.** Route corrigée avec l'aller-retour CP1 | 238,0 km | +3 195 m | 9 h 37 | ✅ (99 m) | ~0 |
| **C.** Hybride (`B to C Hybrid.gpx`) | 185,3 km | +2 930 m | **8 h 11** | ✅ sur le tracé | 21 km roulants |

B′ est la version route retracée avec l'aller-retour, mesurée sur le fichier réel. **Elle est
dominée par C sur tous les critères** : −52,7 km, −265 m de D+, −1 h 26, même validation de
CP1, et autant de bitume sur la partie qui compte. Le fichier `B to C Road.gpx` a été retiré
de `Stages/` — l'option route sans gravier n'a pas d'intérêt tant que CP1 impose de monter à
Pessonada.

### L'hybride : découpler les deux décisions

La liaison 6 gravier contient en réalité **deux choix indépendants** que le fichier unique
mélangeait :

1. **Le raccourci CP1** (km 0-23, 21 km de piste roulante à −1,6 %) — c'est un **gain** :
   −45 km et −1 h 22 face au détour bitumé, et il pose CP1 directement sur le tracé.
2. **Le col à 2 006 m** (km 107-139 : 10 km à +6,5 %, puis **12 km de descente à −7,5 % sur
   gravier grade2**) — c'est un **coût** en risque, assumé pour la montagne.

Les deux traces se rejoignent **à un point strictement commun, à la Pobla de Segur, 524 m**
(gravier km 32,7 = route km 52,6, écart mesuré 0 m). L'hybride garde donc le gain et
supprime le coût, sans raccord approximatif.

`6.TPRn6 B to C Hybrid.gpx` est écrit dans `Stages/` (non intégré à la chaîne). Concrètement :
**on prend le gravier jusqu'à CP1, on redescend sur la Pobla de Segur, et on ne quitte plus
le bitume.**

Vérifié par analyse OSM du fichier hybride (`Stages/analysis/6_hybrid_terrain.md`) :

| Classe | Distance | Part |
|---|---:|---:|
| Bitume explicite | 123,0 km | 66,4 % |
| Probablement bitumé | 31,1 km | 16,8 % |
| Non bitumé | 19,4 km | 10,5 % |
| Suspect non bitumé | 9,0 km | 4,9 % |

**Tout le non bitumé est avant la Pobla de Segur.** Après le km 33, l'analyse ne trouve
aucune section non bitumée de plus de 200 m sur les 152 km restants. Les deux seules
sections notables sont le raccourci lui-même (21,4 km de `track` / `gravel` à −1,7 %) et
1,0 km de piste à plat vers le km 30.

### Le vrai arbitrage : A contre C

**40 minutes pour supprimer le col à 2 006 m et ses 12 km de descente à −7,5 % sur gravier.**

C'est une prime d'assurance bon marché, à comparer aux 2 h 00 que coûtait l'option route
telle que sauvegardée. Recommandation :

- **Par temps sec, garder A.** Le col est un morceau de parcours, la descente en gravier
  grade2 est roulante et le modèle intègre déjà sa pénalité. 40 min valent d'être gardées.
- **Par gravier humide, basculer sur C.** Une descente de 12 km à −7,5 % mouillée, en 32 mm
  chargé, à 2 000 m et loin de tout, n'est pas un pari à 40 minutes près. L'hybride garde
  quand même 21 km de piste, mais roulants et à faible pente.
- **Le point de décision est net** : la bifurcation se fait à la Pobla de Segur, au km 384 de
  course, après CP1. On peut donc décider sur place, avec la météo du jour et l'heure réelle.
  Charger les deux traces.

## Effet sur le total de course

| Scénario | Total | Écart |
|---|---:|---:|
| Tout gravier | 1 849,3 km | −71,5 km, −1 h 34 |
| Liaison 4 route seule | 1 873,9 km | −46,9 km, −40 min |
| Liaison 6 hybride seule | 1 895,8 km | −25,0 km, −54 min |
| **Retenu : liaison 4 route + liaison 6 hybride** | **1 920,8 km** | **référence** |

Le parcours retenu coûte **1 h 34 de roulage de plus que la version tout gravier**, pour
supprimer les deux engagements les plus risqués (Navès grade4, col à 2 006 m et ses 12 km à
−7,5 %) et poser Solsona et Ainsa sur le tracé.

À croiser avec les cut-offs — CP2 Sarvisé dim 27/09 16h00, CP3 Orio mar 29/09 09h00, GC sam
03/10 23h59 — au moment de figer le découpage en étapes.

## Points de bascule vers les variantes gravier

Les deux traces gravier restent dans `Stages/` et se prennent à un embranchement net :

| Variante | Point de décision | Gain si prise |
|---|---|---:|
| `4.TPRn6 A to B Gravel.gpx` | fin du Parcours A, km 271,7 | −24,6 km, −54 min |
| `6.TPRn6 B to C.gpx` (col) | la Pobla de Segur, km ~400 après CP1 | −46,5 km, −40 min |

Conditions pour basculer : gravier sec, jour, et retard réel sur le cut-off suivant. Le
raccourci CP1 est commun aux deux versions de la liaison 6, il se prend dans tous les cas.

## Ravitaillement

Points de passage mesurés sur les traces (distance au tracé) :

| Localité | Sur la variante route | Sur l'hybride C | Sur le gravier A |
|---|---:|---|---|
| Isona | 58 m (km 22,3) | non — avant la jonction | non |
| Tremp | 31 m (km 39,5) | non — avant la jonction | non |
| La Pobla de Segur | 29 m (km 52,7) | oui, km ~33 | oui, km ~31 |
| Ainsa | 70 m (km 167,8) | **oui, km ~148** | non |

Les deux options passent par **la Pobla de Segur**, juste après CP1 : le premier vrai
ravitaillement après le Parcours B est donc le même dans les deux cas. La différence est
plus loin — **l'hybride pose Ainsa sur le tracé**, là où le gravier franchit le col et
redescend sur les villages de la vallée de Gistaín. À vérifier avant de figer : ce que Chía
et Plan offrent réellement en horaires d'ouverture, sachant qu'on y arrivera probablement en
soirée.

## Reste à vérifier

- Services et horaires à Chía / Plan sur l'option A, et à Ainsa sur l'option C (relevé
  Overpass à refaire, serveurs saturés au moment de l'analyse).
- Statut des pistes du raccourci CP1 vis-à-vis de la liste des routes interdites, toujours à
  demander à `tpr@lostdot.cc`.
