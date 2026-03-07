import requests
from bs4 import BeautifulSoup
import hashlib
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

URL = "https://www.dcrustm.ac.in/welcome/dcrustnews/news"

def send_telegram(message):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_notices():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tr")[1:6]  # top 5 notices

    notices = []

    for row in rows:
        cols = row.select("td")

        title = cols[1].text.strip()
        date = cols[2].text.strip()

        notices.append(f"{title} | {date}")

    return notices


def load_hashes():
    if not os.path.exists("hashes.txt"):
        return set()

    with open("hashes.txt","r") as f:
        return set(f.read().splitlines())


def save_hash(hash_value):
    with open("hashes.txt","a") as f:
        f.write(hash_value+"\n")


def main():

    notices = get_notices()
    processed = load_hashes()

    for notice in notices:

        h = hashlib.md5(notice.encode()).hexdigest()

        if h not in processed:

            message = f"📢 New DCRUST Notice\n\n{notice}\n\n{URL}"

            send_telegram(message)

            save_hash(h)


if __name__ == "__main__":
    main()
