from app.models.command import Command
from app.services.celery_service import execute_command


class CommandController:
    def __init__(self):
        pass

    @staticmethod
    def get_all_recent_commands(db, start_index: int = 0, end_index: int = 10):
        try:
            commands = db.query(Command).order_by(Command.created_at).slice(start_index, end_index).all()
            result_list = []
            for command in commands:
                result_list.append({
                    "task_id": command.task_id,
                    "command_text": command.command_text,
                    "status": command.status,
                    "result": command.result,
                    "created_at": command.created_at,
                    "updated_at": command.updated_at,
                })
            return result_list
        except Exception as e:
            print(f"get_all_recent_commands :: error occurred :: {e}")
            return None

    @staticmethod
    def execute_command(db, command_text: str):
        try:
            # add command to database
            task_id = execute_command(command_text=command_text)
            command = Command(
                task_id=task_id,
                command_text=command_text,
                status="submitted",
                result="",
            )
            db.add(command)
            try:
                db.commit()
                db.refresh(command)
            except Exception as e:
                db.rollback()
                print(f"execute_command :: error occurred :: {e}")
                return None
            return command
        except Exception as e:
            print(f"execute_command :: error occurred :: {e}")
            return None

    @staticmethod
    def get_result(db, command_id: str = None):
        try:
            if command_id is None:
                return None
            query_result = db.query(Command).filter(Command.task_id == command_id).first()
            return {
                "task_id": query_result.task_id,
                "command_text": query_result.command_text,
                "status": query_result.status,
                "result": query_result.result,
                "created_at": query_result.created_at,
                "updated_at": query_result.updated_at,
            }
        except Exception as e:
            print(f"get_command_result :: error occurred :: {e}")
            return None
