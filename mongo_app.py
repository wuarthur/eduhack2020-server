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
            '/summary POST \n'
            '/summary/date GET \n'
            '/summary/date/type GET \n')

@app.route('/summary', methods=['POST'])
@exception_handler
def post_summary():
    try:
        request_body = request.form
        image_name = request_body['image_name']
        scan_time = float(request_body['scantime'])
        is_broken = BOOL_SWITCH[request_body['is_broken']]
        is_crack_detected = BOOL_SWITCH[request_body['is_crack_detected']]
    except ValueError:
        raise MissingHeaders
    except KeyError:
        raise MissingHeaders

    if is_duplicate_image(image_name):
        return jsonify({"response": 'Image already exist'}, 409)

    index_entry = store_day(image_name, is_broken, is_crack_detected, scan_time)
    store_interval(image_name, is_broken, is_crack_detected, scan_time)
    return jsonify({"success": True, "status": 200}, 200)

@app.route('/summary', methods=['GET'])
@exception_handler
def get_summary():
    try:
        from_unix = float(request.args.get('from_unix'))
        to_unix = float(request.args.get('to_unix'))
    except ValueError:
        raise MissingHeaders
    data = get_interval_by_type(from_unix, to_unix, 'total')
    ## type: total, broken, others, crack_detected, broken-not-detected
    total = len(data['broken']) + len(data['broken-not-detected']) + len(data['crack-detected']) + len(data['others'])
    response = {'total': total,
                'broken': {'detected':len(data['broken']),
                           'not_detected':len(data['broken-not-detected'])},
                'crack_detected':len(data['crack-detected'])}
    return jsonify(response, 200)


@app.route('/summary/<date_or_type>', methods=['GET'])
@exception_handler
def get_summery(date_or_type):
    #todo test this not with postman
    types = ['total', 'broken', 'crack-detected', 'others']
    if date_or_type in types:
        ## <type>: [“total”, “broken”, “crack-detected”, “others”]
        try:
            from_unix = float(request.args.get('from_unix'))
            to_unix = float(request.args.get('to_unix'))
        except ValueError:
            raise MissingHeaders
        data = get_interval_by_type(from_unix, to_unix, date_or_type)
        return jsonify(data, 200)
    else: #todo check if is int, if not throw
        try:
            int(date_or_type)
        except ValueError:
            raise InvalidWaferType
        index_entry = get_day(date_or_type)
        del index_entry['_id']
        return jsonify(index_entry, 200)


@app.route('/summary/<date>/<type>', methods=['GET'])
@exception_handler
def get_summery_by_type(date,type):
    #returns empty entry if none are stored
    index_entry = get_day(date)
    if type in TYPES:
        key = TYPES[type]
        data = {type:index_entry[key]}
    elif type == 'broken':
        data = {'broken_detected': index_entry['broken-detected'],
                'broken_not_detected':index_entry['broken-not-detected']}
    else:
        return jsonify({"Error": 'invalid type, use broken, total, or crack-detected'}, 422)
    return jsonify(data, 200)

if __name__ == '__main__':
     # app.run(host='127.0.0.1',port='1991', debug=True)
     http_server = WSGIServer(('0.0.0.0', 1991), app)
     http_server.serve_forever()