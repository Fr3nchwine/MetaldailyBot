import schedule
import time
from bot import main

# 7h00 heure de Paris = 05h00 UTC en été (UTC+2)
# Si tu es en hiver (UTC+1), change en "06:00"
schedule.every().day.at("05:00").do(main)

print("⏰ Bot @fr3nch_wine démarré — brief metal à 7h00 (Paris) chaque matin")
print("📡 Sources : Blabbermouth, Metal Injection, Metal Underground, MetalSucks,")
print("             Loudwire, Metal Hammer, Kerrang, Radio Metal, La Grosse Radio, Rock Hard FR")

while True:
    schedule.run_pending()
    time.sleep(30)
