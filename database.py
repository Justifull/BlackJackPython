import json


accounts_json = "accounts.json"


def load():
    with open(accounts_json, 'r') as json_data:
        loaded_data = json.load(json_data)
    return loaded_data


def save(name, password, money):
    with open(accounts_json, 'r') as json_data:
        loaded_data = json.load(json_data)

    loaded_data.update({name: [password, money]})

    with open(accounts_json, 'w') as json_data:
        json.dump(loaded_data, json_data)
