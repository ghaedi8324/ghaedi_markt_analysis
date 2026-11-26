import json
import os
import urllib.parse
import urllib.request
import urllib.error


def send_message(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise RuntimeError(
            "Telegram token or channel ID is missing"
        )

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )
    except urllib.error.HTTPError as error:
        details = error.read().decode(
            "utf-8", errors="replace"
        )
        raise RuntimeError(details) from error

    if not result.get("ok"):
        raise RuntimeError(str(result))

    return result


if __name__ == "__main__":
    message = (
        "تست اتصال ربات Market Analysis موفق بود.\n"
        "این پیام آزمایشی است."
    )

    result = send_message(message)

    print(
        "Message sent:",
        result["result"]["message_id"]
    )
