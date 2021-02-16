from flask import Flask, jsonify, Response, request
from functools import wraps
from os import getenv
from oidc_provider import OIDCProvider

oidc_provider = OIDCProvider(
    client_id=getenv('AUTH_CLIENT_ID'),
    client_secret=getenv('AUTH_CLIENT_SECRET'),
    auth_uri=getenv('AUTH_PROVIDER_URI')
)
oidc_provider.refresh_jwks_keys()

def secure_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'missing/invalid token'}), 401
        auth_header_parts = auth_header.split(' ')
        if auth_header_parts[0] != 'Bearer':
            return jsonify({'error': 'missing/invalid token'}), 401
        token = auth_header_parts[1]
        if not oidc_provider.decode_token(token):
            return jsonify({'error': 'missing/invalid token'}), 401
        return f(*args, **kwargs)
    return wrapper


def init_routes(app: Flask):
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Home Route'
        })

    @app.route('/auth', methods = ['POST'])
    def auth():
        if 'code' not in request.form.keys() or 'redirect_uri' not in request.form.keys():
            return jsonify({ 'message': 'missing code or redirect_uri' }), 400
        code = request.form['code']
        redirect_uri = request.form['redirect_uri']
        token = oidc_provider.get_token(code = code, redirect_uri = redirect_uri)
        return jsonify({ 'message': 'Auth endpoint' })
    
    @app.route('/user')
    @secure_route
    def user():
        return jsonify({'message': 'secure user endpoint'})