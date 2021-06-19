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


from pyrogram import Client, __version__
from .config import (
    CONFIG_FILE,
    SESSION_FILE
)


class Uploadgram(Client):
    """ modded client """

    def __init__(self):
        super().__init__(
            session_name=SESSION_FILE,
            config_file=CONFIG_FILE,
            parse_mode="html",
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        print(
            f"@{usr_bot_me.username} based on Pyrogram v{__version__} started."
        )

    async def stop(self, *args):
        await super().stop()
        print("UploadGram stopped. Bye.")
