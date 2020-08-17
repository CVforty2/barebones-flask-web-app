import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

# Fill in with your own id and secret
client_id = ''
client_secret = ''

google_bp = make_google_blueprint(client_id=client_id, client_secret=client_secret,
                                offline=True, scope=['profile', 'email'])

@google_bp.route('/')
def google_login():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    return render_template('welcome_user.html')
