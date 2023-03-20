from database import Base,engine
from models import Bookmark, User

Base.metadata.create_all(engine)