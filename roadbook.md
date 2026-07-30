# 🚵‍♂️ TransPyrenees Race No. 6 (2026) — Roadbook

> **Généré le 2026-07-30 16:29** par `scripts/race/build_roadbook.py` depuis les 15 GPX de `Stages/` et `config/stages.json`. Ne pas éditer à la main.

- **Distance :** **1921 km**
- **Dénivelé positif :** **+34641 m** (altitude lissée, méthode `audit_tpr_chain`)
- **Discontinuités (> 50 m) :** **aucune — chaîne continue** (mesuré à la génération)
- **Roulage modélisé :** **95.8 h** pénalité de surface comprise (91.8 h sur bitume seul, soit +4.0 h de non-bitume)
- **Control points :** CP1 Pessonada (km 401 · S6 km 23), CP2 Sarvise (km 625 · S8 km 20), CP3 Gran Camping Zarautz (km 1035 · S10 km 149)

> **Deux kilométrages, et ils ne disent pas la même chose.** Le **cumul** est la coordonnée du plan : cut-off, horaires et marges sont construits dessus, et c'est la référence commune avec l'organisation. Le **km de segment**, noté `S6 km 23`, est la coordonnée mesurable : c'est ce qu'affiche le compteur quand le fichier `6.` est chargé. Le second survit à une variante prise ailleurs sur le parcours, le premier non — passer la liaison 6 par la route décale de plusieurs dizaines de kilomètres tous les cumuls en aval, sans toucher au km de segment des étapes suivantes.

---
## 🏆 Découpage en 7 étapes

| Étape | Date | Départ → Arrivée | Distance | Cumul à l'arrivée | D+ | Départ | Arrivée | Pauses | Roulage | Sommeil net |
|---|---|---|---:|---|---:|---|---|---:|---:|---:|
| **E1** | Ven 25 sept. | **Girona (départ) → Solsona** | **292 km** | km 292 · S4 km 20 | +4 892 m | 07h00 | **23h57** | 2h30 | 14h28 | **4h17** |
| **E2** | Sam 26 sept. | **Solsona → Plan** | **271 km** | km 563 · S7 km 0 | +5 053 m | 05h30 | **22h06** | 2h30 | 14h06 | **6h09** |
| **E3** | Dim 27 sept. | **Plan → Saint-Michel / Saint-Jean-Pied-de-Port** | **276 km** | km 839 · S9 km 3 | +4 012 m | 05h30 | **20h00** | 2h00 | 12h30 | **8h15** |
| **E4** | Lun 28 sept. | **Saint-Michel / Saint-Jean-Pied-de-Port → Saint-Jean-de-Luz / Ciboure** | **274 km** | km 1113 · S12 km 59 | +3 571 m | 05h30 | **19h46** | 2h00 | 12h17 | **6h28** |
| **E5** | Mar 29 sept. | **Saint-Jean-de-Luz / Ciboure → Esquièze-Sère / Luz-Saint-Sauveur** | **259 km** | km 1372 · S13 km 174 | +5 713 m | 03h30 | **19h29** | 2h30 | 13h29 | **8h46** |
| **E6** | Mer 30 sept. | **Esquièze-Sère / Luz-Saint-Sauveur → Tarascon-sur-Ariège / Ax-les-Thermes** | **257 km** | km 1629 · S13 km 431 | +6 489 m | 05h30 | **22h14** | 2h30 | 14h15 | **6h00** |
| **E7** | Jeu 1 oct. | **Tarascon-sur-Ariège / Ax-les-Thermes → Girona (arrivée)** | **292 km** | km 1921 · S15 km 33 | +4 912 m | 05h30 | **22h44** | 2h30 | 14h44 | 🏁 |

> Modèle : vitesse par bande de pente (`audit_tpr_chain.SPEED_BY_GRADE`), fatigue +12 %, et pénalité de surface par bac de 200 m (paved ×1.0, unknown_likely_paved ×0.95, suspect_unpaved ×0.8, unpaved ×0.65). Départ 05h30 les jours 2+, sauf E5 à 03h30, 1h15 de logistique hôtel déduite du sommeil.


> ⏰ **Nuit 4 — Saint-Jean-de-Luz / Ciboure : départ 03h30 au lieu de 05h30.** Arrivée 19h46, nuit ramenée à **6h28** ; en échange E5 arrive à **19h29** et la nuit suivante monte à **8h46**, devant E6 et ses +6 489 m.
>
> Partir à 03h30 au lieu de 05h30 déplace deux heures de sommeil de cette nuit vers la nuit 5, juste avant E6 et ses +6 489 m. Le plan d'origine donnait la nuit la plus longue avant la moins dure des trois dernières journées et la plus courte avant la plus dure. E6 est aussi la seule des trois où exploser coûte cher : il reste 292 km derrière. Le départ se fait sur 45 km plats sous 115 m d'altitude, sans descente technique. 03h30 est la limite basse : plus tôt ferait passer cette nuit sous le plancher de 6 h. Suppose un hôtel d'où sortir avec le vélo en pleine nuit — Colbert a un veilleur de 22h à 8h.


