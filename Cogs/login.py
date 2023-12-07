from flask import redirect


def login_cogs(ctx, database):
    to_redirect = database.select('''SELECT fqdn FROM cantina_administration.domain WHERE name="cerbere"''',
                                  number_of_data=1)
    try:
        return redirect('https://'+to_redirect[0]+'/auth/olympe', code=302)
    except TypeError as e:
        return "Un problème lors de l'acquisition de l'url de Cerbere. Si vous venez d'installer Cantina, avez vous installer Cerbere?"
