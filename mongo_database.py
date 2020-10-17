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
print('clearing db...')
mongo_client.drop_database('test')
db = mongo_client['test']
print('connection to Mongodb made')

def update(collection, id_str, id,  **kwargs):
    collection = db[collection]
    print({id_str: id})
    document = collection.find_one({id_str: id})
    if document is None:
        raise ItemNotFoundException
    else:
        for key, val in kwargs.items():
            document[key]=val
        collection.update_one({id_str: id}, {"$set": document}, upsert=False)
    return document

def get_all(collection):
    collection = db[collection]
    cursor = collection.find({})
    all=[]
    for post in cursor:
        del post['_id']
        all.append(post)
    return all

def get_teachers(**kwargs):
    if len(kwargs) ==0:
        return get_all('Teachers')
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
    if len(kwargs) ==0:
        return get_all('Students')
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

def get_classes(**kwargs):
    if len(kwargs) ==0:
        return get_all('Courses')
    collection = db['Courses']
    query = []
    for key, val in kwargs.items():
        query.append({key:val})

    course=[]
    print({"$and": query})
    for post in collection.find({"$and": query}):
        del post['_id']
        course.append(post)
    # for posts in collection.find({'height': '190cm'}):
    #     teachers.append(posts)
    return course

def get_class(class_id):
    #attended = 0,1
    collection = db['Courses']
    print(class_id)
    document = collection.find_one({"class-id": class_id})
    if document is None:
        raise ItemNotFoundException
    else:
        del document['_id']
        return document

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
    for class_id in courses:
        doc = get_class(class_id)
        # doc[id]=[]
        students = doc['students']
        students.append(id)
        update_class(class_id, students= students)

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
    return update('Teachers', 'teacher-id',id, **kwargs)

def update_student(id, **kwargs):
    return update('Students', 'student-id',id, **kwargs)

def update_class(id, **kwargs):
    return update('Courses', 'class-id', id, **kwargs)

def take_attendence(class_id, student_id, attended):
    #attended = 0,1
    collection = db['Courses']
    document = collection.find_one({'class-id': class_id})
    if document is None:
        raise ItemNotFoundException
    else:
        #todo check if inplace append works
        if student_id not in document:
            document[student_id]=[attended]
        else:
            attendence = document[student_id].append(attended)
            document[student_id]=attendence
        collection.update_one({'class-id': class_id}, {"$set": document}, upsert=False)
        print('ok', document)
    del document['_id']
    return document



