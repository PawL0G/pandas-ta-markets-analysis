""" TODO:
 1. Retrieve data from API. URL: https://stocknewsapi.com/
 2. Add Amazon and Apple tickers
 3. Sort sentiment by Negative in news
"""

import requests


def news_api(url, token) -> str:
    # define tickers AMZN as Amazon and AAPL as Apple
    tickers = ['AMZN', 'AAPL']

    # item count, according to API max value for trial period is 50
    itm_count = 50

    response = requests.get(f'{url}api/v1?tickers={tickers}&items={itm_count}&token={token}')

    data = response.json()

    # create a dict of sentimental as status for each value
    sentimental = {
        'neu': 'Neutral',
        'pos': 'Positive',
        'neg': 'Negative',
    }

    try:

        for result in data['data']:
            if result.get('sentiment') in sentimental.get('neg'):
                print(result.get('tickers'), f"\nTitle: {result['title']} \nSentiment: {result['sentiment']} \nDate: {result['date']} \n")

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return data


if __name__ == '__main__':
    news_api(url='https://stocknewsapi.com/', token='byn1x1lzi2389kmcr7nswmkj7j3yszkm8wlsxlfl')
