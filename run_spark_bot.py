from pprint import pprint
import requests
import json
import sys
import os


try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()

bearer = "ZGZlMjJjNTItYzUwOC00NzQ1LWJlODktY2M0MzYyM2U0YzI5NGM4N2NkNTEtYjFm"  # BOT'S ACCESS TOKEN
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}


expected_messages = {"help me": "help",
                     "need help": "help",
                     "can you help me": "help",
                     "ayuda me": "help",
                     "help": "help",
                     "greetings": "greetings",
                     "hello": "greetings",
                     "hi": "greetings",
                     "how are you": "greetings",
                     "what's up": "greetings",
                     "what's up doc": "greetings",
                     }


def send_spark_get(url, payload=None, js=True):
    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request


def send_spark_post(url, data):
    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request


def help_me():
    return "Sure! I can help. Below are the commands that I understand:<br/>" \
           "`Help me` - I will display what I can do.<br/>" \
           "`Hello` - I will display my greeting message.<br/>" \
           "`Price <symbol>` - I will retrieve the stock price data for the given ticker symbol. <br/>"


def greetings():
    return "Hi my name is %s.<br/>" \
           "Type `Help me` to see what I can do.<br/>" % bot_name


def stock_info(symbol):
    # Define filter to specify what parameters to extract from API
    param_filter = '?filter=companyName,latestPrice,latestTime,change,changePercent'

    # HTTP GET request to the IEX stock API
    resp = requests.get('https://api.iextrading.com/1.0/stock/{}/quote/{}'.format(symbol, param_filter))

    # Check for error in response
    if resp.status_code == 200:
        stock_json = resp.json()
        return "Here are the details for symbol: {0}<br/>" \
               "Date: {1}<br/>" \
               "Name: {2}<br/>" \
               "Latest Price: ${3}<br/>" \
               "Price Change: ${4}<br/>" \
               "Percent Change: {5}%<br/>".format(symbol,
                                           stock_json['latestTime'],
                                           stock_json['companyName'],
                                           stock_json['latestPrice'],
                                           stock_json['change'],
                                           stock_json['changePercent'])


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def spark_webhook():
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        # if webhook['data']['personEmail'] != bot_email:
        #     pprint(webhook)
        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            send_spark_post("https://api.ciscospark.com/v1/messages",
                            {
                                "roomId": webhook['data']['roomId'],
                                "markdown": (greetings() +
                                             "**Note This is a group room and you have to call "
                                             "me specifically with `@%s` for me to respond**" % bot_name)
                            }
                            )
        msg = None
        # print(webhook['data']['personEmail'])
        if webhook['data']['personEmail'] != bot_email:
            result = send_spark_get(
                'https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower() + " ", "")
            translation_table = dict.fromkeys(map(ord, '!@#$.?<>;:%^&'), None)
            in_message = in_message.translate(translation_table)
            if in_message in expected_messages and expected_messages[in_message] is "help":
                msg = help_me()
            elif in_message in expected_messages and expected_messages[in_message] is "greetings":
                msg = greetings()
            # elif in_message.startswith("repeat after me"):
            #     msg = in_message.split('repeat after me')[1]
            elif in_message.startswith("price"):
                msg = stock_info(in_message.split(' ')[1])
            if msg != None:
                send_spark_post("https://api.ciscospark.com/v1/messages",
                                {
                                    "roomId": webhook['data']['roomId'],
                                    "markdown": msg
                                }
                                )
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\" alt=\"Spark Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Cisco Spark!</i></b></center>" % bot_name
        return message
    return ""


def main():
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = send_spark_get("https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.ciscospark.com/apps.html "
                  "URL and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token.")
        sys.exit()
    if "@webex.bot" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access to review it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token for your Bot.")
        sys.exit()
    else:
        app.run(host='localhost', port=8080)


if __name__ == "__main__":
    main()
