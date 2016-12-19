#coding=utf-8

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def tick():
 print('Tick! The time is: %s' % datetime.now())

def task():
    scheduler = BlockingScheduler()
    scheduler.add_job(tick,'cron', second='*/3', hour='*')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()