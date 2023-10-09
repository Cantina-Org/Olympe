from hashlib import new
from os import mkdir
from uuid import uuid3, uuid1
from flask import render_template, url_for
from werkzeug.utils import secure_filename, redirect
from Utils.utils import user_login, make_log
from argon2 import PasswordHasher

ph = PasswordHasher()


def add_user_cogs(ctx, database):
    admin = 0
    admin_and_login = user_login(database, ctx)

    if admin_and_login[0] and admin_and_login[1]:
        if ctx.method == 'GET':
            user_name = database.select('''SELECT user_name FROM cantina_administration.user WHERE token=%s''',
                                        (ctx.cookies.get('userID'),))
            return render_template('admin/add_user.html', user_name=user_name)
        elif ctx.method == 'POST':

            if ctx.form['pword1'] == ctx.form['pword2']:
                data = ctx.form
                new_uuid = str(uuid3(uuid1(), str(uuid1())))
                new_salt = new('sha256').hexdigest()
                try:
                    dir_path = database.select("""SELECT content FROM cantina_administration.config WHERE name = %s""",
                                                ("dir_path",), 1)[0]
                except TypeError:
                    dir_path = None
                try:
                    share_path = database.select("""SELECT content FROM cantina_administration.config WHERE name = %s""",
                                                 ("share_path",), 1)[0]
                except TypeError:
                    share_path = None
                try:
                    for i in data:
                        if i == 'admin':
                            admin = 1
                    if dir_path:
                        work_path = dir_path + '/' + secure_filename(ctx.form['uname'])
                    else:
                        work_path = None
                    database.insert('''INSERT INTO cantina_administration.user(token, user_name, salt, password, 
                            admin, work_Dir) VALUES (%s, %s, %s, %s, %s, %s)''',
                                    (new_uuid, ctx.form['uname'], new_salt,
                                     ph.hash(ctx.form['pword2']),
                                     admin, work_path
                                     ))

                except Exception as error:
                    print(error)
                    make_log('Error', ctx.remote_addr, ctx.cookies.get('userID'), 2, database, str(error))
                    return redirect(url_for('admin_add_user'))

                if dir_path and share_path:
                    mkdir(dir_path + '/' + secure_filename(ctx.form['uname']))
                    mkdir(share_path + '/' + secure_filename(ctx.form['uname']))
                make_log('add_user', ctx.remote_addr, ctx.cookies.get('userID'), 2, database,
                         'Created user token: ' + new_uuid)
                return redirect(url_for('admin_show_user'))
    else:
        make_log('Error', ctx.remote_addr, ctx.cookies.get('userID'), 2, database)
        return redirect(url_for('home'))
