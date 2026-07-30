# TPRn6 — surfaces du parcours et choix de pneus

Date : 2026-07-29 · Parcours : `TPRn6 Full v2.gpx` — **1 920,8 km / +34 641 m**, chaîne
continue, 3 CP sur le tracé.
Mesures : **`surface_by_segment.md`**, produit par `scripts/race/analyze_segments.py`
(analyse OSM segment par segment, pas sur le fichier assemblé — voir la note de méthode en
fin de document).
Contrainte posée : **section 32 mm actée**, reste à choisir le type.

## 1. Répartition des surfaces

| Classe | Distance | Part |
|---|---:|---:|
| Bitume explicite | 1 192,7 km | 62,1 % |
| Probablement bitumé (route sans tag `surface`) | 525,3 km | 27,3 % |
| Non bitumé explicite | 61,2 km | 3,2 % |
| Suspect non bitumé (`track`, `path`, `cycleway` sans tag) | 116,4 km | 6,1 % |
| Inconnu | 25,2 km | 1,3 % |
| **Non bitumé au sens large** | **178,0 km** | **9,3 %** |

Et le chiffre qui compte vraiment, parce que c'est lui qui casse des pneus et des clavicules :

| | Distance |
|---|---:|
| **Descente non bitumée à moins de −5 %** | **29,0 km** |
| dont dans les parcours officiels (subi) | 11,6 km |
| dont dans les liaisons (choisi) | 17,4 km |

Pour mémoire, avant la bascule de la liaison 4 sur la route et de la liaison 6 sur l'hybride,
le parcours comptait ~235 km de non bitumé et ~46 km de descente rugueuse. **Les deux
décisions du 29/07 ont retiré 17 km de descente raide**, soit plus d'un tiers.

## 2. Les quatre secteurs qui restent

| km | Long. | Pente | Surface OSM | Où | Statut |
|---:|---:|---:|---|---|---|
| ~379 | **21,4 km** | −1,7 % | `track` / `gravel` | raccourci vers **CP1 Pessonada** | liaison 6 |
| ~1 775 | **6,0 km** | **−7,6 %** | `track` **grade5** | **Toses** (Ripollès) | liaison 14 |
| ~1 732 | 4,4 km | −2,4 % | `track` / `compacted` | dans le RAID | **OFFICIEL** |
| ~1 897 | 17,6 km | −0,5 % | `cycleway` | voie verte d'arrivée sur Gérone | **OFFICIEL** |

Le reste est de la poussière : des sections de 0,5 à 1,5 km, pour l'essentiel des chemins et
voies vertes à faible pente.

**Toses est désormais le pire point du parcours.** 6 km à −7,6 % sur du `track` `grade5` — la
catégorie OSM la plus molle, sans revêtement dur — au **km 1 775 sur 1 920**, c'est-à-dire au
sixième jour, quand la vigilance est au plus bas. C'est le seul secteur du parcours qui
combine longueur, pente forte, mauvaise surface et fatigue maximale.

Le raccourci CP1 est long mais bénin : −1,7 % de moyenne, du `gravel` tagué, et il fait
gagner 45 km. La voie verte de Gérone et le chemin du RAID sont roulants.

## 3. Répartition par segment

Voir `surface_by_segment.md` pour le tableau complet. Les trois segments qui portent le
non bitumé :

| Segment | Distance | Non bitumé | Part | Descente raide |
|---|---:|---:|---:|---:|
| 15. Finish (voie verte de Gérone) | 33,4 km | 20,0 km | **59,8 %** | 0,0 km |
| 14. F to End (**Toses**) | 112,5 km | 24,4 km | 21,7 % | **5,0 km** |
| 1. Start parcours | 103,2 km | 20,0 km | 19,4 % | 2,0 km |
| 6. B to C Hybrid (**raccourci CP1**) | 185,3 km | 28,4 km | 15,3 % | **7,2 km** |
| 13. Parcours F (le RAID) | 577,4 km | 30,0 km | 5,2 % | **7,8 km** |

