# Copyright (c) 2015 Jonathan M. Lange <jml@mumak.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Client library for Hazard.
"""

import json
import requests
from pyrsistent import pmap


def register_user(users_endpoint, username):
    data = {'username': username}
    result = pmap(requests.post(users_endpoint, data=json.dumps(data)).json())
    return result.update(data)


def _make_credentials(registration_data):
    return (registration_data['username'], registration_data['password'])


def get_user_info(credentials, user_info_endpoint):
    return pmap(
        requests.get(
            user_info_endpoint, auth=credentials,
            headers={'Accept': 'application/json'}
        ).json())

# TODO: Handle errors

# TODO: Encode routes in functions, rather than requiring full URLs to be
# passed in.

# TODO: Double check that when we play Clown we actually find out what they've
# got.

def register_game(credentials, game_endpoint, num_players, turn_timeout=3600):
    data = {'numPlayers': num_players, 'turnTimeout': turn_timeout}
    response = requests.post(
        game_endpoint, data=json.dumps(data), auth=credentials)
    result = response.json()
    result['url'] = response.headers['location']
    return pmap(result)


def join_game(credentials, game_endpoint):
    return pmap(requests.post(game_endpoint, data='', auth=credentials).json())


def get_game_info(credentials, game_endpoint):
    return pmap(
        requests.get(
            game_endpoint, auth=credentials,
            headers={'Accept': 'application/json'},
        ).json())


def get_round_info(credentials, round_endpoint):
    return pmap(
        requests.get(
            round_endpoint, auth=credentials,
            headers={'Accept': 'application/json'},
        ).json())


def play_turn(credentials, round_endpoint, play):
    # XXX: Necessary for JSON serialization. Is there a better way?
    play = dict(play.items())
    return pmap(
        requests.post(
            round_endpoint, auth=credentials, data=json.dumps(play)).json())
