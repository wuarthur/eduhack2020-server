import time
from exceptions import *
from flask import Flask, jsonify, request
import traceback

def timer(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        # print ('func:%r args:[%r, %r] took: %2.4f sec' % \
        #   (f.__name__, args, kw, te-ts))
        print ('func:%r took: %2.4f sec' % \
          (f.__name__, te-ts))
        return result
    return timed

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except MissingHeaders:
            traceback.print_exc()
            return jsonify({'Error': 'Missing required header(s) for this request or one of the provided headers contains invalid parameters'}, 404)
        except MissingBody:
            traceback.print_exc()
            return jsonify({'Error': "missing required body data"}, 404)
        except ItemNotFoundException:
            traceback.print_exc()
            return jsonify({'Error': "the document with the search id does not exist in the databse, please create first"}, 404)
        except Exception as e:
            traceback.print_exc()
            return jsonify({'Error': traceback.format_exc().replace('"', "'")}, 404)

    inner_function.__name__ = func.__name__
    return inner_function

@exception_handler
def ttest(sttt):
    sttt = 'as'
    float(sttt)

#ttest(0)


