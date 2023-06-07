import smtplib
import ssl
from todo_app.auth.routers import get_users
from celery import Celery
from todo_app.config import SMTP_USER, SMTP_PASSWORD
from .utils import get_email_template_expirated_tasks
from fastapi import Depends
from celery.schedules import crontab

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

celery = Celery('tasks', broker=f'redis://localhost:6379')

celery.conf.beat_schedule = {
    'Email': {
        'task': 'task_1',
        'schedule': crontab(minute='*/1'),
        # 'kwargs': {'users': get_some()}
    },
}
celery.conf.timezone = 'UTC'


@celery.task(name='task_1')
async def send_email_number_expiration_tasks():
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASSWORD)
        users = await get_users()
        for user in users:
            email = get_email_template_expirated_tasks(user)
            server.send_message(email)
