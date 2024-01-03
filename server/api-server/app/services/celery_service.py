from celery import Celery
from celery.result import AsyncResult
from config.settings import Settings

celery_app = Celery(
    'celery_service',
    broker=Settings.REDIS_URL,
    backend=Settings.REDIS_URL
)

# define queue
celery_app.conf.task_default_queue = Settings.C2_EXECUTOR_QUEUE
celery_app.conf.task_serializer = 'json'
# celery_app.conf.database_engine_options = {'echo': True}
# celery_app.conf.database_table_names = {
#     'task': 'c2_executor_results',
#     'group': 'c2_executor_groupmeta',
# }


def execute_command(command_text: str):
    # This is where you would implement the logic to execute the command.
    # return the task id if successful, else return None
    try:
        result = celery_app.send_task('execute_command', args=(command_text,))
        return result.id
    except Exception as e:
        print(f"execute_command :: error occurred :: {e}")
        return None

