from os import walk
from subprocess import check_output
from flask import render_template, redirect, url_for
from Utils.utils import user_login, make_log


def home_admin_cogs(ctx, database,):
    count = 0
    admin_and_login = user_login(database, ctx)
    if admin_and_login[0] and admin_and_login[1]:
        user_name = database.select('''SELECT user_name FROM cantina_administration.user WHERE token=%s''',
                                    (ctx.cookies.get('userID'),))
        return render_template('admin/home.html', data=user_name, file_number=count)
    else:
        make_log('login_error', ctx.remote_addr, ctx.cookies.get('userID'), 2, database)
        return redirect(url_for('home'))
