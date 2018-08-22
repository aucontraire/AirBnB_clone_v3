#!/usr/bin/python3
'''
    Define class DatabaseStorage
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base
from sqlalchemy.orm.exc import MultipleResultsFound


class DBStorage:
    '''
        Create SQLalchemy database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Create engine and link to MySQL databse (hbnb_dev, hbnb_dev_db)
        '''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Query current database session
        '''
        db_dict = {}

        if cls != "":
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dict[key] = obj
            return db_dict

    def new(self, obj):
        '''
            Add object to current database session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            Commit all changes of current database session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Delete from current database session
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            Commit all changes of current database session
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Remove private session attribute
        '''
        self.__session.close()

    def get(self, cls, id):
        """
            Method to retrieve one object from db
            Args:
                cls (str): string representation of class to query
                id (str): id of object
            Returns:
                object that matches query otherwise None
        """
        if cls not in models.classes.keys():
            return None

        cls = models.classes[cls]

        try:
            return self.__session.query(cls).filter_by(id=id).one_or_none()
        except MultipleResultsFound:
            return None

    def count(self, cls=None):
        """
            Returns the number of objects in storage matching the given class
        """
        if cls == None:
            return len(models.storage.all().values())
        elif cls not in models.classes.keys():
            return 0
        else:
            return len(models.storage.all(cls).values())
