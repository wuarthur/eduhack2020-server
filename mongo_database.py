from pymongo import MongoClient
import pymongo
from pprint import pprint
from datetime import datetime, timedelta
from decorators import timer
from exceptions import *

print('starting db')
mongo_client = MongoClient('mongodb://localhost:27017/',
                           #serverSelectionTimeoutMS=5,
                           # username = 'admin',
                           password = 'password')
#mongo_client.server_info()
db = mongo_client['test']
print('connection to Mongodb made')

def update(collection, id_str, **kwargs):
    collection = db[collection]
    document = collection.find_one({id_str: id})
    if document is None:
        raise ItemNotFoundException
    else:
        for key, val in kwargs.items():
            document[key]=val
        collection.update_one({id_str: id}, {"$set": document}, upsert=False)
    return document

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

def get_student(**kwargs):
    collection = db['Students']
    query = []
    for key, val in kwargs.items():
        query.append({key:val})

    students=[]
    print({"$and": query})
    for post in collection.find({"$and": query}):
        del post['_id']
        students.append(post)
    # for posts in collection.find({'height': '190cm'}):
    #     teachers.append(posts)
    return students

def add_student(id, name, courses, **kwargs):
    doc={'student-id': id,
         'name': name,
         'courses': courses}
    for key, val in kwargs.items():
        if key not in doc: #avoid overriding required fields
            doc[key] = val
    collection_name = 'Students'
    db[collection_name].insert_one(doc)
    db[collection_name].create_index('name') #sort by name


def add_class(id, name, year, students, lectures_count, **kwargs):
    #todo check for duplicate
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

def generate_id():
    collection_name = 'Teachers'

def update_teacher(id, **kwargs):
    return update('Teachers', 'teacher-id', **kwargs)

def update_student(id, **kwargs):
    return update('Students', 'student-id', **kwargs)

def update_class(id, **kwargs):
    return update('Courses', 'class-id', **kwargs)

def take_attendence(class_id, student_id, attended):
    #attended = 0,1
    collection = db['Courses']
    document = collection.find_one({class_id: id})
    if document is None:
        raise ItemNotFoundException
    else:
        #todo check if inplace append works
        attendence = document[student_id].append(attended)
        #document[student_id]=attendence
        collection.update_one({class_id: id}, {"$set": document}, upsert=False)
    return document

