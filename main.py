import cv2
import pytesseract
import requests
import yt_dlp
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
YOUTUBE_URL = os.getenv("YOUTUBE_URL")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def get_stream_url(youtube_url):
    ydl_opts = {"format": "best", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["url"]

def main():
    stream_url = get_stream_url(YOUTUBE_URL)
    cap = cv2.VideoCapture(stream_url)
    print("Bot started, watching live stream...")

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue

        text = pytesseract.image_to_string(frame).lower()
        print(text)

        if "smart buy" in text or "buy" in text:
            send_telegram("🚀 BUY detected!")
        elif "smart sell" in text or "sell" in text:
            send_telegram("🔻 SELL detected!")

if __name__ == "__main__":
    main()