### Fichiers GPX à charger, par étape

Le compteur est chargé segment par segment : la distance qu'il affiche est celle du fichier courant, jamais celle de la journée. Ce tableau dit quel fichier ouvrir, à quel cumul basculer, et ce qu'il reste de l'étape à ce moment-là.

| Étape | Fichier | Cumul | Km fichier | Reste de l'étape |
|---|---|---:|---:|---:|
| **E1** | `1.TPRn6 Start parcours.gpx` | 0 | 0 | 292 km |
|  | `2.TPRn6 start to parcours A road.gpx` | 103 | 0 | 188 km |
|  | `3.TPRn6 A.gpx` | 270 | 0 | 22 km |
|  | `4.TPRn6 A to B Road.gpx` | 272 | 0 | 20 km |
| **E2** | `4.TPRn6 A to B Road.gpx` _(reprise)_ | 292 | 20 | 271 km |
|  | `5.TPRn6 parcours B.gpx` | 316 | 0 | 247 km |
|  | `6.TPRn6 B to C Hybrid.gpx` | 377 | 0 | 185 km |
| **E3** | `7.TPRn6 parcours C.gpx` | 563 | 0 | 276 km |
|  | `8.TPRn6 C to D.gpx` | 605 | 0 | 234 km |
|  | `9.TPRn6 parcours D.gpx` | 836 | 0 | 3 km |
| **E4** | `9.TPRn6 parcours D.gpx` _(reprise)_ | 839 | 3 | 274 km |
|  | `10.TPRn6 D to E.gpx` | 886 | 0 | 227 km |
|  | `11.TPRn6 parcours E.gpx` | 1039 | 0 | 74 km |
|  | `12.TPRn6 E to F.gpx` | 1053 | 0 | 59 km |
| **E5** | `12.TPRn6 E to F.gpx` _(reprise)_ | 1113 | 59 | 259 km |
|  | `13.TPRn6 Parcours F.gpx` | 1197 | 0 | 174 km |
| **E6** | `13.TPRn6 Parcours F.gpx` _(reprise)_ | 1372 | 174 | 257 km |
| **E7** | `13.TPRn6 Parcours F.gpx` _(reprise)_ | 1629 | 431 | 292 km |
|  | `14.TPRn6 F to End.gpx` | 1775 | 0 | 146 km |
|  | `15.TPRn6 Finish.gpx` | 1887 | 0 | 33 km |

> ⚠️ **E1** : deux changements de fichier en 2.0 km, aux cumuls 270 et 272 (`3.TPRn6 A.gpx` puis `4.TPRn6 A to B Road.gpx`). Préparer la bascule à l'avance.

> ⚠️ **E3** change de fichier 2.7 km avant l'arrivée (`9.TPRn6 parcours D.gpx`, cumul 836). Ces derniers kilomètres se font aussi bien à vue, sans toucher au compteur.

> ⚠️ **E6** tient entièrement dans `13.TPRn6 Parcours F.gpx` (577 km) : aucune bascule, et donc aucune lecture de la journée sur le compteur. Se repérer au cumul.

---
## 🏬 Hébergement aux villes-étapes

> Relevé OpenStreetMap dans un rayon de 3 km (`find_route_lodging.py`) enrichi par vérification web directe (`config/lodging_enriched.json`). **Présence référencée, pas disponibilité :** ouverture fin septembre et accueil tardif restent à confirmer par téléphone.

### Nuit 1 — Solsona (km 292 · S4 km 20, arrivée Ven 25 sept. 23h57)

| Nom | Type | Écart | Tarif | Téléphone | Accès à l'arrivée | Vélo / petit-déj |
|---|---|---:|---:|---|---|---|
| **Hotel Gran Sol** | hotel | 0.1 km | 60 - 85 € | `+34 973 48 09 75` | 🔑 réception fermée 1.9 h avant — clé ou code à convenir à la réservation | Services cyclotourisme & stockage vélos disponible <br> Restaurant / cafétéria |
| **Hostal Crisami** | hotel | 0.1 km | 45 - 65 € | `+34 973 48 04 13` | 🔑 réception fermée 4.0 h avant — clé ou code à convenir à la réservation | Établissement adapté aux sports de plein air & cyclisme <br> Cafétéria sur place |
| **Sant Roc** | hotel | 0.3 km | 100 - 170 € | `+34 973 48 00 06` · ⚠️ OSM `+34 973484003` · WhatsApp `+34 683 14 75 77` | ✅ réception 24h/24 | Trastero / Local sécurisé pour rangement des vélos <br> Petit-déjeuner dès 07:00 / plateau sur demande |
| **Hotel Solsona Central** | hotel | 0.6 km | — | — | ❓ à appeler | — |
| **Restaurant hotel El Pi** | hotel | 3.0 km | — | — | ❓ à appeler | — |

