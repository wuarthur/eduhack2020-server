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
    'classes': [], #list of id
}

TEACHER_TEMPLATE={
    #required fields, todo maybe support arbitary fields in code
    'teacher-id': None,
    'name': None,
    'classes': [], #list of id
}


CLASS_TEMPLATE={
    #required fields, todo maybe support arbitary fields in code
    'class-id': None,
    'course-name': None,
    'year-offered': None,
    'students': [], #list of student-id
    'student-id':[], #attendence for this student, will have meny of this per class
    'number-of-lectures':None,
}

def add_student(id, name, classes, **kwargs):
    doc={'student-id': id,
         'name': name,
         'classes': classes}
    for key, val in kwargs.items():
        if key not in doc: #avoid overriding required fields
            doc[key] = val
    collection_name = 'Student'
    db[collection_name].insert_one(doc)
    db[collection_name].create_index('name') #sort by name

def update_student():
    pass

def add_class(id, name, year, students, lectures_count, **kwargs):
    doc = {'class-id': id,
            'course-name': name,
            'year-offered': year,
            'students': students, #list of student-id
            'number-of-lectures':lectures_count,}
    for key, val in kwargs.items():
        if key not in doc:  # avoid overriding required fields
            doc[key] = val
    collection_name = 'Courses'
    db[collection_name].insert_one(doc)
    db[collection_name].create_index('course-name')  # sort by name
    db[collection_name].create_index('year-offered')  # sort by name

def update_class():
    #called most often, each time a student signs in need one update
    pass

def update_class_batch():
    #todo: allow client side to send a array of student ids for one class.
    pass

def add_teacher():
    pass

def update_teacher():
    pass