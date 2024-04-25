import json


def install_module(config_file: dict):
    """
    :param config_file: list
    :return: integer
    """
    if not isinstance(config_file, dict):  # Vérification du paramètre rentré, si pas correcte => exit
        exit('config_file: type error')

    # Vérification de si tout les éléments sont requis sont présent
    check_if_all_items_are_presents(config_file)

    return 0


# Fonction permettant de vérifier si tout les paramètres sont présent dans le fichier de configuration
def check_if_all_items_are_presents(config_file: dict):
    pass


f = open('/Users/matyu/Code/Cantina/Olympe/Example/example-installation.json')
data = json.load(f)

print(install_module(data))
