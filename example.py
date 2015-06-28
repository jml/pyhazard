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
Simple example client
"""

import random
from pyrsistent import pmap

# TODO: Export from public names.
from hazard._client import (
    get_game_info,
    get_round_info,
    join_game,
    play_turn,
    register_game,
    register_user,
)
from hazard._rules import iter_valid_plays
from hazard._client import _make_credentials


"""
The server running Hazard. https://haverer.jml.io/ in production.
"""
BASE_URL = 'http://localhost:3000'
# TODO: These endpoints ought to be in the library, rather than something that
# users need to know.
USERS_ENDPOINT = BASE_URL + '/users'
GAMES_ENDPOINT = BASE_URL + '/games'


def get_game_endpoint(game):
    # TODO: This also should be in the library.
    return BASE_URL + game['url']


def get_round_endpoint(round_url):
    # TODO: This also should be in the library.
    return BASE_URL + round_url


def player_info(round_info, player_id):
    for info in round_info['players']:
        if info['id'] == player_id:
            return info


def get_status(player):
    if player['active']:
        if player['protected']:
            return ' (protected)'
        else:
            return ''
    else:
        return ' (eliminated)'


def print_round_info(round_info):
    current_player = round_info['currentPlayer']
    print 'Players:'
    for player in round_info['players']:
        status = get_status(player)
        if player['id'] == current_player:
            current = '* '
        else:
            current = '  '
        print '{}{}{}: {}'.format(
            current, player['id'], status, player['discards'])
    print


def choose_play(hand, dealt_card, myself, others):
    valid_plays = list(iter_valid_plays(hand, dealt_card, myself, others))
    try:
        return random.choice(valid_plays)
    except IndexError:
        return None


def play_round(users, round_url):
    while True:
        # Figure out whose turn it is
        round_info = get_round_info(None, round_url)
        print_round_info(round_info)
        current_player_id = round_info.get('currentPlayer', None)
        if not current_player_id:
            return round_info['winners']

        # Play as that person
        current_player = users[current_player_id]
        current_player_creds = _make_credentials(current_player)
        current_player_view = get_round_info(current_player_creds, round_url)

        # Figure out their hand
        dealt_card = current_player_view['dealtCard']
        hand = player_info(current_player_view, current_player_id)['hand']
        others = [
            p['id'] for p in round_info['players']
            if p['id'] != current_player_id]

        # Choose a play at random.
        play = choose_play(dealt_card, hand, current_player_id, others)
        print 'Playing: {}'.format(play)
        response = play_turn(current_player_creds, round_url, play)
        print 'Result: {}'.format(response)


def main():
    # Register two users, 'foo' and 'bar'.
    foo = register_user(USERS_ENDPOINT, 'foo')
    foo_creds = _make_credentials(foo)
    bar = register_user(USERS_ENDPOINT, 'bar')
    bar_creds = _make_credentials(bar)

    users = pmap({
        foo['id']: foo,
        bar['id']: bar,
    })

    # 'foo' creates a 2-player game
    game = register_game(foo_creds, GAMES_ENDPOINT, 2)
    game_url = get_game_endpoint(game)

    # 'bar' joins the game, and the game begins.
    join_game(bar_creds, game_url)
    while True:
        game = get_game_info(None, game_url)
        print 'Game: {}'.format(game)
        if game['state'] != 'in-progress':
            break
        current_round_url = get_round_endpoint(game['currentRound'])
        winners = play_round(users, current_round_url)
        print 'Round over. Winners: {}'.format(winners)
    print 'Game over. Winners: {}'.format(game['winners'])


if __name__ == '__main__':
    main()
