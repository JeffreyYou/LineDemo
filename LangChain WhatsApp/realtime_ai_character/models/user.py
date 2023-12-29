from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.inspection import inspect
from realtime_ai_character.database.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(String(100))
    user_name = Column(String(100))
    user_gender = Column(String(100))
    is_in_group = Column(Boolean)
    is_open_account = Column(Boolean)
    investment_knowledge = Column(String(100))
    account_agency = Column(String(100))

    def to_dict(self):
        return {
            c.key:
                getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

    def save(self, db):
        db.add(self)
        db.commit()