> ⚠️ **Un seul accueil en direct à 23h57 un vendredi.** Les autres demandent un arrangement préalable.

### Nuit 2 — Plan (km 563 · S7 km 0, arrivée Sam 26 sept. 22h06)

| Nom | Type | Écart | Tarif | Téléphone | Accès à l'arrivée | Vélo / petit-déj |
|---|---|---:|---:|---|---|---|
| **Hotel Mediodía** | hotel | 0.1 km | 50 - 70 € | `+34 974 50 60 06` | ✅ ouvert à l'arrivée | Aparcamiento seguro / Parking sécurisé couvert pour vélos <br> Petit-déjeuner sur place |
| **Apartamentos Villa de Plan** | apartment | 0.1 km | 65 - 90 € | `+34 974 50 64 73` · WhatsApp `+34 676 95 63 40` | ⏳ ferme 24 min après l'arrivée | Appartements autonomes (vélos acceptés à l'intérieur) <br> Cuisine autonome équipée dans chaque appartement |
| **Casa Torres** | apartment | 1.0 km | — | — | ❓ à appeler | — |
| **Hotel Casa Anita Restaurante** | hotel | 1.3 km | — | — | ❓ à appeler | — |

> Replis camping : Refugio de Lavasar (1.9 km).

### Nuit 3 — Saint-Michel / Saint-Jean-Pied-de-Port (km 839 · S9 km 3, arrivée Dim 27 sept. 20h00)

| Nom | Type | Écart | Tarif | Téléphone | Accès à l'arrivée | Vélo / petit-déj |
|---|---|---:|---:|---|---|---|
| **Albergue La Coquille Napoleón** | hostel | 0.0 km | 22 - 35 € | `+33 6 62 25 99 40` | ❓ horaires non chiffrés | Gîte d'étape sur la Route Napoléon <br> Formule gîte d'étape |
| **Albergue Ferme Ithurburia** | hostel | 0.0 km | — | `+33 559371117` | ❓ à appeler | — |
| **Maison Kaserna** | hostel | 0.1 km | 25 - 40 € | `+33 5 59 37 65 17` | ⛔ vélos refusés | ⚠️ ATTENTION : Refuge paroissial réservé EXCLUSIVEMENT aux pèlerins à pied (VÉLOS NON ACCEPTÉS) <br> Demi-pension gîte |
| **Villa Goxoki** | hostel | 0.1 km | — | `+33 6 73 89 49 21` | ❓ à appeler | — |
| **Maison Donamaria** | guest_house | 0.3 km | — | `+33559370232;+33661902921` | ❓ à appeler | — |
| **Xoko Goxoa** | hotel | 1.3 km | — | `+33 5 59 37 06 34` | ❓ à appeler | — |
| **Hôtel des Remparts (SJPdP)** | hors OSM | — | 65 - 85 € | `+33 5 59 37 13 79` · WhatsApp `+33 6 76 12 28 58` | ❓ horaires non chiffrés | Local matériel fermé & sécurisé pour vélos <br> Petit-déjeuner hôtel |

> Les 1 dernière(s) ligne(s) viennent de la vérification manuelle sans correspondance dans le relevé OSM : écart à la trace non mesuré.

> Replis camping : Camping Municipal Plaza Berri (0.2 km), Gite Zazpiak-Bat (0.2 km), Gîte Urondoa (1.6 km).

> ❓ **Aucun horaire chiffré pour cette étape** : rien ne dit si quelqu'un accueille à 20h00 un dimanche. À régler au téléphone.

### Nuit 4 — Saint-Jean-de-Luz / Ciboure (km 1113 · S12 km 59, arrivée Lun 28 sept. 19h46)

