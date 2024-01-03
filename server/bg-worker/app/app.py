from celery import Celery
from celery import current_task
from config.settings import Settings
from app.models import Command
from app.database.db import get_db
from app.command.executor import CommandExecutor
from app.command.builder import CommandBuilder


cmd_executor = CommandExecutor()
cmd_builder = CommandBuilder()

app = Celery(
    'app',
    broker=Settings.REDIS_URL,
    backend=Settings.REDIS_URL
)

app.conf.task_default_queue = Settings.C2_EXECUTOR_QUEUE
# app.conf.database_engine_options = {'echo': True}
# app.conf.database_table_names = {
#     'task': 'c2_executor_results',
#     'group': 'c2_executor_groupmeta',
# }
app.conf.broker_connection_retry_on_startup = True
app.conf.prefetch_multiplier = 4


def update_command_status(task_id: str, status: str, result: str = None):
    session = get_db()
    try:
        record = session.query(Command).filter_by(task_id=task_id).first()
        if record:
            record.status = status
            if result:
                record.result = result
            session.commit()
            session.close()
        return True
    except Exception as e:
        session.rollback()
        session.close()
        print(f"update_command_status :: error occurred :: {e}")
        return False


@app.task(name="execute_command")
def execute_command(command_text: str):
    try:
        # update command status to pending
        update_command_status(task_id=current_task.request.id, status="pending")

        command = cmd_builder.build(command_text=command_text)
        if not command:
            update_command_status(
                task_id=current_task.request.id,
                status="failed",
                result="Invalid command"
            )
            return "failed"

        update_command_status(task_id=current_task.request.id, status="executing")

        result = cmd_executor.execute(command=command)
        if not result:
            update_command_status(task_id=current_task.request.id, status="failed",
                                  result="Error occurred while executing command")
            return "failed"

        update_command_status(task_id=current_task.request.id, status="completed", result=result)
        return "success"
    except Exception as e:
        print(f"execute_command :: error occurred :: {e}")
        update_command_status(task_id=current_task.request.id, status="failed")
        return "failed"
