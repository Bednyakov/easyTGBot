import requests
import time
from random import choice
from config import API_TOKEN as secret

API_URL: str = 'https://api.telegram.org/'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL = 'https://random.dog/woof.json'
API_FOXES_URL = 'https://randomfox.ca/floof/'
BOT_TOKEN_URL: str = secret
ERROR_TEXT: str = 'Тут должна была быть картинка.'
MAX_counter: int = 100

api_urls = (API_CATS_URL, API_DOGS_URL, API_FOXES_URL)

offset: int = -2
counter: int = 0
response: requests.Response
link: str

while counter < MAX_counter:
    random_url = choice(api_urls)

    print('attempt = ', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN_URL}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            response = requests.get(random_url)
            if response.status_code == 200 and random_url == API_CATS_URL:
                link = response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN_URL}/sendPhoto?chat_id={chat_id}&photo={link}')
            elif response.status_code == 200 and random_url == API_DOGS_URL:
                link = response.json()['url']
                requests.get(f'{API_URL}{BOT_TOKEN_URL}/sendPhoto?chat_id={chat_id}&photo={link}')
            elif response.status_code == 200 and random_url == API_FOXES_URL:
                link = response.json()['image']
                requests.get(f'{API_URL}{BOT_TOKEN_URL}/sendPhoto?chat_id={chat_id}&photo={link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN_URL}/sendMassage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1