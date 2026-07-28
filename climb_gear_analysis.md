# Analyse Développements × Parcours TPR

> Sources :
> - FIT : `archive/test-rides/2026-06-27-035719-ELEMNT ROAM 72A8-563-0.fit` — données SRAM AXS corrigées
> - GPX : `archive/test-rides/TPRn6 Full v1.gpx`
> - Setup : **pédalier 46/33 · cassette 10-36 · roue 700×40c (dev 2,136 m)**

---

## Partie 1 — Ce que dit la sortie Gumefens-Thun avec ton vrai setup

### Combos réellement utilisées (SRAM AXS, 46/33 × 10-36)

Après décodage des données SRAM Force AXS (12 vitesses) avec ta circonférence de roue (2,136 m) :

| Rapport | Développement | Usage type |
|---|---|---|
| **33×36** | **1,96 m** | Bosses raides (>7%) |
| 33×32 | 2,20 m | Montée soutenue |
| 33×28 | 2,52 m | Montée modérée |
| 33×25 | 2,82 m | Faux plats montants |
| 46×18 | 5,46 m | Plat / faux plat |
| 46×16 | 6,14 m | Plat rapide |
| 46×10 | 9,83 m | Descente |

### Les 4 grosses bosses — en 33×36, le constat brut

````carousel
### Bosse à 7,7% — 6,2 km / 476 m D+ / 35 min

| Métrique | Valeur |
|---|---|
| Puissance moy. | **247 W** |
| Cadence moy. | **70 rpm** |
| FC | 130 bpm |
| Vitesse | 10,7 km/h |

**Temps en 33×36 : 22%** (459s) — les 33% restants en 33×32.
Quand tu étais en 33×36 : **cadence 70 rpm, puissance 244 W, 0% du temps sous 60 rpm.**

✅ Le 33×36 fonctionne correctement à 7,7%. Tu as du headroom.
<!-- slide -->
### Bosse à 10,3% — 7,5 km / 776 m D+ / 55 min ⚠️ LA BOSSE CRITIQUE

| Métrique | Valeur |
|---|---|
| Puissance moy. | **251 W** |
| Cadence moy. | **66 rpm** |
| FC | 134 bpm |
| Vitesse | 8,2 km/h |

**Temps en 33×36 : 57%** (1 896s = 32 min en butée basse).
Quand tu étais en 33×36 : **cadence 66 rpm, puissance 252 W, 8% du temps sous 60 rpm.**

🔴 **Même en 33×36 (ton plus petit rapport), tu es obligé de pousser 250W pour ne pas tomber sous 60 rpm.** C'est la bosse qui justifie ta question.
<!-- slide -->
### Gurnigel à 8,3% — 9,3 km / 776 m D+ / 57 min (30°C, fin de sortie)

| Métrique | Valeur |
|---|---|
| Puissance moy. | **237 W** |
| Cadence moy. | **70 rpm** |
| FC | **144 bpm** |
| Vitesse | 10,0 km/h |

**Temps en 33×36 : 42%** (1 403s = 23 min).
Quand tu étais en 33×36 : **cadence 68 rpm, puissance 248 W, seulement 1% sous 60 rpm.**

🟡 À 8,3% moyen, le 33×36 tient, mais tu es à **cadence moy. 68 rpm avec 248 W** — pas de marge pour baisser la puissance si tu craques en fin d'ultra.
<!-- slide -->
### Bosse d'échauffement à 4,8% — 3,7 km / 177 m D+ / 15 min

| Métrique | Valeur |
|---|---|
| Puissance moy. | **241 W** |
| Cadence moy. | **73 rpm** |
| FC | 131 bpm |
| Vitesse | 14,6 km/h |

**Temps en 33×36 : 33%** — utilisé dans les raidillons.
Quand tu étais en 33×36 : **cadence 67 rpm, puissance 254 W, 3% sous 60 rpm.**

✅ Le 33×36 n'est pas nécessaire ici — tu avais de la marge en 33×32 et 33×28.
````

### Résumé : à quel % de pente le 33×36 te bloque ?

