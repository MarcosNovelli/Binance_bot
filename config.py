from dotenv import load_dotenv
import os
from app import paper_money

load_dotenv()
API_KEY = os.environ["API_KEY_PAPER"] if paper_money else os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET_PAPER"] if paper_money else os.environ["API_SECRET"]
