from workers.utils.cel_workers import celery, shared_task, send_mail
from models import Tasks
from datetime import datetime
from sqlalchemy import or_


@shared_task
def add_number(a, b):
    return a + b