| Pente moy. | Rapport principal | Cadence en 33×36 | Verdict |
|---|---|---|---|
| 4,8% | Mix 33×28-36 | 67 rpm (sections raides) | ✅ OK |
| **7,7%** | 33×32 + 33×36 | **70 rpm à 244 W** | ✅ Ça passe |
| **8,3%** | 33×36 dominant | **68 rpm à 248 W** | 🟡 Juste |
| **10,3%** | **33×36 en butée** | **66 rpm à 252 W** | 🔴 **Bloqué** |

> [!IMPORTANT]
> **Le seuil critique est à ~9-10% de pente.** En dessous, le 33×36 fonctionne. Au-dessus, tu es prisonnier du développement : soit tu pushes ≥250 W pour rester au-dessus de 60 rpm, soit la cadence tombe et le pédalage devient musculaire.

---

## Partie 2 — Le profil de la TPR n6

### Vue d'ensemble

| Métrique | Valeur |
|---|---|
| Distance totale | **~1 865 km** |
| D+ total (estimé GPX) | **~26 800 m** |
| Nombre de montées > 2 km | **71** |
| Km total en montée | **746 km** (40% du parcours) |

### Distribution des pentes sur l'ensemble du parcours

| Catégorie | Km | % du total |
|---|---|---|
| Descente (<-2%) | 404 km | 21,7% |
| Plat (-2 à 2%) | 635 km | 34,0% |
| Faux-plat montant (2-4%) | 282 km | 15,1% |
| Montée modérée (4-6%) | 216 km | 11,6% |
| Montée soutenue (6-8%) | 155 km | 8,3% |
| **Raide (8-10%)** | **97 km** | **5,2%** |
| **Très raide (10-12%)** | **44 km** | **2,3%** |
| **Mur (>12%)** | **32 km** | **1,7%** |

### Répartition du temps de grimpe par catégorie de pente

| Pente | Km dans les montées | % des km de montée | Ton rapport | Cadence type |
|---|---|---|---|---|
| < 4% (replats dans les cols) | ~350 km | 47% | 46×28 à 33×25 | 75-85 rpm ✅ |
| 4-6% | ~120 km | 16% | 33×28 à 33×36 | 70-80 rpm ✅ |
| **6-8%** | ~82 km | **11%** | 33×36 | **68-72 rpm** 🟡 |
| **8-10%** | ~52 km | **7%** | 33×36 (butée) | **62-68 rpm** 🔴 |
| **>10%** | ~25 km | **3%** | 33×36 (butée) | **<62 rpm** 🔴 |

### Les 5 cols les plus gros de la TPR

| # | Km | Dist | D+ | Pente moy. | Km >8% | Km >10% |
|---|---|---|---|---|---|---|
| 1 | 1327→1357 | 29,9 km | 1 567 m | 5,2% | 4,0 km | 2,4 km |
| 2 | 1269→1292 | 22,6 km | 1 194 m | 5,3% | 4,3 km | 2,5 km |
| 3 | 1191→1212 | 21,0 km | 1 153 m | 5,5% | 3,2 km | 1,7 km |
| 4 | 809→827 | 17,9 km | 1 039 m | 5,8% | 3,2 km | 2,0 km |
| 5 | 509→525 | 16,9 km | 1 038 m | 6,2% | 3,2 km | 1,4 km |

> [!NOTE]
> Les gros cols de la TPR sont longs (15-30 km) avec des **pentes moyennes de 4-6%**, mais contiennent des **rampes à 8-12%+ totalisant 3-5 km par col**. C'est dans ces rampes que le développement est critique.

---

## Partie 3 — Croisement : Gumefens × TPR

### Le calcul décisif

Sur la TPR, tu vas passer environ :
- **~82 km à 6-8% de pente** → 33×36 = 68-72 rpm à 230-250 W. **Ça tient.**
- **~52 km à 8-10%** → 33×36 = 62-68 rpm à 230-250 W. **En limite.**
- **~25 km à >10%** → 33×36 en butée, **cadence <62 rpm à 250 W, impossible de baisser la puissance sans tomber sous 55 rpm.**

Mais surtout, sur un ultra de 1 865 km, tu ne seras **pas à 250 W dans les bosses**. L'expérience de la Corsica et du BRM montre un pacing montagne à **200-230 W** en deuxième moitié de course. Et c'est là que le problème s'amplifie :

