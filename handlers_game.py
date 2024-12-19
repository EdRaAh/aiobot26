import os
import random
from confa import logger, users, ATTEMPTS, get_random_letter, alphabet, bot
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InputFile
router: Router = Router()


images_folder: str = 'cats'  # путь к папке с фото


if not os.path.exists(images_folder) or not os.listdir(images_folder):
    raise FileNotFoundError(f"The folder '{images_folder}' does not exist or is empty.")
images = os.listdir(images_folder)

async def send_image(chat_id:int, caption:str):
    try:
        random_image = random.choice(images)
        image_path = os.path.join(images_folder, random_image) #полный путь
        photo = InputFile(file = image_path)
        #with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id, photo=photo, caption=caption)

    except Exception as e:
        logger.error('Failed to send photo: %s', str(e))

@router.message(Command(commands=['start', 'START']))
async def start(message: Message):
    logger.info("User %s started the bot.", message.from_user.id)
<<<<<<<<< Temporary merge branch 1
    await message.answer(
    'I am online! Я в сети!\n Чтобы сыграть в игру напиши "играть"\nУзнать правила отправь команду /help')

=========
    chat_id = message.chat.id
    response_text = 'I am online! Я в сети!\n Чтобы сыграть в игру напиши "играть"\nУзнать правила отправь команду /help'
    await message.send_image(chat_id, response_text)
>>>>>>>>> Temporary merge branch 2
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_letter': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }


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


# Этот хендлер будет срабатывать на согласие пользователя сыграть в игру
@router.message(lambda x: x.text.lower() in ['да', 'давай', 'yes', 'играть', 'ok', 'хорошо'])
async def process_positive_answer(message: Message):
    logger.info("User %s agreed to play.", message.from_user.id)
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_letter'] = get_random_letter()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer('Ура!\n\nЯ загадал букву, попробуйте угадать ее в этом ряду -ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        #await send_image(message.chat.id, response_text)
    else:
        await message.answer(
            'Пока мы играем в игру я могу реагировать на команды /cancel и /stat'
        )


# Этот хендлер будет срабатывать на отказ пользователя сыграть в игру
@router.message(lambda x: x.text.lower() in ['нет', 'no', 'не хочу', 'не буду'])
async def process_negative_answer(message: Message):
    logger.info("User %s refused to play.", message.from_user.id)
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, пожалуйста, англ. букву'
        )


# Этот хендлер будет срабатывать на отправку пользователем буквы от a-z
@router.message(lambda x: x.text and any('A' <= char <= 'Z' or 'a' <= char <= 'z' for char in x.text))
async def process_letter_answer(message: Message):
    logger.info("User %s sent a letter: %s", message.from_user.id, message.text)
    guess = message.text.strip().lower()

    if users[message.from_user.id]['in_game']:
        if guess == users[message.from_user.id]['secret_letter']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали букву! Yay! You guessed the letter!\n\n'
                'Хотите еще раз? Do you want to do it again?'
                'Если нет, пишите "нет" If not, write "no"'
            )

        else:
            users[message.from_user.id]['attempts'] -= 1

            if users[message.from_user.id]['attempts'] > 0:
                try:
                    guess_index = alphabet.index(guess)
                    secret_index = alphabet.index(users[message.from_user.id]['secret_letter'])
                except ValueError as e:
                    logger.error("Failed to find index of letter '%s'. Error: %s", guess, e)
                    await message.answer("Произошла ошибка при обработке вашей буквы.")
                    return

                if guess_index < secret_index:
                    hint = (
                        f"Неправильно, загаданная буква правее в алфавитном ряду ABCDEFGHIJKLMNOPQRSTUVWXYZ, попробуйте ещё раз.\n"
                        f"Incorrect, the mystery letter is to the right in alphabetical order ABCDEFGHIJKLMLMNOPQRSTUVWXYZ, try again.")
                else:
                    hint = (
                        f"Неправильно, загаданная буква левее в алфавитном ряду ABCDEFGHIJKLMNOPQRSTUVWXYZ, попробуйте ещё раз.\n"
                        f"Incorrect, the mystery letter is to the left in the alphabetical order ABCDEFGHIJKLMLMNOPQRSTUVWXYZ, try again.")

                await message.answer(hint)
            else:
                await message.answer(f"К сожалению, у вас закончились попытки.\n"
                                     f" Загаданная буква была {users[message.from_user.id]['secret_letter'].upper()}.\n"
                                     f"Unfortunately, you have run out of attempts. The target letter was {users[message.from_user.id]['secret_letter'].upper()}"
                                     f"Сыграем еще? Play again?")
                users[message.from_user.id]['in_game'] = False
