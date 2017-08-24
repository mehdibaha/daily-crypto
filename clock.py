from apscheduler.schedulers.blocking import BlockingScheduler

from main import do_job

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=8)
def scheduled_job():
    print('This job is run every day at 8am.')
    do_job()

sched.start()