| Scénario | Puissance | Pente | Vitesse | Cadence 33×36 | Cadence 33×40 | Cadence 33×42 |
|---|---|---|---|---|---|---|
| Début de course (frais) | 250 W | 8% | 9,9 km/h | **84 rpm** ✅ | 94 | 98 |
| Mi-course (fatigué) | 220 W | 8% | 8,7 km/h | **74 rpm** 🟡 | 82 | 86 |
| **Fin de course (cramé)** | **200 W** | **8%** | **7,9 km/h** | **67 rpm** 🔴 | **75** ✅ | **79** ✅ |
| Fin de course | 200 W | 10% | 6,3 km/h | **54 rpm**  | **60 rpm**  | **63 rpm** |
| Fin de course | 200 W | 12% | 5,3 km/h | **45 rpm**  | **50 rpm**  | **52 rpm**  |

> [!WARNING]
> ### Le verdict final
>
> **Le 33×36 est suffisant pour 90% du parcours TPR** (tout ce qui est sous 8% de pente). Mais il te **bloque dans les 77 km à > 8%** — soit environ **5 à 8 heures de pédalage en butée basse** sur l'ensemble de la course, avec un développement musculaire forcé qui te coûte du glycogène et de la récupération à chaque col.
>
> **Un 33×40 ou 33×42 te donnerait 8-12 rpm de marge sur ces sections.** C'est la différence entre pédaler en aérobie et pédaler en force quand tu es cramé au km 1400.

---

## Recommandation

### Ce que tu as : 46/33 × 10-36 — c'est **déjà un bon braquet**

Tu as déjà le braquet le plus court possible sur ce setup avec le 33×36. Le problème est subtil : le 33×36 suffit jusqu'à ~8%, mais pas au-delà à faible puissance.

### Les options réalistes

| Option | Changement | Plus petit dev | Gain à 200W/10% | Coût |
|---|---|---|---|---|
| **A — Ne rien changer** | — | 1,96 m (33×36) | — | 0 € |
| **B — Cassette 10-44** | Cassette XPLR + dérailleur | 1,60 m (33×44) | **+16 rpm** (54→70) | ~300-400 € |
| **C — Plateau 30T** | Plateau intérieur 30T | 1,78 m (30×36) | **+5 rpm** | ~50 € |

### Ma recommandation : **Option A — ne rien changer**

Raisons :

1. **Seulement 3% du parcours TPR est à >10%** (25 km sur 1 865). Le coût mécanique/financier d'un changement de cassette pour 25 km ne se justifie pas.
2. **Les 52 km à 8-10% sont gérables à 62-68 rpm en 33×36** si tu paces correctement (220-240 W, pas 250 W).
3. **La Corsica a prouvé que ta durabilité ne vient pas du développement mais du pacing** — VAM constante sur 28h.
4. **Le risque d'un changement de cassette est la perte de granularité** au milieu de la plage, où tu passes 80% de ton temps.

> [!TIP]
> **Le vrai levier n'est pas le développement, c'est le pacing.** Sur les rampes à >10%, accepte de tomber à 200 W et 55 rpm pendant 3-5 min plutôt que de forcer 250 W pour maintenir la cadence. Sur un ultra de 1 865 km, la micro-gestion de la cadence sur les murs compte beaucoup moins que la gestion du glycogène et de la fatigue neuromusculaire globale.
>
> Si malgré tout tu veux un braquet supplémentaire, un **plateau intérieur 30T** (option C, ~50 €) te donnerait 30×36 = 1,78 m sans toucher à la cassette ni au dérailleur.

---

## Option mono-plateau — Validé (2026-07-13)

### Contexte

2 déraillements avant sur le BRM 1000 lors du passage petit → grand plateau (plateaux Passquest). Sur 1 865 km de TPR avec 30 000 m D+, ce risque mécanique répétitif n'est pas acceptable → décision mono-plateau.

### Fitting session du 13/07 — ce qu'on a appris

**Tests effectués (vélo route, bases ~405 mm soit 2,5 cm plus courtes que le gravel) :**

