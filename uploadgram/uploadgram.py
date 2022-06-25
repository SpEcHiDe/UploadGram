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
from pyrogram.enums import ParseMode
from .get_config import get_config


class Uploadgram(Client):
    """ modded client """

    def __init__(self):
        super().__init__(
            name="UploadGram",
            api_id=int(get_config("UG_TG_APP_ID")),
            api_hash=get_config("UG_TG_API_HASH"),
            parse_mode=ParseMode.HTML,
            sleep_threshold=int(get_config("UG_TG_ST", 10)),
            no_updates=True
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
