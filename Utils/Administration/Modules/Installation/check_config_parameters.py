# Fonction permettant de vérifier si tout les paramètres sont présent dans le fichier de configuration
def check_config_parameters(config_file: dict):
    # Vérification des éléments globaux
    if "name" not in config_file:
        exit("parameter missing: 'name' is not defined")

    if "url-repo" not in config_file:
        exit("parameter missing: 'url-repo' is not defined")

    if "guidelines" not in config_file:
        exit("parameter missing: 'guidelines' is not defined")

    if "beta" not in config_file:
        exit("parameter missing: 'beta' is not defined")

    if "configuration" not in config_file:
        exit("parameter missing: 'config' is not defined")

    # Vérification des éléments présents dans 'configuration'
    if "html-input" not in config_file['configuration']:
        exit("parameter missing: 'html-input' is not defined in 'configuration'")

    if "database" not in config_file['configuration']:
        exit("parameter missing: 'database' is not defined in 'configuration'")

    if "global" not in config_file['configuration']:
        exit("parameter missing: 'global' is not defined in 'configuration'")

    # Vérification des éléments présent dans 'configuration/database'
    if "connection" not in config_file['configuration']['database']:
        exit("parameter missing: 'global' is not defined in 'configuration/database'")

    if "table" not in config_file['configuration']['database']:
        exit("parameter missing: 'table' is not defined in 'configuration/database'")

    # Vérification des éléments présent dans 'configuration/database/connection'
    if "url" not in config_file['configuration']['database']['connection']:
        exit("parameter missing: 'url' is not defined in 'configuration/database/connection'")

    if "port" not in config_file['configuration']['database']['connection']:
        exit("parameter missing: 'port' is not defined in 'configuration/database/connection'")

    if "username" not in config_file['configuration']['database']['connection']:
        exit("parameter missing: 'username' is not defined in 'configuration/database/connection'")

    if "password" not in config_file['configuration']['database']['connection']:
        exit("parameter missing: 'password' is not defined in 'configuration/database/connection'")

    # Vérification des éléments présent dans 'configuration/global'
    if "url" not in config_file['configuration']['global']:
        exit("parameter missing: 'url' is not defined in 'configuration/global'")

    if "installation" not in config_file['configuration']['global']:
        exit("parameter missing: 'installation' is not defined in 'configuration/global'")

    # Vérification des éléments présent dans 'configuration/global/installation'
    if "ssh-url" not in config_file['configuration']['global']['installation']:
        exit("parameter missing: 'ssh-url' is not defined in 'configuration/global'")

    if "ssh-port" not in config_file['configuration']['global']['installation']:
        exit("parameter missing: 'ssh-port' is not defined in 'configuration/global'")

    if "ssh-username" not in config_file['configuration']['global']['installation']:
        exit("parameter missing: 'ssh-username' is not defined in 'configuration/global'")

    if "ssh-password" not in config_file['configuration']['global']['installation']:
        exit("parameter missing: 'ssh-password' is not defined in 'configuration/global'")

    if "path-to-clone" not in config_file['configuration']['global']['installation']:
        exit("parameter missing: 'path-to-clone' is not defined in 'configuration/global'")

    if "auto-restart" not in config_file['configuration']['global']['installation']:
        exit("parameter missing: 'auto-restart' is not defined in 'configuration/global'")
