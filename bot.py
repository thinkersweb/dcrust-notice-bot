import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

URL = "https://www.dcrustm.ac.in/welcome/dcrustnews/news"

def get_latest_notice():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text,"html.parser")

    row = soup.select("table tr")[1]

    title = row.select("td")[1].text.strip()
    date = row.select("td")[2].text.strip()

    return f"{title} | {date}"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id": CHAT_ID,
        "text": message
    })

def main():
    latest = get_latest_notice()

    try:
        with open("last_notice.txt","r") as f:
            old = f.read()
    except:
        old = ""

    if latest != old:
        message = f"📢 New DCRUST Notice\n\n{latest}\n\n{URL}"
        send_telegram(message)

        with open("last_notice.txt","w") as f:
            f.write(latest)

if __name__ == "__main__":
    main()