Les deux extrêmes disent l'essentiel : le Finish est à 60 % non bitumé et ne pose **aucun**
problème (voie verte plate), tandis que le RAID est à 5 % et porte la plus grosse part de
descente raide, en petits morceaux dispersés sur 577 km.

## 4. Ce que ça implique pour le pneu

Avec la section figée à 32 mm, trois paramètres restent ouverts : la sculpture, la carcasse,
le montage.

**Sculpture — semi-slick, pas de slick pur, pas de crampons marqués.**
89 % du parcours est roulant : la résistance au roulement pèse sur un budget de ~92 h, donc
un pneu à crampons pleine largeur coûterait des heures. Mais un slick pur n'a rien à opposer
aux 29 km de descente rugueuse. La cible est une bande centrale lisse ou finement striée avec
des **épaulements dessinés** qui accrochent en appui.

**Carcasse — c'est le critère décisif, avant la sculpture.**
Les modes de défaillance ici ne sont pas « ça glisse » mais « ça coupe » et « ça pince » :
freinage prolongé sur gravier, ornières `grade5` à Toses, cailloux vifs en altitude. Une
carcasse renforcée coûte quelques watts sur toute la course ; une coupure de flanc à Toses
au sixième jour, en autosuffisance, coûte la course. **Prendre la version protégée.**

**Montage — tubeless, non négociable**, avec préventif frais avant le départ, mèches, une
chambre de secours et un pneu pliable + une rustine de flanc. En 32 mm et chargé, la marge
avant pincement est faible : gonfler plutôt bas les jours de gravier que haut « au cas où ».

Trois archétypes, à vérifier en disponibilité 32 mm avant achat :

| Type | Exemple | Pour |
|---|---|---|
| Semi-slick rapide | GravelKing SS | Le meilleur compromis si les descentes sont sèches |
| Centre lisse + épaulements | Pathfinder Pro | Un cran de sécurité en appui, coût faible |
| Crampons légers | GravelKing SK | Uniquement si prévision de pluie sur les Pyrénées |

## 5. Ce qu'il reste à trancher

1. **Décider le type à J−5 sur la météo**, pas maintenant. Le parcours est figé ; c'est
   l'humidité qui fait basculer le verdict.
2. **Tester aux 7 Majeurs (5-6/09)** une longue descente sur chemin, chargé, avec le montage
   de course. C'est le seul moyen de savoir si 32 mm passe à −7,5 % sur du grade5.
3. **Regarder Toses de près.** C'est le seul secteur qui justifierait encore de retoucher une
   liaison. Il occupe les 6 premiers kilomètres de `14.TPRn6 F to End.gpx` sur 112,5 km, donc
   il se modifie localement sans toucher au reste. Aucun contournement court n'existe (le
   routeur rend 4 km de non bitumé pour +6 km), mais une reprise plus en amont est possible.
4. **Croiser avec la liste des routes interdites**, toujours à demander à `tpr@lostdot.cc` :
   plusieurs de ces secteurs sont des pistes forestières dont le statut mérite vérification,
   notamment le raccourci CP1 dans le secteur de Boumort.

## Note de méthode — pourquoi l'analyse est faite par segment

L'analyse OSM tourne désormais **fichier par fichier** (`scripts/race/analyze_segments.py`)
et non sur le GPX assemblé. Trois raisons :

- **Robustesse.** Le fichier global demande ~33 requêtes Overpass en une passe ; un seul refus
  faisait perdre 25 minutes. Par segment, chaque analyse tient en quelques appels et se cache
  indépendamment.
- **Incrémentalité.** Modifier une liaison ne réinvalide que son propre résultat. Le script
  saute les segments dont l'analyse est plus récente que le GPX.
- **Précision.** Les boîtes Overpass sont plus serrées, donc la densité de voies chargées est
  meilleure là où le réseau est dense. Sur le Finish, autour de Gérone, la distance médiane
  entre la trace et la voie OSM retenue tombe de **16 m à 4 m** : l'analyse globale accrochait
  la route parallèle au lieu de la voie verte, et sous-estimait le non bitumé de 6 km sur ce
  seul segment.
