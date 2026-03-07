import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

URL = "https://www.dcrustm.ac.in/welcome/dcrustnews/news"

def get_latest_notices():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tr")[1:6]

    notices = []

    for row in rows:
        cols = row.select("td")
        title = cols[1].text.strip()
        date = cols[2].text.strip()

        notices.append(f"{title} | {date}")

    return notices


def get_recent_messages():

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    r = requests.get(url)

    data = r.json()

    messages = []

    for update in data["result"]:
        if "message" in update:
            messages.append(update["message"]["text"])

    return messages


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })


def main():

    notices = get_latest_notices()
    sent_messages = get_recent_messages()

    for notice in notices:

        if notice not in str(sent_messages):

            message = f"📢 New DCRUST Notice\n\n{notice}\n\n{URL}"

            send_message(message)


if __name__ == "__main__":
    main()
