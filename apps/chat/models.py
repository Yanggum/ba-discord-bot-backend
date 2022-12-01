# coding: utf-8
from sqlalchemy import Column, Float, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER, TEXT, TINYTEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CcChar(Base):
    __tablename__ = 'cc_char'

    CHAR_NO = Column(INTEGER(11), primary_key=True, unique=True, comment='캐릭터 넘버')
    CHAR_NAME = Column(VARCHAR(256), comment='캐릭터 이름')
    CHAR_TYPE = Column(CHAR(1), server_default=text("'C'"), comment='C: 캐릭터: U: 유저')
    CHAR_INFO = Column(TEXT, comment='캐릭터 정보')
    UPD_ID = Column(VARCHAR(50), server_default=text("'admin'"))
    UPD_DT = Column(TIMESTAMP)
    REG_ID = Column(VARCHAR(50), server_default=text("'admin'"))
    REG_DT = Column(TIMESTAMP)
    STD_CODE_NAME = Column(VARCHAR(256))
    STD_FULL_NAME = Column(VARCHAR(256))
    STD_INC_ID = Column(VARCHAR(256))
    STD_ID = Column(BIGINT(20))
    STD_TOKEN = Column(VARCHAR(256))
    STD_ROLE = Column(BIGINT(20))
    STD_ERROR_MSG = Column(VARCHAR(256), server_default=text("'사랑해요.'"))
    STD_STATUS = Column(VARCHAR(256), server_default=text("'공부'"))
    THUMBNAIL = Column(String(256, 'utf8mb4_unicode_ci'))
    TEMPERATURE = Column(Float(asdecimal=True), server_default=text("'0.5'"))
    F_PENALTY = Column(Float(asdecimal=True), server_default=text("'0.5'"))
    P_PENALTY = Column(Float(asdecimal=True), server_default=text("'0'"))


class CcCharChat(Base):
    __tablename__ = 'cc_char_chat'

    CHAT_NO = Column(INTEGER(11), primary_key=True, unique=True, comment='채팅 일련번호')
    CHAR_NO = Column(INTEGER(11), nullable=False, comment='캐릭터 일련번호')
    CHAT_ROOM_NO = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    IS_LEARN = Column(CHAR(1), server_default=text("'N'"))
    REG_DT = Column(TIMESTAMP)
    UPD_ID = Column(VARCHAR(50))
    UPD_DT = Column(TIMESTAMP)
    CHAT_CONT = Column(TEXT(), comment='채팅 내용')
    REG_ID = Column(VARCHAR(50), comment='업데이트 ID')


class CcCharChatForLearn(Base):
    __tablename__ = 'cc_char_chat_for_learn'

    CHAT_LEARN_NO = Column(INTEGER(11), primary_key=True, unique=True, comment='학습용 채팅 일련번호')
    CHAT_CONT = Column(TINYTEXT, comment='채팅 내용')
    REG_ID = Column(VARCHAR(50), comment='업데이트 ID')
    REG_DT = Column(TIMESTAMP)
    UPD_ID = Column(VARCHAR(50))
    UPD_DT = Column(TIMESTAMP)
    CHAR_NO = Column(INTEGER(11), nullable=False, comment='캐릭터 일련번호')
    CHAT_ROOM_NO = Column(INTEGER(11), nullable=False, server_default=text("'1'"))


class CcCharChatLog(Base):
    __tablename__ = 'cc_char_chat_log'

    CHAT_LOG_NO = Column(INTEGER(11), primary_key=True, unique=True, comment='채팅 일련번호')
    CHAR_NO = Column(INTEGER(11), nullable=False, comment='캐릭터 일련번호')
    CHAT_ROOM_NO = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    IS_LEARN = Column(CHAR(1), server_default=text("'N'"))
    REG_DT = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    UPD_ID = Column(VARCHAR(50), server_default=text("'admin'"))
    UPD_DT = Column(TIMESTAMP, server_default=text("'0000-00-00 00:00:00'"))
    CHAT_CONT = Column(TEXT, comment='채팅 내용')
    REG_ID = Column(VARCHAR(50), server_default=text("'admin'"), comment='업데이트 ID')


class CcUser(Base):
    __tablename__ = 'cc_user'

    USER_NO = Column(INTEGER(11), primary_key=True, unique=True)
    USER_NAME = Column(VARCHAR(256))
    REG_ID = Column(VARCHAR(50), server_default=text("'admin'"))
    REG_DT = Column(TIMESTAMP)
    UPD_ID = Column(VARCHAR(50), server_default=text("'admin'"))
    UPD_DT = Column(TIMESTAMP)
