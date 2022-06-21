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
from typing import Union
from .uploadgram import Uploadgram
from .upload import upload_dir_contents


async def upload(
    uploadgram: Uploadgram,
    files: str,
    to: Union[str, int],
    delete_on_success: bool = False,
    thumbnail_file: str = None,
    force_document: bool = False,
    custom_caption: str = None,
    console_progress: bool = False
):
    # sent a message to verify write permission in the "to"
    status_message = await uploadgram.send_message(
        chat_id=to,
        text="."
    )

    # get the max tg file_size that is allowed for this account
    tg_max_file_size = 4194304000 if uploadgram.me.is_premium else 2097152000

    await upload_dir_contents(
        tg_max_file_size,
        files,
        delete_on_success,
        thumbnail_file,
        force_document,
        custom_caption,
        status_message,
        console_progress
    )
    
    await status_message.delete()


async def moin(
    args
):
    uploadgram = Uploadgram()
    await uploadgram.start()

    dest_chat = args.chat_id
    if not dest_chat:
        dest_chat = input(
            "enter chat_id to send the files to: "
        )
    if (
        dest_chat.isnumeric() or
        dest_chat.startswith("-100")
    ):
        dest_chat = int(dest_chat)
    dest_chat = (
        await uploadgram.get_chat(dest_chat)
    ).id

    dir_path = args.dir_path
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
        dest_chat,
        delete_on_success=args.delete_on_success,
        thumbnail_file=args.t,
        force_document=args.fd,
        custom_caption=args.caption,
        console_progress=args.progress
    )
    await uploadgram.stop()


def main():
    import asyncio
    import argparse
    parser = argparse.ArgumentParser(
        prog="UploadGram",
        description="Upload to Telegram, from the Terminal."
    )
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
    parser.add_argument(
        "--delete_on_success",
        nargs="?",
        type=bool,
        help="delete file on successful upload",
        default=False,
        required=False
    )
    parser.add_argument(
        "--fd",
        nargs="?",
        type=bool,
        help="force uploading as documents",
        default=False,
        required=False
    )
    parser.add_argument(
        "--t",
        nargs="?",
        type=str,
        help="thumbnail for the upload",
        default=None,
        required=False
    )
    parser.add_argument(
        "--caption",
        nargs="?",
        type=str,
        help="custom caption for the files, instead of file_name as caption",
        default=None,
        required=False
    )
    parser.add_argument(
        "--progress",
        nargs="?",
        type=bool,
        const=True,
        help="show upload progress in terminal",
        default=False,
        required=False
    )
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(moin(args))


if __name__ == "__main__":
    main()
