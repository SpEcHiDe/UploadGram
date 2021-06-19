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

""" progress helper """


import math
from asyncio import sleep
from pyrogram.errors import (
    FloodWait
)
from pyrogram.types import (
    Message
)
from time import time
from .humanbytes import humanbytes
from .time_formatter import time_formatter


async def progress_for_pyrogram(
    current: int,
    total: int,
    message: Message,
    sfw: int,
    ud_type: str
):
    now = time()
    diff = now - sfw
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        try:
            percentage = current * 100 / total
        except ZeroDivisionError:
            percentage = 0
        elapsed_time = round(diff)
        if elapsed_time == 0:
            return
        speed = current / elapsed_time
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = time_formatter(elapsed_time)
        estimated_total_time = time_formatter(estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            "".join(["█" for _ in range(math.floor(percentage / 5))]),
            "".join(["░" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 seconds"
        )
        try:
            await message.edit_text(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except FloodWait as e:
            await sleep(e.x)
        except:  # noqa: E722
            pass
