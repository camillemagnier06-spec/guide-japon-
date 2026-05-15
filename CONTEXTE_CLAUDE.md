# CONTEXTE CLAUDE — Guide Interactif Japon 2026

> **RÈGLE N°1 — LIS CE FICHIER EN ENTIER AVANT TOUTE MODIFICATION.**
> **RÈGLE N°2 — METS CE FICHIER À JOUR APRÈS CHAQUE MODIFICATION DU PROJET.**

---

## 0. Contrat de travail pour tout Claude Code qui intervient sur ce projet

Ce fichier est le **point de vérité unique** du projet. Il doit rester à jour en permanence pour que chaque nouvelle session Claude Code puisse reprendre le travail sans perdre de contexte.

**Ce que tu dois faire dès le début de chaque session :**

1. **Lire ce fichier intégralement** avant de toucher quoi que ce soit.
2. **Lire `index.html`** pour voir l'état réel du code (il peut être plus récent que ta mémoire).
3. Confirmer à l'utilisateur ce que tu as compris avant de commencer.

**Ce que tu dois faire pendant et après chaque modification :**

1. **Pendant le travail** : noter ce qui change (nouvelles fonctions, bugs corrigés, données modifiées).
2. **Après chaque modification significative** : mettre à jour ce fichier immédiatement — pas à la fin de session, au fil de l'eau.
3. **Après toute modification de `index.html`** : proposer à l'utilisateur de déployer en lançant toi-même :
   ```
   ! python3 "/Users/magniercamille/Desktop/japon /deploy.py"
   ```
   Si le token n'est pas configuré dans `deploy.py`, guider l'utilisateur vers la section 2b.

**Ce qu'il faut mettre à jour selon le type de changement :**

| Type de changement | Section à mettre à jour |
|---|---|
| Nouveau restaurant ou activité ajouté | Section 3 (comptage), Section 7 (structure si elle change) |
| Nouveau bug corrigé | Section 6 (liste des bugs corrigés) |
| Nouvelle fonction JS créée | Section 3 (fonctions principales) |
| Nouvel onglet ou section HTML | Section 4 (liste des onglets) |
| Modification de l'itinéraire | Section 5 |
| Nouvelle tâche future identifiée | Section 9 |
| Tâche future réalisée | Section 9 (la retirer ou la cocher) |
| Changement de déploiement | Section 2 |

**Format des mises à jour :**
- Sois précis et concis. Une ligne par information.
- Pour les bugs : décris le symptôme, la cause, et la solution en une phrase.
- Ne supprime jamais d'ancienne information sans bonne raison — la mémoire des bugs évite de les réintroduire.

---

## 1. C'est quoi ce projet ?

Un guide de voyage interactif en **single-file HTML** (`index.html`) pour un voyage au Japon du **15 juillet au 13 août 2026**, 2 voyageurs, base à Nakano (Tokyo).

**Fichier unique :** `/Users/magniercamille/Desktop/japon /index.html` (2242 lignes)

**Google Doc (contexte partagé) :** https://docs.google.com/document/d/1or44Ij_01MLsbZ_bX3nabJ3SqGheXjBg6JjbpSk325s/edit?usp=sharing
→ Miroir de ce fichier. À mettre à jour manuellement quand CONTEXTE_CLAUDE.md change (ou via Claude Code pendant une session connectée à Google Drive).

---

## 2. Déploiement

### 2a. Infos

| | URL |
|---|---|
| **Netlify (live)** | https://delicate-pasca-e5789f.netlify.app/ |
| **GitHub (source)** | github.com/camillemagnier06-spec/quide-japon- (privé) |

**Auto-deploy actif** : chaque push sur la branche `main` du repo GitHub redéploie automatiquement Netlify en ~30 secondes. Plus besoin de glisser le fichier manuellement.

**Pour mettre à jour le site (méthode recommandée — script automatique) :**
1. Modifier `index.html` localement
2. Exécuter `deploy.py` (voir section 2b ci-dessous)
3. Netlify redéploie automatiquement en ~30 secondes

**Méthode manuelle (fallback) :**
1. Aller sur GitHub → `index.html` → icône crayon (Edit) → coller le nouveau contenu → Commit
3. Netlify redéploie automatiquement

### 2b. Script de déploiement automatique — `deploy.py`

**Fichier :** `/Users/magniercamille/Desktop/japon /deploy.py`

Ce script Python (sans dépendances, built-in uniquement) pousse `index.html` sur GitHub via l'API REST. Netlify détecte le commit et redéploie automatiquement.

**Setup unique (à faire une seule fois) :**
1. Aller sur https://github.com/settings/tokens/new
2. Donner un nom (ex: "japon-deploy"), durée 1 an
3. Cocher uniquement **"repo"** dans les permissions
4. Cliquer "Generate token", copier le token (commence par `ghp_...`)
5. Ouvrir `deploy.py` et remplacer `COLLE_TON_TOKEN_ICI` par le token

