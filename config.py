import os
from binance.client import Client
from dotenv import load_dotenv

paper_money = 1

load_dotenv()
API_KEY = os.environ["API_KEY_PAPER"] if paper_money else os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET_PAPER"] if paper_money else os.environ["API_SECRET"]
discord_address = os.environ["discord_address"]
discord_authorization = os.environ['discord_authorization']

client = Client(API_KEY, API_SECRET, testnet=paper_money)