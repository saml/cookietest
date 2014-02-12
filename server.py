import argparse
from functools import wraps
from urlparse import urlparse

from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
app = Flask(__name__)

def cors(fun):
    @wraps(fun)
    def decorated_function(*args, **kwargs):
        resp = make_response(fun(*args, **kwargs))
        
        origin_header = request.headers.get('Origin', '*')
        resp.headers['Access-Control-Allow-Origin'] = origin_header
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        
        if request.method == 'OPTIONS':
            resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
            resp.headers['Access-Control-Max-Age'] = '60'

        return resp

    return decorated_function

def set_login_cookie(resp):
    resp.set_cookie('user', 'admin')
    return resp

def set_logout_cookie(resp):
    resp.set_cookie('user','', expires=0)
    return resp

class RedirectLoginLogout(object):
    def __init__(self, path):
        sites_str = request.args.get('sites', '')
        sites = set(x for x in sites_str.split(',') if x)

        visited_str = request.args.get('visited', '')
        visited = set(x for x in visited_str.split(',') if x)
        visited.add(request.host)

        redirect_to = request.args.get('redirect_to')
        
        to_visit = sites - visited
        if len(to_visit) <= 0:
            redirect_to = redirect_to or url_for('index')
        else:
            hostname = to_visit.pop()
            redirect_to = 'http://%s%s?sites=%s&visited=%s&redirect_to=%s' % (hostname, path, sites_str, ','.join(visited), redirect_to)

        self.sites = sites
        self.visited = visited
        self.redirect_to = redirect_to
        


@app.route('/')
@cors
def index():
    return render_template('index.html')

@app.route('/redirectlogin')
@cors
def redirectlogin():
    login_manager = RedirectLoginLogout(url_for('redirectlogin'))
    return set_login_cookie(redirect(login_manager.redirect_to))

@app.route('/redirectlogout')
@cors
def redirectlogout():
    logout_manager = RedirectLoginLogout(url_for('redirectlogout'))
    return set_logout_cookie(redirect(logout_manager.redirect_to))
   

@app.route('/login', methods=['POST'])
@cors
def login():
    return set_login_cookie(jsonify())

@app.route('/logout', methods=['POST'])
@cors
def logout():
    return set_logout_cookie(jsonify())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='port to listen [%(default)s]')
    parser.add_argument('--nodebug', action='store_true', default=False, help='no debug mode? [%(default)s]')
    args = parser.parse_args()
    app.run(debug=not args.nodebug, host='0.0.0.0', port=args.port)
