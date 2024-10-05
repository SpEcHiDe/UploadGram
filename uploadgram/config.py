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
from dotenv import load_dotenv
from .get_config import get_config


BASE_DIR = os.path.expanduser("~/.config/uploadgram/")
OLD_CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")
if os.path.exists(
    OLD_CONFIG_FILE
):
    os.remove(OLD_CONFIG_FILE)
CONFIG_FILE = os.path.join(BASE_DIR, "config.env")
SESSION_FILE = os.path.join(BASE_DIR, "default")
TG_VIDEO_TYPES = (
    "M4V", "MP4", "MOV", "FLV", "WMV", "3GP", "MPEG", "MKV"
)
TG_AUDIO_TYPES = (
    "MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS"
)


def write_default_config():
    """ write the default config.ini file
    """
    if os.path.lexists(CONFIG_FILE):
        return load_dotenv(CONFIG_FILE)
    os.makedirs(BASE_DIR, exist_ok=True)
    print(
        "Go to https://my.telegram.org (or @useTGxBot) "
        "and create a app in API development tools"
    )
    app_id = int(get_config("app_id ", should_prompt=True))
    api_hash = get_config("api_hash ", should_prompt=True)
    with open(CONFIG_FILE, "w") as f:
        f.write(f"UG_TG_APP_ID={app_id}\n")
        f.write(f"UG_TG_API_HASH={api_hash}\n\n")
    return load_dotenv(CONFIG_FILE)


write_default_config()
