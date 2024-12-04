from flask import make_response, redirect, url_for

def sso_logout_cogs():
    response = make_response(redirect(url_for('sso_login')))

    response.set_cookie('token', "")
    response.set_cookie('validation', "")

    return response