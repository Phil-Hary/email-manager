from sqlalchemy import create_engine
from models import Base

class DBUtils:
    """
        This class holds core DB util methods
    """
    _engine = None

    @classmethod
    def initialize(cls):
        cls._engine = create_engine("sqlite:///email_manager.db")
        Base.metadata.bind = cls._engine
    
    @classmethod
    def get_engine(cls):
        if not cls._engine:
             cls.initialize()
        
        return cls._engine

