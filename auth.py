from flask import Flask, jsonify, Response, request

from os import getenv
from oidc_provider import OIDCProvider

oidc_provider = OIDCProvider(
    client_id=getenv('AUTH_CLIENT_ID'),
    client_secret=getenv('AUTH_CLIENT_SECRET'),
    auth_uri=getenv('AUTH_PROVIDER_URI')
)

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