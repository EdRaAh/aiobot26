import random
import logging
from aiogram import Bot
TOKEN="7575340257:AAGtsdY_G6KXFv8aDMC4Vse3Zqinf84_5sI"
bot = Bot(token=TOKEN)
alphabet = 'abcdefghijklmnopqrstuvwxyz'

logger = logging.getLogger(__file__)

users = {}

ATTEMPTS = 7

def get_random_letter() -> str:
    return chr(random.randint(ord('a'), ord('z')))