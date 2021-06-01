# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

from dataclasses import dataclass


@dataclass
class Message:
    filename: str
    filesize: int
    value: bytes or str
