from sqlalchemy import Column, Integer, Text
from app.database.db import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class Command(Base):
    __tablename__ = "c2_executor"

    task_id = Column(Text, primary_key=True, index=True)
    command_text = Column(Text, index=True)
    status = Column(Text, index=True)
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())