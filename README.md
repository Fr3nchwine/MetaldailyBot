# 🤘 Bot @fr3nch_wine — Brief Metal RSS
### 100% gratuit — aucune API payante

Scrape 10 sites metal chaque matin à 7h00 et envoie les meilleures news sur Telegram.

**Sources :** Blabbermouth · Metal Injection · Metal Underground · MetalSucks · 
Loudwire · Metal Hammer · Kerrang · Radio Metal · La Grosse Radio · Rock Hard France

---

## ÉTAPE 1 — Créer le bot Telegram (5 min)

1. Ouvre Telegram → cherche **@BotFather**
2. Envoie `/newbot`
3. Nom : `fr3nchwine_brief`
4. Username : `fr3nchwine_brief_bot`
5. **Copie le token** → ressemble à `7123456789:AAFxxx...`

### Récupérer ton Chat ID
1. Cherche **@userinfobot** sur Telegram
2. Envoie `/start`
3. **Copie ton ID** (un nombre genre `123456789`)

---

## ÉTAPE 2 — Mettre les fichiers sur GitHub (5 min)

1. Crée un compte sur **github.com**
2. Clique **"New repository"** → nom : `fr3nchwine-bot` → Public ou Private
3. Upload les 4 fichiers : `bot.py`, `cron.py`, `requirements.txt`, `Procfile`

---

## ÉTAPE 3 — Déployer sur Railway (10 min)

1. Va sur **railway.app** → crée un compte (GitHub login)
2. **"New Project"** → **"Deploy from GitHub repo"**
3. Sélectionne `fr3nchwine-bot`

### Variables d'environnement
Dans Railway → ton projet → **"Variables"** → ajoute :

| Variable | Valeur |
|---|---|
| `TELEGRAM_TOKEN` | Le token de @BotFather |
| `TELEGRAM_CHAT_ID` | Ton Chat ID numérique |

4. Railway démarre automatiquement

---

## ÉTAPE 4 — Tester immédiatement

Dans Railway → **"Shell"** → tape :
```
python bot.py
```
Tu reçois le brief dans la seconde sur Telegram.

---

## Format du message reçu

```
🤘 BRIEF METAL — 23.06.2026
by @fr3nch_wine
━━━━━━━━━━━━━━━━

🔴 1. METALLICA — Kirk Hammett chute sur scène à Dublin
🌍 Blabbermouth
🔗 Lire

🔴 2. DIMMU BORGIR — Grand Serpent Rising disponible
🌍 Metal Injection
🔗 Lire

🔴 3. IRON MAIDEN — Inductés au Rock Hall of Fame
🌍 Kerrang
🔗 Lire

🔴 4. CONVERGE — Nouvel album annoncé
🇫🇷 Radio Metal
🔗 Lire

🔴 5. MEGADETH — Tournée d'adieu en cours
🇫🇷 La Grosse Radio
🔗 Lire

━━━━━━━━━━━━━━━━
Growl And Drink 🍷
```

---

## Coût total

| Service | Prix |
|---|---|
| Railway | Gratuit |
| Telegram | Gratuit |
| API Anthropic | ❌ Non utilisée |
| **TOTAL** | **0€/mois** |

---

## Changer l'heure

Dans `cron.py`, ligne `schedule.every().day.at("05:00")` :
- **Été (UTC+2)** → mettre `"05:00"` pour recevoir à 7h00 Paris
- **Hiver (UTC+1)** → mettre `"06:00"` pour recevoir à 7h00 Paris

---

*Growl And Drink 🍷*
