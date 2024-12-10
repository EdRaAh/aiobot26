
from aiogram.types import Message
from aiogram import Router, F
from confa import logger
router: Router = Router()

photo_ids: list = []  # Список для хранения photo_id
@router.message(F.photo)
async def handler_photo(message: Message):
    logger.info(f"получено фото: {message.photo[-1].file_id}")
    photo_ids.append(message.photo[-1].file_id)
