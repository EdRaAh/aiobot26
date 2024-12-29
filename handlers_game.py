
import random
import logging
from config import users, ATTEMPTS, alphabet
from aiogram import Router
from aiogram.types import Message

router: Router = Router()
logger = logging.getLogger(__file__)

def get_random_letter() -> str:
    return chr(random.randint(ord('a'), ord('z')))
# Этот хендлер будет срабатывать на согласие пользователя сыграть в игру
@router.message(lambda x: x.text.lower() in ['да', 'давай', 'yes', 'играть', 'ok', 'хорошо'])
async def process_positive_answer(message: Message):
    logger.info("User %s agreed to play.", message.from_user.id)
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_letter'] = get_random_letter()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer('Ура!\n\nЯ загадал букву, попробуйте угадать ее в этом ряду -ABCDEFGHIJKLMNOPQRSTUVWXYZ')
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
@router.message(lambda x: len(x.text) == 1 and any('A' <= char <= 'Z' or 'a' <= char <= 'z' for char in x.text))
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
