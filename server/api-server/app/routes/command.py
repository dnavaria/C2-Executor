from fastapi import APIRouter, Request
from app.database.db import get_db
from fastapi.responses import ORJSONResponse
from fastapi import Depends
from app.controller import CommandController
from pydantic import BaseModel

cmd_controller = CommandController()

router = APIRouter()


class CommandRequest(BaseModel):
    command_text: str = None


@router.get("/", response_class=ORJSONResponse)
async def get_all_recent_commands(request: Request, db=Depends(get_db)):
    # This function will retrieve all commands from the database.
    # will be paginated with a limit of 10 records per page.
    # Get start and end index from the request url query parameters
    try:
        start_index = int(request.query_params.get("start_index", 0))
        end_index = int(request.query_params.get("end_index", 10))
        commands = cmd_controller.get_all_recent_commands(
            db=db,
            start_index=start_index,
            end_index=end_index
        )
        if not commands:
            return ORJSONResponse(
                content={
                    "commands": [],
                    "exception": None,
                    "message": "No commands found"
                },
                status_code=404,
            )

        return ORJSONResponse(
            content={
                "commands": commands,
                "exception": None,
                "message": "Commands retrieved successfully"
            },
            status_code=200,
        )
    except Exception as e:
        print(f"get_all_recent_commands :: error occurred :: {e}")
        return ORJSONResponse(
            content={
                "commands": [],
                "exception": e,
                "message": "Error occurred while retrieving commands"
            },
            status_code=500,
        )


@router.post("/run")
async def run_command(request: CommandRequest, db=Depends(get_db)):
    # This function will create a new command in the database and send it to the Celery worker.
    # Implement database insertion here and call the execute_command function.
    try:
        command_text = request.command_text
        if command_text is None:
            return ORJSONResponse(
                content={
                    "command": None,
                    "exception": "Command text is required",
                    "message": "Error occurred while executing command",
                },
                status_code=500,
            )
        record = cmd_controller.execute_command(command_text=command_text, db=db)
        if record is None:
            return ORJSONResponse(
                content={
                    "command": None,
                    "exception": "Error occurred while sending task to Celery worker",
                    "message": "Error occurred while executing command",
                },
                status_code=500,
            )
        return ORJSONResponse(
            content={
                "command": {
                    "id": record.task_id,
                    "command_text": record.command_text,
                    "status": record.status,
                    "result": record.result,
                    "created_at": record.created_at,
                    "updated_at": record.updated_at,
                },
                "exception": None,
                "message": "Command sent for execution",
            },
            status_code=200,
        )
    except Exception as e:
        print(f"create_command :: error occurred :: {e}")
        return ORJSONResponse(
            content={
                "command": None,
                "exception": e,
                "message": "Error occurred while executing command",
            },
            status_code=500,
        )


@router.get("/results/{command_id}", response_class=ORJSONResponse)
async def get_command_result(command_id: str, db=Depends(get_db)):
    try:
        if command_id is None:
            return ORJSONResponse(
                content={
                    "result": None,
                    "exception": "Command ID is required",
                    "message": "Error occurred while retrieving command result",
                },
                status_code=500,
            )
        result = cmd_controller.get_result(command_id=command_id, db=db)
        if result is None:
            return ORJSONResponse(
                content={
                    "result": None,
                    "exception": "Command result not found",
                    "message": "Command result not found",
                },
                status_code=404,
            )
        return ORJSONResponse(
            content={
                "result": result,
                "exception": None,
                "message": "Command result retrieved successfully",
            },
            status_code=200,
        )
    except Exception as e:
        print(f"get_command_result :: error occurred :: {e}")
        return ORJSONResponse(
            content={
                "result": None,
                "exception": e,
                "message": "Error occurred while retrieving command result",
            },
            status_code=500,
        )