| Nom | Type | Écart | Tarif | Téléphone | Accès à l'arrivée | Vélo / petit-déj |
|---|---|---:|---:|---|---|---|
| **La Caravelle** | hotel | 0.0 km | — | `+33 5 59 47 18 05` | ❓ à appeler | — |
| **Hôtel de Paris** | hotel | 0.0 km | 64 € (chambre double) | `+33 5 59 85 20 20` | ⏳ ferme 14 min après l'arrivée | Garage sécurisé pour les vélos (référencé accueil vélo) <br> Buffet 07h30–10h30 — après le départ prévu, prévoir la veille |
| **Hôtel Le relais de Saint Jacques** | hotel | 0.0 km | à partir de 133 € | `+33 5 59 26 02 55` | 🔑 réception fermée 0.8 h avant — clé ou code à convenir à la réservation | Rangements pour vélos ; parking hôtel sur réservation 20 €, ou parking gratuit de 450 places derrière la gare <br> Bouilloire en chambre ; petit-déjeuner après le départ prévu, prévoir la veille |
| **Hôtel Colbert** | hotel | 0.0 km | — | `+33 5 59 26 31 99` | ✅ réception 24h/24 | Vélo entreposé au sous-sol sur demande (confirmé par la réception) + bagagerie fermée à clé 24h/24 <br> Buffet 07h00–10h30 — après le départ prévu ; bouilloire en chambre, prévoir la veille |
| **Hôtel Chantaco Golf et Wellness** | hotel | 0.1 km | — | `+33 5 59 41 32 87` | ❓ à appeler | — |
| **Ibis Ciboure Saint-Jean-de-Luz** | hotel | 0.1 km | — | `+33 5 59 41 76 80` | ❓ à appeler | — |
| **ibis budget Ciboure Saint-Jean-de-Luz** | hors OSM | — | — | — | ✅ réception 24h/24 | Vélo rentré dans un local sur demande (retour client cycliste) ; parking privé gratuit fermé <br> Petit-déjeuner sur place, heure d'ouverture à confirmer ; bar dans l'hôtel |

> Les 1 dernière(s) ligne(s) viennent de la vérification manuelle sans correspondance dans le relevé OSM : écart à la trace non mesuré.

> Replis camping : Centre de vacances Léo Lagrange Borda Zahar (0.2 km), Suhiberry (1.3 km), Le Bord de Mer (2.1 km).

### Nuit 5 — Esquièze-Sère / Luz-Saint-Sauveur (km 1372 · S13 km 174, arrivée Mar 29 sept. 19h29)

| Nom | Type | Écart | Tarif | Téléphone | Accès à l'arrivée | Vélo / petit-déj |
|---|---|---:|---:|---|---|---|
| **Hôtel Tourmalet - Pyrénées** | hotel | 0.0 km | 55 - 75 € | `+33 5 62 92 80 09` · mobile `+336 08 16 49 79` | ❓ horaires non chiffrés | 🌟 LABELLISÉ CYCLISME : Garaje fermé/surveillé + station de lavage + pied de réparation + séchoir chaussures <br> Formule vélo & demi-pension |
| **Hôtel des Cimes** | hotel | 0.1 km | — | — | ❓ à appeler | — |
| **Les Templiers** | hotel | 0.1 km | — | — | ❓ à appeler | — |
| **Le Montaigu** | hotel | 0.1 km | — | — | ❓ à appeler | — |
| **Auberge de Viella** | hostel | 0.1 km | — | — | ❓ à appeler | — |
| **Les Cascades** | guest_house | 0.3 km | — | — | ❓ à appeler | — |

> Replis camping : Camping Le Bastan (0.0 km), La Grange Bigourdane (0.1 km), Camping le Bergons (0.1 km).

> ❓ **Aucun horaire chiffré pour cette étape** : rien ne dit si quelqu'un accueille à 19h29 un mardi. À régler au téléphone.

### Nuit 6 — Tarascon-sur-Ariège / Ax-les-Thermes (km 1629 · S13 km 431, arrivée Mer 30 sept. 22h14)

| Nom | Type | Écart | Tarif | Téléphone | Accès à l'arrivée | Vélo / petit-déj |
|---|---|---:|---:|---|---|---|
| **Hostellerie de la poste** | hotel | 0.0 km | 55 - 75 € | `+33 5 61 05 60 41` · ⚠️ OSM `+33561017945` | ❓ horaires non chiffrés | Garage à vélos fermé et gratuit (annexe hôtel) <br> Petit-déjeuner sur place |
| **Le Manoir d'Agnès** | hotel | 0.0 km | 90 - 120 € | `+33 5 61 02 32 81` | 🔑 réception fermée 0.7 h avant — clé ou code à convenir à la réservation | 🌟 LABELLISÉ ACCUEIL VÉLO : Local à vélos sécurisé + kit réparation + pompe <br> Petit-déjeuner buffet |
| **Hôtel Confort** | hotel | 0.0 km | — | — | ❓ à appeler | — |
| **Les chataigniers de Florac** | guest_house | 1.1 km | — | — | ❓ à appeler | — |
| **Le Jardin d’En Vie** | guest_house | 1.2 km | — | — | ❓ à appeler | — |
| **Domaine Fournié** | guest_house | 1.3 km | — | — | ❓ à appeler | — |

> Replis camping : Pré Lombard (0.5 km), Le Sédour (1.1 km), Gîte du couchant (1.6 km).

