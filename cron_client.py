from crontab import CronTab
import uuid


# job.hour.on(2)     # Set to * 2 * * *
# job.setall(2, 10, '2-4', '*/2', None)
# job.setall('2 10 * * *')
# job.setall(time(10, 2))
# job.setall(date(2000, 4, 2))
# job.setall(datetime(2000, 4, 2, 10, 2))
def add_cron_job(command: str):
    job_id = str(uuid.uuid4())
    with CronTab(user=True) as cron:
        job = cron.new(command=command, comment=job_id)
        job.minute.every(1)

    return job_id

def find_job_by_comment(comment:str):
    with CronTab(user=True) as cron:
        iter = cron.find_comment(comment)
        for it in iter:
            print(it)

job_id = add_cron_job("echo dan")
print(job_id)
find_job_by_comment(job_id)
