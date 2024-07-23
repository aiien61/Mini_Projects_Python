import os
import requests
from twilio.rest import Client
from datetime import datetime, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"

TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

VIRTUAL_TWILIO_NUMBER = "YOUR_VIRTUAL_TWILIO_NUMBER"
VERIFIED_NUMBER = "YOUR_OWN_TWILIO_VERIFIED_NUMBER"


## Use https://www.alphavantage.co/documentation/#daily
# 1. - Get yesterday's closing stock price.
stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [v for k, v in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']

# 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

# 3. - Find the difference between 1 and 2.
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = "🔺" if difference > 0 else "🔻"

# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(percent) > 1:
    ## https://newsapi.org/ 
    # 5. - Use the News API to get articles related to the COMPANY_NAME.
    new_parameters = {
        'qInTitle': COMPANY_NAME,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url=NEWS_ENDPOINT, params=new_parameters)
    response.raise_for_status()

    # 6. - Create a list that contains the first 3 articles.
    articles = response.json()['articles'][:3]

    ## Use twilio.com/docs/sms/quickstart/python
    # 7. - Create a new list of the first 3 article's headline and description.
    title = f"{STOCK_NAME}: {up_down}{percent}%\n"
    formatted_articles = [title + f"Headline: {article['title']}.\nBrief: {article['description']}" for article in articles]

    # 8. - Send each article as a separate message via Twilio. 
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