> 🔑 **Personne à la réception à 22h14 un mercredi** : les 1 option(s) vérifiée(s) exigent une clé ou un code convenu à la réservation. Réservable, mais pas improvisable.

> Levier : **partir 0 h 44 plus tôt** (05h30 → 04h46) ferait arriver avant la fermeture de **Le Manoir d'Agnès**, et donc entrer sans arrangement. Coût : autant de sommeil en moins la nuit précédente. ⚠️ Mais cette journée-là commence par monter à **2089 m** avant une descente à **-9.2 %** : avancer le départ déplace cette descente vers le froid et la nuit noire au lieu de l'en sortir. Le levier coûte ici plus cher qu'ailleurs.


> ☕ **Aucun petit-déjeuner servi avant le départ, sur aucune étape vérifiée.** Le plus matinal est **Sant Roc Hotel Boutique** à 07h00, soit 3 h 30 après le départ le plus matinal du plan, 03h30. Le premier repas de chaque journée se prépare donc la veille au soir : c'est une contrainte de ravitaillement, pas un détail d'hôtel. Demander systématiquement un plateau ou un sac à emporter, et vérifier la bouilloire en chambre.

> ℹ️ **Fiches vérifiées sans étape correspondante** — un arrêt a été déplacé depuis leur relevé. Elles restent valables comme repli en route, pas comme ville-étape : **Souraïde / Espelette**.


---
## ☎️ Checklist d'appels

Aucune ligne du tableau précédent n'a été confirmée de vive voix : les horaires viennent des sites officiels, qui ne disent pas ce qui se passe quand on arrive à 23 h à vélo. Cinq questions suffisent, les mêmes partout — l'heure d'arrivée et l'heure de départ de chaque nuit sont rappelées dans les titres ci-dessous :

1. **Accueil à l'heure d'arrivée prévue ?** Si la réception est fermée : boîte à clés, digicode, code par SMS ?
2. **Le vélo rentre-t-il ?** Chambre ou local fermé à clé — un parking ouvert ne compte pas.
3. **Peut-on repartir à l'heure de départ prévue, vélo compris ?** C'est la question symétrique de la première, et elle se pose même quand l'accueil du soir est réglé : un vélo enfermé dans une cave sans veilleur ni code ne sort pas avant l'ouverture. À poser en donnant l'heure exacte.
4. **Petit-déjeuner** possible à cette heure-là, ou de quoi emporter la veille ?
5. **Annulation gratuite jusqu'à quand ?** Le plan peut basculer sur 8 jours en course : une nuit non annulable gratuitement enlève cette liberté.

### Nuit 1 — Solsona · arrivée Ven 25 sept. 23h57, départ Sam 26 sept. 05h30

| Ordre | Établissement | Numéros | Pourquoi cet ordre |
|---:|---|---|---|
| 1 | **Sant Roc** | `+34 973 48 00 06` · ⚠️ OSM `+34 973484003` · WhatsApp `+34 683 14 75 77` | accueil en direct à l'arrivée |
| 2 | **Hotel Gran Sol** | `+34 973 48 09 75` | réception fermée : demander clé, digicode ou code SMS |
| 3 | **Hostal Crisami** | `+34 973 48 04 13` | réception fermée : demander clé, digicode ou code SMS |

### Nuit 2 — Plan · arrivée Sam 26 sept. 22h06, départ Dim 27 sept. 05h30

| Ordre | Établissement | Numéros | Pourquoi cet ordre |
|---:|---|---|---|
| 1 | **Hotel Mediodía** | `+34 974 50 60 06` | accueil en direct à l'arrivée |
| 2 | **Apartamentos Villa de Plan** | `+34 974 50 64 73` · WhatsApp `+34 676 95 63 40` | ouvert de justesse |

### Nuit 3 — Saint-Michel / Saint-Jean-Pied-de-Port · arrivée Dim 27 sept. 20h00, départ Lun 28 sept. 05h30

| Ordre | Établissement | Numéros | Pourquoi cet ordre |
|---:|---|---|---|
| 1 | **Albergue La Coquille Napoleón** | `+33 6 62 25 99 40` | horaires inconnus |
| 2 | **Hôtel des Remparts (SJPdP)** | `+33 5 59 37 13 79` · WhatsApp `+33 6 76 12 28 58` | horaires inconnus |
| 3 | **Albergue Ferme Ithurburia** | `+33 559371117` | non vérifié |
| 4 | **Villa Goxoki** | `+33 6 73 89 49 21` | non vérifié |

### Nuit 4 — Saint-Jean-de-Luz / Ciboure · arrivée Lun 28 sept. 19h46, départ Mar 29 sept. 03h30

