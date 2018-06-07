import requests
import json

url = ""  # FORWARDING URL BY NGROK, replace with your own, e.g. http://00000000.ngrok.io
bearer = ""  # BOT'S ACCESS TOKEN
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}

def main():
    request = requests.post("https://api.ciscospark.com/v1/webhooks",
                            json.dumps(
                            {
                                "name": "Messages",
                                "targetUrl": url,
                                "resource": "messages",
                                "event": "created"
                            }
                            ), headers=headers).json()
    request2 = requests.post("https://api.ciscospark.com/v1/webhooks",
                            json.dumps(
                                {
                                    "name": "Messages",
                                    "targetUrl": url,
                                    "resource": "memberships",
                                    "event": "created"
                                }
                            ), headers=headers).json()
    return ""


if __name__ == "__main__":
    main()
