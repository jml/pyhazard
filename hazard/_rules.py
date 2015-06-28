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
Information about how to play the game.
"""

from pyrsistent import m, v


CARDS = v(
    'Soldier',
    'Clown',
    'Knight',
    'Priestess',
    'Wizard',
    'General',
    'Minister',
    'Prince',
)


def iter_valid_plays_for_card(card, myself, others):
    """Iterate through a list of valid plays for the given card.

    The plays are only valid within the rules of the game. They don't pay
    attention to the current state. Thus, they might guess that a player has
    the Minister even though it has already been played.

    The order of iteration is irrelevant and not guaranteed to be stable.
    """
    play = m(card=card)
    if card in ('Priestess', 'Minister', 'Prince'):
        yield play
    elif card in ('Wizard',):
        yield play.set('target', myself)
        for target in others:
            yield play.set('target', target)
    elif card in ('Clown', 'Knight', 'General'):
        for target in others:
            yield play.set('target', target)
    else:
        for target in others:
            targeted = play.set('target', target)
            for card in CARDS:
                if card == 'Soldier':
                    continue
                yield targeted.set('guess', card)


def iter_valid_plays(card_one, card_two, myself, others):
    if not is_busting_hand(card_one, card_two):
        for play in iter_valid_plays_for_card(card_one, myself, others):
            yield play
        for play in iter_valid_plays_for_card(card_two, myself, others):
            yield play


def is_busting_hand(card_one, card_two):
    other = _other((card_one, card_two), 'Minister')
    return other in ('Wizard', 'General', 'Prince')


def _other((fst, snd), thing, neither=None):
    if fst == thing:
        return snd
    elif snd == thing:
        return fst
    else:
        return neither
