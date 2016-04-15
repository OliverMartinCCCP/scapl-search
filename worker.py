import os
import sys
from celery import Celery 
from celery.utils.log import get_task_logger

app = Celery('scapl-search')
app.config_from_object('celeryconfig')
logger = get_task_logger(__name__)

if __name__ == "__main__":
    app.start()
