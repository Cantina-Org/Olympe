from flask import redirect, url_for


def home_cogs(ctx, database):
    return redirect(url_for('my_account'))
