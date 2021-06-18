#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Copyright (C) 2021 The Authors
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
from .get_config import get_config


BASE_DIR = os.path.expanduser("~/.config/uploadgram/")
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")
SESSION_FILE = os.path.join(BASE_DIR, "default")
TG_MAX_FILE_SIZE = 2097152000


def write_default_config():
    if os.path.lexists(CONFIG_FILE):
        return CONFIG_FILE
    os.makedirs(BASE_DIR, exist_ok=True)
    print(
        "Go to https://my.telegram.org (or @useTGxBot) "
        "and create a app in API development tools"
    )
    api_id = int(get_config("api_id ", should_prompt=True))
    api_hash = get_config("api_hash ", should_prompt=True)
    with open(CONFIG_FILE, "w") as f:
        f.write("[pyrogram]\n")
        f.write(f"api_id = {api_id}\n")
        f.write(f"api_hash = {api_hash}\n\n")
    return CONFIG_FILE


write_default_config()
