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
    return pmap(requests.post(users_endpoint, data=json.dumps(data)).json())


def get_user_info(username, password, user_info_endpoint):
    return pmap(
        requests.get(user_info_endpoint, auth=(username, password)).json())
