# schema.py

from datetime import datetime
from pydantic import BaseModel
from apps.database import db_engine, db_metadata
from sqlalchemy.ext.automap import automap_base


# Pydantic을 이용한 Type Hinting
class ChatCreate(BaseModel):
    regdate : datetime
    title : str
    body : str


class CharChatCreate(BaseModel):
    charNo : int
    chatRoomNo : int
    regId : str
    regDt : str
    updId : str
    updDt : str
    chatCont : str

# Base = automap_base()
# Base.prepare(db_engine)
#
# req_cc_char                 = Base.classes.cc_char
# req_cc_char_chat            = Base.classes.cc_char_chat
# req_cc_char_chat_for_learn  = Base.classes.cc_char_chat_for_learn
# req_cc_user                 = Base.classes.cc_user
