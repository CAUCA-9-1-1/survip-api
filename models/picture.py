from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BLOB, DateTime, Boolean

Base = declarative_base()


class Picture(Base):
    __tablename__ = "tbl_picture"

    id_picture = Column(String(36), primary_key=True)
    picture = Column(BLOB)
    created_on = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    def __init__(self, picture, id_picture):
        self.id_picture = id_picture
        self.picture = picture