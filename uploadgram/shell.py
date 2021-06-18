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
import shutil
from typing import List, Union
from .uploadgram import Uploadgram
from .upload import upload_dir_contents


async def upload(
    uploadgram: Uploadgram,
    files: str,
    to: Union[str, int],
    delete_on_success: bool = False,
    thumbnail_file: str = None
):
    # sent a message to verify write permission in the "to"
    status_message = await uploadgram.send_message(
        chat_id=to,
        text="."
    )
    await upload_dir_contents(files, status_message)
    if delete_on_success:
        shutil.rmtree(files, ignore_errors=True)
    await status_message.delete()


async def moin(
    dest_chat: Union[str, int] = None,
    dir_path: str = None
):
    uploadgram = Uploadgram()
    await uploadgram.start()

    if not dest_chat:
        dest_chat = input(
            "enter chat_id to send the files to: "
        )
        if dest_chat.isnumeric():
            dest_chat = int(dest_chat)
    dest_chat = (
        await uploadgram.get_chat(dest_chat)
    ).id

    if not dir_path:
        dir_path = input(
            "enter path to upload to Telegram: "
        )
    while not os.path.exists(dir_path):
        print(os.listdir("."))
        dir_path = input(
            "please enter valid path to upload to Telegram: "
        )
    dir_path = os.path.abspath(dir_path)

    await upload(
        uploadgram,
        dir_path,
        dest_chat
    )
    await uploadgram.stop()


def niom():
    import asyncio
    import argparse
    parser = argparse.ArgumentParser(description="Upload to Telegram, from the Terminal.")
    parser.add_argument(
        "chat_id",
        type=str,
        help="chat id for this bot to send the message to",
    )
    parser.add_argument(
        "dir_path",
        type=str,
        help="enter path to upload to Telegram",
    )
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(moin(args.chat_id, args.dir_path))


if __name__ == "__main__":
    niom()
