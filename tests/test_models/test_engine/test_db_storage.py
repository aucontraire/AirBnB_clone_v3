#!/usr/bin/python3
'''
    Testing the file_storage module.
'''
import time
import unittest
import sys
from models.engine.db_storage import DBStorage
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models import storage
from console import HBNBCommand
from os import getenv
from io import StringIO
from models.base_model import Base

db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBstorage only")
class TestDBStorage(unittest.TestCase):
    '''
        Testing the DB_Storage class
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Initializing classes
        '''
        cls.dbstorage = DBStorage()
        cls.output = StringIO()
        sys.stdout = cls.output

    @classmethod
    def tearDownClass(cls):
        '''
            delete variables
        '''
        del cls.dbstorage
        del cls.output

    def create(self):
        '''
            Create HBNBCommand()
        '''
        return HBNBCommand()

    def test_new(self):
        '''
            Test DB new
        '''
        new_obj = State(name="California")
        self.assertEqual(new_obj.name, "California")

    def test_dbstorage_user_attr(self):
        '''
            Testing User attributes
        '''
        new = User(email="melissa@hbtn.com", password="hello")
        self.assertTrue(new.email, "melissa@hbtn.com")

    def test_dbstorage_check_method(self):
        '''
            Check methods exists
        '''
        self.assertTrue(hasattr(self.dbstorage, "all"))
        self.assertTrue(hasattr(self.dbstorage, "__init__"))
        self.assertTrue(hasattr(self.dbstorage, "new"))
        self.assertTrue(hasattr(self.dbstorage, "save"))
        self.assertTrue(hasattr(self.dbstorage, "delete"))
        self.assertTrue(hasattr(self.dbstorage, "reload"))
        self.assertTrue(hasattr(self.dbstorage, "get"))
        self.assertTrue(hasattr(self.dbstorage, "count"))

    def test_dbstorage_all(self):
        '''
            Testing all function
        '''
        storage.reload()
        result = storage.all("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        new = User(email="adriel@hbtn.com", password="abc")
        console = self.create()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

    def test_dbstorage_new_save(self):
        '''
           Testing save method
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        save_id = new_state.id
        result = storage.all("State")
        temp_list = []
        for k, v in result.items():
            temp_list.append(k.split('.')[1])
            obj = v
        self.assertTrue(save_id in temp_list)
        self.assertIsInstance(obj, State)

    def test_dbstorage_delete(self):
        '''
            Testing delete method
        '''
        new_user = User(email="haha@hehe.com", password="abc",
                        first_name="Adriel", last_name="Tolentino")
        storage.new(new_user)
        save_id = new_user.id
        key = "User.{}".format(save_id)
        self.assertIsInstance(new_user, User)
        storage.save()
        old_result = storage.all("User")
        del_user_obj = old_result[key]
        storage.delete(del_user_obj)
        new_result = storage.all("User")
        self.assertNotEqual(len(old_result), len(new_result))

    def test_model_storage(self):
        '''
            Test to check if storage is an instance for DBStorage
        '''
        self.assertTrue(isinstance(storage, DBStorage))

    def test_dbstorage_get(self):
        '''
            Testing the get method
        '''
        new_state = State(name="Illinois")
        self.assertIsInstance(new_state, State)
        storage.new(new_state)
        save_id = new_state.id
        storage.save()
        test_state = storage.get("State", save_id)
        self.assertEqual(test_state.id, save_id)

    def test_dbstorage_count_withfilter(self):
        '''
            Testing count method with an optional filter class
        '''
        counts = 0
        storage.reload()
        objs = storage.all('State')
        for obj in objs:
            counts = counts + 1
        total = storage.count('State')
        self.assertEqual(total, counts)
        new_state1 = State(name="Wyoming")
        new_state2 = State(name="Washington")
        storage.new(new_state1)
        storage.new(new_state2)
        storage.save()
        total = storage.count('State')
        self.assertEqual(total, counts + 2)

    def test_dbstorage_count_withoutfilter(self):
        '''
            Testing count method without an optional filter class
        '''
        counts = 0
        storage.reload()
        objs = storage.all("")
        for obj in objs:
            counts = counts + 1
        total = storage.count()
        self.assertEqual(total, counts)
        new_state = State(name="Delaware")
        new_city = City(name="Dover", state_id=new_state.id)
        storage.new(new_state)
        storage.new(new_city)
        storage.save()
        total = storage.count()
        self.assertEqual(total, counts + 2)
