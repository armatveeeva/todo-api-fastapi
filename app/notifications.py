import logging

logger = logging.getLogger(__name__)

async def send_notification(todo_title: str) -> bool:
    logger.info(f"Отправка уведомления для задачи: '{todo_title}'")
    return True
