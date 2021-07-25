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
from time import time
from asyncio import sleep
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import (
    Message
)
from .config import (
    TG_AUDIO_TYPES,
    TG_MAX_FILE_SIZE,
    TG_VIDEO_TYPES
)
from .progress import progress_for_pyrogram
from .take_screen_shot import take_screen_shot


async def upload_dir_contents(
    dir_path: str,
    delete_on_success: bool,
    thumbnail_file: str,
    force_document: bool,
    custom_caption: str,
    bot_sent_message: Message
):
    dir_contents = []
    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            dir_contents.append(dir_path)
        else:
            return False
    else:
        dir_contents = os.listdir(dir_path)
    dir_contents.sort()
    for dir_cntn in dir_contents:
        current_name = os.path.join(
            dir_path,
            dir_cntn
        )

        if os.path.isdir(current_name):
            await upload_dir_contents(
                current_name,
                delete_on_success,
                thumbnail_file,
                force_document,
                custom_caption,
                bot_sent_message
            )

        elif os.stat(current_name).st_size < TG_MAX_FILE_SIZE:
            response_message = await upload_single_file(
                current_name,
                thumbnail_file,
                force_document,
                custom_caption,
                bot_sent_message
            )
            if (
                isinstance(response_message, Message) and
                delete_on_success
            ):
                os.remove(current_name)

        await sleep(10)


async def upload_single_file(
    file_path: str,
    thumbnail_file: str,
    force_document: bool,
    custom_caption: str,
    bot_sent_message: Message
):
    if not os.path.exists(file_path):
        return False
    usr_sent_message = bot_sent_message
    start_time = time()
    b_asen_am_e = os.path.basename(file_path)
    caption_al_desc = (
        f"<code>{b_asen_am_e}</code>"
    )
    if custom_caption:
        caption_al_desc = custom_caption

    if file_path.upper().endswith(TG_VIDEO_TYPES) and not force_document:
        return await upload_as_video(
            usr_sent_message,
            bot_sent_message,
            file_path,
            caption_al_desc,
            thumbnail_file,
            start_time
        )

    elif file_path.upper().endswith(TG_AUDIO_TYPES) and not force_document:
        return await upload_as_audio(
            usr_sent_message,
            bot_sent_message,
            file_path,
            caption_al_desc,
            thumbnail_file,
            start_time
        )

    else:
        return await upload_as_document(
            usr_sent_message,
            bot_sent_message,
            file_path,
            caption_al_desc,
            thumbnail_file,
            start_time
        )


async def upload_as_document(
    usr_sent_message: Message,
    bot_sent_message: Message,
    file_path: str,
    caption_rts: str,
    thumbnail_file: str,
    start_time: int
):

    return await usr_sent_message._client.send_document(
        chat_id=usr_sent_message.chat.id,
        document=file_path,
        caption=caption_rts,
        force_document=True,
        thumb=thumbnail_file,
        progress=progress_for_pyrogram,
        progress_args=(
            bot_sent_message,
            start_time,
            "UpLoading to Telegram",
        )
    )


async def upload_as_video(
    usr_sent_message: Message,
    bot_sent_message: Message,
    file_path: str,
    caption_rts: str,
    thumbnail_file: str,
    start_time: int
):
    try:
        metadata = extractMetadata(createParser(file_path))
        duration = 0
        width = 0
        height = 0
        if metadata and metadata.has("duration"):
            duration = metadata.get("duration").seconds
        thumb_nail_img = await take_screen_shot(
            file_path,
            os.path.dirname(os.path.abspath(file_path)),
            (duration / 2)
        )
    except AssertionError:
        return await upload_as_document(
            usr_sent_message,
            bot_sent_message,
            file_path,
            caption_rts,
            thumbnail_file,
            start_time
        )
    try:
        metadata = extractMetadata(createParser(thumb_nail_img))
        if metadata and metadata.has("width"):
            width = metadata.get("width")
        if metadata and metadata.has("height"):
            height = metadata.get("height")
    except AssertionError:
        pass
    _tmp_m = await usr_sent_message.reply_video(
        video=file_path,
        quote=True,
        thumb=thumb_nail_img if not thumbnail_file else thumbnail_file,
        duration=duration,
        width=width,
        height=height,
        supports_streaming=True,
        caption=caption_rts,
        progress=progress_for_pyrogram,
        progress_args=(
            bot_sent_message,
            start_time,
            "UpLoading to Telegram",
        )
    )
    if (
        thumb_nail_img and
        os.path.exists(thumb_nail_img)
    ):
        os.remove(thumb_nail_img)
    return _tmp_m


async def upload_as_audio(
    usr_sent_message: Message,
    bot_sent_message: Message,
    file_path: str,
    caption_rts: str,
    thumbnail_file: str,
    start_time: int
):
    metadata = extractMetadata(createParser(file_path))
    duration = 0
    title = None
    performer = None
    if metadata:
        # some audio files might cause errors
        # don't fail, and just
        # upload the file with zero (0) duration
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("title"):
            title = metadata.get("title")
        if metadata.has("artist"):
            performer = metadata.get("artist")
        if not performer:
            if metadata.has("author"):
                performer = metadata.get("author")
        if not performer:
            if metadata.has("album"):
                performer = metadata.get("album")

    return await usr_sent_message.reply_audio(
        audio=file_path,
        quote=True,
        caption=caption_rts,
        duration=duration,
        performer=performer,
        title=title,
        thumb=thumbnail_file,
        progress=progress_for_pyrogram,
        progress_args=(
            bot_sent_message,
            start_time,
            "UpLoading to Telegram",
        )
    )
