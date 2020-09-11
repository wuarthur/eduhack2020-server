import mongo_database
from mongo_database import *
from gevent.pywsgi import WSGIServer
import sys
from flask import Flask, jsonify, request
import ssl
from decorators import  *


app = Flask(__name__)

BOOL_SWITCH={'true':True,
             True: True,
             'false':False,
             False: False}

TYPES = {'total':'names',
         'crack-detected':'crack-detected'}


@app.route('/')
@exception_handler
def index():
    return ('HEY!, please try calling again with one of the following path \n'
            '/teacher POST \n'
            '/student POST \n'
            '/class POST \n')


@app.route('/student', methods=['POST'])
@exception_handler
def add_student():
    try:
        request_body = request.form.to_dict()
        id = request_body.pop('student-id')
        name = request_body.pop('name')
        courses = request_body.pop('courses')
        mongo_database.add_student(id, name, courses, **request_body)
    except ValueError:
        raise MissingBody
    except KeyError:
        raise MissingBody
    return jsonify({"success": True, "status": 200}, 200)

@app.route('/teacher', methods=['POST'])
@exception_handler
def add_teacher():
    try:
        request_body = request.form.to_dict()
        id = request_body.pop('teacher-id')
        name = request_body.pop('name')
        courses = request_body.pop('courses')
        mongo_database.add_teacher(id, name, courses, **request_body)
    except ValueError:
        raise MissingBody
    except KeyError:
        raise MissingBody
    return jsonify({"success": True, "status": 200}, 200)

@app.route('/class', methods=['POST'])
@exception_handler
def add_class():
    try:
        request_body = request.form.to_dict()
        id = request_body.pop('class-id')
        name = request_body.pop('course-name')
        courses = request_body.pop('year-offered')
        students = request_body.pop('students')
        number_lecture = request_body.pop('number-of-lectures')
        mongo_database.add_class(id, name, courses, students, number_lecture, **request_body)
    except ValueError:
        raise MissingBody
    except KeyError:
        raise MissingBody
    return jsonify({"success": True, "status": 200}, 200)

@app.route('/teacher', methods=['GET'])
@exception_handler
def search_teacher():
    request_body = request.form.to_dict()
    teachers = mongo_database.get_teachers(**request_body)
    response = {'results': teachers}
    print(response)
    return jsonify(response, 200)

@app.route('/student', methods=['GET'])
@exception_handler
def search_student():
    request_body = request.form.to_dict()
    teachers = mongo_database.get_student(**request_body)
    response = {'results': teachers}
    print(response)
    return jsonify(response, 200)


@app.route('/class/<id>', methods=['POST'])
@exception_handler
def update_class(id):
    request_body = request.form.to_dict()
    updated_doc = mongo_database.update_class(id, **request_body)
    return jsonify({"success": True, "updated_doc": updated_doc}, 200)

@app.route('/student/<id>', methods=['POST'])
@exception_handler
def update_student(id):
    request_body = request.form.to_dict()
    updated_doc = mongo_database.update_class(id, **request_body)
    return jsonify({"success": True, "updated_doc": updated_doc}, 200)

@app.route('/teacher/<id>', methods=['POST'])
@exception_handler
def update_teacher(id):
    request_body = request.form.to_dict()
    updated_doc = mongo_database.update_class(id, **request_body)
    return jsonify({"success": True, "updated_doc": updated_doc}, 200)


if __name__ == '__main__':
     app.run(host='127.0.0.1',port='1911', debug=True)
     # http_server = WSGIServer(('0.0.0.0', 1911), app)
     # http_server.serve_forever()