| Ordre | Établissement | Numéros | Pourquoi cet ordre |
|---:|---|---|---|
| 1 | **Hôtel Colbert** | `+33 5 59 26 31 99` | accueil en direct à l'arrivée |
| 2 | **Hôtel de Paris** | `+33 5 59 85 20 20` | ouvert de justesse |
| 3 | **Hôtel Le relais de Saint Jacques** | `+33 5 59 26 02 55` | réception fermée : demander clé, digicode ou code SMS |
| 4 | **La Caravelle** | `+33 5 59 47 18 05` | non vérifié |

### Nuit 5 — Esquièze-Sère / Luz-Saint-Sauveur · arrivée Mar 29 sept. 19h29, départ Mer 30 sept. 05h30

| Ordre | Établissement | Numéros | Pourquoi cet ordre |
|---:|---|---|---|
| 1 | **Hôtel Tourmalet - Pyrénées** | `+33 5 62 92 80 09` · mobile `+336 08 16 49 79` | horaires inconnus |

### Nuit 6 — Tarascon-sur-Ariège / Ax-les-Thermes · arrivée Mer 30 sept. 22h14, départ Jeu 1 oct. 05h30

| Ordre | Établissement | Numéros | Pourquoi cet ordre |
|---:|---|---|---|
| 1 | **Le Manoir d'Agnès** | `+33 5 61 02 32 81` | réception fermée : demander clé, digicode ou code SMS |
| 2 | **Hostellerie de la poste** | `+33 5 61 05 60 41` · ⚠️ OSM `+33561017945` | horaires inconnus |

### Numéros à trancher

Fiche et OpenStreetMap ne disent pas la même chose ; l'un des deux est périmé. Le premier appel règle la question.

- Nuit 1 · **Sant Roc** : fiche `+34 973 48 00 06` contre OSM `+34 973484003`
- Nuit 6 · **Hostellerie de la poste** : fiche `+33 5 61 05 60 41` contre OSM `+33561017945`

> **16 appels** au total, dont les plus urgents sont ceux des nuits sans option confirmée ouverte. À passer avant le départ : une fois en course, la marge pour chercher un lit de repli est nulle.

---
## 📍 Repères, ravitos et control points

