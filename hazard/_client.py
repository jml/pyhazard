"""
Client library for Hazard.
"""

import json
import requests
from pyrsistent import pmap


def register_user(users_endpoint, username):
    data = {'username': username}
    return pmap(requests.post(users_endpoint, data=json.dumps(data)).json())


def get_user_info(username, password, user_info_endpoint):
    return pmap(requests.get(user_info_endpoint, auth=(username, password)).json())
