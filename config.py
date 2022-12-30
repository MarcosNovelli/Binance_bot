import os
from binance.client import Client
from dotenv import load_dotenv

paper_money = 1

load_dotenv()
API_KEY = os.environ["API_KEY_PAPER"] if paper_money else os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET_PAPER"] if paper_money else os.environ["API_SECRET"]

CLIENT = Client(API_KEY, API_SECRET)