**Utilisation après chaque modification de `index.html` :**
```bash
python3 "/Users/magniercamille/Desktop/japon /deploy.py"
```
Ou depuis Claude Code : `! python3 "/Users/magniercamille/Desktop/japon /deploy.py"`

**Ce que fait le script :**
1. Lit `index.html` localement
2. Récupère le SHA actuel du fichier sur GitHub (requis par l'API)
3. Envoie la nouvelle version via PUT (crée un commit automatiquement)
4. Netlify détecte le commit et redéploie en ~30 secondes

**Variables de configuration dans deploy.py :**
- `GITHUB_TOKEN` — token personnel GitHub (à remplir)
- `GITHUB_OWNER` = `camillemagnier06-spec`
- `GITHUB_REPO` = `quide-japon-`
- `GITHUB_BRANCH` = `main`
- `FILE_PATH` = `index.html`

**Règle pour tout Claude Code :** Après avoir modifié `index.html`, proposer systématiquement à l'utilisateur de lancer le déploiement avec `! python3 "/Users/magniercamille/Desktop/japon /deploy.py"`.

---

## 3. Architecture technique

### Stack
- HTML/CSS/JS vanilla, zéro framework
- **Leaflet.js + OpenStreetMap** pour la carte interactive
- **localStorage** pour toute la persistance (pas de backend)

### Clés localStorage utilisées
| Clé | Contenu |
|---|---|
| `jp_favs` | Array des noms favoris |
| `jp_visited` | Array des noms visités |
| `jp_expenses` | Array des dépenses budget |
| `jp_notes` | Object `{dayNum: "texte"}` |
| `jp_done` | Array des jours cochés |
| `jp_checklist` | Object `{id: bool}` |
| `jp_docs` | Object `{key: value}` pour documents |
| `jp_shopping` | Object `{gi_ii: bool}` pour liste courses |
| `jp_tiktok` | Array de liens vidéos |
| `jp_rate` | Taux de change EUR/JPY |

### Données principales (constantes JS)
- `RESTAURANTS` — array de 54 restaurants (objets `{name, city, neighborhood, type, price, desc, gmaps, booking}`)
- `ACTIVITIES` — array de 45 activités (même structure)
- `MAP_PLACES` — spread de RESTAURANTS + ACTIVITIES pour la carte Leaflet
- `DAYS` — array de 30 objets (planning jour par jour)
- `PHRASES` — **objet** organisé par catégories (PAS un array plat)
- `SUGGESTIONS` — array de suggestions IA générées
- `SHOPPING` — array de groupes avec items à cocher
- `CHECKLIST` — array de groupes avec items à cocher

### Fonctions principales
| Fonction | Rôle |
|---|---|
| `renderDays()` | Génère les cartes planning |
| `applyFoodFilters()` | Filtre et affiche les restaurants |
| `applyActFilters()` | Filtre et affiche les activités |
| `placeCard(item, type)` | Génère une carte lieu (resto ou activité) |
| `toggleFav(name, btn)` | Toggle favori + refresh si mode Favoris actif |
| `toggleVisit(name, btn)` | Toggle visité |
| `renderExpenses()` | Affiche le tableau de dépenses |
| `updateBudgetChart()` | Met à jour les barres de progression budget |
| `renderPhrases()` | Génère le tableau du phrasebook par catégories |
| `renderChecklist()` | Génère la checklist pré-départ |
| `renderShoppingList()` | Génère la liste de courses shopping |
| `renderSuggestions()` | Affiche les suggestions IA |
| `updateFestivalCountdown()` | Met à jour les 3 banners d'événements |
| `updateStats()` | Met à jour les stats d'accueil |
| `globalSearch(q)` | Recherche globale dans tout le guide |
| `setFoodFilter(key, val, el)` | Filtre restaurants + reset quartier si hors Tokyo |
| `setActFilter(key, val, el)` | Filtre activités + reset quartier si hors Tokyo |
| `loadDocs()` | Charge les documents depuis localStorage |

---

## 4. Onglets / sections

```
🏠 Accueil     — Stats, banners festivals, itinéraire général, infos clés
📅 Planning    — 30 jours dépliables avec notes et checkbox
🗺️ Carte       — Carte Leaflet avec tous les lieux (filtrable)
🏠 Logements   — Airbnb Nakano + hébergements par ville
🍜 Food        — 54 restaurants filtrables par ville / quartier / type
⛩️ Activités   — 45 activités filtrables
🚄 Transport   — Suica, JR Pass, trajets entre villes
💴 Budget      — Tracker de dépenses + graphiques + tableau prévisionnel
✨ Suggestions — Suggestions générées par IA (peut en ajouter)
✅ Checklist   — Pré-départ, réservations, à faire sur place
📱 Pratique    — Phrasebook, konbini guide, menu vocabulaire, tailles EU/JP, urgences
🎬 TikTok      — Liens vidéos TikTok/YouTube pour inspiration
```

---

## 5. Itinéraire (résumé)

| Jours | Dates | Ville |
|---|---|---|
| 1–12 | 15–26 Juillet | Tokyo (base Nakano) |
| 13–14 | 27–28 Juillet | Hakone |
| 15–20 | 29 Juillet – 3 Août | Kyoto |
| 21–26 | 4–9 Août | Osaka |
| 27–30 | 10–13 Août | Tokyo (retour) |

---

## 6. Bugs corrigés (ne pas réintroduire)

1. **Stats accueil** : affichent 54 restaurants et 45 activités (valeurs hardcodées dans le HTML, pas dynamiques)
2. **Boutons Maps cassés** : `placeCard()` génère une URL Google Maps automatique si `item.gmaps` est absent — NE PAS utiliser `href="${item.gmaps}"` sans condition
3. **Boutons qui débordent des cartes** : `.place-actions` a `flex-wrap:wrap` — ne pas l'enlever
4. **Graphique budget bloqué à 0%** : `updateBudgetChart()` utilise un `catMap` pour mapper les catégories aux IDs HTML (`activite→act`, `transport→trans`, `shopping→shop`). Ne pas casser ce mapping
5. **Filtre quartier bloqué** : `setFoodFilter` et `setActFilter` reset le filtre quartier quand on change de ville hors Tokyo — logique présente, ne pas la supprimer
6. **toggleFav ne rafraîchit pas le mode Favoris** : `toggleFav()` appelle `applyFoodFilters()` et `applyActFilters()` quand `city === 'favs'` — garder cette logique
7. **Hanadako** : lat corrigée à `34.7014` (Osaka) — ne pas remettre `35.7014` (Tokyo)
8. **Hozenji Yokocho** : le restaurant s'appelle "Hozenji Yokocho — Izakayas" pour éviter collision avec l'activité du même nom
9. **Ninnaji** : nom "🏛️ Ninnaji" (sans mention "Été 2025"), pas de lien de réservation
10. **PHRASES** : c'est un **objet** par catégories, PAS un array — `renderPhrases()` utilise `Object.entries(PHRASES)`

---

## 7. Structure des objets de données

### Restaurant / Activité
```javascript
{
  name: "Nom du lieu",
  city: "Tokyo" | "Kyoto" | "Osaka" | "Hakone" | "Nikko" | "Kamakura" | "Nara",
  neighborhood: "Shinjuku" | "Shibuya" | ... | null,
  type: "ramen" | "sushi" | ... (restos) | "temple" | "musee" | ... (activités),
  price: "€" | "€€" | "€€€",
  desc: "Description courte",
  gmaps: "https://maps.google.com/..." | null,  // null = URL auto-générée
  booking: "https://..." | null,  // optionnel
  lat: 35.xxxx,  // coordonnées pour la carte
  lng: 139.xxxx
}
```

### updateBudgetChart — catMap CRITIQUE
```javascript
const catMap = {
  resto: 'resto',
  activite: 'act',      // ← ID HTML est "bar-act", pas "bar-activite"
  transport: 'trans',   // ← ID HTML est "bar-trans", pas "bar-transport"
  shopping: 'shop',     // ← ID HTML est "bar-shop", pas "bar-shopping"
  logement: 'logement',
  autre: 'autre'
};
```

---

## 8. Permissions et workflow

- **Permission mode** : `acceptEdits` sur `/Users/magniercamille/Desktop/japon /` — modifier `index.html` directement sans demander confirmation
- **Après modification** : rappeler à l'utilisateur de pusher sur GitHub pour que Netlify redéploie automatiquement
- **Pas de système de build** : c'est un fichier HTML statique, pas de npm, pas de bundler

---

## 9. Ce qui reste à faire (idées futures)

- Ajouter des photos/images aux restaurants et activités
- Ajouter un onglet météo en temps réel (API)
- Mode hors-ligne (Service Worker / PWA)
- Export PDF amélioré (le print CSS basique est déjà en place)
- Connecter GitHub proprement à Netlify avec un workflow de commit depuis le terminal (actuellement : édition manuelle sur github.com)

---

## 10. Comment modifier ce fichier

Le fichier fait 2242 lignes. Pour s'y retrouver, rechercher :

| Pour trouver | Chercher |
|---|---|
| Données restaurants | `const RESTAURANTS` |
| Données activités | `const ACTIVITIES` |
| Planning 30 jours | `const DAYS` |
| Phrasebook | `const PHRASES` |
| Carte Leaflet | `initMap()` |
| Rendu restaurants | `applyFoodFilters()` |
| Budget tracker | `renderExpenses()` |
| Checklist | `renderChecklist()` |
| Styles CSS | Début du fichier (lignes 9–301) |
| HTML accueil | `id="tab-accueil"` |
| JS principal | après `</main>` (~ligne 800+) |