| Test | Résultat |
|---|---|
| 46T standard BCD110 + Eagle 10-52 | ❌ Déraille sur le grand pignon (pas de narrow-wide) |
| Alugear 40T direct mount + Eagle X01 AXS + 10-52 | ❌ Aucune longueur de chaîne ne convient : N maillons = petits pignons KO ; N-2 = dérailleur en butée sur le 52T |
| Alugear 40T + Eagle X01 AXS + 10-50 | ⚠️ Mieux mais toujours entre deux longueurs de chaîne |
| **Alugear 40T direct mount + XPLR AXS + 10-44** | **✅ Silencieux, indexation parfaite, toutes les vitesses passent** |

**Cause racine :** le dérailleur Eagle (X01 AXS) est conçu pour des bases de 425-450 mm. Sur des bases de ~405 mm, l'enveloppe de travail de la chape ne couvre pas la plage 10-52 ni 10-50 — aucune longueur de chaîne standard ne permet au dérailleur de gérer les deux extrêmes de la cassette. Le dérailleur XPLR est conçu pour des bases courtes (400-425 mm) avec cassette 10-44.

### Setup retenu : XPLR AXS + 40T Alugear direct mount + 10-44

| Config | Braquet le plus bas | Braquet le plus haut | vs 33/36 route |
|---|---|---|---|
| **40T × 10-44 (XPLR)** | **40/44 = 0,909** (1,94 m) | **40/10 = 4,00** (8,54 m) | **+1% plus facile en bas** |
| Ancien 46/33 × 10-36 | 33/36 = 0,917 (1,96 m) | 46/10 = 4,60 (9,83 m) | référence |

### Comparaison grimpe : 40/44 vs 33/36

| Scénario | Puissance | Pente | Vitesse | Cadence 33/36 (0,917) | Cadence 40/44 (0,909) |
|---|---|---|---|---|---|
| Col frais | 250 W | 8% | 9,9 km/h | 84 rpm | **86 rpm** ✅ |
| Col fatigué | 220 W | 8% | 8,7 km/h | 74 rpm | **75 rpm** ✅ |
| Fin de course | 200 W | 8% | 7,9 km/h | 67 rpm | **68 rpm** ✅ |
| Fin de course | 200 W | 10% | 6,3 km/h | 54 rpm | **54 rpm** ⚠️ |
| Fin de course | 200 W | 12% | 5,3 km/h | 45 rpm | **46 rpm** 🔴 |

> [!NOTE]
> **Le 40/44 est quasi-identique au 33/36 en montée** — même expérience de pédalage, même plage de cadence. La grimpe n'est pas sacrifiée.

### Limitation : top-end

40/10 = 4,00 → **spin out à ~46 km/h @90 rpm** (vs 54 km/h avec l'ancien 46/10). Sur un ultra de 1 865 km :
- Cruising plat 35 km/h → 68 rpm ✅
- Plat vent de dos 42 km/h → 82 rpm ✅
- Plat à fond 46 km/h → 90 rpm ⚠️ (max confortable)
- Descente >50 km/h → roue libre (on mange, on s'étire, on récupère)

**Pour la TPR, la limitation top-end est marginale** — on ne soutient pas 50+ km/h sur un ultra.

### Option upgrade : plateau 44T direct mount

Si le test sur les 7 Majeurs révèle une frustration top-end réelle :

| Config | Bas | Haut | Compromis |
|---|---|---|---|
| 40T × 10-44 (actuel) | 0,909 ✅ | 46 km/h @90rpm ⚠️ | Grimpe confortable, plat un peu juste |
| **44T × 10-44** | **1,000** 🟡 (minimum viable cols raides) | **50 km/h @90rpm** ✅ | Plat OK, grimpe serrée sur >10% |

→ Décision finale post-7 Majeurs (25/07).

### Plan de validation

- **7 Majeurs (25/07)** : Rouler la boucle Confrérie (360 km / 11 000 m D+) avec le setup validé 40×10-44 XPLR.
- Points à valider :
  1. Comportement 40/44 dans les rampes >12% (Agnel, Fauniera, Lombarde).
  2. Frustration top-end réelle ou théorique sur les faux-plats et transitions.
  3. Fiabilité mécanique sur 24h continu (zéro déraillement).
  4. Bruit et confort de transmission sur route dégradée / cols italiens.
- Si validé → **configuration officielle TPR.**
- Si top-end frustrant → commander plateau 44T direct mount avant mi-août.
