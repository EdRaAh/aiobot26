import logging
from config import users, ATTEMPTS
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__file__)
router: Router = Router()

# этот хендлер будет срабатывать на команду "/start" в любом регистре
@router.message(Command(commands=['start', 'START']))
async def start(message: Message):
    logger.info("User %s started the bot.", message.from_user.id)
    chat_id = message.chat.id
    await message.answer('I am online! Я в сети!\n '
                         'Чтобы сыграть в игру напиши "играть"\nУзнать правила отправь команду /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_letter': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }

# Этот хендлер будет срабатывать на команду "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\n'
        f'Я загадываю букву от A-Z, а вам нужно её угадать(отправлять в любом регистре).\n'
        f' Это полезная игра научит вас английскому алфавиту, и не только.\n'
        f'У вас есть {ATTEMPTS} попыток\n\n'
        f'Доступные команды:\n'
        f'/help - правила игры и список команд\n'
        f'/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\n'
        f'Давай сыграем?'
    )


# Этот хендлер будет срабатывать на команду "/stat"
@router.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}'
                         )


# Этот хендлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    logger.info("User %s tried to cancel the game.", message.from_user.id)
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. Может, сыграем разок?'
        )

