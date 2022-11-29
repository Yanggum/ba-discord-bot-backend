from datetime import datetime
from typing import Any

from apps.database import db_engine, db_metadata
from sqlalchemy import Table, Column, String, Integer, DateTime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# chat = Table(
#     "memo",
#     db_metadata,
#     Column("idx", Integer, primary_key=True, autoincrement=True),
#     Column("regdate", DateTime(timezone=True), nullable=False, default=datetime.now),
#     Column("title", String(255), nullable=False),
#     Column("body", String(2048), nullable=False)
# )
class ChatModel:
    def __init__(self):
        self.base = automap_base()
        self.base.prepare(db_engine)

        self.cc_char = self.base.classes.cc_char
        self.cc_char_chat = self.base.classes.cc_char_chat
        self.cc_char_chat_for_learn = self.base.classes.cc_char_chat_for_learn
        self.cc_user = self.base.classes.cc_user

# 테이블 정보로 테이블 생성한다
# memo.metadata.create_all(db_engine)
