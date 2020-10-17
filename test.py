import requests
import json



data={
'class-id':'1',
'course-name': 'name1',
'year-offered': 2018,
'students':[],
'number-of-lectures':9

}

requests.post('http://127.0.0.1:1911/class', data=data)


data={
'student-id':1,
'name': 'student1',
'year-offered': 2018,
'courses':['1'],

}
requests.post('http://127.0.0.1:1911/student', data=data)

data={
'student-id':12,
'name': 'student1',
'year-offered': 2018,
'courses':['1'],

}
requests.post('http://127.0.0.1:1911/student', data=data)

data={
'student-id':13,
'name': 'student1',
'year-offered': 2018,
'courses':['1'],

}
requests.post('http://127.0.0.1:1911/student', data=data)


data={
'student-id':13,
'class-id': '1',
'attended': 1,

}
requests.post('http://127.0.0.1:1911/attendance', data=data)