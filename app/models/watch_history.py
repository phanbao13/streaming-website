from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_slug = Column(String, index=True, nullable=False)
    movie_name = Column(String, nullable=False)
    episode_slug = Column(String, nullable=True)  # For series
    episode_name = Column(String, nullable=True)
    progress = Column(Float, default=0.0)  # Watch progress in seconds
    last_watched = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="watch_history")
