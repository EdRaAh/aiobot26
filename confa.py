import os
import random
import logging

from aiogram import Bot
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

logger = logging.getLogger(__file__)

users = {}

ATTEMPTS = 7

def get_random_letter() -> str:
    return chr(random.randint(ord('a'), ord('z')))