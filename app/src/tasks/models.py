from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.src.utils.db import Base


class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255))
    is_completed = Column(Boolean, default=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # relationship back to user
    user = relationship("User", back_populates="tasks")

    @property
    def get_title_user_id(self):
        return f"{self.title}_{self.user_id}"
