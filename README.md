# Cisco-Webex-Teams-Bot-Stock_Bot
Stock data retrieval bot for Cisco Webex Teams application

How to run:
1. Run the ngrok application in the terminal to open a secure introspectable tunnel to localhost for webhooks.

    ngrok http 8080

2. Copy and paste the forwarding url provided by the ngrok application into the "url" variable in "create_post_webhooks.py".
    e.g. url = http://12345ab6.ngrok.io

3. Run "create_post_webhooks.py" to set up the post webhooks.

    python create_post_webhooks.py

4. Run "run_spark_bot.py" to run up the bot server.

    python run_spark_bot.py

How to interact with bot:
1. Begin a one-on-one chat in the Cisco Webex Teams application with "stock_bot@webex.bot", or add it to a team space.
2. The bot will accept the following commands:

    hello
    help me
    price <symbol>

2. Enter the price command, followed by a valid ticker-symbol, to view the stock price data.
    
    price csco

Sample output:

    Here are the details for symbol: csco
    Date: 11:09:26 AM
    Name: Cisco Systems Inc.
    Latest Price: $42.91
    Price Change: $-0.35
    Percent Change: -0.00809%

