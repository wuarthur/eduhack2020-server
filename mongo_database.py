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
    'courses': [], #list of id
}

TEACHER_TEMPLATE={
    #required fields, todo maybe support arbitary fields in code
    'teacher-id': None,
    'name': None,
    'courses': [], #list of id
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

def get_teachers(**kwargs):
    collection = db['Teachers']
    query = []
    for key, val in kwargs.items():
        query.append({key:val})

    teachers=[]
    print({"$and": query})
    for post in collection.find({"$and": query}):
        del post['_id']
        teachers.append(post)
    # for posts in collection.find({'height': '190cm'}):
    #     teachers.append(posts)

    return teachers

def add_student(id, name, courses, **kwargs):
    doc={'student-id': id,
         'name': name,
         'courses': courses}
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

def add_teacher(id, name, courses, **kwargs):
    doc = { 'teacher-id': id,
            'name': name,
            'courses': courses, #list of id
         }
    for key, val in kwargs.items():
        if key not in doc:  # avoid overriding required fields
            doc[key] = val
    collection_name = 'Teachers'
    db[collection_name].insert_one(doc)
    db[collection_name].create_index('name')  # sort by name

def update_teacher():
    pass