| Compteur (fichier GPX + km) | Cumul | Repère | Alt. | Écart trace | Notes |
|---|---:|---|---:|---:|---|
| `1.TPRn6 Start parcours.gpx` — **km 3** | **km 3** | **Girona (Départ Officiel)** | 82 m | 0.5 km | Départ vendredi 25 sept. à 07h00. Supermarchés & boutiques vélo. |
| `1.TPRn6 Start parcours.gpx` — **km 72** | **km 72** | **Sant Feliu de Guíxols** | 13 m | sur la trace | Côte méditerranéenne, boulangeries, épiceries. |
| `2.TPRn6 start to parcours A road.gpx` — **km 1** | **km 105** | **Lloret de Mar** | 10 m | sur la trace | Dernière grande ville avant la section isolée des Guilleries (129 km). |
| `2.TPRn6 start to parcours A road.gpx` — **km 123** | **km 226** | **Puig-reig** | 591 m | ⚠️ **5.9 km** | ⚠️ **HORS TRACE — détour de 5.9 km (12 km aller-retour). Ne pas compter dessus.** Sortie Berguedà, supermarchés, restaurants. |
| `4.TPRn6 A to B Road.gpx` — **km 43** | **km 314** | **Sant Llorenç de Morunys** | 1369 m | 3.3 km | Hôtels, pharmacies, bars. |
| `5.TPRn6 parcours B.gpx` — **km 44** | **km 360** | **Coll de Nargó** | 552 m | sur la trace | Vallée du Segre, station-service, épicerie. |
| `6.TPRn6 B to C Hybrid.gpx` — **km 23** | **km 401** | **CP1 Pessonada (Control Point 1)** | 883 m | sur la trace | CP1 Officiel orga. Contrôle passif par photo/GPS. |
| `6.TPRn6 B to C Hybrid.gpx` — **km 33** | **km 410** | **Tremp / La Pobla de Segur** | 519 m | sur la trace | Gros ravito après CP1. Supermarchés Mercadona/BonÀrea. |
| `6.TPRn6 B to C Hybrid.gpx` — **km 72** | **km 449** | **El Pont de Suert** | 858 m | sur la trace | Dernière grande ville avant la haute vallée de Ribagorça. |
| `6.TPRn6 B to C Hybrid.gpx` — **km 115** | **km 492** | **Castejón de Sos** | 792 m | ⚠️ **12.7 km** | ⚠️ **HORS TRACE — détour de 12.7 km (25 km aller-retour). Ne pas compter dessus.** Vallée de Benasque, boulangeries, fontaine. |
| `8.TPRn6 C to D.gpx` — **km 20** | **km 625** | **Sarvisé / Hostal Pirineos** | 865 m | sur la trace | CP2 Officiel orga. Cut-off Dimanche 27/09 à 16h00. |
| `8.TPRn6 C to D.gpx` — **km 56** | **km 661** | **Sabiñánigo / Jaca** | 793 m | sur la trace | Dernier gros point de ravito espagnol avant 100 km. |
| `8.TPRn6 C to D.gpx` — **km 178** | **km 783** | **Tardets / Mauléon** | 223 m | sur la trace | Entrée en France (Soule), commerces français. |
| `10.TPRn6 D to E.gpx` — **km 42** | **km 928** | **Pamplona (Navarre)** | 435 m | 2.2 km | Ville H24, épiceries de nuit, pharmacies. |
| `10.TPRn6 D to E.gpx` — **km 113** | **km 999** | **Tolosa** | 79 m | sur la trace | Pays Basque espagnol, ravito avant CP3. |
| `10.TPRn6 D to E.gpx` — **km 149** | **km 1035** | **CP3 Gran Camping Zarautz** | 119 m | sur la trace | CP3 Officiel orga. Cut-off Mardi 29/09 à 09h00. |
| `12.TPRn6 E to F.gpx` — **km 89** | **km 1142** | **Cambo-les-Bains** | 82 m | 3.0 km | Dernière ville française avant la traversée d'Iraty (104 km). |
| `12.TPRn6 E to F.gpx` — **km 119** | **km 1172** | **Saint-Jean-Pied-de-Port** | 173 m | sur la trace | Hôtels, boulangeries, matériel. |
| `13.TPRn6 Parcours F.gpx` — **km 18** | **km 1215** | **Larrau** | 630 m | sur la trace | Village de montagne isolé. Horaires d'ouverture restreints. |
| `13.TPRn6 Parcours F.gpx` — **km 112** | **km 1309** | **Laruns (Vallée d'Ossau)** | 490 m | 0.8 km | Fin du trou d'autonomie d'Iraty. Supermarché Carrefour Contact. |
| `13.TPRn6 Parcours F.gpx` — **km 158** | **km 1355** | **Argelès-Gazost / Luz-Saint-Sauveur** | 637 m | 1.8 km | Vallée des gaves, ravito très dense au pied du Tourmalet. |
| `13.TPRn6 Parcours F.gpx` — **km 210** | **km 1408** | **Sainte-Marie-de-Campan** | 858 m | sur la trace | Pied est du Tourmalet et pied ouest d'Aspin. Épicerie/boulangerie. |
| `13.TPRn6 Parcours F.gpx` — **km 273** | **km 1470** | **Bagnères-de-Luchon** | 631 m | sur la trace | Hôtels, restaurants, pharmacies. |
| `13.TPRn6 Parcours F.gpx` — **km 368** | **km 1565** | **Seix (Ariège)** | 514 m | sur la trace | Cœur du Couserans. Alimentation générale. |
| `13.TPRn6 Parcours F.gpx` — **km 431** | **km 1629** | **Tarascon-sur-Ariège / Ax-les-Thermes** | 474 m | sur la trace | Vallée de l'Ariège, accès gare et supermarchés. |
| `13.TPRn6 Parcours F.gpx` — **km 541** | **km 1738** | **Mont-Louis / Puigcerdà** | 1579 m | sur la trace | Cerdagne, avant l'ascension du Coll de Pal (2 194 m). |
| `14.TPRn6 F to End.gpx` — **km 51** | **km 1826** | **Ripoll / Olot** | 929 m | sur la trace | Hôtels Bed & Bike. |
| `15.TPRn6 Finish.gpx` — **km 33** | **km 1921** | **Girona (Arrivée Finale 🏆)** | 76 m | sur la trace | Finish line officielle de la TransPyrenees Race No. 6 ! |

> ⚠️ **2 repère(s) au-delà du seuil de 5 km** (règle 5) : Puig-reig (5.9 km), Castejón de Sos (12.7 km). Traiter les tronçons concernés comme des sections en autonomie.

---
## 🏁 Control points et cut-offs

| Control point | Km | Compteur | Étape | Passage modélisé | Cut-off | Marge |
|---|---:|---|---|---|---|---:|
| **CP1 Pessonada** | 401 | S6 km 23 | E2 | Sam 26 sept. 12h56 | aucun (auto-validation) | — |
| **CP2 Sarvise (Hostal Pirineos)** | 625 | S8 km 20 | E3 | Dim 27 sept. 08h56 | Dim 27 sept. 16h00 | **+7.1 h** |
| **CP3 Gran Camping Zarautz** | 1035 | S10 km 149 | E4 | Lun 28 sept. 15h49 | Mar 29 sept. 09h00 | **+17.2 h** |

> Une fermeture ratée ne disqualifie pas : elle coûte le **General Classification** (pas de temps officiel, retrait du processus de validation), le **Race Finish** restant acquis si les 10 règles sont respectées. Cut-off global GC : **samedi 3 octobre 23h59 CEST**.


---
## 🕰️ Marges et bascule 8 jours

Le plan n'est pas également serré du début à la fin. Chaque échéance n'ajoute que ce qui reste après la précédente :

| Échéance | Km | Marge cumulée | Marge gagnée sur le tronçon précédent |
|---|---:|---:|---:|
| **CP2 Sarvise (Hostal Pirineos)** | 625 | +7.1 h | +7.1 h |
| **CP3 Gran Camping Zarautz** | 1035 | +17.2 h | +10.1 h |
| **Arrivée / cut-off GC** | 1921 | +49.2 h | +32.1 h |

> Tout le serrage est avant **CP3** (km 1035, E4). Après CP3 il n'y a plus aucun contrôle horaire : seulement le cut-off GC, sur lequel le plan a **32 h** d'avance supplémentaire. Autrement dit, la fatigue n'a le droit de coûter cher que dans les trois premiers jours ; passé CP3 elle ne coûte presque rien.

### Heure limite d'arrivée à chaque étape

Au-delà de cette heure, finir dans les temps impose 5 h de sommeil par nuit jusqu'à Gérone. C'est le signal de bascule, pas un objectif.

| Étape | Km | Compteur | Arrivée prévue | Retard absorbable | Heure limite |
|---|---:|---|---|---:|---|
| **E1 Solsona** | 292 | S4 km 20 | Ven 25 sept. 23h57 | **7.5 h** | Sam 26 sept. 07h27 |
| **E2 Plan** | 563 | S7 km 0 | Sam 26 sept. 22h06 | **8.2 h** | Dim 27 sept. 06h18 |
| **E3 Saint-Michel / Saint-Jean-Pied-de-Port** | 839 | S9 km 3 | Dim 27 sept. 20h00 | **20.4 h** | Lun 28 sept. 16h25 |
| **E4 Saint-Jean-de-Luz / Ciboure** | 1113 | S12 km 59 | Lun 28 sept. 19h46 | **55.5 h** | Jeu 1 oct. 03h15 |
| **E5 Esquièze-Sère / Luz-Saint-Sauveur** | 1372 | S13 km 174 | Mar 29 sept. 19h29 | **54.0 h** | Ven 2 oct. 01h30 |
| **E6 Tarascon-sur-Ariège / Ax-les-Thermes** | 1629 | S13 km 431 | Mer 30 sept. 22h14 | **50.3 h** | Sam 3 oct. 00h29 |

### Ajouter une nuit : où, et ce que ça coûte

Le plan 8 jours n'est pas un plan concurrent à choisir au départ : c'est le plan A avec une nuit de plus, insérée au moment où la fatigue le demande. Le découpage de la fin est alors recalculé sur les villes restantes.

| Bascule après | Jours | Jour le plus long | Nuit la plus courte (hors N1) | Marge CP3 | Arrivée | Marge GC |
|---|---:|---:|---:|---:|---|---:|
| _plan A (référence)_ | 7 | 14.7 h | 6.0 h | +17.2 h | Jeu 1 oct. 22h44 | +49.2 h |
| après **E1 Solsona** | 8 | 14.5 h | 8.0 h | ⚠️ +1.5 h | Ven 2 oct. 19h35 | +28.4 h |
| après **E2 Plan** | 8 | 14.5 h | 6.1 h | +17.0 h | Ven 2 oct. 19h35 | +28.4 h |
| après **E3 Saint-Michel / Saint-Jean-Pied-de-Port** | 8 | 14.5 h | 6.1 h | +17.0 h | Ven 2 oct. 19h35 | +28.4 h |
| après **E4 Saint-Jean-de-Luz / Ciboure** | 8 | 14.5 h | 6.1 h | +17.2 h | Ven 2 oct. 19h35 | +28.4 h |
| après **E5 Esquièze-Sère / Luz-Saint-Sauveur** | 8 | 14.5 h | 6.1 h | +17.2 h | Ven 2 oct. 16h35 | +31.4 h |
| après **E6 Tarascon-sur-Ariège / Ax-les-Thermes** | 8 | 14.5 h | 6.0 h | +17.2 h | Ven 2 oct. 15h06 | +32.9 h |

> La bascule reste dans les temps depuis n'importe quelle nuit. Seule l'insertion après E1 est chère : la journée ajoutée tombe avant CP3 et mange presque toute sa marge. À partir d'E2 elle est quasi gratuite, parce que le jour gagné se paie sur la partie non contrôlée.
