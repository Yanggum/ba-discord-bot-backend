-- auto-generated definition
create schema char_chat collate utf8mb4_unicode_ci;

create table cc_char
(
    CHAR_NO       int auto_increment comment '캐릭터 넘버'
        primary key,
    CHAR_NAME     varchar(256) charset utf8                            null comment '캐릭터 이름',
    CHAR_TYPE     char collate utf8_unicode_ci         default 'C'     null comment 'C: 캐릭터: U: 유저',
    CHAR_INFO     text collate utf8_unicode_ci                         null comment '캐릭터 정보',
    UPD_ID        varchar(50) charset utf8             default 'admin' null,
    UPD_DT        timestamp                                            null,
    REG_ID        varchar(50) charset utf8             default 'admin' null,
    REG_DT        timestamp                                            null,
    STD_CODE_NAME varchar(256) collate utf8_unicode_ci                 null,
    STD_FULL_NAME varchar(256) collate utf8_unicode_ci                 null,
    STD_INC_ID    varchar(256) collate utf8_unicode_ci                 null,
    STD_ID        bigint                                               null,
    STD_TOKEN     varchar(256) collate utf8_unicode_ci                 null,
    STD_ROLE      bigint                                               null,
    STD_ERROR_MSG varchar(256) collate utf8_unicode_ci default '사랑해요.' null,
    STD_STATUS    varchar(256) collate utf8_unicode_ci default '공부'    null,
    constraint ch_char_CHAR_NO_uindex
        unique (CHAR_NO)
);

create table cc_char_chat
(
    CHAT_NO      int auto_increment comment '채팅 일련번호'
        primary key,
    CHAR_NO      int              not null comment '캐릭터 일련번호',
    CHAT_ROOM_NO int  default 1   not null,
    IS_LEARN     char default 'N' null,
    REG_DT       timestamp        null,
    UPD_ID       varchar(50)      null,
    UPD_DT       timestamp        null,
    CHAT_CONT    text             null comment '채팅 내용',
    REG_ID       varchar(50)      null comment '업데이트 ID',
    constraint cc_char_chat_CHAT_NO_uindex
        unique (CHAT_NO)
)
    collate = utf8_unicode_ci;

create table cc_char_chat_for_learn
(
    CHAT_LEARN_NO int auto_increment comment '학습용 채팅 일련번호'
        primary key,
    CHAT_CONT     tinytext      null comment '채팅 내용',
    REG_ID        varchar(50)   null comment '업데이트 ID',
    REG_DT        timestamp     null,
    UPD_ID        varchar(50)   null,
    UPD_DT        timestamp     null,
    CHAR_NO       int           not null comment '캐릭터 일련번호',
    CHAT_ROOM_NO  int default 1 not null,
    constraint cc_char_chat_CHAT_LEARN_NO_uindex
        unique (CHAT_LEARN_NO)
)
    collate = utf8_unicode_ci;

create table cc_char_chat_log
(
    CHAT_LOG_NO  int auto_increment comment '채팅 일련번호'
        primary key,
    CHAR_NO      int                                                               not null comment '캐릭터 일련번호',
    CHAT_ROOM_NO int                                 default 1                     not null,
    IS_LEARN     char collate utf8_unicode_ci        default 'N'                   null,
    REG_DT       timestamp                           default CURRENT_TIMESTAMP     null,
    UPD_ID       varchar(50) collate utf8_unicode_ci default 'admin'               null,
    UPD_DT       timestamp                           default '0000-00-00 00:00:00' null,
    CHAT_CONT    text collate utf8_unicode_ci                                      null comment '채팅 내용',
    REG_ID       varchar(50) collate utf8_unicode_ci default 'admin'               null comment '업데이트 ID',
    constraint cc_char_chat_CHAT_NO_uindex
        unique (CHAT_LOG_NO)
);

create table cc_user
(
    USER_NO   int auto_increment
        primary key,
    USER_NAME varchar(256) charset utf8                null,
    REG_ID    varchar(50) charset utf8 default 'admin' null,
    REG_DT    timestamp                                null,
    UPD_ID    varchar(50) charset utf8 default 'admin' null,
    UPD_DT    timestamp                                null,
    constraint cc_user_USER_NO_uindex
        unique (USER_NO)
);

