from celery.schedules import crontab


imports = ("workers.cron_jobs.jobs", "workers.background_tasks")
result_expires = 30
timezone = "UTC"

accept_content = ["json", "msgpack", "yaml"]
task_serializer = "json"
result_serializer = "json"
broker_connection_retry_on_startup = True

# beat_schedule = {
#     "check_task": {
#         "task": "celery_config.cron_job.jobs.check_pending_tasks",
#         "schedule": crontab(minute=28, hour=20),
#     },
#     "update_expired_task": {
#         "task": "celery_config.cron_job.jobs.update_expired_tasks",
#         "schedule": crontab(minute=30, hour=00),
#     },
# }
