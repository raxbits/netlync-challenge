from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text
from sqlalchemy.sql.expression import null
   
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)
    def __repr__(self):
        return f"<User email={self.email}"
    
class Bookmark(Base):
    __tablename__='bookmarks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, nullable=False)
    url = Column(String(512), nullable=False)
    private = Column(Boolean, default=True)
    def __repr__(self):
        return f"<url={self.url}>"
    
