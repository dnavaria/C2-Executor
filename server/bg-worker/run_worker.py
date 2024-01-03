from app import app
from config import Settings


if __name__ == "__main__":
    # run celery worker in solo mode with queue name "c2_executor" and concurrency of 1
    # celery -A app.app worker -l info -Q c2_worker -c 1
    app.worker_main(
        [
            "worker",
            "-l", "info",
            "-Q", Settings.C2_EXECUTOR_QUEUE,
            "-c", Settings.WORKER_CONCURRENCY,
            "-n", Settings.WORKER_NAME,
            "-P", Settings.WORKER_POOL,
            "-Ofair",
        ]
    )
