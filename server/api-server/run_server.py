from app.app import app
from config import Settings
from app.database.db import Base, engine
import uvicorn

# TODO: Add logging

if __name__ == "__main__":
    # create tables
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=Settings.API_SERVER_HOST, port=Settings.API_SERVER_PORT)
