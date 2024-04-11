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
from pyrogram.enums import ParseMode, ClientPlatform
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
            workers=int(get_config("UG_TG_WS", 10)),
            max_concurrent_transmissions=int(get_config("UG_TG_MCTS", 4))
            no_updates=True,
            device_model="Samsung SM-G998B",
            app_version="8.4.1 (2522)",
            system_version="SDK 31",
            lang_pack="",
            lang_code="en",
            system_lang_code="en",
            max_message_cache_size=int(get_config("UG_TG_MMC", 0)),
            max_business_user_connection_cache_size=int(get_config("UG_TG_MBUC", 0)),
            client_platform=ClientPlatform.ANDROID
        )

    async def start(self):
        await super().start()
        print(
            f"{self.me} based on Pyrogram v{__version__} started."
        )

    async def stop(self, *args):
        usr_bot_me = self.me
        await super().stop()
        print(f"{usr_bot_me} stopped. Bye.")
