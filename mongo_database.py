from pymongo import MongoClient
import pymongo
from pprint import pprint
from datetime import datetime, timedelta
from decorators import timer

print('starting db')
mongo_client = MongoClient('mongodb://localhost:27017/',
                           #serverSelectionTimeoutMS=5,
                           # username = 'admin',
                           password = 'password')
#mongo_client.server_info()
db = mongo_client['test']
print('connection to Mongodb made')

STUDENT_TEMPLATE={
    #required fields, todo maybe support arbitary fields in code
    'student-id': None,
    'name': None,
    'classes': [],
}

TEACHER_TEMPLATE={
    #required fields, todo maybe support arbitary fields in code
    'teacher-id': None,
    'name': None,
    'classes': [],
}

CLASS_TEMPLATE={
    #required fields, todo maybe support arbitary fields in code
    'class-id': None,
    'course-name': None,
    'year-offered': None,
    'students': [],
    'student-id':[], #attendence for this student
    'number-of-lectures':None,
}
