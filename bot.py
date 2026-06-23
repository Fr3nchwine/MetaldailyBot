import os
import requests
import feedparser
from datetime import datetime, timezone
import html
import re

# === CONFIG ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# === 10 SOURCES RSS METAL ===
RSS_FEEDS = [
    {
        "name": "Blabbermouth",
        "url": "https://www.blabbermouth.net/feed/",
        "lang": "EN"
    },
    {
        "name": "Metal Injection",
        "url": "https://metalinjection.net/feed",
        "lang": "EN"
    },
    {
        "name": "Metal Underground",
        "url": "https://www.metalunderground.com/rss/news.cfm",
        "lang": "EN"
    },
    {
        "name": "MetalSucks",
        "url": "https://www.metalsucks.net/feed/",
        "lang": "EN"
    },
    {
        "name": "Loudwire",
        "url": "https://loudwire.com/feed/",
        "lang": "EN"
    },
    {
        "name": "Metal Hammer",
        "url": "https://www.loudersound.com/feeds/all",
        "lang": "EN"
    },
    {
        "name": "Kerrang",
        "url": "https://kerrang.com/feed",
        "lang": "EN"
    },
    {
        "name": "Radio Metal",
        "url": "https://www.radiometal.com/rss.xml",
        "lang": "FR"
    },
    {
        "name": "La Grosse Radio",
        "url": "https://www.lagrosseradio.com/feed/",
        "lang": "FR"
    },
    {
        "name": "Rock Hard France",
        "url": "https://www.rockhard.fr/feed/",
        "lang": "FR"
    },
]

# Mots-clés prioritaires (metalcore, death, black, festival)
PRIORITY_KEYWORDS = [
    "album", "single", "clip", "video", "tour", "festival",
    "new song", "announces", "release", "death metal", "black metal",
    "metalcore", "djent", "nouvel album", "nouveau single", "tournée",
    "annonce", "sortie", "clip vidéo"
]

def clean_html(text):
    """Nettoie le HTML et les caractères spéciaux."""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = text.strip()
    return text

def is_recent(entry):
    """Vérifie si l'article date de moins de 24h."""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = now - pub_date
            return diff.total_seconds() < 86400  # 24h
    except Exception:
        pass
    return True  # Si pas de date, on garde

def score_entry(entry):
    """Score l'article selon les mots-clés prioritaires."""
    title = entry.get('title', '').lower()
    score = 0
    for keyword in PRIORITY_KEYWORDS:
        if keyword.lower() in title:
            score += 1
    return score

def fetch_all_news():
    """Scrape les 10 flux RSS et retourne les meilleures news."""
    all_entries = []

    for feed_info in RSS_FEEDS:
        try:
            print(f"📡 Scraping {feed_info['name']}...")
            feed = feedparser.parse(feed_info['url'])

            for entry in feed.entries[:10]:  # 10 derniers articles par source
                if is_recent(entry):
                    all_entries.append({
                        "title": clean_html(entry.get('title', 'Sans titre')),
                        "link": entry.get('link', ''),
                        "source": feed_info['name'],
                        "lang": feed_info['lang'],
                        "score": score_entry(entry)
                    })
        except Exception as e:
            print(f"⚠️ Erreur sur {feed_info['name']}: {e}")
            continue

    # Trie par score décroissant
    all_entries.sort(key=lambda x: x['score'], reverse=True)

    return all_entries

def format_message(entries):
    """Formate le message Telegram."""
    today = datetime.now().strftime("%d.%m.%Y")

    message = f"🤘 *BRIEF METAL — {today}*\n"
    message += f"_by @fr3nch\\_wine_\n"
    message += "━━━━━━━━━━━━━━━━\n\n"

    if not entries:
        message += "⚠️ Aucune news trouvée aujourd'hui.\n"
        return message

    # Top 5 news EN
    en_entries = [e for e in entries if e['lang'] == 'EN'][:3]
    # Top 2 news FR
    fr_entries = [e for e in entries if e['lang'] == 'FR'][:2]

    top_entries = en_entries + fr_entries

    for i, entry in enumerate(top_entries, 1):
        flag = "🇫🇷" if entry['lang'] == 'FR' else "🌍"
        message += f"🔴 *{i}. {entry['title']}*\n"
        message += f"{flag} _{entry['source']}_\n"
        message += f"[🔗 Lire]({entry['link']})\n\n"

    message += "━━━━━━━━━━━━━━━━\n"
    message += "_Growl And Drink_ 🍷"

    return message

def send_telegram(message):
    """Envoie le message sur Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"✅ Brief envoyé avec succès !")
    else:
        print(f"❌ Erreur Telegram : {response.text}")

def main():
    print(f"🔍 Scraping des 10 sources metal...")
    entries = fetch_all_news()
    print(f"✅ {len(entries)} articles trouvés")
    message = format_message(entries)
    print(f"📨 Envoi sur Telegram...")
    send_telegram(message)

if __name__ == "__main__":
    main()
